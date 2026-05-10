import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API key not found")

from google import genai

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)

if response.usage_metadata is None:
    raise RuntimeError("Cannot run request. Metadata is None")

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\nResponse: {response.text}")