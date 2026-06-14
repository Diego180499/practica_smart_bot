from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.preguntas import (
    BusquedaResponse,
    PreguntaCreate,
    PreguntaResponse,
    PreguntaUpdate,
)
from app.services import preguntas_service, configuracion_service

router = APIRouter(prefix="/api/preguntas", tags=["Preguntas"])


@router.get("/buscar", response_model=BusquedaResponse)
def buscar_pregunta(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Endpoint público para que el bot busque respuesta a un mensaje."""
    pregunta = preguntas_service.buscar_respuesta(q, db)
    if pregunta:
        return BusquedaResponse(
            encontro_respuesta=True,
            pregunta_id=pregunta.id,
            pregunta=pregunta.pregunta,
            respuesta=pregunta.respuesta,
        )
    respuesta_default = (
        configuracion_service.obtener_valor("RESPUESTA_DEFAULT", db)
        or "No encontré una respuesta para tu consulta."
    )
    return BusquedaResponse(encontro_respuesta=False, respuesta=respuesta_default)


@router.get("", response_model=List[PreguntaResponse])
def listar_preguntas(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    id_categoria: Optional[int] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return preguntas_service.listar_preguntas(db, skip, limit, id_categoria)


@router.get("/{id}", response_model=PreguntaResponse)
def obtener_pregunta(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return preguntas_service.obtener_pregunta(id, db)


@router.post("", response_model=PreguntaResponse, status_code=201)
def crear_pregunta(
    data: PreguntaCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return preguntas_service.crear_pregunta(data, db)


@router.put("/{id}", response_model=PreguntaResponse)
def actualizar_pregunta(
    id: int,
    data: PreguntaUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return preguntas_service.actualizar_pregunta(id, data, db)


@router.delete("/{id}")
def eliminar_pregunta(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return preguntas_service.eliminar_pregunta(id, db)
