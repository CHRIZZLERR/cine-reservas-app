from fastapi import APIRouter
from app.database.conexion import obtener_conexion

router = APIRouter()

@router.get("/funciones")
def obtener_funciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            f.id,
            f.fecha,
            f.hora,
            f.sala,
            f.precio,
            p.titulo AS pelicula,
            p.genero,
            p.clasificacion
        FROM funciones f
        INNER JOIN peliculas p ON f.pelicula_id = p.id
    """)

    funciones = cursor.fetchall()
    conexion.close()

    return funciones