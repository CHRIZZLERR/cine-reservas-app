import reflex as rx  # type: ignore[import]

try:
    from data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE
except ModuleNotFoundError:
    from .data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE


class State(rx.State):
    hero_index: int = 0
    movie_id: int = 1
    search_text: str = ""
    show_search: bool = False
    show_menu: bool = False
    show_trailer: bool = False
    selected_location: str = "Downtown Center"
    selected_date: str = "Hoy · Vie 29"
    selected_showtime: str = ""
    seats: list[dict] = INIT_SEATS
    selected_seats: list[str] = []
    food_cart: list[dict] = FOOD_MENU
    booking_step: int = 1
    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""
    reservation_code: str = ""

    @rx.var
    def hero_movie(self) -> dict:
        return HERO_SLIDES[self.hero_index]

    @rx.var
    def current_movie(self) -> dict:
        for movie in MOVIES:
            if movie["id"] == self.movie_id:
                return movie
        return MOVIES[0]

    @rx.var
    def trailer_url(self) -> str:
        return (
            f"https://www.youtube.com/embed/{self.current_movie.get('trailer', '')}"
            "?autoplay=1&rel=0&modestbranding=1"
        )

    @rx.var
    def cartelera_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "cartelera"]
        return movies if not q else [
            m for m in movies
            if q in m["titulo"].lower() or q in m["genero"].lower() or q in m["clasificacion"].lower()
        ]

    @rx.var
    def pronto_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "proximamente"]
        return movies if not q else [
            m for m in movies
            if q in m["titulo"].lower() or q in m["genero"].lower() or q in m["clasificacion"].lower()
        ]

    @rx.var
    def showtimes(self) -> list[str]:
        return self.current_movie.get("funciones", {}).get(self.selected_location, [])

    @rx.var
    def selected_seats_text(self) -> str:
        return ", ".join(self.selected_seats) if self.selected_seats else "Ninguno"

    @rx.var
    def total_boletos(self) -> int:
        total = 0
        for sid in self.selected_seats:
            for seat in self.seats:
                if seat["id"] == sid:
                    total += (
                        self.current_movie["precio_vip"]
                        if seat["tipo"] == "vip"
                        else self.current_movie["precio_regular"]
                    )
                    break
        return total

    @rx.var
    def total_comida(self) -> int:
        return sum(item["precio"] * item.get("qty", 0) for item in self.food_cart)

    @rx.var
    def cargo_servicio(self) -> int:
        return len(self.selected_seats) * SERVICE_FEE

    @rx.var
    def gran_total(self) -> int:
        return self.total_boletos + self.total_comida + self.cargo_servicio

    @rx.var
    def row_A(self) -> list[dict]: return self.seats[0:14]
    @rx.var
    def row_B(self) -> list[dict]: return self.seats[14:28]
    @rx.var
    def row_C(self) -> list[dict]: return self.seats[28:42]
    @rx.var
    def row_D(self) -> list[dict]: return self.seats[42:56]
    @rx.var
    def row_E(self) -> list[dict]: return self.seats[56:70]
    @rx.var
    def row_F(self) -> list[dict]: return self.seats[70:84]
    @rx.var
    def row_G(self) -> list[dict]: return self.seats[84:98]
    @rx.var
    def row_H(self) -> list[dict]: return self.seats[98:112]
    @rx.var
    def row_I(self) -> list[dict]: return self.seats[112:126]
    @rx.var
    def row_J(self) -> list[dict]: return self.seats[126:140]
    @rx.var
    def row_K(self) -> list[dict]: return self.seats[140:154]
    @rx.var
    def row_L(self) -> list[dict]: return self.seats[154:168]

    def next_hero(self): self.hero_index = (self.hero_index + 1) % len(HERO_SLIDES)
    def prev_hero(self): self.hero_index = (self.hero_index - 1) % len(HERO_SLIDES)
    def go_to_slide(self, idx: int): self.hero_index = idx
    def set_search_text(self, value: str): self.search_text = value
    def toggle_search(self): self.show_search = not self.show_search
    def close_search(self): self.show_search = False
    def toggle_menu(self): self.show_menu = not self.show_menu
    def close_menu(self): self.show_menu = False

    def go_to_movie(self, movie_id: int):
        self.movie_id = movie_id
        self.show_trailer = False
        self.selected_showtime = ""
        self.selected_location = "Downtown Center"
        return rx.redirect("/pelicula")

    def hero_details(self):
        self.movie_id = self.hero_movie["id"]
        self.show_trailer = False
        return rx.redirect("/pelicula")

    def hero_trailer(self):
        self.movie_id = self.hero_movie["id"]
        self.show_trailer = True
        return rx.redirect("/pelicula")

    def open_trailer(self): self.show_trailer = True
    def close_trailer(self): self.show_trailer = False

    def set_location(self, location: str):
        self.selected_location = location
        self.selected_showtime = ""

    def set_date(self, date: str): self.selected_date = date
    def set_showtime(self, time: str): self.selected_showtime = time

    def start_booking(self):
        if not self.selected_showtime:
            return
        self.booking_step = 1
        self.selected_seats = []
        self.food_cart = [dict(item) for item in FOOD_MENU]
        self.seats = [dict(s) for s in INIT_SEATS]
        return rx.redirect("/reservar")

    def toggle_seat(self, seat_id: str):
        for seat in self.seats:
            if seat["id"] == seat_id and seat["estado"] == "reservado":
                return
        if seat_id in self.selected_seats:
            self.selected_seats = [s for s in self.selected_seats if s != seat_id]
        elif len(self.selected_seats) < 8:
            self.selected_seats = self.selected_seats + [seat_id]

    def next_step(self):
        if self.booking_step == 1 and not self.selected_seats:
            return
        if self.booking_step < 4:
            self.booking_step += 1

    def prev_step(self):
        if self.booking_step > 1:
            self.booking_step -= 1

    def add_food(self, fid: str):
        self.food_cart = [
            {**item, "qty": item.get("qty", 0) + 1} if item["id"] == fid else item
            for item in self.food_cart
        ]

    def remove_food(self, fid: str):
        self.food_cart = [
            {**item, "qty": max(0, item.get("qty", 0) - 1)} if item["id"] == fid else item
            for item in self.food_cart
        ]

    def set_customer_name(self, v: str): self.customer_name = v
    def set_customer_email(self, v: str): self.customer_email = v
    def set_customer_phone(self, v: str): self.customer_phone = v

    def confirm_reservation(self):
        import random
        self.reservation_code = f"CNH-{random.randint(10000, 99999)}"
        self.booking_step = 4