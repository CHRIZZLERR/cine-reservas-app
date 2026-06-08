from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.database.conexion import obtener_conexion

router = APIRouter()


class PeliculaCreate(BaseModel):
    titulo: str
    sinopsis: str | None = None
    genero: str | None = None
    clasificacion: str | None = None
    duracion_minutos: int | None = None
    poster_url: str | None = None
    backdrop_url: str | None = None
    trailer: str | None = None
    director: str | None = None
    reparto: str | None = None
    estado: str | None = "cartelera"
    fecha_estreno: str | None = None


class PeliculaUpdate(BaseModel):
    titulo: str | None = None
    sinopsis: str | None = None
    genero: str | None = None
    clasificacion: str | None = None
    duracion_minutos: int | None = None
    poster_url: str | None = None
    backdrop_url: str | None = None
    trailer: str | None = None
    director: str | None = None
    reparto: str | None = None
    estado: str | None = None
    fecha_estreno: str | None = None
    activa: bool | None = None


@router.get("/peliculas")
def obtener_peliculas(
    estado: str | None = Query(default=None),
    sucursal: str | None = Query(default=None),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        filtros = ["p.activa = TRUE"]
        valores = []

        if estado:
            filtros.append("p.estado = %s")
            valores.append(estado.strip().lower())

        if sucursal:
            filtros.append("s.nombre = %s")
            valores.append(sucursal.strip())

            query = f"""
                SELECT DISTINCT p.*
                FROM peliculas p
                INNER JOIN funciones f ON f.pelicula_id = p.id
                INNER JOIN sucursales s ON s.id = f.sucursal_id
                WHERE {' AND '.join(filtros)}
                ORDER BY p.id DESC
            """
        else:
            query = f"""
                SELECT p.*
                FROM peliculas p
                WHERE {' AND '.join(filtros)}
                ORDER BY p.id DESC
            """

        cursor.execute(query, tuple(valores))
        peliculas = cursor.fetchall()

        return peliculas

    finally:
        cursor.close()
        conexion.close()


@router.get("/admin/peliculas")
def obtener_peliculas_admin():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM peliculas
            ORDER BY id DESC
        """)

        peliculas = cursor.fetchall()
        return peliculas

    finally:
        cursor.close()
        conexion.close()


@router.get("/peliculas/{pelicula_id}")
def obtener_pelicula_por_id(pelicula_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM peliculas
            WHERE id = %s
        """, (pelicula_id,))

        pelicula = cursor.fetchone()

        if pelicula is None:
            raise HTTPException(status_code=404, detail="La película no existe")

        return pelicula

    finally:
        cursor.close()
        conexion.close()


