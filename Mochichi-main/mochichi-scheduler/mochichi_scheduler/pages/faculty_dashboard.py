import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.utils.supabase_client import supabase
from mochichi_scheduler.components.sidebar import sidebar

# ==========================================
# 1. STATE & DATABASE LOGIC (Micro-Slice 3)
# ==========================================
class FacultyState(BaseState):
    current_tab: str = "Overview"

    # Form fields for new schedule slot
    day_of_week: str = ""
    start_time: str = ""
    end_time: str = ""
    location: str = ""

    # Live Presence Badge Status
    current_status_color: str = "#16A34A"
    current_status_text: str = "Available"

    def set_tab(self, tab_name: str):
        self.current_tab = tab_name
        
    def set_day_of_week(self, val: str): self.day_of_week = val
    def set_start_time(self, val: str): self.start_time = val
    def set_end_time(self, val: str): self.end_time = val
    def set_location(self, val: str): self.location = val

    async def change_status(self, color: str, text: str):
        """Updates the faculty's live status badge locally and in Supabase."""
        self.current_status_color = color
        self.current_status_text = text
        if self.user_id and supabase:
            try:
                # Saves the presence badge to the users table so students see it
                supabase.table("users").update({
                    "status_color": color,
                    "status_text": text
                }).eq("user_id", self.user_id).execute()
            except Exception as e:
                print(f"Status Update Notice: {e}")

    async def publish_slot(self):
        """Inserts a new open consultation slot into the schedules table."""
        if not self.user_id:
            return rx.window_alert("Error: Not logged in. Please log in as faculty.")
        
        if not self.day_of_week or not self.start_time or not self.end_time or not self.location:
            return rx.window_alert("Please fill in all fields before publishing.")
            
        if supabase:
            try:
                supabase.table("schedules").insert({
                    "faculty_id": self.user_id,
                    "day_of_week": self.day_of_week,
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                    "location": self.location,
                    "is_booked": False
                }).execute()
                
                # Clear the form after successful publish
                self.day_of_week = ""
                self.start_time = ""
                self.end_time = ""
                self.location = ""
                return rx.window_alert("Slot published successfully!")
            except Exception as e:
                print(f"Error publishing slot: {e}")
                return rx.window_alert(f"Database Error: {e}")


# ==========================================
# 2. HEADER & DROPDOWN (Wired)
# ==========================================
def live_availability_dropdown() -> rx.Component:
    def menu_item(color, text):
        return rx.menu.item(
            rx.hstack(
                rx.icon("circle", color=color, fill=color, size=14),
                rx.text(text, weight="bold", color="#374151"),
                align="center",
                spacing="3",
            ),
            on_click=lambda: FacultyState.change_status(color, text),
            padding="2",
            cursor="pointer",
        )

    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("circle", color=FacultyState.current_status_color, size=14, fill=FacultyState.current_status_color),
                FacultyState.current_status_text,
                variant="surface",
                color="#111827",
                background_color="#FDFBF7",
                border="1px solid #E5E7EB",
                radius="full",
                cursor="pointer",
                padding="2 4",
            ),
        ),
        rx.menu.content(
            menu_item("#16A34A", "Available"),
            menu_item("#EAB308", "In Class"),
            menu_item("#EF4444", "Do not Disturb"),
            menu_item("#8B5CF6", "Out of office"),
            menu_item("#F97316", "Busy"),
            style={"background_color": "#FDFBF7", "border_radius": "12px"},
        ),
    )


def top_header() -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.box(
                rx.text(FacultyState.user_initials, color="white", weight="bold"),
                background_color="#BE123C",
                padding="4px 10px",
                border_radius="6px",
            ),
            rx.text("Mochichi Scheduler", weight="bold", color="#111827", size="3"),
            align="center",
            spacing="3",
        ),
        rx.spacer(),
        live_availability_dropdown(),
        width="100%",
        height="70px",
        padding="0 24px",
        background_color="white",
        border_bottom="1px solid #E5E7EB",
        align="center",
        flex_shrink="0",
    )


