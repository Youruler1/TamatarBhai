# stream_test.py
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os

load_dotenv(find_dotenv())

client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "openai/gpt-oss-120b"),
    messages=[{"role":"user","content":"Write one short sentence about paneer butter masala."}],
    temperature=0.7,
    top_p=1,
    max_tokens=200,
    stream=True
)

for chunk in completion:
    reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
    if reasoning:
        print(reasoning, end="")
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
