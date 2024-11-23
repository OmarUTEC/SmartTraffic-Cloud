
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
	ultimo_ingreso TIMESTAMP,
	tiempo_activo INTEGER
)
INHERITS (usuario);


INSERT INTO administrador (nombre, apellidos, correo, password, telefono)
VALUES ('Aaron', 'Santamaria', 'coldroad.inherit@gmail.com', 'pass', 9129313)

CREATE OR REPLACE FUNCTION incrementar_tiempo_activo(
    incremento INTEGER, -- Tipo de dato especificado
    id_user INTEGER     -- Tipo de dato especificado
)
RETURNS VOID AS $$
BEGIN
    -- Actualizar la columna tiempo_activo incrementando su valor
    UPDATE visitante
    SET tiempo_activo = COALESCE(tiempo_activo, 0) + incremento
    WHERE id = id_user;
END;
$$ LANGUAGE plpgsql;

select incrementar_tiempo_activo(2,6);

select * from visitante;






















