from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.models import Base
from app.routers import auth, categorias, preguntas, configuracion, bot, logs, estadisticas


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea todas las tablas si no existen
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SmartBot API",
    description="API REST para el sistema de respuestas automatizadas SmartBot",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — ajustar origins en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
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
