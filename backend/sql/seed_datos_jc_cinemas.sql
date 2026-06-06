USE cine_reservas;

SET SQL_SAFE_UPDATES = 0;

-- =====================================================
-- SEED OFICIAL - JC CINEMAS
-- Sucursales y funciones iniciales
-- =====================================================

-- Este archivo NO inserta películas falsas.
-- Las películas deben importarse desde TMDB usando:
-- POST /admin/peliculas/importar-tmdb/{tmdb_id}
--
-- Luego este seed crea funciones para las películas existentes.

-- =====================================================
-- 1. SUCURSALES
-- =====================================================

-- Limpia nombres viejos de CineMax si existen.
UPDATE sucursales
SET nombre = REPLACE(nombre, 'CineMax ', '')
WHERE nombre LIKE 'CineMax %';

-- Inserta sucursales si no existen.
INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Downtown Center', 'Av. Núñez de Cáceres, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM sucursales WHERE nombre = 'Downtown Center'
);

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Galería 360', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM sucursales WHERE nombre = 'Galería 360'
);

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Ágora Mall', 'Av. Abraham Lincoln, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM sucursales WHERE nombre = 'Ágora Mall'
);

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Blue Mall', 'Av. Winston Churchill, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM sucursales WHERE nombre = 'Blue Mall'
);

INSERT INTO sucursales (nombre, direccion, ciudad, activa)
SELECT 'Sambil', 'Av. John F. Kennedy, Santo Domingo', 'Santo Domingo', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM sucursales WHERE nombre = 'Sambil'
);

UPDATE sucursales
SET activa = TRUE
WHERE nombre IN ('Downtown Center', 'Galería 360', 'Ágora Mall', 'Blue Mall', 'Sambil');

-- =====================================================
-- 2. FUNCIONES PARA PELÍCULAS EN CARTELERA
-- =====================================================

-- Limpia funciones futuras de prueba repetidas para evitar duplicados raros.
-- No borra reservas existentes.
DELETE f
FROM funciones f
LEFT JOIN reservas r ON r.funcion_id = f.id
WHERE r.id IS NULL
AND f.fecha BETWEEN '2026-06-06' AND '2026-06-10';

-- =====================================================
-- MORTAL KOMBAT II
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '18:00:00', 'Sala 1', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '18:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '21:00:00', 'Sala 2', 550.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '21:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '20:45:00', 'Sala 2', 550.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '20:45:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '19:30:00', 'Sala 2', 520.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Galería 360'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '19:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-08', '18:30:00', 'Sala VIP 1', 650.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Ágora Mall'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-08'
    AND f.hora = '18:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-09', '21:20:00', 'Sala VIP 2', 675.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Blue Mall'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-09'
    AND f.hora = '21:20:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-10', '20:00:00', 'Sala 3', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Sambil'
WHERE p.titulo = 'Mortal Kombat II'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-10'
    AND f.hora = '20:00:00'
);

-- =====================================================
-- SUPERMAN
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '15:20:00', 'Sala 1', 475.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '15:20:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '18:40:00', 'Sala 2', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '18:40:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '20:10:00', 'Sala 3', 525.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Galería 360'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '20:10:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-08', '19:00:00', 'Sala VIP 1', 650.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Ágora Mall'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-08'
    AND f.hora = '19:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-09', '21:30:00', 'Sala VIP 2', 675.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Blue Mall'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-09'
    AND f.hora = '21:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-10', '16:40:00', 'Sala 4', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Sambil'
WHERE p.titulo LIKE 'Superman%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-10'
    AND f.hora = '16:40:00'
);

-- =====================================================
-- F1: LA PELÍCULA
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '16:00:00', 'Sala 3', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'F1%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '16:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '18:00:00', 'Sala 2', 520.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Galería 360'
WHERE p.titulo LIKE 'F1%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '18:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-08', '20:30:00', 'Sala VIP 1', 650.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Ágora Mall'
WHERE p.titulo LIKE 'F1%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-08'
    AND f.hora = '20:30:00'
);

-- =====================================================
-- JURASSIC WORLD
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '17:45:00', 'Sala 4', 475.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'Jurassic%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '17:45:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '21:10:00', 'Sala 3', 525.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Galería 360'
WHERE p.titulo LIKE 'Jurassic%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '21:10:00'
);

-- =====================================================
-- BALLERINA
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '19:20:00', 'Sala 5', 450.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'Ballerina%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '19:20:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-08', '22:00:00', 'Sala VIP 2', 625.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Blue Mall'
WHERE p.titulo LIKE 'Ballerina%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-08'
    AND f.hora = '22:00:00'
);

-- =====================================================
-- DE TAL PALO, TAL ASTILLA
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '18:15:00', 'Sala 6', 400.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'De tal palo%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '18:15:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-07', '20:30:00', 'Sala 4', 425.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Sambil'
WHERE p.titulo LIKE 'De tal palo%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-07'
    AND f.hora = '20:30:00'
);

-- =====================================================
-- STAR WARS
-- =====================================================

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-06', '20:00:00', 'Sala 7', 500.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Downtown Center'
WHERE p.titulo LIKE 'Star Wars%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-06'
    AND f.hora = '20:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, s.id, '2026-06-09', '21:00:00', 'Sala VIP 1', 675.00
FROM peliculas p
INNER JOIN sucursales s ON s.nombre = 'Ágora Mall'
WHERE p.titulo LIKE 'Star Wars%'
AND p.activa = TRUE
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = s.id
    AND f.fecha = '2026-06-09'
    AND f.hora = '21:00:00'
);

-- =====================================================
-- 3. VERIFICACIÓN
-- =====================================================

SET SQL_SAFE_UPDATES = 1;

SELECT
    id,
    nombre,
    direccion,
    ciudad,
    activa
FROM sucursales
ORDER BY id;

SELECT
    id,
    tmdb_id,
    titulo,
    genero,
    clasificacion,
    duracion_minutos,
    estado,
    activa
FROM peliculas
ORDER BY estado, titulo;

SELECT
    f.id,
    p.titulo AS pelicula,
    s.nombre AS sucursal,
    f.fecha,
    f.hora,
    f.sala,
    f.precio
FROM funciones f
INNER JOIN peliculas p ON f.pelicula_id = p.id
INNER JOIN sucursales s ON f.sucursal_id = s.id
ORDER BY p.titulo, s.nombre, f.fecha, f.hora;