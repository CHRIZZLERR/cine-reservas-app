import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def login_form() -> rx.Component:
    return rx.box(
        rx.heading("Iniciar sesión", class_name="auth-title"),
        rx.text("Accede para guardar tus reservas y datos.", class_name="auth-subtitle"),
        rx.input(
            placeholder="Correo electrónico",
            value=State.login_email,
            on_change=State.set_login_email,
            class_name="form-input",
        ),
        rx.input(
            placeholder="Contraseña",
            type="password",
            value=State.login_password,
            on_change=State.set_login_password,
            class_name="form-input",
        ),
        rx.button("Entrar", class_name="checkout-btn", on_click=State.login),
        rx.button(
            "Crear una cuenta",
            class_name="btn-ghost full",
            on_click=State.show_register,
        ),
        rx.text(State.auth_message, class_name="auth-message"),
        class_name="auth-card",
    )


def register_form() -> rx.Component:
    return rx.box(
        rx.heading("Registrarse", class_name="auth-title"),
        rx.text("Crea tu cuenta para reservar más rápido.", class_name="auth-subtitle"),
        rx.input(
            placeholder="Nombre completo",
            value=State.register_name,
            on_change=State.set_register_name,
            class_name="form-input",
        ),
        rx.input(
            placeholder="Correo electrónico",
            value=State.register_email,
            on_change=State.set_register_email,
            class_name="form-input",
        ),
        rx.input(
            placeholder="Contraseña",
            type="password",
            value=State.register_password,
            on_change=State.set_register_password,
            class_name="form-input",
        ),
        rx.input(
            placeholder="Confirmar contraseña",
            type="password",
            value=State.register_confirm_password,
            on_change=State.set_register_confirm_password,
            class_name="form-input",
        ),
        rx.button("Crear cuenta", class_name="checkout-btn", on_click=State.register_user),
        rx.button(
            "Ya tengo cuenta",
            class_name="btn-ghost full",
            on_click=State.show_login,
        ),
        rx.text(State.auth_message, class_name="auth-message"),
        class_name="auth-card",
    )


def auth_page() -> rx.Component:
    return rx.box(
        navbar("auth"),
        rx.box(
            rx.box(
                rx.text("MI CUENTA", class_name="section-kicker"),
                rx.heading("Bienvenido a JC Cinemas", class_name="page-title"),
                rx.text(
                    "Inicia sesión o crea una cuenta para continuar con tus reservas.",
                    class_name="auth-main-text",
                ),
                class_name="auth-info",
            ),
            rx.cond(
                State.auth_mode == "login",
                login_form(),
                register_form(),
            ),
            class_name="auth-layout",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )