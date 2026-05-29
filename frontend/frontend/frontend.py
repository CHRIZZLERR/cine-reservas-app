import reflex as rx

GFONT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Rajdhani:wght@400;500;600;700&"
    "family=Anton&display=swap"
)

MOVIES = [
    {
        "id": 1,
        "titulo": "Detective Pikachu",
        "genero": "Acción / Aventura / Comedia",
        "clasificacion": "12+",
        "duracion": "1h 45min",
        "estado": "Cartelera",
        "fecha_estreno": "En cartelera",
        "director": "Rob Letterman",
        "precio": 500,
        "rating": "6.8",
        "poster": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?q=80&w=800",
        "banner": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1f?q=80&w=1800",
        "resumen": "En un mundo donde las personas conviven con criaturas extraordinarias, un joven descubre una pista que cambia su destino.",
    },
    {
        "id": 2,
        "titulo": "Mortal Kombat II",
        "genero": "Acción / Fantasía",
        "clasificacion": "R/14",
        "duracion": "1h 55min",
        "estado": "Cartelera",
        "fecha_estreno": "En cartelera",
        "director": "Simon McQuoid",
        "precio": 500,
        "rating": "7.4",
        "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800",
        "banner": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?q=80&w=1800",
        "resumen": "Una batalla brutal entre reinos amenaza con decidir el destino de la humanidad.",
    },
    {
        "id": 3,
        "titulo": "Tron: Ares",
        "genero": "Ciencia ficción / Acción",
        "clasificacion": "PG-13",
        "duracion": "1h 59min",
        "estado": "Próximamente",
        "fecha_estreno": "10 octubre 2026",
        "director": "Joachim Rønning",
        "precio": 525,
        "rating": "7.8",
        "poster": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?q=80&w=800",
        "banner": "https://images.unsplash.com/photo-1535223289827-42f1e9919769?q=80&w=1800",
        "resumen": "La frontera entre el mundo digital y el real desaparece en una guerra visual futurista.",
    },
    {
        "id": 4,
        "titulo": "El Heladero",
        "genero": "Thriller / Terror",
        "clasificacion": "R/16",
        "duracion": "1h 26min",
        "estado": "Próximamente",
        "fecha_estreno": "3 septiembre 2026",
        "director": "Eli Roth",
        "precio": 475,
        "rating": "7.0",
        "poster": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?q=80&w=800",
        "banner": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=1800",
        "resumen": "Un pueblo tranquilo cae en terror cuando un heladero empieza a servir algo más que dulces.",
    },
    {
        "id": 5,
        "titulo": "Black Phone 2",
        "genero": "Horror / Thriller",
        "clasificacion": "R/16",
        "duracion": "1h 54min",
        "estado": "Próximamente",
        "fecha_estreno": "17 octubre 2026",
        "director": "Scott Derrickson",
        "precio": 500,
        "rating": "7.5",
        "poster": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=800",
        "banner": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?q=80&w=1800",
        "resumen": "El teléfono vuelve a sonar, trayendo voces del pasado y una amenaza más oscura.",
    },
]

FOODS = [
    {"id": 1, "nombre": "Combo Clásico", "detalle": "Palomitas grandes + refresco", "precio": 350},
    {"id": 2, "nombre": "Nachos Premium", "detalle": "Nachos con queso y salsa", "precio": 280},
    {"id": 3, "nombre": "Hot Dog", "detalle": "Hot dog grande estilo cine", "precio": 220},
    {"id": 4, "nombre": "Refresco Grande", "detalle": "Bebida fría 22oz", "precio": 150},
]

LOCATIONS = ["Downtown Center", "Galería 360", "Sambil", "Megaplex 10", "Coral Mall"]
TIMES = ["3:25 PM", "6:30 PM", "8:40 PM", "10:15 PM"]


