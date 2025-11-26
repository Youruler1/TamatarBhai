"""
StabilityAI service for image generation
"""

import os
import logging
import httpx
import aiofiles
from typing import Optional
from pathlib import Path
import time
import hashlib

logger = logging.getLogger(__name__)


class StabilityAIService:
    """Service for StabilityAI image generation"""
    
    def __init__(self, api_key: Optional[str] = None, engine: str = "stable-diffusion-2"):
        self.api_key = api_key or os.getenv("STABILITY_KEY")
        self.engine = engine
        self.base_url = "https://api.stability.ai"
        self.images_dir = Path("data/images")
        
        # Ensure images directory exists
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        if self.api_key:
            logger.info("✅ StabilityAI service initialized successfully")
        else:
            logger.warning("⚠️ StabilityAI API key not provided")
    
    async def generate_dish_image(self, dish: str) -> Optional[str]:
        """Generate dish image using Stability API"""
        if not self.api_key:
            logger.warning("⚠️ StabilityAI API key not available, using fallback")
            return await self._get_fallback_image(dish)
        
        try:
            # Create a unique filename
            timestamp = int(time.time())
            safe_dish_name = self._sanitize_filename(dish)
            filename = f"{safe_dish_name}_{timestamp}.png"
            filepath = self.images_dir / filename
            
            # Generate image prompt
            prompt = self._create_image_prompt(dish)
            
            # Make API request
            image_data = await self._make_stability_request(prompt)
            
            if image_data:
                # Save image
                await self._save_image(image_data, filepath)
                image_url = f"/data/images/{filename}"
                logger.info(f"✅ Generated image for {dish}: {image_url}")
                return image_url
            else:
                return await self._get_fallback_image(dish)
                
        except Exception as e:
            logger.error(f"❌ StabilityAI image generation failed: {e}")
            return await self._get_fallback_image(dish)
    
    def _create_image_prompt(self, dish: str) -> str:
        """Create optimized prompt for dish image generation"""
        # Enhanced prompt for better food photography
        prompt = f"""A beautifully plated {dish}, professional food photography, 
        appetizing presentation, natural lighting, high quality, detailed, 
        traditional Indian cuisine, colorful, fresh ingredients, 
        restaurant quality plating, top view, clean background"""
        
        return prompt
    
    async def _make_stability_request(self, prompt: str) -> Optional[bytes]:
        """Make request to StabilityAI API"""
        try:
            url = f"{self.base_url}/v1/generation/{self.engine}/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1.0
                    }
                ],
                "cfg_scale": 7,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30,
                "style_preset": "photographic"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("artifacts") and len(result["artifacts"]) > 0:
                        # Decode base64 image
                        import base64
                        image_data = base64.b64decode(result["artifacts"][0]["base64"])
                        return image_data
                    else:
                        logger.error("❌ No image artifacts in StabilityAI response")
                        return None
                else:
                    logger.error(f"❌ StabilityAI API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ StabilityAI API request failed: {e}")
            return None
    
    async def _save_image(self, image_data: bytes, filepath: Path):
        """Save image data to file"""
        try:
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(image_data)
            logger.info(f"✅ Image saved to {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to save image: {e}")
            raise
    
    async def _get_fallback_image(self, dish: str) -> str:
        """Get fallback image when API fails"""
        try:
            # Try to fetch from web or use placeholder
            placeholder_path = await self._create_placeholder_image(dish)
            return placeholder_path
        except Exception as e:
            logger.error(f"❌ Fallback image creation failed: {e}")
            return "/data/images/placeholder.png"
    
    async def _create_placeholder_image(self, dish: str) -> str:
        """Create a simple placeholder image"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple colored placeholder
            img = Image.new('RGB', (512, 512), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Add dish name to image
            text = f"🍽️ {dish}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (512 - text_width) // 2
            y = (512 - text_height) // 2
            
            draw.text((x, y), text, fill='#333333', font=font)
            
            # Save placeholder
            safe_dish_name = self._sanitize_filename(dish)
            filename = f"placeholder_{safe_dish_name}.png"
            filepath = self.images_dir / filename
            
            img.save(filepath)
            
            image_url = f"/data/images/{filename}"
            logger.info(f"✅ Created placeholder image for {dish}: {image_url}")
            return image_url
            
        except Exception as e:
            logger.error(f"❌ Placeholder image creation failed: {e}")
            return "/data/images/default_placeholder.png"
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system usage"""
        # Remove special characters and spaces
        safe_name = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        return safe_name[:50]  # Limit length
    
    async def create_default_placeholder(self):
        """Create a default placeholder image"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (512, 512), color='#e8f4f8')
            draw = ImageDraw.Draw(img)
            
            # Draw a simple food icon representation
            draw.ellipse([156, 156, 356, 356], fill='#ffd700', outline='#ffb347', width=3)
            
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            text = "🍅 Tamatar Bhai"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (512 - text_width) // 2
            
            draw.text((x, 400), text, fill='#333333', font=font)
            
            filepath = self.images_dir / "default_placeholder.png"
            img.save(filepath)
            
            logger.info("✅ Created default placeholder image")
            
        except Exception as e:
            logger.error(f"❌ Failed to create default placeholder: {e}")


# Initialize default placeholder on import
async def init_stability_service():
    """Initialize StabilityAI service with default placeholder"""
    service = StabilityAIService()
    await service.create_default_placeholder()
    return service