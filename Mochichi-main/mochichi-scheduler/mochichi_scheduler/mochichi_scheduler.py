import sys
import os

# Ensure the root project directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import reflex as rx

# Import pages so Reflex registers all routes cleanly on startup
from mochichi_scheduler.pages.log_in_sign_in import auth_view, dashboard_view, State
from mochichi_scheduler.pages.appointments import appointments_page
from mochichi_scheduler.pages.faculty import faculty_page  # Registers /faculty via @rx.page
from mochichi_scheduler.pages.mochichi import mochichi_page  # Registers /mochichi via @rx.page
from mochichi_scheduler.pages.admin_dashboard import admin_dashboard_view  # Registers /admin-dashboard via @rx.page
from mochichi_scheduler.pages.faculty_dashboard import faculty_dashboard_view  # Registers /faculty-dashboard via @rx.page


def index() -> rx.Component:
    """Conditionally renders login/signup or the role-matched dashboard based on user state."""
    return rx.cond(
        State.is_logged_in,
        rx.match(
            State.user_role,
            ("admin", admin_dashboard_view()),
            ("faculty", faculty_dashboard_view()),  # Routes Faculty to their correct dashboard!
            dashboard_view(),  # Defaults to Student
        ),
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

# Register primary routes
app.add_page(index, route="/", title="Mochichi: AI Appointment System")
app.add_page(appointments_page, route="/appointments", title="Mochichi: Upcoming Bookings")