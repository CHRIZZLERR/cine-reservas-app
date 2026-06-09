import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def back_button() -> rx.Component:
    return rx.link(
        rx.button(
            "← Volver al panel",
            background="rgba(255,255,255,.06)",
            color="white",
            border="1px solid rgba(255,255,255,.12)",
            border_radius="14px",
            padding="10px 16px",
            font_weight="800",
            cursor="pointer",
        ),
        href="/admin",
        text_decoration="none",
    )


def stat_card(label: str, value, detail: str) -> rx.Component:
    return rx.box(
        rx.text(label, color="#aab4ca", font_size="13px", font_weight="800"),
        rx.heading(value, color="white", font_size="34px", margin_y="8px"),
        rx.text(detail, color="#7f8aa3", font_size="13px"),
        padding="22px",
        border_radius="22px",
        background="rgba(255,255,255,.045)",
        border="1px solid rgba(255,255,255,.08)",
    )


def form_input(label: str, value, on_change, placeholder: str = "") -> rx.Component:
    return rx.box(
        rx.text(label, color="#aab4ca", font_size="12px", font_weight="900", letter_spacing="2px", margin_bottom="8px"),
        rx.input(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            background="#090d17",
            color="white",
            border="1px solid rgba(255,255,255,.14)",
            border_radius="14px",
            padding="12px 14px",
            outline="none",
        ),
    )


def comida_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading(
                rx.cond(State.admin_edit_comida_id > 0, "Editar comida", "Nueva comida"),
                color="white",
                font_size="30px",
            ),
            rx.spacer(),
            rx.button(
                "Limpiar",
                on_click=State.clear_admin_comida_form,
                background="rgba(255,255,255,.07)",
                color="white",
                border="1px solid rgba(255,255,255,.12)",
                border_radius="14px",
                padding="10px 16px",
                font_weight="800",
                cursor="pointer",
            ),
            width="100%",
            align="center",
            margin_bottom="20px",
        ),
        rx.grid(
            form_input("NOMBRE", State.admin_comida_nombre, State.set_admin_comida_nombre, "Ej: Combo palomitas"),
            form_input("PRECIO", State.admin_comida_precio, State.set_admin_comida_precio, "Ej: 250"),
            columns="2",
            spacing="4",
            width="100%",
        ),
        rx.box(height="16px"),
        form_input("DESCRIPCIÓN", State.admin_comida_descripcion, State.set_admin_comida_descripcion, "Descripción del producto"),
        rx.box(height="16px"),
        form_input("IMAGEN URL", State.admin_comida_imagen_url, State.set_admin_comida_imagen_url, "Link de imagen o placeholder"),
        rx.box(height="16px"),
        rx.hstack(
            rx.checkbox(
                "Activa",
                checked=State.admin_comida_activa,
                on_change=State.set_admin_comida_activa,
                color_scheme="red",
            ),
            rx.spacer(),
            rx.button(
                rx.cond(State.admin_edit_comida_id > 0, "Guardar cambios", "Crear comida"),
                on_click=State.save_admin_comida,
                background="#d90429",
                color="white",
                border="none",
                border_radius="16px",
                padding="13px 24px",
                font_weight="900",
                cursor="pointer",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            State.admin_message != "",
            rx.box(
                State.admin_message,
                color="#FFD60A",
                background="rgba(255,214,10,.10)",
                border="1px solid rgba(255,214,10,.25)",
                padding="12px 16px",
                border_radius="14px",
                margin_top="18px",
                font_weight="800",
            ),
            rx.fragment(),
        ),
        padding="26px",
        border_radius="26px",
        background="linear-gradient(145deg, rgba(18,24,39,.96), rgba(30,12,27,.92))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 45px rgba(0,0,0,.35)",
    )


