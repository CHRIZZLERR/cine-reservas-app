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


def booking_page() -> rx.Component:
    return rx.box(
        navbar("boletos"),
        rx.grid(
            rx.box(
                rx.hstack(
                    rx.box("1", class_name=rx.cond(State.booking_step == 1, "step step-active", "step")),
                    rx.box("2", class_name=rx.cond(State.booking_step == 2, "step step-active", "step")),
                    rx.box("3", class_name=rx.cond(State.booking_step == 3, "step step-active", "step")),
                    rx.box("4", class_name=rx.cond(State.booking_step == 4, "step step-active", "step")),
                    spacing="2", class_name="steps",
                ),
                rx.cond(State.booking_step == 1, seat_map(), rx.cond(State.booking_step == 2, food_section(), rx.cond(State.booking_step == 3, customer_form(), confirmation()))),
                class_name="booking-main",
            ),
            invoice(),
            columns="2", spacing="4", class_name="booking-layout",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )