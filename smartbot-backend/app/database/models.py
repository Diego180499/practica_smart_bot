from datetime import datetime
from sqlalchemy import (
    BigInteger, Column, DateTime, ForeignKey,
    Integer, SmallInteger, String, Text,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class UsuarioAdmin(Base):
    __tablename__ = "usuarios_admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(150), nullable=True)
    activo = Column(SmallInteger, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(SmallInteger, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    preguntas = relationship("Pregunta", back_populates="categoria")


class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    palabras_clave = Column(Text, nullable=True)
    activo = Column(SmallInteger, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="preguntas")
    consultas = relationship("ConsultaLog", back_populates="pregunta")


class ConfiguracionBot(Base):
    __tablename__ = "configuracion_bot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(100), nullable=False, unique=True)
    valor = Column(Text, nullable=True)
    descripcion = Column(String(255), nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)


class UsuarioTelegram(Base):
    __tablename__ = "usuarios_telegram"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100), nullable=True)
    nombre = Column(String(150), nullable=True)
    primera_interaccion = Column(DateTime, nullable=False, default=datetime.utcnow)
    ultima_interaccion = Column(DateTime, nullable=True)

    consultas = relationship("ConsultaLog", back_populates="usuario_telegram")


class ConsultaLog(Base):
    __tablename__ = "consultas_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario_telegram = Column(Integer, ForeignKey("usuarios_telegram.id"), nullable=True)
    id_pregunta = Column(Integer, ForeignKey("preguntas.id"), nullable=True)
    mensaje_recibido = Column(Text, nullable=False)
    respuesta_enviada = Column(Text, nullable=False)
    encontro_respuesta = Column(SmallInteger, nullable=False, default=0)
    fecha_consulta = Column(DateTime, nullable=False, default=datetime.utcnow)

    usuario_telegram = relationship("UsuarioTelegram", back_populates="consultas")
    pregunta = relationship("Pregunta", back_populates="consultas")