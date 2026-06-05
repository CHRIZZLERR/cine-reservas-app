import reflex as rx  # type: ignore[import]

try:
    from config import APP_NAME, APP_TAGLINE
    from data import LOCATIONS, LOCATION_DETAILS
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..config import APP_NAME, APP_TAGLINE
    from ..data import LOCATIONS, LOCATION_DETAILS
    from .navbar import navbar, search_overlay, side_menu


def site_footer() -> rx.Component:
    return rx.box(
        rx.box(
            rx.grid(
                # Col 1 — branding
                rx.vstack(
                    rx.hstack(
                        rx.box(APP_NAME[0:2], class_name="footer-brand-mark"),
                        rx.vstack(
                            rx.text(APP_NAME.upper(), class_name="footer-brand-title"),
                            rx.text("CINE PREMIUM", class_name="footer-brand-sub"),
                            spacing="0", align="start",
                        ),
                        spacing="3", align="center",
                    ),
                    rx.text(APP_TAGLINE, class_name="footer-tagline"),
                    rx.hstack(
                        rx.link("📘", href="#", class_name="footer-social"),
                        rx.link("📸", href="#", class_name="footer-social"),
                        rx.link("🐦", href="#", class_name="footer-social"),
                        spacing="3",
                    ),
                    spacing="4", align="start",
                ),
                # Col 2 — navegación
                rx.vstack(
                    rx.text("Navegación", class_name="footer-heading"),
                    rx.link("Inicio", href="/", class_name="footer-link"),
                    rx.link("Cartelera", href="/cartelera", class_name="footer-link"),
                    rx.link("Próximamente", href="/proximamente", class_name="footer-link"),
                    rx.link("Ubicaciones", href="/ubicaciones", class_name="footer-link"),
                    rx.link("Comprar boletos", href="/reservar", class_name="footer-link"),
                    spacing="2", align="start",
                ),
                # Col 3 — cines
                rx.vstack(
                    rx.text("Nuestros cines", class_name="footer-heading"),
                    *[rx.text(loc, class_name="footer-link") for loc in LOCATIONS],
                    spacing="2", align="start",
                ),
                # Col 4 — info
                rx.vstack(
                    rx.text("Información", class_name="footer-heading"),
                    rx.text("Lunes a Domingo", class_name="footer-link"),
                    rx.text("12:00 PM – 11:00 PM", class_name="footer-link"),
                    rx.text("info@jccinemas.do", class_name="footer-link"),
                    rx.text("+1 (809) 555-0100", class_name="footer-link"),
                    spacing="2", align="start",
                ),
                columns="4", spacing="8", width="100%",
            ),
            rx.divider(border_color="rgba(255,255,255,.08)", margin_y="32px"),
            rx.hstack(
                rx.text(f"© 2026 {APP_NAME}. Todos los derechos reservados.", class_name="footer-copy"),
                rx.spacer(),
                rx.text("Hecho con ❤️ en Santo Domingo", class_name="footer-copy"),
                width="100%", wrap="wrap",
            ),
            class_name="footer-inner",
        ),
        class_name="site-footer",
    )


def location_card(loc: str, data: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(src=data["image"], class_name="location-img"),
            rx.box(class_name="location-img-layer"),
            rx.box("📍", class_name="location-pin"),
            class_name="location-media",
        ),
        rx.box(
            rx.text(data["zona"], class_name="location-zone"),
            rx.heading(loc, class_name="location-title"),
            rx.text(data["salas"], class_name="location-text"),
            rx.hstack(
                rx.text("2D", class_name="location-chip"),
                rx.text("VIP", class_name="location-chip"),
                spacing="2", wrap="wrap",
            ),
            rx.link(
                rx.button("Abrir en Maps", class_name="btn-primary-sm location-btn"),
                href=data["map"], is_external=True, width="100%",
            ),
            class_name="location-body",
        ),
        class_name="location-card",
    )


def locations_page() -> rx.Component:
    return rx.box(
        navbar("ubicaciones"),
        rx.box(
            rx.text("CINES DISPONIBLES", class_name="section-kicker"),
            rx.heading("Ubicaciones", class_name="page-title locations-title"),
            rx.text(
                "Selecciona el cine más cercano y abre su ubicación directamente en Google Maps.",
                class_name="locations-subtitle",
            ),
            rx.grid(
                *[location_card(loc, LOCATION_DETAILS[loc]) for loc in LOCATIONS],
                columns="5", spacing="3", width="100%",
            ),
            class_name="page-section page-top locations-section",
        ),
        site_footer(),
        search_overlay(),
        side_menu(),
        class_name="page",
    )