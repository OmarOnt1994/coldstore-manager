from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

# ---------- Warehouses ----------
class WarehouseBase(BaseModel):
    code: str
    name: str
    type: str
    description: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseRead(WarehouseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- Locations ----------
class LocationBase(BaseModel):
    code: str
    aisle: Optional[str] = None
    level: Optional[int] = None
    position: Optional[int] = None
    status: str = "disponible"
    capacity: int = 4
    notes: Optional[str] = None

class LocationCreate(LocationBase):
    warehouse_id: int

class LocationRead(LocationBase):
    id: int
    warehouse_id: int
    created_at: datetime
    updated_at: datetime
    items_count: Optional[int] = None

    class Config:
        from_attributes = True

# ---------- Items ----------
class ItemBase(BaseModel):
    product_name: str
    weight_kg: Optional[float] = None
    entry_date: date
    expiry_date: Optional[date] = None
    batch: Optional[str] = None
    tag: Optional[int] = None

class ItemCreate(ItemBase):
    location_id: int

class ItemRead(ItemBase):
    id: int
    location_id: int
    location_code: Optional[str] = None
    warehouse_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    updated_at: datetime

    class Config:
        from_attributes = True