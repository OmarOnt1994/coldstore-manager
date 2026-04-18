from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Item, Location, Warehouse
from app.schemas.schemas import ItemCreate, ItemRead
from app.crud.crud import (create_item, get_items, get_items_by_location, 
                            get_item, update_item, delete_item, get_location)

def enrich_item(item: Item) -> dict:
    """Agrega información de ubicación y almacén a un item"""
    location = item.location
    warehouse = location.warehouse if location else None
    
    # Construir diccionario con todos los campos necesarios
    item_dict = {
        "id": item.id,
        "product_name": item.product_name,
        "weight_kg": item.weight_kg,
        "entry_date": item.entry_date,
        "expiry_date": item.expiry_date,
        "batch": item.batch,
        "tag": item.tag,
        "location_id": item.location_id,
        "location_code": location.code if location else None,
        "warehouse_name": warehouse.name if warehouse else None,
        "created_at": item.created_at,
        "updated_at": item.updated_at
    }
    return item_dict

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemRead)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Validar que la ubicación existe
    location = get_location(db, item.location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    created = create_item(db, item.model_dump())
    enriched = enrich_item(created)
    return ItemRead(**enriched)

@router.get("/", response_model=list[ItemRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip, limit)
    return [ItemRead(**enrich_item(item)) for item in items]

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    enriched = enrich_item(db_item)
    return ItemRead(**enriched)

@router.get("/location/{location_id}", response_model=list[ItemRead])
def read_items_by_location(location_id: int, db: Session = Depends(get_db)):
    location = get_location(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    items = get_items_by_location(db, location_id)
    return [ItemRead(**enrich_item(item)) for item in items]

@router.put("/{item_id}", response_model=ItemRead)
def update_item_endpoint(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    updated = update_item(db, item_id, item.model_dump())
    enriched = enrich_item(updated)
    return ItemRead(**enriched)

@router.delete("/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    delete_item(db, item_id)
    return {"message": "Artículo eliminado"}