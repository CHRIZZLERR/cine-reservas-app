from fastapi import APIRouter, HTTPException
from app.database.conexion import obtener_conexion

router = APIRouter()


@router.get("/sucursales")
def obtener_sucursales():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            direccion,
            ciudad,
            activa
        FROM sucursales
        WHERE activa = TRUE
        ORDER BY nombre
    """)

    sucursales = cursor.fetchall()

    conexion.close()
    return sucursales


@router.get("/admin/sucursales")
def obtener_sucursales_admin():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            direccion,
            ciudad,
            activa
        FROM sucursales
        ORDER BY nombre
    """)

    sucursales = cursor.fetchall()

    conexion.close()
    return sucursales


@router.get("/sucursales/{sucursal_id}")
def obtener_sucursal_por_id(sucursal_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            direccion,
            ciudad,
            activa
        FROM sucursales
        WHERE id = %s
    """, (sucursal_id,))

    sucursal = cursor.fetchone()

    conexion.close()

    if sucursal is None:
        raise HTTPException(status_code=404, detail="La sucursal no existe")

    return sucursal