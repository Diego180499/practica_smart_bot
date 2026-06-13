from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.preguntas import BusquedaResponse
from app.services import bot_service, preguntas_service, configuracion_service
from app.services import telegram_service

router = APIRouter(prefix="/api/bot", tags=["Bot / Webhook"])


@router.post("/webhook")
def webhook_telegram(update: Dict[str, Any], db: Session = Depends(get_db)):
    """Recibe actualizaciones de Telegram (webhook).

    Telegram enviará un POST con el objeto Update a este endpoint cada vez
    que un usuario escriba al bot. El servicio busca la respuesta en la DB,
    la registra en el log y la envía de vuelta al usuario via Bot API.
    """
    respuesta = bot_service.procesar_mensaje(update, db)
    return {"status": "ok", "respuesta_enviada": respuesta}


@router.get("/consulta", response_model=BusquedaResponse)
def consulta_directa(
    mensaje: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Endpoint de prueba: busca respuesta para un texto dado sin pasar por Telegram."""
    pregunta = preguntas_service.buscar_respuesta(mensaje, db)
    if pregunta:
        return BusquedaResponse(
            encontro_respuesta=True,
            pregunta_id=pregunta.id,
            pregunta=pregunta.pregunta,
            respuesta=pregunta.respuesta,
        )
    respuesta_default = (
        configuracion_service.obtener_valor("RESPUESTA_DEFAULT", db)
        or "No encontré una respuesta para tu consulta."
    )
    return BusquedaResponse(encontro_respuesta=False, respuesta=respuesta_default)


@router.get("/verificar")
def verificar_bot(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    """Verifica que el token de Telegram configurado sea válido (llama a getMe).

    Útil para confirmar que el token guardado en configuracion_bot funciona
    antes de registrar el webhook.
    """
    token = configuracion_service.obtener_valor("TELEGRAM_BOT_TOKEN", db)
    try:
        info = telegram_service.verificar_bot(token=token)
        return {
            "status": "ok",
            "bot": info,
        }
    except RuntimeError as exc:
        return {"status": "error", "detalle": str(exc)}


@router.post("/registrar-webhook")
def registrar_webhook(
    url_webhook: str = Body(..., embed=True, description="URL pública HTTPS del endpoint /api/bot/webhook"),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    """Registra la URL del webhook en Telegram.

    Telegram empezará a enviar los updates (mensajes) a la URL indicada.
    La URL debe ser HTTPS pública y apuntar a /api/bot/webhook del backend.

    Ejemplo de body:
    {
        "url_webhook": "https://mi-servidor.com/api/bot/webhook"
    }
    """
    token = configuracion_service.obtener_valor("TELEGRAM_BOT_TOKEN", db)
    try:
        resultado = telegram_service.registrar_webhook(
            url_webhook=url_webhook,
            token=token,
        )
        return {"status": "ok", "telegram_response": resultado}
    except RuntimeError as exc:
        return {"status": "error", "detalle": str(exc)}


@router.get("/info-webhook")
def info_webhook(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    """Consulta la información del webhook actualmente registrado en Telegram."""
    token = configuracion_service.obtener_valor("TELEGRAM_BOT_TOKEN", db)
    try:
        info = telegram_service.obtener_info_webhook(token=token)
        return {"status": "ok", "webhook": info}
    except RuntimeError as exc:
        return {"status": "error", "detalle": str(exc)}


@router.delete("/webhook")
def eliminar_webhook(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    """Elimina el webhook registrado en Telegram (útil para cambiar de URL o modo polling)."""
    token = configuracion_service.obtener_valor("TELEGRAM_BOT_TOKEN", db)
    try:
        resultado = telegram_service.eliminar_webhook(token=token)
        return {"status": "ok", "telegram_response": resultado}
    except RuntimeError as exc:
        return {"status": "error", "detalle": str(exc)}
