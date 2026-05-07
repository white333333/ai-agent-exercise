import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")
    client = genai.Client(api_key=api_key)

    

    #parsing the input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #response
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    #counting tokens:
    if args.verbose:
        if response.usage_metadata is None:
            raise RuntimeError("failed API request")
        else:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    if response.function_calls is not None:   
        for i in response.function_calls:
            print(f"Calling function: {i.name}({i.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
