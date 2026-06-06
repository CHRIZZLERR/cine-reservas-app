USE cine_reservas;

-- =====================================================
-- 001 - CAMPOS TMDB PARA PELÍCULAS
-- JC Cinemas
-- Compatible con MySQL Workbench
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS agregar_columna_si_no_existe $$

CREATE PROCEDURE agregar_columna_si_no_existe(
    IN nombre_tabla VARCHAR(64),
    IN nombre_columna VARCHAR(64),
    IN definicion_columna TEXT
)
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = nombre_tabla
        AND COLUMN_NAME = nombre_columna
    ) THEN
        SET @sql = CONCAT(
            'ALTER TABLE ',
            nombre_tabla,
            ' ADD COLUMN ',
            nombre_columna,
            ' ',
            definicion_columna
        );

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- AGREGAR COLUMNAS TMDB
-- =====================================================

CALL agregar_columna_si_no_existe(
    'peliculas',
    'tmdb_id',
    'INT NULL AFTER id'
);

CALL agregar_columna_si_no_existe(
    'peliculas',
    'backdrop_url',
    'TEXT NULL AFTER poster_url'
);

CALL agregar_columna_si_no_existe(
    'peliculas',
    'trailer',
    'VARCHAR(255) NULL AFTER backdrop_url'
);

CALL agregar_columna_si_no_existe(
    'peliculas',
    'director',
    'VARCHAR(255) NULL AFTER trailer'
);

CALL agregar_columna_si_no_existe(
    'peliculas',
    'reparto',
    'TEXT NULL AFTER director'
);

CALL agregar_columna_si_no_existe(
    'peliculas',
    'rating',
    'DECIMAL(3,1) NULL DEFAULT 0 AFTER reparto'
);

DROP PROCEDURE IF EXISTS agregar_columna_si_no_existe;

-- =====================================================
-- ÍNDICE ÚNICO PARA TMDB
-- =====================================================

SET @existe_indice = (
    SELECT COUNT(1)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'peliculas'
    AND INDEX_NAME = 'idx_peliculas_tmdb_id'
);

SET @sql_indice = IF(
    @existe_indice = 0,
    'CREATE UNIQUE INDEX idx_peliculas_tmdb_id ON peliculas (tmdb_id)',
    'SELECT "El índice idx_peliculas_tmdb_id ya existe" AS mensaje'
);

PREPARE stmt_indice FROM @sql_indice;
EXECUTE stmt_indice;
DEALLOCATE PREPARE stmt_indice;

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

DESCRIBE peliculas;