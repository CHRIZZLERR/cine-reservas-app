# JC Cinemas - Sistema de Reservas de Cine

## Descripción del proyecto

**JC Cinemas** es una aplicación web desarrollada para simular un sistema moderno de reservas de cine. El proyecto permite a los usuarios consultar películas en cartelera, ver detalles de cada película, seleccionar funciones, escoger asientos, agregar comida y bebida, registrarse o iniciar sesión, y finalmente generar una reserva con código de confirmación.

Además, el sistema cuenta con un **panel administrativo** donde un administrador puede gestionar películas, funciones, reservas, usuarios, sucursales, comidas y contenido importado desde TMDB.

Este proyecto fue desarrollado como una práctica completa de integración entre frontend, backend y base de datos, utilizando tecnologías modernas como **Reflex**, **FastAPI**, **MySQL** y **Aiven**.

---

## Objetivo del proyecto

El objetivo principal de este proyecto es crear una plataforma funcional de reservas de cine que permita aplicar conocimientos de desarrollo web, programación backend, conexión con base de datos, consumo de APIs externas y diseño de interfaces.

El sistema busca simular el funcionamiento real de una plataforma de cine, permitiendo:

* Mostrar películas en cartelera y próximamente.
* Consultar detalles de películas.
* Seleccionar sucursal, fecha y horario.
* Reservar asientos.
* Agregar comida y bebida.
* Registrar usuarios e iniciar sesión.
* Guardar reservas de clientes.
* Administrar el contenido desde un panel privado.

---

## Tecnologías utilizadas

### Frontend

* **Reflex**
* **Python**
* **HTML generado por componentes**
* **CSS personalizado**
* **Diseño responsive básico**

### Backend

* **FastAPI**
* **Python**
* **Pydantic**
* **Uvicorn**
* **HTTPX**

### Base de datos

* **MySQL**
* **Aiven MySQL Cloud**
* **MySQL Workbench**

### APIs externas

* **TMDB API** para búsqueda e importación de películas.
* **QR Server API** para generar códigos QR de reservas.

### Control de versiones

* **Git**
* **GitHub**

---

## Funcionalidades principales

## 1. Cartelera pública

El sistema muestra las películas disponibles en cartelera desde el backend. Cada película contiene información como:

* Título
* Sinopsis
* Género
* Clasificación
* Duración
* Poster
* Fondo o backdrop
* Trailer
* Director
* Reparto
* Estado de la película

Las películas pueden estar en estado:

* `cartelera`
* `proximamente`
* `inactiva`

---

## 2. Detalle de película

Cada película cuenta con una página de detalle donde el usuario puede ver:

* Imagen principal
* Poster
* Sinopsis
* Género
* Clasificación
* Duración
* Director
* Reparto
* Trailer
* Funciones disponibles

Desde esta pantalla el usuario puede elegir:

* Sucursal
* Fecha
* Horario
* Sala

Luego puede continuar al proceso de reserva.

---

## 3. Proceso de reserva

El flujo de reserva está dividido en pasos:

1. **Cuenta**

   * El usuario puede continuar como invitado.
   * También puede iniciar sesión.
   * También puede registrarse.

2. **Asientos**

   * El usuario selecciona los asientos disponibles.
   * Los asientos ocupados aparecen como reservados.

3. **Comida y carrito**

   * El usuario puede agregar productos de comida y bebida.
   * Los productos se cargan desde la base de datos.

4. **Pago**

   * Se muestra un resumen de la reserva.
   * El método de pago configurado es “Pago en taquilla”.
   * El usuario confirma la reserva.

5. **Confirmación**

   * Se genera un código de reserva.
   * Se muestra un resumen del ticket.
   * Se genera un código QR.

---

## 4. Reservas como invitado

El sistema permite que un usuario pueda reservar sin tener una cuenta.

En este caso, la reserva se guarda con:

* Nombre del cliente
* Correo del cliente
* Teléfono del cliente
* Asientos seleccionados
* Función seleccionada
* Total de la reserva

