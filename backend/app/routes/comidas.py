from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.conexion import obtener_conexion


router = APIRouter()


class ComidaCreate(BaseModel):
    nombre: str
    descripcion: str | None = ""
    precio: float
    imagen_url: str | None = ""
    activa: bool | None = True


class ComidaUpdate(BaseModel):
    nombre: str
    descripcion: str | None = ""
    precio: float
    imagen_url: str | None = ""
    activa: bool | None = True


def limpiar_comida(comida: dict) -> dict:
    return {
        "id": int(comida.get("id", 0)),
        "nombre": str(comida.get("nombre") or ""),
        "descripcion": str(comida.get("descripcion") or ""),
        "precio": float(comida.get("precio") or 0),
        "imagen_url": str(comida.get("imagen_url") or ""),
        "activa": bool(comida.get("activa", False)),
        "fecha_creacion": str(comida.get("fecha_creacion") or ""),
    }


@router.get("/comidas")
def obtener_comidas_publicas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            precio,
            imagen_url,
            activa,
            fecha_creacion
        FROM comidas
        WHERE activa = TRUE
        ORDER BY id ASC
        """
    )

    comidas = [limpiar_comida(comida) for comida in cursor.fetchall()]

    conexion.close()
    return comidas


@router.get("/admin/comidas")
def obtener_comidas_admin():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            precio,
            imagen_url,
            activa,
            fecha_creacion
        FROM comidas
        ORDER BY id DESC
        """
    )

    comidas = [limpiar_comida(comida) for comida in cursor.fetchall()]

    conexion.close()
    return comidas


@router.post("/admin/comidas")
def crear_comida(datos: ComidaCreate):
    if not datos.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    if datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO comidas
            (
                nombre,
                descripcion,
                precio,
                imagen_url,
                activa
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                datos.nombre.strip(),
                datos.descripcion.strip() if datos.descripcion else "",
                datos.precio,
                datos.imagen_url.strip() if datos.imagen_url else "",
                bool(datos.activa),
            ),
        )

        conexion.commit()

        comida_id = cursor.lastrowid

        return {
            "mensaje": "Comida creada correctamente",
            "id": comida_id,
        }

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear comida: {str(error)}",
        )

    finally:
        conexion.close()


@router.put("/admin/comidas/{comida_id}")
def actualizar_comida(comida_id: int, datos: ComidaUpdate):
    if not datos.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    if datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id
            FROM comidas
            WHERE id = %s
            """,
            (comida_id,),
        )

        comida = cursor.fetchone()

        if comida is None:
            raise HTTPException(status_code=404, detail="La comida no existe")

        cursor.execute(
            """
            UPDATE comidas
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                imagen_url = %s,
                activa = %s
            WHERE id = %s
            """,
            (
                datos.nombre.strip(),
                datos.descripcion.strip() if datos.descripcion else "",
                datos.precio,
                datos.imagen_url.strip() if datos.imagen_url else "",
                bool(datos.activa),
                comida_id,
            ),
        )

        conexion.commit()

        return {
            "mensaje": "Comida actualizada correctamente",
            "id": comida_id,
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar comida: {str(error)}",
        )

    finally:
        conexion.close()


@router.delete("/admin/comidas/{comida_id}")
def cambiar_estado_comida(comida_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, activa
            FROM comidas
            WHERE id = %s
            """,
            (comida_id,),
        )

        comida = cursor.fetchone()

        if comida is None:
            raise HTTPException(status_code=404, detail="La comida no existe")

        nuevo_estado = not bool(comida["activa"])

        cursor.execute(
            """
            UPDATE comidas
            SET activa = %s
            WHERE id = %s
            """,
            (nuevo_estado, comida_id),
        )

        conexion.commit()

        return {
            "mensaje": "Estado de comida actualizado correctamente",
            "id": comida_id,
            "activa": nuevo_estado,
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al cambiar estado de comida: {str(error)}",
        )

    finally:
        conexion.close()