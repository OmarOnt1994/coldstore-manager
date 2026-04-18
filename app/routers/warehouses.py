from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Warehouse
from app.schemas.schemas import WarehouseCreate, WarehouseRead
from app.crud.crud import get_warehouses, create_warehouse, get_warehouse, update_warehouse, delete_warehouse

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])

@router.post("/", response_model=WarehouseRead)
def create_new_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    # Validar que el código sea único
    existing = db.query(Warehouse).filter(Warehouse.code == warehouse.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="El código de almacén ya existe")
    return create_warehouse(db, warehouse.model_dump())

@router.get("/", response_model=list[WarehouseRead])
def read_warehouses(db: Session = Depends(get_db)):
    return get_warehouses(db)

@router.get("/{warehouse_id}", response_model=WarehouseRead)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    db_warehouse = get_warehouse(db, warehouse_id)
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return db_warehouse

@router.put("/{warehouse_id}", response_model=WarehouseRead)
def update_warehouse_endpoint(warehouse_id: int, warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = get_warehouse(db, warehouse_id)
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return update_warehouse(db, warehouse_id, warehouse.model_dump())

@router.delete("/{warehouse_id}")
def delete_warehouse_endpoint(warehouse_id: int, db: Session = Depends(get_db)):
    db_warehouse = get_warehouse(db, warehouse_id)
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    delete_warehouse(db, warehouse_id)
    return {"message": "Almacén eliminado"}
