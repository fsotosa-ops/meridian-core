from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """Atributos base compartidos por los modelos de usuario"""
    email: EmailStr = Field(..., description="Correo electrónico del BDR")
    plan_type: str = Field(default="free", description="Nivel de suscripción del usuario")

class UserCreate(UserBase):
    """Modelo para la creación inicial de un usuario"""
    # No se incluye hashed_api_key aquí porque se genera internamente
    pass

class User(UserBase):
    """Modelo completo que representa un usuario en la base de datos"""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True # Permite trabajar con objetos de Supabase/SQLAlchemy

class APIKeyResponse(BaseModel):
    """Modelo para entregar la API Key al usuario por única vez"""
    email: str
    api_key: str = Field(..., description="TU API KEY DE MERIDIAN. Guárdala en un lugar seguro.")
    note: str = "Esta llave es privada. No la compartas y úsala en el header X-Meridian-Key."