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
    sale_id VARCHAR(255) PRIMARY KEY,
    id_sale_dian VARCHAR(50) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    sale_cost DECIMAL(15, 2) NOT NULL,
    sale_discount DECIMAL(15, 2) NOT NULL,
    sale_profit DECIMAL(15, 2) NOT NULL,
    sale_total DECIMAL(15, 2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_ferroelectricos_yambitara(user_id)
);
-- Crear una tabla para registrar las ventas
CREATE TABLE IF NOT EXISTS sales_detail_ferroelectricos_yambitara (
    sale_id_detail INT PRIMARY KEY,
    sale_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity_product DECIMAL(15, 2) NOT NULL,
    cost_product DECIMAL(15, 2) NOT NULL,
    profit_product DECIMAL(15, 2) NOT NULL,
    discount_product DECIMAL(15, 2) NOT NULL,
    sale_product DECIMAL(15, 2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales_ferroelectricos_yambitara(sale_id),
    FOREIGN KEY (product_id) REFERENCES products_ferroelectricos_yambitara(product_id)
);

-- Insertar registros de ejemplo en la tabla 'users_ferroelectricos_yambitara'
INSERT INTO users_ferroelectricos_yambitara (user_id, document, name, email, password, type_user, type_document, contact_user)
VALUES 
('1', '123456789', 'John Doe', 'john.doe@example.com', '$2b$12$GyzIsbet9oPpq3VBVf1jNOyT7Rv85GfafWz2BhEen645LeTd/EEaK', 'admin', 'ID', '123-456-7890'),
('2', '987654321', 'Jane Smith', 'jane.smith@example.com', '$2b$12$s1P12wOVDbxRfKNywHfec.KnCU6y3sxEn3DeHtB0RT1sFvSTjNEeO', 'user', 'ID', '098-765-4321'),
('3', '234567890', 'Alice Johnson', 'alice.johnson@example.com', '$2b$12$GUrQ65IJkPQw.vjBoj1QlupKkxy5deomJu0nk2w7qe7dxnyIMsWbG', 'seller', 'ID', '234-567-8901'),
('4', '345678901', 'Bob Brown', 'bob.brown@example.com', '$2b$12$U6CWGzE.S6OnwtQWzmLfVegiZ9dIi6TwPeJYvlUz2WclBUMtOmDSO', 'user', 'ID', '345-678-9012'),
('5', '456789012', 'Charlie Davis', 'charlie.davis@example.com', '$2b$12$R2.tpthprkj9VxiEbsDzdec1yP4hCSv5Cj9P3p8cQ8KyqeXiyuPiC', 'user', 'ID', '456-789-0123'),
('6', '567890123', 'Diana Evans', 'diana.evans@example.com', '$2b$12$HriNGxDxtxwOoJJHVtpKq.dpj45aSh/WNyqvqUSmuYJaek7DmTnTm', 'user', 'ID', '567-890-1234'),
('7', '678901234', 'Ethan Harris', 'ethan.harris@example.com', '$2b$12$.1hCPiFu.NDK/pajybHTCuW.xbAa2b251pGg8LbfDdFxc4MDBc/jG', 'user', 'ID', '678-901-2345');

-- Insertar registros de ejemplo en la tabla 'user_types_ferroelectricos_yambitara'
INSERT INTO user_types_ferroelectricos_yambitara (document, type_name, description)
VALUES 
('123456789', 'admin', 'Administrator with full access'),
('987654321', 'user', 'Regular user with limited access');

-- Insertar registros de ejemplo en la tabla 'products_ferroelectricos_yambitara'
INSERT INTO products_ferroelectricos_yambitara (product_id, product_name, cost_products, sale_price, quantity, suppliers, description_products, profit_margin, image_reference)
VALUES 
('p1', 'Product A', 10.00, 15.00, 100, 'Supplier A', 'Description of Product A', 5.00, 'imageA.jpg'),
('p10', 'Product J', 100.00, 150.00, 1000, 'Supplier J', 'Description of Product J', 50.00, 'imageJ.jpg'),
('p9', 'Product I', 90.00, 135.00, 900, 'Supplier I', 'Description of Product I', 45.00, 'imageI.jpg'),
('p8', 'Product H', 80.00, 120.00, 800, 'Supplier H', 'Description of Product H', 40.00, 'imageH.jpg'),
('p7', 'Product G', 70.00, 105.00, 700, 'Supplier G', 'Description of Product G', 35.00, 'imageG.jpg'),
('p6', 'Product F', 60.00, 90.00, 600, 'Supplier F', 'Description of Product F', 30.00, 'imageF.jpg'),
('p5', 'Product E', 50.00, 75.00, 500, 'Supplier E', 'Description of Product E', 25.00, 'imageE.jpg'),
('p4', 'Product D', 40.00, 60.00, 400, 'Supplier D', 'Description of Product D', 20.00, 'imageD.jpg'),
('p3', 'Product C', 30.00, 45.00, 300, 'Supplier C', 'Description of Product C', 15.00, 'imageC.jpg'),
('p2', 'Product B', 20.00, 30.00, 200, 'Supplier B', 'Description of Product B', 10.00, 'imageB.jpg');

-- Insertar registros de ejemplo en la tabla 'suppliers_ferroelectricos_yambitara'
INSERT INTO suppliers_ferroelectricos_yambitara (supplier_id, supplier_nit, supplier_name, supplier_contact_name, supplier_contact_email, supplier_contact_contable, supplier_phone, supplier_phone_two, supplier_address)
VALUES 
('1', '111111111', 'Supplier A', 'Contact A', 'contactA@example.com', 'contableA@example.com', '111-111-1111', '222-222-2222', 'Address A'),
('2', '222222222', 'Supplier B', 'Contact B', 'contactB@example.com', 'contableB@example.com', '333-333-3333', '444-444-4444', 'Address B');

