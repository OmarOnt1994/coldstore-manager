from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.models import Warehouse, Location, Item
from datetime import date, timedelta
import string

def seed_database():
    db: Session = SessionLocal()

    # 1. Crear los almacenes
    warehouses_data = [
        {"code": "FRIO", "name": "Almacén Frío Principal", "type": "cold", "description": "Rack industrial con ubicaciones A-W"},
        {"code": "SECO", "name": "Almacén en Seco", "type": "dry", "description": "Pequeño almacén seco"},
        {"code": "CONT-01", "name": "Contenedor Trailer 01", "type": "container", "description": ""},
        {"code": "CONT-02", "name": "Contenedor Trailer 02", "type": "container", "description": ""},
        {"code": "CONT-03", "name": "Contenedor Trailer 03", "type": "container", "description": ""},
        {"code": "CONT-04", "name": "Contenedor Trailer 04", "type": "container", "description": ""},
        {"code": "CONT-05", "name": "Contenedor Trailer 05", "type": "container", "description": ""},
        {"code": "CONT-06", "name": "Contenedor Trailer 06", "type": "container", "description": ""},
        {"code": "CONT-07", "name": "Contenedor Trailer 07", "type": "container", "description": ""},
    ]

    print("Creando almacenes...")
    for wh in warehouses_data:
        existing = db.query(Warehouse).filter(Warehouse.code == wh["code"]).first()
        if not existing:
            db_warehouse = Warehouse(**wh)
            db.add(db_warehouse)
            db.commit()
            db.refresh(db_warehouse)
            print(f"✓ Almacén creado: {wh['code']}")

    # Obtener el ID del almacén FRIO
    frio = db.query(Warehouse).filter(Warehouse.code == "FRIO").first()
    if not frio:
        print("Error: No se encontró el almacén FRIO")
        db.close()
        return

    # 2. Crear las ubicaciones del almacén FRIO (A1-A4, B1-B4, ..., W1-W4)
    print("Generando ubicaciones del Almacén Frío (A1-A4, B1-B4, ... W1-W4)...")
    aisles = list(string.ascii_uppercase[:23])  # A hasta W

    created_count = 0
    for aisle in aisles:
        for pos_num in range(1, 5):  # 1, 2, 3, 4
            code = f"{aisle}{pos_num}"
            
            # Verificar si ya existe
            existing = db.query(Location).filter(Location.code == code).first()
            if not existing:
                location = Location(
                    warehouse_id=frio.id,
                    code=code,
                    aisle=aisle,
                    level=1,
                    position=pos_num,
                    status="disponible"
                )
                db.add(location)
                created_count += 1
                
                # Commit cada 50 para no saturar la memoria
                if created_count % 50 == 0:
                    db.commit()

    db.commit()
    print(f"✓ Se crearon {created_count} ubicaciones en el Almacén Frío (23 aisles x 4 posiciones)")

    # 3. Crear algunas ubicaciones en el almacén SECO
    print("Generando ubicaciones del Almacén Seco...")
    seco = db.query(Warehouse).filter(Warehouse.code == "SECO").first()
    if seco:
        for i in range(1, 11):  # 10 ubicaciones simples
            code = f"SEA-{i}"
            existing = db.query(Location).filter(Location.code == code).first()
            if not existing:
                location = Location(
                    warehouse_id=seco.id,
                    code=code,
                    aisle="A",
                    level=1,
                    position=i,
                    status="disponible"
                )
                db.add(location)
        db.commit()
        print(f"✓ Se crearon 10 ubicaciones en el Almacén Seco")

    # 4. Crear productos de ejemplo (Items)
    print("\nCreando productos de ejemplo...")
    products = [
        {"name": "Pollo Congelado", "weight": 2.5, "batch": "PC-2024-001", "expiry_days": 60},
        {"name": "Atún en Lata", "weight": 0.5, "batch": "AT-2024-002", "expiry_days": 90},
        {"name": "Arveja Congelada", "weight": 1.0, "batch": "AR-2024-003", "expiry_days": 120},
        {"name": "Carne Molida", "weight": 1.5, "batch": "CM-2024-004", "expiry_days": 45},
        {"name": "Camarones", "weight": 0.8, "batch": "CA-2024-005", "expiry_days": 30},
    ]

    # Obtener ubicaciones disponibles
    available_locations = db.query(Location).filter(Location.status == "disponible").limit(10).all()
    
    for idx, product in enumerate(products):
        if idx < len(available_locations):
            location = available_locations[idx]
            expiry_date = date.today() + timedelta(days=product["expiry_days"])
            
            existing = db.query(Item).filter(Item.product_name == product["name"]).first()
            if not existing:
                item = Item(
                    product_name=product["name"],
                    weight_kg=product["weight"],
                    entry_date=date.today(),
                    expiry_date=expiry_date,
                    batch=product["batch"],
                    location_id=location.id,
                    tag=None
                )
                db.add(item)
                print(f"✓ Producto creado: {product['name']} en {location.code}")
    
    db.commit()
    db.close()
    print("\n✅ Seed completado exitosamente!")


if __name__ == "__main__":
    # Crear tablas primero
    Base.metadata.create_all(bind=engine)
    seed_database()