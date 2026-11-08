import reflex as rx
from ..state import BaseState
from ..components.sidebar import sidebar

def quick_action_card(icon_name: str, label: str) -> rx.Component:
    return rx.hstack(
        rx.icon(icon_name, size=16, color="#a33"),
        rx.text(label, font_size="13px", font_weight="500", color="#222"),
        spacing="3",
        align="center",
        padding="12px",
        background_color="#fff5f5",
        border_radius="8px",
        width="100%",
        cursor="pointer",
        _hover={"background_color": "#ffebeb"},
    )

def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.badge(
        status,
        color_scheme=rx.cond(
            status == "Confirmed",
            "green",
            rx.cond(
                status == "Requested",
                "yellow",
                rx.cond(status == "Pending", "orange", "gray"),
            ),
        ),
        variant="soft",
    )

def faculty_card(faculty: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.avatar(fallback="PK", size="2"),
                rx.vstack(
                    rx.text(faculty["name"], font_weight="bold", font_size="13px", color="#111"),
                    rx.text(faculty["dept"], color="#444", font_size="11px"),
                    spacing="0",
                    align_items="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.vstack(
                rx.text("Visit Reason Summary", color="#444", font_size="10px", font_weight="600"),
                rx.text(faculty["summary"], font_size="12px", font_weight="600", color="#222"),
                spacing="1",
                align_items="start",
            ),
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background_color=faculty["color"],
                ),
                rx.text(faculty["status"], font_size="11px", color="#333", font_weight="500"),
                spacing="2",
                align="center",
            ),
            spacing="3",
            align_items="start",
        ),
        background_color="white",
        border="1px solid #e6dec9",
        border_radius="10px",
        padding="14px",
        width="210px",
        height="220px",
    )

