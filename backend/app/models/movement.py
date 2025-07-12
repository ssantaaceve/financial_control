from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum

class MovementType(str, Enum):
    """Tipos de movimiento."""
    INGRESO = "Ingreso"
    GASTO = "Gasto"

class MovementBase(BaseModel):
    """Modelo base para movimientos."""
    amount: float = Field(..., gt=0, description="Monto del movimiento")
    category: str = Field(..., min_length=1, description="Categoría del movimiento")
    description: Optional[str] = Field(None, description="Descripción del movimiento")
    movement_type: MovementType = Field(..., description="Tipo de movimiento")

class MovementCreate(MovementBase):
    """Modelo para crear un movimiento."""
    movement_date: date = Field(..., description="Fecha del movimiento")

class MovementUpdate(BaseModel):
    """Modelo para actualizar un movimiento."""
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    movement_type: Optional[MovementType] = None
    movement_date: Optional[date] = None

class MovementResponse(MovementBase):
    """Modelo de respuesta para movimientos."""
    id: str
    user_id: str
    movement_date: date
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MovementFilter(BaseModel):
    """Modelo para filtrar movimientos."""
    movement_type: Optional[MovementType] = None
    category: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None 