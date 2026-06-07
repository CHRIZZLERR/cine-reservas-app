import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def tmdb_result_card(movie: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src=movie["poster_url"],
                width="96px",
                height="144px",
                object_fit="cover",
                border_radius="16px",
                border="1px solid rgba(255,255,255,.10)",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        movie["title"],
                        color="white",
                        font_size="22px",
                        font_weight="900",
                    ),
                    rx.box(
                        movie["year"],
                        color="#6BAEFF",
                        background="rgba(107,174,255,.12)",
                        border="1px solid rgba(107,174,255,.35)",
                        padding="5px 10px",
                        border_radius="999px",
                        font_size="12px",
                        font_weight="900",
                    ),
                    rx.box(
                        movie["rating_text"],
                        color="#FFD60A",
                        background="rgba(255,214,10,.12)",
                        border="1px solid rgba(255,214,10,.35)",
                        padding="5px 10px",
                        border_radius="999px",
                        font_size="12px",
                        font_weight="900",
                    ),
                    spacing="3",
                    wrap="wrap",
                    align="center",
                ),
                rx.text(
                    movie["overview_short"],
                    color="#b8c0d4",
                    font_size="14px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.button(
                        "Importar a JC Cinemas",
                        on_click=lambda: State.import_tmdb_movie(movie["id"]),
                        background="#d90429",
                        color="white",
                        border_radius="14px",
                        padding="10px 16px",
                        font_weight="900",
                        border="none",
                        cursor="pointer",
                    ),
                    rx.button(
                        "Ver detalle",
                        on_click=lambda: State.load_tmdb_detail(movie["id"]),
                        background="rgba(107,174,255,.15)",
                        color="#6BAEFF",
                        border="1px solid rgba(107,174,255,.35)",
                        border_radius="14px",
                        padding="10px 16px",
                        font_weight="900",
                        cursor="pointer",
                    ),
                    spacing="3",
                    wrap="wrap",
                    margin_top="10px",
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="22px",
        border_radius="24px",
        background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 55px rgba(0,0,0,.34)",
        margin_bottom="18px",
    )


