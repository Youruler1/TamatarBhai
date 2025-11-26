"""
Service manager for handling external API integrations with fallbacks.

Robust loading strategy:
 - Searches for model_routes.json in sensible locations (cwd, parent dirs, service dir).
 - Honors MODEL_ROUTES_PATH env var if set.
 - If model_routes.json missing, falls back to environment variables to initialize services.
 - Supports GPT-OSS style OpenAI config: model, api_key_env, base_url/base_url_env, stream.
"""

import os
import logging
from typing import Optional, Dict, Any
import json
from pathlib import Path
from .openai_service import OpenAIService
from .stability_service import StabilityAIService
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class ServiceManager:
    """Manages external API services with fallback mechanisms"""

    def __init__(self):
        self.openai_service: Optional[OpenAIService] = None
        self.stability_service: Optional[StabilityAIService] = None
        self.model_routes = self._load_model_routes()
        self._initialize_services()

    def _guess_model_routes_paths(self):
        """Yield candidate paths to find model_routes.json"""
        # 1) explicit env var
        env_path = os.getenv("MODEL_ROUTES_PATH")
        if env_path:
            yield Path(env_path)

        # 2) current working directory
        yield Path(os.getcwd()) / "model_routes.json"

        # 3) directory relative to this file (services/)
        here = Path(__file__).resolve().parent  # services dir
        yield here / "model_routes.json"
        # parent of services -> backend/
        yield here.parent / "model_routes.json"
        # two levels up (project root)
        yield here.parent.parent / "model_routes.json"

    def _load_model_routes(self) -> Dict[str, Any]:
        """Load model routing configuration from JSON (robust search)."""
        for candidate in self._guess_model_routes_paths():
            try:
                if candidate and candidate.exists():
                    with open(candidate, "r", encoding="utf-8") as f:
                        routes = json.load(f)
                        logger.info(f"✅ Model routes configuration loaded from {candidate}")
                        return routes
            except Exception as e:
                logger.warning(f"Failed to read model_routes.json at {candidate}: {e}")

        logger.warning("⚠️ model_routes.json not found in standard locations; falling back to environment variables")
        return {}

    def _initialize_services(self):
        """Initialize external API services (falling back to env vars if model_routes missing)."""
        try:
            # ----- OpenAI / caption service init (supports GPT-OSS style) -----
            openai_route = self.model_routes.get("caption", {}) or {}
            openai_config = openai_route.get("external_config", {}) or {}

            # Prefer config values from model_routes.json, but fall back to environment variables.
            api_key_env = openai_config.get("api_key_env", "OPENAI_API_KEY")
            api_key = os.getenv(api_key_env) or os.getenv("OPENAI_API_KEY")

            # model id (default to GPT-OSS style model id)
            model = openai_config.get("model") or os.getenv("OPENAI_MODEL") or "openai/gpt-oss-120b"

            # optional base_url in config OR via env var name in config OR via OPENAI_BASE_URL
            base_url = None
            # config may supply a literal base_url
            if openai_config.get("base_url"):
                base_url = openai_config.get("base_url")
            # or config may specify an env var name that contains base_url
            elif openai_config.get("base_url_env"):
                base_url = os.getenv(openai_config.get("base_url_env"))
            # or fall back to OPENAI_BASE_URL env var
            else:
                base_url = os.getenv("OPENAI_BASE_URL")

            # streaming flag (optional boolean in config or env var)
            stream_flag = False
            if "stream" in openai_config:
                stream_flag = bool(openai_config.get("stream"))
            else:
                stream_env = os.getenv("OPENAI_STREAM")
                if stream_env is not None:
                    stream_flag = stream_env.lower() in ("1", "true", "yes")

            # Initialize OpenAIService even if model_routes.json was missing, using env vars/defaults
            self.openai_service = OpenAIService(
                api_key=api_key,
                model=model,
                base_url=base_url,
                stream=stream_flag
            )

            # ----- StabilityAI / image service init (unchanged) -----
            stability_route = self.model_routes.get("image", {}) or {}
            stability_config = stability_route.get("external_config", {}) or {}

            stability_api_key_env = stability_config.get("api_key_env", "STABILITY_KEY")
            stability_api_key = os.getenv(stability_api_key_env) or os.getenv("STABILITY_KEY")

            engine = stability_config.get("engine") or os.getenv("STABILITY_ENGINE") or "stable-diffusion-2"

            self.stability_service = StabilityAIService(
                api_key=stability_api_key,
                engine=engine
            )

            logger.info("✅ All services initialized (OpenAI/Stability).")
        except Exception as e:
            logger.error(f"❌ Service initialization failed: {e}")

    async def generate_bhai_caption(self, dish: str, calories: int) -> str:
        """Generate bhai-style caption with fallback"""
        try:
            if self.openai_service:
                return await self.openai_service.generate_bhai_caption(dish, calories)
            else:
                return self._fallback_bhai_caption(dish, calories)
        except Exception as e:
            logger.error(f"❌ Bhai caption generation failed: {e}")
            return self._fallback_bhai_caption(dish, calories)

    async def generate_formal_caption(self, dish: str, calories: int) -> str:
        """Generate formal caption with fallback"""
        try:
            if self.openai_service:
                return await self.openai_service.generate_formal_caption(dish, calories)
            else:
                return self._fallback_formal_caption(dish, calories)
        except Exception as e:
            logger.error(f"❌ Formal caption generation failed: {e}")
            return self._fallback_formal_caption(dish, calories)

    async def generate_dish_image(self, dish: str) -> str:
        """Generate dish image with fallback"""
        try:
            if self.stability_service:
                image_url = await self.stability_service.generate_dish_image(dish)
                return image_url or "/data/images/default_placeholder.png"
            else:
                return "/data/images/default_placeholder.png"
        except Exception as e:
            logger.error(f"❌ Image generation failed: {e}")
            return "/data/images/default_placeholder.png"

    async def generate_comparison_suggestion(self, dish_a: str, dish_b: str,
                                           calories_a: int, calories_b: int) -> str:
        """Generate comparison suggestion with fallback"""
        try:
            if self.openai_service:
                return await self.openai_service.generate_comparison_suggestion(
                    dish_a, dish_b, calories_a, calories_b
                )
            else:
                return self._fallback_comparison(dish_a, dish_b, calories_a, calories_b)
        except Exception as e:
            logger.error(f"❌ Comparison generation failed: {e}")
            return self._fallback_comparison(dish_a, dish_b, calories_a, calories_b)

    async def generate_weekly_summary(self, total_calories: int,
                                    date_range: str, avg_per_day: int) -> str:
        """Generate weekly summary with fallback"""
        try:
            if self.openai_service:
                return await self.openai_service.generate_weekly_summary(
                    total_calories, date_range, avg_per_day
                )
            else:
                return self._fallback_weekly_summary(total_calories, avg_per_day)
        except Exception as e:
            logger.error(f"❌ Weekly summary generation failed: {e}")
            return self._fallback_weekly_summary(total_calories, avg_per_day)

    def get_service_status(self) -> Dict[str, bool]:
        """Get status of all services"""
        return {
            "openai": self.openai_service is not None and getattr(self.openai_service, "client", None) is not None,
            "stability": self.stability_service is not None and getattr(self.stability_service, "api_key", None) is not None,
            "model_routes_loaded": bool(self.model_routes)
        }

    # Fallback methods

    def _fallback_bhai_caption(self, dish: str, calories: int) -> str:
        """Fallback bhai caption when service unavailable"""
        templates = [
            f"Bhai, {dish} looks solid - {calories} calories, not bad!",
            f"Scene simple hai bhai: {dish} with {calories} calories, decent choice.",
            f"Bhai, {dish} ka taste aur {calories} calories - balance theek hai!",
            f"{dish} bhai - {calories} calories, mazedaar lagta hai!"
        ]
        template_index = hash(dish) % len(templates)
        return templates[template_index]

    def _fallback_formal_caption(self, dish: str, calories: int) -> str:
        """Fallback formal caption when service unavailable"""
        return f"{dish} provides {calories} calories per serving and offers a balanced nutritional profile suitable for a complete meal."

    def _fallback_comparison(self, dish_a: str, dish_b: str,
                           calories_a: int, calories_b: int) -> str:
        """Fallback comparison when service unavailable"""
        if calories_a < calories_b:
            return f"Bhai, {dish_a} is lighter at {calories_a} calories - better choice than {dish_b}!"
        elif calories_b < calories_a:
            return f"Bhai, {dish_b} is lighter at {calories_b} calories - go for it over {dish_a}!"
        else:
            return f"Bhai, both {dish_a} and {dish_b} are similar at around {calories_a} calories - pick jo mann kare!"

    def _fallback_weekly_summary(self, total_calories: int, avg_per_day: int) -> str:
        """Fallback weekly summary when service unavailable"""
        return f"Your weekly intake totaled {total_calories} calories with an average of {avg_per_day} calories per day. This shows a consistent eating pattern with moderate caloric consumption. Consider maintaining this balanced approach for optimal nutrition."


# Global service manager instance
service_manager = ServiceManager()
