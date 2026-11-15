import reflex as rx
from mochichi_scheduler.components.sidebar import sidebar


def _status_badge(status: str) -> rx.Component:
    """Renders status pills matching the Figma design (Requested = yellow, Confirmed = green)."""
    return rx.cond(
        status == "Confirmed",
        rx.box(
            rx.text("Confirmed", font_size="12px", font_weight="500", color="#15803D"),
            bg="#DCFCE7",
            padding_x="14px",
            padding_y="4px",
            border_radius="6px",
            min_width="90px",
            text_align="center",
        ),
        rx.box(
            rx.text(status, font_size="12px", font_weight="500", color="#CA8A04"),
            bg="#FEF9C3",
            padding_x="14px",
            padding_y="4px",
            border_radius="6px",
            min_width="90px",
            text_align="center",
        ),
    )


def _booking_row(
    professor: str,
    datetime_str: str,
    status: str,
    location: str,
    reason: str,
) -> rx.Component:
    """Single row matching the Figma 'Your upcoming bookings' layout."""
    return rx.hstack(
        rx.text(professor, font_size="13px", color="#1F2937", width="140px"),
        rx.text(datetime_str, font_size="13px", color="#374151", width="150px"),
        rx.box(_status_badge(status), width="120px"),
        rx.button(
            "Cancel",
            size="1",
            bg="#FEE2E2",
            color="#B91C1C",
            border_radius="6px",
            padding_x="14px",
            cursor="pointer",
            _hover={"bg": "#FECACA"},
            # Will be wired to State.cancel_appointment in Phase 2, Micro-Slice 4
        ),
        rx.text(location, font_size="13px", color="#374151", width="120px", text_align="center"),
        rx.text(reason, font_size="13px", color="#1F2937", flex="1"),
        width="100%",
        align="center",
        justify="between",
        padding_y="14px",
        border_bottom="1px solid #E5E7EB",
    )


def appointments_page() -> rx.Component:
    """Student 'Upcoming bookings' view matching the finalized Figma UI."""
    return rx.hstack(
        sidebar(active_page="Upcoming bookings"),
        rx.vstack(
            # Top Header Bar
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.text("M", color="white", font_weight="bold", font_size="13px"),
                        bg="#B93829",
                        width="24px",
                        height="24px",
                        border_radius="6px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text("Mochichi Scheduler", font_weight="600", font_size="14px", color="#1F2937"),
                    spacing="2",
                    align="center",
                ),
                width="100%",
                padding_x="24px",
                padding_y="14px",
                bg="white",
                border_bottom="1px solid #EDE8DE",
            ),
            # Centered Main Content Card
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Your upcoming bookings",
                            size="5",
                            font_weight="700",
                            color="#111827",
                            margin_bottom="16px",
                        ),
                        # Placeholder rows matching Figma until Phase 2 Supabase binding
                        _booking_row("Prof. Kumari", "Oct 7 - 7:00 am", "Requested", "Faculty room", "Draft review"),
                        _booking_row("Prof. Kumari", "Oct 8 - 12:00 pm", "Confirmed", "Faculty room", "Schedule discussion"),
                        _booking_row("Prof. Kumari", "Oct 9 - 9:00 am", "Confirmed", "Faculty room", "Schedule discussion"),
                        width="100%",
                        spacing="0",
                    ),
                    bg="white",
                    border="1px solid #E6DEC8",
                    border_radius="14px",
                    padding="32px",
                    width="100%",
                    max_width="860px",
                ),
                width="100%",
                padding="40px",
                flex="1",
                align_items="flex-start",
            ),
            flex="1",
            height="100vh",
            bg="#F9F6EE",
            spacing="0",
        ),
        width="100%",
        spacing="0",
    )