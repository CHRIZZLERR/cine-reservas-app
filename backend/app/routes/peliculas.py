from fastapi import APIRouter

router = APIRouter()

@router.get("/peliculas")
def obtener_peliculas():
    return [
        {"id": 1, "titulo": "Avengers", "genero": "Accion"},
        {"id": 2, "titulo": "Batman", "genero": "Accion"},
    ]