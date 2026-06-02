import reflex as rx  # type: ignore[import]
from ..state import State


def movie_card(movie: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(src=movie["poster"], class_name="movie-img"),
            rx.box(rx.text(movie["clasificacion"], class_name="movie-rating"), class_name="rating-wrap"),
            rx.box(class_name="movie-img-gradient"),
            class_name="movie-img-wrap",
        ),
        rx.box(
            rx.text(movie["genero"], class_name="movie-genre"),
            rx.heading(movie["titulo"], class_name="movie-title"),
            rx.hstack(
                rx.text(movie["duracion"], class_name="movie-duration"),
                rx.spacer(),
                rx.text(movie["fecha_estreno"], class_name="movie-date"),
            ),
            rx.button(
                "Ver detalles",
                class_name="movie-btn",
                on_click=lambda: State.go_to_movie(movie["id"]),
            ),
            class_name="movie-body",
        ),
        class_name="movie-card",
    )