def comida_row(comida: dict) -> rx.Component:
    return rx.box(
        rx.grid(
            rx.vstack(
                rx.text(comida["nombre"], color="white", font_weight="900", font_size="17px"),
                rx.text(comida["descripcion"], color="#aab4ca", font_size="13px", line_height="1.5"),
                rx.text(comida["imagen_url"], color="#6f7b91", font_size="11px", no_of_lines=1),
                spacing="1",
                align="start",
            ),
            rx.text(comida["precio_texto"], color="#FFD60A", font_weight="900"),
            rx.badge(
                rx.cond(comida["activa"], "Activa", "Inactiva"),
                color_scheme=rx.cond(comida["activa"], "green", "red"),
            ),
            rx.hstack(
                rx.button(
                    "Editar",
                    on_click=lambda: State.select_admin_comida(comida["id"]),
                    background="rgba(255,255,255,.07)",
                    color="white",
                    border="1px solid rgba(255,255,255,.12)",
                    border_radius="12px",
                    font_weight="800",
                    cursor="pointer",
                ),
                rx.button(
                    rx.cond(comida["activa"], "Desactivar", "Activar"),
                    on_click=lambda: State.toggle_admin_comida_status(comida["id"]),
                    background=rx.cond(comida["activa"], "#7a0014", "#116b3a"),
                    color="white",
                    border="none",
                    border_radius="12px",
                    font_weight="800",
                    cursor="pointer",
                ),
                spacing="2",
                justify="end",
            ),
            columns="4",
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="18px",
        border_radius="18px",
        background="rgba(255,255,255,.04)",
        border="1px solid rgba(255,255,255,.08)",
        margin_bottom="12px",
    )


def comidas_table() -> rx.Component:
    return rx.box(
        rx.heading("Comidas registradas", color="white", font_size="30px", margin_bottom="18px"),
        rx.cond(
            State.admin_comidas.length() > 0,
            rx.box(
                rx.foreach(State.admin_comidas, comida_row),
                width="100%",
            ),
            rx.box(
                rx.text("No hay comidas registradas.", color="#aab4ca", font_weight="800"),
                padding="24px",
                border_radius="18px",
                background="rgba(255,255,255,.04)",
                border="1px solid rgba(255,255,255,.08)",
            ),
        ),
        padding="26px",
        border_radius="26px",
        background="rgba(255,255,255,.035)",
        border="1px solid rgba(255,255,255,.08)",
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.vstack(
                rx.heading("Acceso restringido", color="white", font_size="46px"),
                rx.text("Debes iniciar sesión como administrador.", color="#b8c0d4"),
                rx.link(rx.button("Iniciar sesión", background="#d90429", color="white"), href="/auth"),
                spacing="4",
                align="center",
            ),
            min_height="80vh",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )


def admin_comidas_dashboard() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.box(
            rx.hstack(
                back_button(),
                rx.spacer(),
                rx.button(
                    "Recargar",
                    on_click=State.load_admin_comidas,
                    background="rgba(255,255,255,.07)",
                    color="white",
                    border="1px solid rgba(255,255,255,.12)",
                    border_radius="14px",
                    padding="10px 16px",
                    font_weight="800",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
                padding_top="42px",
            ),
            rx.text("ADMINISTRACIÓN", color="#ff004c", letter_spacing="8px", font_size="13px", font_weight="900", margin_top="34px"),
            rx.heading("Comidas y bebidas", color="white", font_size="54px", line_height="1", margin_top="10px"),
            rx.text(
                "Crea, edita y activa o desactiva los productos de dulcería que aparecen en el checkout.",
                color="#b8c0d4",
                font_size="17px",
                max_width="820px",
                line_height="1.7",
                margin_top="12px",
            ),
            rx.grid(
                stat_card("Total comidas", State.total_admin_comidas, "Productos registrados"),
                stat_card("Activas", State.total_comidas_activas, "Se muestran al cliente"),
                stat_card("Inactivas", State.total_comidas_inactivas, "Ocultas del checkout"),
                columns="3",
                spacing="4",
                width="100%",
                margin_y="34px",
            ),
            rx.grid(
                comida_form(),
                comidas_table(),
                columns="2",
                spacing="5",
                width="100%",
            ),
            padding_x="7%",
            padding_bottom="80px",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
        on_mount=State.load_admin_comidas_page,
    )


def admin_comidas_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_comidas_dashboard(),
        access_denied(),
    )
