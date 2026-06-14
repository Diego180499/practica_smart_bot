"""
Script de datos iniciales (seed).
Inserta:
  - Usuario admin preconfigrado: IA1-User / IA1-password@_new
  - 4 categorías
  - 25 preguntas frecuentes distribuidas en las categorías
  - Configuración base del bot

Uso:
    python -m scripts.seed_data
"""
import sys
import os

# Permitir ejecutar desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, engine
from app.database.models import (
    Base,
    UsuarioAdmin,
    Categoria,
    Pregunta,
    ConfiguracionBot,
)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed(db: Session) -> None:
    # ------------------------------------------------------------------ #
    # 1. Usuario administrador                                             #
    # ------------------------------------------------------------------ #
    if not db.query(UsuarioAdmin).filter(UsuarioAdmin.username == "IA1-User").first():
        admin = UsuarioAdmin(
            username="IA1-User",
            password_hash=hash_password("IA1-password@_new"),
            nombre_completo="Administrador IA1",
            activo=1,
        )
        db.add(admin)
        db.commit()
        print("✓ Usuario admin creado: IA1-User")
    else:
        print("  Usuario admin ya existe, se omite.")

    # ------------------------------------------------------------------ #
    # 2. Categorías                                                        #
    # ------------------------------------------------------------------ #
    categorias_data = [
        {"nombre": "Información General", "descripcion": "Preguntas sobre el sistema y la empresa"},
        {"nombre": "Soporte Técnico",      "descripcion": "Problemas técnicos y soluciones"},
        {"nombre": "Facturación y Pagos",  "descripcion": "Consultas sobre cobros, pagos y facturación"},
        {"nombre": "Servicios",            "descripcion": "Información sobre los servicios disponibles"},
    ]

    cat_ids: dict[str, int] = {}
    for cat_data in categorias_data:
        existente = db.query(Categoria).filter(Categoria.nombre == cat_data["nombre"]).first()
        if not existente:
            cat = Categoria(**cat_data)
            db.add(cat)
            db.commit()
            db.refresh(cat)
            cat_ids[cat.nombre] = cat.id
            print(f"✓ Categoría creada: {cat.nombre}")
        else:
            cat_ids[existente.nombre] = existente.id
            print(f"  Categoría ya existe: {existente.nombre}")

    # ------------------------------------------------------------------ #
    # 3. Preguntas frecuentes (25 preguntas)                              #
    # ------------------------------------------------------------------ #
    preguntas_data = [
        # --- Información General (7) ---
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Cuál es el horario de atención?",
            "respuesta": "Nuestro horario de atención es de lunes a viernes de 8:00 a 18:00 horas y sábados de 9:00 a 13:00 horas.",
            "palabras_clave": "horario, atencion, horas, apertura, cierre",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Dónde están ubicados?",
            "respuesta": "Estamos ubicados en la Zona 10, Ciudad de Guatemala. Puedes encontrarnos en Google Maps buscando 'SmartBot Guatemala'.",
            "palabras_clave": "ubicacion, direccion, lugar, donde, mapa",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Cómo puedo contactarlos?",
            "respuesta": "Puedes contactarnos por este chat, por correo a soporte@smartbot.gt, o llamando al +502 2222-3333.",
            "palabras_clave": "contacto, telefono, correo, email, comunicacion",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Tienen redes sociales?",
            "respuesta": "Sí, nos encuentras como @SmartBotGT en Facebook, Instagram y Twitter/X.",
            "palabras_clave": "redes, sociales, facebook, instagram, twitter",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Cuánto tiempo llevan en el mercado?",
            "respuesta": "Llevamos más de 5 años brindando soluciones tecnológicas en Guatemala y Centroamérica.",
            "palabras_clave": "tiempo, mercado, años, experiencia, historia",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Trabajan con empresas de otros países?",
            "respuesta": "Sí, trabajamos con clientes de Guatemala, El Salvador, Honduras, Costa Rica y México.",
            "palabras_clave": "internacional, paises, extranjero, centroamerica",
        },
        {
            "id_categoria": cat_ids["Información General"],
            "pregunta": "¿Cómo registro una queja o sugerencia?",
            "respuesta": "Puedes enviar tu queja o sugerencia al correo feedback@smartbot.gt o usando el formulario en nuestra web.",
            "palabras_clave": "queja, sugerencia, reclamo, feedback, comentario",
        },

        # --- Soporte Técnico (6) ---
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "No puedo iniciar sesión en el sistema",
            "respuesta": "Verifica que tu usuario y contraseña sean correctos. Si olvidaste tu contraseña, usa la opción '¿Olvidaste tu contraseña?' en la pantalla de login.",
            "palabras_clave": "login, sesion, contraseña, acceso, iniciar",
        },
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "La aplicación no carga correctamente",
            "respuesta": "Prueba vaciando el caché de tu navegador (Ctrl+Shift+Del) o intenta desde otro navegador. Si el problema persiste, contáctanos.",
            "palabras_clave": "carga, aplicacion, navegador, cache, error",
        },
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "¿Cómo cambio mi contraseña?",
            "respuesta": "Ingresa a tu perfil → Configuración → Cambiar contraseña. Necesitarás ingresar tu contraseña actual y la nueva dos veces.",
            "palabras_clave": "cambiar, contraseña, password, seguridad, actualizar",
        },
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "¿Qué hago si olvidé mi contraseña?",
            "respuesta": "Haz clic en '¿Olvidaste tu contraseña?' en la pantalla de login y te enviaremos un correo para restablecerla.",
            "palabras_clave": "olvide, contraseña, recuperar, restablecer",
        },
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "El sistema está lento, ¿qué puedo hacer?",
            "respuesta": "Verifica tu conexión a internet. Si el problema continúa, puede ser mantenimiento programado. Revisa nuestro canal de estado en status.smartbot.gt.",
            "palabras_clave": "lento, rendimiento, velocidad, lag, performance",
        },
        {
            "id_categoria": cat_ids["Soporte Técnico"],
            "pregunta": "¿Cómo reporto un bug o error técnico?",
            "respuesta": "Puedes reportar errores técnicos en soporte@smartbot.gt con capturas de pantalla y descripción del problema. Respondemos en 24 horas.",
            "palabras_clave": "bug, error, falla, reporte, tecnico",
        },

        # --- Facturación y Pagos (6) ---
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Cuáles son los métodos de pago aceptados?",
            "respuesta": "Aceptamos tarjetas Visa y Mastercard (crédito y débito), transferencias bancarias y pago en efectivo en agencias autorizadas.",
            "palabras_clave": "pago, metodo, tarjeta, visa, mastercard, transferencia, efectivo",
        },
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Cómo obtengo mi factura?",
            "respuesta": "Tu factura se envía automáticamente al correo registrado al realizar cada pago. También puedes descargarla desde tu portal de cliente.",
            "palabras_clave": "factura, recibo, comprobante, pago",
        },
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Cada cuánto se factura el servicio?",
            "respuesta": "La facturación es mensual, el día 1 de cada mes. Puedes cambiar a facturación anual con un 10% de descuento.",
            "palabras_clave": "facturacion, mensual, anual, ciclo, frecuencia",
        },
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Puedo solicitar un reembolso?",
            "respuesta": "Sí, aceptamos solicitudes de reembolso dentro de los primeros 15 días del mes facturado. Escríbenos a facturacion@smartbot.gt.",
            "palabras_clave": "reembolso, devolucion, cancelacion, dinero",
        },
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Qué pasa si no pago a tiempo?",
            "respuesta": "Si el pago no se procesa en los primeros 5 días del mes, el servicio se suspende temporalmente hasta regularizar el pago.",
            "palabras_clave": "mora, retraso, suspension, pago, vencimiento",
        },
        {
            "id_categoria": cat_ids["Facturación y Pagos"],
            "pregunta": "¿Tienen planes de precios?",
            "respuesta": "Sí, ofrecemos planes Básico, Estándar y Empresarial. Visita smartbot.gt/precios para ver los detalles de cada plan.",
            "palabras_clave": "precio, plan, costo, tarifa, paquete",
        },

        # --- Servicios (6) ---
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿Qué servicios ofrecen?",
            "respuesta": "Ofrecemos bots de Telegram personalizados, paneles administrativos web, APIs REST, integración con bases de datos y capacitación.",
            "palabras_clave": "servicios, oferta, productos, soluciones",
        },
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿Ofrecen servicio de capacitación?",
            "respuesta": "Sí, incluimos sesiones de capacitación con cada implementación. También ofrecemos capacitaciones adicionales bajo demanda.",
            "palabras_clave": "capacitacion, entrenamiento, curso, formacion",
        },
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿Pueden desarrollar bots personalizados?",
            "respuesta": "Sí, desarrollamos bots a medida según los requerimientos del cliente. Contáctanos para agendar una consultoría gratuita.",
            "palabras_clave": "personalizado, desarrollo, bot, medida, custom",
        },
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿El sistema funciona en dispositivos móviles?",
            "respuesta": "Sí, el panel administrativo es totalmente responsive y funciona en smartphones y tablets desde cualquier navegador moderno.",
            "palabras_clave": "movil, celular, tablet, responsive, smartphone",
        },
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿Tienen garantía de disponibilidad (SLA)?",
            "respuesta": "Garantizamos un 99.5% de disponibilidad mensual para todos los planes. Los detalles del SLA están en nuestros términos de servicio.",
            "palabras_clave": "sla, disponibilidad, garantia, uptime, servicio",
        },
        {
            "id_categoria": cat_ids["Servicios"],
            "pregunta": "¿Cómo empiezo a usar el servicio?",
            "respuesta": "Regístrate en smartbot.gt, elige tu plan y sigue el asistente de configuración. En menos de 10 minutos tendrás tu bot activo.",
            "palabras_clave": "empezar, inicio, registro, comenzar, activar",
        },
    ]

    insertadas = 0
    for p_data in preguntas_data:
        existente = db.query(Pregunta).filter(
            Pregunta.pregunta == p_data["pregunta"]
        ).first()
        if not existente:
            pregunta = Pregunta(**p_data)
            db.add(pregunta)
            insertadas += 1

    db.commit()
    print(f"✓ Preguntas insertadas: {insertadas} (de {len(preguntas_data)} totales)")

    # ------------------------------------------------------------------ #
    # 4. Configuración del bot                                            #
    # ------------------------------------------------------------------ #
    configuraciones = [
        {
            "clave": "TELEGRAM_BOT_TOKEN",
            "valor": os.getenv("TELEGRAM_BOT_TOKEN", ""),
            "descripcion": "Token del bot de Telegram (obtenido desde @BotFather)",
        },
        {
            "clave": "TELEGRAM_CHAT_ID",
            "valor": os.getenv("TELEGRAM_CHAT_ID", ""),
            "descripcion": "ID del grupo o chat de Telegram donde el bot responde",
        },
        {
            "clave": "RESPUESTA_DEFAULT",
            "valor": "Lo siento, no encontré una respuesta para tu consulta. Por favor escribe a soporte@smartbot.gt o llama al +502 2222-3333.",
            "descripcion": "Mensaje de respuesta cuando no se encuentra coincidencia",
        },
        {
            "clave": "BOT_ACTIVO",
            "valor": "1",
            "descripcion": "Habilitar (1) o deshabilitar (0) el bot",
        },
    ]

    from app.database.models import ConfiguracionBot
    for cfg in configuraciones:
        existente = db.query(ConfiguracionBot).filter(
            ConfiguracionBot.clave == cfg["clave"]
        ).first()
        if not existente:
            db.add(ConfiguracionBot(**cfg))
            print(f"✓ Config creada: {cfg['clave']}")
        else:
            print(f"  Config ya existe: {cfg['clave']}")
    db.commit()

    print("\n✅ Seed completado exitosamente.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
