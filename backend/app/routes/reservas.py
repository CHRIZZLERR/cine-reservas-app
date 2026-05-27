from fastapi import APIRouter
from app.database.conexion import obtener_conexion

router = APIRouter()

@router.get("/reservas")
def obtener_reservas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()

    conexion.close()

    return reservas