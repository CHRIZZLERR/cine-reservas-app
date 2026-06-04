# =============================================================
# CineMax / CineHub · footer.py
# Ubicaciones y footer simple.
# =============================================================
import reflex as rx

from ..data import LOCATIONS, LOCATION_DETAILS
from .navbar import navbar, search_overlay, side_menu


def location_card(loc: str, data: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src=data["image"],
                class_name="location-img",
            ),
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
                rx.text("Dulcería", class_name="location-chip"),
                spacing="2",
                wrap="wrap",
            ),
            rx.link(
                rx.button(
                    "Abrir ubicación en Google Maps →",
                    class_name="btn-primary-sm location-btn",
                    width="100%",
                ),
                href=data["map"],
                is_external=True,
                width="100%",
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
                *[
                    location_card(loc, LOCATION_DETAILS[loc])
                    for loc in LOCATIONS
                    if loc in LOCATION_DETAILS
                ],
                columns="5",
                spacing="3",
                width="100%",
                class_name="locations-grid",
            ),
            class_name="page-section page-top locations-section",
        ),
        search_overlay(),
        side_menu(),
        footer(),
        class_name="page",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("CINEMAX", class_name="footer-brand"),
                rx.text(
                    "Tu cine, tus asientos, tu experiencia.",
                    class_name="footer-text",
                ),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text("Frontend realizado en Reflex", class_name="footer-text"),
                rx.text("Sistema de reservas de cine físico", class_name="footer-text"),
                spacing="1",
                align_items="end",
            ),
            width="100%",
            align="center",
        ),
        class_name="footer",
    )