# ==========================================
# 3. REUSABLE UI COMPONENTS (Static for now)
# ==========================================
def status_badge(status: str) -> rx.Component:
    if status == "Requested":
        return rx.badge("Requested", color="#CA8A04", bg="#FEF08A", radius="medium", size="2", padding="1 3")
    elif status == "Cancelled":
        return rx.badge("Cancelled", color="#DC2626", bg="#FECACA", radius="medium", size="2", padding="1 3")
    return rx.badge("Confirmed", color="#16A34A", bg="#BBF7D0", radius="medium", size="2", padding="1 3")


def action_icons(status: str) -> rx.Component:
    red_btn = rx.box(rx.icon("x", size=14, color="#DC2626", stroke_width=3), bg="#FEE2E2", padding="2px 10px", border_radius="8px", cursor="pointer")
    green_btn = rx.box(rx.icon("check", size=14, color="#16A34A", stroke_width=3), bg="#DCFCE7", padding="2px 10px", border_radius="8px", cursor="pointer")

    if status == "Requested": return rx.hstack(red_btn, green_btn, spacing="2")
    elif status == "Cancelled": return red_btn
    else: return green_btn


def table_header() -> rx.Component:
    return rx.hstack(
        rx.box(rx.text("Students", weight="bold", size="2", color="#111827"), width="150px", flex_shrink="0"),
        rx.box(rx.text("Section", weight="bold", size="2", color="#111827"), width="90px", flex_shrink="0"),
        rx.box(rx.text("Dates/Time", weight="bold", size="2", color="#111827"), width="150px", flex_shrink="0"),
        rx.box(rx.text("Approval", weight="bold", size="2", color="#111827"), width="180px", flex_shrink="0"),
        rx.box(rx.text("Location", weight="bold", size="2", color="#111827"), width="90px", flex_shrink="0"),
        rx.box(rx.text("Visit reason", weight="bold", size="2", color="#111827"), flex="1", min_width="150px"),
        border_bottom="1px solid #E5E7EB", padding_bottom="2", width="100%", align="center",
    )


def table_row(student, section, datetime, status, location, reason) -> rx.Component:
    return rx.hstack(
        rx.box(rx.text(student, size="2", color="#374151"), width="150px", flex_shrink="0"),
        rx.box(rx.text(section, size="2", color="#374151"), width="90px", flex_shrink="0"),
        rx.box(rx.text(datetime, size="2", color="#374151"), width="150px", flex_shrink="0"),
        rx.box(rx.hstack(status_badge(status), action_icons(status), spacing="2"), width="180px", flex_shrink="0"),
        rx.box(rx.text(location, size="2", color="#374151"), width="90px", flex_shrink="0"),
        rx.box(rx.text(reason, size="2", color="#374151"), flex="1", min_width="150px"),
        align="center", padding_y="3", border_bottom="1px solid #F3F4F6", width="100%",
    )


def reschedule_modal(student_name: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.badge("Reschedule", bg="#FEF08A", color="#CA8A04", cursor="pointer", padding="1 3", radius="full")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Reschedule Appointments", style={"color": "#111827", "margin": "0", "font_weight": "bold", "text_decoration": "underline", "text_decoration_color": "#3B82F6", "text_decoration_thickness": "2px"}),
                rx.dialog.close(rx.icon("x", color="#DC2626", size=24, stroke_width=3, cursor="pointer"), position="absolute", top="20px", right="20px"),
                justify="between", align="center", margin_bottom="4", position="relative",
            ),
            rx.text(f"Student: {student_name}", margin_bottom="4", color="#374151"),
            rx.text("New date:", size="2", weight="bold", color="#111827"),
            rx.input(type="date", margin_bottom="3", radius="full", border="1.5px solid #111827", bg="white"),
            rx.text("New time:", size="2", weight="bold", color="#111827"),
            rx.input(type="time", margin_bottom="5", radius="full", border="1.5px solid #111827", bg="white"),
            rx.flex(
                rx.dialog.close(rx.button("Cancel", bg="#FECACA", color="#DC2626", radius="full", padding="4 6", cursor="pointer", _hover={"opacity": 0.8})),
                rx.dialog.close(rx.button("Confirmed", bg="#DCFCE7", color="#16A34A", radius="full", padding="4 6", cursor="pointer", _hover={"opacity": 0.8})),
                spacing="4", justify="center", width="100%",
            ),
            style={"max_width": "350px", "border_radius": "16px", "background_color": "#FDFBF7"},
        ),
    )


