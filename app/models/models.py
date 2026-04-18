from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # cold, dry, container
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    locations = relationship("Location", back_populates="warehouse", cascade="all, delete")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(30), unique=True, nullable=False, index=True)
    aisle = Column(String(10))
    level = Column(Integer)
    position = Column(Integer)
    status = Column(String(20), default="disponible")
    capacity = Column(Integer, default=4)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    warehouse = relationship("Warehouse", back_populates="locations")
    items = relationship("Item", back_populates="location", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    weight_kg = Column(Numeric(10, 2))
    entry_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    batch = Column(String(100))
    tag = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    location_id = Column(Integer, ForeignKey("locations.id", ondelete="RESTRICT"), nullable=False)
    location = relationship("Location", back_populates="items")