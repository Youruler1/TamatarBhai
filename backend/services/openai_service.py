"""
openai_service.py

Refactored OpenAIService to support NVIDIA's GPT-OSS style endpoint / client.
Compatible with the sample integrator usage:
  client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key="...")
  model="openai/gpt-oss-120b"
"""

import os
import logging
from typing import Optional
import asyncio

from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI / GPT-OSS API integration."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "openai/gpt-oss-120b",
        base_url: Optional[str] = None,
        stream: bool = False,
    ):
        """
        :param api_key: API key (falls back to OPENAI_API_KEY env var).
        :param model: Model id (default: openai/gpt-oss-120b).
        :param base_url: Optional base_url for the OSS integrator (e.g. https://integrate.api.nvidia.com/v1).
        :param stream: If True, use streaming iterator mode (SDK yields chunks).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = base_url
        self.stream = stream
        self.client: Optional[OpenAI] = None

        if self.api_key:
            try:
                if self.base_url:
                    self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
                else:
                    self.client = OpenAI(api_key=self.api_key)
                logger.info("✅ OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("⚠️ OpenAI API key not provided")

    def _get_bhai_style_prompt(self) -> str:
        """Get the explicit bhai style definition for prompts"""
        return """
You are a friendly Indian college student talking casually to a friend. Use this "bhai style" personality:

BHAI STYLE RULES:
- Sound like a friendly Indian college student
- Use Hinglish (mix of English + Hindi words)
- Light humor and casual tone
- Informal slang allowed but NO profanity
- Keep responses short and punchy (1-2 lines max)
- Use "bhai" naturally in conversation

EXAMPLES:
- "Bhai, yeh dish full mazedaar hai — calories thodi zyada, but worth it."
- "Scene simple hai bhai: rajma lelo, pet bhi bharega aur protein bhi milega."
- "Bhai, if gym ka plan hai toh B better — clean aur halka."

Always respond in this bhai style for the following request:
"""

    # ----- Public methods (same signatures as before) -----
    async def generate_bhai_caption(self, dish: str, calories: int) -> str:
        """Generate bhai-style caption for a dish"""
        if not self.client:
            return self._get_fallback_bhai_caption(dish, calories)

        try:
            prompt = f"""{self._get_bhai_style_prompt()}

Generate a bhai-style caption for this dish:
Dish: {dish}
Calories: {calories}

Make it sound natural and friendly, mentioning the dish and calories in bhai style."""
            response = await self._make_openai_request(prompt, max_tokens=60, temperature=0.7)
            if response:
                caption = response.strip().strip('"').strip("'")
                logger.info(f"✅ Generated bhai caption for {dish}")
                return caption
            else:
                return self._get_fallback_bhai_caption(dish, calories)
        except Exception as e:
            logger.error(f"❌ OpenAI bhai caption generation failed: {e}")
            return self._get_fallback_bhai_caption(dish, calories)

    async def generate_formal_caption(self, dish: str, calories: int) -> str:
        """Generate formal caption for a dish"""
        if not self.client:
            return self._get_fallback_formal_caption(dish, calories)

        try:
            prompt = f"""Generate a professional, informative caption for this dish:

Dish: {dish}
Calories: {calories}

Write 1-2 sentences in formal English that describes the dish nutritionally and contextually. Be informative but concise."""
            response = await self._make_openai_request(prompt, max_tokens=120, temperature=0.3)
            if response:
                caption = response.strip().strip('"').strip("'")
                logger.info(f"✅ Generated formal caption for {dish}")
                return caption
            else:
                return self._get_fallback_formal_caption(dish, calories)
        except Exception as e:
            logger.error(f"❌ OpenAI formal caption generation failed: {e}")
            return self._get_fallback_formal_caption(dish, calories)

    async def generate_comparison_suggestion(self, dish_a: str, dish_b: str, calories_a: int, calories_b: int) -> str:
        """Generate bhai-style comparison suggestion"""
        if not self.client:
            return self._get_fallback_comparison(dish_a, dish_b, calories_a, calories_b)

        try:
            prompt = f"""{self._get_bhai_style_prompt()}

Compare these two dishes and give a bhai-style recommendation:
Dish A: {dish_a} ({calories_a} calories)
Dish B: {dish_b} ({calories_b} calories)

