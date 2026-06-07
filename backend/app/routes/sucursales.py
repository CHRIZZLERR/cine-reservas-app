from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.conexion import obtener_conexion

router = APIRouter()


class SucursalCreate(BaseModel):
    nombre: str
    direccion: str
    ciudad: str


class SucursalUpdate(BaseModel):
    nombre: str
    direccion: str
    ciudad: str
    activa: bool = True


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
        ORDER BY nombre ASC
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
        ORDER BY id DESC
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


@router.post("/admin/sucursales")
def crear_sucursal(sucursal: SucursalCreate):
    nombre = sucursal.nombre.strip()
    direccion = sucursal.direccion.strip()
    ciudad = sucursal.ciudad.strip()

    if not nombre:
        raise HTTPException(status_code=400, detail="El nombre de la sucursal es obligatorio")

    if not direccion:
        raise HTTPException(status_code=400, detail="La dirección de la sucursal es obligatoria")

    if not ciudad:
        raise HTTPException(status_code=400, detail="La ciudad de la sucursal es obligatoria")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id
            FROM sucursales
            WHERE LOWER(nombre) = LOWER(%s)
            AND LOWER(ciudad) = LOWER(%s)
            LIMIT 1
        """, (nombre, ciudad))

        sucursal_existente = cursor.fetchone()

        if sucursal_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una sucursal con ese nombre en esa ciudad"
            )

        cursor.execute("""
            INSERT INTO sucursales
            (nombre, direccion, ciudad, activa)
            VALUES (%s, %s, %s, TRUE)
        """, (
            nombre,
            direccion,
            ciudad
        ))

        conexion.commit()

        sucursal_id = cursor.lastrowid

        return {
            "mensaje": "Sucursal creada correctamente",
            "id": sucursal_id,
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "activa": True
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear sucursal: {str(error)}")

    finally:
        conexion.close()


@router.put("/admin/sucursales/{sucursal_id}")
def actualizar_sucursal(sucursal_id: int, sucursal: SucursalUpdate):
    nombre = sucursal.nombre.strip()
    direccion = sucursal.direccion.strip()
    ciudad = sucursal.ciudad.strip()

    if not nombre:
        raise HTTPException(status_code=400, detail="El nombre de la sucursal es obligatorio")

    if not direccion:
        raise HTTPException(status_code=400, detail="La dirección de la sucursal es obligatoria")

    if not ciudad:
        raise HTTPException(status_code=400, detail="La ciudad de la sucursal es obligatoria")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id
            FROM sucursales
            WHERE id = %s
        """, (sucursal_id,))

        sucursal_actual = cursor.fetchone()

        if sucursal_actual is None:
            raise HTTPException(status_code=404, detail="La sucursal no existe")

        cursor.execute("""
            SELECT id
            FROM sucursales
            WHERE LOWER(nombre) = LOWER(%s)
            AND LOWER(ciudad) = LOWER(%s)
            AND id <> %s
            LIMIT 1
        """, (nombre, ciudad, sucursal_id))

        sucursal_repetida = cursor.fetchone()

        if sucursal_repetida is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe otra sucursal con ese nombre en esa ciudad"
            )

        cursor.execute("""
            UPDATE sucursales
            SET
                nombre = %s,
                direccion = %s,
                ciudad = %s,
                activa = %s
            WHERE id = %s
        """, (
            nombre,
            direccion,
            ciudad,
            sucursal.activa,
            sucursal_id
        ))

        conexion.commit()

        return {
            "mensaje": "Sucursal actualizada correctamente",
            "id": sucursal_id,
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "activa": sucursal.activa
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar sucursal: {str(error)}")

    finally:
        conexion.close()


@router.delete("/admin/sucursales/{sucursal_id}")
def desactivar_sucursal(sucursal_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                nombre,
                activa
            FROM sucursales
            WHERE id = %s
        """, (sucursal_id,))

        sucursal = cursor.fetchone()

        if sucursal is None:
            raise HTTPException(status_code=404, detail="La sucursal no existe")

        cursor.execute("""
            SELECT COUNT(*) AS total_funciones
            FROM funciones
            WHERE sucursal_id = %s
        """, (sucursal_id,))

        total_funciones = cursor.fetchone()["total_funciones"]

        nueva_activa = not bool(sucursal["activa"])

        cursor.execute("""
            UPDATE sucursales
            SET activa = %s
            WHERE id = %s
        """, (nueva_activa, sucursal_id))

        conexion.commit()

        accion = "activada" if nueva_activa else "desactivada"

        return {
            "mensaje": f"Sucursal {accion} correctamente",
            "id": sucursal_id,
            "nombre": sucursal["nombre"],
            "activa": nueva_activa,
            "funciones_asociadas": total_funciones
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al cambiar estado de sucursal: {str(error)}")

    finally:
        conexion.close()