En la base de datos, el campo `usuario_id` queda como `NULL`.

---

## 5. Reservas como cliente registrado

Si el usuario inicia sesión o se registra, sus reservas quedan relacionadas con su cuenta mediante el campo `usuario_id`.

Esto permite diferenciar reservas de invitados y reservas de clientes registrados.

---

## 6. Registro e inicio de sesión

El sistema cuenta con autenticación básica para:

* Clientes
* Administradores

El usuario puede:

* Crear cuenta
* Iniciar sesión
* Cerrar sesión
* Reservar con su cuenta

Después de registrarse, el sistema inicia sesión automáticamente.

---

## 7. Panel administrativo

El panel administrativo permite gestionar las partes principales del sistema.

Módulos disponibles:

* Películas
* Funciones
* Reservas
* Usuarios
* Sucursales
* Comidas
* Importación desde TMDB

Solo los usuarios con rol `admin` pueden acceder a este panel.

---

## 8. Administración de películas

Desde el panel de películas, el administrador puede:

* Ver películas registradas.
* Editar información de películas.
* Cambiar estado entre cartelera, próximamente o inactiva.
* Gestionar posters, trailers y datos básicos.
* Importar películas desde TMDB.

---

## 9. Administración de funciones

Desde el módulo de funciones, el administrador puede:

* Crear funciones.
* Editar funciones existentes.
* Eliminar funciones.
* Asignar película.
* Asignar sucursal.
* Definir fecha.
* Definir hora.
* Definir sala.
* Definir precio.

---

## 10. Administración de reservas

Desde el módulo de reservas, el administrador puede:

* Ver todas las reservas realizadas.
* Ver código de reserva.
* Ver cliente.
* Ver correo.
* Ver teléfono.
* Ver película.
* Ver sucursal.
* Ver fecha y hora.
* Ver asientos.
* Cambiar estado de reserva.

Estados disponibles:

* `pendiente`
* `confirmada`
* `cancelada`

---

## 11. Administración de usuarios

Desde el módulo de usuarios, el administrador puede:

* Ver usuarios registrados.
* Diferenciar clientes y administradores.
* Activar o desactivar usuarios.

---

## 12. Administración de sucursales

Desde el módulo de sucursales, el administrador puede:

* Crear sucursales.
* Editar sucursales.
* Activar o desactivar sucursales.
* Gestionar nombre, dirección y ciudad.

---

## 13. Administración de comidas

Desde el módulo de comidas, el administrador puede:

* Ver comidas y bebidas.
* Crear productos.
* Editar productos.
* Activar o desactivar productos.
* Definir nombre.
* Definir descripción.
* Definir precio.
* Definir imagen.

Las comidas se cargan desde la tabla `comidas` en la base de datos.

---

## 14. Integración con TMDB

El sistema incluye integración con TMDB para buscar e importar películas.

Desde el panel de administración, el administrador puede buscar películas externas y traer información como:

* Título
* Sinopsis
* Poster
* Fecha de estreno
* Rating
* Datos visuales

Para esta función se utiliza una variable de entorno llamada:

```env
TMDB_BEARER_TOKEN=TU_TOKEN_LARGO_DE_TMDB
```

---

## Base de datos

La base de datos utilizada se llama:

```sql
cine_reservas
```

El sistema utiliza las siguientes tablas principales:

* `usuarios`
* `peliculas`
* `sucursales`
* `funciones`
* `reservas`
* `asientos_reservados`
* `comidas`

---

## Estructura general de la base de datos

### usuarios

Guarda los usuarios registrados en el sistema.

Campos principales:

* `id`
* `nombre`
* `email`
* `password`
* `password_hash`
* `rol`
* `activo`
* `fecha_creacion`

---

### peliculas

Guarda la información de las películas.

Campos principales:

* `id`
* `tmdb_id`
* `titulo`
* `sinopsis`
* `genero`
* `clasificacion`
* `duracion_minutos`
* `poster_url`
* `backdrop_url`
* `trailer`
* `director`
* `reparto`
* `rating`
* `estado`
* `fecha_estreno`
* `activa`

