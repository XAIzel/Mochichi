import sys
import os
import reflex as rx
from dotenv import load_dotenv
from supabase import create_client, Client

# Reflex standard: Always use absolute imports starting with your main app folder
from mochichi_scheduler.pages.log_in_sign_in import auth_view, dashboard_view, State

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client safely
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def index() -> rx.Component:
    """Previewing the dashboard view layout."""
    return dashboard_view()

# Note: In a standard Reflex app, you usually only define rx.App() ONCE in your main 
# mochichi_scheduler.py file, and sub-pages just define components. However, I have 
# kept your structure exactly as you wrote it to ensure the import error is resolved.
app = rx.App(
    style={
        "::placeholder": {
            "color": "#9CA3AF !important",
            "opacity": "0.85 !important",
        },
    }
)
app.add_page(index, title="Mochichi: AI Appointment System")