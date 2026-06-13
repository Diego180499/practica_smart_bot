"""Servicio principal del bot: orquesta la recepción de mensajes de Telegram,
la búsqueda de respuestas en la base de datos y el envío de la respuesta
de vuelta al usuario a través de la Bot API.
"""
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from sqlalchemy.orm import Session

from app.database.models import UsuarioTelegram
from app.services import configuracion_service, preguntas_service, log_service
from app.services import telegram_service

# Claves de configuración en la tabla configuracion_bot
_CLAVE_TOKEN = "TELEGRAM_BOT_TOKEN"
_CLAVE_RESPUESTA_DEFAULT = "RESPUESTA_DEFAULT"
_CLAVE_BOT_ACTIVO = "BOT_ACTIVO"

RESPUESTA_FALLBACK = (
    "Lo siento, no encontré una respuesta para tu consulta. "
    "Por favor contacta al soporte."
)


def _obtener_token(db: Session) -> Optional[str]:
    """Lee el token del bot desde la tabla configuracion_bot."""
    return configuracion_service.obtener_valor(_CLAVE_TOKEN, db) or None


def _bot_activo(db: Session) -> bool:
    """Retorna True si el bot está habilitado en configuracion_bot."""
    valor = configuracion_service.obtener_valor(_CLAVE_BOT_ACTIVO, db)
    return str(valor).strip() == "1"


def registrar_usuario_telegram(
    telegram_user: Dict[str, Any], db: Session
) -> UsuarioTelegram:
    """Crea o actualiza el registro del usuario de Telegram."""
    telegram_id = telegram_user.get("id")
    usuario = db.query(UsuarioTelegram).filter(
        UsuarioTelegram.telegram_id == telegram_id
    ).first()

    nombre_parts = [
        telegram_user.get("first_name", ""),
        telegram_user.get("last_name", ""),
    ]
    nombre = " ".join(p for p in nombre_parts if p).strip() or None

    if usuario:
        usuario.username = telegram_user.get("username")
        usuario.nombre = nombre
        usuario.ultima_interaccion = datetime.utcnow()
    else:
        usuario = UsuarioTelegram(
            telegram_id=telegram_id,
            username=telegram_user.get("username"),
            nombre=nombre,
            ultima_interaccion=datetime.utcnow(),
        )
        db.add(usuario)

    db.commit()
    db.refresh(usuario)
    return usuario


def procesar_mensaje(telegram_update: Dict[str, Any], db: Session) -> str:
    """Punto de entrada del webhook de Telegram.

    Flujo completo:
    1. Verifica si el bot está activo.
    2. Extrae el mensaje y el usuario del objeto Update.
    3. Registra / actualiza el usuario de Telegram.
    4. Busca la respuesta en la base de datos.
    5. Registra la consulta en consultas_log.
    6. Envía la respuesta de vuelta al usuario via Telegram Bot API.

    Returns:
        Texto de la respuesta que se envió (o intentó enviar) al usuario.
    """
    # 1. Verificar si el bot está activo
    if not _bot_activo(db):
        return "Bot desactivado"

    message = telegram_update.get("message", {})
    if not message:
        return "Update sin mensaje de texto, ignorado"

    telegram_user_data = message.get("from", {})
    texto_mensaje: str = message.get("text", "").strip()
    chat_id: str = str(message.get("chat", {}).get("id", ""))

    if not texto_mensaje:
        return "Mensaje vacío, ignorado"

    # 2 & 3. Registrar / actualizar usuario
    usuario_telegram = None
    if telegram_user_data.get("id"):
        usuario_telegram = registrar_usuario_telegram(telegram_user_data, db)

    # 4. Buscar respuesta
    pregunta_encontrada = preguntas_service.buscar_respuesta(texto_mensaje, db)

    if pregunta_encontrada:
        respuesta = pregunta_encontrada.respuesta
        encontro = True
        id_pregunta = pregunta_encontrada.id
    else:
        respuesta = (
            configuracion_service.obtener_valor(_CLAVE_RESPUESTA_DEFAULT, db)
            or RESPUESTA_FALLBACK
        )
        encontro = False
        id_pregunta = None

    # 5. Registrar en log
    log_service.registrar_consulta(
        db=db,
        mensaje_recibido=texto_mensaje,
        respuesta_enviada=respuesta,
        encontro_respuesta=encontro,
        id_usuario_telegram=usuario_telegram.id if usuario_telegram else None,
        id_pregunta=id_pregunta,
    )

    # 6. Enviar respuesta de vuelta al usuario via Telegram Bot API
    if chat_id:
        token = _obtener_token(db)
        try:
            telegram_service.enviar_mensaje(
                texto=respuesta,
                chat_id=chat_id,
                token=token,
            )
        except (RuntimeError, httpx.RequestError) as exc:
            # No propagar el error al webhook para que Telegram no reintente
            # el update indefinidamente. El log ya quedó guardado.
            print(f"[bot_service] Error enviando respuesta a Telegram: {exc}")

    return respuesta
