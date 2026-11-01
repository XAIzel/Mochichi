import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Find the root .env file reliably
env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def ask_mochichi_ai(prompt: str) -> str:
    """Sends a query to Google Gemini AI for the Mochichi assistant."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"You are Mochichi, an AI-powered academic appointment assistant for LSPU. "
            f"Help faculty and students manage their appointments professionally. User query: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"AI Assistant Error: {str(e)}"