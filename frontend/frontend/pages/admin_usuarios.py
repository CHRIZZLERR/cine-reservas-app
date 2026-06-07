import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def estado_badge(activo) -> rx.Component:
    return rx.cond(
        activo,
        rx.box(
            "Activo",
            color="#22c55e",
            background="rgba(34,197,94,.12)",
            border="1px solid rgba(34,197,94,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="800",
            text_align="center",
        ),
        rx.box(
            "Inactivo",
            color="#ff4d6d",
            background="rgba(255,77,109,.12)",
            border="1px solid rgba(255,77,109,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="800",
            text_align="center",
        ),
    )


def rol_badge(rol) -> rx.Component:
    return rx.cond(
        rol == "admin",
        rx.box(
            "Admin",
            color="#FFD60A",
            background="rgba(255,214,10,.12)",
            border="1px solid rgba(255,214,10,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="900",
            text_align="center",
        ),
        rx.box(
            "Cliente",
            color="#6BAEFF",
            background="rgba(107,174,255,.12)",
            border="1px solid rgba(107,174,255,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="900",
            text_align="center",
        ),
    )


def usuario_row(usuario: dict) -> rx.Component:
    return rx.box(
        rx.grid(
            rx.vstack(
                rx.text(
                    usuario["nombre"],
                    color="white",
                    font_weight="900",
                    font_size="15px",
                ),
                rx.text(
                    usuario["email"],
                    color="#9aa7c0",
                    font_size="13px",
                ),
                spacing="1",
                align="start",
            ),
            rol_badge(usuario["rol"]),
            estado_badge(usuario["activo"]),
            rx.text(
                usuario["fecha_creacion"],
                color="#b8c0d4",
                font_size="13px",
            ),
            rx.button(
                rx.cond(usuario["activo"], "Desactivar", "Activar"),
                on_click=lambda: State.toggle_user_status(usuario["id"]),
                background=rx.cond(
                    usuario["activo"],
                    "rgba(255,77,109,.16)",
                    "rgba(34,197,94,.16)",
                ),
                color=rx.cond(
                    usuario["activo"],
                    "#ff4d6d",
                    "#22c55e",
                ),
                border=rx.cond(
                    usuario["activo"],
                    "1px solid rgba(255,77,109,.35)",
                    "1px solid rgba(34,197,94,.35)",
                ),
                border_radius="12px",
                padding="10px 16px",
                font_weight="900",
                cursor="pointer",
            ),
            columns="5",
            spacing="4",
            width="100%",
            align_items="center",
        ),
        padding="18px",
        border_radius="18px",
        background="rgba(255,255,255,.045)",
        border="1px solid rgba(255,255,255,.075)",
        margin_bottom="12px",
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.box(
                rx.heading(
                    "Acceso restringido",
                    color="white",
                    font_size="46px",
                    margin_bottom="14px",
                ),
                rx.text(
                    "Debes iniciar sesión como administrador para ver usuarios.",
                    color="#b8c0d4",
                    font_size="17px",
                    margin_bottom="24px",
                ),
                rx.link(
                    rx.button(
                        "Iniciar sesión",
                        background="#d90429",
                        color="white",
                        border_radius="16px",
                        padding="12px 26px",
                        font_weight="800",
                    ),
                    href="/auth",
                ),
                padding="50px",
                border_radius="28px",
                background="rgba(12,16,28,.92)",
                border="1px solid rgba(255,255,255,.09)",
                box_shadow="0 20px 70px rgba(0,0,0,.45)",
                text_align="center",
                max_width="650px",
            ),
            min_height="80vh",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )


def usuarios_admin_content() -> rx.Component:
    return rx.box(
        navbar("admin"),

        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "ADMINISTRACIÓN",
                        color="#ff004c",
                        letter_spacing="8px",
                        font_size="13px",
                        font_weight="900",
                    ),
                    rx.heading(
                        "Usuarios",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Consulta los usuarios registrados y activa o desactiva cuentas dentro del sistema.",
                        color="#b8c0d4",
                        font_size="17px",
                        max_width="800px",
                        line_height="1.7",
                    ),
                    spacing="3",
                    align="start",
                ),
                rx.spacer(),
                rx.link(
                    rx.button(
                        "Volver al panel",
                        background="rgba(255,255,255,.08)",
                        color="white",
                        border="1px solid rgba(255,255,255,.12)",
                        border_radius="14px",
                        padding="12px 20px",
                        font_weight="900",
                        cursor="pointer",
                    ),
                    href="/admin",
                ),
                width="100%",
                align="center",
                wrap="wrap",
                margin_bottom="34px",
            ),

            rx.hstack(
                rx.box(
                    rx.text("Total usuarios", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_usuarios, color="white", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Administradores", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_roles, color="#FFD60A", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Clientes", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_cliente_roles, color="#6BAEFF", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                spacing="4",
                wrap="wrap",
                margin_bottom="30px",
            ),

            rx.cond(
                State.admin_message != "",
                rx.box(
                    State.admin_message,
                    color="#FFD60A",
                    background="rgba(255,214,10,.10)",
                    border="1px solid rgba(255,214,10,.25)",
                    padding="14px 18px",
                    border_radius="16px",
                    margin_bottom="20px",
                    font_weight="800",
                ),
                rx.fragment(),
            ),

            rx.box(
                rx.grid(
                    rx.text("Usuario", color="#9aa7c0", font_size="13px", font_weight="900"),
                    rx.text("Rol", color="#9aa7c0", font_size="13px", font_weight="900"),
                    rx.text("Estado", color="#9aa7c0", font_size="13px", font_weight="900"),
                    rx.text("Creado", color="#9aa7c0", font_size="13px", font_weight="900"),
                    rx.text("Acción", color="#9aa7c0", font_size="13px", font_weight="900"),
                    columns="5",
                    spacing="4",
                    width="100%",
                    padding="0 18px 14px 18px",
                ),
                rx.foreach(State.admin_usuarios, usuario_row),
                padding="22px",
                border_radius="26px",
                background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
                border="1px solid rgba(255,255,255,.08)",
                box_shadow="0 22px 70px rgba(0,0,0,.36)",
            ),

            padding_x="7%",
            padding_top="70px",
            padding_bottom="90px",
        ),

        search_overlay(),
        side_menu(),
        class_name="page",
        on_mount=State.load_admin_usuarios,
    )


def admin_usuarios_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        usuarios_admin_content(),
        access_denied(),
    )