class State(rx.State):
    selected_movie_id: int = 1
    hero_movie_id: int = 1
    selected_location: str = "Downtown Center"
    selected_time: str = "6:30 PM"
    selected_day: str = "Hoy"
    selected_seats: list[str] = []
    food_cart: list[dict] = []
    search_text: str = ""
    show_checkout: bool = False
    show_search: bool = False
    show_menu: bool = False
    reserved_seats: list[str] = ["A4", "B7", "C5", "D9", "E2", "F10", "G6"]

    def set_search_text(self, value: str):
        self.search_text = value

    def toggle_search(self):
        self.show_search = not self.show_search

    def close_search(self):
        self.show_search = False

    def toggle_menu(self):
        self.show_menu = not self.show_menu

    def close_menu(self):
        self.show_menu = False

    @rx.var
    def selected_movie(self) -> dict:
        for movie in MOVIES:
            if movie["id"] == self.selected_movie_id:
                return movie
        return MOVIES[0]

    @rx.var
    def hero_movie(self) -> dict:
        for movie in MOVIES:
            if movie["id"] == self.hero_movie_id:
                return movie
        return MOVIES[0]

    @rx.var
    def movies_showing(self) -> list[dict]:
        return [m for m in MOVIES if m["estado"] == "Cartelera"]

    @rx.var
    def movies_coming(self) -> list[dict]:
        return [m for m in MOVIES if m["estado"] == "Próximamente"]

    @rx.var
    def ticket_subtotal(self) -> int:
        return len(self.selected_seats) * self.selected_movie["precio"]

    @rx.var
    def food_subtotal(self) -> int:
        total = 0
        for item in self.food_cart:
            total += item["precio"]
        return total

    @rx.var
    def service_fee(self) -> int:
        if len(self.selected_seats) == 0:
            return 0
        return 45 * len(self.selected_seats)

    @rx.var
    def subtotal(self) -> int:
        return self.ticket_subtotal + self.food_subtotal

    @rx.var
    def tax(self) -> int:
        return int(self.subtotal * 0.18)

    @rx.var
    def total(self) -> int:
        return self.subtotal + self.tax + self.service_fee

    def select_movie(self, movie_id: int):
        self.selected_movie_id = movie_id
        self.hero_movie_id = movie_id
        self.selected_seats = []
        self.food_cart = []
        self.show_checkout = False

    def select_hero_movie(self, movie_id: int):
        self.select_movie(movie_id)

    def next_hero_movie(self):
        ids = [movie["id"] for movie in MOVIES]
        current_index = ids.index(self.hero_movie_id)
        next_index = (current_index + 1) % len(ids)
        self.hero_movie_id = ids[next_index]
        self.selected_movie_id = ids[next_index]

    def prev_hero_movie(self):
        ids = [movie["id"] for movie in MOVIES]
        current_index = ids.index(self.hero_movie_id)
        prev_index = (current_index - 1) % len(ids)
        self.hero_movie_id = ids[prev_index]
        self.selected_movie_id = ids[prev_index]

    def set_location(self, value: str):
        self.selected_location = value

    def set_time(self, value: str):
        self.selected_time = value

    def toggle_seat(self, seat: str):
        if seat in self.reserved_seats:
            return
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            self.selected_seats.append(seat)

    def add_food(self, food_id: int):
        for food in FOODS:
            if food["id"] == food_id:
                self.food_cart.append(food)

    def remove_food(self, index: int):
        self.food_cart.pop(index)

    def clear_cart(self):
        self.selected_seats = []
        self.food_cart = []
        self.show_checkout = False

    def go_checkout(self):
        self.show_checkout = True

    def close_checkout(self):
        self.show_checkout = False


def page_style():
    return rx.el.style(
        f"""
        @import url('{GFONT_URL}');
        html {{ scroll-behavior: smooth; }}
        body {{ margin: 0; background: #020617; }}
        """
    )


def money_text(value, class_name="cart-text"):
    return rx.hstack(
        rx.text("RD$", class_name=class_name),
        rx.text(value, class_name=class_name),
        rx.text(".00", class_name=class_name),
        spacing="0",
        align="center",
    )


def label_value_row(label, value, value_class="cart-text"):
    return rx.hstack(
        rx.text(label, class_name="cart-text"),
        rx.spacer(),
        money_text(value, value_class),
        width="100%",
    )


