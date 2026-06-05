import reflex as rx  # type: ignore[import]

try:
    from state import State
    from data import LOCATIONS, DATES
    from config import APP_NAME, APP_BRAND_MARK, APP_BRAND_SUB
except ModuleNotFoundError:
    from ..state import State
    from ..data import LOCATIONS, DATES
    from ..config import APP_NAME, APP_BRAND_MARK, APP_BRAND_SUB


def _loc_button(loc: str) -> rx.Component:
    return rx.button(loc, class_name=rx.cond(State.selected_location == loc, "pill pill-active", "pill"), on_click=lambda: State.set_location(loc))

def _date_button(date: str) -> rx.Component:
    return rx.button(date, class_name=rx.cond(State.selected_date == date, "pill pill-active", "pill"), on_click=lambda: State.set_date(date))

def _showtime_button(t: str) -> rx.Component:
    return rx.button(t, class_name=rx.cond(State.selected_showtime == t, "showtime showtime-active", "showtime"), on_click=lambda: State.set_showtime(t))

def _showtimes_section() -> rx.Component:
    return rx.box(
        rx.text("FUNCIONES", class_name="section-kicker"),
        rx.heading("Elige cine, fecha y horario", class_name="section-title"),
        rx.text("Selecciona una función para continuar al mapa de asientos.", class_name="muted"),
        rx.text("Ubicación", class_name="block-label"),
        rx.hstack(rx.foreach(LOCATIONS, _loc_button), spacing="2", wrap="wrap"),
        rx.text("Fecha", class_name="block-label"),
        rx.hstack(rx.foreach(DATES, _date_button), spacing="2", wrap="wrap"),
        rx.text("Horarios disponibles", class_name="block-label"),
        rx.hstack(rx.foreach(State.showtimes, _showtime_button), spacing="2", wrap="wrap"),
        rx.button("Continuar a asientos", class_name="btn-primary-lg", on_click=State.start_booking),
        class_name="page-section showtimes-card",
    )

def _navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(rx.hstack(rx.box(APP_BRAND_MARK, class_name="brand-mark"), rx.vstack(rx.text(APP_NAME.upper(), class_name="brand-title"), rx.text(APP_BRAND_SUB, class_name="brand-sub"), spacing="0", align="start"), spacing="3", align="center"), href="/", text_decoration="none"),
            rx.spacer(),
            rx.hstack(rx.button("⌕", class_name="nav-icon", on_click=State.toggle_search), rx.button("☰", class_name="nav-icon", on_click=State.toggle_menu), spacing="3"),
            align="center", width="100%",
        ),
        class_name="navbar",
    )

def _search_overlay() -> rx.Component:
    return rx.cond(
        State.show_search,
        rx.box(rx.box(rx.hstack(rx.input(placeholder="Buscar película, género o clasificación...", value=State.search_text, on_change=State.set_search_text, class_name="search-input-big"), rx.link(rx.button("Ver cartelera", class_name="btn-primary-sm"), href="/cartelera"), rx.button("✕", class_name="close-btn", on_click=State.close_search), spacing="3", width="100%"), class_name="search-panel"), class_name="overlay"),
        rx.fragment(),
    )

def _side_menu() -> rx.Component:
    return rx.cond(
        State.show_menu,
        rx.box(
            rx.box(class_name="menu-backdrop", on_click=State.close_menu),
            rx.vstack(
                rx.hstack(rx.heading(APP_NAME.upper(), class_name="drawer-logo"), rx.spacer(), rx.button("✕", class_name="close-btn", on_click=State.close_menu), width="100%"),
                rx.input(placeholder="Buscar película...", value=State.search_text, on_change=State.set_search_text, class_name="drawer-search"),
                rx.link("Inicio", href="/", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Cartelera", href="/cartelera", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Próximamente", href="/proximamente", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Ubicaciones", href="/ubicaciones", class_name="drawer-link", on_click=State.close_menu),
                rx.link("Comprar boletos", href="/reservar", class_name="drawer-link", on_click=State.close_menu),
                rx.box(rx.text("Cines disponibles", class_name="drawer-kicker"), rx.foreach(LOCATIONS, lambda loc: rx.text(loc, class_name="drawer-small")), class_name="drawer-card"),
                spacing="4", align="start", class_name="drawer",
            ),
            class_name="drawer-wrapper",
        ),
        rx.fragment(),
    )

def detail_page() -> rx.Component:
    return rx.box(
        _navbar(),
        rx.box(
            rx.image(src=State.current_movie["image"], class_name="detail-bg"),
            rx.box(class_name="detail-overlay"),
            rx.grid(
                rx.box(rx.image(src=State.current_movie["poster"], class_name="detail-poster"), class_name="detail-poster-wrap"),
                rx.vstack(
                    rx.text(State.current_movie["fecha_estreno"], class_name="section-kicker"),
                    rx.heading(State.current_movie["titulo"], class_name="detail-title"),
                    rx.hstack(rx.text(State.current_movie["genero"], class_name="detail-chip"), rx.text(State.current_movie["clasificacion"], class_name="detail-chip"), rx.text(State.current_movie["duracion"], class_name="detail-chip"), spacing="2", wrap="wrap"),
                    rx.text(State.current_movie["sinopsis"], class_name="detail-desc"),
                    rx.hstack(rx.text("Director:", class_name="detail-label"), rx.text(State.current_movie["director"], class_name="detail-value")),
                    rx.hstack(rx.text("Reparto:", class_name="detail-label"), rx.text(State.current_movie["reparto"], class_name="detail-value")),
                    rx.hstack(rx.button("Ver trailer", class_name="btn-primary-sm", on_click=State.open_trailer), rx.button("Ocultar trailer", class_name="btn-ghost", on_click=State.close_trailer), spacing="2"),
                    rx.cond(
                        State.show_trailer,
                        rx.box(rx.el.iframe(src=State.trailer_url, class_name="trailer-frame", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", allowfullscreen=True), class_name="trailer-box"),
                        rx.box(rx.image(src=State.current_movie["image"], class_name="trailer-placeholder-img"), rx.box("Presiona \"Ver trailer\" para cargar el video aquí mismo.", class_name="trailer-placeholder-text"), class_name="trailer-placeholder"),
                    ),
                    spacing="3", align="start", class_name="detail-info",
                ),
                columns="2", spacing="6", class_name="detail-grid",
            ),
            class_name="detail-hero",
        ),
        _showtimes_section(),
        _search_overlay(),
        _side_menu(),
        class_name="page",
    )