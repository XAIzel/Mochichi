import reflex as rx
from mochichi_scheduler.state import BaseState

# ==========================================
# 1. STATE
# ==========================================
class FacultyState(rx.State):
    current_tab: str = "Overview"

    def set_tab(self, tab_name: str):
        self.current_tab = tab_name

# ==========================================
# 2. HEADER & DROPDOWN
# ==========================================
def live_availability_dropdown() -> rx.Component:
    def menu_item(color, text):
        return rx.menu.item(
            rx.hstack(
                rx.icon("circle", color=color, fill=color, size=14), 
                rx.text(text, weight="bold", color="#374151"), 
                align="center", spacing="3"
            ),
            padding="2", cursor="pointer"
        )
    
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("circle", color="#16A34A", size=14, fill="#16A34A"),
                "Available",
                variant="surface", color="#111827", background_color="#FDFBF7",
                border="1px solid #E5E7EB", radius="full", cursor="pointer", padding="2 4"
            ),
        ),
        rx.menu.content(
            menu_item("#16A34A", "Available"),
            menu_item("#EAB308", "In Class"),
            menu_item("#EF4444", "Do not Disturb"),
            menu_item("#8B5CF6", "Out of office"),
            menu_item("#F97316", "Busy"),
            style={"background_color": "#FDFBF7", "border_radius": "12px"}
        ),
    )

def top_header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.box(
                rx.text("M", color="white", font_weight="bold", font_size="13px"),
                background_color="#BE123C", width="24px", height="24px", border_radius="6px",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.text("Mochichi Scheduler", font_weight="600", font_size="14px", color="#1F2937"),
            spacing="2", align="center",
        ),
        rx.spacer(),
        live_availability_dropdown(),
        width="100%", padding_x="24px", padding_y="14px", 
        background_color="white", border_bottom="1px solid #EDE8DE",
    )

# ==========================================
# 3. REUSABLE UI COMPONENTS 
# ==========================================
def _context_tile(count: str, label: str, bg_color: str) -> rx.Component:
    """Single status metric tile matching student UI."""
    return rx.box(
        rx.vstack(
            rx.text(count, font_weight="700", font_size="28px", color="#111827"),
            rx.text(label, font_size="12px", color="#374151", font_weight="500"),
            spacing="2", align_items="start",
        ),
        padding="18px", background_color=bg_color, border_radius="12px", width="100%",
    )

def status_badge(status: str) -> rx.Component:
    if status == "Requested":
        return rx.badge("Requested", color="#CA8A04", bg="#FEF08A", radius="medium", size="2", padding="1 3")
    elif status == "Cancelled":
        return rx.badge("Cancelled", color="#DC2626", bg="#FECACA", radius="medium", size="2", padding="1 3")
    return rx.badge("Confirmed", color="#16A34A", bg="#BBF7D0", radius="medium", size="2", padding="1 3")

def action_icons(status: str) -> rx.Component:
    red_btn = rx.box(rx.icon("x", size=14, color="#DC2626", stroke_width=3), bg="#FEE2E2", padding="2px 10px", border_radius="8px", cursor="pointer")
    green_btn = rx.box(rx.icon("check", size=14, color="#16A34A", stroke_width=3), bg="#DCFCE7", padding="2px 10px", border_radius="8px", cursor="pointer")
    
    if status == "Requested":
        return rx.hstack(red_btn, green_btn, spacing="2")
    elif status == "Cancelled":
        return red_btn
    else:
        return green_btn

def table_header() -> rx.Component:
    return rx.hstack(
        rx.box(rx.text("Students", weight="bold", size="2", color="#111827"), width="150px", flex_shrink="0"), 
        rx.box(rx.text("Section", weight="bold", size="2", color="#111827"), width="90px", flex_shrink="0"),
        rx.box(rx.text("Dates/Time", weight="bold", size="2", color="#111827"), width="150px", flex_shrink="0"), 
        rx.box(rx.text("Approval", weight="bold", size="2", color="#111827"), width="170px", flex_shrink="0"),
        rx.box(rx.text("Location", weight="bold", size="2", color="#111827"), width="90px", flex_shrink="0"), 
        rx.box(rx.text("Visit reason", weight="bold", size="2", color="#111827"), flex="1", min_width="120px"),
        padding_bottom="1", width="100%", align="center"
    )

def table_row(student, section, datetime, status, location, reason) -> rx.Component:
    return rx.hstack(
        rx.box(rx.text(student, size="2", color="#374151"), width="150px", flex_shrink="0"),
        rx.box(rx.text(section, size="2", color="#374151"), width="90px", flex_shrink="0"),
        rx.box(rx.text(datetime, size="1", color="#374151"), width="150px", flex_shrink="0"),
        rx.box(rx.hstack(status_badge(status), action_icons(status), spacing="2"), width="170px", flex_shrink="0"),
        rx.box(rx.text(location, size="2", color="#374151"), width="90px", flex_shrink="0"),
        rx.box(rx.text(reason, size="2", color="#374151"), flex="1", min_width="120px"),
        align="center", padding_y="3", width="100%"
    )

