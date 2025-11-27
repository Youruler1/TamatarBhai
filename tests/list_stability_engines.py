# list_stability_engines.py
import os, asyncio
from dotenv import load_dotenv, find_dotenv
import httpx

load_dotenv(find_dotenv())

async def main():
    key = os.getenv("STABILITY_KEY")
    if not key:
        print("STABILITY_KEY not set in environment.")
        return

    url = "https://api.stability.ai/v1/engines/list"
    headers = {"Authorization": f"Bearer {key}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(url, headers=headers)
        print("HTTP", r.status_code)
        try:
            j = r.json()
            # pretty-print engines if list available
            if isinstance(j, list):
                for e in j:
                    print(f"- id: {e.get('id')}  name: {e.get('name')}")
            else:
                print(j)
        except Exception:
            print("Response text:", r.text[:1000])

if __name__ == "__main__":
    asyncio.run(main())
