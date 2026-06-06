import reflex as rx  # type: ignore[import]

try:
    from state import State
except ModuleNotFoundError:
    from ..state import State


def seat_button(seat: dict) -> rx.Component:
    return rx.button(
        seat["id"],
        title=seat["id"],
        class_name=rx.cond(
            State.selected_seats.contains(seat["id"]),
            "seat seat-selected",
            rx.cond(
                seat["estado"] == "reservado",
                "seat seat-reserved",
                rx.cond(seat["tipo"] == "vip", "seat seat-vip", "seat"),
            ),
        ),
        on_click=lambda: State.toggle_seat(seat["id"]),
    )


def seat_row(label: str, seats_var) -> rx.Component:
    return rx.hstack(
        rx.text(label, class_name="row-label"),
        rx.foreach(seats_var, seat_button),
        spacing="1",
        class_name="seat-row",
    )


def seat_map() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("🎟️", class_name="section-icon"),
            rx.vstack(
                rx.text("SELECCIÓN DE ASIENTOS", class_name="block-label"),
                rx.text("Elige hasta 8 asientos disponibles para esta función.", class_name="form-subtitle"),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="form-header",
        ),
        rx.box(
            rx.text("PANTALLA", class_name="screen-label"),
            rx.box(class_name="screen"),
            rx.vstack(
                seat_row("A", State.row_A),
                seat_row("B", State.row_B),
                seat_row("C", State.row_C),
                seat_row("D", State.row_D),
                seat_row("E", State.row_E),
                seat_row("F", State.row_F),
                seat_row("G", State.row_G),
                seat_row("H", State.row_H),
                seat_row("I", State.row_I),
                seat_row("J", State.row_J),
                seat_row("K", State.row_K),
                seat_row("L", State.row_L),
                spacing="2",
                class_name="seat-map",
            ),
            class_name="seat-theater",
        ),
        rx.hstack(
            rx.hstack(rx.box(class_name="legend-dot dot-available"), rx.text("Disponible", class_name="legend-text")),
            rx.hstack(rx.box(class_name="legend-dot dot-selected"), rx.text("Seleccionado", class_name="legend-text")),
            rx.hstack(rx.box(class_name="legend-dot dot-reserved"), rx.text("Reservado", class_name="legend-text")),
            rx.hstack(rx.box(class_name="legend-dot dot-vip"), rx.text("VIP", class_name="legend-text")),
            spacing="4",
            wrap="wrap",
            class_name="legend",
        ),
        class_name="seat-card checkout-section-card",
    )