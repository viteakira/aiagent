import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)

def list_groq_models():
    """Print every model that the current Groq key can use."""
    try:
        resp = client.models.list()          # same `client` you created earlier
        print("Available Groq models for this key:")
        for m in resp.data:
            # `m.id` is the string you have to pass to `model=`
            print(f" - {m.id}")
    except Exception as e:
        print("❌ Could not fetch model list:", e)

if __name__ == "__main__":
    # just run this snippet once
    list_groq_models()
