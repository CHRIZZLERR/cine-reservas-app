import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from fastapi import APIRouter, HTTPException
from app.database.conexion import obtener_conexion

router = APIRouter()

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"


def cargar_env_manual():
    """
    Carga variables desde backend/.env sin depender obligatoriamente de python-dotenv.
    Esto ayuda a evitar errores si python-dotenv no está instalado.
    """
    posibles_rutas = [
        ".env",
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()

                    if not linea or linea.startswith("#") or "=" not in linea:
                        continue

                    clave, valor = linea.split("=", 1)
                    clave = clave.strip()
                    valor = valor.strip().strip('"').strip("'")

                    if clave and valor and clave not in os.environ:
                        os.environ[clave] = valor


cargar_env_manual()


def obtener_token_tmdb() -> str:
    token = os.getenv("TMDB_BEARER_TOKEN", "").strip()

    if not token or token == "PEGA_AQUI_TU_TOKEN_DE_TMDB":
        raise HTTPException(
            status_code=500,
            detail="No se encontró TMDB_BEARER_TOKEN en el archivo .env"
        )

    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    return token


def construir_url_tmdb(endpoint: str, params: dict | None = None) -> str:
    params = params or {}

    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    url = TMDB_BASE_URL + endpoint

    if params:
        url += "?" + urlencode(params)

    return url


def consultar_tmdb(endpoint: str, params: dict | None = None):
    token = obtener_token_tmdb()
    url = construir_url_tmdb(endpoint, params)

    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "accept": "application/json",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    except HTTPError as error:
        detalle = error.read().decode("utf-8")

        raise HTTPException(
            status_code=error.code,
            detail=f"Error consultando TMDB: {detalle}"
        )

    except URLError as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo conectar con TMDB: {str(error)}"
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado consultando TMDB: {str(error)}"
        )


def url_imagen(path: str | None) -> str | None:
    if not path:
        return None

    return f"{TMDB_IMAGE_BASE_URL}{path}"


def obtener_clasificacion(release_dates: dict) -> str:
    """
    Intenta sacar clasificación por edades.
    Primero busca US, luego cualquier país que tenga certification.
    """
    resultados = release_dates.get("results", [])

    for pais in resultados:
        if pais.get("iso_3166_1") == "US":
            for release in pais.get("release_dates", []):
                certificacion = release.get("certification")
                if certificacion:
                    return certificacion

    for pais in resultados:
        for release in pais.get("release_dates", []):
            certificacion = release.get("certification")
            if certificacion:
                return certificacion

    return "S/R"


def obtener_director(credits: dict) -> str:
    crew = credits.get("crew", [])

    directores = [
        persona.get("name")
        for persona in crew
        if persona.get("job") == "Director" and persona.get("name")
    ]

    return ", ".join(directores) if directores else "No disponible"


def obtener_reparto(credits: dict) -> str:
    cast = credits.get("cast", [])

    actores = [
        persona.get("name")
        for persona in cast[:6]
        if persona.get("name")
    ]

    return ", ".join(actores) if actores else "No disponible"


def obtener_trailer(videos: dict) -> str | None:
    resultados = videos.get("results", [])

    for video in resultados:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("official") is True
            and video.get("key")
        ):
            return video.get("key")

    for video in resultados:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("key")
        ):
            return video.get("key")

    for video in resultados:
        if video.get("site") == "YouTube" and video.get("key"):
            return video.get("key")

    return None


def formatear_pelicula_busqueda(pelicula: dict) -> dict:
    return {
        "tmdb_id": pelicula.get("id"),
        "titulo": pelicula.get("title"),
        "titulo_original": pelicula.get("original_title"),
        "sinopsis": pelicula.get("overview") or "",
        "fecha_estreno": pelicula.get("release_date") or None,
        "poster_url": url_imagen(pelicula.get("poster_path")),
        "backdrop_url": url_imagen(pelicula.get("backdrop_path")),
        "rating": pelicula.get("vote_average"),
    }


