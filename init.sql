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
-- Eliminar todas las tablas si existen
-- DROP TABLE IF EXISTS sales_ferroelectricos_yambitara;
-- DROP TABLE IF EXISTS suppliers_ferroelectricos_yambitara;
-- DROP TABLE IF EXISTS products_ferroelectricos_yambitara;
-- DROP TABLE IF EXISTS user_types_ferroelectricos_yambitara;
-- DROP TABLE IF EXISTS users_ferroelectricos_yambitara;

CREATE TABLE IF NOT EXISTS users_ferroelectricos_yambitara (
    user_id  VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    document VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    type_user VARCHAR(50) NOT NULL,
    type_document VARCHAR(50) NOT NULL,
    contact_user VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear una tabla para gestionar el tipo de usuario
CREATE TABLE IF NOT EXISTS user_types_ferroelectricos_yambitara (
    document VARCHAR(50) NOT NULL PRIMARY KEY UNIQUE,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Crear una tabla para registrar los detalles de los productos
CREATE TABLE IF NOT EXISTS products_ferroelectricos_yambitara (
    product_id  VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    cost_products DECIMAL(15, 2) NOT NULL,
    sale_price DECIMAL(15, 2) NOT NULL,
    quantity DECIMAL(15, 2) NOT NULL,
    suppliers VARCHAR(100) NOT NULL,
    description_products TEXT,
    profit_margin DECIMAL(5, 2) NOT NULL,
    image_reference TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear una tabla para los proveedores
CREATE TABLE IF NOT EXISTS suppliers_ferroelectricos_yambitara (
    supplier_id VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    supplier_nit VARCHAR(50) NOT NULL UNIQUE,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_contact_name VARCHAR(100),
    supplier_contact_email VARCHAR(100),
    supplier_contact_contable VARCHAR(100),
    supplier_phone VARCHAR(20),
    supplier_phone_two VARCHAR(20),
    supplier_address TEXT,
    supplier_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear una tabla para registrar las ventas
CREATE TABLE IF NOT EXISTS sales_ferroelectricos_yambitara (
    sale_id SERIAL NOT NULL PRIMARY KEY,
    id_sale_dian VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    cost_sale DECIMAL(15, 2) NOT NULL,
    profit_sale DECIMAL(15, 2) NOT NULL,
    total DECIMAL(15, 2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_ferroelectricos_yambitara(user_id),
    FOREIGN KEY (product_id) REFERENCES products_ferroelectricos_yambitara(product_id)
);

