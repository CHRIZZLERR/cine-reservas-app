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
        rx.text(f"{item['nombre']} x{item['qty']}", class_name="cart-food-name"),
        rx.spacer(),
        money(item["subtotal"]),
        width="100%",
        align="center",
        class_name="cart-food-row",
    )


def account_choice_guest() -> rx.Component:
    return rx.box(
        rx.grid(
            rx.box(
                rx.text("¿Ya tienes una cuenta?", class_name="cc-account-title"),
                rx.text(
                    "Inicia sesión para que este boleto quede guardado automáticamente en tu perfil.",
                    class_name="cc-account-text",
                ),
                rx.link(
                    rx.button(
                        "Iniciar sesión",
                        class_name="cc-account-btn",
                        on_click=State.show_login,
                    ),
                    href="/auth",
                ),
                class_name="cc-account-option",
            ),
            rx.box(
                rx.text("¿Primera vez en JC Cinemas?", class_name="cc-account-title"),
                rx.text(
                    "Regístrate y podrás consultar tus reservas después desde tu cuenta.",
                    class_name="cc-account-text",
                ),
                rx.link(
                    rx.button(
                        "Registrarse",
                        class_name="cc-account-btn cc-account-btn-outline",
                        on_click=State.show_register,
                    ),
                    href="/auth",
                ),
                class_name="cc-account-option",
            ),
            columns="2",
            spacing="3",
            width="100%",
            class_name="cc-account-grid",
        ),
        rx.box(
            rx.text("Continuar como invitado", class_name="cc-guest-heading"),
            rx.text(
                "No necesitas iniciar sesión. Solo completa tus datos y recibirás tu código de reserva.",
                class_name="cc-account-text",
            ),
            class_name="cc-guest-strip",
        ),
        class_name="cc-account-card",
    )


