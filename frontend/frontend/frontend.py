
# =============================================================
# CineMax · Frontend Cliente V5 Pro
# UI refinada: posters, carrusel automático, lupa, drawer,
# detalle con trailer, funciones, mapa de asientos y factura.
# =============================================================
import reflex as rx

GFONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
)

SERVICE_FEE = 45
LOCATIONS = ["Downtown Center", "Galería 360", "Ágora Mall", "Blue Mall", "Sambil"]
LOCATION_DETAILS = {
    "Downtown Center": {
        "zona": "Av. Núñez de Cáceres, Santo Domingo",
        "salas": "Salas CXC, VIP, 2D y dulcería premium",
        "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Caribbean+Cinemas+Downtown+Center+Santo+Domingo",
    },
    "Galería 360": {
        "zona": "Av. John F. Kennedy, Santo Domingo",
        "salas": "Cine moderno, funciones familiares y área de snacks",
        "image": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Caribbean+Cinemas+Galeria+360+Santo+Domingo",
    },
    "Ágora Mall": {
        "zona": "Av. Abraham Lincoln, Santo Domingo",
        "salas": "Experiencia premium en plaza comercial",
        "image": "https://images.unsplash.com/photo-1533488765986-dfa2a9939acd?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Caribbean+Cinemas+Agora+Mall+Santo+Domingo",
    },
    "Blue Mall": {
        "zona": "Av. Winston Churchill, Santo Domingo",
        "salas": "Cine ejecutivo, salas cómodas y ambiente premium",
        "image": "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Blue+Mall+Santo+Domingo",
    },
    "Sambil": {
        "zona": "Av. John F. Kennedy, Santo Domingo",
        "salas": "Funciones para toda la familia, dulcería y estrenos",
        "image": "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Caribbean+Cinemas+Sambil+Santo+Domingo",
    },
}
DATES = ["Hoy · Vie 29", "Sáb 30", "Dom 31", "Lun 01", "Mar 02", "Mié 03"]
SEAT_ROWS = list("ABCDEFGHIJKL")