# ==========================================
# 4. TAB VIEWS 
# ==========================================
def overview_view() -> rx.Component:
    """Tab 1: Overview - Using the Student Dashboard Layout Structure"""
    return rx.hstack(
        # Left Card: Upcoming Work Context
        rx.box(
            rx.vstack(
                rx.heading("Upcoming Work Context", size="4", font_weight="700", color="#111827", margin_bottom="8px"),
                rx.grid(
                    _context_tile("5", "Confirmed Appointments", "#FDE8E8"), # Pinkish
                    _context_tile("3", "Blocked Time Slots", "#FEF9C3"), # Yellowish
                    _context_tile("2", "Open Available Slots", "#E0F2FE"), # Blueish
                    _context_tile("1", "Completed Session", "#DCFCE7"), # Greenish
                    columns="2", spacing="4", width="100%"
                ),
                spacing="3", align_items="start", width="100%"
            ),
            background_color="white", border="1px solid #E6DEC8", border_radius="14px", 
            padding="28px", width="380px", min_height="440px"
        ),
        
        # Right Card: Approval Table
        rx.box(
            rx.vstack(
                table_header(),
                rx.text("Approval Quick View", size="1", color="#6B7280", margin_bottom="2"),
                rx.vstack(
                    table_row("Stud. James Reid", "BSIT - 1A", "Oct 7 - 7:40 am", "Requested", "Eng 412", "Draft review"),
                    table_row("Stud. James Reid", "BSIT - 2C", "Oct 7 - 12:00 pm", "Requested", "Zoom", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSCS - 2A", "Oct 8 - 12:00 pm", "Requested", "Lab 2B", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSCS - 2B", "Oct 8 - 9:00 am", "Cancelled", "Lab 2B", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSIS - 1C", "Oct 8 - 12:00 pm", "Confirmed", "Lab 2B", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSIS - 2B", "Oct 8 - 12:00 pm", "Confirmed", "Lab 2B", "Schedule discussion"),
                    table_row("Stud. James Reid", "BSIS - 4A", "Oct 9 - 9:00 am", "Confirmed", "Lab 2B", "Schedule discussion"),
                    spacing="0", width="100%"
                ),
                width="100%"
            ),
            background_color="white", border="1px solid #E6DEC8", border_radius="14px", 
            padding="28px", width="850px", min_height="440px"
        ),
        spacing="6", 
        align="stretch", # Forces both boxes to scale to equal heights
        justify="center",
        wrap="wrap"
    )

# ==========================================
# 5. MAIN LAYOUT 
# ==========================================
def sidebar_item(text: str, icon_tag: str) -> rx.Component:
    is_active = FacultyState.current_tab == text
    return rx.hstack(
        rx.icon(icon_tag, size=18, color=rx.cond(is_active, "#927345", "#6B7280")),
        rx.text(text, weight=rx.cond(is_active, "bold", "regular"), size="2", color=rx.cond(is_active, "#111827", "#4B5563")),
        background_color=rx.cond(is_active, "#F3E8D6", "transparent"),
        padding="3", border_radius="8px", width="100%", align="center", cursor="pointer",
        on_click=FacultyState.set_tab(text)
    )

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.avatar(fallback="Prof", color_scheme="blue", size="3", radius="full"),
            rx.vstack(
                rx.text("Prof. Elena Cruz", weight="bold", size="2", color="#111827"),
                rx.text("elena.cruz@university.edu", size="1", color="#6B7280"),
                spacing="0"
            ),
            padding="3", border="1px solid #E5E7EB", border_radius="12px", margin_bottom="4", bg="white", width="100%"
        ),
        sidebar_item("Overview", "layout-grid"),
        sidebar_item("View all Confirmed Appointments", "calendar-check"),
        sidebar_item("Approval", "file-check-2"),
        sidebar_item("Actions", "sliders-horizontal"),
        
        rx.spacer(),
        rx.hstack(rx.icon("log-out", size=18, color="#111827"), rx.text("Sign out", weight="bold", size="2", color="#111827"), padding="3", width="100%", align="center", cursor="pointer"),
        height="100vh", width="260px", padding="4", bg="#FCFBFA", border_right="1px solid #E5E7EB", flex_shrink="0"
    )

def dashboard_view() -> rx.Component:
    return rx.hstack(
        # 1. Left Sidebar
        sidebar(),
        
        # 2. Main Layout Area (Exactly mirroring the student structure)
        rx.vstack(
            top_header(),
            
            # The Content Box below the header centered beautifully
            rx.center(
                rx.match(
                    FacultyState.current_tab,
                    ("Overview", overview_view()),
                    overview_view() 
                ),
                width="100%",
                flex="1",
                padding="40px", 
            ),
            
            flex="1",
            height="100vh",
            overflow_y="auto",
            background_color="#FAF6EE",
            spacing="0",
        ),
        
        width="100%",
        height="100vh",
        spacing="0",
    )

@rx.page(
    route="/dashboard", 
    title="Faculty Dashboard | Mochichi"
)
def dashboard_page() -> rx.Component:
    return rx.box(
        rx.html("<style>body { margin: 0; padding: 0; background-color: #FAF6EE; }</style>"),
        dashboard_view(),
    )