import reflex as rx
from typing import Callable, Any


def stat_card(title: str, value: str | rx.Var) -> rx.Component:
    return rx.box(
        rx.text(title, color="#6B7280", font_size="13px"),
        rx.heading(value, size="7", color="#26352D"),
        padding="20px",
        background="white",
        border="1px solid #E6DEC8",
        border_radius="12px",
        width="100%",
    )


def booking_row(
    booking: dict[str, Any],
    on_confirm: Callable | None = None,
    on_cancel: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    is_confirmed = booking["status"] == "Confirmed"
    is_cancelled = booking["status"] == "Cancelled"

    return rx.table.row(
        rx.table.cell(booking["student"]),
        rx.table.cell(booking["date"]),
        rx.table.cell(booking["time"]),
        rx.table.cell(
            rx.badge(
                booking["status"],
                color_scheme=rx.cond(
                    is_confirmed,
                    "jade",
                    rx.cond(is_cancelled, "red", "amber"),
                ),
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Confirm",
                    color_scheme="jade",
                    size="1",
                    loading=is_loading,
                    disabled=is_confirmed or is_cancelled or is_loading,
                    on_click=(
                        lambda: on_confirm(booking["id"])
                    ) if on_confirm is not None else None,
                ),
                rx.button(
                    "Cancel",
                    color_scheme="red",
                    variant="soft",
                    size="1",
                    loading=is_loading,
                    disabled=is_cancelled or is_loading,
                    on_click=(
                        lambda: on_cancel(booking["id"])
                    ) if on_cancel is not None else None,
                ),
                spacing="2",
            )
        ),
    )


def booking_requests_table(
    bookings: list[dict[str, Any]],
    on_confirm: Callable | None = None,
    on_cancel: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Booking Requests", size="4"),
            rx.cond(
                bookings.length() > 0,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("STUDENT"),
                            rx.table.column_header_cell("DATE"),
                            rx.table.column_header_cell("TIME"),
                            rx.table.column_header_cell("STATUS"),
                            rx.table.column_header_cell("ACTIONS"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            bookings,
                            lambda booking: booking_row(
                                booking,
                                on_confirm,
                                on_cancel,
                                is_loading,
                            ),
                        )
                    ),
                    width="100%",
                ),
                rx.text(
                    "No booking requests available yet.",
                    color="#6B7280",
                    padding="20px",
                    text_align="center",
                    width="100%",
                ),
            ),
            width="100%",
            spacing="3",
        ),
        padding="20px",
        background="white",
        border="1px solid #E6DEC8",
        border_radius="12px",
        width="100%",
    )


def faculty_summary(
    confirmed: str | rx.Var,
    open_slots: str | rx.Var,
    bookings: list[dict[str, Any]],
    on_confirm: Callable | None = None,
    on_cancel: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Confirmed Bookings", confirmed),
            stat_card("Open Slots", open_slots),
            columns="2",
            spacing="3",
            width="100%",
        ),
        booking_requests_table(
            bookings,
            on_confirm,
            on_cancel,
            is_loading,
        ),
        width="100%",
        spacing="4",
    )