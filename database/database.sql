
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE administrador (
	telefono INTEGER NOT NULL,
	nombre VARCHAR(10) NOT NULL,
	apellidos VARCHAR(40) NOT NULL
)
INHERITS (usuario);
CREATE TABLE visitante (
	username VARCHAR(20) NOT NULL,
	ultimo_ingreso TIMESTAMP
)
INHERITS (usuario);


INSERT INTO administrador (nombre, apellidos, correo, password, telefono)
VALUES ('Aaron', 'Santamaria', 'coldroad.inherit@gmail.com', 'pass', 9129313)
























