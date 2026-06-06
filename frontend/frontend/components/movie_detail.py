import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
    from components.schedule import showtimes_section
except ModuleNotFoundError:
    from ..state import State
    from .navbar import navbar, search_overlay, side_menu
    from .schedule import showtimes_section


def detail_page() -> rx.Component:
    return rx.box(
        navbar("cartelera"),

        rx.box(
            rx.image(
                src=State.current_movie["image"],
                class_name="detail-bg",
            ),
            rx.box(class_name="detail-overlay"),

            rx.grid(
                rx.box(
                    rx.image(
                        src=State.current_movie["poster"],
                        class_name="detail-poster",
                    ),
                    class_name="detail-poster-wrap",
                ),

                rx.vstack(
                    rx.text(
                        State.current_movie["fecha_estreno"],
                        class_name="section-kicker",
                    ),

                    rx.heading(
                        State.current_movie["titulo"],
                        class_name="detail-title",
                    ),

                    rx.hstack(
                        rx.text(
                            State.current_movie["genero"],
                            class_name="detail-chip",
                        ),
                        rx.text(
                            State.current_movie["clasificacion"],
                            class_name="detail-chip",
                        ),
                        rx.text(
                            State.current_movie["duracion"],
                            class_name="detail-chip",
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),

                    rx.text(
                        State.current_movie["sinopsis"],
                        class_name="detail-desc",
                    ),

                    rx.hstack(
                        rx.text("Director:", class_name="detail-label"),
                        rx.text(State.current_movie["director"], class_name="detail-value"),
                    ),

                    rx.hstack(
                        rx.text("Reparto:", class_name="detail-label"),
                        rx.text(State.current_movie["reparto"], class_name="detail-value"),
                    ),

                    rx.hstack(
                        rx.button(
                            "Ver trailer",
                            class_name="btn-primary-sm",
                            on_click=State.open_trailer,
                        ),
                        rx.button(
                            "Ocultar trailer",
                            class_name="btn-ghost",
                            on_click=State.close_trailer,
                        ),
                        spacing="2",
                    ),

                    rx.cond(
                        State.show_trailer,
                        rx.box(
                            rx.el.iframe(
                                src=State.trailer_url,
                                class_name="trailer-frame",
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",
                                allowfullscreen=True,
                            ),
                            class_name="trailer-box",
                        ),
                        rx.box(
                            rx.image(
                                src=State.current_movie["image"],
                                class_name="trailer-placeholder-img",
                            ),
                            rx.box(
                                'Presiona "Ver trailer" para cargar el video aquí mismo.',
                                class_name="trailer-placeholder-text",
                            ),
                            class_name="trailer-placeholder",
                        ),
                    ),

                    spacing="3",
                    align="start",
                    class_name="detail-info",
                ),

                columns="2",
                spacing="6",
                class_name="detail-grid",
            ),

            class_name="detail-hero",
        ),

        showtimes_section(),

        search_overlay(),
        side_menu(),

        class_name="page",
        on_mount=State.cargar_funciones_api,
    )