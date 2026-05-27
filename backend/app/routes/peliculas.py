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

@router.get("/peliculas/{pelicula_id}/funciones")
def obtener_funciones_por_pelicula(pelicula_id: int):
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
        WHERE p.id = %s
    """, (pelicula_id,))

    funciones = cursor.fetchall()

    conexion.close()
    return funciones