CREATE DATABASE IF NOT EXISTS erp_agricola;
USE erp_agricola;

-- 1. USUARIOS Y FISCALIDAD
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nif_cif VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    direccion_fiscal VARCHAR(200),
    iban VARCHAR(34),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. CLIENTES
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nif_cif VARCHAR(20) NOT NULL,
    nombre_empresa VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. PARCELAS
CREATE TABLE parcelas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre_finca VARCHAR(100) NOT NULL,
    provincia INT NOT NULL,
    municipio INT NOT NULL,
    poligono INT NOT NULL,
    parcela INT NOT NULL,
    recinto INT DEFAULT 1,
    referencia_catastral VARCHAR(20),
    superficie_ha DECIMAL(8,4) NOT NULL,
    regimen ENUM('PROPIEDAD', 'ARRENDAMIENTO') DEFAULT 'PROPIEDAD',
    coste_renta_campana DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. CAMPAÑAS
CREATE TABLE campanas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
) ENGINE=InnoDB;

-- 5. RELACIÓN CAMPAÑA-PARCELA (Incluye Barbecho)
CREATE TABLE campana_parcela (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campana_id INT NOT NULL,
    parcela_id INT NOT NULL,
    tipo_cultivo VARCHAR(50) NOT NULL,
    estado_cultivo ENUM('EN_PRODUCCION', 'BARBECHO', 'DESCANSO') DEFAULT 'EN_PRODUCCION',
    FOREIGN KEY (campana_id) REFERENCES campanas(id) ON DELETE CASCADE,
    FOREIGN KEY (parcela_id) REFERENCES parcelas(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. DIARIO DE OPERACIONES
CREATE TABLE diario_operaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campana_parcela_id INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_operacion ENUM('PODA', 'ARADO', 'TRATAMIENTO', 'SIEMBRA', 'RECOLECCION', 'OTROS') NOT NULL,
    producto_aplicado VARCHAR(100),
    dosis VARCHAR(50),
    coste_mano_obra DECIMAL(8,2) DEFAULT 0.00,
    observaciones TEXT,
    FOREIGN KEY (campana_parcela_id) REFERENCES campana_parcela(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. FACTURAS
CREATE TABLE facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    cliente_id INT NOT NULL,
    numero_factura VARCHAR(50) NOT NULL,
    fecha_emision DATE NOT NULL,
    porcentaje_iva DECIMAL(4,2) DEFAULT 21.00,
    porcentaje_irpf DECIMAL(4,2) DEFAULT 2.00,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
) ENGINE=InnoDB;

-- 8. LÍNEAS DE FACTURA
CREATE TABLE lineas_factura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    concepto VARCHAR(200) NOT NULL,
    cantidad DECIMAL(8,2) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. MARKETPLACE B2B
CREATE TABLE marketplace_servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_nombre VARCHAR(100) NOT NULL,
    categoria ENUM('TALA', 'COSECHADORA', 'SULFATO', 'SUMINISTROS') NOT NULL,
    provincia VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    es_patrocinado BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;
