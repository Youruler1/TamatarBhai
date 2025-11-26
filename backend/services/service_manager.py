"""
Service manager for handling external API integrations with fallbacks
"""

import os
import logging
from typing import Optional, Dict, Any
import json
from .openai_service import OpenAIService
from .stability_service import StabilityAIService

logger = logging.getLogger(__name__)


class ServiceManager:
    """Manages external API services with fallback mechanisms"""
    
    def __init__(self):
        self.openai_service = None
        self.stability_service = None
        self.model_routes = self._load_model_routes()
        self._initialize_services()
    
    def _load_model_routes(self) -> Dict[str, Any]:
        """Load model routing configuration"""
        try:
            with open("model_routes.json", "r") as f:
                routes = json.load(f)
                logger.info("✅ Model routes configuration loaded")
                return routes
        except Exception as e:
            logger.error(f"❌ Failed to load model_routes.json: {e}")
            return {}
    
    def _initialize_services(self):
        """Initialize external API services"""
        try:
            # Initialize OpenAI service
            openai_config = self.model_routes.get("caption", {}).get("external_config", {})
            api_key_env = openai_config.get("api_key_env", "OPENAI_API_KEY")
            model = openai_config.get("model", "gpt-4o-mini")
            
            self.openai_service = OpenAIService(
                api_key=os.getenv(api_key_env),
                model=model
            )
            
            # Initialize StabilityAI service
            stability_config = self.model_routes.get("image", {}).get("external_config", {})
            api_key_env = stability_config.get("api_key_env", "STABILITY_KEY")
            engine = stability_config.get("engine", "stable-diffusion-2")
            
            self.stability_service = StabilityAIService(
                api_key=os.getenv(api_key_env),
                engine=engine
            )
            
            logger.info("✅ All services initialized successfully")
            
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
            "openai": self.openai_service is not None and self.openai_service.client is not None,
            "stability": self.stability_service is not None and self.stability_service.api_key is not None,
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