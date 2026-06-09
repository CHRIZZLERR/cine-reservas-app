# JC Cinemas - Plataforma Web de Reservas de Cine

## Proyecto Final - Desarrollo Web

**Nombre del proyecto:** JC Cinemas
**Tipo de proyecto:** Plataforma web de reservas
**Área:** Desarrollo Web, API REST y Base de Datos
**Rama principal funcional:** `integracion-jc`
**Repositorio:** `cine-reservas-app`

---

## Descripción general

**JC Cinemas** es una plataforma web desarrollada para gestionar reservas de cine de forma moderna, organizada y funcional. El sistema permite a los usuarios consultar películas disponibles, ver información detallada de cada película, seleccionar una sucursal, elegir fecha y horario, escoger asientos, agregar comida y bebida, y finalmente crear una reserva.

El proyecto fue desarrollado como una adaptación del tema original **“Plataforma de Reservas y Ofertas Turísticas”**, manteniendo la misma lógica principal: mostrar ofertas disponibles, consultar detalles, gestionar reservas y almacenar la información en una base de datos conectada a una API.

En este caso, las “ofertas turísticas” fueron adaptadas a un entorno de cine, donde las ofertas o actividades disponibles son las **películas, funciones, horarios, sucursales y servicios de comida**.

La plataforma incluye una parte pública para los clientes y un panel administrativo para gestionar el contenido del sistema.

---

## Objetivo del proyecto

El objetivo principal del proyecto es diseñar y desarrollar una página web funcional que permita gestionar reservas mediante una API conectada a una base de datos MySQL.

El sistema busca aplicar conocimientos de:

* Desarrollo web con Reflex.
* Creación de interfaces dinámicas.
* Diseño de una experiencia de usuario atractiva.
* Programación backend con FastAPI.
* Consumo de API REST.
* Conexión con base de datos MySQL.
* Uso de base de datos en la nube con Aiven.
* Control de versiones con Git y GitHub.
* Organización de ramas de trabajo.
* Documentación técnica del proyecto.

---

## Relación con los requisitos del proyecto

Aunque el proyecto original pedía una plataforma de reservas y ofertas turísticas, JC Cinemas mantiene la estructura funcional solicitada, adaptada a un sistema de reservas de cine.

| Requisito solicitado                 | Implementación en JC Cinemas                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Página de Inicio                     | Página principal con carrusel, cartelera destacada, próximos estrenos e información de la empresa |
| Página de Descripción                | Página de detalle de película con descripción, imagen, trailer, director, reparto y funciones     |
| Página de Reservas                   | Flujo completo de reserva con cuenta, asientos, comida, pago y confirmación                       |
| Formulario de búsqueda               | Búsqueda de películas por nombre, género o clasificación                                          |
| Ofertas con imágenes y descripciones | Películas en cartelera y próximas películas con imágenes, género y sinopsis                       |
| Contacto o información de la empresa | Footer con información del cine, horarios, contacto y sucursales                                  |
| API REST                             | Backend desarrollado con FastAPI                                                                  |
| Consultar ofertas                    | Endpoints para consultar películas, funciones, sucursales y comidas                               |
| Registrar reservas POST              | Endpoint `POST /reservas`                                                                         |
| Ver reservas GET                     | Endpoint `GET /reservas`                                                                          |
| Base de datos MySQL                  | Base de datos `cine_reservas` en Aiven MySQL                                                      |
| GitHub y control de versiones        | Proyecto subido a GitHub con ramas de trabajo                                                     |
| Documentación README                 | Este documento explica instalación, estructura, uso y funcionalidades                             |

---

## Tecnologías utilizadas

### Frontend

* **Reflex**
* **Python**
* **CSS personalizado**
* **Componentes dinámicos**
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
* **QR Server API** para generar códigos QR de las reservas.

### Control de versiones

* **Git**
* **GitHub**
* **Ramas de desarrollo**

---

## Funcionalidades principales

## 1. Página de inicio

La página de inicio presenta una vista general del cine y permite al usuario explorar el contenido disponible.

Incluye:

* Carrusel principal de películas.
* Películas destacadas en cartelera.
* Sección de próximos estrenos.
* Navegación hacia cartelera, ubicaciones, boletos y autenticación.
* Diseño visual con estilo cinematográfico.
* Footer con información de la empresa.

