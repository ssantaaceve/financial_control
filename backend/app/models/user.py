from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Modelo base para usuarios."""
    email: EmailStr
    name: str

class UserCreate(UserBase):
    """Modelo para crear un usuario."""
    password: str

class UserLogin(BaseModel):
    """Modelo para login de usuario."""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Modelo de respuesta para usuarios."""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    """Modelo para actualizar un usuario."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    """Modelo para tokens JWT."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Modelo para datos del token."""
    user_id: Optional[str] = None 