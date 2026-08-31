import argparse
import os
import sys

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

broken = False
counter = 0
limit = 20

while counter < limit:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if response.usage == None:
        raise RuntimeError("usage is None")

    message = response.choices[0].message
    messages.append(message)

    promptTokens = response.usage.prompt_tokens
    completionTokens = response.usage.completion_tokens
    answer = message.content

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)

            if not result_message["content"]: raise Exception("Error: Content is None")

            messages.append(result_message)

            if (verbose) :
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {promptTokens}")
                print(f"Response tokens: {completionTokens}")
                print(f"-> {result_message['content']}")
        counter+= 1

    else:
        print(f"Response: {answer}") # call the model, handle responses, etc.
        broken = True
        break;

if not broken:
    print("Error: Agent could not complete the task")
    sys.exit(1)
