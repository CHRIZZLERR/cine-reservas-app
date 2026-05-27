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
    """)

    funciones = cursor.fetchall()
    conexion.close()
    return funciones