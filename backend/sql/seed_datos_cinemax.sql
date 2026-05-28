USE cine_reservas;

SET SQL_SAFE_UPDATES = 0;

-- =====================================================
-- 009 - DATOS DE PRUEBA REALISTAS PARA CINEMAX
-- Cartelera, próximas películas y funciones
-- =====================================================

-- Actualizar películas existentes
UPDATE peliculas
SET 
    titulo = 'Avatar',
    sinopsis = 'Una aventura de ciencia ficción ambientada en un mundo visualmente impresionante.',
    genero = 'Ciencia ficción',
    clasificacion = 'PG-13',
    duracion_minutos = 162,
    poster_url = 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa',
    estado = 'cartelera',
    fecha_estreno = '2025-12-18',
    activa = TRUE
WHERE id = 1;

UPDATE peliculas
SET 
    titulo = 'Batman',
    sinopsis = 'Un héroe protege Ciudad Gótica mientras enfrenta amenazas que ponen a prueba su justicia.',
    genero = 'Acción',
    clasificacion = 'PG-13',
    duracion_minutos = 176,
    poster_url = 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb',
    estado = 'cartelera',
    fecha_estreno = '2025-11-10',
    activa = TRUE
WHERE id = 2;

-- Reactivar Interestelar si existe
UPDATE peliculas
SET 
    titulo = 'Interestelar',
    sinopsis = 'Un grupo de exploradores viaja por el espacio en busca de un nuevo hogar para la humanidad.',
    genero = 'Ciencia ficción',
    clasificacion = 'PG-13',
    duracion_minutos = 169,
    poster_url = 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564',
    estado = 'cartelera',
    fecha_estreno = '2025-12-20',
    activa = TRUE
WHERE id > 0
AND titulo LIKE 'Interestelar%';

-- Insertar Interestelar si no existe
INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'Interestelar',
    'Un grupo de exploradores viaja por el espacio en busca de un nuevo hogar para la humanidad.',
    'Ciencia ficción',
    'PG-13',
    169,
    'https://images.unsplash.com/photo-1462331940025-496dfbfc7564',
    'cartelera',
    '2025-12-20',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo LIKE 'Interestelar%'
);

-- Insertar más películas si no existen
INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'Rápidos y Furiosos X',
    'Una nueva misión llena de velocidad, acción y adrenalina pone al equipo al límite.',
    'Acción',
    'PG-13',
    141,
    'https://images.unsplash.com/photo-1511919884226-fd3cad34687c',
    'cartelera',
    '2025-10-15',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'Rápidos y Furiosos X'
);

INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'El Reino Perdido',
    'Un grupo de aventureros descubre una ciudad oculta llena de secretos antiguos.',
    'Aventura',
    'PG',
    128,
    'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee',
    'cartelera',
    '2025-09-28',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'El Reino Perdido'
);

INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'Noche de Terror',
    'Una familia se muda a una casa donde comienzan a ocurrir sucesos inexplicables.',
    'Terror',
    'R',
    112,
    'https://images.unsplash.com/photo-1509248961158-e54f6934749c',
    'cartelera',
    '2025-10-31',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'Noche de Terror'
);

INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'Super Mario Galaxy',
    'Mario y sus amigos viajan por mundos coloridos para salvar la galaxia.',
    'Animación',
    'PG',
    104,
    'https://images.unsplash.com/photo-1550745165-9bc0b252726f',
    'cartelera',
    '2025-08-22',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'Super Mario Galaxy'
);

INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'Duna: Nuevo Amanecer',
    'La batalla por el control del desierto continúa en una nueva historia épica.',
    'Ciencia ficción',
    'PG-13',
    155,
    'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429',
    'proximamente',
    '2026-01-18',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'Duna: Nuevo Amanecer'
);

INSERT INTO peliculas
(titulo, sinopsis, genero, clasificacion, duracion_minutos, poster_url, estado, fecha_estreno, activa)
SELECT 
    'La Última Expedición',
    'Un equipo de exploradores se enfrenta a una misión peligrosa en territorio desconocido.',
    'Aventura',
    'PG-13',
    132,
    'https://images.unsplash.com/photo-1501785888041-af3ef285b470',
    'proximamente',
    '2026-02-05',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM peliculas WHERE titulo = 'La Última Expedición'
);

