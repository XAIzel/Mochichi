import reflex as rx
from mochichi_scheduler.state import BaseState


def sidebar_item(
    icon: str,
    text: str,
    url: str,
    active: bool | rx.Var[bool] = False,
    on_click=None,
) -> rx.Component:
    """Single navigation link styled to match the Mochichi Figma sidebar."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=17, color=rx.cond(active, "#a33", "#2c2c2c")),
            rx.text(
                text,
                font_weight=rx.cond(active, "600", "500"),
                font_size="13px",
                color=rx.cond(active, "#1a1a1a", "#374151"),
                line_height="1.3",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        href=url,
        on_click=on_click,
        width="100%",
        padding="10px 12px",
        border_radius="8px",
        background_color=rx.cond(active, "#f3ece0", "transparent"),
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


def _student_nav(active_page: str | rx.Var[str]) -> rx.Component:
    """Student navigation items matching the Student Figma screens."""
    return rx.vstack(
        sidebar_item(
            "layout-dashboard",
            "Overview",
            "/dashboard",
            active=(active_page == "Overview"),
        ),
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


def _faculty_nav(active_page: str | rx.Var[str]) -> rx.Component:
    """Faculty navigation items matching the Faculty Figma screens."""
    # Local import prevents circular import with faculty_dashboard.py
    from mochichi_scheduler.pages.faculty_dashboard import FacultyState

    return rx.vstack(
        sidebar_item(
            "layout-dashboard",
            "Overview",
            "/faculty-dashboard",
            active=(active_page == "Overview"),
            on_click=FacultyState.set_tab("Overview"),
        ),
        sidebar_item(
            "clipboard-check",
            "View all Confirmed Appointments",
            "/faculty-dashboard",
            active=(active_page == "View all Confirmed Appointments"),
            on_click=FacultyState.set_tab("View all Confirmed Appointments"),
        ),
        sidebar_item(
            "user-check",
            "Approval",
            "/faculty-dashboard",
            active=(active_page == "Approval"),
            on_click=FacultyState.set_tab("Approval"),
        ),
        sidebar_item(
            "sliders-horizontal",
            "Actions",
            "/faculty-dashboard",
            active=(active_page == "Actions"),
            on_click=FacultyState.set_tab("Actions"),
        ),
        spacing="1",
        width="100%",
    )


def _admin_nav(active_page: str | rx.Var[str]) -> rx.Component:
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


def sidebar(active_page: str | rx.Var[str] = "Overview") -> rx.Component:
    """Role-aware persistent sidebar for Student, Faculty, and Admin views."""
    # Local import prevents circular import: log_in_sign_in -> dashboard -> sidebar -> log_in_sign_in
    from mochichi_scheduler.pages.log_in_sign_in import State

    return rx.vstack(
        # Static Profile Header Card
        rx.hstack(
            _profile_badge(),
            rx.vstack(
                rx.text(
                    rx.cond(BaseState.user_name != "", BaseState.user_name, "User"),
                    font_weight="600",
                    font_size="13px",
                    color="#1a1a1a",
                    line_height="1.2",
                ),
                rx.text(
                    rx.cond(
                        BaseState.user_email != "",
                        BaseState.user_email,
                        "user@lspu.edu.ph",
                    ),
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

        # Bottom Sign Out Action (Clears auth state & redirects to /login)
        rx.vstack(
            rx.hstack(
                rx.icon("log-out", size=17, color="#2c2c2c"),
                rx.text(
                    "Sign out",
                    font_weight="500",
                    font_size="13px",
                    color="#374151",
                    line_height="1.3",
                ),
                spacing="3",
                width="100%",
                align="center",
                padding="10px 12px",
                border_radius="8px",
                cursor="pointer",
                _hover={"background_color": "#f3ece0"},
                on_click=State.handle_logout,
            ),
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