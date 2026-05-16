import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="Chatbot") # Using parse for user-generated prompts
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output") # Added optional '--verbose' flag for more 
    args = parser.parse_args()

    load_dotenv() #API key to access Google Gemini mode
    api_key = os.environ.get("GEMINI_API_KEY") 
    if api_key == None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key) #Setting gen AI and messages
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n") #Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\nResponse: {response.text}")
   # else:
       # print(f"Response: {response.text}")
    
    generate_content(client, messages, args.verbose)

# --- Set responses
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0)
    ) # Generate responses to user prompts, set system prompt, and list of functions for LLM.

    if response.usage_metadata is None:
        raise RuntimeError("Cannot run request. Metadata is None")

    if verbose: #Print tokens if '--verbose' flag is used
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is not None: 
        print(f"Response: {response.text}")
        function_results = []

        for function_call in response.function_calls: 
            function_call_results = call_function(function_call, verbose)

            #Checking for errors below
            if not function_call_results.parts:
                raise RuntimeError("call_function returned no parts")
            
            first_part = function_call_results.parts[0]
            if first_part.function_response is None:
                raise RuntimeError("Expected function_response on first part")
            
            function_response = first_part.function_response.response
            if function_response is None:
                raise RuntimeError("Expected response in function_response")
            
            #Adding response to list now that we know there are no errors
            function_results.append(first_part)

            if verbose:
                print(f"-> {function_response}")

if __name__ == "__main__":
    main()
