import reflex as rx
from mochichi_scheduler.utils.supabase_client import supabase
from mochichi_scheduler.utils.gemini_ai import ask_mochichi_ai

class State(rx.State):
    """App state for Mochichi: An AI-Powered Faculty and Student Appointment System."""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    full_name: str = ""
    role: str = "student"
    auth_error: str = ""
    is_logged_in: bool = False
    current_user_id: str = ""
    is_signup_mode: bool = True  # Toggle between register and sign in views
    
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

    def handle_login(self):
        """Authenticates user against Supabase with LSPU institutional email validation."""
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
                self.auth_error = ""
        except Exception as e:
            self.auth_error = f"Login failed: {str(e)}"

    def handle_signup(self):
        """Registers a new LSPU institutional user account in Supabase."""
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
            self.auth_error = "Account created successfully! You can now log in."
            self.is_signup_mode = False
        except Exception as e:
            self.auth_error = f"Sign up failed: {str(e)}"

    def handle_logout(self):
        """Logs out the current user."""
        self.is_logged_in = False
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.current_user_id = ""

    def ask_ai(self):
        """Triggers Google Gemini response."""
        if self.ai_prompt.strip():
            self.ai_response = ask_mochichi_ai(self.ai_prompt)
            self.ai_prompt = ""

def render_input_field(label: str, placeholder: str, value, on_change, icon_name: str, is_password: bool = False) -> rx.Component:
    """Custom input component wrapper with reliable embedded icon and balanced placeholder visibility."""
    return rx.vstack(
        rx.text(label, font_size="14px", font_weight="500", color="#2C221E"),
        rx.hstack(
            rx.icon(icon_name, size=18, color="#8B7355"),  # Subtle Gold Tint icon color
            rx.input(
                type_="password" if is_password else "text",
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                width="100%",
                border="none",
                outline="none",
                bg="transparent",
                color="#2C221E",  # Typed text color (Deep Espresso)
            ),
            width="100%",
            bg="#FFFFFF",
            border="1px solid #E5E7EB",
            border_radius="8px",
            padding_x="12px",
            padding_y="8px",
            align="center",
            spacing="2",
            _hover={"border_color": "#C0392B"},
            _focus_within={"border_color": "#C0392B", "box_shadow": "0 0 0 1px #C0392B"},
        ),
        width="100%",
        align_items="start",
        spacing="1",
    )

