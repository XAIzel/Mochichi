import reflex as rx

def component_name() -> rx.Component:
    return rx.box(
        rx.text("Build the UI here!"),
    )