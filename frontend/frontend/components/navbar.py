import reflex as rx  # type: ignore[import]

try:
    from config import APP_NAME, APP_BRAND_LOGO
    from state import State
    from data import LOCATIONS
except ModuleNotFoundError:
    from ..config import APP_NAME, APP_BRAND_LOGO
    from ..state import State
    from ..data import LOCATIONS


def nav_class(active: str, name: str) -> str:
    return "nav-link active-link" if active == name else "nav-link"


def navbar(active: str = "") -> rx.Component:
    return rx.box(
        rx.box(
            rx.link(
                rx.image(
                    src=APP_BRAND_LOGO,
                    alt=APP_NAME,
                    class_name="brand-logo-img",
                ),
                href="/",
                text_decoration="none",
                class_name="brand-link",
            ),

            rx.box(
                rx.link("Inicio", href="/", class_name=nav_class(active, "inicio")),
                rx.link("Cartelera", href="/cartelera", class_name=nav_class(active, "cartelera")),
                rx.link("Próximamente", href="/proximamente", class_name=nav_class(active, "proximamente")),
                rx.link("Ubicaciones", href="/ubicaciones", class_name=nav_class(active, "ubicaciones")),
                rx.link("Boletos", href="/reservar", class_name=nav_class(active, "boletos")),
                rx.cond(
                    State.logged_user_role == "admin",
                    rx.link(
                        "Panel Admin",
                        href="/admin",
                        class_name="nav-link admin-panel-link",
                    ),
                    rx.fragment(),
                ),
                class_name="nav-menu",
            ),

            rx.box(
                rx.cond(
                    State.is_logged_in,
                    rx.hstack(
                        rx.text("Hola,", class_name="nav-user-muted"),
                        rx.text(State.display_user_name, class_name="nav-user-name"),
                        rx.button(
                            "Salir",
                            class_name="nav-logout",
                            on_click=State.logout,
                        ),
                        spacing="2",
                        align="center",
                        class_name="nav-user-box",
                    ),
                    rx.link(
                        "Iniciar sesión",
                        href="/auth",
                        class_name="login-link",
                    ),
                ),
                rx.button("⌕", class_name="nav-icon", on_click=State.toggle_search),
                rx.button("☰", class_name="nav-icon", on_click=State.toggle_menu),
                class_name="nav-actions",
            ),

            class_name="navbar-inner",
        ),
        class_name="navbar",
    )


def search_overlay() -> rx.Component:
    return rx.cond(
        State.show_search,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("🔍 Buscar película", class_name="search-panel-title"),
                        rx.spacer(),
                        rx.button("✕", class_name="close-btn", on_click=State.close_search),
                        width="100%",
                        align="center",
                    ),
                    rx.input(
                        placeholder="Escribe el nombre, género o clasificación...",
                        value=State.search_text,
                        on_change=State.set_search_text,
                        class_name="search-input-big",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button("Ver resultados en cartelera →", class_name="btn-primary-lg"),
                            href="/cartelera",
                        ),
                        rx.button("Limpiar", class_name="btn-ghost", on_click=State.set_search_text("")),
                        spacing="3",
                    ),
                    spacing="4",
                    width="100%",
                ),
                class_name="search-panel",
            ),
            class_name="overlay",
        ),
        rx.fragment(),
    )


def side_menu() -> rx.Component:
    return rx.cond(
        State.show_menu,
        rx.box(
            rx.box(class_name="menu-backdrop", on_click=State.close_menu),
            rx.vstack(
                rx.hstack(
                    rx.heading(APP_NAME.upper(), class_name="drawer-logo"),
                    rx.spacer(),
                    rx.button("✕", class_name="close-btn", on_click=State.close_menu),
                    width="100%",
                ),
                rx.input(
                    placeholder="Buscar película...",
                    value=State.search_text,
                    on_change=State.set_search_text,
                    class_name="drawer-search",
                ),
                rx.link("Inicio", href="/", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Cartelera", href="/cartelera", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Próximamente", href="/proximamente", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Ubicaciones", href="/ubicaciones", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Comprar boletos", href="/reservar", class_name="drawer-link", on_click=State.close_menu),
                rx.cond(
                    State.logged_user_role == "admin",
                    rx.link(
                        "Panel Admin",
                        href="/admin",
                        class_name="drawer-link",
                        on_click=State.close_menu,
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    State.is_logged_in,
                    rx.vstack(
                        rx.text(f"Hola, {State.display_user_name}", class_name="drawer-small"),
                        rx.button("Cerrar sesión", class_name="btn-ghost full", on_click=State.logout),
                        width="100%",
                        spacing="2",
                    ),
                    rx.link("Iniciar sesión", href="/auth", class_name="drawer-link", on_click=State.close_menu),
                ),
                rx.box(
                    rx.text("Cines disponibles", class_name="drawer-kicker"),
                    rx.foreach(LOCATIONS, lambda loc: rx.text(loc, class_name="drawer-small")),
                    class_name="drawer-card",
                ),
                spacing="4",
                align="start",
                class_name="drawer",
            ),
            class_name="drawer-wrapper",
        ),
        rx.fragment(),
    )