# Nota: Las imágenes de cartelera usan assets servidos por Caribbean Cinemas/Indy Systems.
# En cards se usa poster vertical; en hero se usa imagen panorámica.
MOVIES: list[dict] = [
    {
        "id": 1, "titulo": "Mortal Kombat II", "genero": "Acción / Fantasía", "clasificacion": "R/18", "duracion": "1h 56m",
        "director": "Simon McQuoid", "productor": "Todd Garner, James Wan", "reparto": "Karl Urban, Adeline Rudolph, Jessica McNamee, Hiroyuki Sanada",
        "sinopsis": "Los campeones favoritos de los fans, ahora acompañados por Johnny Cage, se enfrentan en una batalla definitiva para detener el dominio de Shao Kahn sobre Earthrealm.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 500, "precio_vip": 850, "rating": "7.4",
        "image": "https://indy-systems.imgix.net/r5e5qth1g9nif0nnmgmixufkc2jc?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/r5e5qth1g9nif0nnmgmixufkc2jc?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "b24oG7qCwp4",
        "funciones": {"Downtown Center": ["4:20 PM", "6:55 PM", "8:35 PM", "9:30 PM"], "Galería 360": ["3:45 PM", "6:20 PM", "9:10 PM"], "Ágora Mall": ["5:00 PM", "7:30 PM", "10:00 PM"], "Blue Mall": ["6:15 PM", "9:20 PM"], "Sambil": ["4:40 PM", "7:10 PM", "9:55 PM"]},
    },
    {
        "id": 2, "titulo": "The Devil Wears Prada 2", "genero": "Drama / Comedia", "clasificacion": "R/14", "duracion": "1h 59m",
        "director": "David Frankel", "productor": "Wendy Finerman", "reparto": "Meryl Streep, Anne Hathaway, Emily Blunt, Stanley Tucci",
        "sinopsis": "Miranda Priestly navega su carrera en medio del declive de la publicación tradicional y se enfrenta a Emily Charlton, ahora una poderosa ejecutiva de lujo.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 500, "precio_vip": 850, "rating": "7.1",
        "image": "https://indy-systems.imgix.net/n63odn7qc2n4vgiwjn4e51z4ubod?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/n63odn7qc2n4vgiwjn4e51z4ubod?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "PMd1at7OwiE",
        "funciones": {"Downtown Center": ["4:05 PM", "6:55 PM", "8:45 PM", "9:35 PM"], "Galería 360": ["4:30 PM", "6:55 PM", "9:35 PM"], "Ágora Mall": ["5:25 PM", "7:40 PM", "10:05 PM"], "Blue Mall": ["6:00 PM", "8:40 PM"], "Sambil": ["4:10 PM", "7:00 PM", "9:20 PM"]},
    },
    {
        "id": 3, "titulo": "Lee Cronin's The Mummy", "genero": "Terror / Suspenso", "clasificacion": "R/18", "duracion": "2h 13m",
        "director": "Lee Cronin", "productor": "Atomic Monster, Blumhouse", "reparto": "Jack Reynor, Laia Costa, May Calamawy",
        "sinopsis": "La hija de un periodista desaparece en el desierto y regresa ocho años después, convirtiendo una reunión familiar en una pesadilla viviente.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 500, "precio_vip": 850, "rating": "7.0",
        "image": "https://indy-systems.imgix.net/7y2gkw4acwxtmlxg1w2hiaecle9g?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/7y2gkw4acwxtmlxg1w2hiaecle9g?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "XJ0uv-phsDk",
        "funciones": {"Downtown Center": ["3:15 PM", "6:05 PM", "9:00 PM"], "Galería 360": ["4:15 PM", "7:05 PM", "10:00 PM"], "Ágora Mall": ["5:30 PM", "8:30 PM"], "Blue Mall": ["6:45 PM", "9:45 PM"], "Sambil": ["5:20 PM", "8:50 PM"]},
    },
    {
        "id": 4, "titulo": "Hoppers", "genero": "Animación / Familiar", "clasificacion": "S/R", "duracion": "1h 45m",
        "director": "Daniel Chong", "productor": "Pixar Animation Studios", "reparto": "Piper Curda, Bobby Moynihan, Jon Hamm",
        "sinopsis": "Mabel aprovecha una tecnología que permite transferir la conciencia humana a animales robóticos para descubrir misterios del mundo animal.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 450, "precio_vip": 800, "rating": "6.9",
        "image": "https://indy-systems.imgix.net/30vf44btt3ora5lcbmakqndq4cct?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/30vf44btt3ora5lcbmakqndq4cct?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "PypDSyIRRSs",
        "funciones": {"Downtown Center": ["3:55 PM", "6:20 PM"], "Galería 360": ["2:15 PM", "5:05 PM", "7:20 PM"], "Ágora Mall": ["1:30 PM", "4:15 PM", "6:45 PM"], "Blue Mall": ["3:00 PM", "5:30 PM"], "Sambil": ["2:40 PM", "5:10 PM", "7:30 PM"]},
    },
    {
        "id": 5, "titulo": "De tal palo, tal astilla", "genero": "Comedia Dominicana", "clasificacion": "R/12", "duracion": "1h 25m",
        "director": "Frank Perozo", "productor": "Caribbean Films", "reparto": "Raymond Pozo, Miguel Céspedes, Hony Estrella",
        "sinopsis": "En un hotel de lujo, una escultura invaluable desaparece durante un apagón y desata una investigación caótica llena de secretos y viejos conflictos.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 450, "precio_vip": 800, "rating": "7.3",
        "image": "https://indy-systems.imgix.net/tq2rmjo090yq9nmoj8f4yvbvj9me?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/tq2rmjo090yq9nmoj8f4yvbvj9me?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "JHif2sq226E",
        "funciones": {"Downtown Center": ["5:25 PM", "7:35 PM", "9:35 PM"], "Galería 360": ["4:30 PM", "7:10 PM", "9:20 PM"], "Ágora Mall": ["5:00 PM", "7:30 PM"], "Blue Mall": ["6:40 PM", "8:55 PM"], "Sambil": ["5:40 PM", "8:10 PM", "10:00 PM"]},
    },
    {
        "id": 6, "titulo": "Star Wars: The Mandalorian and Grogu", "genero": "Acción / Aventura", "clasificacion": "R/14", "duracion": "2h 20m",
        "director": "Jon Favreau", "productor": "Dave Filoni, Kathleen Kennedy", "reparto": "Pedro Pascal, Sigourney Weaver, Jeremy Allen White",
        "sinopsis": "La Nueva República recluta al legendario Mandaloriano Din Djarin y a Grogu para proteger lo que la Rebelión luchó por construir.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 550, "precio_vip": 900, "rating": "8.1",
        "image": "https://indy-systems.imgix.net/ynkoxyun8l0g4zsvobovmmhbkhsy?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/ynkoxyun8l0g4zsvobovmmhbkhsy?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "IHWlvwu8t1w",
        "funciones": {"Downtown Center": ["3:30 PM", "6:25 PM", "9:20 PM"], "Galería 360": ["3:00 PM", "6:00 PM", "9:00 PM"], "Ágora Mall": ["4:20 PM", "7:20 PM"], "Blue Mall": ["5:10 PM", "8:15 PM"], "Sambil": ["3:50 PM", "6:40 PM", "9:40 PM"]},
    },
    {
        "id": 7, "titulo": "Panda Plan: The Magical Tribe", "genero": "Comedia / Familiar", "clasificacion": "S/R", "duracion": "1h 40m",
        "director": "Derek Hui", "productor": "Mandarin Motion Pictures", "reparto": "Jackie Chan, Ma Li, Qiao Shan",
        "sinopsis": "El panda gigante Hu Hu y Jackie Chan tropiezan con una misteriosa tribu primitiva, iniciando una aventura familiar llena de acción y humor.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 450, "precio_vip": 800, "rating": "6.6",
        "image": "https://indy-systems.imgix.net/v4edwffeo3lzicxd6aan5buqso9r?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/v4edwffeo3lzicxd6aan5buqso9r?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "O4dasmRRXLE",
        "funciones": {"Downtown Center": ["4:05 PM", "6:20 PM"], "Galería 360": ["2:30 PM", "5:15 PM"], "Ágora Mall": ["3:20 PM", "6:10 PM"], "Blue Mall": ["4:50 PM", "7:00 PM"], "Sambil": ["3:30 PM", "6:00 PM"]},
    },
    {
        "id": 8, "titulo": "Fuze", "genero": "Drama / Thriller", "clasificacion": "R/14", "duracion": "1h 38m",
        "director": "David Mackenzie", "productor": "Anton, Sigma Films", "reparto": "Aaron Taylor-Johnson, Theo James, Gugu Mbatha-Raw",
        "sinopsis": "Una bomba sin explotar de la Segunda Guerra Mundial aparece en una obra en Londres, desatando una evacuación masiva y una carrera contra el tiempo.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 500, "precio_vip": 850, "rating": "7.8",
        "image": "https://indy-systems.imgix.net/1cpvffjm9yy6ovaq0j6nat7ycm91?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/1cpvffjm9yy6ovaq0j6nat7ycm91?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "b-_42xDX43w",
        "funciones": {"Downtown Center": ["4:50 PM", "7:10 PM", "9:30 PM"], "Galería 360": ["6:00 PM", "8:30 PM"], "Ágora Mall": ["5:40 PM", "8:45 PM"], "Blue Mall": ["7:20 PM", "9:40 PM"], "Sambil": ["5:30 PM", "8:25 PM"]},
    },
    {
        "id": 9, "titulo": "The Super Mario Galaxy Movie", "genero": "Animación / Aventura", "clasificacion": "PG", "duracion": "1h 50m",
        "director": "Aaron Horvath, Michael Jelenic", "productor": "Nintendo, Illumination", "reparto": "Chris Pratt, Anya Taylor-Joy, Charlie Day",
        "sinopsis": "Mario y sus amigos exploran galaxias nuevas en una aventura familiar llena de humor, color y mundos imposibles.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 500, "precio_vip": 850, "rating": "7.2",
        "image": "https://images.unsplash.com/photo-1612404730960-5c71577fca11?auto=format&fit=crop&w=1280&q=80",
        "poster": "https://images.unsplash.com/photo-1612404730960-5c71577fca11?auto=format&fit=crop&w=700&h=1050&q=80",
        "trailer": "8B8n5w5mT7Y",
        "funciones": {"Downtown Center": ["2:15 PM", "4:45 PM", "7:15 PM"], "Galería 360": ["2:00 PM", "4:30 PM", "6:55 PM"], "Ágora Mall": ["1:40 PM", "4:05 PM", "6:30 PM"], "Blue Mall": ["3:30 PM", "6:10 PM"], "Sambil": ["2:50 PM", "5:20 PM"]},
    },
    {
        "id": 10, "titulo": "Perla", "genero": "Drama", "clasificacion": "R/14", "duracion": "1h 48m",
        "director": "Alexis Morante", "productor": "Película Latina", "reparto": "Reparto internacional",
        "sinopsis": "Una historia íntima sobre decisiones, memoria y familia, contada con una mirada humana y visualmente elegante.",
        "tab": "cartelera", "fecha_estreno": "En cartelera", "precio_regular": 450, "precio_vip": 800, "rating": "6.8",
        "image": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=1280&q=80",
        "poster": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=700&h=1050&q=80",
        "trailer": "dQw4w9WgXcQ",
        "funciones": {"Downtown Center": ["5:10 PM", "8:00 PM"], "Galería 360": ["6:30 PM", "9:00 PM"], "Ágora Mall": ["5:50 PM"], "Blue Mall": ["7:10 PM"], "Sambil": ["6:20 PM"]},
    },
    # Próximamente: ampliado con títulos listados por Caribbean Cinemas RD.
    {
        "id": 11, "titulo": "Dune: Part Three", "genero": "Ciencia ficción / Épica", "clasificacion": "PG-13", "duracion": "2h 45m",
        "director": "Denis Villeneuve", "productor": "Mary Parent, Cale Boyter", "reparto": "Timothée Chalamet, Zendaya, Florence Pugh, Robert Pattinson",
        "sinopsis": "Paul Atreides enfrenta las consecuencias de su ascenso al poder mientras una guerra sagrada amenaza el futuro de Arrakis y de toda la galaxia.",
        "tab": "pronto", "fecha_estreno": "17 diciembre 2026", "precio_regular": 550, "precio_vip": 900, "rating": "8.4",
        "image": "https://indy-systems.imgix.net/uv4oh117gv3q6v0mtm6ryw7e9erq?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/uv4oh117gv3q6v0mtm6ryw7e9erq?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "n9xhJrPXop4", "funciones": {},
    },
    {
        "id": 12, "titulo": "Toy Story 5", "genero": "Animación / Familiar", "clasificacion": "G", "duracion": "1h 42m",
        "director": "Andrew Stanton", "productor": "Lindsey Collins", "reparto": "Tom Hanks, Tim Allen, Joan Cusack",
        "sinopsis": "Bonnie recibe una tablet Lilypad y los juguetes deben enfrentarse a una nueva amenaza para el tiempo de juego.",
        "tab": "pronto", "fecha_estreno": "18 junio 2026", "precio_regular": 500, "precio_vip": 850, "rating": "7.9",
        "image": "https://indy-systems.imgix.net/wgj12qskqmyg2uxzc7nx35o6dcjg?auto=format&fit=crop&fm=jpeg&h=720&w=1280",
        "poster": "https://indy-systems.imgix.net/wgj12qskqmyg2uxzc7nx35o6dcjg?auto=format&fit=crop&fm=jpeg&h=1050&w=700",
        "trailer": "wmiIUN-7qhE", "funciones": {},
    },
    {"id": 13, "titulo": "Spider-Man: Brand New Day", "genero": "Acción / Aventura", "clasificacion": "PG-13", "duracion": "2h 20m", "director": "Destin Daniel Cretton", "productor": "Kevin Feige, Amy Pascal", "reparto": "Tom Holland, Zendaya, Sadie Sink, Jacob Batalon", "sinopsis": "Peter Parker empieza una nueva vida en Nueva York mientras una amenaza inesperada cambia su destino como Spider-Man.", "tab": "pronto", "fecha_estreno": "30 julio 2026", "precio_regular": 550, "precio_vip": 900, "rating": "8.0", "image": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?auto=format&fit=crop&w=1280&q=80", "poster": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?auto=format&fit=crop&w=700&h=1050&q=80", "trailer": "JfVOs4VSpmA", "funciones": {}},
    {"id": 14, "titulo": "Supergirl", "genero": "Acción / Ciencia ficción", "clasificacion": "NR", "duracion": "1h 50m", "director": "Craig Gillespie", "productor": "James Gunn, Peter Safran", "reparto": "Milly Alcock, Matthias Schoenaerts, Eve Ridley", "sinopsis": "Kara Zor-El se une a una compañera inesperada en un viaje interstellar de justicia y venganza.", "tab": "pronto", "fecha_estreno": "25 junio 2026", "precio_regular": 550, "precio_vip": 900, "rating": "7.7", "image": "https://images.unsplash.com/photo-1535016120720-40c646be5580?auto=format&fit=crop&w=1280&q=80", "poster": "https://images.unsplash.com/photo-1535016120720-40c646be5580?auto=format&fit=crop&w=700&h=1050&q=80", "trailer": "8ugaeA-nMTc", "funciones": {}},
    {"id": 15, "titulo": "Masters of the Universe", "genero": "Ciencia ficción / Aventura", "clasificacion": "PG-13", "duracion": "2h 20m", "director": "Travis Knight", "productor": "Robbie Brenner, Todd Black", "reparto": "Nicholas Galitzine, Camila Mendes, Alison Brie, Jared Leto", "sinopsis": "Prince Adam regresa a Eternia para enfrentar a Skeletor y asumir su destino como He-Man.", "tab": "pronto", "fecha_estreno": "4 junio 2026", "precio_regular": 550, "precio_vip": 900, "rating": "7.6", "image": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?auto=format&fit=crop&w=1280&q=80", "poster": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?auto=format&fit=crop&w=700&h=1050&q=80", "trailer": "KQidFLWXD2Y", "funciones": {}},
    {"id": 16, "titulo": "Animal Farm", "genero": "Animación / Drama", "clasificacion": "PG", "duracion": "1h 35m", "director": "Andy Serkis", "productor": "The Imaginarium", "reparto": "Reparto de voces internacional", "sinopsis": "Una nueva adaptación animada de la clásica fábula política de George Orwell.", "tab": "pronto", "fecha_estreno": "Próximamente", "precio_regular": 500, "precio_vip": 850, "rating": "7.0", "image": "https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=1280&q=80", "poster": "https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=700&h=1050&q=80", "trailer": "rfG63qvqiPA", "funciones": {}},
]

