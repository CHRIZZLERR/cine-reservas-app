import reflex as rx  # type: ignore[import]
from ..state import State
from ..components.hero import hero_section
from ..components.movie_card import movie_card
from ..components.navbar import search_overlay, side_menu

GFONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
)


def page_style() -> rx.Component:
    return rx.el.style(f"""
        @import url('{GFONTS}');
        html {{ scroll-behavior: smooth; }}
        body {{ margin: 0; background: #040407; }}
        * {{ box-sizing: border-box; }}
    """)


def home_sections() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("NOW SHOWING", class_name="section-kicker"),
                    rx.heading("Cartelera destacada", class_name="section-title"),
                    spacing="0", align="start",
                ),
                rx.spacer(),
                rx.link("Ver cartelera →", href="/cartelera", class_name="view-all"),
                align="center",
            ),
            rx.grid(rx.foreach(State.cartelera_movies, movie_card), columns="6", spacing="3", width="100%"),
            class_name="page-section compact-section",
        ),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("COMING SOON", class_name="section-kicker"),
                    rx.heading("Próximamente", class_name="section-title"),
                    spacing="0", align="start",
                ),
                rx.spacer(),
                rx.link("Ver próximas →", href="/proximamente", class_name="view-all"),
                align="center",
            ),
            rx.grid(rx.foreach(State.pronto_movies, movie_card), columns="6", spacing="3", width="100%"),
            class_name="page-section compact-section",
        ),
    )


def index() -> rx.Component:
    return rx.box(
        page_style(),
        hero_section(),
        home_sections(),
        search_overlay(),
        side_menu(),
        class_name="page",
    )