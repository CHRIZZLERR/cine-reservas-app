-- =============================================================
-- JC Cinemas - Esquema completo de base de datos
-- Archivo: 000_full_schema_jc_cinemas.sql
-- Uso: montar la base desde cero en MySQL / Aiven
-- ADVERTENCIA: este script borra y vuelve a crear la base cine_reservas.
-- =============================================================

DROP DATABASE IF EXISTS cine_reservas;
CREATE DATABASE cine_reservas
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cine_reservas;

-- =============================================================
-- TABLA: usuarios
-- =============================================================

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NULL DEFAULT NULL,
    password_hash VARCHAR(255) NULL DEFAULT NULL,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO usuarios (nombre, email, password, password_hash, rol, activo)
VALUES
('Administrador JC Cinemas', 'admin@jccinemas.com', 'admin123', 'admin123', 'admin', TRUE),
('Cliente de Prueba', 'cliente@jccinemas.com', 'cliente123', 'cliente123', 'cliente', TRUE);

-- =============================================================
-- TABLA: peliculas
-- =============================================================

CREATE TABLE peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id INT NULL,
    titulo VARCHAR(200) NOT NULL,
    sinopsis TEXT NULL,
    genero VARCHAR(150) NULL,
    clasificacion VARCHAR(20) NULL DEFAULT 'S/R',
    duracion_minutos INT NULL DEFAULT 0,
    poster_url TEXT NULL,
    backdrop_url TEXT NULL,
    trailer TEXT NULL,
    director VARCHAR(200) NULL,
    reparto TEXT NULL,
    rating DECIMAL(3,1) NULL DEFAULT 0.0,
    estado ENUM('cartelera', 'proximamente', 'inactiva') NOT NULL DEFAULT 'cartelera',
    fecha_estreno DATE NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO peliculas
(tmdb_id, titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, backdrop_url, trailer, director, reparto, rating, estado, fecha_estreno, activa)
VALUES
(NULL, 'Superman', 'Superman debe reconciliar su herencia kryptoniana con su crianza humana mientras protege al mundo.', 'Acción / Aventura', 'PG-13', 129,
'https://image.tmdb.org/t/p/w500/ombsmhYUqR4qqOLOxAyr5V8hbyv.jpg',
'https://image.tmdb.org/t/p/original/6izwz7rsy95ARzTR3poZ8H6c5pp.jpg',
'https://www.youtube.com/watch?v=uhUht6vAsMY', 'James Gunn', 'David Corenswet, Rachel Brosnahan, Nicholas Hoult', 7.0, 'cartelera', '2026-06-06', TRUE),

(NULL, 'F1: La Película', 'Un expiloto de Fórmula 1 regresa a las pistas para entrenar a una joven promesa y competir nuevamente.', 'Acción / Drama', 'PG-13', 155,
'https://image.tmdb.org/t/p/w500/9PXZIUsSDh4alB80jheWX4fhZmy.jpg',
'https://image.tmdb.org/t/p/original/6mF9g7F4F6kM2P1xH6zKc4s0p3Q.jpg',
'https://www.youtube.com/watch?v=DrE9umGiPZQ', 'Joseph Kosinski', 'Brad Pitt, Damson Idris, Kerry Condon', 7.5, 'cartelera', '2026-06-06', TRUE),

(NULL, 'Ballerina', 'Una asesina entrenada busca venganza mientras se adentra en un mundo criminal peligroso.', 'Acción / Suspenso', 'R', 125,
'https://image.tmdb.org/t/p/w500/2VUmvqsHb6cEtdfscEA6fqqVzLg.jpg',
'https://image.tmdb.org/t/p/original/7U3m1P7G4xQ5l9Tn9iMxD5Q6J9V.jpg',
'https://www.youtube.com/watch?v=0FSwsrFpkbw', 'Len Wiseman', 'Ana de Armas, Keanu Reeves, Ian McShane', 7.0, 'cartelera', '2026-06-06', TRUE),

(NULL, 'Jurassic World: El Renacimiento', 'Una nueva expedición busca revelar secretos de criaturas prehistóricas en una isla peligrosa.', 'Aventura / Ciencia ficción', 'PG-13', 134,
'https://image.tmdb.org/t/p/w500/q0fGCmjLu42MPlSO9OYWpI5w86I.jpg',
'https://image.tmdb.org/t/p/original/yAqL0makiGke5yYiVWpmBDSKIVP.jpg',
'https://www.youtube.com/watch?v=jan5CFWs9ic', 'Gareth Edwards', 'Scarlett Johansson, Jonathan Bailey, Mahershala Ali', 7.2, 'cartelera', '2026-06-06', TRUE),

