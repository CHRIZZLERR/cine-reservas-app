import reflex as rx  # type: ignore[import]
from urllib.parse import quote

try:
    from data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE
except ModuleNotFoundError:
    from .data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE


class State(rx.State):
    hero_index: int = 0
    movie_id: int = 1

    is_logged_in: bool = False
    logged_user_name: str = ""
    logged_user_email: str = ""

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

    auth_mode: str = "login"
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    register_confirm_password: str = ""
    auth_message: str = ""

    is_logged_in: bool = False
    logged_user_name: str = ""
    logged_user_email: str = ""

    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""
    reservation_code: str = ""

    # LOGIN / REGISTRO SIMULADO
    auth_mode: str = "login"
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    register_confirm_password: str = ""
    auth_message: str = ""
    is_logged_in: bool = False
    logged_user_name: str = ""

    @rx.var
    def hero_movie(self) -> dict:
        return HERO_SLIDES[self.hero_index] if HERO_SLIDES else MOVIES[0]

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
    def ticket_count(self) -> int:
        return len(self.selected_seats)

    @rx.var
    def selected_food_items(self) -> list[dict]:
        return [item for item in self.food_cart if item.get("qty", 0) > 0]

    @rx.var
    def selected_food_text(self) -> str:
        items = [f"{item['nombre']} x{item.get('qty', 0)}" for item in self.food_cart if item.get("qty", 0) > 0]
        return ", ".join(items) if items else "Sin productos"

    @rx.var
    def current_step_name(self) -> str:
        if self.booking_step == 1:
            return "Selecciona tus asientos"
        if self.booking_step == 2:
            return "Agrega comida y bebidas"
        if self.booking_step == 3:
            return "Completa tus datos"
        return "Reserva confirmada"

    @rx.var
    def next_button_text(self) -> str:
        if self.booking_step == 1:
            return "Continuar a dulcería"
        if self.booking_step == 2:
            return "Continuar a datos"
        if self.booking_step == 3:
            return "Confirmar reserva"
        return "Reserva creada"

    @rx.var
    def cartelera_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "cartelera"]

        # Filtrar por localización seleccionada
        movies = [
            m for m in movies
            if self.selected_location in m.get("funciones", {})
        ]

        if not q:
            return movies

        return [
            m for m in movies
            if q in m["titulo"].lower()
            or q in m["genero"].lower()
            or q in m["clasificacion"].lower()
        ]

    @rx.var
    def pronto_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "proximamente"]

        if not q:
            return movies

        return [
            m for m in movies
            if q in m["titulo"].lower()
            or q in m["genero"].lower()
            or q in m["clasificacion"].lower()
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
    def selected_food_items(self) -> list[dict]:
        return [
            {
                **item,
                "subtotal": item["precio"] * item.get("qty", 0),
            }
            for item in self.food_cart
            if item.get("qty", 0) > 0
        ]

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
    def reservation_qr_data(self) -> str:
        return (
            f"Reserva: {self.reservation_code}\n"
            f"Cliente: {self.customer_name}\n"
            f"Correo: {self.customer_email}\n"
            f"Pelicula: {self.current_movie['titulo']}\n"
            f"Cine: {self.selected_location}\n"
            f"Fecha: {self.selected_date}\n"
            f"Hora: {self.selected_showtime}\n"
            f"Asientos: {self.selected_seats_text}\n"
            f"Total: RD${self.gran_total}"
        )

    @rx.var
    def reservation_qr_url(self) -> str:
        data = quote(self.reservation_qr_data)
        return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={data}"


    @rx.var
    def reservation_email_link(self) -> str:
        subject = quote(f"Reserva {self.reservation_code} - JC Cinemas")
        body = quote(
            f"Hola {self.customer_name},\n\n"
            f"Tu reserva fue creada correctamente.\n\n"
            f"Código: {self.reservation_code}\n"
            f"Película: {self.current_movie['titulo']}\n"
            f"Cine: {self.selected_location}\n"
            f"Fecha: {self.selected_date}\n"
            f"Hora: {self.selected_showtime}\n"
            f"Asientos: {self.selected_seats_text}\n"
            f"Total: RD${self.gran_total}\n\n"
            f"QR de la reserva:\n{self.reservation_qr_url}\n\n"
            f"Presenta este código o QR en taquilla."
        )
        return f"mailto:{self.customer_email}?subject={subject}&body={body}"

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

    @rx.var
    def display_user_name(self) -> str:
        return self.logged_user_name if self.is_logged_in else "Iniciar sesión"


    @rx.var
    def reservation_customer_name(self) -> str:
        return self.logged_user_name if self.is_logged_in else self.customer_name


    @rx.var
    def reservation_customer_email(self) -> str:
        return self.logged_user_email if self.is_logged_in else self.customer_email


    @rx.var
    def reservation_qr_data(self) -> str:
        return (
            f"Reserva: {self.reservation_code}\n"
            f"Cliente: {self.reservation_customer_name}\n"
            f"Correo: {self.reservation_customer_email}\n"
            f"Pelicula: {self.current_movie['titulo']}\n"
            f"Cine: {self.selected_location}\n"
            f"Fecha: {self.selected_date}\n"
            f"Hora: {self.selected_showtime}\n"
            f"Asientos: {self.selected_seats_text}\n"
            f"Total: RD${self.gran_total}"
        )


    @rx.var
    def reservation_qr_url(self) -> str:
        from urllib.parse import quote

        data = quote(self.reservation_qr_data)
        return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={data}"


    @rx.var
    def reservation_email_link(self) -> str:
        from urllib.parse import quote

        subject = quote(f"Reserva {self.reservation_code} - JC Cinemas")
        body = quote(
            f"Hola {self.reservation_customer_name},\n\n"
            f"Tu reserva fue creada correctamente.\n\n"
            f"Código: {self.reservation_code}\n"
            f"Película: {self.current_movie['titulo']}\n"
            f"Cine: {self.selected_location}\n"
            f"Fecha: {self.selected_date}\n"
            f"Hora: {self.selected_showtime}\n"
            f"Asientos: {self.selected_seats_text}\n"
            f"Total: RD${self.gran_total}\n\n"
            f"QR de la reserva:\n{self.reservation_qr_url}\n\n"
            f"Presenta este código o QR en taquilla."
        )

        return f"mailto:{self.reservation_customer_email}?subject={subject}&body={body}"

    def next_hero(self):
        self.hero_index = (self.hero_index + 1) % len(HERO_SLIDES)

    def prev_hero(self):
        self.hero_index = (self.hero_index - 1) % len(HERO_SLIDES)

    def go_to_slide(self, idx: int):
        self.hero_index = idx

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

    def open_trailer(self):
        self.show_trailer = True

    def close_trailer(self):
        self.show_trailer = False

    def logout(self):
        self.is_logged_in = False
        self.logged_user_name = ""
        self.logged_user_email = ""
        self.login_email = ""
        self.login_password = ""
        self.customer_name = ""
        self.customer_email = ""
        self.auth_message = ""
        return rx.redirect("/")

    def set_location(self, location: str):
        self.selected_location = location
        self.selected_showtime = ""

    def set_date(self, date: str):
        self.selected_date = date

    def set_showtime(self, time: str):
        self.selected_showtime = time

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

    def set_customer_name(self, v: str):
        self.customer_name = v

    def set_customer_email(self, v: str):
        self.customer_email = v

    def set_customer_phone(self, v: str):
        self.customer_phone = v

    def confirm_reservation(self):
        import random

        if self.is_logged_in:
            self.customer_name = self.logged_user_name
            self.customer_email = self.logged_user_email
        else:
            if not self.customer_name or not self.customer_email:
                return

        if not self.customer_phone:
            return

        self.reservation_code = f"JCC-{random.randint(10000, 99999)}"
        self.booking_step = 4

    def new_booking(self):
            self.booking_step = 1
            self.selected_seats = []
            self.food_cart = [dict(item) for item in FOOD_MENU]
            self.seats = [dict(s) for s in INIT_SEATS]
            self.customer_phone = ""
            self.reservation_code = ""
            return rx.redirect("/pelicula")
    
    # AUTH
    def show_login(self):
        self.auth_mode = "login"
        self.auth_message = ""

    def show_register(self):
        self.auth_mode = "register"
        self.auth_message = ""

    def set_login_email(self, v: str):
        self.login_email = v

    def set_login_password(self, v: str):
        self.login_password = v

    def set_register_name(self, v: str):
        self.register_name = v

    def set_register_email(self, v: str):
        self.register_email = v

    def set_register_password(self, v: str):
        self.register_password = v

    def set_register_confirm_password(self, v: str):
        self.register_confirm_password = v

    def login(self):
        if not self.login_email or not self.login_password:
            self.auth_message = "Completa tu correo y contraseña."
            return

        self.is_logged_in = True
        self.logged_user_email = self.login_email
        self.logged_user_name = self.login_email.split("@")[0].title()

        self.customer_name = self.logged_user_name
        self.customer_email = self.logged_user_email

        self.auth_message = "Sesión iniciada correctamente."
        return rx.redirect("/")

    def register_user(self):
        if not self.register_name or not self.register_email or not self.register_password:
            self.auth_message = "Completa todos los campos."
            return

        if self.register_password != self.register_confirm_password:
            self.auth_message = "Las contraseñas no coinciden."
            return

        self.is_logged_in = True
        self.logged_user_name = self.register_name
        self.logged_user_email = self.register_email

        self.customer_name = self.register_name
        self.customer_email = self.register_email

        self.auth_message = "Cuenta creada correctamente."
        return rx.redirect("/")