def dashboard_view() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            # Top Header
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.text("M", color="white", font_weight="bold", font_size="12px"),
                        background_color="#a33",
                        padding="4px 8px",
                        border_radius="4px",
                    ),
                    rx.text("Mochichi Scheduler", font_weight="600", font_size="14px", color="#111"),
                    rx.badge("Dashboard", variant="soft", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                rx.hstack(
                    rx.icon("bell", size=18, color="#444"),
                    rx.box(
                        rx.text(
                            BaseState.user_initials,
                            color="white",
                            font_weight="bold",
                            font_size="10px",
                        ),
                        background_color="#2c2c2c",
                        width="36px",
                        height="26px",
                        border_radius="6px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        padding_x="6px",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="12px 24px",
                background_color="white",
                border_bottom="1px solid #e6dec9",
                justify_content="space-between",
            ),
            # Main Scrollable Body
            rx.vstack(
                # Section 1: Dashboard Cards Row
                rx.hstack(
                    # Weekly Schedule Card
                    rx.box(
                        rx.vstack(
                            rx.text("Weekly Schedule & Slots", font_weight="bold", font_size="14px", color="#222"),
                            rx.text("Current Week Open Advising", font_size="12px", color="#555", font_weight="500"),
                            rx.vstack(
                                rx.foreach(
                                    BaseState.weekly_slots,
                                    lambda slot: rx.hstack(
                                        rx.vstack(
                                            rx.text(slot["day"], font_weight="bold", font_size="12px", color="#222"),
                                            rx.text(slot["time"], font_size="11px", color="#444"),
                                            spacing="0",
                                            align_items="start",
                                        ),
                                        rx.badge(
                                            slot["status"],
                                            color_scheme=rx.cond(slot["status"] == "Open", "green", "gray"),
                                            size="1",
                                        ),
                                        width="100%",
                                        justify_content="space-between",
                                        align="center",
                                        padding="8px 12px",
                                        border_radius="6px",
                                        background_color="#f9f9f9",
                                    ),
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        background_color="white",
                        border="1px solid #e6dec9",
                        border_radius="12px",
                        padding="16px",
                        flex="1",
                    ),
                    # Student Specific Context Card
                    rx.box(
                        rx.vstack(
                            rx.text("Student-Specific Context", font_weight="bold", font_size="14px", color="#222"),
                            rx.grid(
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(rx.icon("calendar", size=16, color="#333"), rx.text("5", font_weight="bold", font_size="18px", color="#111")),
                                        rx.text("Confirmed", font_size="11px", color="#333", font_weight="500"),
                                    ),
                                    padding="12px",
                                    background_color="#ffebee",
                                    border_radius="8px",
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(rx.icon("clock", size=16, color="#333"), rx.text("3", font_weight="bold", font_size="18px", color="#111")),
                                        rx.text("Requested", font_size="11px", color="#333", font_weight="500"),
                                    ),
                                    padding="12px",
                                    background_color="#fffde7",
                                    border_radius="8px",
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(rx.icon("help-circle", size=16, color="#333"), rx.text("1", font_weight="bold", font_size="18px", color="#111")),
                                        rx.text("Pending", font_size="11px", color="#333", font_weight="500"),
                                    ),
                                    padding="12px",
                                    background_color="#e1f5fe",
                                    border_radius="8px",
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(rx.icon("help-circle", size=16, color="#333"), rx.text("1", font_weight="bold", font_size="18px", color="#111")),
                                        rx.text("Cancelled", font_size="11px", color="#333", font_weight="500"),
                                    ),
                                    padding="12px",
                                    background_color="#ffebee",
                                    border_radius="8px",
                                ),
                                columns="2",
                                spacing="3",
                                width="100%",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        background_color="white",
                        border="1px solid #e6dec9",
                        border_radius="12px",
                        padding="16px",
                        flex="1",
                    ),
                    # Upcoming Appointments Table Card
                    rx.box(
                        rx.vstack(
                            rx.text("Your upcoming appointments", font_weight="bold", font_size="14px", color="#222"),
                            rx.text("8 THIS FORTNIGHT", font_size="10px", color="#444", font_weight="bold"),
                            rx.vstack(
                                rx.foreach(
                                    BaseState.upcoming_appointments,
                                    lambda appt: rx.hstack(
                                        rx.text(appt["prof"], font_size="11px", font_weight="500", color="#222", width="90px"),
                                        rx.text(appt["date"], font_size="11px", color="#444", width="100px"),
                                        status_badge(appt["status"]),
                                        rx.text(appt["location"], font_size="11px", color="#444", width="70px"),
                                        rx.text(appt["reason"], font_size="11px", color="#333", width="100px"),
                                        width="100%",
                                        justify_content="space-between",
                                        align="center",
                                        padding_y="4px",
                                        border_bottom="1px solid #f0f0f0",
                                    ),
                                ),
                                spacing="1",
                                width="100%",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        background_color="white",
                        border="1px solid #e6dec9",
                        border_radius="12px",
                        padding="16px",
                        flex="2",
                    ),
                    # Quick Actions Card
                    rx.box(
                        rx.vstack(
                            rx.text("Quick Actions & Updates", font_weight="bold", font_size="14px", color="#222"),
                            quick_action_card("calendar-plus", "Start a new request"),
                            quick_action_card("calendar-clock", "Request rescheduling"),
                            quick_action_card("help-circle", "Cancel booking request"),
                            spacing="3",
                            width="100%",
                            align_items="start",
                        ),
                        background_color="white",
                        border="1px solid #e6dec9",
                        border_radius="12px",
                        padding="16px",
                        flex="1",
                    ),
                    width="100%",
                    spacing="4",
                    align_items="stretch",
                ),
                # Section 2: Professor Status Quick View Grid
                rx.box(
                    rx.vstack(
                        rx.text("Professor Status Quick View", font_weight="bold", font_size="14px", color="#222"),
                        rx.hstack(
                            rx.foreach(
                                BaseState.faculty_list,
                                lambda faculty: faculty_card(faculty),
                            ),
                            spacing="3",
                            width="100%",
                            overflow_x="auto",
                        ),
                        spacing="3",
                        align_items="start",
                    ),
                    background_color="white",
                    border="1px solid #e6dec9",
                    border_radius="12px",
                    padding="16px",
                    width="100%",
                ),
                width="100%",
                padding="24px",
                spacing="5",
            ),
            flex="1",
            height="100vh",
            overflow_y="auto",
            background_color="#FAF6EE",
        ),
        width="100%",
        height="100vh",
        spacing="0",
    )