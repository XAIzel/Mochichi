import reflex as rx
from mochichi_scheduler.pages.dashboard import dashboard_view
from mochichi_scheduler.utils.supabase_client import supabase
from mochichi_scheduler.utils.gemini_ai import ask_mochichi_ai
from mochichi_scheduler.state import BaseState
from mochichi_scheduler.components.sidebar import sidebar

class State(BaseState):  # Inherit from BaseState so variables sync!
    """App state for Mochichi Authentication."""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    full_name: str = ""
    role: str = "student"
    auth_error: str = ""
    is_logged_in: bool = False
    current_user_id: str = ""
    is_signup_mode: bool = True

    # AI Assistant State
    ai_prompt: str = ""
    ai_response: str = "Hello! I am Mochichi, your AI academic assistant. How can I help you schedule today?"

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

    def set_ai_prompt(self, prompt: str):
        self.ai_prompt = prompt

    def toggle_mode(self):
        self.is_signup_mode = not self.is_signup_mode
        self.auth_error = ""

    def submit_action(self):
        """Routes the button click to the correct method."""
        if self.is_signup_mode:
            return self.handle_signup()
        else:
            return self.handle_login()

    def handle_login(self):
        if not self.email.endswith("@lspu.edu.ph"):
            self.auth_error = "Please use a valid LSPU institutional email (@lspu.edu.ph)."
            return

        try:
            response = supabase.auth.sign_in_with_password({
                "email": self.email,
                "password": self.password
            })
            if response.user:
                self.is_logged_in = True
                self.current_user_id = response.user.id
                # Sync credentials up to BaseState for the sidebar
                self.user_email = self.email
                self.auth_error = ""
        except Exception as e:
            self.auth_error = f"Login failed: {str(e)}"

    def handle_signup(self):
        if not self.email.endswith("@lspu.edu.ph"):
            self.auth_error = "Registration requires an LSPU institutional email (@lspu.edu.ph)."
            return
        if self.password != self.confirm_password:
            self.auth_error = "Passwords do not match."
            return

        try:
            response = supabase.auth.sign_up({
                "email": self.email,
                "password": self.password,
                "options": {
                    "data": {
                        "full_name": self.full_name,
                        "role": self.role
                    }
                }
            })
            # Sync credentials up to BaseState
            self.user_name = self.full_name
            self.user_email = self.email
            self.user_role = self.role
            self.auth_error = "Account created successfully! You can now log in."
            self.is_signup_mode = False
        except Exception as e:
            self.auth_error = f"Sign up failed: {str(e)}"

    def handle_logout(self):
        self.is_logged_in = False
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.current_user_id = ""
        self.user_email = ""

    def ask_ai(self):
        if self.ai_prompt.strip():
            # Uses Gemini AI connection
            self.ai_response = ask_mochichi_ai(self.ai_prompt)
            self.ai_prompt = ""

def render_input_field(label: str, placeholder: str, value, on_change, icon_name: str, is_password: bool = False) -> rx.Component:
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

