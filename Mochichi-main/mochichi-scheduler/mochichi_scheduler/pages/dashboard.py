import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar
from mochichi_scheduler.utils.supabase_client import supabase

# ==========================================
# 1. STATE & DATABASE LOGIC (Micro-Slice 4)
# ==========================================
class StudentDashboardState(BaseState):
    # Metrics for the UI tiles
    confirmed_count: str = "0"
    requested_count: str = "0"
    pending_count: str = "0"
    cancelled_count: str = "0"

    # Booking Modal State
    is_booking_modal_open: bool = False
    available_slots: list[dict] = []
    selected_slot_id: str = ""
    selected_faculty_id: str = ""
    visit_reason: str = ""

    async def fetch_dashboard_metrics(self):
        """Loads the student's appointment counts from Supabase when the page loads."""
        if not self.user_id or not supabase:
            return

        try:
            # Fetch all appointments for this specific student
            response = supabase.table("appointments").select("status").eq("student_id", self.user_id).execute()
            
            # Count the statuses
            counts = {"Confirmed": 0, "Requested": 0, "Pending": 0, "Cancelled": 0}
            for row in response.data:
                status = row.get("status", "Pending")
                if status in counts:
                    counts[status] += 1
                else:
                    counts["Pending"] += 1 # Default bucket
            
            self.confirmed_count = str(counts["Confirmed"])
            self.requested_count = str(counts["Requested"])
            self.pending_count = str(counts["Pending"])
            self.cancelled_count = str(counts["Cancelled"])
        except Exception as e:
            print(f"Error fetching metrics: {e}")

    async def open_booking_modal(self):
        """Fetches available slots from schedules and opens the modal."""
        if not supabase: return
        
        try:
            # 1. Fetch unbooked slots
            slots_response = supabase.table("schedules").select("*").eq("is_booked", False).execute()
            slots = slots_response.data
            
            # 2. Fetch faculty names to match with the slots
            if slots:
                faculty_ids = list(set([s["faculty_id"] for s in slots]))
                users_response = supabase.table("users").select("user_id, full_name").in_("user_id", faculty_ids).execute()
                faculty_map = {u["user_id"]: u["full_name"] for u in users_response.data}
                
                # Combine data for the UI
                for s in slots:
                    s["faculty_name"] = faculty_map.get(s["faculty_id"], "Unknown Professor")
            
            self.available_slots = slots
            self.is_booking_modal_open = True
        except Exception as e:
            print(f"Error loading slots: {e}")

    def close_booking_modal(self):
        self.is_booking_modal_open = False
        self.selected_slot_id = ""
        self.visit_reason = ""

    def select_slot(self, slot_id: str, faculty_id: str):
        self.selected_slot_id = str(slot_id)
        self.selected_faculty_id = str(faculty_id)

    def set_visit_reason(self, reason: str):
        self.visit_reason = reason

    async def submit_booking(self):
        """Saves the appointment and updates the schedule slot."""
        if not self.selected_slot_id or not self.visit_reason.strip():
            return rx.window_alert("Please select a slot and provide a reason for your visit.")
            
        try:
            # 1. Create the appointment record
            supabase.table("appointments").insert({
                "student_id": self.user_id,
                "faculty_id": self.selected_faculty_id,
                "schedule_id": int(self.selected_slot_id),
                "reason": self.visit_reason,
                "status": "Requested"
            }).execute()

            # 2. Mark the schedule slot as booked so no one else takes it
            supabase.table("schedules").update({"is_booked": True}).eq("id", int(self.selected_slot_id)).execute()

            self.close_booking_modal()
            await self.fetch_dashboard_metrics()
            return rx.window_alert("Appointment requested successfully!")
        except Exception as e:
            print(f"Error booking: {e}")
            return rx.window_alert("Database Error while booking. Check terminal.")


# ==========================================
# 2. UI COMPONENTS
# ==========================================
def _metric_tile(icon_name: str, count: str, label: str, bg_color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(icon_name, size=15, color="#111827"),
                rx.text(count, font_weight="700", font_size="22px", color="#111827", line_height="1"),
                align="center", spacing="4",
            ),
            rx.text(label, font_size="12px", color="#374151", font_weight="500"),
            spacing="4", align_items="start",
        ),
        padding="18px 20px", background_color=bg_color, border_radius="12px", width="100%",
    )


def _quick_action_link(icon_name: str, label: str, target_route: str) -> rx.Component:
    """Standard link router for quick actions."""
    return rx.hstack(
        rx.icon(icon_name, size=16, color="#C03928"),
        rx.text(label, font_size="13px", font_weight="500", color="#1F2937"),
        width="100%", padding="14px 18px", background_color="#FDF2F2", border_radius="10px",
        align="center", spacing="4", cursor="pointer", _hover={"background_color": "#FCE7E7"},
        on_click=rx.redirect(target_route),
    )


def _quick_action_button(icon_name: str, label: str, on_click_action) -> rx.Component:
    """Button trigger for opening modals."""
    return rx.hstack(
        rx.icon(icon_name, size=16, color="#C03928"),
        rx.text(label, font_size="13px", font_weight="500", color="#1F2937"),
        width="100%", padding="14px 18px", background_color="#FDF2F2", border_radius="10px",
        align="center", spacing="4", cursor="pointer", _hover={"background_color": "#FCE7E7"},
        on_click=on_click_action,
    )


