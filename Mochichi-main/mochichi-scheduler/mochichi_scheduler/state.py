import reflex as rx
from mochichi_scheduler.utils.supabase_client import supabase


class BaseState(rx.State):
    """Global application state shell (Wired to Supabase for Phase 2)."""

    # Global User Identity 
    user_id: str = ""
    user_name: str = "Aisha Nakamura"
    user_email: str = "aisha.nakamura@lspu.edu.ph"
    user_role: str = "student"  # 'student' | 'faculty' | 'admin'
    user_department: str = "College of Computer Studies"

    is_loading: bool = False

    @rx.var
    def user_initials(self) -> str:
        """Role badge label matching Figma sidebar cards (Stud / Prof / Admin)."""
        if self.user_role == "faculty":
            return "Prof"
        if self.user_role == "admin":
            return "Admin"
        return "Stud"

    # --- MOCK DATA FOR OTHER PAGES (Kept intact to prevent breaking) ---
    student_confirmed_count: int = 5
    student_requested_count: int = 3
    student_pending_count: int = 1
    student_cancelled_count: int = 1

    faculty_pending_count: str = "4"
    faculty_confirmed_count: str = "2"
    faculty_total_students: str = "15"
    faculty_cancelled_count: str = "0"

    upcoming_appointments: list[dict[str, str]] = [
        {
            "professor": "Prof. Kumari",
            "datetime": "Oct 7 - 7:00 am",
            "status": "Requested",
            "location": "Faculty room",
            "reason": "Draft review",
        },
    ]

    faculty_list: list[dict[str, str]] = [
        {
            "name": "Prof. Rafael Moreau",
            "department": "Engineering",
            "status": "Available",
            "color": "green",
            "available_slots": "3",
        },
    ]

    chat_messages: list[dict[str, str]] = [
        {
            "sender": "mochichi",
            "text": "Hi Aisha! I can help you schedule an appointment. Which professor would you like to meet, and what is your reason for the visit?",
        }
    ]

    # --- LIVE SUPABASE ADMIN DIRECTORY ---
    admin_directory_users: list[dict[str, str]] = []

    def load_admin_directory(self):
        """Fetches live users from Supabase public.users table."""
        self.is_loading = True
        yield
        
        if supabase:
            try:
                response = supabase.table("users").select("*").execute()
                users_data = response.data
                
                formatted_users = []
                for u in users_data:
                    formatted_users.append({
                        "display_id": str(u.get("user_id")),  # Supabase UUID
                        "full_name": u.get("full_name", "Unknown"),
                        "role_label": str(u.get("role", "N/A")).capitalize(),
                        "department": u.get("department", "N/A"),
                        "email": u.get("email", ""),
                        "is_active": "true" if u.get("is_active") else "false"
                    })
                self.admin_directory_users = formatted_users
            except Exception as e:
                print(f"Supabase Fetch Error: {e}")
                
        self.is_loading = False
        yield

    def toggle_user_active(self, user_uuid: str, current_ui_status: bool):
        """Updates the is_active boolean in Supabase when the admin clicks the toggle."""
        self.is_loading = True
        yield
        
        if supabase:
            try:
                # Update the target user's row in Supabase
                supabase.table("users").update({"is_active": current_ui_status}).eq("user_id", user_uuid).execute()
                
                # Re-fetch the directory to ensure UI matches the database exactly
                self.load_admin_directory()
            except Exception as e:
                print(f"Supabase Update Error: {e}")
                
        self.is_loading = False
        yield