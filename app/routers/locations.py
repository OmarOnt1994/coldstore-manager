from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Location, Item
from app.schemas.schemas import LocationCreate, LocationRead
from app.crud.crud import (get_locations_by_warehouse, create_location, get_location, 
                            update_location, delete_location, get_warehouse)

def enrich_location(location: Location) -> dict:
    """Agrega conteo de items a una ubicación"""
    items_count = len(location.items) if location.items else 0
    available = location.capacity - items_count
    return {
        **{col.name: getattr(location, col.name) for col in location.__table__.columns},
        "items_count": items_count,
        "available_spaces": available
    }

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/", response_model=LocationRead)
def create_new_location(location: LocationCreate, db: Session = Depends(get_db)):
    warehouse = get_warehouse(db, location.warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    
    existing = db.query(Location).filter(Location.code == location.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="El código de ubicación ya existe")
    
    created = create_location(db, location.model_dump())
    enriched = enrich_location(created)
    return LocationRead(**enriched)

@router.get("/warehouse/{warehouse_id}", response_model=list[LocationRead])
def read_locations_by_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = get_warehouse(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    locations = get_locations_by_warehouse(db, warehouse_id)
    return [LocationRead(**enrich_location(loc)) for loc in locations]

@router.get("/{location_id}", response_model=LocationRead)
def read_location(location_id: int, db: Session = Depends(get_db)):
    location = get_location(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    enriched = enrich_location(location)
    return LocationRead(**enriched)

@router.put("/{location_id}", response_model=LocationRead)
def update_location_endpoint(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    db_location = get_location(db, location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return update_location(db, location_id, location.model_dump())

@router.delete("/{location_id}")
def delete_location_endpoint(location_id: int, db: Session = Depends(get_db)):
    location = get_location(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    delete_location(db, location_id)
    return {"message": "Ubicación eliminada"}
