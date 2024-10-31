-- Crear una tabla de ejemplo en la base de datos
-- Este script SQL crea una tabla llamada 'users' si no existe.
-- La tabla 'users' contiene la siguiente estructura:
-- 
-- user_id:      Identificador único para cada usuario (tipo SERIAL, clave primaria).
-- username:     Nombre de usuario (tipo VARCHAR(50), no nulo).
-- email:        Dirección de correo electrónico del usuario (tipo VARCHAR(100), no nulo, único).
-- password:     Contraseña del usuario (tipo VARCHAR(255), no nulo).
-- created_at:   Marca de tiempo de la creación del registro (tipo TIMESTAMP, valor por defecto CURRENT_TIMESTAMP).
-- Crear una tabla para los usuarios
CREATE TABLE IF NOT EXISTS users (
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    type_document VARCHAR(50) NOT NULL
    document VARCHAR(50) NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