HERO_SLIDES = [movie for movie in MOVIES if movie["tab"] == "cartelera"][:8]

FOOD_MENU = [
    {"id": "f1", "nombre": "Combo Grande", "descripcion": "Palomitas grandes + refresco 44oz", "precio": 380, "image": "https://images.unsplash.com/photo-1585647347483-22b66260dfff?auto=format&fit=crop&w=500&q=80", "qty": 0},
    {"id": "f2", "nombre": "Nachos Premium", "descripcion": "Nachos con queso y jalapeños", "precio": 280, "image": "https://images.unsplash.com/photo-1619881590738-a111d176d906?auto=format&fit=crop&w=500&q=80", "qty": 0},
    {"id": "f3", "nombre": "Hot Dog CXC", "descripcion": "Hot dog grande estilo cine", "precio": 220, "image": "https://images.unsplash.com/photo-1613482084286-41f25b486fa2?auto=format&fit=crop&w=500&q=80", "qty": 0},
    {"id": "f4", "nombre": "Refresco Grande", "descripcion": "Bebida fría 44oz", "precio": 150, "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=80", "qty": 0},
]

def make_seats() -> list[dict]:
    reserved = {"B5", "B6", "C3", "D10", "D11", "F7", "F8", "H4", "H5", "J12", "K9"}
    seats = []
    for row in SEAT_ROWS:
        for col in range(1, 15):
            sid = f"{row}{col}"
            seats.append({"id": sid, "row": row, "tipo": "vip" if row in "KL" else "regular", "estado": "reservado" if sid in reserved else "disponible"})
    return seats

