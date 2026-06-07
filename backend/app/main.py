from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import peliculas
from app.routes import funciones
from app.routes import reservas
from app.routes import sucursales
from app.routes import tmdb
from app.routes import auth


tags_metadata = [
    {
        "name": "Películas",
        "description": "Rutas públicas y administrativas para gestionar películas.",
    },
    {
        "name": "Funciones",
        "description": "Rutas para horarios, salas, fechas y precios de funciones.",
    },
    {
        "name": "Reservas",
        "description": "Rutas para crear, consultar y administrar reservas.",
    },
    {
        "name": "Sucursales",
        "description": "Rutas para consultar y administrar cines o ubicaciones.",
    },
    {
        "name": "TMDB",
        "description": "Rutas para buscar e importar películas desde TMDB.",
    },
    {
        "name": "Autenticación",
        "description": "Rutas para login, registro y administración de usuarios.",
    },
    {
        "name": "Sistema",
        "description": "Ruta principal para verificar que la API está funcionando.",
    },
]


app = FastAPI(
    title="JC Cinemas API",
    description="API para la plataforma de reservas de cine JC Cinemas",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(peliculas.router, tags=["Películas"])
app.include_router(funciones.router, tags=["Funciones"])
app.include_router(reservas.router, tags=["Reservas"])
app.include_router(sucursales.router, tags=["Sucursales"])
app.include_router(tmdb.router, tags=["TMDB"])
app.include_router(auth.router, tags=["Autenticación"])


@app.get("/", tags=["Sistema"])
def home():
    return {
        "mensaje": "API de JC Cinemas funcionando correctamente",
        "estado": "online",
    }