-- =====================================================
-- FUNCIONES REALISTAS
-- =====================================================

-- Avatar
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-12-18', '18:00:00', 'Sala 1', 300.00
FROM peliculas p
WHERE p.titulo = 'Avatar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-12-18'
    AND f.hora = '18:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-12-18', '21:00:00', 'Sala 1', 350.00
FROM peliculas p
WHERE p.titulo = 'Avatar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-12-18'
    AND f.hora = '21:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-12-18', '19:30:00', 'Sala 2', 320.00
FROM peliculas p
WHERE p.titulo = 'Avatar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-12-18'
    AND f.hora = '19:30:00'
);

-- Batman
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-11-10', '17:30:00', 'Sala 3', 300.00
FROM peliculas p
WHERE p.titulo = 'Batman'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-11-10'
    AND f.hora = '17:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-11-10', '20:00:00', 'Sala 1', 350.00
FROM peliculas p
WHERE p.titulo = 'Batman'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-11-10'
    AND f.hora = '20:00:00'
);

-- Interestelar
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-12-20', '16:00:00', 'Sala 2', 350.00
FROM peliculas p
WHERE p.titulo = 'Interestelar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-12-20'
    AND f.hora = '16:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-12-20', '20:30:00', 'Sala 4', 400.00
FROM peliculas p
WHERE p.titulo = 'Interestelar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-12-20'
    AND f.hora = '20:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-12-20', '21:15:00', 'Sala 5', 400.00
FROM peliculas p
WHERE p.titulo = 'Interestelar'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-12-20'
    AND f.hora = '21:15:00'
);

-- Rápidos y Furiosos X
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-10-15', '19:00:00', 'Sala 5', 325.00
FROM peliculas p
WHERE p.titulo = 'Rápidos y Furiosos X'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-10-15'
    AND f.hora = '19:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-10-15', '21:30:00', 'Sala 3', 350.00
FROM peliculas p
WHERE p.titulo = 'Rápidos y Furiosos X'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-10-15'
    AND f.hora = '21:30:00'
);

-- El Reino Perdido
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-09-28', '15:30:00', 'Sala 2', 275.00
FROM peliculas p
WHERE p.titulo = 'El Reino Perdido'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-09-28'
    AND f.hora = '15:30:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-09-28', '18:30:00', 'Sala 2', 300.00
FROM peliculas p
WHERE p.titulo = 'El Reino Perdido'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-09-28'
    AND f.hora = '18:30:00'
);

-- Noche de Terror
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-10-31', '22:00:00', 'Sala 6', 350.00
FROM peliculas p
WHERE p.titulo = 'Noche de Terror'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-10-31'
    AND f.hora = '22:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-10-31', '23:30:00', 'Sala 4', 375.00
FROM peliculas p
WHERE p.titulo = 'Noche de Terror'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-10-31'
    AND f.hora = '23:30:00'
);

-- Super Mario Galaxy
INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 2, '2025-08-22', '14:00:00', 'Sala 1', 250.00
FROM peliculas p
WHERE p.titulo = 'Super Mario Galaxy'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 2
    AND f.fecha = '2025-08-22'
    AND f.hora = '14:00:00'
);

INSERT INTO funciones (pelicula_id, sucursal_id, fecha, hora, sala, precio)
SELECT p.id, 1, '2025-08-22', '16:45:00', 'Sala 1', 275.00
FROM peliculas p
WHERE p.titulo = 'Super Mario Galaxy'
AND NOT EXISTS (
    SELECT 1 FROM funciones f
    WHERE f.pelicula_id = p.id
    AND f.sucursal_id = 1
    AND f.fecha = '2025-08-22'
    AND f.hora = '16:45:00'
);

SET SQL_SAFE_UPDATES = 1;

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

SELECT 
    id,
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
ORDER BY f.fecha, f.hora;