# diag_stability_http.py
import os, asyncio
import httpx
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

async def main():
    key = os.getenv("STABILITY_KEY")
    base = "https://api.stability.ai"
    engine = "stable-diffusion-2"
    url = f"{base}/v1/generation/{engine}/text-to-image"
    headers = {"Authorization": f"Bearer {key}", "Content-Type":"application/json"}
    payload = {
        "text_prompts":[{"text":"A photorealistic bowl of paneer butter masala, top view, restaurant lighting"}],
        "cfg_scale":7,
        "height":512,"width":512,"samples":1,"steps":30,"style_preset":"photographic"
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        print("HTTP", r.status_code)
        try:
            print(r.json())
        except Exception:
            print("Response text:", r.text[:1000])

if __name__ == "__main__":
    asyncio.run(main())
