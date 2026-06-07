USE cine_reservas;

-- =====================================================
-- 002 - LIMPIEZA REAL DE FUNCIONES REPETIDAS
-- JC Cinemas
-- =====================================================
-- Esta versión limpia duplicados VISUALES, no solo exactos.
--
-- Considera duplicada una función si tiene:
-- - Mismo título de película
-- - Misma sucursal
-- - Misma fecha
-- - Misma hora
-- - Misma sala
--
-- No borra funciones que tengan reservas asociadas.
-- =====================================================

SET SQL_SAFE_UPDATES = 0;

-- =====================================================
-- 1. VER FUNCIONES REPETIDAS POR TÍTULO
-- =====================================================

SELECT
    p.titulo AS pelicula,
    s.nombre AS sucursal,
    f.fecha,
    f.hora,
    f.sala,
    COUNT(*) AS cantidad,
    GROUP_CONCAT(f.id ORDER BY f.id ASC) AS funciones_ids,
    GROUP_CONCAT(f.pelicula_id ORDER BY f.id ASC) AS peliculas_ids,
    GROUP_CONCAT(f.precio ORDER BY f.id ASC) AS precios
FROM funciones f
INNER JOIN peliculas p ON p.id = f.pelicula_id
INNER JOIN sucursales s ON s.id = f.sucursal_id
GROUP BY
    p.titulo,
    s.nombre,
    f.fecha,
    f.hora,
    f.sala
HAVING COUNT(*) > 1
ORDER BY cantidad DESC, p.titulo, f.fecha, f.hora;

-- =====================================================
-- 2. CREAR TABLA TEMPORAL CON FUNCIONES RANKEADAS
-- =====================================================

DROP TEMPORARY TABLE IF EXISTS tmp_funciones_repetidas;

CREATE TEMPORARY TABLE tmp_funciones_repetidas AS
SELECT
    f.id,
    f.pelicula_id,
    p.titulo AS pelicula,
    f.sucursal_id,
    s.nombre AS sucursal,
    f.fecha,
    f.hora,
    f.sala,
    f.precio,
    COUNT(r.id) AS cantidad_reservas,
    ROW_NUMBER() OVER (
        PARTITION BY
            p.titulo,
            s.nombre,
            f.fecha,
            f.hora,
            f.sala
        ORDER BY
            COUNT(r.id) DESC,
            f.id ASC
    ) AS orden_para_conservar
FROM funciones f
INNER JOIN peliculas p ON p.id = f.pelicula_id
INNER JOIN sucursales s ON s.id = f.sucursal_id
LEFT JOIN reservas r ON r.funcion_id = f.id
GROUP BY
    f.id,
    f.pelicula_id,
    p.titulo,
    f.sucursal_id,
    s.nombre,
    f.fecha,
    f.hora,
    f.sala,
    f.precio;

-- =====================================================
-- 3. VER QUÉ FUNCIONES SE VAN A BORRAR
-- =====================================================

SELECT
    id AS funcion_id_a_eliminar,
    pelicula,
    sucursal,
    fecha,
    hora,
    sala,
    precio,
    cantidad_reservas,
    orden_para_conservar
FROM tmp_funciones_repetidas
WHERE orden_para_conservar > 1
AND cantidad_reservas = 0
ORDER BY pelicula, fecha, hora, id;

-- =====================================================
-- 4. BORRAR DUPLICADOS SIN RESERVAS
-- =====================================================

DELETE f
FROM funciones f
INNER JOIN tmp_funciones_repetidas t ON t.id = f.id
WHERE t.orden_para_conservar > 1
AND t.cantidad_reservas = 0;

-- =====================================================
-- 5. VER SI QUEDARON DUPLICADOS VISUALES
-- =====================================================

SELECT
    p.titulo AS pelicula,
    s.nombre AS sucursal,
    f.fecha,
    f.hora,
    f.sala,
    COUNT(*) AS cantidad,
    GROUP_CONCAT(f.id ORDER BY f.id ASC) AS funciones_ids,
    GROUP_CONCAT(f.pelicula_id ORDER BY f.id ASC) AS peliculas_ids,
    GROUP_CONCAT(f.precio ORDER BY f.id ASC) AS precios
FROM funciones f
INNER JOIN peliculas p ON p.id = f.pelicula_id
INNER JOIN sucursales s ON s.id = f.sucursal_id
GROUP BY
    p.titulo,
    s.nombre,
    f.fecha,
    f.hora,
    f.sala
HAVING COUNT(*) > 1
ORDER BY cantidad DESC, p.titulo, f.fecha, f.hora;

-- =====================================================
-- 6. LISTADO FINAL DE FUNCIONES
-- =====================================================

SELECT
    f.id,
    p.titulo AS pelicula,
    s.nombre AS sucursal,
    f.fecha,
    f.hora,
    f.sala,
    f.precio
FROM funciones f
INNER JOIN peliculas p ON p.id = f.pelicula_id
INNER JOIN sucursales s ON s.id = f.sucursal_id
ORDER BY f.id DESC;

SET SQL_SAFE_UPDATES = 1;