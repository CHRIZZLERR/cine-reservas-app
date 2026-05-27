import reflex as rx
import urllib.request
import json

API_URL = "http://127.0.0.1:8000"

GFONT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Rajdhani:wght@400;500;600;700&"
    "family=Anton&display=swap"
)


class State(rx.State):
    peliculas: list[dict] = []

    def cargar_peliculas(self):
        try:
            with urllib.request.urlopen(f"{API_URL}/peliculas") as response:
                self.peliculas = json.loads(response.read())
        except Exception:
            self.peliculas = []


def page_style():
    return rx.el.style(
        f"""
        @import url('{GFONT_URL}');
        html {{ scroll-behavior: smooth; }}
        body {{ margin: 0; background: #020617; }}
        """
    )


def movie_card(pelicula):
    return rx.box(
        rx.box(rx.text("🎬", font_size="72px"), class_name="poster-fake"),
        rx.box(
            rx.heading(pelicula["titulo"], class_name="movie-title"),
            rx.text(pelicula["genero"], class_name="muted"),
            rx.text(f"Clasificación: {pelicula['clasificacion']}", class_name="muted"),
            rx.button("Ver funciones", class_name="primary-btn", width="100%"),
            class_name="movie-info",
        ),
        class_name="movie-card",
    )


def index():
    return rx.box(
        page_style(),

        rx.box(
            rx.hstack(
                rx.heading("CineMax", class_name="logo"),
                rx.spacer(),
                rx.link("Inicio", href="#inicio", class_name="nav-link"),
                rx.link("Cartelera", href="#cartelera", class_name="nav-link"),
                rx.link("Reservas", href="#reservas", class_name="nav-link"),
                class_name="navbar",
            ),

            rx.vstack(
                rx.badge("Cartelera disponible", color_scheme="red"),
                rx.heading("Reserva tu próxima función", class_name="hero-title"),
                rx.text(
                    "Elige película, sucursal, horario y asientos en una experiencia moderna de cine.",
                    class_name="hero-text",
                ),
                rx.hstack(
                    rx.button("Explorar cartelera", class_name="primary-btn"),
                    rx.button("Ver reservas", class_name="secondary-btn"),
                ),
                align="start",
                spacing="5",
                class_name="hero-content",
            ),
            id="inicio",
            class_name="hero",
        ),

        rx.box(
            rx.hstack(
                rx.input(placeholder="Buscar película...", class_name="search-input"),
                rx.button("Buscar", class_name="search-btn"),
                class_name="search-bar",
            ),
        ),

        rx.box(
            rx.heading("Cartelera", class_name="section-title"),
            rx.cond(
                State.peliculas.length() > 0,
                rx.grid(
                    rx.foreach(State.peliculas, movie_card),
                    columns="3",
                    spacing="6",
                    width="100%",
                ),
                rx.text(
                    "No hay películas cargadas. Verifica que el backend esté corriendo.",
                    color="#cbd5e1",
                ),
            ),
            id="cartelera",
            class_name="section",
        ),

        rx.box(
            rx.heading("Flujo de reserva", class_name="section-title"),
            rx.grid(
                rx.box(rx.text("🎞️", font_size="42px"), rx.heading("1. Película"), rx.text("Selecciona una película de la cartelera."), class_name="info-card"),
                rx.box(rx.text("📍", font_size="42px"), rx.heading("2. Sucursal"), rx.text("Downtown Center o Galería 360."), class_name="info-card"),
                rx.box(rx.text("🕒", font_size="42px"), rx.heading("3. Función"), rx.text("Elige fecha, hora y sala."), class_name="info-card"),
                rx.box(rx.text("💺", font_size="42px"), rx.heading("4. Asientos"), rx.text("Disponible, seleccionado o reservado."), class_name="info-card"),
                rx.box(rx.text("🧾", font_size="42px"), rx.heading("5. Resumen"), rx.text("Datos del cliente y total."), class_name="info-card"),
                rx.box(rx.text("✅", font_size="42px"), rx.heading("6. Confirmación"), rx.text("Código de reserva y QR opcional."), class_name="info-card"),
                columns="3",
                spacing="5",
            ),
            id="reservas",
            class_name="section",
        ),

        class_name="page",
    )


app = rx.App(stylesheets=["/style.css"])
app.add_page(index, on_load=State.cargar_peliculas)