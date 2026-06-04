# =============================================================
# CineMax / CineHub · data.py
# Datos estáticos del frontend.
# =============================================================

SERVICE_FEE = 45

LOCATIONS = [
    "Downtown Center",
    "Galería 360",
    "Ágora Mall",
    "Blue Mall",
    "Sambil",
]

LOCATION_DETAILS = {
    "Downtown Center": {
        "zona": "Av. Núñez de Cáceres, Santo Domingo",
        "salas": "Salas 2D, VIP, dulcería premium y estrenos principales.",
        "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Downtown+Center+Santo+Domingo",
    },
    "Galería 360": {
        "zona": "Av. John F. Kennedy, Santo Domingo",
        "salas": "Cine moderno, parqueo cómodo y funciones familiares.",
        "image": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Galeria+360+Santo+Domingo",
    },
    "Ágora Mall": {
        "zona": "Av. Abraham Lincoln, Santo Domingo",
        "salas": "Ubicación céntrica, salas cómodas y experiencia premium.",
        "image": "https://images.unsplash.com/photo-1533488765986-dfa2a9939acd?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Agora+Mall+Santo+Domingo",
    },
    "Blue Mall": {
        "zona": "Av. Winston Churchill, Santo Domingo",
        "salas": "Ambiente ejecutivo, salas VIP y estrenos destacados.",
        "image": "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Blue+Mall+Santo+Domingo",
    },
    "Sambil": {
        "zona": "Av. John F. Kennedy, Santo Domingo",
        "salas": "Funciones para todos, dulcería y experiencia familiar.",
        "image": "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=900&q=80",
        "map": "https://www.google.com/maps/search/?api=1&query=Sambil+Santo+Domingo",
    },
}

DATES = [
    "Hoy · Vie 29",
    "Sáb 30",
    "Dom 31",
    "Lun 01",
    "Mar 02",
    "Mié 03",
]

SEAT_ROWS = list("ABCDEFGHIJKL")


def poster_url(title: str, color: str) -> str:
    clean = title.replace(" ", "+")
    return f"https://dummyimage.com/700x1050/{color}/ffffff.png&text={clean}"


def backdrop_url(title: str, color: str) -> str:
    clean = title.replace(" ", "+")
    return f"https://dummyimage.com/1280x720/{color}/ffffff.png&text={clean}"


