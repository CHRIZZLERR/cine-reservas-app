import reflex as rx  # type: ignore[import]

try:
    from state import State
except ModuleNotFoundError:
    from ..state import State


def money(value) -> rx.Component:
    return rx.hstack(
        rx.text("RD$", class_name="money"),
        rx.text(value, class_name="money"),
        spacing="0",
        align="center",
    )


def food_card(item: dict) -> rx.Component:
    return rx.box(
        rx.image(src=item["image"], class_name="food-img"),
        rx.box(
            rx.heading(item["nombre"], class_name="food-title"),
            rx.text(item["descripcion"], class_name="food-desc"),
            money(item["precio"]),
            class_name="food-info",
        ),
        rx.hstack(
            rx.button("−", class_name="qty-btn", on_click=lambda: State.remove_food(item["id"])),
            rx.text(item["qty"], class_name="qty-text"),
            rx.button("+", class_name="qty-btn", on_click=lambda: State.add_food(item["id"])),
            spacing="2",
            align="center",
            class_name="qty-control",
        ),
        class_name="food-card",
    )


def food_section() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("🍿", class_name="section-icon"),
            rx.vstack(
                rx.text("DULCERÍA", class_name="block-label"),
                rx.text("Agrega tus combos favoritos a la reserva.", class_name="form-subtitle"),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="form-header",
        ),
        rx.grid(
            rx.foreach(State.food_cart, food_card),
            columns="2",
            spacing="3",
            width="100%",
        ),
        class_name="food-section checkout-section-card",
    )