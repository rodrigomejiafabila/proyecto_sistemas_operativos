CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS pedidos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    producto VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    estado VARCHAR(50) DEFAULT 'procesado',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);