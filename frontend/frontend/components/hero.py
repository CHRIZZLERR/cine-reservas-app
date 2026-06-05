import reflex as rx  # type: ignore[import]

try:
    from state import State
    from data import HERO_SLIDES
    from components.navbar import navbar
except ModuleNotFoundError:
    from ..state import State
    from ..data import HERO_SLIDES
    from .navbar import navbar


def hero_thumb(movie: dict, idx: int) -> rx.Component:
    return rx.box(
        rx.el.img(
            src=movie["poster"],
            alt=movie["titulo"],
            style={"width": "110px", "height": "165px", "objectFit": "cover",
                   "borderRadius": "12px", "border": "1.5px solid rgba(255,255,255,.12)",
                   "boxShadow": "0 18px 45px rgba(0,0,0,.65)", "display": "block"},
        ),
        rx.text(movie["titulo"], class_name="hero-thumb-title"),
        class_name=rx.cond(
            State.hero_index == idx,
            "hero-thumb hero-thumb-active",
            "hero-thumb",
        ),
        on_click=lambda: State.go_to_slide(idx),
    )


def hero_section() -> rx.Component:
    return rx.box(
        rx.el.img(
            src=State.hero_movie["image"],
            alt="",
            style={
                "position": "absolute", "inset": "0",
                "width": "100%", "height": "100%",
                "objectFit": "cover", "objectPosition": "center top",
                "filter": "saturate(1.08) contrast(1.06)",
                "animation": "kenBurns 12s ease-in-out infinite alternate",
                "zIndex": "0",
            },
        ),
        rx.box(class_name="hero-layer"),
        navbar("inicio"),
        rx.button("", id="auto-next-hero", on_click=State.next_hero, style={"display": "none"}),
        rx.script(
            "(function(){if(window.__cinehubHeroTimer){clearInterval(window.__cinehubHeroTimer);}"
            "window.__cinehubHeroTimer=setInterval(function(){"
            "const btn=document.getElementById('auto-next-hero');"
            "if(btn){btn.click();}},5000);})();"
        ),
        rx.grid(
            rx.vstack(
                rx.text("new", class_name="hero-badge"),
                rx.heading(State.hero_movie["titulo"], class_name="hero-title"),
                rx.text(State.hero_movie["sinopsis"], class_name="hero-desc"),
                rx.hstack(
                    rx.text("Genres:", class_name="meta-label"),
                    rx.text(State.hero_movie["genero"], class_name="meta-text"),
                    rx.text(State.hero_movie["clasificacion"], class_name="age-chip"),
                    spacing="2", wrap="wrap", align="center",
                ),
                rx.hstack(
                    rx.text("★", class_name="star"),
                    rx.text(State.hero_movie["rating"], class_name="rating"),
                    rx.text("/10", class_name="rating-muted"),
                    spacing="1", align="center",
                ),
                rx.hstack(
                    rx.button("Comprar ahora", class_name="btn-hero", on_click=State.hero_details),
                    rx.button("Ver trailer", class_name="btn-hero-outline", on_click=State.hero_trailer),
                    spacing="3",
                ),
                spacing="3", align="start", class_name="hero-info",
            ),
            rx.box(
                rx.hstack(
                    *[hero_thumb(movie, idx) for idx, movie in enumerate(HERO_SLIDES[:6])],
                    spacing="3", class_name="hero-thumbs",
                ),
                rx.hstack(
                    rx.button("‹", class_name="carousel-btn", on_click=State.prev_hero),
                    rx.button("›", class_name="carousel-btn", on_click=State.next_hero),
                    spacing="2", class_name="carousel-controls",
                ),
                class_name="hero-side",
            ),
            columns="2", spacing="0", class_name="hero-grid-layout",
        ),
        class_name="hero",
    )