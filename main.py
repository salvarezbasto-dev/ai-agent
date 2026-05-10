import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") # Import API Key to access Google Gemini model

if api_key == None:
    raise RuntimeError("API key not found")

import argparse # Import argparse for user-generated prompts

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

from google import genai # Import Google Gemini

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
) # Set Gemini 2.5 Flash to generate text outputs out of user-generated text input

if response.usage_metadata is None:
    raise RuntimeError("Cannot run request. Metadata is None")

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\nResponse: {response.text}")