import reflex as rx
from mochichi_scheduler.components.sidebar import sidebar

@rx.page(route="/mochichi")
def mochichi_page() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.heading("Mochichi AI Assistant", font_size="24px", font_weight="bold", color="#1a1a1a"),
            rx.text("Ask Mochichi anything regarding professor availability or schedule optimization.", font_size="13px", color="#666"),
            
            rx.box(
                rx.text("Mochichi chat interface window placeholder...", font_size="14px", color="#888"),
                background_color="white", padding="40px", border_radius="12px", border="1px solid #e6dec9", width="100%", height="60vh",
                display="flex", align_items="center", justify_content="center",
            ),
            width="100%", height="100vh", overflow_y="auto", background_color="#fcfbfa", padding="32px",
        ),
        width="100vw", height="100vh", spacing="0",
    )