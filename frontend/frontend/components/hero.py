import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar
except ModuleNotFoundError:
    from ..state import State
    from .navbar import navbar


def hero_thumb(movie: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src=movie["poster_url"],
                alt=movie["titulo"],
                style={
                    "width": "100%",
                    "height": "100%",
                    "objectFit": "cover",
                    "objectPosition": "center",
                    "display": "block",
                },
            ),
            style={
                "width": "132px",
                "height": "198px",
                "borderRadius": "16px",
                "overflow": "hidden",
                "background": "#05070d",
                "border": "1.5px solid rgba(255,255,255,.14)",
                "boxShadow": "0 18px 45px rgba(0,0,0,.65)",
            },
        ),
        rx.text(
            movie["titulo"],
            class_name="hero-thumb-title",
            style={
                "width": "132px",
                "maxWidth": "132px",
                "whiteSpace": "nowrap",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "textAlign": "center",
                "fontWeight": "800",
                "fontSize": "13px",
                "color": "rgba(255,255,255,.82)",
                "marginTop": "10px",
            },
        ),
        class_name="hero-thumb",
        style={
            "cursor": "pointer",
            "transition": "all .25s ease",
        },
        on_click=lambda: State.seleccionar_pelicula_home(movie["id"]),
    )


def hero_section() -> rx.Component:
    return rx.box(
        rx.el.img(
            src=rx.cond(
                State.hero_movie["backdrop_url"] != "",
                State.hero_movie["backdrop_url"],
                State.hero_movie["poster_url"],
            ),
            alt=State.hero_movie["titulo"],
            style={
                "position": "absolute",
                "inset": "0",
                "width": "100%",
                "height": "100%",
                "objectFit": "cover",
                "objectPosition": "center top",
                "filter": "saturate(1.08) contrast(1.06)",
                "animation": "kenBurns 12s ease-in-out infinite alternate",
                "zIndex": "0",
            },
        ),
        rx.box(class_name="hero-layer"),
        navbar("inicio"),
        rx.button(
            "",
            id="auto-next-hero",
            on_click=State.next_hero,
            style={"display": "none"},
        ),
        rx.script(
            "(function(){if(window.__cinehubHeroTimer){clearInterval(window.__cinehubHeroTimer);}"
            "window.__cinehubHeroTimer=setInterval(function(){"
            "const btn=document.getElementById('auto-next-hero');"
            "if(btn){btn.click();}},5000);})();"
        ),
        rx.grid(
            rx.vstack(
                rx.text("new", class_name="hero-badge"),
                rx.heading(
                    State.hero_movie["titulo"],
                    class_name="hero-title",
                ),
                rx.text(
                    State.hero_movie["sinopsis"],
                    class_name="hero-desc",
                ),
                rx.hstack(
                    rx.text("Genres:", class_name="meta-label"),
                    rx.text(
                        State.hero_movie["genero"],
                        class_name="meta-text",
                    ),
                    rx.text(
                        State.hero_movie["clasificacion"],
                        class_name="age-chip",
                    ),
                    spacing="2",
                    wrap="wrap",
                    align="center",
                ),
                rx.hstack(
                    rx.text("★", class_name="star"),
                    rx.text(
                        State.hero_movie["rating"],
                        class_name="rating",
                    ),
                    rx.text("/10", class_name="rating-muted"),
                    spacing="1",
                    align="center",
                ),
                rx.hstack(
                    rx.button(
                        "Comprar ahora",
                        class_name="btn-hero",
                        on_click=State.hero_details,
                    ),
                    rx.button(
                        "Ver trailer",
                        class_name="btn-hero-outline",
                        on_click=State.hero_trailer,
                    ),
                    spacing="3",
                ),
                spacing="3",
                align="start",
                class_name="hero-info",
            ),
            rx.box(
                rx.hstack(
                    rx.foreach(
                        State.hero_cartelera_movies,
                        hero_thumb,
                    ),
                    spacing="3",
                    class_name="hero-thumbs",
                ),
                rx.hstack(
                    rx.button(
                        "‹",
                        class_name="carousel-btn",
                        on_click=State.prev_hero,
                    ),
                    rx.button(
                        "›",
                        class_name="carousel-btn",
                        on_click=State.next_hero,
                    ),
                    spacing="2",
                    class_name="carousel-controls",
                ),
                class_name="hero-side",
            ),
            columns="2",
            spacing="0",
            class_name="hero-grid-layout",
        ),
        class_name="hero",
    )