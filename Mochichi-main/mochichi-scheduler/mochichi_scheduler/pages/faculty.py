import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar

def faculty_card(prof: dict) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.text("PK", color="white", font_weight="bold"), 
                background_color="#333", 
                width="40px", 
                height="40px", 
                border_radius="50%", 
                display="flex", 
                align_items="center", 
                justify_content="center"
            ),
            rx.vstack(
                rx.text(prof["name"], font_weight="bold", font_size="14px"),
                rx.text(f"Department: {prof['dept']}", font_size="12px", color="#666"),
                spacing="0", 
                align_items="start",
            ),
        ),
        rx.text(f"Focus: {prof['summary']}", font_size="12px", color="#444"),
        rx.badge(prof["status"], color_scheme="green"),
        background_color="white", padding="16px", border_radius="10px", border="1px solid #e6dec9", width="100%",
    )

@rx.page(route="/faculty")
def faculty_page() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.heading("CCS Faculty Directory", font_size="24px", font_weight="bold", color="#1a1a1a"),
            rx.text("Browse all available department professors across CS, IT, and IS programs.", font_size="13px", color="#666"),
            
            rx.grid(
                rx.foreach(BaseState.faculty_list, faculty_card),
                columns="3", spacing="4", width="100%",
            ),
            width="100%", height="100vh", overflow_y="auto", background_color="#fcfbfa", padding="32px",
        ),
        width="100vw", height="100vh", spacing="0",
    )