import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar


def _metric_tile(icon_name: str, count: rx.Var[int], label: str, bg_color: str) -> rx.Component:
    """Single status metric tile inside 'Student-Specific Context'."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(icon_name, size=15, color="#111827"),
                rx.text(
                    count,
                    font_weight="700",
                    font_size="22px",
                    color="#111827",
                    line_height="1",
                ),
                align="center",
                spacing="4",
            ),
            rx.text(label, font_size="12px", color="#374151", font_weight="500"),
            spacing="4",
            align_items="start",
        ),
        padding="18px 20px",
        background_color=bg_color,
        border_radius="12px",
        width="100%",
    )


def _quick_action_item(icon_name: str, label: str, target_route: str) -> rx.Component:
    """Clickable soft-pink action row inside 'Quick Actions & Updates'."""
    return rx.hstack(
        rx.icon(icon_name, size=16, color="#C03928"),
        rx.text(label, font_size="13px", font_weight="500", color="#1F2937"),
        width="100%",
        padding="14px 18px",
        background_color="#FDF2F2",
        border_radius="10px",
        align="center",
        spacing="4",
        cursor="pointer",
        _hover={"background_color": "#FCE7E7"},
        on_click=rx.redirect(target_route),
    )


def dashboard_view() -> rx.Component:
    """Student Overview Dashboard matching the finalized Figma UI."""
    return rx.hstack(
        sidebar(active_page="Overview"),
        rx.vstack(
            # Top Header Bar (Matches admin_dashboard.py & Student Figma shell)
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
            # Centered Two-Card Overview Section
            rx.center(
                rx.hstack(
                    # Left Card: Student-Specific Context
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Student-Specific Context",
                                size="4",
                                font_weight="700",
                                color="#111827",
                                margin_bottom="14px",
                            ),
                            rx.grid(
                                _metric_tile(
                                    "square-dot",
                                    BaseState.student_confirmed_count,
                                    "Confirmed",
                                    "#FCE8E8",
                                ),
                                _metric_tile(
                                    "clock",
                                    BaseState.student_requested_count,
                                    "Requested",
                                    "#FEF9D7",
                                ),
                                _metric_tile(
                                    "info",
                                    BaseState.student_pending_count,
                                    "Pending",
                                    "#E1F0FA",
                                ),
                                _metric_tile(
                                    "info",
                                    BaseState.student_cancelled_count,
                                    "Cancelled",
                                    "#FCE8E8",
                                ),
                                columns="2",
                                spacing="4",
                                width="100%",
                            ),
                            spacing="3",
                            align_items="start",
                            width="100%",
                        ),
                        background_color="white",
                        border="1px solid #E6DEC8",
                        border_radius="16px",
                        padding="32px",
                        width="375px",
                        min_height="460px",
                    ),
                    # Right Card: Quick Actions & Updates
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Quick Actions & Updates",
                                size="4",
                                font_weight="700",
                                color="#111827",
                                margin_bottom="14px",
                            ),
                            rx.vstack(
                                _quick_action_item(
                                    "square-dot",
                                    "Start a new request",
                                    "/mochichi",
                                ),
                                _quick_action_item(
                                    "clock",
                                    "Request rescheduling",
                                    "/appointments",
                                ),
                                _quick_action_item(
                                    "info",
                                    "Cancel booking request",
                                    "/appointments",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            spacing="3",
                            align_items="start",
                            width="100%",
                        ),
                        background_color="white",
                        border="1px solid #E6DEC8",
                        border_radius="16px",
                        padding="32px",
                        width="375px",
                        min_height="460px",
                    ),
                    spacing="7",
                    align="stretch",
                    justify="center",
                    wrap="wrap",
                ),
                width="100%",
                padding="48px 36px",
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


@rx.page(route="/dashboard", title="Student Dashboard | Mochichi")
def dashboard_page() -> rx.Component:
    return dashboard_view()