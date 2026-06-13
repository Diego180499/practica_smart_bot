import re
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Pregunta
from app.schemas.preguntas import PreguntaCreate, PreguntaUpdate, BusquedaResponse


def listar_preguntas(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    id_categoria: Optional[int] = None,
) -> List[Pregunta]:
    query = db.query(Pregunta).filter(Pregunta.activo == 1)
    if id_categoria is not None:
        query = query.filter(Pregunta.id_categoria == id_categoria)
    return query.offset(skip).limit(limit).all()


def obtener_pregunta(id: int, db: Session) -> Pregunta:
    pregunta = db.query(Pregunta).filter(Pregunta.id == id).first()
    if not pregunta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return pregunta


def _normalizar(texto: str) -> str:
    """Convierte a minúsculas y elimina signos de puntuación."""
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto.strip()


def buscar_respuesta(mensaje: str, db: Session) -> Optional[Pregunta]:
    """
    Lógica principal de búsqueda del bot:
    1. Busca coincidencia exacta parcial en el campo `pregunta` (LIKE).
    2. Si no hay resultado, busca cada palabra del mensaje en `palabras_clave`.
    Retorna la primera coincidencia o None.
    """
    normalizado = _normalizar(mensaje)

    # Paso 1: LIKE en campo pregunta
    resultado = db.query(Pregunta).filter(
        Pregunta.activo == 1,
        Pregunta.pregunta.ilike(f"%{normalizado}%"),
    ).first()

    if resultado:
        return resultado

    # Paso 2: LIKE en palabras_clave por cada palabra
    palabras = [p for p in normalizado.split() if len(p) > 2]
    for palabra in palabras:
        resultado = db.query(Pregunta).filter(
            Pregunta.activo == 1,
            Pregunta.palabras_clave.ilike(f"%{palabra}%"),
        ).first()
        if resultado:
            return resultado

    return None


def crear_pregunta(data: PreguntaCreate, db: Session) -> Pregunta:
    pregunta = Pregunta(**data.model_dump())
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    return pregunta


def actualizar_pregunta(id: int, data: PreguntaUpdate, db: Session) -> Pregunta:
    pregunta = obtener_pregunta(id, db)
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(pregunta, campo, valor)
    db.commit()
    db.refresh(pregunta)
    return pregunta


def eliminar_pregunta(id: int, db: Session) -> dict:
    pregunta = obtener_pregunta(id, db)
    pregunta.activo = 0
    db.commit()
    return {"mensaje": "Pregunta eliminada correctamente"}
