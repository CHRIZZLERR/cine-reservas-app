import reflex as rx  # type: ignore[import]

try:
    from state import State
except ModuleNotFoundError:
    from ..state import State


def movie_card(movie: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src=movie["poster"],
                style={
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "object_fit": "cover",
                    "object_position": "center top",
                    "transition": "transform 0.35s",
                },
            ),
            rx.box(
                rx.text(movie["clasificacion"], class_name="movie-rating"),
                class_name="rating-wrap",
            ),
            rx.box(class_name="movie-img-gradient"),
            style={
                "position": "relative",
                "width": "100%",
                "aspect_ratio": "2/3",
                "overflow": "hidden",
                "background": "#070a11",
                "flex_shrink": "0",
            },
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