---

### sucursales

Guarda las ubicaciones de los cines.

Campos principales:

* `id`
* `nombre`
* `direccion`
* `ciudad`
* `activa`

---

### funciones

Guarda los horarios disponibles.

Campos principales:

* `id`
* `pelicula_id`
* `sucursal_id`
* `fecha`
* `hora`
* `sala`
* `precio`

---

### reservas

Guarda las reservas realizadas.

Campos principales:

* `id`
* `usuario_id`
* `codigo_reserva`
* `funcion_id`
* `nombre_cliente`
* `email_cliente`
* `telefono_cliente`
* `cantidad_asientos`
* `total`
* `metodo_pago`
* `estado`
* `fecha_reserva`

---

### asientos_reservados

Guarda los asientos ocupados por reserva.

Campos principales:

* `id`
* `reserva_id`
* `funcion_id`
* `asiento`

---

### comidas

Guarda los productos de comida y bebida.

Campos principales:

* `id`
* `nombre`
* `descripcion`
* `precio`
* `imagen_url`
* `activa`
* `fecha_creacion`

---

## Archivo SQL completo

El proyecto incluye un archivo SQL completo para crear la base de datos desde cero:

```txt
backend/sql/000_full_schema_jc_cinemas.sql
```

Este archivo crea:

* La base de datos.
* Todas las tablas.
* Usuarios base.
* Películas base.
* Sucursales.
* Funciones.
* Comidas.

Importante: este archivo contiene `DROP DATABASE`, por lo tanto debe usarse solo cuando se quiera reiniciar la base de datos desde cero.

---

## Variables de entorno

El backend utiliza un archivo `.env` para conectarse a la base de datos y a TMDB.

Ejemplo:

```env
DB_HOST=jc-cinemas-mysql-cine-reservas.l.aivencloud.com
DB_PORT=10365
DB_USER=avnadmin
DB_PASSWORD=TU_PASSWORD_DE_AIVEN
DB_NAME=cine_reservas

TMDB_BEARER_TOKEN=TU_TOKEN_LARGO_DE_TMDB
```

Por seguridad, el archivo `.env` no debe subirse a GitHub.

El repositorio incluye un archivo de ejemplo:

```txt
backend/.env.example
```

---

## Credenciales de prueba

### Administrador

```txt
Correo: admin@jccinemas.com
Contraseña: admin123
```

### Cliente

```txt
Correo: cliente@jccinemas.com
Contraseña: cliente123
```

---

## Cómo ejecutar el proyecto

## 1. Clonar el repositorio

```powershell
git clone https://github.com/CHRIZZLERR/cine-reservas-app.git
cd cine-reservas-app
```

---

## 2. Configurar variables de entorno

Crear el archivo:

```txt
backend/.env
```

Agregar las variables correspondientes:

```env
DB_HOST=jc-cinemas-mysql-cine-reservas.l.aivencloud.com
DB_PORT=10365
DB_USER=avnadmin
DB_PASSWORD=TU_PASSWORD_DE_AIVEN
DB_NAME=cine_reservas

TMDB_BEARER_TOKEN=TU_TOKEN_LARGO_DE_TMDB
```

---

## 3. Ejecutar backend

Desde la raíz del proyecto:

```powershell
cd backend
uv run uvicorn app.main:app --reload
```

El backend se ejecuta en:

```txt
http://127.0.0.1:8000
```

La documentación de Swagger se encuentra en:

```txt
http://127.0.0.1:8000/docs
```

---

## 4. Ejecutar frontend

En otra terminal:

```powershell
cd frontend
uv run reflex run --frontend-port 3000 --backend-port 8001
```

El frontend se ejecuta en:

```txt
http://localhost:3000
```

---

## Rutas principales

### Rutas públicas

```txt
/
```

Página principal.

```txt
/cartelera
```

Películas en cartelera.

```txt
/proximamente
```

Películas próximas a estrenarse.

```txt
/ubicaciones
```

Sucursales disponibles.

