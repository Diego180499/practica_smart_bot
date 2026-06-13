import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, SessionLocal
from app.database.models import Base
from app.routers import auth, categorias, preguntas, configuracion, bot, logs, estadisticas
from app.services import bot_service, telegram_service, configuracion_service


async def _polling_loop():
    """Background task: long-polling de Telegram (modo desarrollo / localhost)."""
    offset = None
    print("[polling] Iniciando loop de polling de Telegram...")

    while True:
        db = SessionLocal()
        try:
            # Leer token: primero desde la DB, luego desde el env
            token = configuracion_service.obtener_valor("TELEGRAM_BOT_TOKEN", db)
            if not token:
                token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip() or None

            if not token:
                print("[polling] TELEGRAM_BOT_TOKEN no configurado. Reintentando en 30s...")
                await asyncio.sleep(30)
                continue

            # Si hay webhook activo, el polling no es necesario
            try:
                info = telegram_service.obtener_info_webhook(token=token)
                if info.get("url"):
                    print(f"[polling] Webhook activo en {info['url']}. Polling desactivado.")
                    await asyncio.sleep(60)
                    continue
            except Exception:
                pass

            # Obtener updates via long-polling (30s de espera en Telegram)
            updates = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: telegram_service.obtener_updates(offset=offset, timeout=30, token=token),
            )

            for update in updates:
                try:
                    bot_service.procesar_mensaje(update, db)
                except Exception as exc:
                    print(f"[polling] Error procesando update {update.get('update_id')}: {exc}")
                offset = update["update_id"] + 1

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            print(f"[polling] Error en loop: {exc}. Reintentando en 5s...")
            await asyncio.sleep(5)
        finally:
            db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    polling_task = asyncio.create_task(_polling_loop())
    yield
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="SmartBot API",
    description="API REST para el sistema de respuestas automatizadas SmartBot",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(preguntas.router)
app.include_router(configuracion.router)
app.include_router(bot.router)
app.include_router(logs.router)
app.include_router(estadisticas.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "servicio": "SmartBot API v1.0.0"}
