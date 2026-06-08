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
    admin_funciones: list[dict] = []
    admin_sucursales: list[dict] = []

    # =====================================================
    # ADMIN / PELÍCULAS FORM
    # =====================================================

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
    # ADMIN / FUNCIONES FORM
    # =====================================================

    admin_edit_funcion_id: int = 0
    admin_funcion_pelicula_id: str = ""
    admin_funcion_sucursal_id: str = ""
    admin_funcion_fecha: str = ""
    admin_funcion_hora: str = ""
    admin_funcion_sala: str = ""
    admin_funcion_precio: str = ""

    # =====================================================
    # ADMIN / SUCURSALES FORM
    # =====================================================

    admin_edit_sucursal_id: int = 0
    admin_sucursal_nombre: str = ""
    admin_sucursal_direccion: str = ""
    admin_sucursal_ciudad: str = ""
    admin_sucursal_activa: bool = True

    # =====================================================
    # ADMIN / TMDB
    # =====================================================

    tmdb_query: str = ""
    tmdb_results: list[dict] = []

    tmdb_detail_loaded: bool = False
    tmdb_detail_id_int: int = 0
    tmdb_detail_id: str = ""
    tmdb_detail_title: str = ""
    tmdb_detail_overview: str = ""
    tmdb_detail_poster: str = ""
    tmdb_detail_release_date: str = ""
    tmdb_detail_rating: str = ""

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

    public_movies: list[dict] = []
    public_movies_loaded: bool = False
    public_movies_message: str = ""

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
    # HELPERS
    # =====================================================

    def safe_int(self, value, default: int = 0) -> int:
        try:
            return int(float(value))
        except Exception:
            return default

    def convertir_duracion_minutos(self, value) -> int:
        try:
            return int(float(value))
        except Exception:
            texto = str(value).lower().strip()

            horas = 0
            minutos = 0

            if "h" in texto:
                partes = texto.split("h")

                try:
                    horas = int(partes[0].strip())
                except Exception:
                    horas = 0

                if len(partes) > 1:
                    minutos_texto = (
                        partes[1]
                        .replace("min", "")
                        .replace("m", "")
                        .strip()
                    )

                    try:
                        minutos = int(minutos_texto)
                    except Exception:
                        minutos = 0

                return horas * 60 + minutos

            if "min" in texto or "m" in texto:
                minutos_texto = texto.replace("min", "").replace("m", "").strip()

                try:
                    return int(minutos_texto)
                except Exception:
                    return 0

            return 0

    # =====================================================
    # PELÍCULAS PÚBLICAS DESDE API
    # =====================================================

    def limpiar_pelicula_publica(self, pelicula: dict) -> dict:
        poster_url = str(
            pelicula.get("poster_url")
            or pelicula.get("poster")
            or pelicula.get("imagen")
            or pelicula.get("portada")
            or ""
        )

        if not poster_url:
            poster_url = "https://via.placeholder.com/400x600/0f1320/ffffff?text=JC+Cinemas"

        backdrop_url = str(
            pelicula.get("backdrop_url")
            or pelicula.get("fondo")
            or pelicula.get("banner")
            or poster_url
        )

        trailer = str(pelicula.get("trailer") or "")

        estado = str(
            pelicula.get("estado")
            or pelicula.get("tab")
            or "cartelera"
        ).lower()

        if estado not in ["cartelera", "proximamente", "inactiva"]:
            estado = "cartelera"

        titulo = str(pelicula.get("titulo") or pelicula.get("title") or "Sin título")
        sinopsis = str(pelicula.get("sinopsis") or pelicula.get("descripcion") or "")

        duracion_raw = pelicula.get("duracion_minutos") or pelicula.get("duracion") or 0
        duracion = self.convertir_duracion_minutos(duracion_raw)

        precio_raw = pelicula.get("precio_regular", 500)
        precio_regular = self.safe_int(precio_raw, 500)

        return {
            "id": self.safe_int(pelicula.get("id", 0), 0),
            "tmdb_id": self.safe_int(pelicula.get("tmdb_id") or 0, 0),
            "titulo": titulo,
            "title": titulo,
            "sinopsis": sinopsis,
            "descripcion": sinopsis,
            "resumen": sinopsis,
            "genero": str(pelicula.get("genero") or "No disponible"),
            "clasificacion": str(pelicula.get("clasificacion") or "S/R"),
            "duracion_minutos": duracion,
            "duracion": duracion,
            "duracion_texto": f"{duracion} min" if duracion > 0 else str(duracion_raw),
            "poster_url": poster_url,
            "poster": poster_url,
            "imagen": poster_url,
            "portada": poster_url,
            "backdrop_url": backdrop_url,
            "fondo": backdrop_url,
            "trailer": trailer,
            "rating": str(pelicula.get("rating") or "0"),
            "estado": estado,
            "tab": estado,
            "fecha_estreno": str(pelicula.get("fecha_estreno") or ""),
            "activa": bool(pelicula.get("activa", True)),
            "precio_regular": precio_regular,
            "image": poster_url,
            "director": str(pelicula.get("director") or "No disponible"),
            "reparto": str(pelicula.get("reparto") or "No disponible"),
        }

    def load_public_movies(self):
        """Carga todas las películas públicas sin filtrar por sucursal.
        Usar para Inicio y Próximamente.
        """
        self.public_movies_message = ""

        try:
            response = httpx.get(
                f"{API_BASE_URL}/peliculas",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.public_movies_message = "No se pudieron cargar las películas desde la API."
                self.public_movies = []
                self.public_movies_loaded = True
                return

            peliculas_limpias = []

            for pelicula in data:
                limpia = self.limpiar_pelicula_publica(pelicula)

                if limpia["activa"] and limpia["estado"] != "inactiva":
                    peliculas_limpias.append(limpia)

            self.public_movies = peliculas_limpias
            self.public_movies_loaded = True

        except Exception as error:
            self.public_movies_message = f"Error cargando cartelera desde API: {str(error)}"
            self.public_movies = []
            self.public_movies_loaded = True

    @rx.var
    def all_movies_public(self) -> list[dict]:
        return self.public_movies
    
    @rx.var
    def hero_cartelera_movies(self) -> list[dict]:
        movies = [
            movie for movie in self.public_movies
            if movie.get("estado") == "cartelera"
        ]

        return movies[:5]

    def load_public_movies_por_sucursal(self):
        """Carga películas filtradas por sucursal.
        Usar solo para Cartelera.
        """
        self.public_movies_message = ""

        try:
            params = {}

            if self.selected_location:
                params["sucursal"] = self.selected_location

            response = httpx.get(
                f"{API_BASE_URL}/peliculas",
                params=params,
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.public_movies_message = "No se pudieron cargar las películas desde la API."
                self.public_movies = []
                self.public_movies_loaded = True
                return

            peliculas_limpias = []

            for pelicula in data:
                limpia = self.limpiar_pelicula_publica(pelicula)

                if limpia["activa"] and limpia["estado"] != "inactiva":
                    peliculas_limpias.append(limpia)

            self.public_movies = peliculas_limpias
            self.public_movies_loaded = True

        except Exception as error:
            self.public_movies_message = f"Error cargando cartelera desde API: {str(error)}"
            self.public_movies = []
            self.public_movies_loaded = True

    @rx.var
    def hero_movie(self) -> dict:
        peliculas = self.hero_cartelera_movies

        if peliculas:
            index = self.hero_index % len(peliculas)
            return peliculas[index]
        return {
            "id": 0,
            "titulo": "Cargando películas...",
            "title": "Cargando películas...",
            "sinopsis": "Estamos cargando la cartelera desde la API.",
            "descripcion": "Estamos cargando la cartelera desde la API.",
            "genero": "",
            "clasificacion": "",
            "duracion_minutos": 0,
            "duracion": 0,
            "duracion_texto": "",
            "poster_url": "",
            "poster": "",
            "backdrop_url": "",
            "fondo": "",
            "trailer": "",
            "rating": "0",
            "estado": "cartelera",
            "fecha_estreno": "",
            "activa": True,
            "precio_regular": 500,
            "image": "",
            "director": "No disponible",
            "reparto": "No disponible",
        }

    @rx.var
    def current_movie(self) -> dict:
        for movie in self.public_movies:
            if int(movie.get("id", 0)) == int(self.movie_id):
                return movie

        if self.public_movies:
            return self.public_movies[0]

        return self.hero_movie

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

        movies = [
            m for m in self.public_movies
            if m.get("estado") == "cartelera"
        ]

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

        movies = [
            m for m in self.public_movies
            if m.get("estado") == "proximamente"
        ]
        if not q:
            return movies

        return [
            m for m in movies
            if q in m.get("titulo", "").lower()
            or q in m.get("genero", "").lower()
            or q in m.get("clasificacion", "").lower()
        ]

    # =====================================================
    # FUNCIONES / HORARIOS PÚBLICOS
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
            params = {}

            if self.selected_location:
                params["sucursal"] = self.selected_location

            response = httpx.get(
                f"{API_BASE_URL}/peliculas/{self.movie_id}/funciones",
                params=params,
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

        self.load_public_movies_por_sucursal()

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

    def seleccionar_pelicula_home(self, pelicula_id: int):
        peliculas = [
            movie for movie in self.public_movies
            if movie.get("estado") == "cartelera"
        ][:5]

        for index, pelicula in enumerate(peliculas):
            if int(pelicula.get("id", 0)) == int(pelicula_id):
                self.hero_index = index
                return
        
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
    # ADMIN / FUNCIONES
    # =====================================================

    @rx.var
    def total_admin_funciones(self) -> int:
        return len(self.admin_funciones)

    @rx.var
    def total_admin_sucursales(self) -> int:
        return len(self.admin_sucursales)

    def limpiar_funcion_admin(self, funcion: dict) -> dict:
        precio = float(funcion.get("precio") or 0)

        return {
            "id": int(funcion.get("id", 0)),
            "pelicula_id": int(funcion.get("pelicula_id", 0)),
            "sucursal_id": int(funcion.get("sucursal_id", 0)),
            "pelicula": str(funcion.get("pelicula") or funcion.get("titulo") or "Sin película"),
            "sucursal": str(funcion.get("sucursal") or funcion.get("nombre_sucursal") or "Sin sucursal"),
            "fecha": str(funcion.get("fecha") or ""),
            "hora": str(funcion.get("hora") or ""),
            "sala": str(funcion.get("sala") or ""),
            "precio": precio,
            "precio_texto": f"RD${precio:,.0f}",
        }

    def load_admin_funciones_page(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver funciones."
            return

        self.load_admin_peliculas()
        self.load_admin_sucursales()
        self.load_admin_funciones()

    def load_admin_funciones(self):
        self.admin_message = ""

        try:
            response = httpx.get(
                f"{API_BASE_URL}/admin/funciones",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudieron cargar las funciones.")
                self.admin_funciones = []
                return

            funciones_limpias = [
                self.limpiar_funcion_admin(funcion)
                for funcion in data
            ]

            funciones_limpias.sort(key=lambda f: int(f.get("id", 0)), reverse=True)

            self.admin_funciones = funciones_limpias

        except Exception as error:
            self.admin_message = f"Error cargando funciones: {str(error)}"
            self.admin_funciones = []

    def load_admin_sucursales(self):
        try:
            response = httpx.get(
                f"{API_BASE_URL}/admin/sucursales",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_sucursales = []
                return

            sucursales_limpias = []

            for sucursal in data:
                sucursales_limpias.append(
                    {
                        "id": int(sucursal.get("id", 0)),
                        "nombre": str(sucursal.get("nombre") or ""),
                        "direccion": str(sucursal.get("direccion") or ""),
                        "ciudad": str(sucursal.get("ciudad") or ""),
                        "activa": bool(sucursal.get("activa", False)),
                    }
                )

            sucursales_limpias.sort(key=lambda s: int(s.get("id", 0)), reverse=True)

            self.admin_sucursales = sucursales_limpias

        except Exception:
            self.admin_sucursales = []

    def set_admin_funcion_pelicula_id(self, v: str):
        self.admin_funcion_pelicula_id = v

    def set_admin_funcion_sucursal_id(self, v: str):
        self.admin_funcion_sucursal_id = v

    def set_admin_funcion_fecha(self, v: str):
        self.admin_funcion_fecha = v

    def set_admin_funcion_hora(self, v: str):
        self.admin_funcion_hora = v

    def set_admin_funcion_sala(self, v: str):
        self.admin_funcion_sala = v

    def set_admin_funcion_precio(self, v: str):
        self.admin_funcion_precio = v

    def clear_admin_funcion_form(self):
        self.admin_edit_funcion_id = 0
        self.admin_funcion_pelicula_id = ""
        self.admin_funcion_sucursal_id = ""
        self.admin_funcion_fecha = ""
        self.admin_funcion_hora = ""
        self.admin_funcion_sala = ""
        self.admin_funcion_precio = ""

    def select_admin_funcion(self, funcion_id: int):
        self.admin_message = ""

        for funcion in self.admin_funciones:
            if int(funcion.get("id", 0)) == funcion_id:
                self.admin_edit_funcion_id = funcion_id
                self.admin_funcion_pelicula_id = str(funcion.get("pelicula_id", ""))
                self.admin_funcion_sucursal_id = str(funcion.get("sucursal_id", ""))
                self.admin_funcion_fecha = str(funcion.get("fecha", ""))
                self.admin_funcion_hora = str(funcion.get("hora", ""))
                self.admin_funcion_sala = str(funcion.get("sala", ""))
                self.admin_funcion_precio = str(int(float(funcion.get("precio", 0))))

                self.admin_message = f"Editando función #{funcion_id}. Modifica los datos arriba y guarda los cambios."

                return rx.call_script("window.scrollTo({ top: 0, behavior: 'smooth' });")

        self.admin_message = "No se encontró la función seleccionada."

    def save_admin_funcion(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para guardar funciones."
            return

        if (
            not self.admin_funcion_pelicula_id
            or not self.admin_funcion_sucursal_id
            or not self.admin_funcion_fecha
            or not self.admin_funcion_hora
            or not self.admin_funcion_sala
            or not self.admin_funcion_precio
        ):
            self.admin_message = "Completa todos los campos de la función."
            return

        try:
            payload = {
                "pelicula_id": int(self.admin_funcion_pelicula_id),
                "sucursal_id": int(self.admin_funcion_sucursal_id),
                "fecha": self.admin_funcion_fecha,
                "hora": self.admin_funcion_hora,
                "sala": self.admin_funcion_sala,
                "precio": float(self.admin_funcion_precio),
            }

            if self.admin_edit_funcion_id > 0:
                response = httpx.put(
                    f"{API_BASE_URL}/admin/funciones/{self.admin_edit_funcion_id}",
                    json=payload,
                    timeout=10,
                )
            else:
                response = httpx.post(
                    f"{API_BASE_URL}/admin/funciones",
                    json=payload,
                    timeout=10,
                )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo guardar la función.")
                return

            self.admin_message = data.get("mensaje", "Función guardada correctamente.")
            self.clear_admin_funcion_form()
            self.load_admin_funciones()

            return rx.call_script("window.scrollTo({ top: 0, behavior: 'smooth' });")

        except ValueError:
            self.admin_message = "Los campos ID y precio deben ser números válidos."

        except Exception as error:
            self.admin_message = f"Error guardando función: {str(error)}"

    def delete_admin_funcion(self, funcion_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para eliminar funciones."
            return

        try:
            response = httpx.delete(
                f"{API_BASE_URL}/admin/funciones/{funcion_id}",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo eliminar la función.")
                return

            self.admin_message = data.get("mensaje", "Función eliminada correctamente.")
            self.load_admin_funciones()

        except Exception as error:
            self.admin_message = f"Error eliminando función: {str(error)}"

    # =====================================================
    # ADMIN / SUCURSALES
    # =====================================================

    @rx.var
    def total_sucursales_activas(self) -> int:
        return len([s for s in self.admin_sucursales if s.get("activa")])

    @rx.var
    def total_sucursales_inactivas(self) -> int:
        return len([s for s in self.admin_sucursales if not s.get("activa")])

    def load_admin_sucursales_page(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver sucursales."
            return

        self.load_admin_sucursales()

    def set_admin_sucursal_nombre(self, v: str):
        self.admin_sucursal_nombre = v

    def set_admin_sucursal_direccion(self, v: str):
        self.admin_sucursal_direccion = v

    def set_admin_sucursal_ciudad(self, v: str):
        self.admin_sucursal_ciudad = v

    def clear_admin_sucursal_form(self):
        self.admin_edit_sucursal_id = 0
        self.admin_sucursal_nombre = ""
        self.admin_sucursal_direccion = ""
        self.admin_sucursal_ciudad = ""
        self.admin_sucursal_activa = True

    def select_admin_sucursal(self, sucursal_id: int):
        self.admin_message = ""

        for sucursal in self.admin_sucursales:
            if int(sucursal.get("id", 0)) == sucursal_id:
                self.admin_edit_sucursal_id = sucursal_id
                self.admin_sucursal_nombre = str(sucursal.get("nombre", ""))
                self.admin_sucursal_direccion = str(sucursal.get("direccion", ""))
                self.admin_sucursal_ciudad = str(sucursal.get("ciudad", ""))
                self.admin_sucursal_activa = bool(sucursal.get("activa", True))

                self.admin_message = f"Editando sucursal #{sucursal_id}. Modifica los datos arriba y guarda los cambios."

                return rx.call_script("window.scrollTo({ top: 0, behavior: 'smooth' });")

        self.admin_message = "No se encontró la sucursal seleccionada."

    def save_admin_sucursal(self):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para guardar sucursales."
            return

        if (
            not self.admin_sucursal_nombre.strip()
            or not self.admin_sucursal_direccion.strip()
            or not self.admin_sucursal_ciudad.strip()
        ):
            self.admin_message = "Completa nombre, dirección y ciudad."
            return

        payload_create = {
            "nombre": self.admin_sucursal_nombre.strip(),
            "direccion": self.admin_sucursal_direccion.strip(),
            "ciudad": self.admin_sucursal_ciudad.strip(),
        }

        payload_update = {
            "nombre": self.admin_sucursal_nombre.strip(),
            "direccion": self.admin_sucursal_direccion.strip(),
            "ciudad": self.admin_sucursal_ciudad.strip(),
            "activa": self.admin_sucursal_activa,
        }

        try:
            if self.admin_edit_sucursal_id > 0:
                response = httpx.put(
                    f"{API_BASE_URL}/admin/sucursales/{self.admin_edit_sucursal_id}",
                    json=payload_update,
                    timeout=10,
                )
            else:
                response = httpx.post(
                    f"{API_BASE_URL}/admin/sucursales",
                    json=payload_create,
                    timeout=10,
                )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo guardar la sucursal.")
                return

            self.admin_message = data.get("mensaje", "Sucursal guardada correctamente.")
            self.clear_admin_sucursal_form()
            self.load_admin_sucursales()

            return rx.call_script("window.scrollTo({ top: 0, behavior: 'smooth' });")

        except Exception as error:
            self.admin_message = f"Error guardando sucursal: {str(error)}"

    def toggle_admin_sucursal_status(self, sucursal_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para cambiar el estado de sucursales."
            return

        try:
            response = httpx.delete(
                f"{API_BASE_URL}/admin/sucursales/{sucursal_id}",
                timeout=10,
            )

            data = response.json()

            if response.status_code != 200:
                self.admin_message = data.get("detail", "No se pudo cambiar el estado de la sucursal.")
                return

            self.admin_message = data.get("mensaje", "Estado de sucursal actualizado correctamente.")
            self.clear_admin_sucursal_form()
            self.load_admin_sucursales()

        except Exception as error:
            self.admin_message = f"Error cambiando estado de sucursal: {str(error)}"

    # =====================================================
    # ADMIN / TMDB
    # =====================================================

    @rx.var
    def tmdb_results_count(self) -> int:
        return len(self.tmdb_results)

    def set_tmdb_query(self, v: str):
        self.tmdb_query = v

    def limpiar_resultado_tmdb(self, movie) -> dict:
        if not isinstance(movie, dict):
            return {
                "id": 0,
                "title": "Resultado inválido",
                "overview": "TMDB devolvió un formato no compatible.",
                "overview_short": "TMDB devolvió un formato no compatible.",
                "poster_url": "https://via.placeholder.com/400x600/0f1320/ffffff?text=TMDB",
                "release_date": "",
                "year": "Sin fecha",
                "rating": 0.0,
                "rating_text": "⭐ 0.0",
            }

        poster_url = str(
            movie.get("poster_url")
            or movie.get("poster")
            or movie.get("poster_completo")
            or ""
        )

        if not poster_url:
            poster_path = str(movie.get("poster_path") or "")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        if not poster_url:
            poster_url = "https://via.placeholder.com/400x600/0f1320/ffffff?text=TMDB"

        title = str(
            movie.get("title")
            or movie.get("titulo")
            or movie.get("name")
            or movie.get("nombre")
            or "Sin título"
        )

        overview = str(
            movie.get("overview")
            or movie.get("sinopsis")
            or movie.get("descripcion")
            or "Sin descripción disponible."
        )

        release_date = str(
            movie.get("release_date")
            or movie.get("fecha_estreno")
            or movie.get("estreno")
            or ""
        )

        year = "Sin fecha"
        if len(release_date) >= 4:
            year = release_date[:4]

        rating = movie.get("vote_average", movie.get("rating", movie.get("calificacion", 0)))

        try:
            rating_float = float(rating)
        except Exception:
            rating_float = 0.0

        return {
            "id": int(movie.get("id", movie.get("tmdb_id", 0)) or 0),
            "title": title,
            "overview": overview,
            "overview_short": overview[:210] + "..." if len(overview) > 210 else overview,
            "poster_url": poster_url,
            "release_date": release_date,
            "year": year,
            "rating": rating_float,
            "rating_text": f"⭐ {rating_float:.1f}",
        }

    def extraer_resultados_tmdb(self, data) -> list:
        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            if isinstance(data.get("results"), list):
                return data["results"]

            if isinstance(data.get("resultados"), list):
                return data["resultados"]

            if isinstance(data.get("peliculas"), list):
                return data["peliculas"]

            if isinstance(data.get("data"), list):
                return data["data"]

            if isinstance(data.get("movies"), list):
                return data["movies"]

        return []

    def search_tmdb_movies(self):
        self.admin_message = ""
        self.tmdb_detail_loaded = False
        self.tmdb_results = []

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para buscar en TMDB."
            return

        if not self.tmdb_query.strip():
            self.admin_message = "Escribe el nombre de una película."
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/tmdb/buscar",
                params={
                    "query": self.tmdb_query.strip(),
                    "language": "es-ES",
                },
                timeout=15,
            )

            try:
                data = response.json()
            except Exception:
                self.admin_message = "TMDB devolvió una respuesta que no es JSON."
                self.tmdb_results = []
                return

            if response.status_code != 200:
                if isinstance(data, dict):
                    self.admin_message = data.get("detail", "No se pudo consultar TMDB.")
                else:
                    self.admin_message = "No se pudo consultar TMDB."
                self.tmdb_results = []
                return

            results = self.extraer_resultados_tmdb(data)

            resultados_limpios = []

            for movie in results:
                limpio = self.limpiar_resultado_tmdb(movie)
                if limpio["id"] > 0:
                    resultados_limpios.append(limpio)

            self.tmdb_results = resultados_limpios

            if len(resultados_limpios) == 0:
                self.admin_message = "No se encontraron resultados para esa búsqueda."
            else:
                self.admin_message = f"Se encontraron {len(resultados_limpios)} resultados."

        except Exception as error:
            self.admin_message = f"Error conectando con TMDB: {str(error)}"
            self.tmdb_results = []

    def load_tmdb_detail(self, tmdb_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para ver detalles de TMDB."
            return

        try:
            response = httpx.get(
                f"{API_BASE_URL}/tmdb/pelicula/{tmdb_id}",
                timeout=15,
            )

            try:
                data = response.json()
            except Exception:
                self.admin_message = "TMDB devolvió un detalle que no es JSON."
                return

            if response.status_code != 200:
                if isinstance(data, dict):
                    self.admin_message = data.get("detail", "No se pudo cargar el detalle.")
                else:
                    self.admin_message = "No se pudo cargar el detalle."
                return

            if isinstance(data, dict) and isinstance(data.get("pelicula"), dict):
                data = data["pelicula"]

            if isinstance(data, dict) and isinstance(data.get("detalle"), dict):
                data = data["detalle"]

            limpio = self.limpiar_resultado_tmdb(data)

            self.tmdb_detail_loaded = True
            self.tmdb_detail_id_int = limpio["id"]
            self.tmdb_detail_id = str(limpio["id"])
            self.tmdb_detail_title = limpio["title"]
            self.tmdb_detail_overview = limpio["overview"]
            self.tmdb_detail_poster = limpio["poster_url"]
            self.tmdb_detail_release_date = limpio["release_date"]
            self.tmdb_detail_rating = limpio["rating_text"]

        except Exception as error:
            self.admin_message = f"Error cargando detalle de TMDB: {str(error)}"

    def clear_tmdb_detail(self):
        self.tmdb_detail_loaded = False
        self.tmdb_detail_id_int = 0
        self.tmdb_detail_id = ""
        self.tmdb_detail_title = ""
        self.tmdb_detail_overview = ""
        self.tmdb_detail_poster = ""
        self.tmdb_detail_release_date = ""
        self.tmdb_detail_rating = ""

    def import_tmdb_movie(self, tmdb_id: int):
        self.admin_message = ""

        if self.logged_user_role != "admin":
            self.admin_message = "No tienes permisos para importar películas."
            return

        if int(tmdb_id) <= 0:
            self.admin_message = "ID de TMDB inválido."
            return

        try:
            response = httpx.post(
                f"{API_BASE_URL}/admin/peliculas/importar-tmdb/{tmdb_id}",
                timeout=20,
            )

            try:
                data = response.json()
            except Exception:
                self.admin_message = "El servidor devolvió una respuesta inválida al importar."
                return

            if response.status_code != 200:
                if isinstance(data, dict):
                    self.admin_message = data.get("detail", "No se pudo importar la película.")
                else:
                    self.admin_message = "No se pudo importar la película."
                return

            if isinstance(data, dict):
                self.admin_message = data.get("mensaje", "Película importada correctamente.")
            else:
                self.admin_message = "Película importada correctamente."

            try:
                self.load_admin_peliculas()
            except Exception:
                pass

        except Exception as error:
            self.admin_message = f"Error importando película desde TMDB: {str(error)}"

    # =====================================================
    # HERO / NAVEGACIÓN
    # =====================================================

    def next_hero(self):
        movies = [
            movie for movie in self.public_movies
            if movie.get("estado") == "cartelera"
        ][:5]

        total = len(movies)

        if total > 0:
            self.hero_index = (self.hero_index + 1) % total


    def prev_hero(self):
        movies = [
            movie for movie in self.public_movies
            if movie.get("estado") == "cartelera"
        ][:5]

        total = len(movies)

        if total > 0:
            self.hero_index = (self.hero_index - 1) % total


    def go_to_slide(self, idx: int):
        movies = [
            movie for movie in self.public_movies
            if movie.get("estado") == "cartelera"
        ][:5]

        total = len(movies)

        if total > 0:
            self.hero_index = idx % total


    def seleccionar_pelicula_home(self, pelicula_id: int):
        peliculas = self.public_movies

        for index, pelicula in enumerate(peliculas):
            if int(pelicula.get("id", 0)) == int(pelicula_id):
                self.hero_index = index
                return

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
        self.movie_id = int(self.hero_movie.get("id", 1))
        self.show_trailer = False
        self.selected_showtime = ""
        self.selected_funcion_id = 0
        self.selected_seats = []
        self.api_message = ""
        self.load_movie_functions()
        return rx.redirect("/pelicula")

    def hero_trailer(self):
        self.movie_id = int(self.hero_movie.get("id", 1))
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