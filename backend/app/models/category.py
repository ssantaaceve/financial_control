from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MovementType(str, Enum):
    INGRESO = "Ingreso"
    GASTO = "Gasto"

class CategoryBase(BaseModel):
    name: str
    type: MovementType
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[MovementType] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True 