INIT_SEATS = make_seats()

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
        return f"https://www.youtube.com/embed/{self.current_movie.get('trailer', '')}?autoplay=1&rel=0&modestbranding=1"

    @rx.var
    def cartelera_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "cartelera"]
        return movies if not q else [m for m in movies if q in m["titulo"].lower() or q in m["genero"].lower() or q in m["clasificacion"].lower()]

    @rx.var
    def pronto_movies(self) -> list[dict]:
        q = self.search_text.strip().lower()
        movies = [m for m in MOVIES if m["tab"] == "pronto"]
        return movies if not q else [m for m in movies if q in m["titulo"].lower() or q in m["genero"].lower() or q in m["clasificacion"].lower()]

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
                    total += self.current_movie["precio_vip"] if seat["tipo"] == "vip" else self.current_movie["precio_regular"]
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
    def set_location(self, location: str): self.selected_location = location; self.selected_showtime = ""
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
        if self.booking_step == 1 and not self.selected_seats: return
        if self.booking_step < 4: self.booking_step += 1
    def prev_step(self):
        if self.booking_step > 1: self.booking_step -= 1
    def add_food(self, fid: str): self.food_cart = [{**item, "qty": item.get("qty", 0) + 1} if item["id"] == fid else item for item in self.food_cart]
    def remove_food(self, fid: str): self.food_cart = [{**item, "qty": max(0, item.get("qty", 0) - 1)} if item["id"] == fid else item for item in self.food_cart]
    def set_customer_name(self, v: str): self.customer_name = v
    def set_customer_email(self, v: str): self.customer_email = v
    def set_customer_phone(self, v: str): self.customer_phone = v
    def confirm_reservation(self):
        import random
        self.reservation_code = f"CMX-{random.randint(10000, 99999)}"
        self.booking_step = 4

