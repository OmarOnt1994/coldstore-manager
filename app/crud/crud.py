from sqlalchemy.orm import Session
from app.models.models import Warehouse, Location, Item

# ========== WAREHOUSES ==========
def get_warehouses(db: Session):
    return db.query(Warehouse).all()

def get_warehouse(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

def create_warehouse(db: Session, warehouse: dict):
    db_warehouse = Warehouse(**warehouse)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def update_warehouse(db: Session, warehouse_id: int, warehouse: dict):
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if db_warehouse:
        for key, value in warehouse.items():
            setattr(db_warehouse, key, value)
        db.commit()
        db.refresh(db_warehouse)
    return db_warehouse

def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if db_warehouse:
        db.delete(db_warehouse)
        db.commit()

# ========== LOCATIONS ==========
def get_locations_by_warehouse(db: Session, warehouse_id: int):
    return db.query(Location).filter(Location.warehouse_id == warehouse_id).all()

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()

def create_location(db: Session, location: dict):
    db_location = Location(**location)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: int, location: dict):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location:
        for key, value in location.items():
            setattr(db_location, key, value)
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()

# ========== ITEMS ==========
def create_item(db: Session, item: dict):
    db_item = Item(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_items_by_location(db: Session, location_id: int):
    return db.query(Item).filter(Item.location_id == location_id).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: dict):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()