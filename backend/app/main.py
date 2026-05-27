from fastapi import FastAPI
from app.routes import peliculas, funciones

app = FastAPI()

app.include_router(peliculas.router)
app.include_router(funciones.router)

@app.get("/")
def home():
    return {"mensaje": "API de cine funcionando"}