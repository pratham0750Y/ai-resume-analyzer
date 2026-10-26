import os

from dotenv import load_dotenv
from google import genai

load_dotenv() 

MODEL = os.getenv("GEMINI_MODEL")


def ask_ai(prompt):
    """Send a prompt to the AI model and return the answer text. Returns None if no key is set."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    client = genai.Client(api_key=api_key)
    return client.models.generate_content(model=MODEL, contents=prompt).text
