import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

prompt = args.user_prompt
verbose = args.verbose

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    temperature=0,
)

if response.usage == None:
    raise RuntimeError("usage is None")
promptTokens = response.usage.prompt_tokens
completionTokens = response.usage.completion_tokens
answer = response.choices[0].message.content

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose)

        if not result_message["content"]: raise Exception("Error: Content is None")

        if (verbose) :
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {promptTokens}")
            print(f"Response tokens: {completionTokens}")
            print(f"-> {result_message['content']}")

else:
    print(f"Response: {answer}")
