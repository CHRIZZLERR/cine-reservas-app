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

@router.get("/peliculas/{pelicula_id}")
def obtener_pelicula_por_id(pelicula_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM peliculas
        WHERE id = %s
    """, (pelicula_id,))

    pelicula = cursor.fetchone()

    conexion.close()

    if pelicula is None:
        return {"error": "La película no existe"}

    return pelicula

@router.get("/peliculas/{pelicula_id}/funciones")
def obtener_funciones_por_pelicula(pelicula_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.id,
            f.pelicula_id,
            f.sucursal_id,
            f.fecha,
            CAST(f.hora AS CHAR) AS hora,
            f.sala,
            f.precio,
            p.titulo AS pelicula,
            p.genero,
            p.clasificacion,
            s.nombre AS sucursal,
            s.direccion AS direccion_sucursal,
            s.ciudad
        FROM funciones f
        INNER JOIN peliculas p ON f.pelicula_id = p.id
        INNER JOIN sucursales s ON f.sucursal_id = s.id
        WHERE p.id = %s
    """, (pelicula_id,))

    funciones = cursor.fetchall()

    conexion.close()
    return funciones