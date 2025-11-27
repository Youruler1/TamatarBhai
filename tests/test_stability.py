# test_stability.py
import asyncio
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from backend.services.service_manager import service_manager

async def main():
    print("Service status:", service_manager.get_service_status())
    # Try generating one image
    image_url = await service_manager.generate_dish_image("Paneer Butter Masala")
    print("Returned image URL:", image_url)
    # Check file exists locally
    if image_url and image_url.startswith("/data/images/"):
        import os
        local_path = image_url.lstrip("/")
        print("Local path:", local_path, "Exists?", os.path.exists(local_path))
    else:
        print("No local image path returned; check logs for API errors.")

if __name__ == "__main__":
    asyncio.run(main())
