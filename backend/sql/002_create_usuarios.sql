USE cine_reservas;

-- =====================================================
-- 002 - TABLA DE USUARIOS
-- JC Cinemas
-- =====================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'admin') NOT NULL DEFAULT 'cliente',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USUARIO ADMINISTRADOR DE PRUEBA
-- =====================================================
-- Contraseña temporal: admin123
-- Luego podemos cambiarla o mejorarla.

INSERT INTO usuarios (nombre, email, password_hash, rol, activo)
SELECT 
    'Administrador JC Cinemas',
    'admin@jccinemas.com',
    'admin123',
    'admin',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE email = 'admin@jccinemas.com'
);

-- =====================================================
-- USUARIO CLIENTE DE PRUEBA
-- =====================================================
-- Contraseña temporal: cliente123

INSERT INTO usuarios (nombre, email, password_hash, rol, activo)
SELECT 
    'Cliente de Prueba',
    'cliente@jccinemas.com',
    'cliente123',
    'cliente',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE email = 'cliente@jccinemas.com'
);

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

SELECT 
    id,
    nombre,
    email,
    rol,
    activo,
    fecha_creacion
FROM usuarios
ORDER BY id;