CREATE DATABASE IF NOT EXISTS fiberhome_db;
USE fiberhome_db;

CREATE TABLE IF NOT EXISTS generated_passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mac_address VARCHAR(17) NOT NULL,
    generated_password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