Give ONE line suggestion in bhai style about which is better and why."""
            response = await self._make_openai_request(prompt, max_tokens=60, temperature=0.7)
            if response:
                suggestion = response.strip().strip('"').strip("'")
                logger.info(f"✅ Generated comparison for {dish_a} vs {dish_b}")
                return suggestion
            else:
                return self._get_fallback_comparison(dish_a, dish_b, calories_a, calories_b)
        except Exception as e:
            logger.error(f"❌ OpenAI comparison generation failed: {e}")
            return self._get_fallback_comparison(dish_a, dish_b, calories_a, calories_b)

    async def generate_weekly_summary(self, total_calories: int, date_range: str, avg_per_day: int) -> str:
        """Generate formal weekly summary"""
        if not self.client:
            return self._get_fallback_weekly_summary(total_calories, avg_per_day)

        try:
            prompt = f"""Generate a professional 3-4 sentence summary for this weekly nutrition data:

Total calories: {total_calories}
Date range: {date_range}
Average per day: {avg_per_day}

Write a formal, informative summary about the eating patterns and nutritional balance. Be encouraging and constructive."""
            response = await self._make_openai_request(prompt, max_tokens=200, temperature=0.25)
            if response:
                summary = response.strip().strip('"').strip("'")
                logger.info(f"✅ Generated weekly summary")
                return summary
            else:
                return self._get_fallback_weekly_summary(total_calories, avg_per_day)
        except Exception as e:
            logger.error(f"❌ OpenAI weekly summary generation failed: {e}")
            return self._get_fallback_weekly_summary(total_calories, avg_per_day)

    # ----- Core request helper -----
    async def _make_openai_request(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7, top_p: float = 1.0) -> Optional[str]:
        """
        Make request to OpenAI / GPT-OSS API.
        Uses asyncio.to_thread to call blocking SDK in an async-friendly way.
        Supports streaming (self.stream True) by iterating the returned generator and accumulating `delta` parts.
        """
        if not self.client:
            return None

        def _sync_call():
            return self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=self.stream,
            )

        try:
            result = await asyncio.to_thread(_sync_call)

            # If streaming mode: iterate and collect `delta` pieces
            if self.stream:
                text_parts = []
                try:
                    for chunk in result:
                        # chunk.choices[0].delta may have .content and/or .reasoning_content
                        delta = chunk.choices[0].delta
                        reasoning = getattr(delta, "reasoning_content", None)
                        content = getattr(delta, "content", None)
                        if reasoning:
                            text_parts.append(reasoning)
                        if content is not None:
                            text_parts.append(content)
                except Exception as e:
                    logger.warning(f"Streaming iteration error: {e}")
                return "".join(text_parts).strip() or None

            # Non-streaming: try to extract message content
            try:
                return result.choices[0].message.content
            except Exception:
                try:
                    return getattr(result.choices[0], "text", None)
                except Exception:
                    return None

        except Exception as e:
            logger.error(f"❌ OpenAI API request failed: {e}")
            return None

    # ----- Fallback methods (unchanged) -----
    def _get_fallback_bhai_caption(self, dish: str, calories: int) -> str:
        templates = [
            f"Bhai, {dish} looks solid - {calories} calories, not bad!",
            f"Scene simple hai bhai: {dish} with {calories} calories, decent choice.",
            f"Bhai, {dish} ka taste aur {calories} calories - balance theek hai!",
            f"{dish} bhai - {calories} calories, mazedaar lagta hai!"
        ]
        template_index = hash(dish) % len(templates)
        return templates[template_index]

    def _get_fallback_formal_caption(self, dish: str, calories: int) -> str:
        return f"{dish} provides {calories} calories per serving and offers a balanced nutritional profile suitable for a complete meal."

    def _get_fallback_comparison(self, dish_a: str, dish_b: str, calories_a: int, calories_b: int) -> str:
        if calories_a < calories_b:
            return f"Bhai, {dish_a} is lighter at {calories_a} calories - better choice than {dish_b}!"
        elif calories_b < calories_a:
            return f"Bhai, {dish_b} is lighter at {calories_b} calories - go for it over {dish_a}!"
        else:
            return f"Bhai, both {dish_a} and {dish_b} are similar at around {calories_a} calories - pick jo mann kare!"

    def _get_fallback_weekly_summary(self, total_calories: int, avg_per_day: int) -> str:
        return f"Your weekly intake totaled {total_calories} calories with an average of {avg_per_day} calories per day. This shows a consistent eating pattern with moderate caloric consumption. Consider maintaining this balanced approach for optimal nutrition."
