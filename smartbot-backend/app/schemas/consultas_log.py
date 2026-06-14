from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ConsultaLogResponse(BaseModel):
    id: int
    id_usuario_telegram: Optional[int] = None
    id_pregunta: Optional[int] = None
    mensaje_recibido: str
    respuesta_enviada: str
    encontro_respuesta: int
    fecha_consulta: datetime

    model_config = {"from_attributes": True}


class ConsultaLogFiltros(BaseModel):
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    telegram_id: Optional[int] = None
    solo_sin_respuesta: bool = False
