import reflex as rx
from mochichi_scheduler.pages.dashboard import dashboard_view
from mochichi_scheduler.utils.supabase_client import supabase
from mochichi_scheduler.state import BaseState


class State(BaseState):
    """App state for Mochichi Authentication (Student, Faculty, Admin)."""

    email: str = ""
    password: str = ""
    confirm_password: str = ""
    full_name: str = ""
    role: str = "student"  # 'student' | 'faculty' | 'admin'
    
    auth_error: str = ""
    auth_success: str = ""
    is_logged_in: bool = False
    is_signup_mode: bool = False

    def set_email(self, email: str):
        self.email = email

    def set_password(self, password: str):
        self.password = password

    def set_confirm_password(self, confirm_password: str):
        self.confirm_password = confirm_password

    def set_full_name(self, full_name: str):
        self.full_name = full_name

    def set_role(self, selected_role: str):
        self.role = selected_role

    def toggle_mode(self):
        self.is_signup_mode = not self.is_signup_mode
        self.auth_error = ""
        self.auth_success = ""

    async def submit_action(self):
        """Routes the button click to signup or login."""
        if self.is_signup_mode:
            return await self.handle_signup()
        return await self.handle_login()

    async def handle_login(self):
        self.auth_success = ""
        if not self.email.endswith("@lspu.edu.ph"):
            self.auth_error = "Please use a valid LSPU institutional email (@lspu.edu.ph)."
            return
        if supabase is None:
            self.auth_error = "Supabase client is not configured yet. Check your .env file."
            return

        try:
            # 1. Authenticate with Supabase Auth
            response = supabase.auth.sign_in_with_password(
                {
                    "email": self.email,
                    "password": self.password,
                }
            )

            if response.user:
                self.is_logged_in = True
                self.user_id = response.user.id
                self.user_email = self.email

                # 2. Fetch identity from Supabase 'users' table
                user_record = (
                    supabase.table("users")
                    .select("role, full_name, department")
                    .eq("user_id", response.user.id)
                    .execute()
                )

                if user_record.data:
                    self.user_role = user_record.data[0].get("role", "student")
                    self.user_name = user_record.data[0].get("full_name", self.email)
                    self.user_department = user_record.data[0].get("department", "Not Assigned")
                else:
                    self.user_role = "student"
                    self.user_name = "Unknown User"

                self.auth_error = ""

                # 3. Role-Based Routing
                if self.user_role == "admin":
                    return rx.redirect("/admin-dashboard")
                elif self.user_role == "faculty":
                    return rx.redirect("/faculty-dashboard")
                else:
                    return rx.redirect("/dashboard")

        except Exception as e:
            self.auth_error = "Invalid email or password."
            print(f"Login Error: {e}")

    async def handle_signup(self):
        self.auth_success = ""
        if not self.email.endswith("@lspu.edu.ph"):
            self.auth_error = "Registration requires an LSPU institutional email (@lspu.edu.ph)."
            return
        if not self.full_name.strip():
            self.auth_error = "Please enter your full name."
            return
        if self.password != self.confirm_password:
            self.auth_error = "Passwords do not match."
            return
        if len(self.password) < 8:
            self.auth_error = "Password must be at least 8 characters."
            return
        if supabase is None:
            self.auth_error = "Supabase client is not configured yet. Check your .env file."
            return

        try:
            # 1. Create the account in Supabase Auth
            response = supabase.auth.sign_up(
                {
                    "email": self.email,
                    "password": self.password,
                }
            )
            
            if response.user:
                # 2. Insert the new user into the public.users directory table
                try:
                    supabase.table("users").insert({
                        "user_id": response.user.id,
                        "email": self.email,
                        "full_name": self.full_name,
                        "role": self.role,
                        "department": "Pending Assignment",
                        "is_active": True
                    }).execute()
                except Exception as insert_e:
                    print(f"Directory Insert Notice (Safe to ignore if trigger exists): {insert_e}")

                self.auth_error = ""
                self.auth_success = "Account created successfully! You can now log in."
                self.is_signup_mode = False
                
        except Exception as e:
            self.auth_error = f"Sign up failed. User may already exist."
            print(f"Signup Error: {e}")

    async def handle_logout(self):
        self.is_logged_in = False
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.full_name = ""
        
        self.user_id = ""
        self.user_name = ""
        self.user_email = ""
        self.user_role = "student"
        
        self.auth_error = ""
        self.auth_success = ""
        
        # Sign out from Supabase session
        if supabase:
            try:
                supabase.auth.sign_out()
            except:
                pass
                
        return rx.redirect("/login")


def render_input_field(
    label: str,
    placeholder: str,
    value,
    on_change,
    icon_name: str,
    is_password: bool = False,
) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="14px", font_weight="500", color="#2C221E"),
        rx.hstack(
            rx.icon(icon_name, size=18, color="#8B7355"),
            rx.input(
                type="password" if is_password else "text",
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                width="100%",
                border="none",
                outline="none",
                bg="transparent",
                color="#2C221E",
            ),
            width="100%",
            bg="#FFFFFF",
            border="1px solid #E5E7EB",
            border_radius="8px",
            padding_x="12px",
            padding_y="8px",
            align_items="center",
            spacing="2",
            _hover={"border_color": "#C03928"},
            _focus_within={"border_color": "#C03928", "box_shadow": "0 0 0 1px #C03928"},
        ),
        width="100%",
        align_items="start",
        spacing="1",
    )


