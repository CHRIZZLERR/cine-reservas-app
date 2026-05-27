from fastapi import FastAPI
from app.routes import peliculas

app = FastAPI()

app.include_router(peliculas.router)

@app.get("/")
def home():
    return {"mensaje": "API de cine funcionando"}