import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def sucursal_card(sucursal: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        sucursal["nombre"],
                        color="white",
                        font_size="24px",
                        font_weight="900",
                    ),
                    rx.box(
                        rx.text(
                            rx.cond(sucursal["activa"], "Activa", "Inactiva"),
                            color=rx.cond(sucursal["activa"], "#25d366", "#ff4d6d"),
                            font_size="12px",
                            font_weight="900",
                        ),
                        padding="6px 12px",
                        border_radius="999px",
                        background=rx.cond(
                            sucursal["activa"],
                            "rgba(37,211,102,.13)",
                            "rgba(255,77,109,.13)",
                        ),
                        border=rx.cond(
                            sucursal["activa"],
                            "1px solid rgba(37,211,102,.28)",
                            "1px solid rgba(255,77,109,.28)",
                        ),
                    ),
                    spacing="3",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(
                    sucursal["direccion"],
                    color="#b8c0d4",
                    font_size="15px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.box(
                        rx.text("ID", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(sucursal["id"], color="white", font_size="14px"),
                    ),
                    rx.box(
                        rx.text("Ciudad", color="#9aa7c0", font_size="12px", font_weight="900"),
                        rx.text(sucursal["ciudad"], color="white", font_size="14px"),
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
                    on_click=lambda: State.select_admin_sucursal(sucursal["id"]),
                    background="rgba(107,174,255,.15)",
                    color="#6BAEFF",
                    border="1px solid rgba(107,174,255,.35)",
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                    width="150px",
                ),
                rx.button(
                    rx.cond(sucursal["activa"], "Desactivar", "Activar"),
                    on_click=lambda: State.toggle_admin_sucursal_status(sucursal["id"]),
                    background=rx.cond(
                        sucursal["activa"],
                        "rgba(255,77,109,.16)",
                        "rgba(37,211,102,.14)",
                    ),
                    color=rx.cond(sucursal["activa"], "#ff4d6d", "#25d366"),
                    border=rx.cond(
                        sucursal["activa"],
                        "1px solid rgba(255,77,109,.35)",
                        "1px solid rgba(37,211,102,.28)",
                    ),
                    border_radius="12px",
                    padding="9px 14px",
                    font_weight="900",
                    cursor="pointer",
                    width="150px",
                ),
                spacing="2",
                align="end",
            ),
            width="100%",
            align="center",
            spacing="4",
        ),
        padding="24px",
        border_radius="24px",
        background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 55px rgba(0,0,0,.34)",
        margin_bottom="18px",
    )


def sucursal_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading(
                rx.cond(
                    State.admin_edit_sucursal_id > 0,
                    "Editar sucursal",
                    "Crear sucursal nueva",
                ),
                color="white",
                font_size="30px",
            ),
            rx.spacer(),
            rx.cond(
                State.admin_edit_sucursal_id > 0,
                rx.button(
                    "Cancelar edición",
                    on_click=State.clear_admin_sucursal_form,
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
            "Administra las ubicaciones donde JC Cinemas tiene funciones disponibles.",
            color="#9aa7c0",
            font_size="14px",
            margin_bottom="18px",
        ),

        rx.grid(
            rx.input(
                placeholder="Nombre de la sucursal",
                value=State.admin_sucursal_nombre,
                on_change=State.set_admin_sucursal_nombre,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Ciudad",
                value=State.admin_sucursal_ciudad,
                on_change=State.set_admin_sucursal_ciudad,
                class_name="form-input",
            ),
            rx.input(
                placeholder="Dirección",
                value=State.admin_sucursal_direccion,
                on_change=State.set_admin_sucursal_direccion,
                class_name="form-input",
            ),
            columns="3",
            spacing="3",
            width="100%",
        ),

        rx.hstack(
            rx.button(
                rx.cond(
                    State.admin_edit_sucursal_id > 0,
                    "Guardar cambios",
                    "Crear sucursal",
                ),
                on_click=State.save_admin_sucursal,
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
                on_click=State.clear_admin_sucursal_form,
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
                    "Debes iniciar sesión como administrador para administrar sucursales.",
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


def admin_sucursales_content() -> rx.Component:
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
                        "Sucursales",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Crea, edita, activa y desactiva las ubicaciones disponibles de JC Cinemas.",
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
                    rx.text("Total sucursales", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_sucursales, color="white", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Activas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_sucursales_activas, color="#25d366", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Inactivas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_sucursales_inactivas, color="#ff4d6d", font_size="34px"),
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

            sucursal_form(),

            rx.heading(
                "Sucursales registradas",
                color="white",
                font_size="32px",
                margin_bottom="18px",
            ),

            rx.cond(
                State.total_admin_sucursales == 0,
                rx.box(
                    rx.heading("No hay sucursales registradas", color="white"),
                    rx.text(
                        "Crea una sucursal usando el formulario superior.",
                        color="#b8c0d4",
                        margin_top="8px",
                    ),
                    padding="34px",
                    border_radius="24px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.foreach(State.admin_sucursales, sucursal_card),
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
        on_mount=State.load_admin_sucursales_page,
    )


def admin_sucursales_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_sucursales_content(),
        access_denied(),
    )