Esta página cumple la función de presentar las ofertas disponibles, que en este proyecto son las películas y funciones del cine.

---

## 2. Cartelera

La sección de cartelera permite ver las películas disponibles actualmente.

Cada película muestra información como:

* Título.
* Género.
* Clasificación.
* Duración.
* Fecha de estreno.
* Imagen o poster.
* Botón para ver detalles.

La cartelera se alimenta desde el backend mediante la API conectada a la base de datos.

---

## 3. Próximamente

La sección “Próximamente” muestra películas que aún no están disponibles para reserva, pero que forman parte del contenido del cine.

Esto permite separar las películas actuales de las futuras, simulando una plataforma real de cine.

---

## 4. Página de detalle de película

Cada película cuenta con una página individual de descripción.

Esta pantalla incluye:

* Poster de la película.
* Fondo o imagen principal.
* Título.
* Sinopsis.
* Género.
* Clasificación.
* Duración.
* Director.
* Reparto.
* Trailer.
* Funciones disponibles por sucursal, fecha y horario.

Esta sección cumple la función de “Página de Descripción” solicitada en el proyecto original.

---

## 5. Selección de función

Antes de reservar, el usuario debe elegir:

* Sucursal.
* Fecha.
* Horario.
* Sala.

El sistema valida que exista una función seleccionada antes de continuar al proceso de reserva.

Las funciones se consultan desde la base de datos y están relacionadas con películas y sucursales.

---

## 6. Flujo de reserva

El flujo de reserva está dividido en cuatro pasos principales:

### Paso 1: Cuenta

El usuario puede:

* Continuar como invitado.
* Iniciar sesión.
* Registrarse.

Si reserva como invitado, sus datos se guardan directamente en la reserva.
Si reserva como cliente registrado, la reserva queda relacionada con su usuario mediante `usuario_id`.

---

### Paso 2: Asientos

El usuario puede seleccionar los asientos disponibles.

El sistema:

* Muestra asientos disponibles.
* Marca asientos reservados.
* Evita reservar asientos ocupados.
* Guarda los asientos elegidos en la base de datos.

---

### Paso 3: Comida y carrito

El usuario puede agregar productos de comida y bebida.

Los productos se cargan desde la tabla `comidas` de la base de datos.

Ejemplos de productos:

* Nachos Premium.
* M&M / Peanuts.
* Palomitas Grandes.
* Refresco Grande.

El total de la reserva se actualiza según:

* Precio de boletos.
* Cantidad de asientos.
* Productos de comida.
* Cargo de servicio.

---

### Paso 4: Pago y confirmación

El sistema muestra un resumen final con:

* Película.
* Sucursal.
* Fecha.
* Hora.
* Asientos.
* Comidas seleccionadas.
* Total a pagar.
* Datos del cliente.

El método de pago usado actualmente es:

```txt
Pago en taquilla
```

Al confirmar, el sistema registra la reserva en la base de datos y genera un código de reserva.

---

## 7. Confirmación y código QR

Después de confirmar una reserva, el sistema muestra:

* Código de reserva.
* Resumen del ticket.
* Información de la película.
* Información de los asientos.
* Total pagado.
* Código QR.

El QR se genera usando una API externa, permitiendo simular un ticket real.

---

## 8. Sistema de usuarios

El sistema permite:

* Registrar usuarios.
* Iniciar sesión.
* Cerrar sesión.
* Diferenciar clientes y administradores.
* Guardar reservas asociadas a un usuario registrado.

Roles principales:

```txt
admin
cliente
```

---

## 9. Reservas como invitado

Un usuario puede reservar sin crear una cuenta.

En ese caso, la reserva se guarda con:

* Nombre del cliente.
* Correo electrónico.
* Teléfono.
* Asientos.
* Función.
* Total.

En la base de datos, el campo `usuario_id` queda como:

```sql
NULL
```

---

## 10. Reservas como cliente registrado

Cuando un cliente registrado realiza una reserva, el sistema guarda su `usuario_id`.

Esto permite identificar qué usuario realizó la reserva y simula una experiencia más realista.

---

## 11. Panel administrativo

El proyecto cuenta con un panel administrativo protegido por rol.

Solo los usuarios con rol `admin` pueden acceder.