def navbar():
    return rx.hstack(
        rx.hstack(
            rx.box("C", class_name="cinemax-mark"),
            rx.vstack(
                rx.heading("CINEMAX", class_name="cinemax-logo"),
                rx.text("CINE PREMIUM", class_name="cinemax-subtitle"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Cines", href="#cines", class_name="cinemax-nav-link"),
            rx.link("Cartelera", href="#cartelera", class_name="cinemax-nav-link"),
            rx.link("Próximamente", href="#proximamente", class_name="cinemax-nav-link"),
            rx.link("Boletos", href="#boletos", class_name="cinemax-nav-link"),
            rx.link("Comida", href="#comida", class_name="cinemax-nav-link"),
            spacing="5",
            class_name="cinemax-nav-menu",
        ),
        rx.hstack(
            rx.button("🔍", class_name="nav-icon-btn", on_click=State.toggle_search),
            rx.button("☰", class_name="nav-icon-btn", on_click=State.toggle_menu),
            spacing="3",
        ),
        align="center",
        width="100%",
        class_name="cinemax-navbar",
    )


def hero_thumb(movie):
    return rx.box(
        rx.image(src=movie["poster"], class_name="hero-thumb-img"),
        rx.text(movie["titulo"], class_name="hero-thumb-title"),
        class_name=rx.cond(
            State.hero_movie_id == movie["id"],
            "hero-thumb active-thumb",
            "hero-thumb",
        ),
        on_click=lambda: State.select_hero_movie(movie["id"]),
    )


def hero():
    return rx.box(
        rx.box(
            rx.image(src=State.hero_movie["banner"], class_name="cinema-hero-bg"),
            rx.box(class_name="cinema-hero-layer"),
            navbar(),
            rx.grid(
                rx.vstack(
                    rx.badge("new", class_name="hero-new-badge"),
                    rx.heading(State.hero_movie["titulo"], class_name="cinema-hero-title"),
                    rx.text(State.hero_movie["resumen"], class_name="cinema-hero-desc"),
                    rx.hstack(
                        rx.text("Genres:", class_name="genre-label"),
                        rx.text(State.hero_movie["genero"], class_name="genre-text"),
                        rx.text(State.hero_movie["clasificacion"], class_name="age-chip"),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.hstack(
                        rx.text("★", class_name="rating-star"),
                        rx.text(State.hero_movie["rating"], class_name="rating-number"),
                        rx.text("/10", class_name="rating-muted"),
                        spacing="1",
                        align="center",
                    ),
                    rx.link(rx.button("Comprar ahora", class_name="watch-now-btn"), href="#boletos"),
                    align="start",
                    spacing="3",
                    class_name="cinema-hero-info",
                ),
                rx.box(
                    rx.hstack(rx.foreach(MOVIES, hero_thumb), spacing="4", class_name="hero-thumbs"),
                    rx.hstack(
                        rx.button("‹", class_name="carousel-arrow", on_click=State.prev_hero_movie),
                        rx.button("›", class_name="carousel-arrow", on_click=State.next_hero_movie),
                        spacing="3",
                        class_name="carousel-controls",
                    ),
                    class_name="cinema-hero-right",
                ),
                columns="2",
                spacing="0",
                class_name="cinema-hero-grid",
            ),
            class_name="cinema-hero-card",
        ),
        id="inicio",
        class_name="cinema-hero-wrapper",
    )


def search_overlay():
    return rx.cond(
        State.show_search,
        rx.box(
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="Buscar película, género o clasificación...",
                        value=State.search_text,
                        on_change=State.set_search_text,
                        class_name="nav-search-input",
                    ),
                    rx.button("Buscar", class_name="nav-search-btn"),
                    rx.button("✕", class_name="nav-close-btn", on_click=State.close_search),
                    spacing="3",
                    width="100%",
                ),
                class_name="nav-search-box",
            ),
            class_name="nav-search-overlay",
        ),
        rx.fragment(),
    )


def side_menu():
    return rx.cond(
        State.show_menu,
        rx.box(
            rx.box(class_name="menu-backdrop", on_click=State.close_menu),
            rx.vstack(
                rx.hstack(
                    rx.heading("CINEMAX", class_name="side-menu-logo"),
                    rx.spacer(),
                    rx.button("✕", class_name="nav-close-btn", on_click=State.close_menu),
                    width="100%",
                ),
                rx.link("Inicio", href="#inicio", class_name="side-menu-link", on_click=State.close_menu),
                rx.link("Cines", href="#cines", class_name="side-menu-link", on_click=State.close_menu),
                rx.link("Cartelera", href="#cartelera", class_name="side-menu-link", on_click=State.close_menu),
                rx.link("Próximamente", href="#proximamente", class_name="side-menu-link", on_click=State.close_menu),
                rx.link("Comprar boletos", href="#boletos", class_name="side-menu-link", on_click=State.close_menu),
                rx.link("Comida y bebida", href="#comida", class_name="side-menu-link", on_click=State.close_menu),
                rx.box(
                    rx.text("Cines disponibles", class_name="side-menu-title"),
                    rx.text("Downtown Center", class_name="side-menu-small"),
                    rx.text("Galería 360", class_name="side-menu-small"),
                    rx.text("Sambil", class_name="side-menu-small"),
                    rx.text("Megaplex 10", class_name="side-menu-small"),
                    class_name="side-menu-section",
                ),
                spacing="5",
                align="start",
                class_name="side-menu-panel",
            ),
            class_name="side-menu-wrapper",
        ),
        rx.fragment(),
    )


