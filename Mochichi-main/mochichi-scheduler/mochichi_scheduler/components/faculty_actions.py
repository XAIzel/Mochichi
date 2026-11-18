import reflex as rx
from typing import Callable


def faculty_status_selector(
    status: str | rx.Var[str] = "Available",
    on_status_change: Callable | None = None,
) -> rx.Component:
    return rx.vstack(
        rx.heading("Availability Status", size="4"),
        rx.text(
            "Set your current availability for students.",
            color="#6B7280",
            font_size="13px",
        ),
        rx.select(
            [
                "Available",
                "In Class",
                "Busy",
                "Do Not Disturb",
                "Out of Office",
            ],
            value=status,
            on_change=on_status_change,
            placeholder="Select your status",
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding="20px",
        background="white",
        border_radius="12px",
        border="1px solid #E6DEC8",
    )


def open_slots_form(
    date_value: str | rx.Var[str] = "",
    start_time_value: str | rx.Var[str] = "",
    end_time_value: str | rx.Var[str] = "",
    on_date_change: Callable | None = None,
    on_start_time_change: Callable | None = None,
    on_end_time_change: Callable | None = None,
    on_publish: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.vstack(
        rx.heading("Publish Open Time Slots", size="4"),
        rx.text(
            "Let students know when you're available for appointments.",
            color="#6B7280",
            font_size="13px",
        ),
        rx.input(
            placeholder="Select date",
            type="date",
            value=date_value,
            on_change=on_date_change,
            width="100%",
        ),
        rx.hstack(
            rx.input(
                placeholder="Start time",
                type="time",
                value=start_time_value,
                on_change=on_start_time_change,
                width="100%",
            ),
            rx.input(
                placeholder="End time",
                type="time",
                value=end_time_value,
                on_change=on_end_time_change,
                width="100%",
            ),
            width="100%",
        ),
        rx.button(
            rx.cond(
                is_loading,
                rx.hstack(
                    rx.spinner(size="1"),
                    rx.text("Publishing..."),
                ),
                rx.text("Publish Availability"),
            ),
            color_scheme="jade",
            width="100%",
            loading=is_loading,
            disabled=is_loading,
            on_click=on_publish,
        ),
        spacing="3",
        width="100%",
        padding="20px",
        background="white",
        border_radius="12px",
        border="1px solid #E6DEC8",
    )


def faculty_actions(
    status: str | rx.Var[str] = "Available",
    on_status_change: Callable | None = None,
    date_value: str | rx.Var[str] = "",
    start_time_value: str | rx.Var[str] = "",
    end_time_value: str | rx.Var[str] = "",
    on_date_change: Callable | None = None,
    on_start_time_change: Callable | None = None,
    on_end_time_change: Callable | None = None,
    on_publish: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.vstack(
        faculty_status_selector(
            status=status,
            on_status_change=on_status_change,
        ),
        open_slots_form(
            date_value=date_value,
            start_time_value=start_time_value,
            end_time_value=end_time_value,
            on_date_change=on_date_change,
            on_start_time_change=on_start_time_change,
            on_end_time_change=on_end_time_change,
            on_publish=on_publish,
            is_loading=is_loading,
        ),
        spacing="4",
        width="100%",
    )