Desde el panel se puede gestionar:

* Películas.
* Funciones.
* Reservas.
* Usuarios.
* Sucursales.
* Comidas.
* Importación desde TMDB.

---

## 12. Administración de películas

El administrador puede:

* Ver películas.
* Editar películas.
* Cambiar estado.
* Desactivar películas.
* Gestionar posters.
* Gestionar trailers.
* Modificar género, clasificación, duración y fecha de estreno.

Estados disponibles:

```txt
cartelera
proximamente
inactiva
```

---

## 13. Administración de funciones

El administrador puede crear y administrar horarios.

Cada función contiene:

* Película.
* Sucursal.
* Fecha.
* Hora.
* Sala.
* Precio.

Esto permite que una misma película tenga funciones en distintas sucursales, fechas y horarios.

---

## 14. Administración de reservas

El administrador puede consultar todas las reservas registradas.

Puede ver:

* Código de reserva.
* Cliente.
* Correo.
* Teléfono.
* Película.
* Sucursal.
* Fecha.
* Hora.
* Asientos.
* Total.
* Estado.

También puede cambiar el estado de una reserva.

Estados:

```txt
pendiente
confirmada
cancelada
```

---

## 15. Administración de usuarios

El administrador puede consultar los usuarios del sistema.

Puede ver:

* Nombre.
* Correo.
* Rol.
* Estado.
* Fecha de creación.

También puede activar o desactivar usuarios.

---

## 16. Administración de sucursales

El sistema permite gestionar las ubicaciones del cine.

Cada sucursal contiene:

* Nombre.
* Dirección.
* Ciudad.
* Estado activo o inactivo.

Sucursales usadas en el proyecto:

* Downtown Center.
* Galería 360.
* Ágora Mall.
* Blue Mall.
* Sambil.

---

## 17. Administración de comidas

El módulo de comidas permite gestionar productos de comida y bebida.

El administrador puede:

* Ver productos.
* Crear productos.
* Editar productos.
* Activar o desactivar productos.
* Definir precio.
* Definir descripción.
* Definir imagen.

Los productos activos aparecen en el checkout durante la reserva.

---

## 18. Integración con TMDB

El sistema incluye integración con TMDB para buscar e importar películas.

El administrador puede buscar películas y traer información como:

* Título.
* Sinopsis.
* Poster.
* Rating.
* Fecha de estreno.
* Datos generales.

Para usar esta función se requiere configurar:

```env
TMDB_BEARER_TOKEN=TU_TOKEN_LARGO_DE_TMDB
```

---

## API REST

El backend fue desarrollado con FastAPI y expone endpoints para consultar información y gestionar reservas.

La documentación automática se puede ver en:

```txt
http://127.0.0.1:8000/docs
```

---

## Endpoints principales

### Sistema

```txt
GET /
```

Verifica que la API esté funcionando.

---

### Películas

```txt
GET /peliculas
GET /peliculas/{pelicula_id}
GET /peliculas/{pelicula_id}/funciones
GET /admin/peliculas
POST /admin/peliculas
PUT /admin/peliculas/{pelicula_id}
DELETE /admin/peliculas/{pelicula_id}
```

---

### Funciones

```txt
GET /funciones
GET /admin/funciones
POST /admin/funciones
PUT /admin/funciones/{funcion_id}
DELETE /admin/funciones/{funcion_id}
```

---

### Reservas

```txt
GET /reservas
POST /reservas
GET /reservas/{codigo_reserva}
GET /funciones/{funcion_id}/asientos
PUT /admin/reservas/{reserva_id}/estado
```

---

### Usuarios y autenticación

```txt
POST /auth/register
POST /auth/login
GET /auth/usuarios
PUT /admin/usuarios/{usuario_id}/estado
```

---

### Sucursales

```txt
GET /sucursales
GET /admin/sucursales
POST /admin/sucursales
PUT /admin/sucursales/{sucursal_id}
DELETE /admin/sucursales/{sucursal_id}
```

---

### Comidas

```txt
GET /comidas
GET /admin/comidas
POST /admin/comidas
PUT /admin/comidas/{comida_id}
DELETE /admin/comidas/{comida_id}
```

---

### TMDB

```txt
GET /tmdb/buscar
GET /tmdb/pelicula/{tmdb_id}
POST /admin/peliculas/importar-tmdb/{tmdb_id}
```

