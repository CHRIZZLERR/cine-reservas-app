import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.navbar import navbar, search_overlay, side_menu


def estado_reserva_badge(estado) -> rx.Component:
    return rx.cond(
        estado == "confirmada",
        rx.box(
            "Confirmada",
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
            estado == "cancelada",
            rx.box(
                "Cancelada",
                color="#ff4d6d",
                background="rgba(255,77,109,.12)",
                border="1px solid rgba(255,77,109,.35)",
                padding="6px 12px",
                border_radius="999px",
                font_size="12px",
                font_weight="900",
                text_align="center",
            ),
            rx.box(
                "Pendiente",
                color="#FFD60A",
                background="rgba(255,214,10,.12)",
                border="1px solid rgba(255,214,10,.35)",
                padding="6px 12px",
                border_radius="999px",
                font_size="12px",
                font_weight="900",
                text_align="center",
            ),
        ),
    )


def action_button(text: str, estado: str, reserva_id) -> rx.Component:
    return rx.button(
        text,
        on_click=lambda: State.update_reserva_estado(reserva_id, estado),
        background=rx.cond(
            estado == "confirmada",
            "rgba(34,197,94,.16)",
            rx.cond(
                estado == "cancelada",
                "rgba(255,77,109,.16)",
                "rgba(255,214,10,.16)",
            ),
        ),
        color=rx.cond(
            estado == "confirmada",
            "#22c55e",
            rx.cond(
                estado == "cancelada",
                "#ff4d6d",
                "#FFD60A",
            ),
        ),
        border=rx.cond(
            estado == "confirmada",
            "1px solid rgba(34,197,94,.35)",
            rx.cond(
                estado == "cancelada",
                "1px solid rgba(255,77,109,.35)",
                "1px solid rgba(255,214,10,.35)",
            ),
        ),
        border_radius="12px",
        padding="8px 12px",
        font_weight="900",
        cursor="pointer",
        font_size="12px",
    )


def reserva_card(reserva: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        reserva["codigo_reserva"],
                        color="#FFD60A",
                        font_weight="900",
                        font_size="18px",
                    ),
                    estado_reserva_badge(reserva["estado"]),
                    spacing="3",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(
                    reserva["pelicula"],
                    color="white",
                    font_size="24px",
                    font_weight="900",
                ),
                rx.text(
                    reserva["cliente_texto"],
                    color="#b8c0d4",
                    font_size="14px",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text("Total", color="#9aa7c0", font_size="13px", font_weight="800"),
                rx.text(reserva["total_texto"], color="white", font_size="22px", font_weight="900"),
                align="end",
                spacing="1",
            ),
            width="100%",
            align="start",
        ),

        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="16px"),

        rx.grid(
            rx.box(
                rx.text("Sucursal", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["sucursal"], color="white", font_size="14px"),
            ),
            rx.box(
                rx.text("Fecha", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["fecha"], color="white", font_size="14px"),
            ),
            rx.box(
                rx.text("Hora", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["hora"], color="white", font_size="14px"),
            ),
            rx.box(
                rx.text("Sala", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["sala"], color="white", font_size="14px"),
            ),
            rx.box(
                rx.text("Asientos", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["asientos_texto"], color="white", font_size="14px"),
            ),
            rx.box(
                rx.text("Método de pago", color="#9aa7c0", font_size="12px", font_weight="900"),
                rx.text(reserva["metodo_pago"], color="white", font_size="14px"),
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),

        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="16px"),

        rx.hstack(
            action_button("Pendiente", "pendiente", reserva["id"]),
            action_button("Confirmar", "confirmada", reserva["id"]),
            action_button("Cancelar", "cancelada", reserva["id"]),
            spacing="3",
            wrap="wrap",
        ),

        padding="24px",
        border_radius="24px",
        background="linear-gradient(145deg, rgba(12,16,28,.96), rgba(32,13,30,.90))",
        border="1px solid rgba(255,255,255,.08)",
        box_shadow="0 18px 55px rgba(0,0,0,.34)",
        margin_bottom="18px",
    )


def access_denied() -> rx.Component:
    return rx.box(
        navbar("admin"),
        rx.center(
            rx.box(
                rx.heading("Acceso restringido", color="white", font_size="44px"),
                rx.text(
                    "Debes iniciar sesión como administrador para ver reservas.",
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


def admin_reservas_content() -> rx.Component:
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
                        "Reservas",
                        color="white",
                        font_size="56px",
                        line_height="1",
                    ),
                    rx.text(
                        "Consulta las reservas creadas por los clientes y actualiza su estado.",
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
                    rx.text("Total reservas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_admin_reservas, color="white", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Pendientes", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_reservas_pendientes, color="#FFD60A", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Confirmadas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_reservas_confirmadas, color="#22c55e", font_size="34px"),
                    padding="22px",
                    border_radius="22px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                    min_width="220px",
                ),
                rx.box(
                    rx.text("Canceladas", color="#9aa7c0", font_size="13px", font_weight="800"),
                    rx.heading(State.total_reservas_canceladas, color="#ff4d6d", font_size="34px"),
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

            rx.cond(
                State.total_admin_reservas == 0,
                rx.box(
                    rx.heading("No hay reservas registradas", color="white"),
                    rx.text(
                        "Cuando un cliente cree una reserva, aparecerá aquí.",
                        color="#b8c0d4",
                        margin_top="8px",
                    ),
                    padding="34px",
                    border_radius="24px",
                    background="rgba(255,255,255,.045)",
                    border="1px solid rgba(255,255,255,.08)",
                ),
                rx.box(
                    rx.foreach(State.admin_reservas, reserva_card),
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
        on_mount=State.load_admin_reservas,
    )


def admin_reservas_page() -> rx.Component:
    return rx.cond(
        State.logged_user_role == "admin",
        admin_reservas_content(),
        access_denied(),
    )