# ==========================================
# 4. TAB VIEWS (Actions Tab is now wired)
# ==========================================
def overview_view() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.text("Upcoming Work Context", weight="bold", size="4", margin_bottom="4", color="#111827"),
            rx.grid(
                rx.vstack(rx.text("5", size="7", weight="bold", color="#111827"), rx.text("Confirmed Appointments", size="1", color="#374151"), bg="#FCE7F3", padding="4", border_radius="12px", height="110px", align="start"),
                rx.vstack(rx.text("3", size="7", weight="bold", color="#111827"), rx.text("Blocked Time Slots", size="1", color="#374151"), bg="#FEF3C7", padding="4", border_radius="12px", height="110px", align="start"),
                rx.vstack(rx.text("2", size="7", weight="bold", color="#111827"), rx.text("Open Available Slots", size="1", color="#374151"), bg="#E0F2FE", padding="4", border_radius="12px", height="110px", align="start"),
                rx.vstack(rx.text("1", size="7", weight="bold", color="#111827"), rx.text("Completed Session", size="1", color="#374151"), bg="#DCFCE7", padding="4", border_radius="12px", height="110px", align="start"),
                columns="2", spacing="3",
            ),
            bg="white", padding="6", border_radius="16px", border="1px solid #E5E7EB", width="380px", flex_shrink="0", box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        ),
        rx.box(
            table_header(),
            rx.text("Approval Quick View", size="1", color="#6B7280", margin_bottom="3", margin_top="1"),
            rx.box(
                rx.vstack(
                    table_row("Stud. James Reid", "BSIT - 1A", "Oct 7 - 7:40 am", "Requested", "Eng 412", "Draft review"),
                    table_row("Stud. James Reid", "BSIT - 2C", "Oct 7 - 12:00 pm", "Requested", "Zoom", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSCS - 2A", "Oct 8 - 12:00 pm", "Requested", "Lab 2B", "Schedule discussion"),
                    spacing="1", width="100%",
                ),
                width="100%",
            ),
            bg="white", padding="6", border_radius="16px", border="1px solid #E5E7EB", flex="1", min_width="800px", overflow_x="auto", box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        ),
        direction="row", gap="24px", align_items="flex-start", width="100%", max_width="1200px",
    )


def confirmed_appointments_view() -> rx.Component:
    def confirmed_row(name, date_time, section, reason, location):
        return rx.box(
            rx.hstack(rx.text(f"{name} | {date_time}", weight="bold", size="2", color="#374151"), rx.spacer(), rx.text(f"Section: {section}", color="#4B5563", size="2"), width="100%"),
            rx.hstack(
                rx.text(f"Visit Reason: {reason}", color="#4B5563", size="2"), rx.spacer(),
                rx.vstack(
                    rx.text(f"Loc. {location}", size="2", color="#4B5563", align="right", width="100%"),
                    rx.hstack(reschedule_modal(name), rx.badge("Cancel", bg="#FECACA", color="#DC2626", cursor="pointer", padding="1 3", radius="full")),
                    align_items="flex-end",
                ), width="100%", margin_top="2",
            ), width="100%", padding="4", bg="#FDFBF7", border_radius="8px",
        )

    return rx.box(
        rx.text("Confirmed Schedule & Appointments", weight="bold", size="4", align="center", margin_bottom="6", color="#111827"),
        rx.box(
            rx.vstack(
                confirmed_row("Mark Abrillo", "Fri. Sept. 1, 1:00 PM - 3:00 PM", "BSCS 2A", "Project checking and passing", "Faculty Office"),
                spacing="4", width="100%",
            ), width="100%",
        ),
        bg="white", padding="8", border_radius="16px", border="1px solid #E5E7EB", width="100%", max_width="950px", box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
    )


