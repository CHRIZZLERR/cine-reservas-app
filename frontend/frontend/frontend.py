import reflex as rx  # type: ignore[import]

from frontend.config import APP_NAME
from frontend.components.movie_card import movie_card
from frontend.components.navbar import navbar, search_overlay, side_menu
from frontend.components.footer import locations_page, site_footer
from frontend.components.movie_detail import detail_page
from frontend.pages.home import index
from frontend.pages.reserva import booking_page
from frontend.pages.auth import auth_page
from frontend.pages.admin import admin_page
from frontend.pages.admin_usuarios import admin_usuarios_page
from frontend.pages.admin_reservas import admin_reservas_page
from frontend.state import State


def location_filter() -> rx.Component:
    from frontend.data import LOCATIONS

    return rx.box(
        rx.text("Selecciona una localización", class_name="block-label"),
        rx.hstack(
            rx.foreach(
                LOCATIONS,
                lambda loc: rx.button(
                    loc,
                    class_name=rx.cond(
                        State.selected_location == loc,
                        "pill pill-active",
                        "pill",
                    ),
                    on_click=lambda: State.set_location(loc),
                ),
            ),
            spacing="2",
            wrap="wrap",
        ),
        rx.text(
            f"Mostrando funciones disponibles en {State.selected_location}",
            class_name="muted",
        ),
        margin_bottom="24px",
    )


def movie_grid(title: str, movies_var, subtitle: str, active: str) -> rx.Component:
    return rx.box(
        navbar(active),
        rx.box(
            rx.text(subtitle, class_name="section-kicker"),
            rx.heading(title, class_name="page-title"),
            rx.cond(
                active == "cartelera",
                location_filter(),
                rx.fragment(),
            ),
            rx.grid(
                rx.foreach(movies_var, movie_card),
                columns="6",
                spacing="3",
                width="100%",
                class_name="movies-grid",
            ),
            class_name="page-section page-top",
        ),
        site_footer(),
        search_overlay(),
        side_menu(),
        class_name="page",
    )


def cartelera() -> rx.Component:
    return movie_grid(
        "Películas en cartelera",
        State.cartelera_movies,
        "NOW SHOWING",
        "cartelera",
    )


def proximamente() -> rx.Component:
    return movie_grid(
        "Próximamente",
        State.pronto_movies,
        "COMING SOON",
        "proximamente",
    )


app = rx.App(stylesheets=["/style.css"])

app.add_page(index, route="/", title=APP_NAME)
app.add_page(cartelera, route="/cartelera", title=f"{APP_NAME} | Cartelera")
app.add_page(proximamente, route="/proximamente", title=f"{APP_NAME} | Próximamente")
app.add_page(locations_page, route="/ubicaciones", title=f"{APP_NAME} | Ubicaciones")
app.add_page(detail_page, route="/pelicula", title=f"{APP_NAME} | Detalle")
app.add_page(booking_page, route="/reservar", title=f"{APP_NAME} | Reservar")
app.add_page(auth_page, route="/auth", title=f"{APP_NAME} | Iniciar sesión")
app.add_page(admin_page, route="/admin", title=f"{APP_NAME} | Panel Admin")
app.add_page(admin_usuarios_page, route="/admin/usuarios", title=f"{APP_NAME} | Usuarios")
app.add_page(admin_reservas_page, route="/admin/reservas", title=f"{APP_NAME} | Reservas")