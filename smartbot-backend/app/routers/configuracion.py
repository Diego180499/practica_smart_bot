from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.configuracion import ConfiguracionResponse, ConfiguracionUpdate
from app.services import configuracion_service

router = APIRouter(prefix="/api/configuracion", tags=["Configuración del Bot"])


@router.get("", response_model=List[ConfiguracionResponse])
def obtener_configuracion(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return configuracion_service.obtener_configuracion(db)


@router.put("/{clave}", response_model=ConfiguracionResponse)
def actualizar_configuracion(
    clave: str,
    data: ConfiguracionUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return configuracion_service.actualizar_valor(clave, data.valor, db)
