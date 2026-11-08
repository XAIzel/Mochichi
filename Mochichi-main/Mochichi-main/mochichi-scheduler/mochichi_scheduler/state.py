import reflex as rx

class BaseState(rx.State):
    # Global User State
    user_name: str = "Aisha Nakamura"
    user_email: str = "student@university.edu"
    user_role: str = "student"  # Lowercase to match select input

    @rx.var
    def user_initials(self) -> str:
        return "Prof" if self.user_role == "faculty" else "Stud"

    # Mock Weekly Available Slots (Replaces complex calendar grid)
    weekly_slots: list[dict] = [
        {"day": "Mon, Oct 5", "time": "9:00 AM - 11:00 AM", "slot_type": "Advising", "status": "Open"},
        {"day": "Tue, Oct 6", "time": "1:00 PM - 3:00 PM", "slot_type": "Consultation", "status": "Open"},
        {"day": "Wed, Oct 7", "time": "10:00 AM - 12:00 PM", "slot_type": "Thesis Check", "status": "Booked"},
        {"day": "Thu, Oct 8", "time": "2:00 PM - 4:00 PM", "slot_type": "Advising", "status": "Open"},
        {"day": "Fri, Oct 9", "time": "10:00 AM - 11:30 AM", "slot_type": "Consultation", "status": "Open"},
    ]

    # Mock Upcoming Appointments (Dashboard Preview)
    upcoming_appointments: list[dict] = [
        {"prof": "Prof. Kumari", "date": "Oct 7 - 7:00 am", "status": "Requested", "location": "Eng 412", "reason": "Draft review"},
        {"prof": "Prof. Kumari", "date": "Oct 8 - 12:00 pm", "status": "Confirmed", "location": "Zoom", "reason": "Schedule discussion"},
        {"prof": "Prof. Kumari", "date": "Oct 9 - 9:00 am", "status": "Confirmed", "location": "Lab 2B", "reason": "Schedule discussion"},
    ]

    # Mock Faculty Directory List
    faculty_list: list[dict] = [
        {"name": "Prof. Kumari", "dept": "CCS", "summary": "Project scope", "status": "Available", "color": "green"},
        {"name": "Prof. Santos", "dept": "CCS", "summary": "Project scope", "status": "In Class", "color": "yellow"},
        {"name": "Prof. Reyes", "dept": "CCS", "summary": "Thesis draft", "status": "Busy", "color": "orange"},
        {"name": "Prof. Cruz", "dept": "CCS", "summary": "Thesis draft", "status": "Do Not Disturb", "color": "red"},
        {"name": "Prof. Del Rosario", "dept": "CCS", "summary": "Thesis draft", "status": "Out of Office", "color": "purple"},
    ]