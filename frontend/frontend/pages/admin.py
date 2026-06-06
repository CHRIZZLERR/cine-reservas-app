import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def admin_card(icon: str, title: str, text: str, href: str) -> rx.Component:
    return rx.link(
        rx.box(
            rx.text(icon, font_size="34px"),
            rx.heading(
                title,
                font_size="24px",
                color="white",
                margin_top="12px",
                margin_bottom="8px",
            ),
            rx.text(
                text,
                color="#b8c0d4",
                font_size="14px",
                line_height="1.6",
            ),
            rx.button(
                "Abrir módulo",
                margin_top="18px",
                background="#d90429",
                color="white",
                border_radius="14px",
                padding="10px 18px",
                font_weight="700",
                border="none",
                cursor="pointer",
            ),
            padding="26px",
            border_radius="24px",
            background="linear-gradient(145deg, rgba(18,24,39,.96), rgba(30,12,27,.92))",
            border="1px solid rgba(255,255,255,.08)",
            box_shadow="0 18px 45px rgba(0,0,0,.35)",
            transition="all .2s ease",
            min_height="230px",
        ),
        href=href,
        text_decoration="none",
    )


def stat_card(label: str, value: str, detail: str) -> rx.Component:
    return rx.box(
        rx.text(label, color="#aab4ca", font_size="13px", font_weight="700"),
        rx.heading(value, color="white", font_size="34px", margin_y="8px"),
        rx.text(detail, color="#7f8aa3", font_size="13px"),
        padding="22px",
        border_radius="22px",
        background="rgba(255,255,255,.045)",
        border="1px solid rgba(255,255,255,.08)",
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.box(
                rx.heading(
                    "Acceso restringido",
                    color="white",
                    font_size="48px",
                    margin_bottom="14px",
                ),
                rx.text(
                    "Debes iniciar sesión como administrador para entrar al panel.",
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


def admin_dashboard() -> rx.Component:
    return rx.box(
        navbar("admin"),

        rx.box(
            rx.box(
                rx.text(
                    "PANEL ADMINISTRATIVO",
                    color="#ff004c",
                    letter_spacing="8px",
                    font_size="13px",
                    font_weight="900",
                    margin_bottom="12px",
                ),
                rx.heading(
                    "Control general de JC Cinemas",
                    color="white",
                    font_size="54px",
                    line_height="1",
                    margin_bottom="16px",
                ),
                rx.text(
                    "Gestiona películas, funciones, reservas, usuarios y contenido importado desde TMDB.",
                    color="#b8c0d4",
                    font_size="17px",
                    max_width="760px",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.box(
                        rx.text("Administrador", color="#9aa7c0", font_size="13px"),
                        rx.text(State.logged_user_name, color="white", font_weight="800"),
                        padding="14px 18px",
                        border_radius="18px",
                        background="rgba(255,255,255,.055)",
                        border="1px solid rgba(255,255,255,.08)",
                    ),
                    rx.box(
                        rx.text("Rol", color="#9aa7c0", font_size="13px"),
                        rx.text(State.logged_user_role, color="#FFD60A", font_weight="800"),
                        padding="14px 18px",
                        border_radius="18px",
                        background="rgba(255,255,255,.055)",
                        border="1px solid rgba(255,255,255,.08)",
                    ),
                    spacing="4",
                    margin_top="26px",
                    wrap="wrap",
                ),
                padding_top="70px",
                padding_bottom="45px",
            ),

            rx.grid(
                stat_card("Películas", "CRUD", "Crear, editar, desactivar e importar."),
                stat_card("Funciones", "Horarios", "Administrar cine, sala, fecha y precio."),
                stat_card("Reservas", "Control", "Ver tickets, estados y asientos."),
                stat_card("Usuarios", "Roles", "Clientes y administradores."),
                columns="4",
                spacing="4",
                width="100%",
                margin_bottom="34px",
            ),

            rx.grid(
                admin_card(
                    "🎬",
                    "Películas",
                    "Gestiona cartelera, próximos estrenos, portadas, trailers y datos de TMDB.",
                    "/admin/peliculas",
                ),
                admin_card(
                    "🕒",
                    "Funciones",
                    "Crea horarios por película, sucursal, fecha, sala y precio.",
                    "/admin/funciones",
                ),
                admin_card(
                    "🎟️",
                    "Reservas",
                    "Consulta reservas realizadas, asientos ocupados y estado de tickets.",
                    "/admin/reservas",
                ),
                admin_card(
                    "🏢",
                    "Sucursales",
                    "Administra las ubicaciones disponibles para mostrar funciones.",
                    "/admin/sucursales",
                ),
                admin_card(
                    "👥",
                    "Usuarios",
                    "Visualiza clientes, administradores y estado de cuentas.",
                    "/admin/usuarios",
                ),
                admin_card(
                    "🌐",
                    "Importar TMDB",
                    "Busca películas en TMDB e impórtalas directo a la base de datos.",
                    "/admin/tmdb",
                ),
                columns="3",
                spacing="5",
                width="100%",
            ),

            padding_x="7%",
            padding_bottom="80px",
        ),

        search_overlay(),
        side_menu(),
        class_name="page",
    )


def admin_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_dashboard(),
        access_denied(),
    )