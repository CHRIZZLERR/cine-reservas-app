import reflex as rx  # type: ignore[import]

try:
    from state import State
except ModuleNotFoundError:
    from ..state import State


LOCATIONS = [
    "Downtown Center",
    "Galería 360",
    "Ágora Mall",
    "Blue Mall",
    "Sambil",
]


def loc_button(loc: str) -> rx.Component:
    return rx.button(
        loc,
        class_name=rx.cond(
            State.selected_location == loc,
            "pill pill-active",
            "pill",
        ),
        on_click=lambda: State.set_location(loc),
    )


def date_button(date: str) -> rx.Component:
    return rx.button(
        date,
        class_name=rx.cond(
            State.selected_date == date,
            "pill pill-active",
            "pill",
        ),
        on_click=lambda: State.set_date(date),
    )


def showtime_button(time: str) -> rx.Component:
    return rx.button(
        time,
        class_name=rx.cond(
            State.selected_showtime == time,
            "showtime showtime-active",
            "showtime",
        ),
        on_click=lambda: State.set_showtime(time),
    )


def empty_schedule_card(message: str) -> rx.Component:
    return rx.box(
        rx.text("Sin funciones disponibles", class_name="schedule-empty-title"),
        rx.text(message, class_name="schedule-empty-text"),
        class_name="schedule-empty-card",
    )


def showtimes_section() -> rx.Component:
    return rx.box(
        rx.text("FUNCIONES", class_name="section-kicker"),
        rx.heading("Elige cine, fecha y horario", class_name="section-title"),
        rx.text(
            "Selecciona una función para continuar al mapa de asientos.",
            class_name="muted",
        ),

        rx.text("Ubicación", class_name="block-label"),
        rx.hstack(
            rx.foreach(LOCATIONS, loc_button),
            spacing="2",
            wrap="wrap",
            class_name="schedule-options-row",
        ),

        rx.text("Fecha", class_name="block-label"),
        rx.cond(
            State.available_dates.length() > 0,
            rx.hstack(
                rx.foreach(State.available_dates, date_button),
                spacing="2",
                wrap="wrap",
                class_name="schedule-options-row",
            ),
            empty_schedule_card(
                "Esta sucursal todavía no tiene fechas disponibles para esta película."
            ),
        ),

        rx.text("Horarios disponibles", class_name="block-label"),
        rx.cond(
            State.showtimes.length() > 0,
            rx.vstack(
                rx.hstack(
                    rx.foreach(State.showtimes, showtime_button),
                    spacing="2",
                    wrap="wrap",
                    class_name="schedule-options-row",
                ),
                rx.cond(
                    State.selected_funcion_id > 0,
                    rx.button(
                        "Continuar a asientos",
                        class_name="btn-primary-lg schedule-continue-btn",
                        on_click=State.start_booking,
                    ),
                    rx.text(
                        "Elige un horario para continuar.",
                        class_name="schedule-helper-text",
                    ),
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            empty_schedule_card(
                "No hay horarios disponibles para esta fecha o sucursal."
            ),
        ),

        class_name="page-section showtimes-card",
    )