def page_style() -> rx.Component:
    return rx.el.style(f"""
        @import url('{GFONTS}');
        html {{ scroll-behavior: smooth; }}
        body {{ margin: 0; background: #040407; }}
        * {{ box-sizing: border-box; }}
    """)

def money(value) -> rx.Component:
    return rx.hstack(rx.text("RD$", class_name="money"), rx.text(value, class_name="money"), spacing="0", align="center")

def nav_class(active: str, name: str) -> str:
    return "nav-link active-link" if active == name else "nav-link"

def navbar(active: str = "") -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(rx.box("C", class_name="brand-mark"), rx.vstack(rx.text("CINEMAX", class_name="brand-title"), rx.text("CINE PREMIUM", class_name="brand-sub"), spacing="0", align="start"), spacing="3", align="center"),
                href="/", text_decoration="none",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href="/", class_name=nav_class(active, "inicio")),
                rx.link("Cartelera", href="/cartelera", class_name=nav_class(active, "cartelera")),
                rx.link("Próximamente", href="/proximamente", class_name=nav_class(active, "proximamente")),
                rx.link("Ubicaciones", href="/ubicaciones", class_name=nav_class(active, "ubicaciones")),
                rx.link("Boletos", href="/reservar", class_name=nav_class(active, "boletos")),
                spacing="6", class_name="nav-menu",
            ),
            rx.hstack(rx.button("⌕", class_name="nav-icon", on_click=State.toggle_search), rx.button("☰", class_name="nav-icon", on_click=State.toggle_menu), spacing="3"),
            align="center", width="100%",
        ),
        class_name="navbar",
    )

def search_overlay() -> rx.Component:
    return rx.cond(
        State.show_search,
        rx.box(rx.box(rx.hstack(rx.input(placeholder="Buscar película, género o clasificación...", value=State.search_text, on_change=State.set_search_text, class_name="search-input-big"), rx.link(rx.button("Ver cartelera", class_name="btn-primary-sm"), href="/cartelera"), rx.button("✕", class_name="close-btn", on_click=State.close_search), spacing="3", width="100%"), class_name="search-panel"), class_name="overlay"),
        rx.fragment(),
    )

