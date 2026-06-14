from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user, get_token_raw
from app.schemas.auth import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica al usuario y retorna un JWT."""
    usuario = auth_service.verificar_credenciales(data.username, data.password, db)
    token = auth_service.generar_token(usuario)
    return TokenResponse(access_token=token)


@router.post("/logout")
def logout(
    token: str = Depends(get_token_raw),
    _: str = Depends(get_current_user),
):
    """Invalida el token actual (blacklist en memoria)."""
    auth_service.invalidar_token(token)
    return {"mensaje": "Sesión cerrada correctamente"}