@router.get("/peliculas/{pelicula_id}/funciones")
def obtener_funciones_por_pelicula(
    pelicula_id: int,
    sucursal: str | None = Query(default=None),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        filtros = ["p.id = %s"]
        valores = [pelicula_id]

        if sucursal:
            filtros.append("s.nombre = %s")
            valores.append(sucursal.strip())

        cursor.execute(f"""
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
            WHERE {' AND '.join(filtros)}
            ORDER BY f.fecha, f.hora
        """, tuple(valores))

        funciones = cursor.fetchall()
        return funciones

    finally:
        cursor.close()
        conexion.close()


@router.post("/admin/peliculas")
def crear_pelicula(pelicula: PeliculaCreate):
    estados_validos = ["cartelera", "proximamente", "inactiva"]
    estado = pelicula.estado.strip().lower() if pelicula.estado else "cartelera"

    if estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido. Use: cartelera, proximamente o inactiva",
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            INSERT INTO peliculas
            (
                titulo,
                sinopsis,
                genero,
                clasificacion,
                duracion_minutos,
                poster_url,
                backdrop_url,
                trailer,
                director,
                reparto,
                estado,
                fecha_estreno,
                activa
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (
            pelicula.titulo,
            pelicula.sinopsis,
            pelicula.genero,
            pelicula.clasificacion,
            pelicula.duracion_minutos,
            pelicula.poster_url,
            pelicula.backdrop_url,
            pelicula.trailer,
            pelicula.director,
            pelicula.reparto,
            estado,
            pelicula.fecha_estreno,
        ))

        conexion.commit()
        pelicula_id = cursor.lastrowid

        return {
            "mensaje": "Película creada correctamente",
            "id": pelicula_id,
            "titulo": pelicula.titulo,
            "estado": estado,
            "activa": True,
        }

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear película: {str(error)}")

    finally:
        cursor.close()
        conexion.close()


@router.put("/admin/peliculas/{pelicula_id}")
def actualizar_pelicula(pelicula_id: int, pelicula: PeliculaUpdate):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM peliculas
            WHERE id = %s
        """, (pelicula_id,))

        pelicula_actual = cursor.fetchone()

        if pelicula_actual is None:
            raise HTTPException(status_code=404, detail="La película no existe")

        nuevo_titulo = pelicula.titulo if pelicula.titulo is not None else pelicula_actual["titulo"]
        nueva_sinopsis = pelicula.sinopsis if pelicula.sinopsis is not None else pelicula_actual["sinopsis"]
        nuevo_genero = pelicula.genero if pelicula.genero is not None else pelicula_actual["genero"]
        nueva_clasificacion = pelicula.clasificacion if pelicula.clasificacion is not None else pelicula_actual["clasificacion"]
        nueva_duracion = pelicula.duracion_minutos if pelicula.duracion_minutos is not None else pelicula_actual["duracion_minutos"]
        nuevo_poster = pelicula.poster_url if pelicula.poster_url is not None else pelicula_actual["poster_url"]
        nuevo_backdrop = pelicula.backdrop_url if pelicula.backdrop_url is not None else pelicula_actual.get("backdrop_url", "")
        nuevo_trailer = pelicula.trailer if pelicula.trailer is not None else pelicula_actual.get("trailer", "")
        nuevo_director = pelicula.director if pelicula.director is not None else pelicula_actual.get("director", "")
        nuevo_reparto = pelicula.reparto if pelicula.reparto is not None else pelicula_actual.get("reparto", "")
        nuevo_estado = pelicula.estado if pelicula.estado is not None else pelicula_actual["estado"]
        nueva_fecha = pelicula.fecha_estreno if pelicula.fecha_estreno is not None else pelicula_actual["fecha_estreno"]
        nueva_activa = pelicula.activa if pelicula.activa is not None else bool(pelicula_actual["activa"])

        estados_validos = ["cartelera", "proximamente", "inactiva"]
        nuevo_estado = nuevo_estado.strip().lower()

        if nuevo_estado not in estados_validos:
            raise HTTPException(
                status_code=400,
                detail="Estado inválido. Use: cartelera, proximamente o inactiva",
            )

        cursor.execute("""
            UPDATE peliculas
            SET titulo = %s,
                sinopsis = %s,
                genero = %s,
                clasificacion = %s,
                duracion_minutos = %s,
                poster_url = %s,
                backdrop_url = %s,
                trailer = %s,
                director = %s,
                reparto = %s,
                estado = %s,
                fecha_estreno = %s,
                activa = %s
            WHERE id = %s
        """, (
            nuevo_titulo,
            nueva_sinopsis,
            nuevo_genero,
            nueva_clasificacion,
            nueva_duracion,
            nuevo_poster,
            nuevo_backdrop,
            nuevo_trailer,
            nuevo_director,
            nuevo_reparto,
            nuevo_estado,
            nueva_fecha,
            nueva_activa,
            pelicula_id,
        ))

        conexion.commit()

        return {
            "mensaje": "Película actualizada correctamente",
            "id": pelicula_id,
            "titulo": nuevo_titulo,
            "estado": nuevo_estado,
            "activa": nueva_activa,
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar película: {str(error)}")

    finally:
        cursor.close()
        conexion.close()


@router.delete("/admin/peliculas/{pelicula_id}")
def desactivar_pelicula(pelicula_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, titulo, activa
            FROM peliculas
            WHERE id = %s
        """, (pelicula_id,))

        pelicula = cursor.fetchone()

        if pelicula is None:
            raise HTTPException(status_code=404, detail="La película no existe")

        cursor.execute("""
            UPDATE peliculas
            SET activa = FALSE,
                estado = 'inactiva'
            WHERE id = %s
        """, (pelicula_id,))

        conexion.commit()

        return {
            "mensaje": "Película desactivada correctamente",
            "id": pelicula_id,
            "titulo": pelicula["titulo"],
            "activa": False,
            "estado": "inactiva",
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al desactivar película: {str(error)}")

    finally:
        cursor.close()
        conexion.close()