def subdivisions():
    return rx.box(
        rx.grid(
            rx.link(rx.box(rx.text("🎬", class_name="sub-icon"), rx.heading("Cartelera", class_name="sub-title"), rx.text("Películas disponibles hoy", class_name="sub-text"), class_name="sub-card"), href="#cartelera"),
            rx.link(rx.box(rx.text("📍", class_name="sub-icon"), rx.heading("Cines", class_name="sub-title"), rx.text("Elige tu sucursal favorita", class_name="sub-text"), class_name="sub-card"), href="#cines"),
            rx.link(rx.box(rx.text("🎟️", class_name="sub-icon"), rx.heading("Boletos", class_name="sub-title"), rx.text("Compra y revisa tu factura", class_name="sub-text"), class_name="sub-card"), href="#boletos"),
            rx.link(rx.box(rx.text("🍿", class_name="sub-icon"), rx.heading("Comida", class_name="sub-title"), rx.text("Combos y bebidas", class_name="sub-text"), class_name="sub-card"), href="#comida"),
            columns="4",
            spacing="5",
            width="100%",
        ),
        class_name="subdivisions",
    )


def section_cines():
    return rx.box(
        rx.text("LOCATIONS", class_name="section-kicker"),
        rx.heading("Nuestros cines", class_name="section-title"),
        rx.grid(
            *[
                rx.box(
                    rx.text("📍", font_size="34px"),
                    rx.heading(location, class_name="coming-title"),
                    rx.text("Salas premium · CXC · IMAX · 4K", class_name="muted"),
                    rx.button("Ver funciones", class_name="outline-btn", width="100%"),
                    class_name="coming-card coming-info",
                )
                for location in LOCATIONS
            ],
            columns="3",
            spacing="6",
            width="100%",
        ),
        id="cines",
        class_name="section",
    )


def movie_card(movie):
    return rx.box(
        rx.box(rx.image(src=movie["poster"], class_name="movie-poster"), rx.badge(movie["estado"], class_name="movie-status"), class_name="poster-wrap"),
        rx.vstack(
            rx.heading(movie["titulo"], class_name="movie-title"),
            rx.text(movie["genero"], class_name="muted"),
            rx.hstack(rx.text(movie["clasificacion"], class_name="chip"), rx.text(movie["duracion"], class_name="chip"), spacing="2"),
            rx.text(movie["resumen"], class_name="movie-desc"),
            rx.button("Ver detalles y comprar", class_name="card-btn", width="100%", on_click=lambda: State.select_movie(movie["id"])),
            spacing="3",
            align="start",
            class_name="movie-info",
        ),
        class_name="movie-card",
    )


def section_showing():
    return rx.box(
        rx.hstack(
            rx.vstack(rx.text("NOW SHOWING", class_name="section-kicker"), rx.heading("Películas en cartelera", class_name="section-title"), spacing="1", align="start"),
            rx.spacer(),
            rx.link("Ver todo →", href="#boletos", class_name="view-all"),
        ),
        rx.grid(rx.foreach(State.movies_showing, movie_card), columns="3", spacing="6", width="100%"),
        id="cartelera",
        class_name="section",
    )


def coming_card(movie):
    return rx.box(
        rx.image(src=movie["poster"], class_name="coming-img"),
        rx.vstack(rx.badge(movie["fecha_estreno"], class_name="date-badge"), rx.heading(movie["titulo"], class_name="coming-title"), rx.text(movie["genero"], class_name="muted"), rx.text(movie["resumen"], class_name="movie-desc"), rx.button("Recordarme estreno", class_name="outline-btn", width="100%"), align="start", spacing="3", class_name="coming-info"),
        class_name="coming-card",
    )


def section_coming():
    return rx.box(rx.text("COMING SOON", class_name="section-kicker"), rx.heading("Próximamente", class_name="section-title"), rx.grid(rx.foreach(State.movies_coming, coming_card), columns="3", spacing="6", width="100%"), id="proximamente", class_name="section")


