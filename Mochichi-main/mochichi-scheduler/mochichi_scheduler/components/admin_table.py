import reflex as rx
from typing import Callable, Any


def _role_badge(role: rx.Var[str]) -> rx.Component:
    return rx.cond(
        role == "Faculty",
        rx.badge("Faculty", color_scheme="amber"),
        rx.cond(
            role == "Admin",
            rx.badge("Admin", color_scheme="purple"),
            rx.badge("Student", color_scheme="blue"),
        ),
    )


def _user_row(
    account: dict[str, Any],
    on_toggle: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.table.row(
        rx.table.cell(account["display_id"]),
        rx.table.cell(
            rx.vstack(
                rx.text(
                    account["full_name"],
                    font_weight="bold",
                    font_size="13px",
                ),
                _role_badge(account["role_label"]),
                align="start",
                spacing="1",
            )
        ),
        rx.table.cell(account["department"]),
        rx.table.cell(account["email"]),
        rx.table.cell(
            rx.switch(
                # THE FIX: Cast the dictionary string value to a strict boolean
                checked=account["is_active"].to(bool),
                color_scheme="jade",
                disabled=is_loading,
                on_change=(
                    lambda checked: on_toggle(
                        account["display_id"], checked
                    )
                ) if on_toggle is not None else None,
            )
        ),
    )


def admin_user_table(
    users: list[dict[str, Any]],
    on_toggle: Callable | None = None,
    is_loading: bool | rx.Var[bool] = False,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("User Directory Management", size="5"),
            rx.text(
                "Manage registered student, faculty, and admin accounts.",
                color="#6B7280",
                font_size="12px",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("USER ID"),
                        rx.table.column_header_cell("NAME & ROLE"),
                        rx.table.column_header_cell("DEPARTMENT"),
                        rx.table.column_header_cell("EMAIL ACCOUNT"),
                        rx.table.column_header_cell("ACTIVE"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        users,
                        lambda account: _user_row(
                            account,
                            on_toggle,
                            is_loading,
                        ),
                    )
                ),
                width="100%",
                variant="surface",
            ),
            width="100%",
            spacing="3",
        ),
        width="100%",
        padding="20px",
        background="white",
        border_radius="12px",
        border="1px solid #E6DEC8",
    )