def auth_view() -> rx.Component:
    """Login and Registration screen using exact system colors, fonts, and reliable form icons."""
    return rx.center(
        # Outer Floating Rounded Card Container
        rx.hstack(
            # --- LEFT PANEL (Warm Cream Branding Box with Enlarged & Blended Mascot Logo) ---
            rx.vstack(
                # Top Brand Header
                rx.hstack(
                    rx.box(
                        rx.text("M", color="#FFFFFF", font_weight="700", font_size="14px"),
                        bg="#C0392B",  # Rustic Red
                        padding="6px 12px",
                        border_radius="8px",
                    ),
                    rx.text("Mochichi", font_weight="700", font_size="16px", color="#2C221E"),  # Deep Espresso
                    align="center",
                    spacing="2",
                ),
                
                # Main Page Heading (Serif, 28px - 32px Bold)
                rx.heading(
                    "Schedule, organize, and track appointments",
                    font_family="serif",
                    font_size="30px",
                    font_weight="700",
                    color="#2C221E",  # Deep Espresso
                    line_height="1.25",
                    margin_top="1.5rem",
                ),
                
                # Enlarged Mascot Logo Image Box (Seamlessly Blended to Background)
                rx.center(
                    rx.image(
                        src="/LOGO.png",
                        width="320px",  # Enlarged size
                        height="auto",
                        alt="Mochichi Mascot Logo",
                    ),
                    width="100%",
                    margin_y="auto",
                ),
                
                # Bottom Quote / Info Card
                rx.hstack(
                    rx.box(
                        rx.icon("message-square", color="#C0392B", size=18),
                        bg="#FAF6EE",  # Warm Cream
                        padding="8px",
                        border_radius="50%",
                    ),
                    rx.text(
                        '"Mochichi: An AI-Powered Faculty and Student Appointment System".',
                        font_size="12px",
                        color="#2C221E",
                        font_weight="500",
                    ),
                    bg="#FFFFFF",  # Pure White card background for crisp contrast
                    padding="12px 16px",
                    border_radius="12px",
                    width="100%",
                    align="center",
                    spacing="3",
                    border="1px solid #E5E7EB",
                ),
                bg="#FAF6EE",  # Warm Cream matches logo background perfectly for a seamless blend
                width="45%",
                height="100%",
                padding="2.5rem",
                align_items="start",
                border_radius="20px 0 0 20px",
                display=["none", "none", "flex"],
            ),
            
            # --- RIGHT PANEL (Pure White Form Container) ---
            rx.box(
                rx.vstack(
                    # Top-right switch link ("Already have an account? Sign in.")
                    rx.hstack(
                        rx.text(
                            rx.cond(State.is_signup_mode, "Already have an account?", "Don't have an account?"),
                            color="#6B7280",  # Muted Text / Secondary
                            font_size="14px",
                        ),
                        rx.link(
                            rx.cond(State.is_signup_mode, "Sign in.", "Sign up."),
                            on_click=State.toggle_mode,
                            color="#C0392B",  # Rustic Red
                            font_weight="600",
                            font_size="14px",
                            cursor="pointer",
                        ),
                        width="100%",
                        justify="end",
                        margin_bottom="0.5rem",
                    ),
                    
                    # Header Title (Serif, 28px - 32px Bold)
                    rx.vstack(
                        rx.heading(
                            rx.cond(State.is_signup_mode, "Create your account", "Welcome back"),
                            font_family="serif",
                            font_size="28px",
                            font_weight="700",
                            color="#2C221E",  # Deep Espresso
                        ),
                        rx.text(
                            rx.cond(State.is_signup_mode, "Free for campus users", "Sign in with your @lspu.edu.ph account"),
                            color="#6B7280",  # Muted Text / Secondary
                            font_size="14px",
                        ),
                        align_items="start",
                        spacing="1",
                        width="100%",
                        margin_bottom="1.2rem",
                    ),
                    
                    # Form Fields Container
                    rx.vstack(
                        # Full Name (Signup only)
                        rx.cond(
                            State.is_signup_mode,
                            render_input_field("Full name", "Juan Dela Cruz", State.full_name, State.set_full_name, "user"),
                            rx.fragment(),
                        ),
                        
                        # University Email
                        render_input_field("University email", "username@lspu.edu.ph", State.email, State.set_email, "mail"),
                        
                        # Role Selection (Signup only)
                        rx.cond(
                            State.is_signup_mode,
                            rx.vstack(
                                rx.text("Account role", font_size="14px", font_weight="500", color="#2C221E"),
                                rx.select(
                                    ["student", "faculty"],
                                    value=State.role,
                                    on_change=State.set_role,
                                    width="100%",
                                    size="3",
                                    radius="large",
                                    bg="#FFFFFF",
                                    color="#2C221E",
                                    border="1px solid #E5E7EB",
                                ),
                                width="100%",
                                align_items="start",
                                spacing="1",
                            ),
                            rx.fragment(),
                        ),
                        
                        # Password row
                        rx.hstack(
                            render_input_field("Password", "8+ characters", State.password, State.set_password, "lock", is_password=True),
                            rx.cond(
                                State.is_signup_mode,
                                render_input_field("Confirm password", "Repeat password", State.confirm_password, State.set_confirm_password, "lock", is_password=True),
                                rx.fragment(),
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        
                        # Primary Action Button (Rustic Red)
                        rx.button(
                            rx.cond(State.is_signup_mode, "Register", "Log In"),
                            on_click=rx.cond(State.is_signup_mode, State.handle_signup, State.handle_login),
                            bg="#C0392B",  # Rustic Red
                            color="#FFFFFF",
                            width="100%",
                            size="3",
                            radius="large",
                            font_weight="600",
                            font_size="14px",
                            margin_top="0.8rem",
                            _hover={"bg": "#A93226"},
                        ),
                        
                        # Status message feedback
                        rx.text(State.auth_error, color="#C0392B", size="2", font_weight="500"),
                        
                        width="100%",
                        spacing="3",
                    ),
                    
                    width="100%",
                    max_width="440px",
                    align_items="center",
                ),
                width=["100%", "100%", "55%"],
                height="100%",
                padding="3rem",
                display="flex",
                justify="center",
                align_items="center",
                bg="#FFFFFF",  # Pure White card panel
                border_radius="0 20px 20px 0",
            ),
            width="980px",
            max_width="95vw",
            height="620px",
            bg="#FFFFFF",
            border_radius="20px",
            box_shadow="0 12px 35px rgba(44, 34, 30, 0.08)",
            border="1px solid #E5E7EB",  # Soft Gray border
        ),
        width="100vw",
        height="100vh",
        bg="#FAF6EE",  # Warm Cream screen background
    )

def dashboard_view() -> rx.Component:
    """UI Wireframe for the Main Dashboard featuring the AI Assistant."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("🐱 Mochichi Dashboard", size="6", color="#2C221E"),
                rx.spacer(),
                rx.text(f"Logged in as: {State.email} ({State.role})", size="2", color="#6B7280"),
                rx.button("Log Out", on_click=State.handle_logout, bg="#C0392B", color="#FFFFFF", size="2"),
                width="100%",
                align="center",
                padding_y="15px",
            ),
            rx.divider(border_color="#E5E7EB"),
            
            # AI Assistant Section Box
            rx.vstack(
                rx.heading("🤖 Mochichi AI Appointment Assistant", size="4", color="#2C221E"),
                rx.box(
                    rx.text(State.ai_response, size="3", color="#2C221E"),
                    padding="15px",
                    background="#FAF6EE",
                    border_radius="6px",
                    border="1px solid #E5E7EB",
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Ask Mochichi about schedules or consultations...",
                        value=State.ai_prompt,
                        on_change=State.set_ai_prompt,
                        width="100%",
                        bg="#FFFFFF",
                        color="#2C221E",
                    ),
                    rx.button("Ask AI", on_click=State.ask_ai, bg="#2C5E3B", color="#FFFFFF"),  # Forest Green
                    width="100%",
                ),
                spacing="3",
                padding="20px",
                border="1px solid #E5E7EB",
                border_radius="8px",
                background="#FFFFFF",
                width="100%",
            ),
            
            spacing="5",
            width="100%",
        ),
        padding_y="30px",
    )

def index() -> rx.Component:
    """Switches view based on authentication state."""
    return rx.cond(
        State.is_logged_in,
        dashboard_view(),
        auth_view(),
    )

# Global stylesheet override setting placeholders to a soft, balanced visibility tone
app = rx.App(
    style={
        "::placeholder": {
            "color": "#9CA3AF !important",
            "opacity": "0.85 !important",
        },
    }
)
app.add_page(index, title="Mochichi: AI Appointment System")