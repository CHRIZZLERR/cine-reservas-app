-- =====================================================
-- 000 - ESQUEMA COMPLETO DE BASE DE DATOS
-- JC Cinemas / Cine Reservas App
-- =====================================================
-- Uso recomendado:
-- 1. Abrir este archivo en MySQL Workbench.
-- 2. Ejecutarlo completo.
-- 3. Luego ejecutar, si aplica:
--    - backend/sql/001_add_tmdb_fields.sql
--    - backend/sql/seed_datos_jc_cinemas.sql
--    - backend/sql/002_create_usuarios.sql
--
-- Este archivo crea la estructura base necesaria para que funcionen:
-- peliculas, sucursales, funciones, reservas, asientos_reservados,
-- usuarios y comidas.
-- =====================================================

CREATE DATABASE IF NOT EXISTS cine_reservas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE cine_reservas;

SET SQL_SAFE_UPDATES = 0;

-- =====================================================
-- TABLA: usuarios
-- =====================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Compatibilidad por si algún script anterior usó password_hash
ALTER TABLE usuarios
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255) NULL AFTER password;

-- Admin base
INSERT INTO usuarios (nombre, email, password_hash, rol, activo)
SELECT
    'Administrador JC Cinemas',
    'admin@jccinemas.com',
    'admin123',
    'admin',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 
    FROM usuarios 
    WHERE email = 'admin@jccinemas.com'
);

-- =====================================================
-- TABLA: peliculas
-- =====================================================

