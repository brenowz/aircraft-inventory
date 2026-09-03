CREATE SCHEMA IF NOT EXISTS aircraft_inventory;

USE aircraft_inventory;

CREATE TABLE IF NOT EXISTS admins (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS aircraft (
    id INT NOT NULL AUTO_INCREMENT,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    color VARCHAR(30),
    type INT,
    PRIMARY KEY (id)
);