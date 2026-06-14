from typing import List
from pydantic import BaseModel


class TopPregunta(BaseModel):
    id: int
    pregunta: str
    total_consultas: int


class TopUsuario(BaseModel):
    telegram_id: int
    nombre: str
    total_consultas: int


class DistribucionCategoria(BaseModel):
    categoria: str
    total_preguntas: int
    total_consultas: int


class EstadisticasResponse(BaseModel):
    total_consultas: int
    consultas_sin_respuesta: int
    total_usuarios_unicos: int
    top_preguntas: List[TopPregunta]
    top_usuarios: List[TopUsuario]
    distribucion_categorias: List[DistribucionCategoria]