def slot_card(slot: dict) -> rx.Component:
    """Renders a single available time slot inside the booking modal."""
    is_selected = StudentDashboardState.selected_slot_id == slot["id"].to(str)
    
    return rx.box(
        rx.vstack(
            rx.text(slot["faculty_name"], font_weight="bold", color="#111827"),
            rx.text(f"{slot['day_of_week']} | {slot['start_time']} - {slot['end_time']}", size="2", color="#4B5563"),
            rx.text(f"Location: {slot['location']}", size="1", color="#6B7280"),
            align_items="start",
            spacing="1"
        ),
        padding="3",
        border=rx.cond(is_selected, "2px solid #C03928", "1px solid #E5E7EB"),
        border_radius="8px",
        background_color=rx.cond(is_selected, "#FDF2F2", "white"),
        cursor="pointer",
        width="100%",
        on_click=lambda: StudentDashboardState.select_slot(slot["id"], slot["faculty_id"]),
        _hover={"border_color": "#C03928"}
    )


def booking_modal() -> rx.Component:
    """The modal that pops up when 'Start a new request' is clicked."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Book an Appointment", style={"color": "#111827", "margin": "0", "font_weight": "bold"}),
                rx.dialog.close(rx.icon("x", color="#6B7280", cursor="pointer", on_click=StudentDashboardState.close_booking_modal)),
                justify="between", align="center", margin_bottom="4",
            ),
            rx.text("Select an available consultation slot:", size="2", weight="bold", margin_bottom="2"),
            rx.box(
                rx.cond(
                    StudentDashboardState.available_slots.length() > 0,
                    rx.vstack(
                        rx.foreach(StudentDashboardState.available_slots, slot_card),
                        spacing="2", width="100%", max_height="250px", overflow_y="auto", padding_right="2"
                    ),
                    rx.text("No open slots available right now.", color="#6B7280", size="2")
                ),
                margin_bottom="4"
            ),
            rx.text("Reason for visit:", size="2", weight="bold", margin_bottom="2"),
            rx.input(
                placeholder="e.g. Project checking, Thesis draft...",
                value=StudentDashboardState.visit_reason,
                on_change=StudentDashboardState.set_visit_reason,
                width="100%", margin_bottom="5"
            ),
            rx.flex(
                rx.button("Cancel", bg="#F3F4F6", color="#374151", cursor="pointer", on_click=StudentDashboardState.close_booking_modal),
                rx.button("Submit Request", bg="#C03928", color="white", cursor="pointer", on_click=StudentDashboardState.submit_booking, _hover={"bg": "#A93226"}),
                spacing="4", justify="end", width="100%",
            ),
            style={"max_width": "450px", "border_radius": "16px", "background_color": "#FFFFFF"},
        ),
        open=StudentDashboardState.is_booking_modal_open,
    )


# ==========================================
# 3. MAIN LAYOUT
# ==========================================
def dashboard_view() -> rx.Component:
    return rx.hstack(
        sidebar(active_page="Overview"),
        rx.vstack(
            # Top Header Bar
            rx.hstack(
                rx.hstack(
                    rx.box(rx.text(StudentDashboardState.user_initials, color="white", font_weight="bold", font_size="13px"), background_color="#B93829", width="24px", height="24px", border_radius="6px", display="flex", align_items="center", justify_content="center"),
                    rx.text("Mochichi Scheduler", font_weight="600", font_size="14px", color="#1F2937"), spacing="2", align="center",
                ), width="100%", padding_x="24px", padding_y="14px", background_color="white", border_bottom="1px solid #EDE8DE",
            ),
            # Centered Two-Card Overview Section
            rx.center(
                rx.hstack(
                    # Left Card: Metrics
                    rx.box(
                        rx.vstack(
                            rx.heading("Student-Specific Context", size="4", font_weight="700", color="#111827", margin_bottom="14px"),
                            rx.grid(
                                _metric_tile("square-dot", StudentDashboardState.confirmed_count, "Confirmed", "#FCE8E8"),
                                _metric_tile("clock", StudentDashboardState.requested_count, "Requested", "#FEF9D7"),
                                _metric_tile("info", StudentDashboardState.pending_count, "Pending", "#E1F0FA"),
                                _metric_tile("info", StudentDashboardState.cancelled_count, "Cancelled", "#FCE8E8"),
                                columns="2", spacing="4", width="100%",
                            ),
                            spacing="3", align_items="start", width="100%",
                        ), background_color="white", border="1px solid #E6DEC8", border_radius="16px", padding="32px", width="375px", min_height="460px",
                    ),
                    # Right Card: Actions
                    rx.box(
                        rx.vstack(
                            rx.heading("Quick Actions & Updates", size="4", font_weight="700", color="#111827", margin_bottom="14px"),
                            rx.vstack(
                                _quick_action_button("square-dot", "Start a new request", StudentDashboardState.open_booking_modal),
                                _quick_action_link("clock", "Request rescheduling", "/appointments"),
                                _quick_action_link("info", "Cancel booking request", "/appointments"),
                                spacing="4", width="100%",
                            ),
                            spacing="3", align_items="start", width="100%",
                        ), background_color="white", border="1px solid #E6DEC8", border_radius="16px", padding="32px", width="375px", min_height="460px",
                    ),
                    spacing="7", align="stretch", justify="center", wrap="wrap",
                ),
                width="100%", padding="48px 36px", flex="1", align_items="start",
            ),
            flex="1", height="100vh", overflow_y="auto", background_color="#FAF6EE", spacing="0",
        ),
        booking_modal(),  # Hidden modal that opens on click
        width="100%", height="100vh", spacing="0",
    )


@rx.page(
    route="/dashboard", 
    title="Student Dashboard | Mochichi",
    on_load=StudentDashboardState.fetch_dashboard_metrics  # Fetches stats on load!
)
def dashboard_page() -> rx.Component:
    return dashboard_view()