import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def login_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Iniciar sesión", class_name="auth-title"),
        rx.text(
            "Accede para guardar tus reservas y consultar tus boletos.",
            class_name="auth-subtitle",
        ),
        rx.input(
            placeholder="Correo electrónico",
            value=State.login_email,
            on_change=State.set_login_email,
            class_name="form-input",
            width="100%",
        ),
        rx.input(
            placeholder="Contraseña",
            type="password",
            value=State.login_password,
            on_change=State.set_login_password,
            class_name="form-input",
            width="100%",
        ),
        rx.button(
            "Entrar",
            class_name="btn-primary-lg full",
            on_click=State.login,
        ),
        rx.button(
            "Crear una cuenta",
            class_name="btn-ghost full",
            on_click=State.show_register,
        ),
        rx.cond(
            State.auth_message != "",
            rx.text(State.auth_message, class_name="auth-message"),
            rx.fragment(),
        ),
        spacing="4",
        align="stretch",
        class_name="auth-card",
    )


def register_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Crear cuenta", class_name="auth-title"),
        rx.text(
            "Regístrate para que tus boletos queden guardados en tu usuario.",
            class_name="auth-subtitle",
        ),
        rx.input(
            placeholder="Nombre completo",
            value=State.register_name,
            on_change=State.set_register_name,
            class_name="form-input",
            width="100%",
        ),
        rx.input(
            placeholder="Correo electrónico",
            value=State.register_email,
            on_change=State.set_register_email,
            class_name="form-input",
            width="100%",
        ),
        rx.input(
            placeholder="Contraseña",
            type="password",
            value=State.register_password,
            on_change=State.set_register_password,
            class_name="form-input",
            width="100%",
        ),
        rx.input(
            placeholder="Confirmar contraseña",
            type="password",
            value=State.register_confirm_password,
            on_change=State.set_register_confirm_password,
            class_name="form-input",
            width="100%",
        ),
        rx.button(
            "Registrarme",
            class_name="btn-primary-lg full",
            on_click=State.register_user,
        ),
        rx.button(
            "Ya tengo una cuenta",
            class_name="btn-ghost full",
            on_click=State.show_login,
        ),
        rx.cond(
            State.auth_message != "",
            rx.text(State.auth_message, class_name="auth-message"),
            rx.fragment(),
        ),
        spacing="4",
        align="stretch",
        class_name="auth-card",
    )


def auth_page() -> rx.Component:
    return rx.box(
        navbar(""),
        rx.grid(
            rx.vstack(
                rx.text("MI CUENTA", class_name="section-kicker"),
                rx.heading("Bienvenido a JC Cinemas", class_name="page-title"),
                rx.text(
                    "Inicia sesión o crea una cuenta para continuar con tus reservas. "
                    "También puedes comprar como invitado desde el checkout.",
                    class_name="auth-main-text",
                ),
                rx.box(
                    rx.text("✓ Guarda tus boletos en tu cuenta", class_name="auth-benefit"),
                    rx.text("✓ Consulta tus reservas después", class_name="auth-benefit"),
                    rx.text("✓ Compra más rápido la próxima vez", class_name="auth-benefit"),
                    class_name="auth-benefits",
                ),
                spacing="4",
                align="start",
                class_name="auth-info",
            ),
            rx.cond(
                State.auth_mode == "login",
                login_form(),
                register_form(),
            ),
            columns="2",
            spacing="8",
            class_name="auth-layout",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )