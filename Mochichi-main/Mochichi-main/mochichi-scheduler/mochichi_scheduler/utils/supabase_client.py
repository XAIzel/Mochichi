import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Find the root .env file reliably
env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(f"Supabase URL and Key must be set in environment variables. Checked path: {env_path}")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)