def account_choice_logged() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("✓", class_name="cc-account-check"),
            rx.vstack(
                rx.text("Cuenta conectada", class_name="cc-guest-heading"),
                rx.text(
                    "Tu reserva quedará guardada en tu usuario después de confirmar.",
                    class_name="cc-account-text",
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        rx.grid(
            rx.box(
                rx.text("Cliente", class_name="payment-label"),
                rx.text(State.logged_user_name, class_name="payment-value"),
                class_name="payment-card account-info-card",
            ),
            rx.box(
                rx.text("Correo", class_name="payment-label"),
                rx.text(State.logged_user_email, class_name="payment-value"),
                class_name="payment-card account-info-card",
            ),
            columns="2",
            spacing="3",
            width="100%",
            class_name="account-info-grid",
        ),
        class_name="cc-account-card cc-account-card-logged",
    )


def customer_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("1", class_name="cc-section-number"),
            rx.vstack(
                rx.text("CUENTA", class_name="block-label"),
                rx.text(
                    "Elige si deseas iniciar sesión o continuar como invitado.",
                    class_name="form-subtitle",
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="form-header",
        ),
        rx.cond(State.is_logged_in, account_choice_logged(), account_choice_guest()),
        rx.box(
            rx.text("Datos para la reserva", class_name="cc-form-title"),
            rx.cond(
                State.is_logged_in,
                rx.grid(
                    rx.input(
                        placeholder="Teléfono",
                        value=State.customer_phone,
                        on_change=State.set_customer_phone,
                        class_name="form-input checkout-input-large",
                    ),
                    rx.box(
                        rx.text("Método de pago", class_name="payment-label"),
                        rx.text("Pago en taquilla", class_name="payment-value"),
                        class_name="payment-card pay-method-card",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                    class_name="form-grid checkout-form-grid",
                ),
                rx.grid(
                    rx.input(
                        placeholder="Nombre completo",
                        value=State.customer_name,
                        on_change=State.set_customer_name,
                        class_name="form-input checkout-input-large",
                    ),
                    rx.input(
                        placeholder="Correo electrónico",
                        value=State.customer_email,
                        on_change=State.set_customer_email,
                        class_name="form-input checkout-input-large",
                    ),
                    rx.input(
                        placeholder="Teléfono",
                        value=State.customer_phone,
                        on_change=State.set_customer_phone,
                        class_name="form-input checkout-input-large",
                    ),
                    rx.box(
                        rx.text("Método de pago", class_name="payment-label"),
                        rx.text("Pago en taquilla", class_name="payment-value"),
                        class_name="payment-card pay-method-card",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                    class_name="form-grid checkout-form-grid",
                ),
            ),
            class_name="cc-form-panel",
        ),
        rx.cond(
            State.api_message != "",
            rx.text(State.api_message, class_name="auth-message"),
            rx.text(""),
        ),
        class_name="form-card checkout-section-card customer-form-pro cc-customer-form",
    )


def payment_review() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("4", class_name="cc-section-number"),
            rx.vstack(
                rx.text("PAGO", class_name="block-label"),
                rx.text(
                    "Revisa tu orden y confirma tu reserva. El pago se realizará en taquilla.",
                    class_name="form-subtitle",
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
            class_name="form-header",
        ),
        rx.grid(
            rx.box(
                rx.text("Cliente", class_name="payment-label"),
                rx.text(State.reservation_customer_name, class_name="payment-value"),
                class_name="payment-card pay-method-card",
            ),
            rx.box(
                rx.text("Correo", class_name="payment-label"),
                rx.text(State.reservation_customer_email, class_name="payment-value"),
                class_name="payment-card pay-method-card",
            ),
            rx.box(
                rx.text("Teléfono", class_name="payment-label"),
                rx.text(State.customer_phone, class_name="payment-value"),
                class_name="payment-card pay-method-card",
            ),
            rx.box(
                rx.text("Método de pago", class_name="payment-label"),
                rx.text("Pago en taquilla", class_name="payment-value"),
                class_name="payment-card pay-method-card",
            ),
            columns="2",
            spacing="3",
            width="100%",
            class_name="cc-payment-grid",
        ),
        rx.box(
            rx.hstack(
                rx.text("ℹ", class_name="pickup-icon"),
                rx.vstack(
                    rx.text("Recogida de dulcería", class_name="pickup-title"),
                    rx.text(
                        "Si agregaste comida o bebida, preséntate en el área de caja con tu código de reserva para retirarla.",
                        class_name="pickup-text",
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            class_name="pickup-notice",
        ),
        rx.box(
            rx.hstack(
                rx.text("Boletos", class_name="cart-label"),
                rx.spacer(),
                money(State.total_boletos),
                width="100%",
            ),
            rx.hstack(
                rx.text("Comida y bebida", class_name="cart-label"),
                rx.spacer(),
                money(State.total_comida),
                width="100%",
            ),
            rx.hstack(
                rx.text("Cargo de servicio", class_name="cart-label"),
                rx.spacer(),
                money(State.cargo_servicio),
                width="100%",
            ),
            rx.divider(border_color="rgba(255,255,255,.10)", margin_y="10px"),
            rx.hstack(
                rx.text("Total a pagar", class_name="invoice-total-label"),
                rx.spacer(),
                money(State.gran_total),
                width="100%",
            ),
            class_name="cc-payment-total-card",
        ),
        rx.cond(
            State.api_message != "",
            rx.text(State.api_message, class_name="auth-message"),
            rx.text(""),
        ),
        class_name="form-card checkout-section-card customer-form-pro cc-payment-review",
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
                cart_row("Comida y bebida", State.selected_food_text),
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
            class_name="cart-movie cart-movie-pro",
        ),
        rx.divider(border_color="rgba(255,255,255,.10)", margin_y="14px"),
        cart_row("Función", State.selected_date),
        cart_row("Hora", State.selected_showtime),
        cart_row("Boletas", State.ticket_count),
        cart_row("Asientos", State.selected_seats_text),
        rx.cond(
            State.total_comida > 0,
            rx.box(
                rx.text("Comida y bebida", class_name="cart-section-title"),
                rx.foreach(State.selected_food_items, food_cart_item),
                rx.box(
                    rx.text("Recoger en caja con tu código de reserva.", class_name="pickup-mini"),
                    class_name="pickup-mini-box",
                ),
                class_name="cart-food-list",
            ),
            rx.text("Sin productos de comida y bebida", class_name="cart-empty"),
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
            State.api_message != "",
            rx.text(State.api_message, class_name="auth-message"),
            rx.text(""),
        ),
        rx.cond(
            State.booking_step < 4,
            rx.button(
                State.next_button_text,
                class_name="checkout-btn",
                on_click=State.next_step,
            ),
            rx.button(
                "Confirmar reserva",
                class_name="checkout-btn",
                on_click=State.confirm_reservation,
            ),
        ),
        rx.cond(
            State.booking_step > 1,
            rx.button(
                "Volver al paso anterior",
                class_name="btn-ghost full",
                on_click=State.prev_step,
            ),
            rx.link(
                rx.button("Cambiar película", class_name="btn-ghost full"),
                href="/cartelera",
            ),
        ),
        class_name="invoice cart-panel",
    )