from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import peliculas
from app.routes import funciones
from app.routes import reservas
from app.routes import sucursales
from app.routes import tmdb
from app.routes import auth

app = FastAPI(
    title="JC Cinemas API",
    description="API para la plataforma de reservas de cine JC Cinemas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(peliculas.router)
app.include_router(funciones.router)
app.include_router(reservas.router)
app.include_router(sucursales.router)
app.include_router(tmdb.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "mensaje": "API de JC Cinemas funcionando correctamente",
        "estado": "online"
    }