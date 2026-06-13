from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.consultas_log import ConsultaLogResponse
from app.services import log_service

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.get("/consultas", response_model=List[ConsultaLogResponse])
def listar_consultas(
    fecha_desde: Optional[datetime] = Query(None),
    fecha_hasta: Optional[datetime] = Query(None),
    telegram_id: Optional[int] = Query(None),
    solo_sin_respuesta: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return log_service.listar_consultas(
        db=db,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        telegram_id=telegram_id,
        solo_sin_respuesta=solo_sin_respuesta,
        skip=skip,
        limit=limit,
    )
