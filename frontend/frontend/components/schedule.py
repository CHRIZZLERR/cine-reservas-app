import reflex as rx  # type: ignore[import]

try:
    from state import State
    from data import LOCATIONS
except ModuleNotFoundError:
    from ..state import State
    from ..data import LOCATIONS


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


def showtime_button(funcion: dict) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.text(funcion["hora"]),
            rx.text("•"),
            rx.text(funcion["sala"]),
            spacing="1",
            align="center",
        ),
        class_name=rx.cond(
            State.selected_funcion_id == funcion["id"],
            "showtime showtime-active",
            "showtime",
        ),
        on_click=lambda: State.set_showtime(
            funcion["id"],
            funcion["hora"],
            funcion["fecha"],
            funcion["precio"],
        ),
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
        ),

        rx.text("Fecha", class_name="block-label"),
        rx.cond(
            State.available_dates.length() > 0,
            rx.hstack(
                rx.foreach(State.available_dates, date_button),
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "No hay fechas disponibles para esta película en esta ubicación.",
                class_name="muted",
            ),
        ),

        rx.text("Horarios disponibles", class_name="block-label"),
        rx.cond(
            State.showtimes.length() > 0,
            rx.hstack(
                rx.foreach(State.showtimes, showtime_button),
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "No hay funciones disponibles para esta película en esta fecha.",
                class_name="muted",
            ),
        ),

        rx.cond(
            State.api_message != "",
            rx.text(State.api_message, class_name="auth-message"),
            rx.fragment(),
        ),

        rx.button(
            "Continuar a asientos",
            class_name="btn-primary-lg",
            on_click=State.start_booking,
        ),

        class_name="page-section showtimes-card",
    )