def auth_view() -> rx.Component:
    return rx.center(
        # Main Unified Card
        rx.flex(
            # ================= LEFT PANEL (Static) =================
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.text("M", color="#FFFFFF", font_weight="700", font_size="14px"),
                            bg="#C03928", padding="6px 12px", border_radius="8px",
                        ),
                        rx.text("Mochichi", font_weight="700", font_size="16px", color="#2C221E"),
                        align_items="center", spacing="2",
                    ),
                    rx.heading(
                        "Schedule, organize, and track appointments",
                        font_family="serif", font_size="30px", font_weight="700",
                        color="#2C221E", line_height="1.25", margin_top="1.5rem",
                    ),
                    align_items="start"
                ),
                rx.center(
                    rx.image(src="/LOGO.png", width="328px", height="auto", alt="Mochichi Mascot"),
                    width="100%", margin_y="auto",
                ),
                rx.hstack(
                    rx.box(
                        rx.icon("message-square", color="#C03928", size=18),
                        bg="#FAF6EE", padding="8px", border_radius="50%",
                    ),
                    rx.text(
                        "Mochichi: An AI-Powered Faculty and Student Appointment System.",
                        font_size="12px", color="#2C221E", font_weight="500",
                    ),
                    bg="#FFFFFF", padding="12px 16px", border_radius="12px",
                    width="100%", align_items="center", spacing="3", border="1px solid #E5E7EB",
                ),
                bg="#FAF6EE", width=["100%", "100%", "45%"], padding="2.5rem",
                align_items="start", justify="between", display=["none", "none", "flex"], 
            ),

            # ================= RIGHT PANEL (Dynamic Forms) =================
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.text(rx.cond(State.is_signup_mode, "Already have an account?", "Don't have an account?"), color="#6B7280", font_size="14px"),
                        rx.link(rx.cond(State.is_signup_mode, "Sign in.", "Sign up."), on_click=State.toggle_mode, color="#C03928", font_weight="600", font_size="14px", cursor="pointer"),
                        width="100%", justify="end", margin_bottom="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading(rx.cond(State.is_signup_mode, "Create your account", "Welcome back"), font_family="serif", font_size="28px", font_weight="700", color="#2C221E"),
                        rx.text(rx.cond(State.is_signup_mode, "Free for campus users", "Sign in with your @lspu.edu.ph account"), color="#6B7280", font_size="14px"),
                        align_items="start", spacing="1", width="100%", margin_bottom="1.2rem",
                    ),
                    rx.vstack(
                        rx.cond(
                            State.is_signup_mode,
                            render_input_field("Full name", "Juan Dela Cruz", State.full_name, State.set_full_name, "user"),
                        ),
                        render_input_field("University email", "username@lspu.edu.ph", State.email, State.set_email, "mail"),
                        rx.cond(
                            State.is_signup_mode,
                            rx.vstack(
                                rx.text("Account role", font_size="14px", font_weight="500", color="#2C221E"),
                                rx.select(
                                    ["student", "faculty"], value=State.role, on_change=State.set_role,
                                    width="100%", size="3", bg="#FFFFFF", color="#2C221E", border="1px solid #E5E7EB",
                                ),
                                width="100%", align_items="start", spacing="1",
                            ),
                        ),
                        rx.hstack(
                            render_input_field("Password", "8+ characters", State.password, State.set_password, "lock", is_password=True),
                            rx.cond(
                                State.is_signup_mode,
                                render_input_field("Confirm password", "Repeat password", State.confirm_password, State.set_confirm_password, "lock", is_password=True),
                            ),
                            width="100%", spacing="3",
                        ),
                        rx.button(
                            rx.cond(State.is_signup_mode, "Register", "Log In"),
                            on_click=State.submit_action,
                            bg="#C03928", color="#FFFFFF", width="100%", size="3", radius="large", font_weight="600", font_size="14px", margin_top="0.8rem", _hover={"bg": "#A93226"},
                        ),
                        rx.text(State.auth_error, color="#C03928", size="2", font_weight="500"),
                        width="100%", align_items="start", spacing="3",
                    ),
                    width="100%", max_width="440px",
                ),
                width=["100%", "100%", "55%"], bg="#FFFFFF", padding="3rem", 
                align_items="center", justify="center", display="flex",
            ),
            
            # Card Wrapper Configuration
            direction="row",
            align="stretch",
            width="980px", max_width="95vw", min_height="620px", 
            bg="#FFFFFF", border_radius="20px", box_shadow="0 12px 35px rgba(44, 34, 30, 0.08)", 
            border="1px solid #E5E7EB", overflow="hidden",
        ),
        # Outer Background Viewport
        width="100vw", min_height="100vh", bg="#FAF6EE", padding="2rem",
    )

def index() -> rx.Component:
    return rx.cond(
        State.is_logged_in,
        dashboard_view(),  # Uses the imported overview grid from dashboard.py!
        auth_view(),
    )