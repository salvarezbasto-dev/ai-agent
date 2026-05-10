import os
from dotenv import load_dotenv

# ---- Import API Key to access Google Gemini model
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") 

if api_key == None:
    raise RuntimeError("API key not found")

# ---- Import argparse for user-generated prompts
import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output") # Added optional '--verbose' flag for more 
args = parser.parse_args()

# ---- Import Google Gemini
from google import genai

client = genai.Client(api_key=api_key)

from google.genai import types

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])] # Set user prompt as only message

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
) # Generate responses to user prompts. 

if response.usage_metadata is None:
    raise RuntimeError("Cannot run request. Metadata is None")

# This is the last thing you revised and it is buggy.
if args.verbose:
    print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\nResponse: {response.text}")
else:
    print(f"Response: {response.text}")