def tmdb_detail_box() -> rx.Component:
    return rx.cond(
        State.tmdb_detail_loaded,
        rx.box(
            rx.hstack(
                rx.heading(
                    State.tmdb_detail_title,
                    color="white",
                    font_size="30px",
                ),
                rx.spacer(),
                rx.button(
                    "Cerrar detalle",
                    on_click=State.clear_tmdb_detail,
                    background="rgba(255,255,255,.08)",
                    color="white",
                    border="1px solid rgba(255,255,255,.12)",
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
                margin_bottom="18px",
            ),
            rx.grid(
                rx.image(
                    src=State.tmdb_detail_poster,
                    width="170px",
                    height="255px",
                    object_fit="cover",
                    border_radius="18px",
                    border="1px solid rgba(255,255,255,.10)",
                ),
                rx.vstack(
                    rx.text(
                        State.tmdb_detail_overview,
                        color="#b8c0d4",
                        font_size="15px",
                        line_height="1.7",
                    ),
                    rx.hstack(
                        rx.box(
                            rx.text("Estreno", color="#9aa7c0", font_size="12px", font_weight="900"),
                            rx.text(State.tmdb_detail_release_date, color="white", font_size="14px"),
                        ),
                        rx.box(
                            rx.text("Rating", color="#9aa7c0", font_size="12px", font_weight="900"),
                            rx.text(State.tmdb_detail_rating, color="white", font_size="14px"),
                        ),
                        rx.box(
                            rx.text("TMDB ID", color="#9aa7c0", font_size="12px", font_weight="900"),
                            rx.text(State.tmdb_detail_id, color="white", font_size="14px"),
                        ),
                        spacing="5",
                        wrap="wrap",
                    ),
                    rx.button(
                        "Importar esta película",
                        on_click=lambda: State.import_tmdb_movie(State.tmdb_detail_id_int),
                        background="#d90429",
                        color="white",
                        border_radius="14px",
                        padding="12px 18px",
                        font_weight="900",
                        border="none",
                        cursor="pointer",
                        margin_top="10px",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                ),
                columns="2",
                spacing="5",
                width="100%",
            ),
            padding="26px",
            border_radius="26px",
            background="linear-gradient(145deg, rgba(12,16,28,.98), rgba(32,13,30,.92))",
            border="1px solid rgba(255,255,255,.09)",
            box_shadow="0 20px 65px rgba(0,0,0,.40)",
            margin_bottom="28px",
        ),
        rx.fragment(),
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.box(
                rx.heading("Acceso restringido", color="white", font_size="44px"),
                rx.text(
                    "Debes iniciar sesión como administrador para importar películas desde TMDB.",
                    color="#b8c0d4",
                    margin_top="12px",
                    margin_bottom="22px",
                ),
                rx.link(
                    rx.button("Iniciar sesión", background="#d90429", color="white"),
                    href="/auth",
                ),
                padding="44px",
                border_radius="26px",
                background="rgba(12,16,28,.95)",
                border="1px solid rgba(255,255,255,.10)",
                text_align="center",
            ),
            min_height="80vh",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )


def admin_tmdb_content() -> rx.Component:
    return rx.box(
        navbar("admin"),

        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "ADMINISTRACIÓN",
                        color="#ff004c",
                        letter_spacing="8px",
                        font_size="13px",
                        font_weight="900",
                    ),
                    rx.heading(
                        "Importar desde TMDB",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Busca películas reales desde TMDB e impórtalas directo a la base de datos de JC Cinemas.",
                        color="#b8c0d4",
                        font_size="17px",
                        max_width="850px",
                        line_height="1.7",
                    ),
                    spacing="3",
                    align="start",
                ),
                rx.spacer(),
                rx.link(
                    rx.button(
                        "Volver al panel",
                        background="rgba(255,255,255,.08)",
                        color="white",
                        border="1px solid rgba(255,255,255,.12)",
                        border_radius="14px",
                        padding="12px 20px",
                        font_weight="900",
                        cursor="pointer",
                    ),
                    href="/admin",
                ),
                width="100%",
                align="center",
                wrap="wrap",
                margin_bottom="34px",
            ),

            rx.box(
                rx.heading(
                    "Buscar película",
                    color="white",
                    font_size="28px",
                    margin_bottom="14px",
                ),
                rx.text(
                    "Ejemplo: Superman, F1, Jurassic World, Ballerina, Toy Story.",
                    color="#9aa7c0",
                    font_size="14px",
                    margin_bottom="18px",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Escribe el nombre de la película...",
                        value=State.tmdb_query,
                        on_change=State.set_tmdb_query,
                        class_name="form-input",
                        width="100%",
                    ),
                    rx.button(
                        "Buscar",
                        on_click=State.search_tmdb_movies,
                        background="#d90429",
                        color="white",
                        border_radius="14px",
                        padding="12px 24px",
                        font_weight="900",
                        border="none",
                        cursor="pointer",
                    ),
                    spacing="3",
                    width="100%",
                    align="center",
                ),
                padding="26px",
                border_radius="26px",
                background="linear-gradient(145deg, rgba(12,16,28,.98), rgba(32,13,30,.92))",
                border="1px solid rgba(255,255,255,.09)",
                box_shadow="0 20px 65px rgba(0,0,0,.40)",
                margin_bottom="28px",
            ),

            rx.cond(
                State.admin_message != "",
                rx.box(
                    State.admin_message,
                    color="#FFD60A",
                    background="rgba(255,214,10,.10)",
                    border="1px solid rgba(255,214,10,.25)",
                    padding="14px 18px",
                    border_radius="16px",
                    margin_bottom="20px",
                    font_weight="800",
                ),
                rx.fragment(),
            ),

            tmdb_detail_box(),

            rx.cond(
                State.tmdb_results_count == 0,
                rx.box(
                    rx.heading("Sin resultados todavía", color="white"),
                    rx.text(
                        "Busca una película para ver resultados desde TMDB.",
                        color="#b8c0d4",
                        margin_top="8px",
                    ),
                    padding="34px",
                    border_radius="24px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.heading(
                        "Resultados encontrados",
                        color="white",
                        font_size="30px",
                        margin_bottom="18px",
                    ),
                    rx.foreach(State.tmdb_results, tmdb_result_card),
                    width="100%",
                ),
            ),

            padding_x="7%",
            padding_top="70px",
            padding_bottom="90px",
        ),

        search_overlay(),
        side_menu(),
        class_name="page",
    )


def admin_tmdb_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_tmdb_content(),
        access_denied(),
    )