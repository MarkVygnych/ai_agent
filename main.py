import argparse
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):
    completion = client.chat.completions.create(
    model="openrouter/free",
    messages = messages,
    temperature=0,
    tools=available_functions,
)
    # call the model, handle responses, etc.
    message = completion.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message["content"]:
                raise Exception("Function returned an empty result. Please check the function implementation.")
            if args.verbose:
                print(f" - Function result: {result_message['content']}")
            messages.append(result_message)
    else:
        print(f"Model response: {message.content}")
        break

    if completion.usage is not None:
        prompt_tokens = completion.usage.prompt_tokens
        response_tokens = completion.usage.completion_tokens
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        raise RuntimeError("Usage information is not available.")

else:
    print("Max iterations reached without a final response.")
    sys.exit(1)
