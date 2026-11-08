import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Initialize Gemini client safely
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def ask_mochichi_ai(prompt: str) -> str:
    """Generates an AI response for Mochichi scheduling assistant."""
    if not prompt or not prompt.strip():
        return "Please ask a question."
        
    if not client:
        return "Gemini API key is missing. Please check your .env file."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"AI Error: {str(e)}"