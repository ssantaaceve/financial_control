from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum

class BudgetPeriod(str, Enum):
    """Períodos de presupuesto."""
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    ANUAL = "anual"

class BudgetBase(BaseModel):
    """Modelo base para presupuestos."""
    category: str = Field(..., min_length=1, description="Categoría del presupuesto")
    max_amount: float = Field(..., gt=0, description="Monto máximo del presupuesto")
    period: BudgetPeriod = Field(..., description="Período del presupuesto")
    start_date: date = Field(..., description="Fecha de inicio")
    end_date: date = Field(..., description="Fecha de fin")

class BudgetCreate(BudgetBase):
    """Modelo para crear un presupuesto."""
    pass

class BudgetUpdate(BaseModel):
    """Modelo para actualizar un presupuesto."""
    category: Optional[str] = Field(None, min_length=1)
    max_amount: Optional[float] = Field(None, gt=0)
    period: Optional[BudgetPeriod] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class BudgetResponse(BudgetBase):
    """Modelo de respuesta para presupuestos."""
    id: str
    user_id: str
    current_amount: float = Field(0, description="Monto actual gastado")
    remaining_amount: float = Field(0, description="Monto restante")
    percentage_used: float = Field(0, description="Porcentaje usado")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BudgetSummary(BaseModel):
    """Modelo para resumen de presupuestos."""
    total_budgets: int
    total_allocated: float
    total_spent: float
    total_remaining: float
    budgets: list[BudgetResponse] 