def side_menu() -> rx.Component:
    return rx.cond(
        State.show_menu,
        rx.box(
            rx.box(class_name="menu-backdrop", on_click=State.close_menu),
            rx.vstack(
                rx.hstack(rx.heading("CINEMAX", class_name="drawer-logo"), rx.spacer(), rx.button("✕", class_name="close-btn", on_click=State.close_menu), width="100%"),
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

def hero_thumb(movie: dict, idx: int) -> rx.Component:
    return rx.box(rx.image(src=movie["poster"], class_name="hero-thumb-img"), rx.text(movie["titulo"], class_name="hero-thumb-title"), class_name=rx.cond(State.hero_index == idx, "hero-thumb hero-thumb-active", "hero-thumb"), on_click=lambda: State.go_to_slide(idx))

def hero_section() -> rx.Component:
    return rx.box(
        rx.image(src=State.hero_movie["image"], class_name="hero-bg-img"), rx.box(class_name="hero-layer"), navbar("inicio"),
        rx.button("", id="auto-next-hero", on_click=State.next_hero, style={"display": "none"}),
        rx.script("""(function(){if(window.__cinemaxHeroTimer){clearInterval(window.__cinemaxHeroTimer);} window.__cinemaxHeroTimer=setInterval(function(){const btn=document.getElementById('auto-next-hero'); if(btn){btn.click();}},5000);})();"""),
        rx.grid(
            rx.vstack(rx.text("new", class_name="hero-badge"), rx.heading(State.hero_movie["titulo"], class_name="hero-title"), rx.text(State.hero_movie["sinopsis"], class_name="hero-desc"), rx.hstack(rx.text("Genres:", class_name="meta-label"), rx.text(State.hero_movie["genero"], class_name="meta-text"), rx.text(State.hero_movie["clasificacion"], class_name="age-chip"), spacing="2", wrap="wrap", align="center"), rx.hstack(rx.text("★", class_name="star"), rx.text(State.hero_movie["rating"], class_name="rating"), rx.text("/10", class_name="rating-muted"), spacing="1", align="center"), rx.hstack(rx.button("Comprar ahora", class_name="btn-hero", on_click=State.hero_details), rx.button("Ver trailer", class_name="btn-hero-outline", on_click=State.hero_trailer), spacing="3"), spacing="3", align="start", class_name="hero-info"),
            rx.box(rx.hstack(*[hero_thumb(movie, idx) for idx, movie in enumerate(HERO_SLIDES[:6])], spacing="3", class_name="hero-thumbs"), rx.hstack(rx.button("‹", class_name="carousel-btn", on_click=State.prev_hero), rx.button("›", class_name="carousel-btn", on_click=State.next_hero), spacing="2", class_name="carousel-controls"), class_name="hero-side"),
            columns="2", spacing="0", class_name="hero-grid-layout"),
        class_name="hero")

def movie_card(movie: dict) -> rx.Component:
    return rx.box(rx.box(rx.image(src=movie["poster"], class_name="movie-img"), rx.box(rx.text(movie["clasificacion"], class_name="movie-rating"), class_name="rating-wrap"), rx.box(class_name="movie-img-gradient"), class_name="movie-img-wrap"), rx.box(rx.text(movie["genero"], class_name="movie-genre"), rx.heading(movie["titulo"], class_name="movie-title"), rx.hstack(rx.text(movie["duracion"], class_name="movie-duration"), rx.spacer(), rx.text(movie["fecha_estreno"], class_name="movie-date")), rx.button("Ver detalles", class_name="movie-btn", on_click=lambda: State.go_to_movie(movie["id"])), class_name="movie-body"), class_name="movie-card")

def movie_grid(title: str, movies_var, subtitle: str, active: str) -> rx.Component:
    return rx.box(navbar(active), rx.box(rx.text(subtitle, class_name="section-kicker"), rx.heading(title, class_name="page-title"), rx.grid(rx.foreach(movies_var, movie_card), columns="6", spacing="3", width="100%", class_name="movies-grid"), class_name="page-section page-top"), search_overlay(), side_menu(), class_name="page")

def home_sections() -> rx.Component:
    return rx.box(
        rx.box(rx.hstack(rx.vstack(rx.text("NOW SHOWING", class_name="section-kicker"), rx.heading("Cartelera destacada", class_name="section-title"), spacing="0", align="start"), rx.spacer(), rx.link("Ver cartelera →", href="/cartelera", class_name="view-all"), align="center"), rx.grid(rx.foreach(State.cartelera_movies, movie_card), columns="6", spacing="3", width="100%"), class_name="page-section compact-section"),
        rx.box(rx.hstack(rx.vstack(rx.text("COMING SOON", class_name="section-kicker"), rx.heading("Próximamente", class_name="section-title"), spacing="0", align="start"), rx.spacer(), rx.link("Ver próximas →", href="/proximamente", class_name="view-all"), align="center"), rx.grid(rx.foreach(State.pronto_movies, movie_card), columns="6", spacing="3", width="100%"), class_name="page-section compact-section"),
    )

def location_card(loc: str, data: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(src=data["image"], class_name="location-img"),
            rx.box(class_name="location-img-layer"),
            rx.box("📍", class_name="location-pin"),
            class_name="location-media",
        ),
        rx.box(
            rx.text(data["zona"], class_name="location-zone"),
            rx.heading(loc, class_name="location-title"),
            rx.text(data["salas"], class_name="location-text"),
            rx.hstack(
                rx.text("2D", class_name="location-chip"),
                rx.text("CXC", class_name="location-chip"),
                rx.text("VIP", class_name="location-chip"),
                spacing="2",
                wrap="wrap",
            ),
            rx.link(
                rx.button("Abrir ubicación", class_name="btn-primary-sm location-btn"),
                href=data["map"],
                is_external=True,
                width="100%",
            ),
            class_name="location-body",
        ),
        class_name="location-card",
    )

def locations_page() -> rx.Component:
    return rx.box(
        navbar("ubicaciones"),
        rx.box(
            rx.text("CINES DISPONIBLES", class_name="section-kicker"),
            rx.heading("Ubicaciones", class_name="page-title locations-title"),
            rx.text("Selecciona el cine más cercano y abre su ubicación directamente en Google Maps.", class_name="locations-subtitle"),
            rx.grid(*[location_card(loc, LOCATION_DETAILS[loc]) for loc in LOCATIONS], columns="5", spacing="3", width="100%"),
            class_name="page-section page-top locations-section",
        ),
        search_overlay(),
        side_menu(),
        class_name="page",
    )

def loc_button(loc: str) -> rx.Component:
    return rx.button(loc, class_name=rx.cond(State.selected_location == loc, "pill pill-active", "pill"), on_click=lambda: State.set_location(loc))
def date_button(date: str) -> rx.Component:
    return rx.button(date, class_name=rx.cond(State.selected_date == date, "pill pill-active", "pill"), on_click=lambda: State.set_date(date))
def showtime_button(t: str) -> rx.Component:
    return rx.button(t, class_name=rx.cond(State.selected_showtime == t, "showtime showtime-active", "showtime"), on_click=lambda: State.set_showtime(t))

def detail_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(rx.image(src=State.current_movie["image"], class_name="detail-bg"), rx.box(class_name="detail-overlay"), rx.grid(rx.box(rx.image(src=State.current_movie["poster"], class_name="detail-poster"), class_name="detail-poster-wrap"), rx.vstack(rx.text(State.current_movie["fecha_estreno"], class_name="section-kicker"), rx.heading(State.current_movie["titulo"], class_name="detail-title"), rx.hstack(rx.text(State.current_movie["genero"], class_name="detail-chip"), rx.text(State.current_movie["clasificacion"], class_name="detail-chip"), rx.text(State.current_movie["duracion"], class_name="detail-chip"), spacing="2", wrap="wrap"), rx.text(State.current_movie["sinopsis"], class_name="detail-desc"), rx.hstack(rx.text("Director:", class_name="detail-label"), rx.text(State.current_movie["director"], class_name="detail-value")), rx.hstack(rx.text("Reparto:", class_name="detail-label"), rx.text(State.current_movie["reparto"], class_name="detail-value")), rx.hstack(rx.button("Ver trailer", class_name="btn-primary-sm", on_click=State.open_trailer), rx.button("Ocultar trailer", class_name="btn-ghost", on_click=State.close_trailer), spacing="2"), rx.cond(State.show_trailer, rx.box(rx.el.iframe(src=State.trailer_url, class_name="trailer-frame", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", allowfullscreen=True), class_name="trailer-box"), rx.box(rx.image(src=State.current_movie["image"], class_name="trailer-placeholder-img"), rx.box("Presiona “Ver trailer” para cargar el video aquí mismo.", class_name="trailer-placeholder-text"), class_name="trailer-placeholder")), spacing="3", align="start", class_name="detail-info"), columns="2", spacing="6", class_name="detail-grid"), class_name="detail-hero"),
        showtimes_section(), search_overlay(), side_menu(), class_name="page")

def showtimes_section() -> rx.Component:
    return rx.box(rx.box(rx.text("FUNCIONES", class_name="section-kicker"), rx.heading("Elige cine, fecha y horario", class_name="section-title"), rx.text("Selecciona una función para continuar al mapa de asientos.", class_name="muted"), rx.text("Ubicación", class_name="block-label"), rx.hstack(rx.foreach(LOCATIONS, loc_button), spacing="2", wrap="wrap"), rx.text("Fecha", class_name="block-label"), rx.hstack(rx.foreach(DATES, date_button), spacing="2", wrap="wrap"), rx.text("Horarios disponibles", class_name="block-label"), rx.hstack(rx.foreach(State.showtimes, showtime_button), spacing="2", wrap="wrap"), rx.button("Continuar a asientos", class_name="btn-primary-lg", on_click=State.start_booking), class_name="page-section showtimes-card"))

def seat_button(seat: dict) -> rx.Component:
    return rx.button(seat["id"], class_name=rx.cond(State.selected_seats.contains(seat["id"]), "seat seat-selected", rx.cond(seat["estado"] == "reservado", "seat seat-reserved", rx.cond(seat["tipo"] == "vip", "seat seat-vip", "seat"))), on_click=lambda: State.toggle_seat(seat["id"]))

def seat_row(label: str, seats_var) -> rx.Component:
    return rx.hstack(rx.text(label, class_name="row-label"), rx.foreach(seats_var, seat_button), spacing="1", class_name="seat-row")

def seat_map() -> rx.Component:
    return rx.box(rx.text("PANTALLA CXC", class_name="screen-label"), rx.box(class_name="screen"), rx.vstack(seat_row("A", State.row_A), seat_row("B", State.row_B), seat_row("C", State.row_C), seat_row("D", State.row_D), seat_row("E", State.row_E), seat_row("F", State.row_F), seat_row("G", State.row_G), seat_row("H", State.row_H), seat_row("I", State.row_I), seat_row("J", State.row_J), seat_row("K", State.row_K), seat_row("L", State.row_L), spacing="2", class_name="seat-map"), rx.hstack(rx.hstack(rx.box(class_name="legend-dot dot-available"), rx.text("Disponible", class_name="legend-text")), rx.hstack(rx.box(class_name="legend-dot dot-selected"), rx.text("Seleccionado", class_name="legend-text")), rx.hstack(rx.box(class_name="legend-dot dot-reserved"), rx.text("Reservado", class_name="legend-text")), rx.hstack(rx.box(class_name="legend-dot dot-vip"), rx.text("VIP", class_name="legend-text")), spacing="4", wrap="wrap", class_name="legend"), class_name="seat-card")

def food_card(item: dict) -> rx.Component:
    return rx.hstack(rx.image(src=item["image"], class_name="food-img"), rx.vstack(rx.heading(item["nombre"], class_name="food-title"), rx.text(item["descripcion"], class_name="food-desc"), money(item["precio"]), spacing="1", align="start"), rx.spacer(), rx.hstack(rx.button("−", class_name="qty-btn", on_click=lambda: State.remove_food(item["id"])), rx.text(item["qty"], class_name="qty-text"), rx.button("+", class_name="qty-btn", on_click=lambda: State.add_food(item["id"])), spacing="2", align="center"), class_name="food-card")

def food_section() -> rx.Component:
    return rx.box(rx.text("COMIDA Y BEBIDAS", class_name="block-label"), rx.grid(rx.foreach(State.food_cart, food_card), columns="2", spacing="3", width="100%"), class_name="food-section")

def invoice() -> rx.Component:
    return rx.box(rx.heading("Factura", class_name="invoice-title"), rx.text(State.current_movie["titulo"], class_name="invoice-movie"), rx.text(State.selected_location, class_name="invoice-muted"), rx.hstack(rx.text(State.selected_date, class_name="invoice-muted"), rx.text("·", class_name="invoice-muted"), rx.text(State.selected_showtime, class_name="invoice-muted"), spacing="1"), rx.divider(border_color="rgba(255,255,255,.10)"), rx.hstack(rx.text("Asientos", class_name="invoice-line"), rx.spacer(), rx.text(State.selected_seats_text, class_name="invoice-line")), rx.hstack(rx.text("Boletos", class_name="invoice-line"), rx.spacer(), money(State.total_boletos)), rx.hstack(rx.text("Comida", class_name="invoice-line"), rx.spacer(), money(State.total_comida)), rx.hstack(rx.text("Cargo servicio", class_name="invoice-line"), rx.spacer(), money(State.cargo_servicio)), rx.divider(border_color="rgba(255,255,255,.10)"), rx.hstack(rx.text("Total", class_name="invoice-total-label"), rx.spacer(), money(State.gran_total)), rx.cond(State.booking_step == 1, rx.button("Siguiente: comida", class_name="checkout-btn", on_click=State.next_step), rx.cond(State.booking_step == 2, rx.button("Siguiente: datos", class_name="checkout-btn", on_click=State.next_step), rx.cond(State.booking_step == 3, rx.button("Confirmar reserva", class_name="checkout-btn", on_click=State.confirm_reservation), rx.button("Reserva creada", class_name="checkout-btn")))), rx.button("Volver", class_name="btn-ghost full", on_click=State.prev_step), class_name="invoice")

def customer_form() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box("👤", class_name="form-icon"),
            rx.vstack(
                rx.text("DATOS DE RESERVA", class_name="block-label"),
                rx.text("Completa tus datos para generar el código de reserva.", class_name="form-subtitle"),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
            class_name="form-header",
        ),
        rx.grid(
            rx.input(placeholder="Nombre completo", value=State.customer_name, on_change=State.set_customer_name, class_name="form-input"),
            rx.input(placeholder="Correo electrónico", value=State.customer_email, on_change=State.set_customer_email, class_name="form-input"),
            rx.input(placeholder="Teléfono", value=State.customer_phone, on_change=State.set_customer_phone, class_name="form-input"),
            rx.box(
                rx.text("Método de pago", class_name="payment-label"),
                rx.text("Pago en taquilla", class_name="payment-value"),
                class_name="payment-card",
            ),
            columns="2",
            spacing="3",
            width="100%",
            class_name="form-grid",
        ),
        class_name="form-card",
    )

def confirmation() -> rx.Component:
    return rx.box(rx.text("✅", class_name="confirm-icon"), rx.heading("Reserva confirmada", class_name="confirm-title"), rx.text("Tu código de reserva es:", class_name="muted"), rx.text(State.reservation_code, class_name="reservation-code"), rx.text("Presenta este código en taquilla para completar el pago.", class_name="muted"), rx.link(rx.button("Volver al inicio", class_name="btn-primary-lg"), href="/"), class_name="confirm-card")

def booking_page() -> rx.Component:
    return rx.box(navbar("boletos"), rx.grid(rx.box(rx.hstack(rx.box("1", class_name=rx.cond(State.booking_step == 1, "step step-active", "step")), rx.box("2", class_name=rx.cond(State.booking_step == 2, "step step-active", "step")), rx.box("3", class_name=rx.cond(State.booking_step == 3, "step step-active", "step")), rx.box("4", class_name=rx.cond(State.booking_step == 4, "step step-active", "step")), spacing="2", class_name="steps"), rx.cond(State.booking_step == 1, seat_map(), rx.cond(State.booking_step == 2, food_section(), rx.cond(State.booking_step == 3, customer_form(), confirmation()))), class_name="booking-main"), invoice(), columns="2", spacing="4", class_name="booking-layout"), search_overlay(), side_menu(), class_name="page")

def index() -> rx.Component:
    return rx.box(page_style(), hero_section(), home_sections(), search_overlay(), side_menu(), class_name="page")
def cartelera() -> rx.Component:
    return movie_grid("Películas en cartelera", State.cartelera_movies, "NOW SHOWING", "cartelera")
def proximamente() -> rx.Component:
    return movie_grid("Próximamente", State.pronto_movies, "COMING SOON", "proximamente")

app = rx.App(stylesheets=["/style.css"])
app.add_page(index, route="/", title="CineMax")
app.add_page(cartelera, route="/cartelera", title="CineMax | Cartelera")
app.add_page(proximamente, route="/proximamente", title="CineMax | Próximamente")
app.add_page(locations_page, route="/ubicaciones", title="CineMax | Ubicaciones")
app.add_page(detail_page, route="/pelicula", title="CineMax | Detalle")
app.add_page(booking_page, route="/reservar", title="CineMax | Reservar")
