from fastapi import APIRouter
from app.database.conexion import obtener_conexion

router = APIRouter()

@router.get("/peliculas")
def obtener_peliculas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()

    conexion.close()

    return peliculas