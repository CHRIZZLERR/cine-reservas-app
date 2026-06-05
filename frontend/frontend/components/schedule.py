import reflex as rx  # type: ignore[import]

try:
    from state import State
    from data import LOCATIONS, DATES
except ModuleNotFoundError:
    from ..state import State
    from ..data import LOCATIONS, DATES


def loc_button(loc: str) -> rx.Component:
    return rx.button(loc, class_name=rx.cond(State.selected_location == loc, "pill pill-active", "pill"), on_click=lambda: State.set_location(loc))

def date_button(date: str) -> rx.Component:
    return rx.button(date, class_name=rx.cond(State.selected_date == date, "pill pill-active", "pill"), on_click=lambda: State.set_date(date))

def showtime_button(t: str) -> rx.Component:
    return rx.button(t, class_name=rx.cond(State.selected_showtime == t, "showtime showtime-active", "showtime"), on_click=lambda: State.set_showtime(t))

def showtimes_section() -> rx.Component:
    return rx.box(
        rx.text("FUNCIONES", class_name="section-kicker"),
        rx.heading("Elige cine, fecha y horario", class_name="section-title"),
        rx.text("Selecciona una función para continuar al mapa de asientos.", class_name="muted"),
        rx.text("Ubicación", class_name="block-label"),
        rx.hstack(rx.foreach(LOCATIONS, loc_button), spacing="2", wrap="wrap"),
        rx.text("Fecha", class_name="block-label"),
        rx.hstack(rx.foreach(DATES, date_button), spacing="2", wrap="wrap"),
        rx.text("Horarios disponibles", class_name="block-label"),
        rx.hstack(rx.foreach(State.showtimes, showtime_button), spacing="2", wrap="wrap"),
        rx.button("Continuar a asientos", class_name="btn-primary-lg", on_click=State.start_booking),
        class_name="page-section showtimes-card",
    )