import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

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
    {"role": "user", "content": prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

if response.usage == None:
    raise RuntimeError("usage is None")
promptTokens = response.usage.prompt_tokens
completionTokens = response.usage.completion_tokens
answer = response.choices[0].message.content

if (verbose) :
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {promptTokens}")
    print(f"Response tokens: {completionTokens}")

print(f"Response: {answer}")
