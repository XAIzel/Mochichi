import reflex as rx
from mochichi_scheduler.state import BaseState


def sidebar_item(icon: str, text: str, url: str, active: bool = False) -> rx.Component:
    """Single navigation link styled to match the Mochichi Figma sidebar."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=17, color="#2c2c2c" if not active else "#a33"),
            rx.text(
                text,
                font_weight="600" if active else "500",
                font_size="13px",
                color="#1a1a1a" if active else "#374151",
                line_height="1.3",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        href=url,
        width="100%",
        padding="10px 12px",
        border_radius="8px",
        background_color="#f3ece0" if active else "transparent",
        text_decoration="none",
        _hover={"background_color": "#f3ece0", "text_decoration": "none"},
    )


def _profile_badge() -> rx.Component:
    """Circular role badge matching Figma: Stud (dark), Prof (blue), Admin (pink)."""
    return rx.match(
        BaseState.user_role,
        (
            "faculty",
            rx.box(
                rx.text("Prof", color="#3B82F6", font_weight="700", font_size="11px"),
                background_color="#DBEAFE",
                width="38px",
                height="38px",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
        ),
        (
            "admin",
            rx.box(
                rx.text("Admin", color="#DB2777", font_weight="700", font_size="10px"),
                background_color="#FCE7F3",
                width="38px",
                height="38px",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
        ),
        # Default: Student ("Stud")
        rx.box(
            rx.text("Stud", color="white", font_weight="700", font_size="11px"),
            background_color="#2c2c2c",
            width="38px",
            height="38px",
            border_radius="50%",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
    )


def _student_nav(active_page: str) -> rx.Component:
    """Student navigation items matching the Student Figma screens."""
    return rx.vstack(
        sidebar_item("layout-dashboard", "Overview", "/", active=(active_page == "Overview")),
        sidebar_item("users", "Faculty", "/faculty", active=(active_page == "Faculty")),
        sidebar_item("bot", "Mochichi", "/mochichi", active=(active_page == "Mochichi")),
        sidebar_item(
            "calendar",
            "Upcoming bookings",
            "/appointments",
            active=(active_page == "Upcoming bookings"),
        ),
        spacing="1",
        width="100%",
    )


def _faculty_nav(active_page: str) -> rx.Component:
    """Faculty navigation items matching the Faculty Figma screens."""
    return rx.vstack(
        sidebar_item(
            "layout-dashboard",
            "Overview",
            "/faculty-dashboard",
            active=(active_page == "Overview"),
        ),
        sidebar_item(
            "clipboard-check",
            "View all Confirmed Appointments",
            "/faculty-confirmed",
            active=(active_page == "View all Confirmed Appointments"),
        ),
        sidebar_item(
            "user-check",
            "Approval",
            "/faculty-approval",
            active=(active_page == "Approval"),
        ),
        sidebar_item(
            "sliders-horizontal",
            "Actions",
            "/faculty-actions",
            active=(active_page == "Actions"),
        ),
        spacing="1",
        width="100%",
    )


def _admin_nav(active_page: str) -> rx.Component:
    """Admin navigation items matching the Admin Figma screen."""
    return rx.vstack(
        sidebar_item(
            "users",
            "User Directory",
            "/admin-dashboard",
            active=(active_page == "User Directory"),
        ),
        spacing="1",
        width="100%",
    )


def sidebar(active_page: str = "Overview") -> rx.Component:
    """Role-aware persistent sidebar for Student, Faculty, and Admin views."""
    return rx.vstack(
        # Static Profile Header Card (No PFP upload/settings modal per finalized scope)
        rx.hstack(
            _profile_badge(),
            rx.vstack(
                rx.text(
                    BaseState.user_name,
                    font_weight="600",
                    font_size="13px",
                    color="#1a1a1a",
                    line_height="1.2",
                ),
                rx.text(
                    BaseState.user_email,
                    font_size="10px",
                    color="#6b7280",
                    line_height="1.2",
                    word_break="break-all",
                ),
                spacing="1",
                align_items="start",
                overflow="hidden",
            ),
            spacing="3",
            padding="12px",
            background_color="white",
            border="1px solid #e6dec9",
            border_radius="10px",
            width="100%",
            align="center",
        ),
        rx.divider(margin_y="6px", border_color="#e6dec9"),

        # Role-Based Navigation Links
        rx.match(
            BaseState.user_role,
            ("faculty", _faculty_nav(active_page)),
            ("admin", _admin_nav(active_page)),
            _student_nav(active_page),
        ),

        rx.spacer(),

        # Bottom Sign Out Action (Wired to Supabase logout in Phase 2, Micro-Slice 1)
        rx.vstack(
            sidebar_item("log-out", "Sign out", "/login", active=False),
            spacing="1",
            width="100%",
        ),

        width="250px",
        min_width="250px",
        height="100vh",
        background_color="#faf7f2",
        border_right="1px solid #e6dec9",
        padding="18px 14px",
        position="sticky",
        top="0",
    )