def full_approval_view() -> rx.Component:
    return rx.box(
        table_header(),
        rx.text("Approval Quick View", size="1", color="#6B7280", margin_bottom="3", margin_top="1"),
        rx.box(
            rx.vstack(
                table_row("Stud. James Reid", "BSIT - 1A", "Oct 7 - 7:40 am", "Requested", "Eng 412", "Draft review"),
                table_row("Stud. James Reid", "BSIT - 2C", "Oct 7 - 12:00 pm", "Requested", "Zoom", "Schedule discussion"),
                spacing="1", width="100%",
            ), width="100%",
        ),
        bg="white", padding="8", border_radius="16px", border="1px solid #E5E7EB", width="100%", max_width="1000px", overflow_x="auto", box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
    )


def actions_view() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(rx.icon("circle-plus", size=20, color="#10B981"), bg="#ECFDF5", padding="2", border_radius="8px"),
            rx.vstack(
                rx.text("Add Available Slots", weight="bold", size="3", color="#111827"),
                rx.text("Create new open consultation hours for students", size="2", color="#6B7280"), spacing="0",
            ), align="center", margin_bottom="4",
        ),
        rx.divider(margin_bottom="6"),
        rx.vstack(
            rx.text("Day of Week", weight="bold", size="2", color="#374151"),
            rx.input(
                placeholder="e.g. Monday", 
                value=FacultyState.day_of_week, 
                on_change=FacultyState.set_day_of_week, 
                width="100%", bg="#FDFBF7", border_color="#E5E7EB", radius="large"
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("Start Time", weight="bold", size="2", color="#374151"),
                    rx.input(type="time", value=FacultyState.start_time, on_change=FacultyState.set_start_time, bg="#FDFBF7", radius="large", width="100%"),
                    width="100%",
                ),
                rx.vstack(
                    rx.text("End Time", weight="bold", size="2", color="#374151"),
                    rx.input(type="time", value=FacultyState.end_time, on_change=FacultyState.set_end_time, bg="#FDFBF7", radius="large", width="100%"),
                    width="100%",
                ),
                spacing="4", width="100%", margin_top="2",
            ),
            rx.text("Consultation Location", weight="bold", size="2", color="#374151", margin_top="2"),
            rx.input(
                placeholder="e.g. Faculty Office", 
                value=FacultyState.location, 
                on_change=FacultyState.set_location, 
                width="100%", bg="#FDFBF7", border_color="#E5E7EB", radius="large"
            ),
            rx.button(
                rx.icon("circle-plus", size=16),
                "Publish Available Slot",
                on_click=FacultyState.publish_slot,
                width="100%", bg="#854D0E", color="white", radius="large", margin_top="6", padding="4", cursor="pointer", _hover={"bg": "#713F12"},
            ),
            align_items="start", width="100%",
        ),
        bg="white", padding="8", border_radius="16px", border="1px solid #E5E7EB", width="100%", max_width="650px", box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
    )


# ==========================================
# 5. MAIN LAYOUT
# ==========================================
def faculty_dashboard_view() -> rx.Component:
    return rx.flex(
        sidebar(active_page=FacultyState.current_tab),
        rx.flex(
            top_header(),
            rx.box(
                rx.match(
                    FacultyState.current_tab,
                    ("Overview", overview_view()),
                    ("View all Confirmed Appointments", confirmed_appointments_view()),
                    ("Approval", full_approval_view()),
                    ("Actions", actions_view()),
                    overview_view(),
                ),
                width="100%", padding="8", height="calc(100vh - 70px)", overflow_y="auto", display="flex", justify_content="center",
            ),
            direction="column", width="100%", height="100vh", background_color="#F8F6F0",
        ),
        direction="row", width="100%", height="100vh",
    )


@rx.page(route="/faculty-dashboard", title="Faculty Dashboard | Mochichi")
def faculty_dashboard_page() -> rx.Component:
    return rx.box(
        rx.html("<style>body { margin: 0; padding: 0; background-color: #F8F6F0; }</style>"),
        faculty_dashboard_view(),
    )