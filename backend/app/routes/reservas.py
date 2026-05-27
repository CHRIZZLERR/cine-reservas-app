from fastapi import APIRouter
from app.database.conexion import obtener_conexion

router = APIRouter()

@router.get("/reservas")
def obtener_reservas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id,
            r.nombre_cliente,
            r.email_cliente,
            r.cantidad_asientos,
            r.total,
            r.fecha_reserva,
            p.titulo AS pelicula,
            f.fecha,
            f.hora,
            f.sala
        FROM reservas r
        INNER JOIN funciones f ON r.funcion_id = f.id
        INNER JOIN peliculas p ON f.pelicula_id = p.id
    """)

    reservas = cursor.fetchall()
    conexion.close()

    return reservas