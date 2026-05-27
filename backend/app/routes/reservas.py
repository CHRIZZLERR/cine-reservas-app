from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.conexion import obtener_conexion

router = APIRouter()


class ReservaCreate(BaseModel):
    funcion_id: int
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: str | None = None
    asientos: list[str]
    metodo_pago: str | None = "Pago en taquilla"


@router.get("/reservas")
def obtener_reservas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id,
            r.codigo_reserva,
            r.nombre_cliente,
            r.email_cliente,
            r.telefono_cliente,
            r.cantidad_asientos,
            r.total,
            r.metodo_pago,
            r.fecha_reserva,
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
        FROM reservas r
        INNER JOIN funciones f ON r.funcion_id = f.id
        INNER JOIN peliculas p ON f.pelicula_id = p.id
        INNER JOIN sucursales s ON f.sucursal_id = s.id
        ORDER BY r.fecha_reserva DESC
    """)

    reservas = cursor.fetchall()

    for reserva in reservas:
        cursor.execute("""
            SELECT asiento
            FROM asientos_reservados
            WHERE reserva_id = %s
            ORDER BY asiento
        """, (reserva["id"],))

        reserva["asientos"] = [fila["asiento"] for fila in cursor.fetchall()]

    conexion.close()
    return reservas


@router.get("/reservas/{codigo_reserva}")
def obtener_reserva_por_codigo(codigo_reserva: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id,
            r.codigo_reserva,
            r.nombre_cliente,
            r.email_cliente,
            r.telefono_cliente,
            r.cantidad_asientos,
            r.total,
            r.metodo_pago,
            r.fecha_reserva,
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
        FROM reservas r
        INNER JOIN funciones f ON r.funcion_id = f.id
        INNER JOIN peliculas p ON f.pelicula_id = p.id
        INNER JOIN sucursales s ON f.sucursal_id = s.id
        WHERE r.codigo_reserva = %s
    """, (codigo_reserva,))

    reserva = cursor.fetchone()

    if reserva is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La reserva no existe")

    cursor.execute("""
        SELECT asiento
        FROM asientos_reservados
        WHERE reserva_id = %s
        ORDER BY asiento
    """, (reserva["id"],))

    reserva["asientos"] = [fila["asiento"] for fila in cursor.fetchall()]

    conexion.close()
    return reserva


@router.get("/funciones/{funcion_id}/asientos")
def obtener_asientos_ocupados(funcion_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id
        FROM funciones
        WHERE id = %s
    """, (funcion_id,))

    funcion = cursor.fetchone()

    if funcion is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La función no existe")

    cursor.execute("""
        SELECT asiento
        FROM asientos_reservados
        WHERE funcion_id = %s
        ORDER BY asiento
    """, (funcion_id,))

    asientos_ocupados = [fila["asiento"] for fila in cursor.fetchall()]

    conexion.close()

    return {
        "funcion_id": funcion_id,
        "asientos_ocupados": asientos_ocupados
    }


@router.post("/reservas")
def crear_reserva(reserva: ReservaCreate):
    if len(reserva.asientos) == 0:
        raise HTTPException(status_code=400, detail="Debe seleccionar al menos un asiento")

    if len(reserva.asientos) > 10:
        raise HTTPException(status_code=400, detail="No se pueden reservar más de 10 asientos")

    # Limpia espacios y convierte a mayúsculas
    asientos_normalizados = [asiento.strip().upper() for asiento in reserva.asientos]

    # Evita asientos repetidos en la misma reserva
    if len(asientos_normalizados) != len(set(asientos_normalizados)):
        raise HTTPException(status_code=400, detail="No puedes repetir asientos en la misma reserva")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        # Verificar que la función exista y obtener precio
        cursor.execute("""
            SELECT id, precio
            FROM funciones
            WHERE id = %s
        """, (reserva.funcion_id,))

        funcion = cursor.fetchone()

        if funcion is None:
            raise HTTPException(status_code=404, detail="La función no existe")

        # Verificar si algún asiento ya está reservado
        placeholders = ", ".join(["%s"] * len(asientos_normalizados))

        cursor.execute(f"""
            SELECT asiento
            FROM asientos_reservados
            WHERE funcion_id = %s
            AND asiento IN ({placeholders})
        """, (reserva.funcion_id, *asientos_normalizados))

        asientos_ya_ocupados = [fila["asiento"] for fila in cursor.fetchall()]

        if len(asientos_ya_ocupados) > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Estos asientos ya están reservados: {', '.join(asientos_ya_ocupados)}"
            )

        cantidad_asientos = len(asientos_normalizados)
        total = float(funcion["precio"]) * cantidad_asientos

        # Crear reserva primero sin código
        cursor.execute("""
            INSERT INTO reservas
            (funcion_id, nombre_cliente, email_cliente, telefono_cliente, cantidad_asientos, total, metodo_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            reserva.funcion_id,
            reserva.nombre_cliente,
            reserva.email_cliente,
            reserva.telefono_cliente,
            cantidad_asientos,
            total,
            reserva.metodo_pago
        ))

        reserva_id = cursor.lastrowid
        codigo_reserva = f"CMX-{reserva_id:05d}"

        # Actualizar código de reserva
        cursor.execute("""
            UPDATE reservas
            SET codigo_reserva = %s
            WHERE id = %s
        """, (codigo_reserva, reserva_id))

        # Guardar asientos seleccionados
        for asiento in asientos_normalizados:
            cursor.execute("""
                INSERT INTO asientos_reservados
                (reserva_id, funcion_id, asiento)
                VALUES (%s, %s, %s)
            """, (reserva_id, reserva.funcion_id, asiento))

        conexion.commit()

        return {
            "mensaje": "Reserva creada correctamente",
            "id": reserva_id,
            "codigo_reserva": codigo_reserva,
            "funcion_id": reserva.funcion_id,
            "nombre_cliente": reserva.nombre_cliente,
            "email_cliente": reserva.email_cliente,
            "telefono_cliente": reserva.telefono_cliente,
            "asientos": asientos_normalizados,
            "cantidad_asientos": cantidad_asientos,
            "total": total,
            "metodo_pago": reserva.metodo_pago
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {str(error)}")

    finally:
        conexion.close()