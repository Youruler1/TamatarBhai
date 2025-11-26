# # inside a python script or REPL
# import asyncio
# from services.service_manager import service_manager
# print(asyncio.run(service_manager.generate_bhai_caption('paneer butter masala', 650)))

# from backend.services.service_manager import service_manager
# print(service_manager.get_service_status())


# repl.py — ENTRYPOINT (run this)
import logging
from dotenv import load_dotenv, find_dotenv
import os

# 1) Load .env from backend/.env (adjust path if necessary)
# Option A: automatic search
load_dotenv(find_dotenv(filename=".env"))

# Option B: explicit path (safer if you know exact location)
# from pathlib import Path
# dotenv_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path)

# 2) basic logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3) quick check (does not print secrets)
logger.info("OPENAI_API_KEY set? %s", bool(os.getenv("OPENAI_API_KEY")))
logger.info("OPENAI_BASE_URL: %s", os.getenv("OPENAI_BASE_URL"))

# 4) Now import rest of app (after env loaded)
from backend.services.service_manager import service_manager
import asyncio

print(service_manager.get_service_status())

# quick test call
res = asyncio.run(service_manager.generate_bhai_caption("paneer butter masala", 650))
print(res)
