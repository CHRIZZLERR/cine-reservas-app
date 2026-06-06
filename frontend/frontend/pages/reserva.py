import reflex as rx  # type: ignore[import]

try:
    from state import State
    from components.seat_map import seat_map
    from components.food_menu import food_section
    from components.booking_summary import invoice, customer_form, confirmation
    from components.navbar import navbar, search_overlay, side_menu
except ModuleNotFoundError:
    from ..state import State
    from ..components.seat_map import seat_map
    from ..components.food_menu import food_section
    from ..components.booking_summary import invoice, customer_form, confirmation
    from ..components.navbar import navbar, search_overlay, side_menu


def step_item(number: int, title: str) -> rx.Component:
    return rx.box(
        rx.box(
            str(number),
            class_name=rx.cond(State.booking_step == number, "step-bubble step-active", "step-bubble"),
        ),
        rx.text(title, class_name=rx.cond(State.booking_step == number, "step-title step-title-active", "step-title")),
        class_name="checkout-step",
    )


def booking_content() -> rx.Component:
    return rx.cond(
        State.booking_step == 1,
        seat_map(),
        rx.cond(
            State.booking_step == 2,
            food_section(),
            rx.cond(
                State.booking_step == 3,
                customer_form(),
                confirmation(),
            ),
        ),
    )


def booking_page() -> rx.Component:
    return rx.box(
        navbar("boletos"),
        rx.box(
            rx.text("COMPRA DE BOLETOS", class_name="section-kicker"),
            rx.heading("Finaliza tu reserva", class_name="page-title"),
            rx.text(
                "Selecciona tus asientos, agrega dulcería y genera tu ticket con código QR.",
                class_name="checkout-subtitle",
            ),
            rx.hstack(
                step_item(1, "Asientos"),
                step_item(2, "Dulcería"),
                step_item(3, "Datos"),
                step_item(4, "Ticket"),
                spacing="3",
                class_name="checkout-steps",
            ),
            class_name="checkout-hero",
        ),
        rx.cond(
            State.booking_step == 4,
            rx.box(
                confirmation(),
                class_name="booking-layout booking-layout-confirm",
            ),
            rx.grid(
                rx.box(
                    booking_content(),
                    class_name="booking-main checkout-main",
                ),
                invoice(),
                columns="2",
                spacing="4",
                class_name="booking-layout",
            ),
        ),
        search_overlay(),
        side_menu(),
        class_name="page checkout-page",
    )