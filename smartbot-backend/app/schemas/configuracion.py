from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ConfiguracionResponse(BaseModel):
    id: int
    clave: str
    valor: Optional[str] = None
    descripcion: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConfiguracionUpdate(BaseModel):
    valor: Optional[str] = None
