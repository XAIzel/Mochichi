import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from your .env file
load_dotenv()

# Get the URL and Key from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Safely initialize the Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("Warning: Supabase URL or Key is missing. Check your .env file.")