---

## Base de datos

La base de datos utilizada se llama:

```sql
cine_reservas
```

Está alojada en Aiven MySQL.

---

## Tablas principales

### usuarios

Guarda los usuarios del sistema.

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

Guarda las películas disponibles.

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

Guarda las ubicaciones.

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

Guarda los asientos ocupados por cada reserva.

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

## Archivo SQL del proyecto

El proyecto incluye un script SQL completo:

```txt
backend/sql/000_full_schema_jc_cinemas.sql
```

Este archivo permite crear la base de datos desde cero.

Incluye:

* Creación de base de datos.
* Creación de tablas.
* Relaciones entre tablas.
* Usuarios base.
* Películas base.
* Sucursales base.
* Funciones base.
* Comidas base.

Advertencia: este archivo contiene instrucciones para reiniciar la base de datos. No debe ejecutarse si se desea conservar las reservas actuales.

---

## Estructura de carpetas

```txt
cine-reservas-app/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   └── conexion.py
│   │   │
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── peliculas.py
│   │   │   ├── funciones.py
│   │   │   ├── reservas.py
│   │   │   ├── sucursales.py
│   │   │   ├── comidas.py
│   │   │   └── tmdb.py
│   │   │
│   │   └── main.py
│   │
│   ├── sql/
│   │   ├── 000_full_schema_jc_cinemas.sql
│   │   ├── 001_add_tmdb_fields.sql
│   │   ├── 002_clean_duplicate_funciones.sql
│   │   ├── 002_create_usuarios.sql
│   │   └── seed_datos_jc_cinemas.sql
│   │
│   └── .env.example
│
├── frontend/
│   ├── frontend/
│   │   ├── components/
│   │   │   ├── navbar.py
│   │   │   ├── movie_card.py
│   │   │   ├── movie_detail.py
│   │   │   ├── schedule.py
│   │   │   ├── seat_map.py
│   │   │   ├── food_menu.py
│   │   │   ├── booking_summary.py
│   │   │   └── footer.py
│   │   │
│   │   ├── pages/
│   │   │   ├── home.py
│   │   │   ├── pelicula.py
│   │   │   ├── reserva.py
│   │   │   ├── auth.py
│   │   │   ├── admin.py
│   │   │   ├── admin_peliculas.py
│   │   │   ├── admin_funciones.py
│   │   │   ├── admin_reservas.py
│   │   │   ├── admin_usuarios.py
│   │   │   ├── admin_sucursales.py
│   │   │   ├── admin_comidas.py
│   │   │   └── admin_tmdb.py
│   │   │
│   │   ├── state.py
│   │   ├── data.py
│   │   ├── config.py
│   │   └── frontend.py
│   │
│   └── assets/
│       └── style.css
│
├── README.md
└── .gitignore
```

---

## Variables de entorno

El proyecto necesita un archivo `.env` dentro de la carpeta `backend`.

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

---

## Archivo de ejemplo

El repositorio incluye:

```txt
backend/.env.example
```

Este archivo sirve como guía para crear el `.env` local.

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

## Instalación y ejecución

## 1. Clonar el repositorio

```powershell
git clone https://github.com/CHRIZZLERR/cine-reservas-app.git
cd cine-reservas-app
```

---

## 2. Configurar backend

Entrar a la carpeta del backend:

```powershell
cd backend
```

Crear el archivo `.env` usando como referencia:

```txt
backend/.env.example
```

Ejemplo de configuración:

```env
DB_HOST=jc-cinemas-mysql-cine-reservas.l.aivencloud.com
DB_PORT=10365
DB_USER=avnadmin
DB_PASSWORD=TU_PASSWORD_DE_AIVEN
DB_NAME=cine_reservas

TMDB_BEARER_TOKEN=TU_TOKEN_LARGO_DE_TMDB
```

Ejecutar el backend:

```powershell
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

```txt
http://127.0.0.1:8000
```

Swagger estará disponible en:

```txt
http://127.0.0.1:8000/docs
```

---

## 3. Configurar frontend

En otra terminal, desde la raíz del proyecto:

```powershell
cd frontend
```

Ejecutar el frontend:

```powershell
uv run reflex run --frontend-port 3000 --backend-port 8001
```

La aplicación estará disponible en:

```txt
http://localhost:3000
```

---

## Despliegue

El requisito del proyecto solicita desplegar el proyecto en Render.

La estructura recomendada para despliegue es:

* Backend FastAPI desplegado como Web Service en Render.
* Frontend Reflex publicado según la configuración disponible.
* Base de datos MySQL alojada en Aiven.

Enlaces de despliegue:

```txt
Frontend: Pendiente / colocar enlace final
Backend: Pendiente / colocar enlace final
Repositorio GitHub: https://github.com/CHRIZZLERR/cine-reservas-app
```

Nota: si el proyecto se presenta localmente, debe verificarse que el backend y frontend estén corriendo correctamente antes de la exposición.

---

## Control de versiones y ramas

El proyecto fue trabajado con Git y GitHub.

Ramas usadas durante el desarrollo:

* `main`
* `chris`
* `jhoan`
* `configurar-aiven`
* `chris-ajustes-finales`
* `integracion-jc`

La rama principal funcional para la entrega es:

```txt
integracion-jc
```

---

## Pruebas recomendadas antes de presentar

Antes de presentar el proyecto, se recomienda probar:

1. Cargar página de inicio.
2. Entrar a cartelera.
3. Ver detalle de una película.
4. Seleccionar sucursal, fecha y horario.
5. Reservar como invitado.
6. Reservar como cliente registrado.
7. Registrar un usuario nuevo.
8. Iniciar sesión como administrador.
9. Entrar al panel de administración.
10. Revisar películas.
11. Revisar funciones.
12. Revisar reservas.
13. Revisar usuarios.
14. Revisar sucursales.
15. Revisar comidas.
16. Probar Swagger en `/docs`.

---

## Estado final del proyecto

Actualmente el proyecto cuenta con:

* Página de inicio.
* Página de cartelera.
* Página de próximos estrenos.
* Página de ubicaciones.
* Página de detalle de película.
* Página de reservas.
* Login.
* Registro.
* Reservas como invitado.
* Reservas como cliente.
* Generación de código de reserva.
* Generación de QR.
* Panel de administración.
* Administración de películas.
* Administración de funciones.
* Administración de reservas.
* Administración de usuarios.
* Administración de sucursales.
* Administración de comidas.
* Integración con TMDB.
* API REST.
* Base de datos MySQL en Aiven.
* Archivo SQL completo.
* Control de versiones en GitHub.

---

## Posibles mejoras futuras

Algunas mejoras que podrían agregarse en el futuro son:

* Integrar pagos reales.
* Agregar historial de reservas por cliente.
* Crear recuperación de contraseña.
* Agregar envío automático de correo.
* Mejorar diseño responsive en celulares.
* Agregar imágenes reales de comidas.
* Crear salas VIP en vez de asientos VIP.
* Agregar dashboard con estadísticas reales.
* Agregar reportes administrativos.
* Agregar filtros avanzados de cartelera.
* Mejorar despliegue final en Render.

---

## Créditos

Proyecto desarrollado por:

* Christopher Sánchez Mateo
* Jhoan

---

## Enlaces útiles

* Repositorio GitHub: `https://github.com/CHRIZZLERR/cine-reservas-app`
* FastAPI Docs local: `http://127.0.0.1:8000/docs`
* Frontend local: `http://localhost:3000`
* TMDB: `https://www.themoviedb.org/`
* Aiven: `https://aiven.io/`
* Reflex: `https://reflex.dev/`
* FastAPI: `https://fastapi.tiangolo.com/`

---

## Conclusión

JC Cinemas es una plataforma web funcional que integra frontend, backend, base de datos y API externa. El proyecto cumple con la lógica principal solicitada en el proyecto final: mostrar ofertas o actividades disponibles, permitir consultar detalles, registrar reservas, almacenar información en una base de datos y gestionar datos mediante una API.

Aunque el tema fue adaptado de turismo a cine, la estructura técnica se mantiene alineada con los requisitos: existe una página de inicio, una página de descripción, una página de reservas, una API REST, conexión a MySQL, registro de reservas, consulta de reservas, control de versiones en GitHub y documentación del sistema.

Este proyecto demuestra la integración de varias áreas del desarrollo web y presenta una base funcional para seguir mejorándolo en el futuro.
