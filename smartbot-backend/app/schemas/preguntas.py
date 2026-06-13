from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class PreguntaBase(BaseModel):
    pregunta: str
    respuesta: str
    id_categoria: Optional[int] = None
    palabras_clave: Optional[str] = None


class PreguntaCreate(PreguntaBase):
    @field_validator("pregunta", "respuesta")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()


class PreguntaUpdate(BaseModel):
    pregunta: Optional[str] = None
    respuesta: Optional[str] = None
    id_categoria: Optional[int] = None
    palabras_clave: Optional[str] = None
    activo: Optional[int] = None


class PreguntaResponse(PreguntaBase):
    id: int
    activo: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BusquedaResponse(BaseModel):
    encontro_respuesta: bool
    pregunta_id: Optional[int] = None
    pregunta: Optional[str] = None
    respuesta: str
