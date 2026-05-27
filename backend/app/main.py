from fastapi import FastAPI
from app.routes import peliculas, funciones, reservas

app = FastAPI()

app.include_router(peliculas.router)
app.include_router(funciones.router)
app.include_router(reservas.router)

@app.get("/")
def home():
    return {"mensaje": "API de cine funcionando"}