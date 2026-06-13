from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.estadisticas import EstadisticasResponse
from app.services import estadisticas_service

router = APIRouter(prefix="/api/estadisticas", tags=["Estadísticas"])


@router.get("", response_model=EstadisticasResponse)
def obtener_estadisticas(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return estadisticas_service.obtener_estadisticas(db)
