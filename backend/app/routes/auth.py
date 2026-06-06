from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.conexion import obtener_conexion

router = APIRouter()


class UsuarioRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


def usuario_response(usuario: dict):
    return {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "email": usuario["email"],
        "rol": usuario["rol"],
        "activo": bool(usuario["activo"]),
    }


@router.post("/auth/register")
def registrar_usuario(datos: UsuarioRegister):
    nombre = datos.nombre.strip()
    email = datos.email.strip().lower()
    password = datos.password.strip()

    if not nombre:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    if len(password) < 4:
        raise HTTPException(status_code=400, detail="La contraseña debe tener mínimo 4 caracteres")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE email = %s
        """, (email,))

        usuario_existente = cursor.fetchone()

        if usuario_existente is not None:
            raise HTTPException(status_code=400, detail="Ya existe una cuenta con este correo")

        cursor.execute("""
            INSERT INTO usuarios
            (nombre, email, password_hash, rol, activo)
            VALUES (%s, %s, %s, 'cliente', TRUE)
        """, (
            nombre,
            email,
            password
        ))

        conexion.commit()

        usuario_id = cursor.lastrowid

        return {
            "mensaje": "Usuario registrado correctamente",
            "usuario": {
                "id": usuario_id,
                "nombre": nombre,
                "email": email,
                "rol": "cliente",
                "activo": True,
            }
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(error)}")

    finally:
        conexion.close()


@router.post("/auth/login")
def iniciar_sesion(datos: UsuarioLogin):
    email = datos.email.strip().lower()
    password = datos.password.strip()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                nombre,
                email,
                password_hash,
                rol,
                activo
            FROM usuarios
            WHERE email = %s
        """, (email,))

        usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        if not usuario["activo"]:
            raise HTTPException(status_code=403, detail="Este usuario está desactivado")

        if usuario["password_hash"] != password:
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        return {
            "mensaje": "Sesión iniciada correctamente",
            "usuario": usuario_response(usuario)
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(error)}")

    finally:
        conexion.close()


@router.get("/auth/usuarios")
def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                nombre,
                email,
                rol,
                activo,
                fecha_creacion
            FROM usuarios
            ORDER BY id DESC
        """)

        usuarios = cursor.fetchall()

        return usuarios

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(error)}")

    finally:
        conexion.close()


@router.put("/admin/usuarios/{usuario_id}/estado")
def cambiar_estado_usuario(usuario_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, nombre, email, activo
            FROM usuarios
            WHERE id = %s
        """, (usuario_id,))

        usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        nuevo_estado = not bool(usuario["activo"])

        cursor.execute("""
            UPDATE usuarios
            SET activo = %s
            WHERE id = %s
        """, (nuevo_estado, usuario_id))

        conexion.commit()

        return {
            "mensaje": "Estado del usuario actualizado correctamente",
            "id": usuario_id,
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "activo": nuevo_estado
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(error)}")

    finally:
        conexion.close()