def movie_detail():
    return rx.box(
        rx.image(src=State.selected_movie["banner"], class_name="detail-bg-img"),
        rx.box(class_name="detail-dark-layer"),
        rx.grid(
            rx.box(rx.image(src=State.selected_movie["poster"], class_name="detail-poster"), class_name="detail-poster-wrap"),
            rx.vstack(
                rx.badge(State.selected_movie["estado"], class_name="hero-badge"),
                rx.heading(State.selected_movie["titulo"], class_name="detail-title"),
                rx.hstack(rx.text(State.selected_movie["fecha_estreno"], class_name="detail-chip"), rx.text(State.selected_movie["genero"], class_name="detail-chip"), rx.text(State.selected_movie["duracion"], class_name="detail-chip"), rx.text(State.selected_movie["clasificacion"], class_name="detail-chip"), spacing="2", wrap="wrap"),
                rx.text("Resumen", class_name="detail-label"),
                rx.text(State.selected_movie["resumen"], class_name="detail-text"),
                rx.text("Director", class_name="detail-label"),
                rx.text(State.selected_movie["director"], class_name="detail-text"),
                rx.link(rx.button("Comprar boletos", class_name="primary-btn"), href="#boletos"),
                spacing="4",
                align="start",
            ),
            columns="2",
            spacing="8",
            class_name="detail-content",
        ),
        class_name="movie-detail",
    )


def time_button(time):
    return rx.button(time, class_name=rx.cond(State.selected_time == time, "time-btn active-time", "time-btn"), on_click=lambda: State.set_time(time))


def seat_button(seat):
    return rx.button(seat, class_name=rx.cond(State.selected_seats.contains(seat), "seat selected-seat", rx.cond(State.reserved_seats.contains(seat), "seat reserved-seat", "seat available-seat")), on_click=lambda: State.toggle_seat(seat))


def seat_row(row_letter):
    seats = [f"{row_letter}{i}" for i in range(1, 13)]
    return rx.hstack(rx.foreach(seats, seat_button), spacing="2", class_name="seat-row")


def seats_map():
    rows = ["A", "B", "C", "D", "E", "F", "G"]
    return rx.box(
        rx.vstack(
            rx.text("SCREEN CXC", class_name="screen-text"),
            rx.box(class_name="screen"),
            rx.vstack(rx.foreach(rows, seat_row), spacing="3", class_name="seats-area"),
            rx.hstack(
                rx.hstack(rx.box(class_name="legend-dot available-dot"), rx.text("Disponible", class_name="legend-text")),
                rx.hstack(rx.box(class_name="legend-dot selected-dot"), rx.text("Seleccionado", class_name="legend-text")),
                rx.hstack(rx.box(class_name="legend-dot reserved-dot"), rx.text("Reservado", class_name="legend-text")),
                spacing="6",
                wrap="wrap",
                class_name="legend",
            ),
            spacing="4",
            align="center",
        ),
        class_name="seats-card",
    )


def food_card(food):
    return rx.box(rx.hstack(rx.box("🍿", class_name="food-icon"), rx.vstack(rx.heading(food["nombre"], class_name="food-title"), rx.text(food["detalle"], class_name="muted"), money_text(food["precio"], "food-price"), spacing="1", align="start"), rx.spacer(), rx.button("+", class_name="add-food-btn", on_click=lambda: State.add_food(food["id"])), align="center"), class_name="food-card")


def cart_food_item(item, index):
    return rx.hstack(rx.text(item["nombre"], class_name="cart-text"), rx.spacer(), money_text(item["precio"]), rx.button("x", class_name="mini-delete", on_click=lambda: State.remove_food(index)), width="100%")


def cart_sidebar():
    return rx.box(
        rx.vstack(
            rx.hstack(rx.text("🎟️", font_size="24px"), rx.heading("Factura", class_name="cart-title"), rx.spacer(), rx.text("Boletos seleccionados", class_name="cart-small"), width="100%"),
            rx.divider(border_color="rgba(255,255,255,.12)"),
            rx.hstack(rx.image(src=State.selected_movie["poster"], class_name="cart-poster"), rx.vstack(rx.heading(State.selected_movie["titulo"], class_name="cart-movie"), rx.hstack(rx.text(State.selected_day, class_name="cart-small"), rx.text("·", class_name="cart-small"), rx.text(State.selected_time, class_name="cart-small"), spacing="1"), rx.text(State.selected_location, class_name="cart-small"), spacing="1", align="start"), align="center"),
            rx.box(rx.text("Asientos", class_name="cart-label"), rx.cond(State.selected_seats.length() > 0, rx.text(State.selected_seats.to_string(), class_name="cart-text"), rx.text("No has seleccionado asientos", class_name="cart-muted")), width="100%"),
            rx.box(rx.text("Comida y bebida", class_name="cart-label"), rx.cond(State.food_cart.length() > 0, rx.vstack(rx.foreach(State.food_cart, cart_food_item), width="100%"), rx.text("Sin combos agregados", class_name="cart-muted")), width="100%"),
            rx.divider(border_color="rgba(255,255,255,.12)"),
            rx.vstack(label_value_row("Boletos", State.ticket_subtotal), label_value_row("Comida", State.food_subtotal), label_value_row("Cargo servicio", State.service_fee), label_value_row("ITBIS 18%", State.tax), rx.hstack(rx.text("Total", class_name="cart-total-label"), rx.spacer(), money_text(State.total, "cart-total"), width="100%"), width="100%", spacing="2"),
            rx.input(placeholder="Tarjeta regalo, cupón o código promocional", class_name="coupon-input"),
            rx.button("Siguiente: pago", class_name="checkout-btn", width="100%", on_click=State.go_checkout),
            rx.button("Limpiar carrito", class_name="clear-btn", width="100%", on_click=State.clear_cart),
            spacing="4",
            align="start",
        ),
        class_name="cart-sidebar",
    )


