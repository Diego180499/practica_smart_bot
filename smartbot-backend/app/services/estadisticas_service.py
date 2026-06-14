from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import ConsultaLog, Pregunta, Categoria, UsuarioTelegram
from app.schemas.estadisticas import (
    EstadisticasResponse,
    TopPregunta,
    TopUsuario,
    DistribucionCategoria,
)


def obtener_estadisticas(db: Session) -> EstadisticasResponse:
    total_consultas = db.query(func.count(ConsultaLog.id)).scalar() or 0
    consultas_sin_respuesta = (
        db.query(func.count(ConsultaLog.id))
        .filter(ConsultaLog.encontro_respuesta == 0)
        .scalar() or 0
    )
    total_usuarios_unicos = db.query(func.count(UsuarioTelegram.id)).scalar() or 0

    # Top 10 preguntas más consultadas
    top_raw = (
        db.query(Pregunta.id, Pregunta.pregunta, func.count(ConsultaLog.id).label("total"))
        .join(ConsultaLog, ConsultaLog.id_pregunta == Pregunta.id)
        .group_by(Pregunta.id, Pregunta.pregunta)
        .order_by(func.count(ConsultaLog.id).desc())
        .limit(10)
        .all()
    )
    top_preguntas = [
        TopPregunta(id=r.id, pregunta=r.pregunta, total_consultas=r.total)
        for r in top_raw
    ]

    # Top 10 usuarios por cantidad de consultas
    top_usuarios_raw = (
        db.query(
            UsuarioTelegram.telegram_id,
            UsuarioTelegram.nombre,
            func.count(ConsultaLog.id).label("total"),
        )
        .join(ConsultaLog, ConsultaLog.id_usuario_telegram == UsuarioTelegram.id)
        .group_by(UsuarioTelegram.telegram_id, UsuarioTelegram.nombre)
        .order_by(func.count(ConsultaLog.id).desc())
        .limit(10)
        .all()
    )
    top_usuarios = [
        TopUsuario(
            telegram_id=r.telegram_id,
            nombre=r.nombre or "Sin nombre",
            total_consultas=r.total,
        )
        for r in top_usuarios_raw
    ]

    # Distribución por categoría
    distribucion_raw = (
        db.query(
            Categoria.nombre,
            func.count(Pregunta.id).label("total_preguntas"),
            func.count(ConsultaLog.id).label("total_consultas"),
        )
        .outerjoin(Pregunta, Pregunta.id_categoria == Categoria.id)
        .outerjoin(ConsultaLog, ConsultaLog.id_pregunta == Pregunta.id)
        .filter(Categoria.activo == 1)
        .group_by(Categoria.nombre)
        .all()
    )
    distribucion_categorias = [
        DistribucionCategoria(
            categoria=r.nombre,
            total_preguntas=r.total_preguntas or 0,
            total_consultas=r.total_consultas or 0,
        )
        for r in distribucion_raw
    ]

    return EstadisticasResponse(
        total_consultas=total_consultas,
        consultas_sin_respuesta=consultas_sin_respuesta,
        total_usuarios_unicos=total_usuarios_unicos,
        top_preguntas=top_preguntas,
        top_usuarios=top_usuarios,
        distribucion_categorias=distribucion_categorias,
    )
