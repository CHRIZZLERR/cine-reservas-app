import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.food_menu import money
except ModuleNotFoundError:
    from ..state import State
    from .food_menu import money


def cart_row(label: str, value) -> rx.Component:
    return rx.hstack(
        rx.text(label, class_name="cart-label"),
        rx.spacer(),
        value if isinstance(value, rx.Component) else rx.text(value, class_name="cart-value"),
        width="100%",
        align="center",
        class_name="cart-row",
    )


def food_cart_item(item: dict) -> rx.Component:
    return rx.hstack(
        rx.text(
            f"{item['nombre']} x{item['qty']}",
            class_name="cart-food-name",
        ),
        rx.spacer(),
        money(item["subtotal"]),
        width="100%",
        align="center",
        class_name="cart-food-row",
    )


def customer_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("👤", class_name="form-icon"),
            rx.vstack(
                rx.text("DATOS DEL CLIENTE", class_name="block-label"),
                rx.cond(
                    State.is_logged_in,
                    rx.text(
                        "Ya iniciaste sesión. Usaremos tu nombre y correo de la cuenta.",
                        class_name="form-subtitle",
                    ),
                    rx.text(
                        "Completa tus datos para generar tu ticket y código QR.",
                        class_name="form-subtitle",
                    ),
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="form-header",
        ),
        rx.cond(
            State.is_logged_in,
            rx.vstack(
                rx.grid(
                    rx.box(
                        rx.text("Cliente", class_name="payment-label"),
                        rx.text(State.logged_user_name, class_name="payment-value"),
                        class_name="payment-card",
                    ),
                    rx.box(
                        rx.text("Correo", class_name="payment-label"),
                        rx.text(State.logged_user_email, class_name="payment-value"),
                        class_name="payment-card",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.input(
                    placeholder="Teléfono",
                    value=State.customer_phone,
                    on_change=State.set_customer_phone,
                    class_name="form-input",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            rx.grid(
                rx.input(
                    placeholder="Nombre completo",
                    value=State.customer_name,
                    on_change=State.set_customer_name,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Correo electrónico",
                    value=State.customer_email,
                    on_change=State.set_customer_email,
                    class_name="form-input",
                ),
                rx.input(
                    placeholder="Teléfono",
                    value=State.customer_phone,
                    on_change=State.set_customer_phone,
                    class_name="form-input",
                ),
                rx.box(
                    rx.text("Método de pago", class_name="payment-label"),
                    rx.text("Pago en taquilla", class_name="payment-value"),
                    class_name="payment-card",
                ),
                columns="2",
                spacing="3",
                width="100%",
                class_name="form-grid",
            ),
        ),
        class_name="form-card checkout-section-card",
    )


def confirmation() -> rx.Component:
    return rx.box(
        rx.grid(
            rx.box(
                rx.text("✅", class_name="ticket-icon"),
                rx.heading("Reserva confirmada", class_name="ticket-title"),
                rx.text("Tu ticket fue generado correctamente.", class_name="ticket-muted"),
                rx.text(State.reservation_code, class_name="ticket-code"),
                rx.image(src=State.reservation_qr_url, class_name="reservation-qr"),
                rx.hstack(
                    rx.link(
                        rx.button("Enviar QR al correo", class_name="btn-primary-lg"),
                        href=State.reservation_email_link,
                    ),
                    rx.button(
                        "Reservar otra boleta",
                        class_name="btn-ghost",
                        on_click=State.new_booking,
                    ),
                    spacing="3",
                    wrap="wrap",
                    justify="center",
                ),
                class_name="ticket-left",
            ),
            rx.box(
                rx.text("RESUMEN DEL TICKET", class_name="ticket-kicker"),
                rx.heading(State.current_movie["titulo"], class_name="ticket-movie"),
                cart_row("Cine", State.selected_location),
                cart_row("Fecha", State.selected_date),
                cart_row("Hora", State.selected_showtime),
                cart_row("Asientos", State.selected_seats_text),
                cart_row("Dulcería", State.selected_food_text),
                rx.divider(border_color="rgba(255,255,255,.10)", margin_y="10px"),
                cart_row("Boletos", money(State.total_boletos)),
                cart_row("Comida", money(State.total_comida)),
                cart_row("Servicio", money(State.cargo_servicio)),
                rx.hstack(
                    rx.text("Total", class_name="ticket-total-label"),
                    rx.spacer(),
                    money(State.gran_total),
                    class_name="ticket-total",
                    width="100%",
                ),
                rx.link(
                    rx.button("Volver al inicio", class_name="btn-ghost full"),
                    href="/",
                    width="100%",
                ),
                class_name="ticket-right",
            ),
            columns="2",
            spacing="5",
            width="100%",
            class_name="ticket-grid",
        ),
        class_name="confirm-ticket-card",
    )


def invoice() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("🛒", class_name="cart-icon"),
            rx.vstack(
                rx.heading("Tu carrito", class_name="invoice-title"),
                rx.text(State.current_step_name, class_name="invoice-muted"),
                spacing="0",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="cart-header",
        ),
        rx.box(
            rx.image(src=State.current_movie["poster"], class_name="cart-poster"),
            rx.vstack(
                rx.text(State.current_movie["titulo"], class_name="invoice-movie"),
                rx.text(State.current_movie["genero"], class_name="invoice-muted"),
                rx.text(State.selected_location, class_name="invoice-muted"),
                spacing="1",
                align="start",
            ),
            class_name="cart-movie",
        ),
        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="14px"),
        cart_row("Función", State.selected_date),
        cart_row("Hora", State.selected_showtime),
        cart_row("Boletas", State.ticket_count),
        cart_row("Asientos", State.selected_seats_text),
        rx.cond(
            State.total_comida > 0,
            rx.box(
                rx.text("Dulcería", class_name="cart-section-title"),
                rx.foreach(State.selected_food_items, food_cart_item),
                class_name="cart-food-list",
            ),
            rx.text("Sin productos de dulcería", class_name="cart-empty"),
        ),
        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="14px"),
        cart_row("Subtotal boletos", money(State.total_boletos)),
        cart_row("Subtotal comida", money(State.total_comida)),
        cart_row("Cargo servicio", money(State.cargo_servicio)),
        rx.hstack(
            rx.text("Total", class_name="invoice-total-label"),
            rx.spacer(),
            money(State.gran_total),
            width="100%",
            class_name="cart-total-row",
        ),
        rx.cond(
            State.booking_step == 1,
            rx.button(
                State.next_button_text,
                class_name="checkout-btn",
                on_click=State.next_step,
            ),
            rx.cond(
                State.booking_step == 2,
                rx.button(
                    State.next_button_text,
                    class_name="checkout-btn",
                    on_click=State.next_step,
                ),
                rx.button(
                    State.next_button_text,
                    class_name="checkout-btn",
                    on_click=State.confirm_reservation,
                ),
            ),
        ),
        rx.cond(
            State.booking_step > 1,
            rx.button("Volver al paso anterior", class_name="btn-ghost full", on_click=State.prev_step),
            rx.link(rx.button("Cambiar película", class_name="btn-ghost full"), href="/cartelera"),
        ),
        class_name="invoice cart-panel",
    )