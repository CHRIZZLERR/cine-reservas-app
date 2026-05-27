from fastapi import APIRouter
from app.database.conexion import obtener_conexion

router = APIRouter()

@router.get("/funciones")
def obtener_funciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM funciones")
    funciones = cursor.fetchall()

    conexion.close()

    return funciones