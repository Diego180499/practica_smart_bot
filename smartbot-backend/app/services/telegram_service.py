"""Servicio de mensajería vía Telegram Bot API.

Consume la API REST de Telegram directamente con httpx (sin librerías de
terceros específicas de Telegram). Documentación de referencia:
https://core.telegram.org/bots/api

Requisitos:
- Crear un bot con @BotFather en Telegram → obtener el token.
- El usuario DEBE enviar /start al bot al menos una vez para que Telegram
  permita que el bot le envíe mensajes (restricción de privacidad de la API).
- El chat_id es el identificador numérico del usuario en Telegram, NO el
  número de teléfono (la Bot API no expone búsqueda por teléfono).

El token y el chat_id por defecto se pueden pasar explícitamente (leídos desde
la tabla `configuracion_bot`) o, como fallback, desde variables de entorno:
    TELEGRAM_BOT_TOKEN   Token del bot, formato: "123456:ABC-DEF..."
    TELEGRAM_CHAT_ID     Chat ID por defecto.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

_TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"
_TIMEOUT_SEGUNDOS = 10


def _resolver_token(override: Optional[str]) -> str:
    """Retorna el token a usar: primero el override, luego la variable de entorno."""
    token = (override or os.getenv("TELEGRAM_BOT_TOKEN", "")).strip()
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN no está configurado. "
            "Configúralo en el panel de administración (configuracion_bot) "
            "o en el archivo .env del proyecto."
        )
    return token


def _resolver_chat_id(override: Optional[str]) -> str:
    """Retorna el chat_id a usar: primero el override, luego la variable de entorno."""
    chat_id = (override or os.getenv("TELEGRAM_CHAT_ID", "")).strip()
    if not chat_id:
        raise RuntimeError(
            "TELEGRAM_CHAT_ID no está configurado. "
            "Configúralo en el panel de administración (configuracion_bot) "
            "o en el archivo .env del proyecto, o pásalo explícitamente."
        )
    return chat_id


def _url(method: str, token: str) -> str:
    """Construye la URL completa para un método de la Bot API."""
    return _TELEGRAM_API_BASE.format(token=token, method=method)


def verificar_bot(token: Optional[str] = None) -> Dict[str, Any]:
    """Verifica que el token sea válido llamando a getMe.

    Args:
        token: Token del bot. Si se omite, se usa TELEGRAM_BOT_TOKEN del env.

    Returns:
        dict con la información del bot (id, first_name, username, etc.).

    Raises:
        RuntimeError: Si el token es inválido o hay error de red.
    """
    tok = _resolver_token(token)
    url = _url("getMe", tok)

    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.get(url)

    datos = respuesta.json()
    if not datos.get("ok"):
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(f"Telegram getMe falló: {descripcion}")

    return datos["result"]


def enviar_mensaje(
    texto: str,
    chat_id: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Envía un mensaje de texto a un usuario de Telegram.

    Llama a POST https://api.telegram.org/bot{TOKEN}/sendMessage

    Args:
        texto:   Contenido del mensaje a enviar.
        chat_id: Identificador del chat de destino. Si se omite, usa
                 TELEGRAM_CHAT_ID del entorno.
        token:   Token del bot. Si se omite, usa TELEGRAM_BOT_TOKEN del entorno.
                 En producción se debe pasar el valor leído desde configuracion_bot.

    Returns:
        dict con el objeto Message devuelto por Telegram.

    Raises:
        RuntimeError: Si Telegram devuelve ok=false o no hay token/chat_id.
        httpx.TimeoutException: Si la llamada excede _TIMEOUT_SEGUNDOS.
        httpx.RequestError: Si hay un problema de conectividad.
    """
    tok = _resolver_token(token)
    destino = _resolver_chat_id(chat_id)

    payload = {
        "chat_id": destino,
        "text": texto,
    }

    url = _url("sendMessage", tok)
    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.post(url, json=payload)

    datos = respuesta.json()
    if not datos.get("ok"):
        codigo = datos.get("error_code", "?")
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(
            f"Telegram sendMessage falló (código {codigo}): {descripcion}"
        )

    return datos["result"]


def registrar_webhook(url_webhook: str, token: Optional[str] = None) -> Dict[str, Any]:
    """Registra la URL del webhook en Telegram.

    Telegram llamará a esta URL con un POST cada vez que llegue un mensaje.

    Args:
        url_webhook: URL pública HTTPS del endpoint /api/bot/webhook del backend.
                     Ejemplo: "https://mi-servidor.com/api/bot/webhook"
        token:       Token del bot. Si se omite, usa TELEGRAM_BOT_TOKEN del env.

    Returns:
        dict con la respuesta de Telegram (ok, description).

    Raises:
        RuntimeError: Si Telegram rechaza el registro.
    """
    tok = _resolver_token(token)
    payload = {"url": url_webhook}

    url = _url("setWebhook", tok)
    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.post(url, json=payload)

    datos = respuesta.json()
    if not datos.get("ok"):
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(f"Telegram setWebhook falló: {descripcion}")

    return datos


def obtener_info_webhook(token: Optional[str] = None) -> Dict[str, Any]:
    """Consulta la información del webhook actualmente registrado.

    Returns:
        dict con url, pending_update_count, last_error_message, etc.
    """
    tok = _resolver_token(token)
    url = _url("getWebhookInfo", tok)

    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.get(url)

    datos = respuesta.json()
    if not datos.get("ok"):
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(f"Telegram getWebhookInfo falló: {descripcion}")

    return datos["result"]


def eliminar_webhook(token: Optional[str] = None) -> Dict[str, Any]:
    """Elimina el webhook registrado (útil para modo polling en desarrollo).

    Returns:
        dict con la respuesta de Telegram.
    """
    tok = _resolver_token(token)
    url = _url("deleteWebhook", tok)

    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.post(url)

    datos = respuesta.json()
    if not datos.get("ok"):
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(f"Telegram deleteWebhook falló: {descripcion}")

    return datos