def booking_section():
    return rx.box(
        rx.text("BOOKING EXPERIENCE", class_name="section-kicker"),
        rx.heading("Compra de boletos", class_name="section-title"),
        rx.grid(
            rx.vstack(
                rx.box(rx.hstack(rx.select(LOCATIONS, value=State.selected_location, on_change=State.set_location, class_name="booking-select"), rx.spacer(), rx.text("Sala 2 · CXC", class_name="room-chip"), width="100%"), class_name="booking-top"),
                rx.box(rx.text("Horarios disponibles", class_name="block-title"), rx.hstack(rx.foreach(TIMES, time_button), spacing="3", wrap="wrap"), class_name="schedule-card"),
                seats_map(),
                rx.box(rx.text("Comida y bebida", class_name="block-title"), rx.grid(rx.foreach(FOODS, food_card), columns="2", spacing="4", width="100%"), id="comida", class_name="food-section"),
                spacing="5",
                align="stretch",
            ),
            cart_sidebar(),
            columns="2",
            spacing="6",
            width="100%",
        ),
        id="boletos",
        class_name="section booking-section",
    )


def checkout_modal():
    return rx.cond(
        State.show_checkout,
        rx.box(rx.box(rx.vstack(rx.heading("✅ Reserva generada", class_name="modal-title"), rx.text("Este es un demo de la página. Aquí conectarías el pago real o el backend.", class_name="modal-text"), rx.hstack(rx.text("Película:", class_name="modal-line"), rx.text(State.selected_movie["titulo"], class_name="modal-line"), spacing="2"), rx.hstack(rx.text("Cine:", class_name="modal-line"), rx.text(State.selected_location, class_name="modal-line"), spacing="2"), rx.hstack(rx.text("Horario:", class_name="modal-line"), rx.text(State.selected_time, class_name="modal-line"), spacing="2"), rx.hstack(rx.text("Total:", class_name="modal-total"), money_text(State.total, "modal-total"), spacing="2"), rx.button("Cerrar", class_name="primary-btn", on_click=State.close_checkout), spacing="4", align="start"), class_name="modal-card"), class_name="modal-overlay"),
        rx.fragment(),
    )


def footer():
    return rx.box(rx.grid(rx.vstack(rx.heading("CINEMAX", class_name="footer-logo"), rx.text("Sistema moderno para cine físico: cartelera, horarios, asientos, comida, factura y compra de boletos.", class_name="footer-text"), align="start"), rx.vstack(rx.heading("Secciones", class_name="footer-title"), rx.link("Inicio", href="#inicio", class_name="footer-link"), rx.link("Cartelera", href="#cartelera", class_name="footer-link"), rx.link("Próximamente", href="#proximamente", class_name="footer-link"), align="start"), rx.vstack(rx.heading("Cines", class_name="footer-title"), rx.text("Downtown Center", class_name="footer-link"), rx.text("Galería 360", class_name="footer-link"), rx.text("Megaplex 10", class_name="footer-link"), align="start"), columns="3", spacing="6"), class_name="footer")


def index():
    return rx.box(page_style(), hero(), subdivisions(), section_cines(), section_showing(), movie_detail(), section_coming(), booking_section(), footer(), checkout_modal(), search_overlay(), side_menu(), class_name="page")


app = rx.App(stylesheets=["/style.css"])
app.add_page(index, route="/", title="CineMax | Boletos de Cine")