@rx.page(route="/login")
def auth_view() -> rx.Component:
    return rx.center(
        rx.flex(
            # ================= LEFT PANEL (Static) =================
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.text("M", color="#FFFFFF", font_weight="700", font_size="14px"),
                            bg="#C03928",
                            padding="6px 12px",
                            border_radius="8px",
                        ),
                        rx.text("Mochichi", font_weight="700", font_size="16px", color="#2C221E"),
                        align_items="center",
                        spacing="2",
                    ),
                    rx.heading(
                        "Schedule, organize, and track appointments",
                        font_family="serif",
                        font_size="30px",
                        font_weight="700",
                        color="#2C221E",
                        line_height="1.25",
                        margin_top="1.5rem",
                    ),
                    align_items="start",
                ),
                rx.center(
                    rx.image(src="/LOGO.png", width="328px", height="auto", alt="Mochichi Mascot"),
                    width="100%",
                    margin_y="auto",
                ),
                rx.hstack(
                    rx.box(
                        rx.icon("message-square", color="#C03928", size=18),
                        bg="#FAF6EE",
                        padding="8px",
                        border_radius="50%",
                    ),
                    rx.text(
                        "Mochichi: An AI-Powered Faculty and Student Appointment System.",
                        font_size="12px",
                        color="#2C221E",
                        font_weight="500",
                    ),
                    bg="#FFFFFF",
                    padding="12px 16px",
                    border_radius="12px",
                    width="100%",
                    align_items="center",
                    spacing="3",
                    border="1px solid #E5E7EB",
                ),
                bg="#FAF6EE",
                width=["100%", "100%", "45%"],
                padding="2.5rem",
                align_items="start",
                justify="between",
                display=["none", "none", "flex"],
            ),

            # ================= RIGHT PANEL (Dynamic Forms) =================
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            rx.cond(
                                State.is_signup_mode,
                                "Already have an account?",
                                "Don't have an account?",
                            ),
                            color="#6B7280",
                            font_size="14px",
                        ),
                        rx.link(
                            rx.cond(State.is_signup_mode, "Sign in.", "Sign up."),
                            on_click=State.toggle_mode,
                            color="#C03928",
                            font_weight="600",
                            font_size="14px",
                            cursor="pointer",
                        ),
                        width="100%",
                        justify="end",
                        margin_bottom="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading(
                            rx.cond(State.is_signup_mode, "Create your account", "Welcome back"),
                            font_family="serif",
                            font_size="28px",
                            font_weight="700",
                            color="#2C221E",
                        ),
                        rx.text(
                            rx.cond(
                                State.is_signup_mode,
                                "Free for campus users",
                                "Sign in with your @lspu.edu.ph account",
                            ),
                            color="#6B7280",
                            font_size="14px",
                        ),
                        align_items="start",
                        spacing="1",
                        width="100%",
                        margin_bottom="1.2rem",
                    ),
                    rx.vstack(
                        rx.cond(
                            State.is_signup_mode,
                            render_input_field(
                                "Full name",
                                "Juan Dela Cruz",
                                State.full_name,
                                State.set_full_name,
                                "user",
                            ),
                        ),
                        render_input_field(
                            "University email",
                            "username@lspu.edu.ph",
                            State.email,
                            State.set_email,
                            "mail",
                        ),
                        rx.cond(
                            State.is_signup_mode,
                            rx.vstack(
                                rx.text(
                                    "Account role",
                                    font_size="14px",
                                    font_weight="500",
                                    color="#2C221E",
                                ),
                                rx.select(
                                    ["student", "faculty", "admin"],
                                    value=State.role,
                                    on_change=State.set_role,
                                    width="100%",
                                    size="3",
                                    bg="#FFFFFF",
                                    color="#2C221E",
                                    border="1px solid #E5E7EB",
                                ),
                                width="100%",
                                align_items="start",
                                spacing="1",
                            ),
                        ),
                        rx.hstack(
                            render_input_field(
                                "Password",
                                "8+ characters",
                                State.password,
                                State.set_password,
                                "lock",
                                is_password=True,
                            ),
                            rx.cond(
                                State.is_signup_mode,
                                render_input_field(
                                    "Confirm password",
                                    "Repeat password",
                                    State.confirm_password,
                                    State.set_confirm_password,
                                    "lock",
                                    is_password=True,
                                ),
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        rx.button(
                            rx.cond(State.is_signup_mode, "Register", "Log In"),
                            on_click=State.submit_action,
                            bg="#C03928",
                            color="#FFFFFF",
                            width="100%",
                            size="3",
                            radius="large",
                            font_weight="600",
                            font_size="14px",
                            margin_top="0.8rem",
                            cursor="pointer",
                            _hover={"bg": "#A93226"},
                        ),
                        rx.cond(
                            State.auth_error != "",
                            rx.text(State.auth_error, color="#C03928", size="2", font_weight="500"),
                        ),
                        rx.cond(
                            State.auth_success != "",
                            rx.text(State.auth_success, color="#15803D", size="2", font_weight="500"),
                        ),
                        width="100%",
                        align_items="start",
                        spacing="3",
                    ),
                    width="100%",
                    max_width="440px",
                ),
                width=["100%", "100%", "55%"],
                bg="#FFFFFF",
                padding="3rem",
                align_items="center",
                justify="center",
                display="flex",
            ),
            direction="row",
            align="stretch",
            width="980px",
            max_width="95vw",
            min_height="620px",
            bg="#FFFFFF",
            border_radius="20px",
            box_shadow="0 12px 35px rgba(44, 34, 30, 0.08)",
            border="1px solid #E5E7EB",
            overflow="hidden",
        ),
        width="100vw",
        min_height="100vh",
        bg="#FAF6EE",
        padding="2rem",
    )