CREATE TABLE IF NOT EXISTS peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id INT NULL UNIQUE,
    titulo VARCHAR(200) NOT NULL,
    sinopsis TEXT NULL,
    genero VARCHAR(120) NULL,
    clasificacion VARCHAR(30) NULL,
    duracion_minutos INT NULL DEFAULT 0,
    poster_url TEXT NULL,
    backdrop_url TEXT NULL,
    trailer TEXT NULL,
    director VARCHAR(180) NULL,
    reparto TEXT NULL,
    rating DECIMAL(3,1) NULL DEFAULT 0.0,
    estado ENUM('cartelera', 'proximamente', 'inactiva') NOT NULL DEFAULT 'cartelera',
    fecha_estreno DATE NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_peliculas_estado (estado),
    INDEX idx_peliculas_activa (activa),
    INDEX idx_peliculas_titulo (titulo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: sucursales
-- =====================================================

CREATE TABLE IF NOT EXISTS sucursales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(120) NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sucursales_activa (activa),
    INDEX idx_sucursales_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: funciones
-- =====================================================

CREATE TABLE IF NOT EXISTS funciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id INT NOT NULL,
    sucursal_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    sala VARCHAR(80) NOT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_funciones_pelicula
        FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_funciones_sucursal
        FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX idx_funciones_pelicula (pelicula_id),
    INDEX idx_funciones_sucursal (sucursal_id),
    INDEX idx_funciones_fecha (fecha),
    INDEX idx_funciones_activa (activa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Evitar duplicados exactos de funciones
CREATE UNIQUE INDEX uq_funcion_unica
ON funciones (pelicula_id, sucursal_id, fecha, hora, sala);

-- =====================================================
-- TABLA: reservas
-- =====================================================

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_reserva VARCHAR(50) NULL UNIQUE,
    funcion_id INT NOT NULL,
    nombre_cliente VARCHAR(150) NOT NULL,
    email_cliente VARCHAR(150) NOT NULL,
    telefono_cliente VARCHAR(50) NULL,
    cantidad_asientos INT NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    metodo_pago VARCHAR(100) NOT NULL DEFAULT 'Pago en taquilla',
    estado ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    fecha_reserva TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reservas_funcion
        FOREIGN KEY (funcion_id) REFERENCES funciones(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX idx_reservas_codigo (codigo_reserva),
    INDEX idx_reservas_funcion (funcion_id),
    INDEX idx_reservas_estado (estado),
    INDEX idx_reservas_fecha (fecha_reserva)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: asientos_reservados
-- =====================================================

CREATE TABLE IF NOT EXISTS asientos_reservados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    funcion_id INT NOT NULL,
    asiento VARCHAR(10) NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_asientos_reserva
        FOREIGN KEY (reserva_id) REFERENCES reservas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_asientos_funcion
        FOREIGN KEY (funcion_id) REFERENCES funciones(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    UNIQUE KEY uq_asiento_por_funcion (funcion_id, asiento),
    INDEX idx_asientos_reserva (reserva_id),
    INDEX idx_asientos_funcion (funcion_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: comidas
-- =====================================================
-- Esta tabla queda lista para el módulo de dulcería.
-- Aunque el frontend todavía pueda usar data.py, aquí queda la estructura
-- para conectar GET /comidas y CRUD admin después.
-- =====================================================

CREATE TABLE IF NOT EXISTS comidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    categoria VARCHAR(80) NOT NULL DEFAULT 'Dulcería',
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    imagen_url TEXT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_comidas_activa (activa),
    INDEX idx_comidas_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DATOS BASE: sucursales
-- =====================================================

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Downtown Center', 'Av. Núñez de Cáceres, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (SELECT 1 FROM sucursales WHERE nombre = 'Downtown Center');

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Galería 360', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (SELECT 1 FROM sucursales WHERE nombre = 'Galería 360');

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Ágora Mall', 'Av. Abraham Lincoln, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (SELECT 1 FROM sucursales WHERE nombre = 'Ágora Mall');

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Blue Mall', 'Av. Winston Churchill, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (SELECT 1 FROM sucursales WHERE nombre = 'Blue Mall');

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Sambil', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (SELECT 1 FROM sucursales WHERE nombre = 'Sambil');

-- =====================================================
-- DATOS BASE: películas
-- =====================================================

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    1061474,
    'Superman',
    'Superman debe reconciliar su herencia kryptoniana con su crianza humana mientras protege al mundo.',
    'Acción / Aventura',
    'PG-13',
    129,
    'https://image.tmdb.org/t/p/w500/ombsmhYUqR4qqOLOxAyr5V8hbyv.jpg',
    'https://image.tmdb.org/t/p/w1280/2Nti3gYAX513wvhp8IiLL6ZDyOm.jpg',
    'https://www.youtube.com/watch?v=uhUht6vAsMY',
    '',
    '',
    7.0,
    'cartelera',
    '2026-06-06',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Superman');

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    911430,
    'F1: La Película',
    'Un piloto retirado regresa a las pistas para entrenar a una nueva promesa de la Fórmula 1.',
    'Acción / Drama',
    'PG-13',
    155,
    'https://image.tmdb.org/t/p/w500/6H6p82aWQFEKEuVUiZll6JxV8Ft.jpg',
    'https://image.tmdb.org/t/p/w1280/7Zx3wDG5bBtcfk8lcnCWDOLM4Y4.jpg',
    '',
    '',
    '',
    7.0,
    'cartelera',
    '2026-06-06',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'F1: La Película');

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    541671,
    'Ballerina',
    'Una asesina entrenada busca venganza mientras se adentra en un mundo criminal peligroso.',
    'Acción / Suspenso',
    'R',
    125,
    'https://image.tmdb.org/t/p/w500/2VUmvqsHb6cEtdfscEA6fqqVzLg.jpg',
    'https://image.tmdb.org/t/p/w1280/7HqLLVjdjhXS0Qoz1SgZofhkIpE.jpg',
    '',
    '',
    '',
    7.0,
    'cartelera',
    '2026-06-06',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Ballerina');

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    1234821,
    'Jurassic World: El Renacimiento',
    'Una nueva etapa inicia cuando los dinosaurios vuelven a cambiar el equilibrio del mundo.',
    'Aventura / Ciencia ficción',
    'PG-13',
    134,
    'https://image.tmdb.org/t/p/w500/q0fGCmjLu42MPlSO9OYWpI5w86I.jpg',
    'https://image.tmdb.org/t/p/w1280/2Nti3gYAX513wvhp8IiLL6ZDyOm.jpg',
    '',
    '',
    '',
    7.0,
    'cartelera',
    '2026-06-06',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Jurassic World: El Renacimiento');

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    1038392,
    'Mortal Kombat II',
    'Los guerreros se preparan para una batalla brutal que decidirá el destino de los reinos.',
    'Acción / Fantasía',
    'R',
    120,
    'https://image.tmdb.org/t/p/w500/8fYluTtB3b3HKO7KQa5tzrvGaps.jpg',
    'https://image.tmdb.org/t/p/w1280/rthMuZfFv4fqEU4JVbgSW9wQ8rs.jpg',
    '',
    '',
    '',
    7.0,
    'proximamente',
    '2026-06-10',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Mortal Kombat II');

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
SELECT
    1084242,
    'Star Wars: The Mandalorian and Grogu',
    'Una nueva aventura galáctica sigue al Mandaloriano y Grogu en una misión decisiva.',
    'Ciencia ficción / Aventura',
    'PG-13',
    130,
    'https://image.tmdb.org/t/p/w500/placeholder.jpg',
    '',
    '',
    '',
    '',
    7.0,
    'proximamente',
    '2026-06-09',
    TRUE
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Star Wars: The Mandalorian and Grogu');

-- =====================================================
-- DATOS BASE: funciones
-- =====================================================

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '15:20:00', 'Sala 1', 475.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Superman' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '18:40:00', 'Sala 2', 500.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Superman' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '20:10:00', 'Sala 3', 525.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Superman' AND s.nombre = 'Galería 360';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '16:00:00', 'Sala 3', 500.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'F1: La Película' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '18:00:00', 'Sala 2', 520.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'F1: La Película' AND s.nombre = 'Galería 360';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '19:20:00', 'Sala 5', 450.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Ballerina' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '17:45:00', 'Sala 4', 475.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Jurassic World: El Renacimiento' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '18:00:00', 'Sala 1', 500.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Mortal Kombat II' AND s.nombre = 'Downtown Center';

INSERT IGNORE INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '20:00:00', 'Sala 7', 575.00
FROM peliculas p, sucursales s
WHERE p.titulo = 'Star Wars: The Mandalorian and Grogu' AND s.nombre = 'Downtown Center';

-- =====================================================
-- DATOS BASE: comidas
-- =====================================================

INSERT INTO comidas (nombre, descripcion, categoria, precio, imagen_url, activa)
SELECT 'Palomitas Grandes', 'Palomitas clásicas tamaño grande.', 'Palomitas', 250.00, 'https://images.unsplash.com/photo-1578849278619-e73505e9610f', TRUE
WHERE NOT EXISTS (SELECT 1 FROM comidas WHERE nombre = 'Palomitas Grandes');

INSERT INTO comidas (nombre, descripcion, categoria, precio, imagen_url, activa)
SELECT 'Nachos con Queso', 'Nachos crujientes con salsa de queso.', 'Snacks', 300.00, 'https://images.unsplash.com/photo-1513456852971-30c0b8199d4d', TRUE
WHERE NOT EXISTS (SELECT 1 FROM comidas WHERE nombre = 'Nachos con Queso');

INSERT INTO comidas (nombre, descripcion, categoria, precio, imagen_url, activa)
SELECT 'Refresco Grande', 'Bebida refrescante tamaño grande.', 'Bebidas', 180.00, 'https://images.unsplash.com/photo-1581006852262-e4307cf6283a', TRUE
WHERE NOT EXISTS (SELECT 1 FROM comidas WHERE nombre = 'Refresco Grande');

INSERT INTO comidas (nombre, descripcion, categoria, precio, imagen_url, activa)
SELECT 'Combo Pareja', 'Dos refrescos y una palomita grande.', 'Combos', 650.00, 'https://images.unsplash.com/photo-1512149177596-f817c7ef5d4c', TRUE
WHERE NOT EXISTS (SELECT 1 FROM comidas WHERE nombre = 'Combo Pareja');

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================

SELECT 'usuarios' AS tabla, COUNT(*) AS total FROM usuarios
UNION ALL
SELECT 'peliculas', COUNT(*) FROM peliculas
UNION ALL
SELECT 'sucursales', COUNT(*) FROM sucursales
UNION ALL
SELECT 'funciones', COUNT(*) FROM funciones
UNION ALL
SELECT 'reservas', COUNT(*) FROM reservas
UNION ALL
SELECT 'asientos_reservados', COUNT(*) FROM asientos_reservados
UNION ALL
SELECT 'comidas', COUNT(*) FROM comidas;

SET SQL_SAFE_UPDATES = 1;