```txt
/pelicula
```

Detalle de película.

```txt
/reservar
```

Flujo de reserva.

```txt
/auth
```

Login y registro.

---

### Rutas administrativas

```txt
/admin
```

Panel principal de administración.

```txt
/admin/peliculas
```

Administración de películas.

```txt
/admin/funciones
```

Administración de funciones.

```txt
/admin/reservas
```

Administración de reservas.

```txt
/admin/usuarios
```

Administración de usuarios.

```txt
/admin/sucursales
```

Administración de sucursales.

```txt
/admin/comidas
```

Administración de comidas y bebidas.

```txt
/admin/tmdb
```

Importación de películas desde TMDB.

---

## Endpoints principales del backend

### Películas

```txt
GET /peliculas
GET /admin/peliculas
POST /admin/peliculas
PUT /admin/peliculas/{pelicula_id}
DELETE /admin/peliculas/{pelicula_id}
```

### Funciones

```txt
GET /funciones
GET /admin/funciones
POST /admin/funciones
PUT /admin/funciones/{funcion_id}
DELETE /admin/funciones/{funcion_id}
```

### Reservas

```txt
GET /reservas
POST /reservas
GET /reservas/{codigo_reserva}
GET /funciones/{funcion_id}/asientos
PUT /admin/reservas/{reserva_id}/estado
```

### Usuarios

```txt
POST /auth/register
POST /auth/login
GET /auth/usuarios
PUT /admin/usuarios/{usuario_id}/estado
```

### Sucursales

```txt
GET /sucursales
GET /admin/sucursales
POST /admin/sucursales
PUT /admin/sucursales/{sucursal_id}
DELETE /admin/sucursales/{sucursal_id}
```

### Comidas

```txt
GET /comidas
GET /admin/comidas
POST /admin/comidas
PUT /admin/comidas/{comida_id}
DELETE /admin/comidas/{comida_id}
```

### TMDB

```txt
GET /tmdb/buscar
GET /tmdb/pelicula/{tmdb_id}
POST /admin/peliculas/importar-tmdb/{tmdb_id}
```

---

## Estado actual del proyecto

El proyecto cuenta actualmente con:

* Frontend funcional.
* Backend conectado con Aiven.
* Base de datos en la nube.
* Flujo de reserva completo.
* Login y registro.
* Panel administrativo.
* Módulo de películas.
* Módulo de funciones.
* Módulo de reservas.
* Módulo de usuarios.
* Módulo de sucursales.
* Módulo de comidas.
* Integración con TMDB.
* Archivo SQL completo.
* Variables de entorno de ejemplo.

---

## Recomendaciones de uso

* No subir el archivo `.env` a GitHub.
* No ejecutar el SQL completo si no se desea reiniciar la base de datos.
* Usar la rama `integracion-jc` como rama principal del proyecto funcional.
* Probar primero el backend antes de ejecutar el frontend.
* Confirmar que Aiven esté activo antes de presentar.

---

## Posibles mejoras futuras

* Agregar pago real con tarjeta.
* Agregar historial de reservas del cliente.
* Agregar recuperación de contraseña.
* Mejorar responsive para celulares.
* Agregar imágenes reales para comidas.
* Mejorar diseño visual de checkout.
* Crear salas VIP en vez de asientos VIP.
* Agregar notificaciones por correo.
* Agregar dashboard con estadísticas reales.
* Agregar filtros avanzados de cartelera.

---

## Integrantes

* Christopher Sánchez Mateo
* Jhoan

---

## Conclusión

JC Cinemas es un sistema de reservas de cine que integra frontend, backend, base de datos en la nube y consumo de API externa. El proyecto demuestra el uso de herramientas modernas para crear una aplicación funcional, organizada y escalable.

El sistema permite gestionar tanto la parte pública del cine como la parte administrativa, incluyendo películas, funciones, reservas, usuarios, sucursales y comidas. Además, el flujo de reserva permite trabajar con usuarios invitados y usuarios registrados, lo que hace que el proyecto sea más realista y completo.
