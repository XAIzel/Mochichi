import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar
from mochichi_scheduler.components.admin_table import admin_user_table


@rx.page(route="/admin-dashboard", on_load=BaseState.load_admin_directory)
def admin_dashboard_view() -> rx.Component:
    """Admin 'User Directory Management' screen using Member 1's component."""
    return rx.hstack(
        sidebar(active_page="User Directory"),
        rx.vstack(
            # Clean Top Header Bar
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.text("M", color="white", font_weight="bold", font_size="13px"),
                        background_color="#B93829",
                        width="24px",
                        height="24px",
                        border_radius="6px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text(
                        "Mochichi Scheduler",
                        font_weight="600",
                        font_size="14px",
                        color="#1F2937",
                    ),
                    spacing="2",
                    align="center",
                ),
                width="100%",
                padding_x="24px",
                padding_y="14px",
                background_color="white",
                border_bottom="1px solid #EDE8DE",
            ),
            # Centered User Directory Card using Member 1's UI Component
            rx.center(
                admin_user_table(
                    users=BaseState.admin_directory_users,
                    on_toggle=BaseState.toggle_user_active,
                    is_loading=BaseState.is_loading,
                ),
                width="100%",
                padding="36px",
                flex="1",
                align_items="start",
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