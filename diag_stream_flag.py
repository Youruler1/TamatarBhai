# diag_stream_flag.py
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from backend.services.service_manager import service_manager

svc = getattr(service_manager, "openai_service", None)
print("service_manager.get_service_status():", service_manager.get_service_status())
print("openai_service present?:", svc is not None)
if svc:
    print("OpenAIService.stream flag:", getattr(svc, "stream", None))
    print("OpenAIService.model:", getattr(svc, "model", None))
    print("OpenAIService.base_url:", getattr(svc, "base_url", None))