MOVIES = [
    {
        "id": 1,
        "titulo": "Mortal Kombat II",
        "genero": "Acción / Fantasía",
        "clasificacion": "R/18",
        "duracion": "1h 56m",
        "director": "Simon McQuoid",
        "productor": "Todd Garner, James Wan",
        "reparto": "Karl Urban, Adeline Rudolph, Jessica McNamee, Hiroyuki Sanada",
        "sinopsis": "Los campeones favoritos de los fans se enfrentan en una batalla definitiva para detener el dominio de Shao Kahn.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 500,
        "precio_vip": 850,
        "rating": "7.4",
        "image": backdrop_url("Mortal Kombat II", "111827"),
        "poster": poster_url("Mortal Kombat II", "111827"),
        "trailer": "b24oG7qCwp4",
        "funciones": {
            "Downtown Center": ["4:20 PM", "6:55 PM", "8:35 PM", "9:30 PM"],
            "Galería 360": ["3:45 PM", "6:20 PM", "9:10 PM"],
            "Ágora Mall": ["5:00 PM", "7:30 PM", "10:00 PM"],
            "Blue Mall": ["6:15 PM", "9:20 PM"],
            "Sambil": ["4:40 PM", "7:10 PM", "9:55 PM"],
        },
    },
    {
        "id": 2,
        "titulo": "F1: La Película",
        "genero": "Acción / Drama",
        "clasificacion": "PG-13",
        "duracion": "2h 25m",
        "director": "Joseph Kosinski",
        "productor": "Jerry Bruckheimer",
        "reparto": "Brad Pitt, Damson Idris, Kerry Condon, Javier Bardem",
        "sinopsis": "Un expiloto de Fórmula 1 regresa a las pistas para guiar a un joven talento hacia la gloria.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 550,
        "precio_vip": 900,
        "rating": "8.1",
        "image": backdrop_url("F1 La Película", "0f172a"),
        "poster": poster_url("F1 La Película", "0f172a"),
        "trailer": "IHWlvwu8t1w",
        "funciones": {
            "Downtown Center": ["2:30 PM", "5:00 PM", "7:30 PM", "10:00 PM"],
            "Galería 360": ["3:00 PM", "6:00 PM", "8:30 PM"],
            "Ágora Mall": ["4:00 PM", "7:00 PM", "9:45 PM"],
            "Blue Mall": ["5:30 PM", "8:30 PM"],
            "Sambil": ["2:00 PM", "4:50 PM", "7:40 PM"],
        },
    },
    {
        "id": 3,
        "titulo": "Jurassic World: El Renacimiento",
        "genero": "Aventura / Ciencia ficción",
        "clasificacion": "PG-13",
        "duracion": "2h 01m",
        "director": "Gareth Edwards",
        "productor": "Frank Marshall",
        "reparto": "Scarlett Johansson, Jonathan Bailey, Mahershala Ali",
        "sinopsis": "Una nueva expedición entra en una zona prohibida donde los dinosaurios todavía dominan la Tierra.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 500,
        "precio_vip": 850,
        "rating": "7.3",
        "image": backdrop_url("Jurassic World", "0b2414"),
        "poster": poster_url("Jurassic World", "0b2414"),
        "trailer": "XJ0uv-phsDk",
        "funciones": {
            "Downtown Center": ["3:15 PM", "6:05 PM", "9:00 PM"],
            "Galería 360": ["4:15 PM", "7:05 PM", "10:00 PM"],
            "Ágora Mall": ["5:30 PM", "8:30 PM"],
            "Blue Mall": ["6:45 PM", "9:45 PM"],
            "Sambil": ["5:20 PM", "8:50 PM"],
        },
    },
    {
        "id": 4,
        "titulo": "Ballerina",
        "genero": "Acción / Thriller",
        "clasificacion": "R",
        "duracion": "1h 53m",
        "director": "Len Wiseman",
        "productor": "Basil Iwanyk",
        "reparto": "Ana de Armas, Keanu Reeves, Ian McShane",
        "sinopsis": "Una asesina entrenada busca venganza dentro del oscuro universo de los asesinos profesionales.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 500,
        "precio_vip": 850,
        "rating": "7.0",
        "image": backdrop_url("Ballerina", "1f1117"),
        "poster": poster_url("Ballerina", "1f1117"),
        "trailer": "dQw4w9WgXcQ",
        "funciones": {
            "Downtown Center": ["4:50 PM", "7:10 PM", "9:30 PM"],
            "Galería 360": ["6:00 PM", "8:30 PM"],
            "Ágora Mall": ["5:40 PM", "8:45 PM"],
            "Blue Mall": ["7:20 PM", "9:40 PM"],
            "Sambil": ["5:30 PM", "8:25 PM"],
        },
    },
    {
        "id": 5,
        "titulo": "De tal palo, tal astilla",
        "genero": "Comedia Dominicana",
        "clasificacion": "R/12",
        "duracion": "1h 25m",
        "director": "Frank Perozo",
        "productor": "Caribbean Films",
        "reparto": "Raymond Pozo, Miguel Céspedes, Hony Estrella",
        "sinopsis": "Una comedia dominicana llena de enredos, secretos familiares y situaciones inesperadas.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 450,
        "precio_vip": 800,
        "rating": "7.3",
        "image": backdrop_url("De tal palo tal astilla", "3b0a0a"),
        "poster": poster_url("De tal palo tal astilla", "3b0a0a"),
        "trailer": "JHif2sq226E",
        "funciones": {
            "Downtown Center": ["5:25 PM", "7:35 PM", "9:35 PM"],
            "Galería 360": ["4:30 PM", "7:10 PM", "9:20 PM"],
            "Ágora Mall": ["5:00 PM", "7:30 PM"],
            "Blue Mall": ["6:40 PM", "8:55 PM"],
            "Sambil": ["5:40 PM", "8:10 PM", "10:00 PM"],
        },
    },
    {
        "id": 6,
        "titulo": "Star Wars: The Mandalorian and Grogu",
        "genero": "Acción / Aventura",
        "clasificacion": "R/14",
        "duracion": "2h 20m",
        "director": "Jon Favreau",
        "productor": "Dave Filoni, Kathleen Kennedy",
        "reparto": "Pedro Pascal, Sigourney Weaver, Jeremy Allen White",
        "sinopsis": "La Nueva República recluta al Mandaloriano Din Djarin y a Grogu para proteger lo que la Rebelión luchó por construir.",
        "tab": "cartelera",
        "fecha_estreno": "En cartelera",
        "precio_regular": 550,
        "precio_vip": 900,
        "rating": "8.1",
        "image": backdrop_url("Mandalorian Grogu", "0a0a1a"),
        "poster": poster_url("Mandalorian Grogu", "0a0a1a"),
        "trailer": "IHWlvwu8t1w",
        "funciones": {
            "Downtown Center": ["3:30 PM", "6:25 PM", "9:20 PM"],
            "Galería 360": ["3:00 PM", "6:00 PM", "9:00 PM"],
            "Ágora Mall": ["4:20 PM", "7:20 PM"],
            "Blue Mall": ["5:10 PM", "8:15 PM"],
            "Sambil": ["3:50 PM", "6:40 PM", "9:40 PM"],
        },
    },
    {
        "id": 7,
        "titulo": "Superman",
        "genero": "Acción / Superhéroes",
        "clasificacion": "PG-13",
        "duracion": "2h 10m",
        "director": "James Gunn",
        "productor": "Peter Safran",
        "reparto": "David Corenswet, Rachel Brosnahan, Nicholas Hoult",
        "sinopsis": "Clark Kent intenta equilibrar su herencia kryptoniana con su vida humana mientras nace un nuevo símbolo de esperanza.",
        "tab": "proximamente",
        "fecha_estreno": "Próximamente",
        "precio_regular": 550,
        "precio_vip": 900,
        "rating": "7.8",
        "image": backdrop_url("Superman", "0a1933"),
        "poster": poster_url("Superman", "0a1933"),
        "trailer": "8ugaeA-nMTc",
        "funciones": {},
    },
    {
        "id": 8,
        "titulo": "Toy Story 5",
        "genero": "Animación / Familiar",
        "clasificacion": "G",
        "duracion": "1h 42m",
        "director": "Andrew Stanton",
        "productor": "Pixar Animation Studios",
        "reparto": "Tom Hanks, Tim Allen, Joan Cusack",
        "sinopsis": "Los juguetes enfrentan una nueva etapa donde la tecnología cambia el tiempo de juego.",
        "tab": "proximamente",
        "fecha_estreno": "Próximamente",
        "precio_regular": 500,
        "precio_vip": 850,
        "rating": "7.9",
        "image": backdrop_url("Toy Story 5", "0f3d91"),
        "poster": poster_url("Toy Story 5", "0f3d91"),
        "trailer": "wmiIUN-7qhE",
        "funciones": {},
    },
]

