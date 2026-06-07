import reflex as rx  # type: ignore[import]
import httpx
from urllib.parse import quote

try:
    from data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE
    from config import API_BASE_URL
except ModuleNotFoundError:
    from .data import MOVIES, HERO_SLIDES, FOOD_MENU, INIT_SEATS, SERVICE_FEE
    from .config import API_BASE_URL


class State(rx.State):
    # =====================================================
    # ESTADO GENERAL
    # =====================================================

    hero_index: int = 0
    movie_id: int = 1

    search_text: str = ""
    show_search: bool = False
    show_menu: bool = False
    show_trailer: bool = False

    api_message: str = ""

    # =====================================================
    # ADMIN
    # =====================================================

    admin_message: str = ""
    admin_usuarios: list[dict] = []
    admin_reservas: list[dict] = []
    admin_peliculas: list[dict] = []

    admin_edit_movie_id: int = 0
    admin_movie_titulo: str = ""
    admin_movie_sinopsis: str = ""
    admin_movie_genero: str = ""
    admin_movie_clasificacion: str = ""
    admin_movie_duracion: str = ""
    admin_movie_poster_url: str = ""
    admin_movie_estado: str = "cartelera"
    admin_movie_fecha_estreno: str = ""

    # =====================================================
    # LOGIN / USUARIO
    # =====================================================

    is_logged_in: bool = False
    logged_user_id: int = 0
    logged_user_name: str = ""
    logged_user_email: str = ""
    logged_user_role: str = ""

    auth_mode: str = "login"
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    register_confirm_password: str = ""
    auth_message: str = ""

    # =====================================================
    # FUNCIONES / RESERVAS
    # =====================================================

    selected_location: str = "Downtown Center"
    selected_date: str = ""
    selected_showtime: str = ""
    selected_funcion_id: int = 0
    selected_payment_method: str = "Pago en taquilla"

    funciones: list[dict] = []

    seats: list[dict] = INIT_SEATS
    selected_seats: list[str] = []
    food_cart: list[dict] = FOOD_MENU
    booking_step: int = 1

    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""

    reservation_code: str = ""
    reservation_message: str = ""

    # =====================================================
    # PELÍCULAS
    # =====================================================

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
        trailer = self.current_movie.get("trailer", "")

        if not trailer:
            return ""

        if "youtube.com/embed/" in trailer:
            return trailer

        if "youtube.com/watch?v=" in trailer:
            video_id = trailer.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0&modestbranding=1"

        if "youtu.be/" in trailer:
            video_id = trailer.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0&modestbranding=1"

        return f"https://www.youtube.com/embed/{trailer}?autoplay=1&rel=0&modestbranding=1"

    @rx.var
    def cartelera_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m.get("tab") == "cartelera"]

        if not q:
            return movies

        return [
            m for m in movies
            if q in m.get("titulo", "").lower()
            or q in m.get("genero", "").lower()
            or q in m.get("clasificacion", "").lower()
        ]

    @rx.var
    def pronto_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m.get("tab") == "proximamente"]

        if not q:
            return movies

        return [
            m for m in movies
            if q in m.get("titulo", "").lower()
            or q in m.get("genero", "").lower()
            or q in m.get("clasificacion", "").lower()
        ]

    # =====================================================
    # FUNCIONES / HORARIOS
    # =====================================================

    @rx.var
    def available_dates(self) -> list[str]:
        dates: list[str] = []

        for funcion in self.funciones:
            if funcion.get("sucursal") == self.selected_location:
                fecha = str(funcion.get("fecha", ""))
                if fecha and fecha not in dates:
                    dates.append(fecha)

        return dates

    @rx.var
    def showtimes(self) -> list[str]:
        horarios: list[str] = []

        for funcion in self.funciones:
            if (
                funcion.get("sucursal") == self.selected_location
                and str(funcion.get("fecha", "")) == self.selected_date
            ):
                hora = str(funcion.get("hora", ""))
                sala = str(funcion.get("sala", ""))
                label = f"{hora} · {sala}"
                horarios.append(label)

        return horarios

    def load_movie_functions(self):
        self.api_message = ""

        try:
            response = httpx.get(
                f"{API_BASE_URL}/peliculas/{self.movie_id}/funciones",
                timeout=10,
            )

            if response.status_code != 200:
                self.funciones = []
                self.api_message = "No se pudieron cargar las funciones."
                return

            self.funciones = response.json()

            if self.funciones:
                primera_funcion = self.funciones[0]
                self.selected_location = primera_funcion.get("sucursal", self.selected_location)
                self.selected_date = str(primera_funcion.get("fecha", ""))
                self.selected_showtime = ""
                self.selected_funcion_id = 0

        except Exception as error:
            self.funciones = []
            self.api_message = f"Error cargando funciones: {str(error)}"

    def set_location(self, location: str):
        self.selected_location = location
        self.selected_showtime = ""
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""

        for funcion in self.funciones:
            if funcion.get("sucursal") == location:
                self.selected_date = str(funcion.get("fecha", ""))
                break

    def set_date(self, date: str):
        self.selected_date = date
        self.selected_showtime = ""
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""

    def set_showtime(self, time: str):
        self.selected_showtime = time
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""

        for funcion in self.funciones:
            label = f"{funcion.get('hora')} · {funcion.get('sala')}"

            if (
                funcion.get("sucursal") == self.selected_location
                and str(funcion.get("fecha", "")) == self.selected_date
                and label == time
            ):
                self.selected_funcion_id = int(funcion.get("id", 0))
                self.selected_showtime = str(funcion.get("hora", ""))
                break

    def load_reserved_seats(self):
        if self.selected_funcion_id <= 0:
            self.seats = [dict(s) for s in INIT_SEATS]
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/funciones/{self.selected_funcion_id}/asientos",
                timeout=10,
            )

            if response.status_code != 200:
                self.seats = [dict(s) for s in INIT_SEATS]
                return

            data = response.json()
            ocupados = data.get("asientos_ocupados", [])

            nuevos_asientos = []

            for seat in INIT_SEATS:
                nuevo = dict(seat)

                if nuevo["id"] in ocupados:
                    nuevo["estado"] = "reservado"
                else:
                    nuevo["estado"] = seat.get("estado", "disponible")

                nuevos_asientos.append(nuevo)

            self.seats = nuevos_asientos

        except Exception:
            self.seats = [dict(s) for s in INIT_SEATS]

    def start_booking(self):
        self.api_message = ""

        if self.selected_funcion_id <= 0:
            self.api_message = "Selecciona una función válida antes de continuar."
            return

        self.booking_step = 1
        self.selected_seats = []
        self.food_cart = [dict(item) for item in FOOD_MENU]
        self.load_reserved_seats()

        return rx.redirect("/reservar")

    # =====================================================
    # CARRITO / TOTALES
    # =====================================================

    @rx.var
    def ticket_count(self) -> int:
        return len(self.selected_seats)

    @rx.var
    def selected_seats_text(self) -> str:
        return ", ".join(self.selected_seats) if self.selected_seats else "Ninguno"

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
    def selected_food_text(self) -> str:
        items = [
            f"{item['nombre']} x{item.get('qty', 0)}"
            for item in self.food_cart
            if item.get("qty", 0) > 0
        ]

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
    def total_boletos(self) -> int:
        total = 0
        precio_base = 0

        for funcion in self.funciones:
            if int(funcion.get("id", 0)) == self.selected_funcion_id:
                precio_base = int(float(funcion.get("precio", 0)))
                break

        if precio_base <= 0:
            precio_base = int(self.current_movie.get("precio_regular", 500))

        for sid in self.selected_seats:
            for seat in self.seats:
                if seat["id"] == sid:
                    if seat.get("tipo") == "vip":
                        total += precio_base + 100
                    else:
                        total += precio_base
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

    # =====================================================
    # QR / TICKET
    # =====================================================

    @rx.var
    def display_user_name(self) -> str:
        return self.logged_user_name if self.logged_user_name else "Cliente"

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
            f"Dulceria: {self.selected_food_text}\n"
            f"Método de pago: {self.selected_payment_method}\n"
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
            f"Hola {self.reservation_customer_name},\n\n"
            f"Tu reserva fue creada correctamente.\n\n"
            f"Código: {self.reservation_code}\n"
            f"Película: {self.current_movie['titulo']}\n"
            f"Cine: {self.selected_location}\n"
            f"Fecha: {self.selected_date}\n"
            f"Hora: {self.selected_showtime}\n"
            f"Asientos: {self.selected_seats_text}\n"
            f"Dulcería: {self.selected_food_text}\n"
            f"Método de pago: {self.selected_payment_method}\n"
            f"Total: RD${self.gran_total}\n\n"
            f"QR de la reserva:\n{self.reservation_qr_url}\n\n"
            f"Presenta este código o QR en taquilla."
        )

        return f"mailto:{self.reservation_customer_email}?subject={subject}&body={body}"

    # =====================================================
    # FILAS DE ASIENTOS
    # =====================================================

    @rx.var
    def row_A(self) -> list[dict]:
        return self.seats[0:14]

    @rx.var
    def row_B(self) -> list[dict]:
        return self.seats[14:28]

    @rx.var
    def row_C(self) -> list[dict]:
        return self.seats[28:42]

    @rx.var
    def row_D(self) -> list[dict]:
        return self.seats[42:56]

    @rx.var
    def row_E(self) -> list[dict]:
        return self.seats[56:70]

    @rx.var
    def row_F(self) -> list[dict]:
        return self.seats[70:84]

    @rx.var
    def row_G(self) -> list[dict]:
        return self.seats[84:98]

    @rx.var
    def row_H(self) -> list[dict]:
        return self.seats[98:112]

    @rx.var
    def row_I(self) -> list[dict]:
        return self.seats[112:126]

    @rx.var
    def row_J(self) -> list[dict]:
        return self.seats[126:140]

    @rx.var
    def row_K(self) -> list[dict]:
        return self.seats[140:154]

    @rx.var
    def row_L(self) -> list[dict]:
        return self.seats[154:168]

    # =====================================================
    # ADMIN / USUARIOS
    # =====================================================

    @rx.var
    def total_admin_usuarios(self) -> int:
        return len(self.admin_usuarios)

    @rx.var
    def total_admin_roles(self) -> int:
        return len([u for u in self.admin_usuarios if u.get("rol") == "admin"])

    @rx.var
    def total_cliente_roles(self) -> int:
        return len([u for u in self.admin_usuarios if u.get("rol") == "cliente"])

    def load_admin_usuarios(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver usuarios."
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/auth/usuarios",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudieron cargar los usuarios.")
                self.admin_usuarios = []
                return

            usuarios_limpios = []

            for usuario in data:
                usuarios_limpios.append(
                    {
                        "id": int(usuario.get("id", 0)),
                        "nombre": str(usuario.get("nombre", "")),
                        "email": str(usuario.get("email", "")),
                        "rol": str(usuario.get("rol", "")),
                        "activo": bool(usuario.get("activo", False)),
                        "fecha_creacion": str(usuario.get("fecha_creacion", "")),
                    }
                )

            self.admin_usuarios = usuarios_limpios

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"
            self.admin_usuarios = []

    def toggle_user_status(self, usuario_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para modificar usuarios."
            return

        try:
            response = httpx.put(
                f"{API_BASE_URL}/admin/usuarios/{usuario_id}/estado",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo actualizar el usuario.")
                return

            self.admin_message = data.get("mensaje", "Usuario actualizado correctamente.")
            self.load_admin_usuarios()

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"

    # =====================================================
    # ADMIN / RESERVAS
    # =====================================================

    @rx.var
    def total_admin_reservas(self) -> int:
        return len(self.admin_reservas)

    @rx.var
    def total_reservas_pendientes(self) -> int:
        return len([r for r in self.admin_reservas if r.get("estado") == "pendiente"])

    @rx.var
    def total_reservas_confirmadas(self) -> int:
        return len([r for r in self.admin_reservas if r.get("estado") == "confirmada"])

    @rx.var
    def total_reservas_canceladas(self) -> int:
        return len([r for r in self.admin_reservas if r.get("estado") == "cancelada"])

    def load_admin_reservas(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver reservas."
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/reservas",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudieron cargar las reservas.")
                self.admin_reservas = []
                return

            reservas_limpias = []

            for reserva in data:
                asientos = reserva.get("asientos", [])
                if isinstance(asientos, list):
                    asientos_texto = ", ".join([str(a) for a in asientos]) if asientos else "Ninguno"
                else:
                    asientos_texto = str(asientos)

                total = float(reserva.get("total", 0))

                reservas_limpias.append(
                    {
                        "id": int(reserva.get("id", 0)),
                        "codigo_reserva": str(reserva.get("codigo_reserva", "")),
                        "nombre_cliente": str(reserva.get("nombre_cliente", "")),
                        "email_cliente": str(reserva.get("email_cliente", "")),
                        "telefono_cliente": str(reserva.get("telefono_cliente", "")),
                        "cliente_texto": f"{reserva.get('nombre_cliente', '')} · {reserva.get('email_cliente', '')}",
                        "cantidad_asientos": int(reserva.get("cantidad_asientos", 0)),
                        "total": total,
                        "total_texto": f"RD${total:,.0f}",
                        "metodo_pago": str(reserva.get("metodo_pago", "Pago en taquilla")),
                        "estado": str(reserva.get("estado", "pendiente")),
                        "fecha_reserva": str(reserva.get("fecha_reserva", "")),
                        "fecha": str(reserva.get("fecha", "")),
                        "hora": str(reserva.get("hora", "")),
                        "sala": str(reserva.get("sala", "")),
                        "pelicula": str(reserva.get("pelicula", "")),
                        "genero": str(reserva.get("genero", "")),
                        "clasificacion": str(reserva.get("clasificacion", "")),
                        "sucursal": str(reserva.get("sucursal", "")),
                        "direccion_sucursal": str(reserva.get("direccion_sucursal", "")),
                        "ciudad": str(reserva.get("ciudad", "")),
                        "asientos": asientos,
                        "asientos_texto": asientos_texto,
                    }
                )

            self.admin_reservas = reservas_limpias

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"
            self.admin_reservas = []

    def update_reserva_estado(self, reserva_id: int, estado: str):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para modificar reservas."
            return

        try:
            response = httpx.put(
                f"{API_BASE_URL}/admin/reservas/{reserva_id}/estado",
                json={"estado": estado},
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo actualizar la reserva.")
                return

            self.admin_message = data.get("mensaje", "Estado de reserva actualizado correctamente.")
            self.load_admin_reservas()

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"

    # =====================================================
    # ADMIN / PELÍCULAS
    # =====================================================

    @rx.var
    def total_admin_peliculas(self) -> int:
        return len(self.admin_peliculas)

    @rx.var
    def total_peliculas_cartelera(self) -> int:
        return len([p for p in self.admin_peliculas if p.get("estado") == "cartelera"])

    @rx.var
    def total_peliculas_proximamente(self) -> int:
        return len([p for p in self.admin_peliculas if p.get("estado") == "proximamente"])

    @rx.var
    def total_peliculas_inactivas(self) -> int:
        return len([p for p in self.admin_peliculas if not p.get("activa") or p.get("estado") == "inactiva"])

    def limpiar_pelicula_admin(self, pelicula: dict) -> dict:
        sinopsis = str(pelicula.get("sinopsis") or "")
        poster_url = str(pelicula.get("poster_url") or "")
        trailer = str(pelicula.get("trailer") or "")

        if not poster_url:
            poster_url = "https://via.placeholder.com/400x600/0f1320/ffffff?text=JC+Cinemas"

        trailer_url = ""
        if trailer:
            if "youtube.com" in trailer or "youtu.be" in trailer:
                trailer_url = trailer
            else:
                trailer_url = f"https://www.youtube.com/watch?v={trailer}"

        return {
            "id": int(pelicula.get("id", 0)),
            "tmdb_id": int(pelicula.get("tmdb_id") or 0),
            "titulo": str(pelicula.get("titulo") or ""),
            "sinopsis": sinopsis,
            "sinopsis_corta": sinopsis[:180] + "..." if len(sinopsis) > 180 else sinopsis,
            "genero": str(pelicula.get("genero") or "No disponible"),
            "clasificacion": str(pelicula.get("clasificacion") or "S/R"),
            "duracion_minutos": int(pelicula.get("duracion_minutos") or 0),
            "duracion_texto": f"{int(pelicula.get('duracion_minutos') or 0)} min",
            "poster_url": poster_url,
            "backdrop_url": str(pelicula.get("backdrop_url") or ""),
            "trailer": trailer,
            "trailer_url": trailer_url,
            "director": str(pelicula.get("director") or ""),
            "reparto": str(pelicula.get("reparto") or ""),
            "rating": str(pelicula.get("rating") or "0"),
            "estado": str(pelicula.get("estado") or "cartelera"),
            "fecha_estreno": str(pelicula.get("fecha_estreno") or ""),
            "activa": bool(pelicula.get("activa", False)),
        }

    def load_admin_peliculas(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver películas."
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/admin/peliculas",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudieron cargar las películas.")
                self.admin_peliculas = []
                return

            peliculas_limpias = []

            for pelicula in data:
                peliculas_limpias.append(self.limpiar_pelicula_admin(pelicula))

            self.admin_peliculas = peliculas_limpias

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"
            self.admin_peliculas = []

    def select_admin_pelicula(self, pelicula_id: int):
        self.admin_message = ""

        for pelicula in self.admin_peliculas:
            if int(pelicula.get("id", 0)) == pelicula_id:
                self.admin_edit_movie_id = pelicula_id
                self.admin_movie_titulo = pelicula.get("titulo", "")
                self.admin_movie_sinopsis = pelicula.get("sinopsis", "")
                self.admin_movie_genero = pelicula.get("genero", "")
                self.admin_movie_clasificacion = pelicula.get("clasificacion", "")
                self.admin_movie_duracion = str(pelicula.get("duracion_minutos", ""))
                self.admin_movie_poster_url = pelicula.get("poster_url", "")
                self.admin_movie_estado = pelicula.get("estado", "cartelera")
                self.admin_movie_fecha_estreno = pelicula.get("fecha_estreno", "")
                break

    def clear_admin_pelicula_form(self):
        self.admin_edit_movie_id = 0
        self.admin_movie_titulo = ""
        self.admin_movie_sinopsis = ""
        self.admin_movie_genero = ""
        self.admin_movie_clasificacion = ""
        self.admin_movie_duracion = ""
        self.admin_movie_poster_url = ""
        self.admin_movie_estado = "cartelera"
        self.admin_movie_fecha_estreno = ""

    def set_admin_movie_titulo(self, v: str):
        self.admin_movie_titulo = v

    def set_admin_movie_sinopsis(self, v: str):
        self.admin_movie_sinopsis = v

    def set_admin_movie_genero(self, v: str):
        self.admin_movie_genero = v

    def set_admin_movie_clasificacion(self, v: str):
        self.admin_movie_clasificacion = v

    def set_admin_movie_duracion(self, v: str):
        self.admin_movie_duracion = v

    def set_admin_movie_poster_url(self, v: str):
        self.admin_movie_poster_url = v

    def set_admin_movie_estado(self, v: str):
        self.admin_movie_estado = v

    def set_admin_movie_fecha_estreno(self, v: str):
        self.admin_movie_fecha_estreno = v

    def update_admin_pelicula(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para modificar películas."
            return

        if self.admin_edit_movie_id <= 0:
            self.admin_message = "Selecciona una película para editar."
            return

        if not self.admin_movie_titulo:
            self.admin_message = "El título es obligatorio."
            return

        try:
            duracion = int(self.admin_movie_duracion) if self.admin_movie_duracion else 0

            response = httpx.put(
                f"{API_BASE_URL}/admin/peliculas/{self.admin_edit_movie_id}",
                json={
                    "titulo": self.admin_movie_titulo,
                    "sinopsis": self.admin_movie_sinopsis,
                    "genero": self.admin_movie_genero,
                    "clasificacion": self.admin_movie_clasificacion,
                    "duracion_minutos": duracion,
                    "poster_url": self.admin_movie_poster_url,
                    "estado": self.admin_movie_estado,
                    "fecha_estreno": self.admin_movie_fecha_estreno,
                    "activa": self.admin_movie_estado != "inactiva",
                },
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo actualizar la película.")
                return

            self.admin_message = data.get("mensaje", "Película actualizada correctamente.")
            self.clear_admin_pelicula_form()
            self.load_admin_peliculas()

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"

    def deactivate_admin_pelicula(self, pelicula_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para desactivar películas."
            return

        try:
            response = httpx.delete(
                f"{API_BASE_URL}/admin/peliculas/{pelicula_id}",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo desactivar la película.")
                return

            self.admin_message = data.get("mensaje", "Película desactivada correctamente.")
            self.load_admin_peliculas()

        except Exception as error:
            self.admin_message = f"Error conectando con el servidor: {str(error)}"

    # =====================================================
    # HERO / NAVEGACIÓN
    # =====================================================

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
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""
        self.load_movie_functions()
        return rx.redirect("/pelicula")

    def hero_details(self):
        self.movie_id = self.hero_movie["id"]
        self.show_trailer = False
        self.selected_showtime = ""
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""
        self.load_movie_functions()
        return rx.redirect("/pelicula")

    def hero_trailer(self):
        self.movie_id = self.hero_movie["id"]
        self.show_trailer = True
        self.selected_showtime = ""
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""
        self.load_movie_functions()
        return rx.redirect("/pelicula")

    def open_trailer(self):
        self.show_trailer = True

    def close_trailer(self):
        self.show_trailer = False

    # =====================================================
    # ASIENTOS
    # =====================================================

    def toggle_seat(self, seat_id: str):
        for seat in self.seats:
            if seat["id"] == seat_id and seat.get("estado") == "reservado":
                return

        if seat_id in self.selected_seats:
            self.selected_seats = [s for s in self.selected_seats if s != seat_id]
        elif len(self.selected_seats) < 8:
            self.selected_seats = self.selected_seats + [seat_id]

    # =====================================================
    # PASOS DE COMPRA
    # =====================================================

    def next_step(self):
        self.api_message = ""

        if self.booking_step == 1 and not self.selected_seats:
            self.api_message = "Selecciona al menos un asiento."
            return

        if self.booking_step < 4:
            self.booking_step += 1

    def prev_step(self):
        self.api_message = ""

        if self.booking_step > 1:
            self.booking_step -= 1

    # =====================================================
    # DULCERÍA
    # =====================================================

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

    # =====================================================
    # DATOS CLIENTE
    # =====================================================

    def set_customer_name(self, v: str):
        self.customer_name = v

    def set_customer_email(self, v: str):
        self.customer_email = v

    def set_customer_phone(self, v: str):
        self.customer_phone = v

    def set_payment_method(self, v: str):
        self.selected_payment_method = v

    # =====================================================
    # CONFIRMAR RESERVA REAL EN BACKEND
    # =====================================================

    def confirm_reservation(self):
        self.api_message = ""
        self.reservation_message = ""

        if self.selected_funcion_id <= 0:
            self.api_message = "Debes seleccionar una función."
            self.reservation_message = "Debes seleccionar una función."
            return

        if not self.selected_seats:
            self.api_message = "Debes seleccionar al menos un asiento."
            self.reservation_message = "Debes seleccionar al menos un asiento."
            return

        if self.is_logged_in:
            self.customer_name = self.logged_user_name
            self.customer_email = self.logged_user_email
        else:
            if not self.customer_name or not self.customer_email:
                self.api_message = "Completa tu nombre y correo."
                self.reservation_message = "Completa tu nombre y correo."
                return

        if not self.customer_phone:
            self.api_message = "Completa tu teléfono."
            self.reservation_message = "Completa tu teléfono."
            return

        try:
            response = httpx.post(
                f"{API_BASE_URL}/reservas",
                json={
                    "funcion_id": self.selected_funcion_id,
                    "nombre_cliente": self.customer_name,
                    "email_cliente": self.customer_email,
                    "telefono_cliente": self.customer_phone,
                    "asientos": self.selected_seats,
                    "metodo_pago": self.selected_payment_method,
                },
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                mensaje = data.get("detail", "No se pudo crear la reserva.")
                self.api_message = mensaje
                self.reservation_message = mensaje
                return

            self.reservation_code = data.get("codigo_reserva", "")
            self.booking_step = 4

        except Exception as error:
            mensaje = f"Error conectando con el servidor: {str(error)}"
            self.api_message = mensaje
            self.reservation_message = mensaje

    def new_booking(self):
        self.booking_step = 1
        self.selected_seats = []
        self.food_cart = [dict(item) for item in FOOD_MENU]
        self.seats = [dict(s) for s in INIT_SEATS]
        self.customer_phone = ""
        self.reservation_code = ""
        self.reservation_message = ""
        self.api_message = ""
        return rx.redirect("/pelicula")

    # =====================================================
    # AUTH
    # =====================================================

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

        try:
            response = httpx.post(
                f"{API_BASE_URL}/auth/login",
                json={
                    "email": self.login_email,
                    "password": self.login_password,
                },
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.auth_message = data.get("detail", "No se pudo iniciar sesión.")
                return

            usuario = data["usuario"]

            self.is_logged_in = True
            self.logged_user_id = int(usuario["id"])
            self.logged_user_name = usuario["nombre"]
            self.logged_user_email = usuario["email"]
            self.logged_user_role = usuario["rol"]

            self.customer_name = usuario["nombre"]
            self.customer_email = usuario["email"]

            self.auth_message = "Sesión iniciada correctamente."

            if usuario["rol"] == "admin":
                return rx.redirect("/admin")

            return rx.redirect("/")

        except Exception as error:
            self.auth_message = f"Error conectando con el servidor: {str(error)}"

    def register_user(self):
        if not self.register_name or not self.register_email or not self.register_password:
            self.auth_message = "Completa todos los campos."
            return

        if self.register_password != self.register_confirm_password:
            self.auth_message = "Las contraseñas no coinciden."
            return

        try:
            response = httpx.post(
                f"{API_BASE_URL}/auth/register",
                json={
                    "nombre": self.register_name,
                    "email": self.register_email,
                    "password": self.register_password,
                },
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.auth_message = data.get("detail", "No se pudo crear la cuenta.")
                return

            usuario = data["usuario"]

            self.is_logged_in = True
            self.logged_user_id = int(usuario["id"])
            self.logged_user_name = usuario["nombre"]
            self.logged_user_email = usuario["email"]
            self.logged_user_role = usuario["rol"]

            self.customer_name = usuario["nombre"]
            self.customer_email = usuario["email"]

            self.auth_message = "Cuenta creada correctamente."
            return rx.redirect("/")

        except Exception as error:
            self.auth_message = f"Error conectando con el servidor: {str(error)}"

    def logout(self):
        self.is_logged_in = False
        self.logged_user_id = 0
        self.logged_user_name = ""
        self.logged_user_email = ""
        self.logged_user_role = ""

        self.login_email = ""
        self.login_password = ""

        self.customer_name = ""
        self.customer_email = ""
        self.auth_message = ""
        self.api_message = ""
        self.admin_message = ""

        return rx.redirect("/")