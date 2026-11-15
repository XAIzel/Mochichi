import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar


def _live_status_pill(prof: dict[str, str]) -> rx.Component:
    """Renders the 5-color FR-03 live presence pill matching the Student Faculty Figma UI."""
    pill_bg = rx.match(
        prof["color"],
        ("green", "#22C55E"),
        ("yellow", "#D9E021"),
        ("orange", "#F97316"),
        ("red", "#EF4444"),
        ("purple", "#9333EA"),
        "#22C55E",
    )

    label_text = rx.cond(
        prof["status"] == "Available",
        "Available slots: " + prof["available_slots"],
        prof["status"],
    )

    return rx.hstack(
        rx.box(
            width="6px",
            height="6px",
            border_radius="50%",
            background_color="white",
            flex_shrink="0",
        ),
        rx.text(
            label_text,
            color="white",
            font_size="10px",
            font_weight="600",
            line_height="1.2",
        ),
        background_color=pill_bg,
        padding_x="10px",
        padding_y="3px",
        border_radius="999px",
        spacing="1",
        align="center",
        width="fit-content",
    )


def faculty_card(prof: dict[str, str]) -> rx.Component:
    """Single professor card matching the finalized Student Faculty Directory Figma UI."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Soft Blue Circular 'Prof.' Avatar
                rx.box(
                    rx.text("Prof.", color="#3B82F6", font_weight="700", font_size="13px"),
                    background_color="#DBEAFE",
                    width="48px",
                    height="48px",
                    border_radius="50%",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                # Name, Status Pill, Department, and Conditional CTA
                rx.vstack(
                    rx.text(
                        prof["name"],
                        font_weight="700",
                        font_size="13px",
                        color="#111827",
                    ),
                    _live_status_pill(prof),
                    rx.hstack(
                        rx.icon("building-2", size=12, color="#6B7280"),
                        rx.text(
                            "Department: " + prof["department"],
                            font_size="11px",
                            color="#4B5563",
                        ),
                        spacing="1",
                        align="center",
                        padding_top="2px",
                    ),
                    rx.cond(
                        prof["status"] == "Available",
                        rx.link(
                            rx.button(
                                "Book with Mochichi",
                                size="1",
                                background_color="#D93829",
                                color="white",
                                font_weight="600",
                                font_size="11px",
                                border_radius="6px",
                                padding_x="14px",
                                padding_y="6px",
                                cursor="pointer",
                                _hover={"background_color": "#B91C1C"},
                            ),
                            href="/mochichi",
                            text_decoration="none",
                            margin_top="4px",
                        ),
                    ),
                    spacing="2",
                    align_items="start",
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            width="100%",
            align_items="start",
        ),
        background_color="white",
        border="1px solid #E6DEC8",
        border_radius="12px",
        padding="24px",
        width="100%",
        min_height="165px",
        display="flex",
        align_items="center",
    )


@rx.page(route="/faculty")
def faculty_page() -> rx.Component:
    """Student Faculty Directory view matching the finalized Figma UI."""
    return rx.hstack(
        sidebar(active_page="Faculty"),
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
            # Scrollable 3-Column Faculty Cards Grid
            rx.box(
                rx.grid(
                    rx.foreach(BaseState.faculty_list, faculty_card),
                    columns="3",
                    spacing="5",
                    width="100%",
                    max_width="1120px",
                ),
                width="100%",
                padding="40px",
                display="flex",
                justify_content="center",
                flex="1",
                overflow_y="auto",
            ),
            flex="1",
            height="100vh",
            background_color="#FAF6EE",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        spacing="0",
    )