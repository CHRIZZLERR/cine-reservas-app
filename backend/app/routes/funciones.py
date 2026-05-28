from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.conexion import obtener_conexion

router = APIRouter()


class FuncionCreate(BaseModel):
    pelicula_id: int
    sucursal_id: int
    fecha: str
    hora: str
    sala: str
    precio: float


class FuncionUpdate(BaseModel):
    pelicula_id: int | None = None
    sucursal_id: int | None = None
    fecha: str | None = None
    hora: str | None = None
    sala: str | None = None
    precio: float | None = None


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
        ORDER BY f.fecha, f.hora
    """)

    funciones = cursor.fetchall()
    conexion.close()
    return funciones


@router.get("/admin/funciones")
def obtener_funciones_admin():
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
            p.estado AS estado_pelicula,
            p.activa AS pelicula_activa,
            s.nombre AS sucursal,
            s.direccion AS direccion_sucursal,
            s.ciudad
        FROM funciones f
        INNER JOIN peliculas p ON f.pelicula_id = p.id
        INNER JOIN sucursales s ON f.sucursal_id = s.id
        ORDER BY f.fecha, f.hora
    """)

    funciones = cursor.fetchall()
    conexion.close()
    return funciones


@router.post("/admin/funciones")
def crear_funcion(funcion: FuncionCreate):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, titulo, activa
            FROM peliculas
            WHERE id = %s
        """, (funcion.pelicula_id,))

        pelicula = cursor.fetchone()

        if pelicula is None:
            raise HTTPException(status_code=404, detail="La película no existe")

        if not pelicula["activa"]:
            raise HTTPException(status_code=400, detail="No se puede crear función para una película inactiva")

        cursor.execute("""
            SELECT id, nombre, activa
            FROM sucursales
            WHERE id = %s
        """, (funcion.sucursal_id,))

        sucursal = cursor.fetchone()

        if sucursal is None:
            raise HTTPException(status_code=404, detail="La sucursal no existe")

        if not sucursal["activa"]:
            raise HTTPException(status_code=400, detail="No se puede crear función para una sucursal inactiva")

        if funcion.precio <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")

        cursor.execute("""
            INSERT INTO funciones
            (pelicula_id, sucursal_id, fecha, hora, sala, precio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            funcion.pelicula_id,
            funcion.sucursal_id,
            funcion.fecha,
            funcion.hora,
            funcion.sala,
            funcion.precio
        ))

        conexion.commit()

        funcion_id = cursor.lastrowid

        return {
            "mensaje": "Función creada correctamente",
            "id": funcion_id,
            "pelicula_id": funcion.pelicula_id,
            "pelicula": pelicula["titulo"],
            "sucursal_id": funcion.sucursal_id,
            "sucursal": sucursal["nombre"],
            "fecha": funcion.fecha,
            "hora": funcion.hora,
            "sala": funcion.sala,
            "precio": funcion.precio
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear función: {str(error)}")

    finally:
        conexion.close()


@router.put("/admin/funciones/{funcion_id}")
def actualizar_funcion(funcion_id: int, funcion: FuncionUpdate):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM funciones
            WHERE id = %s
        """, (funcion_id,))

        funcion_actual = cursor.fetchone()

        if funcion_actual is None:
            raise HTTPException(status_code=404, detail="La función no existe")

        nueva_pelicula_id = funcion.pelicula_id if funcion.pelicula_id is not None else funcion_actual["pelicula_id"]
        nueva_sucursal_id = funcion.sucursal_id if funcion.sucursal_id is not None else funcion_actual["sucursal_id"]
        nueva_fecha = funcion.fecha if funcion.fecha is not None else funcion_actual["fecha"]
        nueva_hora = funcion.hora if funcion.hora is not None else funcion_actual["hora"]
        nueva_sala = funcion.sala if funcion.sala is not None else funcion_actual["sala"]
        nuevo_precio = funcion.precio if funcion.precio is not None else funcion_actual["precio"]

        cursor.execute("""
            SELECT id, titulo, activa
            FROM peliculas
            WHERE id = %s
        """, (nueva_pelicula_id,))

        pelicula = cursor.fetchone()

        if pelicula is None:
            raise HTTPException(status_code=404, detail="La película no existe")

        if not pelicula["activa"]:
            raise HTTPException(status_code=400, detail="No se puede asignar una película inactiva")

        cursor.execute("""
            SELECT id, nombre, activa
            FROM sucursales
            WHERE id = %s
        """, (nueva_sucursal_id,))

        sucursal = cursor.fetchone()

        if sucursal is None:
            raise HTTPException(status_code=404, detail="La sucursal no existe")

        if not sucursal["activa"]:
            raise HTTPException(status_code=400, detail="No se puede asignar una sucursal inactiva")

        if float(nuevo_precio) <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")

        cursor.execute("""
            UPDATE funciones
            SET pelicula_id = %s,
                sucursal_id = %s,
                fecha = %s,
                hora = %s,
                sala = %s,
                precio = %s
            WHERE id = %s
        """, (
            nueva_pelicula_id,
            nueva_sucursal_id,
            nueva_fecha,
            nueva_hora,
            nueva_sala,
            nuevo_precio,
            funcion_id
        ))

        conexion.commit()

        return {
            "mensaje": "Función actualizada correctamente",
            "id": funcion_id,
            "pelicula_id": nueva_pelicula_id,
            "pelicula": pelicula["titulo"],
            "sucursal_id": nueva_sucursal_id,
            "sucursal": sucursal["nombre"],
            "fecha": nueva_fecha,
            "hora": str(nueva_hora),
            "sala": nueva_sala,
            "precio": float(nuevo_precio)
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar función: {str(error)}")

    finally:
        conexion.close()


@router.delete("/admin/funciones/{funcion_id}")
def eliminar_funcion(funcion_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id
            FROM funciones
            WHERE id = %s
        """, (funcion_id,))

        funcion = cursor.fetchone()

        if funcion is None:
            raise HTTPException(status_code=404, detail="La función no existe")

        cursor.execute("""
            SELECT id
            FROM reservas
            WHERE funcion_id = %s
            LIMIT 1
        """, (funcion_id,))

        reserva_existente = cursor.fetchone()

        if reserva_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar esta función porque ya tiene reservas registradas"
            )

        cursor.execute("""
            DELETE FROM funciones
            WHERE id = %s
        """, (funcion_id,))

        conexion.commit()

        return {
            "mensaje": "Función eliminada correctamente",
            "id": funcion_id
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar función: {str(error)}")

    finally:
        conexion.close()