from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services import categorias_service

router = APIRouter(prefix="/api/categorias", tags=["Categorías"])


@router.get("", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return categorias_service.listar_categorias(db)


@router.get("/{id}", response_model=CategoriaResponse)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    return categorias_service.obtener_categoria(id, db)


@router.post("", response_model=CategoriaResponse, status_code=201)
def crear_categoria(
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return categorias_service.crear_categoria(data, db)


@router.put("/{id}", response_model=CategoriaResponse)
def actualizar_categoria(
    id: int,
    data: CategoriaUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return categorias_service.actualizar_categoria(id, data, db)


@router.delete("/{id}")
def eliminar_categoria(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    return categorias_service.eliminar_categoria(id, db)