(NULL, 'Mortal Kombat II', 'Los campeones favoritos de los fans se enfrentan en una batalla definitiva para detener el dominio de Shao Kahn.', 'Acción / Fantasía', 'R', 120,
'https://image.tmdb.org/t/p/w500/1GvBhRxY6MELDfxFrete6BNhBB5.jpg',
'https://image.tmdb.org/t/p/original/8eifdha9GQeZAkexgtD45546XKx.jpg',
'https://www.youtube.com/watch?v=H55FvcpS0hU', 'Simon McQuoid', 'Karl Urban, Adeline Rudolph, Jessica McNamee', 6.8, 'proximamente', '2026-06-10', TRUE),

(NULL, 'Star Wars: The Mandalorian and Grogu', 'El Mandaloriano y Grogu emprenden una nueva aventura por la galaxia enfrentando amenazas inesperadas.', 'Ciencia ficción / Aventura', 'PG-13', 130,
'https://via.placeholder.com/400x600/0f1320/ffffff?text=Star+Wars',
'https://via.placeholder.com/1200x700/0f1320/ffffff?text=Star+Wars',
'', 'Jon Favreau', 'Pedro Pascal, Grogu', 0.0, 'proximamente', '2026-06-09', TRUE);

-- =============================================================
-- TABLA: sucursales
-- =============================================================

CREATE TABLE sucursales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
VALUES
('Downtown Center', 'Av. Núñez de Cáceres, Santo Domingo', 'Santo Domingo', TRUE),
('Galería 360', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE),
('Ágora Mall', 'Av. Abraham Lincoln, Santo Domingo', 'Santo Domingo', TRUE),
('Blue Mall', 'Av. Winston Churchill, Santo Domingo', 'Santo Domingo', TRUE),
('Sambil', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE);

-- =============================================================
-- TABLA: funciones
-- =============================================================

