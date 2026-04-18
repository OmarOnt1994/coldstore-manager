-- 1. Almacenes (Warehouses)
CREATE TABLE IF NOT EXISTS warehouses (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Ubicaciones (Locations)
CREATE TABLE IF NOT EXISTS locations (
    id BIGSERIAL PRIMARY KEY,
    warehouse_id BIGINT NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
    code VARCHAR(30) UNIQUE NOT NULL,
    aisle VARCHAR(10),
    level SMALLINT CHECK (level BETWEEN 1 AND 4 OR level IS NULL),
    position SMALLINT CHECK (position BETWEEN 1 AND 4 OR position IS NULL),
    status VARCHAR(20) DEFAULT 'disponible',
    capacity INTEGER DEFAULT 4,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Productos / Items
CREATE TABLE IF NOT EXISTS items (
    id BIGSERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    weight_kg DECIMAL(10,2),
    entry_date DATE NOT NULL,
    expiry_date DATE,
    batch VARCHAR(100),
    tag INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location_id BIGINT NOT NULL REFERENCES locations(id) ON DELETE RESTRICT
);

-- Índices recomendados
CREATE INDEX IF NOT EXISTS idx_locations_warehouse_id ON locations(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_items_location_id ON items(location_id);
CREATE INDEX IF NOT EXISTS idx_items_expiry_date ON items(expiry_date);