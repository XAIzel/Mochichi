import reflex as rx


class BaseState(rx.State):
    """Global application state shell (static mock data now; wired to Supabase in Phase 2)."""

    # Global User Identity (Matches Data Dictionary Table 1: users)
    user_id: str = ""
    user_name: str = "Aisha Nakamura"
    user_email: str = "aisha.nakamura@lspu.edu.ph"
    user_role: str = "student"  # 'student' | 'faculty' | 'admin'
    user_department: str = "College of Computer Studies"

    @rx.var
    def user_initials(self) -> str:
        """Role badge label matching Figma sidebar cards (Stud / Prof / Admin)."""
        if self.user_role == "faculty":
            return "Prof"
        if self.user_role == "admin":
            return "Admin"
        return "Stud"

    # Student Dashboard Work-Context Counters (Matches Student Overview Figma)
    student_confirmed_count: int = 5
    student_requested_count: int = 3
    student_pending_count: int = 1
    student_cancelled_count: int = 1

    # Faculty Dashboard Work-Context Counters (Matches Faculty Overview Figma)
    faculty_pending_count: str = "4"
    faculty_confirmed_count: str = "2"
    faculty_total_students: str = "15"
    faculty_cancelled_count: str = "0"

    # Mock Upcoming Appointments (Matches Student 'Upcoming bookings' Figma & Table 3)
    upcoming_appointments: list[dict[str, str]] = [
        {
            "professor": "Prof. Kumari",
            "datetime": "Oct 7 - 7:00 am",
            "status": "Requested",
            "location": "Faculty room",
            "reason": "Draft review",
        },
        {
            "professor": "Prof. Kumari",
            "datetime": "Oct 8 - 12:00 pm",
            "status": "Confirmed",
            "location": "Faculty room",
            "reason": "Schedule discussion",
        },
        {
            "professor": "Prof. Kumari",
            "datetime": "Oct 9 - 9:00 am",
            "status": "Confirmed",
            "location": "Faculty room",
            "reason": "Schedule discussion",
        },
    ]

    # Mock Faculty Directory List (Matches FR-03 5 Status Badges & Student Faculty Grid)
    faculty_list: list[dict[str, str]] = [
        {
            "name": "Prof. Rafael Moreau",
            "department": "Engineering",
            "status": "Available",
            "color": "green",
            "available_slots": "3",
        },
        {
            "name": "Prof. Elena Cruz",
            "department": "College of Computer Studies",
            "status": "In Class",
            "color": "yellow",
            "available_slots": "0",
        },
        {
            "name": "Prof. Marky S. Perez",
            "department": "Computer Studies",
            "status": "Do not Disturb",
            "color": "red",
            "available_slots": "0",
        },
        {
            "name": "Prof. Santos",
            "department": "College of Computer Studies",
            "status": "Busy",
            "color": "orange",
            "available_slots": "0",
        },
        {
            "name": "Prof. Del Rosario",
            "department": "College of Computer Studies",
            "status": "Out of office",
            "color": "purple",
            "available_slots": "0",
        },
    ]

    # Mock Admin User Directory List (Matches Admin 'User Directory Management' Figma)
    admin_directory_users: list[dict[str, str]] = [
        {
            "display_id": "MU-20418",
            "full_name": "Dr. Elena Martinez",
            "role_label": "Faculty",
            "department": "Comparative Literature",
            "email": "e.martinez@mochichi.edu",
            "is_active": "true",
        },
        {
            "display_id": "MU-31877",
            "full_name": "Amir Hassan",
            "role_label": "Student",
            "department": "BSc Biochemistry, Y3",
            "email": "a.hassan@students.mochichi.edu",
            "is_active": "true",
        },
        {
            "display_id": "MU-12983",
            "full_name": "Linda Park",
            "role_label": "Student",
            "department": "BSc Biochemistry, Y3",
            "email": "l.park@mochichi.edu",
            "is_active": "true",
        },
        {
            "display_id": "MU-31544",
            "full_name": "Sofia Nguyen",
            "role_label": "Student",
            "department": "MA Public Policy, Y1",
            "email": "s.nguyen@students.mochichi.edu",
            "is_active": "false",
        },
        {
            "display_id": "MU-45912",
            "full_name": "Prof. Marky S. Perez",
            "role_label": "Faculty",
            "department": "Computer Studies",
            "email": "marky.perez@mochichi.edu",
            "is_active": "true",
        },
        {
            "display_id": "MU-88201",
            "full_name": "James Reid",
            "role_label": "Student",
            "department": "BSCS, Y4",
            "email": "j.reid@students.mochichi.edu",
            "is_active": "true",
        },
    ]

    # FIFO Chat Context Queue Shell (Wired to Gemini SDK in Phase 3, Micro-Slice 1)
    chat_messages: list[dict[str, str]] = [
        {
            "sender": "mochichi",
            "text": "Hi Aisha! I can help you schedule an appointment. Which professor would you like to meet, and what is your reason for the visit?",
        }
    ]