HERO_SLIDES = [movie for movie in MOVIES if movie["tab"] == "cartelera"]

FOOD_MENU = [
    {
        "id": "f1",
        "nombre": "Combo Grande",
        "descripcion": "Palomitas grandes + refresco 44oz",
        "precio": 380,
        "image": "https://dummyimage.com/500x350/7f1d1d/ffffff.png&text=Combo+Grande",
        "qty": 0,
    },
    {
        "id": "f2",
        "nombre": "Nachos Premium",
        "descripcion": "Nachos con queso y jalapeños",
        "precio": 280,
        "image": "https://dummyimage.com/500x350/92400e/ffffff.png&text=Nachos",
        "qty": 0,
    },
    {
        "id": "f3",
        "nombre": "Hot Dog Cine",
        "descripcion": "Hot dog grande estilo cine",
        "precio": 220,
        "image": "https://dummyimage.com/500x350/7c2d12/ffffff.png&text=Hot+Dog",
        "qty": 0,
    },
    {
        "id": "f4",
        "nombre": "Refresco Grande",
        "descripcion": "Bebida fría 44oz",
        "precio": 150,
        "image": "https://dummyimage.com/500x350/1d4ed8/ffffff.png&text=Refresco",
        "qty": 0,
    },
]


def make_seats() -> list[dict]:
    reserved = {"B5", "B6", "C3", "D10", "D11", "F7", "F8", "H4", "H5", "J12", "K9"}
    seats = []

    for row in SEAT_ROWS:
        for col in range(1, 15):
            seat_id = f"{row}{col}"

            seats.append(
                {
                    "id": seat_id,
                    "row": row,
                    "col": col,
                    "tipo": "vip" if row in "KL" else "regular",
                    "estado": "reservado" if seat_id in reserved else "disponible",
                }
            )

    return seats


INIT_SEATS = make_seats()
