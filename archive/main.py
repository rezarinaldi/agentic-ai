from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick:free",
    messages=[{"role": "user", "content": "Write a haiku joke about programmer!"}],
)

print(response.choices[0].message.content)
