from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import verificar_token

_bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> str:
    """
    Dependencia FastAPI para rutas protegidas.
    Extrae y valida el JWT del header Authorization: Bearer <token>.
    Retorna el username del token si es válido.
    """
    token = credentials.credentials
    return verificar_token(token)


def get_token_raw(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> str:
    """Retorna el token crudo (necesario para logout/blacklist)."""
    return credentials.credentials
