from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Categoria, Pregunta
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate


def listar_categorias(db: Session) -> List[Categoria]:
    return db.query(Categoria).filter(Categoria.activo == 1).all()


def obtener_categoria(id: int, db: Session) -> Categoria:
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return categoria


def crear_categoria(data: CategoriaCreate, db: Session) -> Categoria:
    existente = db.query(Categoria).filter(Categoria.nombre == data.nombre).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{data.nombre}'",
        )
    categoria = Categoria(**data.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def actualizar_categoria(id: int, data: CategoriaUpdate, db: Session) -> Categoria:
    categoria = obtener_categoria(id, db)
    cambios = data.model_dump(exclude_unset=True)

    if "nombre" in cambios:
        existente = db.query(Categoria).filter(
            Categoria.nombre == cambios["nombre"],
            Categoria.id != id,
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otra categoría con el nombre '{cambios['nombre']}'",
            )

    for campo, valor in cambios.items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)
    return categoria


def eliminar_categoria(id: int, db: Session) -> dict:
    categoria = obtener_categoria(id, db)

    preguntas_activas = db.query(Pregunta).filter(
        Pregunta.id_categoria == id,
        Pregunta.activo == 1,
    ).count()
    if preguntas_activas > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar: la categoría tiene {preguntas_activas} pregunta(s) activa(s)",
        )

    categoria.activo = 0
    db.commit()
    return {"mensaje": "Categoría eliminada correctamente"}
