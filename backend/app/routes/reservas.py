from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.conexion import obtener_conexion


router = APIRouter()


class ReservaCreate(BaseModel):
    usuario_id: int | None = None
    funcion_id: int
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: str | None = None
    asientos: list[str]
    metodo_pago: str | None = "Pago en taquilla"


class EstadoReservaUpdate(BaseModel):
    estado: str


def agregar_asientos_a_reserva(cursor, reserva: dict) -> dict:
    cursor.execute(
        """
        SELECT asiento
        FROM asientos_reservados
        WHERE reserva_id = %s
        ORDER BY asiento
        """,
        (reserva["id"],),
    )

    reserva["asientos"] = [fila["asiento"] for fila in cursor.fetchall()]
    return reserva


@router.get("/reservas")
def obtener_reservas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.id,
            r.usuario_id,
            r.codigo_reserva,
            r.nombre_cliente,
            r.email_cliente,
            r.telefono_cliente,
            r.cantidad_asientos,
            r.total,
            r.metodo_pago,
            r.estado,
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
        """
    )

    reservas = cursor.fetchall()

    for reserva in reservas:
        agregar_asientos_a_reserva(cursor, reserva)

    conexion.close()
    return reservas


@router.get("/usuarios/{usuario_id}/reservas")
def obtener_reservas_por_usuario(usuario_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.id,
            r.usuario_id,
            r.codigo_reserva,
            r.nombre_cliente,
            r.email_cliente,
            r.telefono_cliente,
            r.cantidad_asientos,
            r.total,
            r.metodo_pago,
            r.estado,
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
        WHERE r.usuario_id = %s
        ORDER BY r.fecha_reserva DESC
        """,
        (usuario_id,),
    )

    reservas = cursor.fetchall()

    for reserva in reservas:
        agregar_asientos_a_reserva(cursor, reserva)

    conexion.close()
    return reservas


@router.get("/reservas/{codigo_reserva}")
def obtener_reserva_por_codigo(codigo_reserva: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.id,
            r.usuario_id,
            r.codigo_reserva,
            r.nombre_cliente,
            r.email_cliente,
            r.telefono_cliente,
            r.cantidad_asientos,
            r.total,
            r.metodo_pago,
            r.estado,
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
        """,
        (codigo_reserva,),
    )

    reserva = cursor.fetchone()

    if reserva is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La reserva no existe")

    agregar_asientos_a_reserva(cursor, reserva)

    conexion.close()
    return reserva


@router.get("/funciones/{funcion_id}/asientos")
def obtener_asientos_ocupados(funcion_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id
        FROM funciones
        WHERE id = %s
        """,
        (funcion_id,),
    )

    funcion = cursor.fetchone()

    if funcion is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La función no existe")

    cursor.execute(
        """
        SELECT asiento
        FROM asientos_reservados
        WHERE funcion_id = %s
        ORDER BY asiento
        """,
        (funcion_id,),
    )

    asientos_ocupados = [fila["asiento"] for fila in cursor.fetchall()]

    conexion.close()

    return {
        "funcion_id": funcion_id,
        "asientos_ocupados": asientos_ocupados,
    }


