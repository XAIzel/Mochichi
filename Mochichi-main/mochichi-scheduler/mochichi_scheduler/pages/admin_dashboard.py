import reflex as rx
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar


def _role_pill(role: rx.Var[str]) -> rx.Component:
    """Renders soft yellow 'Faculty' or soft blue 'Student' role pill matching Figma."""
    return rx.cond(
        role == "Faculty",
        rx.box(
            rx.text("Faculty", font_size="10px", font_weight="600", color="#92400E"),
            background_color="#FEF3C7",
            padding_x="8px",
            padding_y="2px",
            border_radius="6px",
        ),
        rx.box(
            rx.text("Student", font_size="10px", font_weight="600", color="#1E40AF"),
            background_color="#DBEAFE",
            padding_x="8px",
            padding_y="2px",
            border_radius="6px",
        ),
    )


def _directory_row(account: dict[str, str]) -> rx.Component:
    """Single row inside the Admin User Directory table matching Figma."""
    return rx.hstack(
        # USER ID column
        rx.text(
            account["display_id"],
            font_size="11px",
            font_family="monospace",
            color="#6B7280",
            width="110px",
            flex_shrink="0",
        ),
        # NAME & ROLE column
        rx.vstack(
            rx.text(
                account["full_name"],
                font_size="13px",
                font_weight="700",
                color="#111827",
                line_height="1.2",
            ),
            rx.hstack(
                _role_pill(account["role_label"]),
                rx.text(
                    "•  " + account["department"],
                    font_size="11px",
                    color="#6B7280",
                ),
                spacing="2",
                align="center",
            ),
            spacing="1",
            align_items="start",
            width="280px",
            flex_shrink="0",
        ),
        # EMAIL ACCOUNT column
        rx.text(
            account["email"],
            font_size="11px",
            font_family="monospace",
            color="#374151",
            flex="1",
        ),
        # ACTIVE toggle switch column (UI shell now; wired to Supabase update in Phase 2)
        rx.box(
            rx.switch(
                checked=account["is_active"] == "true",
                color_scheme="jade",
                size="2",
            ),
            width="70px",
            display="flex",
            justify_content="center",
        ),
        width="100%",
        padding_y="14px",
        padding_x="12px",
        border_bottom="1px solid #F3EFE6",
        align="center",
    )


@rx.page(route="/admin-dashboard")
def admin_dashboard_view() -> rx.Component:
    """Admin 'User Directory Management' screen matching the finalized Figma UI."""
    return rx.hstack(
        sidebar(active_page="User Directory"),
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
            # Centered User Directory Card
            rx.center(
                rx.box(
                    rx.vstack(
                        # Card Title & Subtitle
                        rx.vstack(
                            rx.heading(
                                "User Directory Management",
                                size="5",
                                font_weight="700",
                                color="#111827",
                            ),
                            rx.text(
                                "All Accounts: 6 accounts",
                                font_size="12px",
                                color="#6B7280",
                            ),
                            spacing="1",
                            align_items="start",
                            width="100%",
                            margin_bottom="12px",
                        ),
                        # Table Header Row
                        rx.hstack(
                            rx.text(
                                "USER ID",
                                font_size="10px",
                                font_weight="700",
                                color="#6B7280",
                                letter_spacing="0.05em",
                                width="110px",
                            ),
                            rx.text(
                                "NAME & ROLE",
                                font_size="10px",
                                font_weight="700",
                                color="#6B7280",
                                letter_spacing="0.05em",
                                width="280px",
                            ),
                            rx.text(
                                "EMAIL ACCOUNT",
                                font_size="10px",
                                font_weight="700",
                                color="#6B7280",
                                letter_spacing="0.05em",
                                flex="1",
                            ),
                            rx.text(
                                "ACTIVE",
                                font_size="10px",
                                font_weight="700",
                                color="#6B7280",
                                letter_spacing="0.05em",
                                width="70px",
                                text_align="center",
                            ),
                            width="100%",
                            padding_y="10px",
                            padding_x="12px",
                            border_top="1px solid #EDE8DE",
                            border_bottom="1px solid #EDE8DE",
                        ),
                        # Directory Rows
                        rx.vstack(
                            rx.foreach(BaseState.admin_directory_users, _directory_row),
                            spacing="0",
                            width="100%",
                        ),
                        spacing="0",
                        width="100%",
                    ),
                    background_color="white",
                    border="1px solid #E6DEC8",
                    border_radius="16px",
                    padding="28px 32px",
                    width="100%",
                    max_width="820px",
                ),
                width="100%",
                padding="36px",
                flex="1",
                align_items="start",
            ),
            flex="1",
            height="100vh",
            overflow_y="auto",
            background_color="#FAF6EE",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        spacing="0",
    )