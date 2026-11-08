import reflex as rx
from mochichi_scheduler.state import BaseState

def sidebar_item(icon: str, text: str, url: str, active: bool = False) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=18, color="#2c2c2c" if not active else "#a33"),
            rx.text(text, font_weight="500", font_size="14px", color="#2c2c2c" if not active else "#1a1a1a"),
            spacing="3",
            width="100%",
            align="center",
        ),
        href=url,
        width="100%",
        padding="10px 12px",
        border_radius="8px",
        background_color="#f3ece0" if active else "transparent",
        _hover={"background_color": "#f3ece0"},
    )

def sidebar() -> rx.Component:
    return rx.vstack(
        # Profile Header Card
        rx.hstack(
            rx.box(
                rx.text(BaseState.user_initials, color="white", font_weight="bold", font_size="12px"),
                background_color="#2c2c2c",
                width="36px",
                height="36px",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(BaseState.user_name, font_weight="600", font_size="13px", color="#1a1a1a"),
                rx.text(BaseState.user_email, font_size="11px", color="#666"),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            padding="12px",
            background_color="white",
            border="1px solid #e6dec9",
            border_radius="10px",
            width="100%",
        ),
        rx.divider(margin_y="4px", border_color="#e6dec9"),
        
        # Navigation Links
        rx.vstack(
            sidebar_item("layout-dashboard", "Overview", "/", active=True),
            sidebar_item("calendar", "Appointments", "/appointments"),
            sidebar_item("users", "Faculty", "/faculty"),
            sidebar_item("bot", "Mochichi", "/mochichi"),
            spacing="1",
            width="100%",
        ),
        
        rx.spacer(),
        
        # Bottom Utilities
        rx.vstack(
            sidebar_item("settings", "Settings", "#"),
            sidebar_item("log-out", "Sign out", "#"), # Ideally this binds to a logout function
            spacing="1",
            width="100%",
        ),
        
        width="260px",
        height="100vh",
        background_color="#faf7f2",
        border_right="1px solid #e6dec9",
        padding="20px 16px",
        position="sticky",
        top="0",
    )