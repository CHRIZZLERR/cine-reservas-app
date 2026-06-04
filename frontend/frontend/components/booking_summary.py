import reflex as rx  # type: ignore[import]
from ..state import State
from .food_menu import money


def customer_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("👤", class_name="form-icon"),
            rx.vstack(
                rx.text("DATOS DE RESERVA", class_name="block-label"),
                rx.text("Completa tus datos para generar el código de reserva.", class_name="form-subtitle"),
                spacing="1", align="start",
            ),
            align="center", spacing="3", class_name="form-header",
        ),
        rx.grid(
            rx.input(placeholder="Nombre completo", value=State.customer_name, on_change=State.set_customer_name, class_name="form-input"),
            rx.input(placeholder="Correo electrónico", value=State.customer_email, on_change=State.set_customer_email, class_name="form-input"),
            rx.input(placeholder="Teléfono", value=State.customer_phone, on_change=State.set_customer_phone, class_name="form-input"),
            rx.box(
                rx.text("Método de pago", class_name="payment-label"),
                rx.text("Pago en taquilla", class_name="payment-value"),
                class_name="payment-card",
            ),
            columns="2", spacing="3", width="100%", class_name="form-grid",
        ),
        class_name="form-card",
    )


def confirmation() -> rx.Component:
    return rx.box(
        rx.text("✅", class_name="confirm-icon"),
        rx.heading("Reserva confirmada", class_name="confirm-title"),
        rx.text("Tu código de reserva es:", class_name="muted"),
        rx.text(State.reservation_code, class_name="reservation-code"),
        rx.text("Presenta este código en taquilla para completar el pago.", class_name="muted"),
        rx.link(rx.button("Volver al inicio", class_name="btn-primary-lg"), href="/"),
        class_name="confirm-card",
    )


def invoice() -> rx.Component:
    return rx.box(
        rx.heading("Factura", class_name="invoice-title"),
        rx.text(State.current_movie["titulo"], class_name="invoice-movie"),
        rx.text(State.selected_location, class_name="invoice-muted"),
        rx.hstack(
            rx.text(State.selected_date, class_name="invoice-muted"),
            rx.text("·", class_name="invoice-muted"),
            rx.text(State.selected_showtime, class_name="invoice-muted"),
            spacing="1",
        ),
        rx.divider(border_color="rgba(255,255,255,.10)"),
        rx.hstack(rx.text("Asientos", class_name="invoice-line"), rx.spacer(), rx.text(State.selected_seats_text, class_name="invoice-line")),
        rx.hstack(rx.text("Boletos", class_name="invoice-line"), rx.spacer(), money(State.total_boletos)),
        rx.hstack(rx.text("Comida", class_name="invoice-line"), rx.spacer(), money(State.total_comida)),
        rx.hstack(rx.text("Cargo servicio", class_name="invoice-line"), rx.spacer(), money(State.cargo_servicio)),
        rx.divider(border_color="rgba(255,255,255,.10)"),
        rx.hstack(rx.text("Total", class_name="invoice-total-label"), rx.spacer(), money(State.gran_total)),
        rx.cond(
            State.booking_step == 1,
            rx.button("Siguiente: comida", class_name="checkout-btn", on_click=State.next_step),
            rx.cond(
                State.booking_step == 2,
                rx.button("Siguiente: datos", class_name="checkout-btn", on_click=State.next_step),
                rx.cond(
                    State.booking_step == 3,
                    rx.button("Confirmar reserva", class_name="checkout-btn", on_click=State.confirm_reservation),
                    rx.button("Reserva creada", class_name="checkout-btn"),
                ),
            ),
        ),
        rx.button("Volver", class_name="btn-ghost full", on_click=State.prev_step),
        class_name="invoice",
    )