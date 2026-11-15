import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar


def _chat_bubble(msg: dict[str, str]) -> rx.Component:
    """Renders a single FIFO chat message bubble matching the Mochichi Figma UI."""
    return rx.cond(
        msg["sender"] == "mochichi",
        # Assistant (Mochichi) Bubble on the Left
        rx.hstack(
            rx.box(
                rx.icon("bot", size=20, color="#6B7280"),
                width="34px",
                height="34px",
                border_radius="8px",
                border="1px solid #D1D5DB",
                background_color="white",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            rx.box(
                rx.text(
                    msg["text"],
                    font_size="13px",
                    color="#1F2937",
                    line_height="1.5",
                ),
                background_color="white",
                border="1px solid #D6CFC2",
                border_radius="12px",
                padding="14px 18px",
                max_width="420px",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        # Student Message Bubble on the Right
        rx.hstack(
            rx.spacer(),
            rx.box(
                rx.text(
                    msg["text"],
                    font_size="13px",
                    color="white",
                    line_height="1.5",
                ),
                background_color="#B93829",
                border_radius="12px",
                padding="12px 16px",
                max_width="420px",
            ),
            width="100%",
        ),
    )


@rx.page(route="/mochichi")
def mochichi_page() -> rx.Component:
    """Student 'Mochichi' AI chat shell matching the finalized Figma UI."""
    return rx.hstack(
        sidebar(active_page="Mochichi"),
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
            # Centered Chat Container
            rx.center(
                rx.vstack(
                    # Scrollable Message History Area
                    rx.vstack(
                        rx.foreach(BaseState.chat_messages, _chat_bubble),
                        spacing="4",
                        width="100%",
                        padding="28px",
                        flex="1",
                        overflow_y="auto",
                        background_color="white",
                    ),
                    # Bottom Input Bar matching Figma ("Book with mochichi")
                    rx.hstack(
                        rx.input(
                            placeholder="Book with mochichi",
                            width="100%",
                            height="44px",
                            background_color="white",
                            border="1px solid #D6CFC2",
                            border_radius="10px",
                            padding_x="16px",
                            font_size="13px",
                            color="#1F2937",
                            # Input value & submit handler wired to Gemini SDK in Phase 3, Micro-Slice 1
                        ),
                        rx.button(
                            rx.icon("send", size=16, color="white"),
                            height="44px",
                            padding_x="16px",
                            background_color="#B93829",
                            border_radius="10px",
                            cursor="pointer",
                            _hover={"background_color": "#991B1B"},
                        ),
                        width="100%",
                        padding="16px 20px",
                        background_color="#F7F3E8",
                        border_top="1px solid #E6DEC8",
                        spacing="3",
                        align="center",
                    ),
                    width="100%",
                    max_width="960px",
                    height="calc(100vh - 110px)",
                    border="1px solid #E6DEC8",
                    border_radius="12px",
                    overflow="hidden",
                    spacing="0",
                ),
                width="100%",
                padding="28px",
                flex="1",
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