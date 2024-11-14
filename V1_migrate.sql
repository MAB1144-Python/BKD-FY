CREATE TABLE products_ferroelectricos_yambitara (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255) NOT NULL,
    reference VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,,
    profit_percentage DECIMAL(5, 2) NOT NULL
    quantity INT NOT NULL,
    distributor VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE distributor_ferroelectricos_yambitara (
    distributor_id VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    distributor_name VARCHAR(255) NOT NULL,
    distributor_nit VARCHAR(50) NOT NULL,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),
    contact_email VARCHAR(255),
    contact_name_accounting VARCHAR(255),
    contact_phone_accounting VARCHAR(50),
    contact_email_accounting VARCHAR(255),
    city_address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- add tipo de persona persona natural o persona juridica
ALTER TABLE users_ferroelectricos_yambitara ADD COLUMN type_document VARCHAR(50) NOT NULL;