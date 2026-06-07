import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def funcion_card(funcion: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    funcion["pelicula"],
                    color="white",
                    font_size="22px",
                    font_weight="900",
                ),
                rx.text(
                    funcion["sucursal"],
                    color="#b8c0d4",
                    font_size="15px",
                ),
                rx.hstack(
                    rx.box(
                        rx.text("Fecha", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(funcion["fecha"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Hora", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(funcion["hora"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Sala", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(funcion["sala"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Precio", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(funcion["precio_texto"], color="white", font_size="14px"),
                    ),
                    spacing="5",
                    wrap="wrap",
                    margin_top="8px",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.spacer(),
            rx.vstack(
                rx.button(
                    "Editar",
                    on_click=lambda: State.select_admin_funcion(funcion["id"]),
                    background="rgba(107,174,255,.15)",
                    color="#6BAEFF",
                    border="1px solid rgba(107,174,255,.35)",
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                    width="130px",
                ),
                rx.button(
                    "Eliminar",
                    on_click=lambda: State.delete_admin_funcion(funcion["id"]),
                    background="rgba(255,77,109,.16)",
                    color="#ff4d6d",
                    border="1px solid rgba(255,77,109,.35)",
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                    width="130px",
                ),
                spacing="2",
                align="end",
            ),
            width="100%",
            align="center",
            spacing="4",
        ),
        padding="22px",
        border_radius="24px",
        background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 55px rgba(0,0,0,.34)",
        margin_bottom="18px",
    )


def pelicula_option_card(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.text(pelicula["titulo"], color="white", font_weight="900", font_size="14px"),
        rx.text(f"ID: {pelicula['id']} · {pelicula['estado']}", color="#9aa7c0", font_size="12px"),
        padding="14px",
        border_radius="16px",
        background="rgba(255,255,255,.045)",
        border="1px solid rgba(255,255,255,.08)",
    )


def sucursal_option_card(sucursal: dict) -> rx.Component:
    return rx.box(
        rx.text(sucursal["nombre"], color="white", font_weight="900", font_size="14px"),
        rx.text(f"ID: {sucursal['id']} · {sucursal['ciudad']}", color="#9aa7c0", font_size="12px"),
        padding="14px",
        border_radius="16px",
        background="rgba(255,255,255,.045)",
        border="1px solid rgba(255,255,255,.08)",
    )


def funcion_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading(
                rx.cond(
                    State.admin_edit_funcion_id > 0,
                    "Editar función",
                    "Crear función nueva",
                ),
                color="white",
                font_size="28px",
            ),
            rx.spacer(),
            rx.cond(
                State.admin_edit_funcion_id > 0,
                rx.button(
                    "Cancelar edición",
                    on_click=State.clear_admin_funcion_form,
                    background="rgba(255,255,255,.08)",
                    color="white",
                    border="1px solid rgba(255,255,255,.12)",
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                ),
                rx.fragment(),
            ),
            width="100%",
            align="center",
            margin_bottom="18px",
        ),

        rx.text(
            "Usa los ID de película y sucursal que aparecen debajo. Luego podrás mejorar esto con selectores.",
            color="#9aa7c0",
            font_size="14px",
            margin_bottom="18px",
        ),

        rx.grid(
            rx.input(
                placeholder="ID de película",
                value=State.admin_funcion_pelicula_id,
                on_change=State.set_admin_funcion_pelicula_id,
                class_name="form-input",
            ),
            rx.input(
                placeholder="ID de sucursal",
                value=State.admin_funcion_sucursal_id,
                on_change=State.set_admin_funcion_sucursal_id,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Fecha: 2026-06-06",
                value=State.admin_funcion_fecha,
                on_change=State.set_admin_funcion_fecha,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Hora: 18:00:00",
                value=State.admin_funcion_hora,
                on_change=State.set_admin_funcion_hora,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Sala: Sala 1",
                value=State.admin_funcion_sala,
                on_change=State.set_admin_funcion_sala,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Precio: 500",
                value=State.admin_funcion_precio,
                on_change=State.set_admin_funcion_precio,
                class_name="form-input",
            ),
            columns="3",
            spacing="3",
            width="100%",
        ),

        rx.hstack(
            rx.button(
                rx.cond(
                    State.admin_edit_funcion_id > 0,
                    "Guardar cambios",
                    "Crear función",
                ),
                on_click=State.save_admin_funcion,
                background="#d90429",
                color="white",
                border_radius="14px",
                padding="12px 20px",
                font_weight="900",
                border="none",
                cursor="pointer",
            ),
            rx.button(
                "Limpiar formulario",
                on_click=State.clear_admin_funcion_form,
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
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.box(
                rx.heading("Acceso restringido", color="white", font_size="44px"),
                rx.text(
                    "Debes iniciar sesión como administrador para administrar funciones.",
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


def admin_funciones_content() -> rx.Component:
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
                        "Funciones y horarios",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Crea, edita y elimina horarios por película, sucursal, fecha, sala y precio.",
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
                    rx.text("Total funciones", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_funciones, color="white", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Películas disponibles", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_peliculas, color="#6BAEFF", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Sucursales", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_sucursales, color="#FFD60A", font_size="34px"),
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

            funcion_form(),

            rx.grid(
                rx.box(
                    rx.heading("Películas disponibles", color="white", font_size="22px", margin_bottom="14px"),
                    rx.grid(
                        rx.foreach(State.admin_peliculas, pelicula_option_card),
                        columns="2",
                        spacing="3",
                        width="100%",
                    ),
                    padding="22px",
                    border_radius="24px",
                    background="rgba(255,255,255,.035)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.heading("Sucursales disponibles", color="white", font_size="22px", margin_bottom="14px"),
                    rx.grid(
                        rx.foreach(State.admin_sucursales, sucursal_option_card),
                        columns="1",
                        spacing="3",
                        width="100%",
                    ),
                    padding="22px",
                    border_radius="24px",
                    background="rgba(255,255,255,.035)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                columns="2",
                spacing="4",
                width="100%",
                margin_bottom="32px",
            ),

            rx.heading(
                "Funciones registradas",
                color="white",
                font_size="32px",
                margin_bottom="18px",
            ),

            rx.cond(
                State.total_admin_funciones == 0,
                rx.box(
                    rx.heading("No hay funciones registradas", color="white"),
                    rx.text(
                        "Crea una función usando el formulario superior.",
                        color="#b8c0d4",
                        margin_top="8px",
                    ),
                    padding="34px",
                    border_radius="24px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.foreach(State.admin_funciones, funcion_card),
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
        on_mount=State.load_admin_funciones_page,
    )


def admin_funciones_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_funciones_content(),
        access_denied(),
    )