import sys
import os

# Ensure the root project directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import reflex as rx
from dotenv import load_dotenv
from supabase import create_client, Client

# Standard Reflex absolute import
from mochichi_scheduler.pages.log_in_sign_in import auth_view, dashboard_view, State

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client safely
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def index() -> rx.Component:
    """Conditionally renders login or dashboard based on user state."""
    return rx.cond(
        State.is_logged_in,
        dashboard_view(),
        auth_view(),
    )

app = rx.App(
    style={
        "::placeholder": {
            "color": "#9CA3AF !important",
            "opacity": "0.85 !important",
        },
    }
)
app.add_page(index, title="Mochichi: AI Appointment System")