def obtener_detalle_pelicula(tmdb_id: int, language: str = "es-ES") -> dict:
    pelicula = consultar_tmdb(
        f"/movie/{tmdb_id}",
        {
            "language": language,
            "append_to_response": "credits,videos,release_dates",
        }
    )

    generos = pelicula.get("genres", [])
    genero_texto = " / ".join([g.get("name") for g in generos if g.get("name")]) or "No disponible"

    duracion = pelicula.get("runtime") or 0
    release_dates = pelicula.get("release_dates", {})
    credits = pelicula.get("credits", {})
    videos = pelicula.get("videos", {})

    return {
        "tmdb_id": pelicula.get("id"),
        "titulo": pelicula.get("title"),
        "titulo_original": pelicula.get("original_title"),
        "sinopsis": pelicula.get("overview") or "Sin sinopsis disponible.",
        "genero": genero_texto,
        "clasificacion": obtener_clasificacion(release_dates),
        "duracion_minutos": duracion,
        "fecha_estreno": pelicula.get("release_date") or None,
        "poster_url": url_imagen(pelicula.get("poster_path")),
        "backdrop_url": url_imagen(pelicula.get("backdrop_path")),
        "trailer": obtener_trailer(videos),
        "director": obtener_director(credits),
        "reparto": obtener_reparto(credits),
        "rating": pelicula.get("vote_average") or 0,
    }


@router.get("/tmdb/buscar")
def buscar_peliculas(query: str, language: str = "es-ES"):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Debe escribir un texto de búsqueda")

    datos = consultar_tmdb(
        "/search/movie",
        {
            "query": query,
            "language": language,
            "include_adult": "false",
        }
    )

    resultados = datos.get("results", [])

    peliculas = [
        formatear_pelicula_busqueda(pelicula)
        for pelicula in resultados
    ]

    return {
        "query": query,
        "resultados": peliculas,
    }


@router.get("/tmdb/pelicula/{tmdb_id}")
def detalle_pelicula_tmdb(tmdb_id: int, language: str = "es-ES"):
    return obtener_detalle_pelicula(tmdb_id, language)


@router.post("/admin/peliculas/importar-tmdb/{tmdb_id}")
def importar_pelicula_desde_tmdb(
    tmdb_id: int,
    estado: str = "cartelera",
    language: str = "es-ES"
):
    estados_validos = ["cartelera", "proximamente", "inactiva"]
    estado = estado.strip().lower()

    if estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido. Use: cartelera, proximamente o inactiva"
        )

    pelicula = obtener_detalle_pelicula(tmdb_id, language)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, titulo
            FROM peliculas
            WHERE tmdb_id = %s
            LIMIT 1
        """, (tmdb_id,))

        pelicula_existente = cursor.fetchone()

        if pelicula_existente is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Esta película ya existe en la base de datos: {pelicula_existente['titulo']}"
            )

        cursor.execute("""
            INSERT INTO peliculas
            (
                tmdb_id,
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
                rating,
                estado,
                fecha_estreno,
                activa
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (
            pelicula["tmdb_id"],
            pelicula["titulo"],
            pelicula["sinopsis"],
            pelicula["genero"],
            pelicula["clasificacion"],
            pelicula["duracion_minutos"],
            pelicula["poster_url"],
            pelicula["backdrop_url"],
            pelicula["trailer"],
            pelicula["director"],
            pelicula["reparto"],
            pelicula["rating"],
            estado,
            pelicula["fecha_estreno"],
        ))

        conexion.commit()
        pelicula_id = cursor.lastrowid

        return {
            "mensaje": "Película importada correctamente desde TMDB",
            "id": pelicula_id,
            "tmdb_id": pelicula["tmdb_id"],
            "titulo": pelicula["titulo"],
            "sinopsis": pelicula["sinopsis"],
            "genero": pelicula["genero"],
            "clasificacion": pelicula["clasificacion"],
            "duracion_minutos": pelicula["duracion_minutos"],
            "fecha_estreno": pelicula["fecha_estreno"],
            "poster_url": pelicula["poster_url"],
            "backdrop_url": pelicula["backdrop_url"],
            "trailer": pelicula["trailer"],
            "director": pelicula["director"],
            "reparto": pelicula["reparto"],
            "rating": pelicula["rating"],
            "estado": estado,
            "activa": True,
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al importar película desde TMDB: {str(error)}"
        )

    finally:
        conexion.close()