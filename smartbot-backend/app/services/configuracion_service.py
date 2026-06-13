from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import ConfiguracionBot


def obtener_configuracion(db: Session) -> List[ConfiguracionBot]:
    return db.query(ConfiguracionBot).all()


def obtener_valor(clave: str, db: Session) -> Optional[str]:
    config = db.query(ConfiguracionBot).filter(ConfiguracionBot.clave == clave).first()
    return config.valor if config else None


def actualizar_valor(clave: str, valor: Optional[str], db: Session) -> ConfiguracionBot:
    config = db.query(ConfiguracionBot).filter(ConfiguracionBot.clave == clave).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clave de configuración '{clave}' no encontrada",
        )
    config.valor = valor
    db.commit()
    db.refresh(config)
    return config
