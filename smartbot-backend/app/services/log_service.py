from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import ConsultaLog


def registrar_consulta(
    db: Session,
    mensaje_recibido: str,
    respuesta_enviada: str,
    encontro_respuesta: bool,
    id_usuario_telegram: Optional[int] = None,
    id_pregunta: Optional[int] = None,
) -> ConsultaLog:
    log = ConsultaLog(
        id_usuario_telegram=id_usuario_telegram,
        id_pregunta=id_pregunta,
        mensaje_recibido=mensaje_recibido,
        respuesta_enviada=respuesta_enviada,
        encontro_respuesta=1 if encontro_respuesta else 0,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def listar_consultas(
    db: Session,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    telegram_id: Optional[int] = None,
    solo_sin_respuesta: bool = False,
    skip: int = 0,
    limit: int = 50,
) -> List[ConsultaLog]:
    query = db.query(ConsultaLog)

    if fecha_desde:
        query = query.filter(ConsultaLog.fecha_consulta >= fecha_desde)
    if fecha_hasta:
        query = query.filter(ConsultaLog.fecha_consulta <= fecha_hasta)
    if telegram_id:
        from app.database.models import UsuarioTelegram
        ut = db.query(UsuarioTelegram).filter(
            UsuarioTelegram.telegram_id == telegram_id
        ).first()
        if ut:
            query = query.filter(ConsultaLog.id_usuario_telegram == ut.id)
    if solo_sin_respuesta:
        query = query.filter(ConsultaLog.encontro_respuesta == 0)

    return query.order_by(ConsultaLog.fecha_consulta.desc()).offset(skip).limit(limit).all()
