from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import UsuarioAdmin

# Blacklist en memoria para tokens invalidados (logout)
_token_blacklist: set[str] = set()


def verificar_credenciales(username: str, password: str, db: Session) -> UsuarioAdmin:
    usuario = db.query(UsuarioAdmin).filter(
        UsuarioAdmin.username == username,
        UsuarioAdmin.activo == 1,
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    password_valida = bcrypt.checkpw(
        password.encode("utf-8"),
        usuario.password_hash.encode("utf-8"),
    )
    if not password_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    return usuario


def generar_token(usuario: UsuarioAdmin) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": usuario.username, "exp": expiracion}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verificar_token(token: str) -> str:
    """Decodifica y valida el JWT. Retorna el username o lanza 401."""
    if token in _token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalidado",
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )


def invalidar_token(token: str) -> None:
    """Agrega el token a la blacklist (logout)."""
    _token_blacklist.add(token)