@router.put("/admin/reservas/{reserva_id}/estado")
def actualizar_estado_reserva(reserva_id: int, datos: EstadoReservaUpdate):
    estados_validos = ["pendiente", "confirmada", "cancelada"]
    nuevo_estado = datos.estado.strip().lower()

    if nuevo_estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido. Use: pendiente, confirmada o cancelada",
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, codigo_reserva, estado
            FROM reservas
            WHERE id = %s
            """,
            (reserva_id,),
        )

        reserva = cursor.fetchone()

        if reserva is None:
            raise HTTPException(status_code=404, detail="La reserva no existe")

        cursor.execute(
            """
            UPDATE reservas
            SET estado = %s
            WHERE id = %s
            """,
            (nuevo_estado, reserva_id),
        )

        conexion.commit()

        return {
            "mensaje": "Estado de reserva actualizado correctamente",
            "id": reserva_id,
            "codigo_reserva": reserva["codigo_reserva"],
            "estado_anterior": reserva["estado"],
            "estado_nuevo": nuevo_estado,
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar estado: {str(error)}",
        )

    finally:
        conexion.close()


@router.post("/reservas")
def crear_reserva(reserva: ReservaCreate):
    if len(reserva.asientos) == 0:
        raise HTTPException(
            status_code=400,
            detail="Debe seleccionar al menos un asiento",
        )

    if len(reserva.asientos) > 10:
        raise HTTPException(
            status_code=400,
            detail="No se pueden reservar más de 10 asientos",
        )

    if not reserva.nombre_cliente.strip():
        raise HTTPException(
            status_code=400,
            detail="El nombre del cliente es obligatorio",
        )

    if not reserva.email_cliente.strip():
        raise HTTPException(
            status_code=400,
            detail="El correo del cliente es obligatorio",
        )

    if not reserva.telefono_cliente or not reserva.telefono_cliente.strip():
        raise HTTPException(
            status_code=400,
            detail="El teléfono del cliente es obligatorio",
        )

    asientos_normalizados = [
        asiento.strip().upper()
        for asiento in reserva.asientos
    ]

    if len(asientos_normalizados) != len(set(asientos_normalizados)):
        raise HTTPException(
            status_code=400,
            detail="No puedes repetir asientos en la misma reserva",
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        if reserva.usuario_id is not None and reserva.usuario_id > 0:
            cursor.execute(
                """
                SELECT id, activo
                FROM usuarios
                WHERE id = %s
                """,
                (reserva.usuario_id,),
            )

            usuario = cursor.fetchone()

            if usuario is None:
                raise HTTPException(
                    status_code=404,
                    detail="El usuario de la reserva no existe",
                )

            if not usuario["activo"]:
                raise HTTPException(
                    status_code=403,
                    detail="El usuario está inactivo y no puede reservar",
                )

        cursor.execute(
            """
            SELECT id, precio
            FROM funciones
            WHERE id = %s
            """,
            (reserva.funcion_id,),
        )

        funcion = cursor.fetchone()

        if funcion is None:
            raise HTTPException(status_code=404, detail="La función no existe")

        placeholders = ", ".join(["%s"] * len(asientos_normalizados))

        cursor.execute(
            f"""
            SELECT asiento
            FROM asientos_reservados
            WHERE funcion_id = %s
            AND asiento IN ({placeholders})
            """,
            (reserva.funcion_id, *asientos_normalizados),
        )

        asientos_ya_ocupados = [
            fila["asiento"]
            for fila in cursor.fetchall()
        ]

        if len(asientos_ya_ocupados) > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Estos asientos ya están reservados: {', '.join(asientos_ya_ocupados)}",
            )

        cantidad_asientos = len(asientos_normalizados)
        total = float(funcion["precio"]) * cantidad_asientos
        usuario_id = reserva.usuario_id if reserva.usuario_id and reserva.usuario_id > 0 else None

        cursor.execute(
            """
            INSERT INTO reservas
            (
                usuario_id,
                funcion_id,
                nombre_cliente,
                email_cliente,
                telefono_cliente,
                cantidad_asientos,
                total,
                metodo_pago,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """,
            (
                usuario_id,
                reserva.funcion_id,
                reserva.nombre_cliente.strip(),
                reserva.email_cliente.strip(),
                reserva.telefono_cliente.strip(),
                cantidad_asientos,
                total,
                reserva.metodo_pago,
            ),
        )

        reserva_id = cursor.lastrowid
        codigo_reserva = f"JCC-{reserva_id:05d}"

        cursor.execute(
            """
            UPDATE reservas
            SET codigo_reserva = %s
            WHERE id = %s
            """,
            (codigo_reserva, reserva_id),
        )

        for asiento in asientos_normalizados:
            cursor.execute(
                """
                INSERT INTO asientos_reservados
                (reserva_id, funcion_id, asiento)
                VALUES (%s, %s, %s)
                """,
                (reserva_id, reserva.funcion_id, asiento),
            )

        conexion.commit()

        return {
            "mensaje": "Reserva creada correctamente",
            "id": reserva_id,
            "usuario_id": usuario_id,
            "codigo_reserva": codigo_reserva,
            "funcion_id": reserva.funcion_id,
            "nombre_cliente": reserva.nombre_cliente.strip(),
            "email_cliente": reserva.email_cliente.strip(),
            "telefono_cliente": reserva.telefono_cliente.strip(),
            "asientos": asientos_normalizados,
            "cantidad_asientos": cantidad_asientos,
            "total": total,
            "metodo_pago": reserva.metodo_pago,
            "estado": "pendiente",
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear la reserva: {str(error)}",
        )

    finally:
        conexion.close()