CREATE TABLE funciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id INT NOT NULL,
    sucursal_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    sala VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_funciones_pelicula
        FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_funciones_sucursal
        FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)
        ON DELETE CASCADE,
    UNIQUE KEY uq_funcion_unica (pelicula_id, sucursal_id, fecha, hora, sala)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Funciones base para 2026-06-06
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
VALUES
-- Downtown Center
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '15:20:00', 'Sala 1', 475.00),
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '18:40:00', 'Sala 2', 500.00),
((SELECT id FROM peliculas WHERE titulo = 'Ballerina'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '19:20:00', 'Sala 5', 450.00),
((SELECT id FROM peliculas WHERE titulo = 'F1: La Película'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '16:00:00', 'Sala 3', 500.00),
((SELECT id FROM peliculas WHERE titulo = 'Jurassic World: El Renacimiento'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '17:45:00', 'Sala 4', 475.00),
((SELECT id FROM peliculas WHERE titulo = 'Mortal Kombat II'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '18:00:00', 'Sala 1', 500.00),
((SELECT id FROM peliculas WHERE titulo = 'Star Wars: The Mandalorian and Grogu'), (SELECT id FROM sucursales WHERE nombre = 'Downtown Center'), '2026-06-06', '20:00:00', 'Sala 7', 575.00),

-- Galería 360
((SELECT id FROM peliculas WHERE titulo = 'F1: La Película'), (SELECT id FROM sucursales WHERE nombre = 'Galería 360'), '2026-06-06', '18:00:00', 'Sala 2', 520.00),
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Galería 360'), '2026-06-06', '20:10:00', 'Sala 3', 525.00),

-- Ágora Mall
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Ágora Mall'), '2026-06-06', '15:30:00', 'Sala 1', 475.00),
((SELECT id FROM peliculas WHERE titulo = 'F1: La Película'), (SELECT id FROM sucursales WHERE nombre = 'Ágora Mall'), '2026-06-06', '18:20:00', 'Sala 2', 500.00),
((SELECT id FROM peliculas WHERE titulo = 'Ballerina'), (SELECT id FROM sucursales WHERE nombre = 'Ágora Mall'), '2026-06-06', '20:40:00', 'Sala 3', 450.00),

-- Blue Mall
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Blue Mall'), '2026-06-06', '16:10:00', 'Sala 1', 525.00),
((SELECT id FROM peliculas WHERE titulo = 'Jurassic World: El Renacimiento'), (SELECT id FROM sucursales WHERE nombre = 'Blue Mall'), '2026-06-06', '18:50:00', 'Sala 2', 500.00),
((SELECT id FROM peliculas WHERE titulo = 'Mortal Kombat II'), (SELECT id FROM sucursales WHERE nombre = 'Blue Mall'), '2026-06-06', '21:00:00', 'Sala 3', 525.00),

-- Sambil
((SELECT id FROM peliculas WHERE titulo = 'F1: La Película'), (SELECT id FROM sucursales WHERE nombre = 'Sambil'), '2026-06-06', '15:00:00', 'Sala 1', 450.00),
((SELECT id FROM peliculas WHERE titulo = 'Ballerina'), (SELECT id FROM sucursales WHERE nombre = 'Sambil'), '2026-06-06', '17:40:00', 'Sala 2', 475.00),
((SELECT id FROM peliculas WHERE titulo = 'Superman'), (SELECT id FROM sucursales WHERE nombre = 'Sambil'), '2026-06-06', '20:30:00', 'Sala 3', 500.00);

-- Copiar funciones base a dos fechas adicionales para simular cartelera real
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT pelicula_id, sucursal_id, '2026-06-07', hora, sala, precio
FROM funciones
WHERE fecha = '2026-06-06';

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT pelicula_id, sucursal_id, '2026-06-08', hora, sala, precio
FROM funciones
WHERE fecha = '2026-06-06';

-- =============================================================
-- TABLA: reservas
-- =============================================================

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    funcion_id INT NOT NULL,
    codigo_reserva VARCHAR(50) NULL UNIQUE,
    nombre_cliente VARCHAR(150) NOT NULL,
    email_cliente VARCHAR(150) NOT NULL,
    telefono_cliente VARCHAR(30) NULL,
    cantidad_asientos INT NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    metodo_pago VARCHAR(100) NULL DEFAULT 'Pago en taquilla',
    estado ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reservas_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_reservas_funcion
        FOREIGN KEY (funcion_id) REFERENCES funciones(id)
        ON DELETE CASCADE,
    INDEX idx_reservas_usuario_id (usuario_id),
    INDEX idx_reservas_funcion_id (funcion_id),
    INDEX idx_reservas_codigo (codigo_reserva)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- TABLA: asientos_reservados
-- =============================================================

CREATE TABLE asientos_reservados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    funcion_id INT NOT NULL,
    asiento VARCHAR(10) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_asientos_reserva
        FOREIGN KEY (reserva_id) REFERENCES reservas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_asientos_funcion
        FOREIGN KEY (funcion_id) REFERENCES funciones(id)
        ON DELETE CASCADE,
    UNIQUE KEY uq_asiento_funcion (funcion_id, asiento),
    INDEX idx_asientos_reserva_id (reserva_id),
    INDEX idx_asientos_funcion_id (funcion_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- TABLA: comidas
-- =============================================================

CREATE TABLE comidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    imagen_url TEXT NULL,
    categoria VARCHAR(100) NULL DEFAULT 'General',
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO comidas (nombre, descripcion, precio, imagen_url, categoria, activa)
VALUES
('Nachos Premium', 'Nachos con queso y salsa especial.', 280.00, 'https://via.placeholder.com/500x350/0f1320/ffffff?text=Nachos', 'Comida', TRUE),
('M&M / Peanuts', 'Dulce clásico para acompañar la película.', 150.00, 'https://via.placeholder.com/500x350/0f1320/ffffff?text=M%26M', 'Dulces', TRUE),
('Palomitas Grandes', 'Palomitas grandes recién preparadas.', 220.00, 'https://via.placeholder.com/500x350/0f1320/ffffff?text=Palomitas', 'Comida', TRUE),
('Refresco Grande', 'Bebida refrescante tamaño grande.', 130.00, 'https://via.placeholder.com/500x350/0f1320/ffffff?text=Refresco', 'Bebidas', TRUE);

-- =============================================================
-- CONSULTAS DE VERIFICACIÓN
-- =============================================================

SELECT 'usuarios' AS tabla, COUNT(*) AS total FROM usuarios
UNION ALL
SELECT 'peliculas' AS tabla, COUNT(*) AS total FROM peliculas
UNION ALL
SELECT 'sucursales' AS tabla, COUNT(*) AS total FROM sucursales
UNION ALL
SELECT 'funciones' AS tabla, COUNT(*) AS total FROM funciones
UNION ALL
SELECT 'reservas' AS tabla, COUNT(*) AS total FROM reservas
UNION ALL
SELECT 'asientos_reservados' AS tabla, COUNT(*) AS total FROM asientos_reservados
UNION ALL
SELECT 'comidas' AS tabla, COUNT(*) AS total FROM comidas;

SELECT
    s.nombre AS sucursal,
    COUNT(f.id) AS total_funciones
FROM sucursales s
LEFT JOIN funciones f ON f.sucursal_id = s.id
GROUP BY s.id, s.nombre
ORDER BY s.nombre;
