from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.database.conexion import obtener_conexion

router = APIRouter()

class ReservaCrear(BaseModel):
    funcion_id: int
    nombre_cliente: str
    email_cliente: str
    cantidad_asientos: int = Field(ge=1, le=10)

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

@router.post("/reservas")
def crear_reserva(reserva: ReservaCrear):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT precio FROM funciones WHERE id = %s",
        (reserva.funcion_id,)
    )

    funcion = cursor.fetchone()

    if funcion is None:
        conexion.close()
        return {"error": "La función no existe"}

    total = float(funcion["precio"]) * reserva.cantidad_asientos

    cursor.execute("""
        INSERT INTO reservas
        (funcion_id, nombre_cliente, email_cliente, cantidad_asientos, total)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        reserva.funcion_id,
        reserva.nombre_cliente,
        reserva.email_cliente,
        reserva.cantidad_asientos,
        total
    ))

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Reserva creada correctamente",
        "total": total
    }