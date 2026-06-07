import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def estado_pelicula_badge(estado) -> rx.Component:
    return rx.cond(
        estado == "cartelera",
        rx.box(
            "Cartelera",
            color="#22c55e",
            background="rgba(34,197,94,.12)",
            border="1px solid rgba(34,197,94,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="900",
            text_align="center",
        ),
        rx.cond(
            estado == "proximamente",
            rx.box(
                "Próximamente",
                color="#6BAEFF",
                background="rgba(107,174,255,.12)",
                border="1px solid rgba(107,174,255,.35)",
                padding="6px 12px",
                border_radius="999px",
                font_size="12px",
                font_weight="900",
                text_align="center",
            ),
            rx.box(
                "Inactiva",
                color="#ff4d6d",
                background="rgba(255,77,109,.12)",
                border="1px solid rgba(255,77,109,.35)",
                padding="6px 12px",
                border_radius="999px",
                font_size="12px",
                font_weight="900",
                text_align="center",
            ),
        ),
    )


def activa_badge(activa) -> rx.Component:
    return rx.cond(
        activa,
        rx.box(
            "Activa",
            color="#22c55e",
            background="rgba(34,197,94,.12)",
            border="1px solid rgba(34,197,94,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="900",
            text_align="center",
        ),
        rx.box(
            "Desactivada",
            color="#ff4d6d",
            background="rgba(255,77,109,.12)",
            border="1px solid rgba(255,77,109,.35)",
            padding="6px 12px",
            border_radius="999px",
            font_size="12px",
            font_weight="900",
            text_align="center",
        ),
    )


def pelicula_card(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src=pelicula["poster_url"],
                width="92px",
                height="138px",
                object_fit="cover",
                border_radius="16px",
                border="1px solid rgba(255,255,255,.10)",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        pelicula["titulo"],
                        color="white",
                        font_size="22px",
                        font_weight="900",
                    ),
                    estado_pelicula_badge(pelicula["estado"]),
                    activa_badge(pelicula["activa"]),
                    spacing="3",
                    wrap="wrap",
                    align="center",
                ),
                rx.text(
                    pelicula["sinopsis_corta"],
                    color="#b8c0d4",
                    font_size="14px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.box(
                        rx.text("Género", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(pelicula["genero"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Clasificación", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(pelicula["clasificacion"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Duración", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(pelicula["duracion_texto"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Estreno", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(pelicula["fecha_estreno"], color="white", font_size="14px"),
                    ),
                    spacing="5",
                    wrap="wrap",
                    margin_top="8px",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            align="start",
            spacing="4",
            width="100%",
        ),

        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="16px"),

        rx.hstack(
            rx.button(
                "Editar",
                on_click=lambda: State.select_admin_pelicula(pelicula["id"]),
                background="rgba(107,174,255,.15)",
                color="#6BAEFF",
                border="1px solid rgba(107,174,255,.35)",
                border_radius="12px",
                padding="9px 14px",
                font_weight="900",
                cursor="pointer",
            ),
            rx.button(
                "Desactivar",
                on_click=lambda: State.deactivate_admin_pelicula(pelicula["id"]),
                background="rgba(255,77,109,.16)",
                color="#ff4d6d",
                border="1px solid rgba(255,77,109,.35)",
                border_radius="12px",
                padding="9px 14px",
                font_weight="900",
                cursor="pointer",
            ),
            rx.cond(
                pelicula["trailer"] != "",
                rx.link(
                    rx.button(
                        "Trailer",
                        background="rgba(255,214,10,.14)",
                        color="#FFD60A",
                        border="1px solid rgba(255,214,10,.35)",
                        border_radius="12px",
                        padding="9px 14px",
                        font_weight="900",
                        cursor="pointer",
                    ),
                    href=pelicula["trailer_url"],
                    is_external=True,
                ),
                rx.fragment(),
            ),
            spacing="3",
            wrap="wrap",
        ),

        padding="22px",
        border_radius="24px",
        background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 55px rgba(0,0,0,.34)",
        margin_bottom="18px",
    )


def edit_form() -> rx.Component:
    return rx.cond(
        State.admin_edit_movie_id > 0,
        rx.box(
            rx.hstack(
                rx.heading(
                    "Editar película",
                    color="white",
                    font_size="28px",
                ),
                rx.spacer(),
                rx.button(
                    "Cerrar",
                    on_click=State.clear_admin_pelicula_form,
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
                rx.input(
                    placeholder="Título",
                    value=State.admin_movie_titulo,
                    on_change=State.set_admin_movie_titulo,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Género",
                    value=State.admin_movie_genero,
                    on_change=State.set_admin_movie_genero,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Clasificación",
                    value=State.admin_movie_clasificacion,
                    on_change=State.set_admin_movie_clasificacion,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Duración en minutos",
                    value=State.admin_movie_duracion,
                    on_change=State.set_admin_movie_duracion,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Fecha de estreno",
                    value=State.admin_movie_fecha_estreno,
                    on_change=State.set_admin_movie_fecha_estreno,
                    class_name="form-input",
                ),
                rx.select(
                    ["cartelera", "proximamente", "inactiva"],
                    value=State.admin_movie_estado,
                    on_change=State.set_admin_movie_estado,
                    class_name="form-input",
                ),
                columns="2",
                spacing="3",
                width="100%",
            ),

            rx.text_area(
                placeholder="Sinopsis",
                value=State.admin_movie_sinopsis,
                on_change=State.set_admin_movie_sinopsis,
                class_name="form-input",
                width="100%",
                min_height="120px",
                margin_top="14px",
            ),

            rx.input(
                placeholder="URL del póster",
                value=State.admin_movie_poster_url,
                on_change=State.set_admin_movie_poster_url,
                class_name="form-input",
                width="100%",
                margin_top="14px",
            ),

            rx.hstack(
                rx.button(
                    "Guardar cambios",
                    on_click=State.update_admin_pelicula,
                    background="#d90429",
                    color="white",
                    border_radius="14px",
                    padding="12px 20px",
                    font_weight="900",
                    border="none",
                    cursor="pointer",
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.clear_admin_pelicula_form,
                    background="rgba(255,255,255,.08)",
                    color="white",
                    border="1px solid rgba(255,255,255,.12)",
                    border_radius="14px",
                    padding="12px 20px",
                    font_weight="900",
                    cursor="pointer",
                ),
                spacing="3",
                margin_top="18px",
                wrap="wrap",
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
                    "Debes iniciar sesión como administrador para ver películas.",
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


def admin_peliculas_content() -> rx.Component:
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
                        "Películas",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Gestiona cartelera, próximos estrenos, estado de publicación y datos principales de cada película.",
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

            rx.hstack(
                rx.box(
                    rx.text("Total películas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_peliculas, color="white", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Cartelera", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_peliculas_cartelera, color="#22c55e", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Próximamente", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_peliculas_proximamente, color="#6BAEFF", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Inactivas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_peliculas_inactivas, color="#ff4d6d", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                spacing="4",
                wrap="wrap",
                margin_bottom="30px",
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

            edit_form(),

            rx.cond(
                State.total_admin_peliculas == 0,
                rx.box(
                    rx.heading("No hay películas registradas", color="white"),
                    rx.text(
                        "Cuando agregues o importes películas desde TMDB, aparecerán aquí.",
                        color="#b8c0d4",
                        margin_top="8px",
                    ),
                    padding="34px",
                    border_radius="24px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.foreach(State.admin_peliculas, pelicula_card),
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
        on_mount=State.load_admin_peliculas,
    )


def admin_peliculas_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_peliculas_content(),
        access_denied(),
    )