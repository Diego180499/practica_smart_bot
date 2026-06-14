# Manual Técnico — SmartBot Admin

> **Versión:** 1.0.0  
> **Fecha:** Junio 2026  
> **Proyecto:** Sistema de respuestas automatizadas con bot de Telegram

---

## Tabla de Contenido

1. [Frontend — SmartBot Admin](#1-frontend--smartbot-admin)
   - 1.1 [Tecnologías Usadas](#11-tecnologías-usadas)
   - 1.2 [Patrón de Diseño](#12-patrón-de-diseño)
   - 1.3 [Responsabilidad de Cada Vista](#13-responsabilidad-de-cada-vista)
   - 1.4 [Distribución de Carpetas](#14-distribución-de-carpetas)
   - 1.5 [Consumo de la API REST](#15-consumo-de-la-api-rest)
   - 1.6 [Paleta de Colores](#16-paleta-de-colores)
   - 1.7 [Gestión de Estado y Autenticación](#17-gestión-de-estado-y-autenticación)
   - 1.8 [Despliegue del Frontend](#18-despliegue-del-frontend)

2. [Backend — SmartBot API](#2-backend--smartbot-api)
   - 2.1 [Tecnologías Usadas](#21-tecnologías-usadas)
   - 2.2 [Patrón de Diseño](#22-patrón-de-diseño)
   - 2.3 [Detalle de Endpoints](#23-detalle-de-endpoints)
   - 2.4 [Distribución de Carpetas](#24-distribución-de-carpetas)
   - 2.5 [Modelos de Base de Datos](#25-modelos-de-base-de-datos)
   - 2.6 [Lógica de Búsqueda de Respuestas (Equivalente Prolog)](#26-lógica-de-búsqueda-de-respuestas-equivalente-prolog)
   - 2.7 [Responsabilidades de Python](#27-responsabilidades-de-python)
   - 2.8 [Pasos para Iniciar la Aplicación Backend](#28-pasos-para-iniciar-la-aplicación-backend)

---

---

# 1. Frontend — SmartBot Admin

## 1.1 Tecnologías Usadas

El frontend es una **Single Page Application (SPA) construida con HTML, CSS y JavaScript puro (Vanilla JS)**, sin frameworks de UI. Las tecnologías específicas son:

| Tecnología | Versión | Descripción |
|---|---|---|
| HTML5 | — | Estructura semántica de las vistas |
| CSS3 | — | Estilos personalizados con variables CSS (CSS Custom Properties) |
| JavaScript (ES Modules) | ES2020+ | Lógica del cliente, consumo de API, manejo del DOM |
| Google Fonts (Inter) | — | Tipografía principal: familia `Inter` en pesos 400, 500, 600, 700 |
| Nginx | 1.25-alpine | Servidor web para servir los archivos estáticos en producción |
| Docker | — | Containerización del frontend vía imagen nginx |

El uso de módulos ES nativos (`type="module"`) permite importar y exportar funciones entre archivos JS sin necesidad de un bundler (Webpack, Vite, etc.), manteniendo la arquitectura modular sin agregar complejidad de build.

---

## 1.2 Patrón de Diseño

El frontend implementa el patrón **Módulo + Router Hash-based SPA**.

**Patrón Módulo (Module Pattern):** Cada sección funcional del dashboard tiene su propio archivo JavaScript que exporta dos funciones estándar:
- `init<Sección>()` — inicializa los event listeners de la sección.
- `load<Sección>()` — realiza la petición HTTP y renderiza los datos en el DOM.

Este patrón evita variables globales, encapsula la lógica de cada sección y hace el código mantenible y extensible.

**Router de un solo archivo (Single-file SPA con hash routing):** El archivo `main.js` actúa como controlador central que:
1. Verifica autenticación al cargar.
2. Inicializa todos los módulos de sección.
3. Maneja la navegación mediante `window.location.hash`, mostrando u ocultando secciones `<section>` dentro del único archivo `dashboard.html`.

Este enfoque evita recargas de página, simula una SPA real y mantiene el estado de navegación en la URL.

**Separación de responsabilidades por capas:**
- `api.js` → Capa de comunicación HTTP (transporte).
- `ui.js` → Capa de presentación (renderizado, modales, toasts).
- `auth.js` → Capa de autenticación y sesión.
- `<sección>.js` → Capa de lógica de negocio por dominio.

---

## 1.3 Responsabilidad de Cada Vista

El frontend tiene dos páginas HTML y seis secciones funcionales dentro del dashboard:

### Página: `index.html` — Login
Responsable de autenticar al usuario administrador. Presenta el formulario de inicio de sesión, valida credenciales contra el backend (`POST /api/auth/login`), almacena el JWT recibido en `sessionStorage` y redirige al dashboard. También incluye la funcionalidad de mostrar/ocultar contraseña y muestra mensajes de error de autenticación.

### Página: `dashboard.html` — Panel Principal
Página única que contiene todas las secciones del panel. Carga los módulos JS necesarios y delega el control al router para mostrar la sección activa.

### Sección: `estadisticas` — Dashboard / KPIs
Controlada por `estadisticas.js`. Consume el endpoint `GET /api/estadisticas` y presenta:
- Tarjetas KPI: total de consultas, consultas sin respuesta y usuarios únicos.
- Tabla de top preguntas más consultadas.
- Tabla de top usuarios con mayor actividad.
- Tabla de distribución de consultas por categoría.

### Sección: `categorias` — Gestión de Categorías
Controlada por `categorias.js`. Permite listar, crear, editar y eliminar (soft delete) las categorías que agrupan las preguntas frecuentes. Las operaciones de escritura requieren JWT. Muestra una tabla con opciones de acción por fila y usa el modal global para formularios.

### Sección: `preguntas` — Preguntas Frecuentes
Controlada por `preguntas.js`. Es la sección central del panel. Ofrece:
- Listado paginado (navegación Anterior/Siguiente) de preguntas.
- Filtro por categoría mediante `<select>`.
- Búsqueda en tiempo real en la tabla local.
- Creación, edición y eliminación de preguntas vía modal.
- Visualización de palabras clave y categoría de cada pregunta.

### Sección: `configuracion` — Configuración del Bot
Controlada por `configuracion.js`. Carga los parámetros de `GET /api/configuracion` y los presenta como formularios editables. Permite actualizar:
- `TELEGRAM_BOT_TOKEN`: Token del bot registrado en @BotFather.
- `TELEGRAM_CHAT_ID`: Chat ID del receptor de mensajes.
- `RESPUESTA_DEFAULT`: Mensaje enviado cuando no se encuentra respuesta.
- `BOT_ACTIVO`: Interruptor (`1`/`0`) para habilitar o deshabilitar el bot.

### Sección: `bot` — Gestión del Bot
Controlada por `bot.js`. Centraliza las operaciones de control del bot de Telegram:
- **Verificar Token**: Llama a `GET /api/bot/verificar` y muestra información del bot.
- **Registrar Webhook**: Envía una URL HTTPS a `POST /api/bot/registrar-webhook` para que Telegram envíe los mensajes al backend.
- **Ver Info Webhook**: Consulta `GET /api/bot/info-webhook` con los datos del webhook activo.
- **Eliminar Webhook**: Llama a `DELETE /api/bot/webhook` para volver al modo polling.
- **Prueba de Consulta Directa**: Permite al administrador probar el motor de búsqueda enviando un mensaje de prueba a `GET /api/bot/consulta`.

### Sección: `logs` — Logs de Consultas
Controlada por `logs.js`. Muestra el historial completo de interacciones del bot con usuarios de Telegram. Incluye:
- Filtros por rango de fechas (`fecha_desde`, `fecha_hasta`).
- Filtro por Telegram ID de usuario.
- Checkbox para mostrar solo consultas sin respuesta.
- Paginación del historial.
- Indicadores visuales (badges) de si se encontró o no respuesta.

---

## 1.4 Distribución de Carpetas

```
smartbot-frontend/
│
├── index.html              # Vista de login
├── dashboard.html          # Vista principal del panel (SPA)
│
├── css/
│   ├── variables.css       # Variables CSS globales: colores, tipografía, espaciados
│   ├── base.css            # Reset y estilos base (body, tipografía, utilidades)
│   ├── layout.css          # Estructura del dashboard: sidebar, topbar, main-content
│   ├── components.css      # Componentes reutilizables: botones, cards, modales, toasts, badges
│   └── pages.css           # Estilos específicos por sección: login, KPIs, tablas, filtros
│
├── js/
│   ├── api.js              # Capa HTTP: función request(), métodos get/post/put/delete
│   ├── auth.js             # Login, logout, gestión del JWT en sessionStorage
│   ├── ui.js               # Utilidades UI: renderTable, openModal, showToast, showLoader
│   ├── main.js             # Router, inicialización de módulos, control de sidebar
│   ├── estadisticas.js     # Módulo de KPIs y estadísticas
│   ├── categorias.js       # Módulo CRUD de categorías
│   ├── preguntas.js        # Módulo CRUD de preguntas con paginación y filtros
│   ├── configuracion.js    # Módulo de configuración del bot
│   ├── bot.js              # Módulo de gestión del bot de Telegram
│   └── logs.js             # Módulo de logs de consultas
│
├── Dockerfile              # Imagen Docker: nginx:1.25-alpine sirviendo los estáticos
└── nginx.conf              # Configuración de Nginx para SPA
```

---

## 1.5 Consumo de la API REST

El frontend consume la API REST del backend a través del módulo centralizado `js/api.js`, implementado con la **Fetch API nativa del navegador**.

### Arquitectura del cliente HTTP

```javascript
// Configuración base
const API_BASE = 'http://localhost:8000';
const TOKEN_KEY = 'smartbot_token';
```

El módulo expone un objeto `api` con cuatro métodos:

```javascript
const api = {
  get:    (path, auth = true) => request('GET',    path, null, auth),
  post:   (path, body, auth = true) => request('POST',   path, body, auth),
  put:    (path, body, auth = true) => request('PUT',    path, body, auth),
  delete: (path, auth = true) => request('DELETE', path, null, auth),
};
```

### Comportamiento de la función `request()`

1. **Construcción de headers:** Agrega `Content-Type: application/json` en todas las peticiones. Si `requiresAuth = true`, agrega el header `Authorization: Bearer <token>`.
2. **Manejo de 401/403:** Si el servidor responde con código no autorizado, limpia el token de `sessionStorage` y redirige al login automáticamente.
3. **Manejo de errores de red:** Si no hay conexión, lanza un objeto de error con `status: 0` y `detail: 'No se puede conectar con el servidor'`.
4. **Parsing de respuesta:** Parsea automáticamente el JSON de la respuesta y lanza el error con `detail` si el status HTTP no es exitoso.

### Almacenamiento del Token

El JWT se almacena en `sessionStorage` (no `localStorage`) bajo la clave `smartbot_token`. Esto garantiza que la sesión se cierre automáticamente al cerrar la pestaña del navegador, lo que es un comportamiento más seguro para un panel de administración.

### Ejemplo de consumo en un módulo

```javascript
// estadisticas.js
import api from './api.js';

export async function loadEstadisticas() {
  const data = await api.get('/api/estadisticas');
  renderKPIs(data);
  renderTopPreguntas(data.top_preguntas);
}
```

---

## 1.6 Paleta de Colores

El proyecto usa un tema oscuro definido mediante **CSS Custom Properties** en `css/variables.css`. Todos los componentes referencian estas variables, lo que permite cambiar el tema completo modificando un único archivo.

| Variable CSS | Valor HEX | Descripción |
|---|---|---|
| `--color-primary` | `#1A1A40` | Color de fondo principal (azul marino muy oscuro) |
| `--color-secondary` | `#4C0027` | Color secundario (burdeos oscuro), usado en acentos |
| `--color-accent` | `#1E5128` | Color de acento (verde oscuro), texto destacado y logo |
| `--color-dark` | `#082032` | Fondo más profundo para contraste |
| `--color-surface` | `#1f1f4a` | Superficie de cards, sidebar, modales |
| `--color-border` | `#2a2a5a` | Color de bordes de elementos |
| `--color-text-primary` | `#e8e8f0` | Texto principal (blanco ligeramente azulado) |
| `--color-text-secondary` | `#9999bb` | Texto secundario, etiquetas, subtítulos |
| `--color-danger` | `#7a0038` | Acciones destructivas, botones de eliminar, badges de error |
| `--color-success` | `#2a6e3a` | Confirmaciones, badges "Activo" o "Sí" |
| `--color-warning` | `#8a6a00` | Alertas y advertencias |

La paleta sigue un esquema **monocromático oscuro** basado en azul-violeta (`#1A1A40`) como color base, con acentos en verde (`#1E5128`) y burdeos (`#4C0027`) para jerarquía visual.

---

## 1.7 Gestión de Estado y Autenticación

El frontend no usa ninguna librería de gestión de estado (Redux, Zustand, etc.). El "estado" de la aplicación es mínimo:

- **Sesión:** El JWT almacenado en `sessionStorage` es el único estado persistente.
- **Sección activa:** Determinada por `window.location.hash`.
- **Datos en pantalla:** Se re-consultan desde la API cada vez que se navega a una sección, garantizando datos frescos sin necesidad de caché en cliente.

El flujo de autenticación es:

```
Usuario ingresa credenciales
        ↓
POST /api/auth/login
        ↓
Respuesta con access_token
        ↓
sessionStorage.setItem('smartbot_token', token)
        ↓
Redirección a dashboard.html
        ↓
Cada petición protegida → Authorization: Bearer <token>
        ↓
Al recibir 401/403 → clearToken() → redirección a index.html
```

---

## 1.8 Despliegue del Frontend

El frontend se sirve como archivos estáticos mediante **Nginx 1.25-alpine**. En producción Docker el contenedor escucha en el puerto `80` y se expone al host en el puerto `3000`.

```bash
# Levantar solo el frontend con Docker
docker compose up frontend

# URL de acceso
http://localhost:3000
```

---

---

# 2. Backend — SmartBot API

## 2.1 Tecnologías Usadas

| Tecnología | Versión | Descripción |
|---|---|---|
| Python | 3.11 | Lenguaje de programación del backend |
| FastAPI | 0.111.0 | Framework web asíncrono para construcción de APIs REST |
| Uvicorn | 0.29.0 | Servidor ASGI de alto rendimiento que ejecuta FastAPI |
| SQLAlchemy | 2.0.30 | ORM (Object Relational Mapper) para gestión de la base de datos |
| PyMySQL | 1.1.1 | Driver Python para conectar con MySQL |
| MySQL | 8.0 | Sistema gestor de base de datos relacional |
| Pydantic | 2.7.1 | Validación y serialización de datos (schemas/DTOs) |
| pydantic-settings | 2.2.1 | Gestión de configuración desde variables de entorno |
| python-jose | 3.3.0 | Generación y validación de tokens JWT (JSON Web Tokens) |
| bcrypt | 4.1.3 | Hashing seguro de contraseñas |
| httpx | 0.27.0 | Cliente HTTP asíncrono para comunicarse con la API de Telegram |
| python-dotenv | 1.0.1 | Carga de variables de entorno desde archivo `.env` |
| Docker | — | Containerización del backend y la base de datos |

---

## 2.2 Patrón de Diseño

El backend implementa el patrón **Router → Service → Repository (Capas)**, que es una variante del patrón **MVC (Model-View-Controller)** adaptada a APIs REST, donde:

- **Model** → `app/database/models.py` y `app/schemas/` (modelos ORM y Pydantic).
- **Controller/Router** → `app/routers/` (equivalente al Controller en MVC).
- **Service** → `app/services/` (lógica de negocio desacoplada del HTTP).

### Por qué se eligió este patrón

**1. Separación clara de responsabilidades:** Los routers solo reciben la petición HTTP y devuelven la respuesta. Toda la lógica de negocio vive en los servicios, haciendo que los routers sean delgados y fáciles de leer.

**2. Reutilización de servicios:** Un mismo servicio puede ser llamado desde múltiples routers o desde tareas en background (como el loop de polling de Telegram), sin duplicar código. Por ejemplo, `preguntas_service.buscar_respuesta()` es usado tanto por `routers/preguntas.py` como por `routers/bot.py` y el loop de polling en `main.py`.

**3. Testabilidad:** Los servicios no dependen de HTTP, pueden probarse de forma unitaria pasando una sesión de base de datos de prueba, sin necesidad de levantar el servidor HTTP.

**4. Escalabilidad:** Agregar un nuevo endpoint requiere únicamente: crear el router, agregar la función en el servicio correspondiente y registrar el router en `main.py`, sin tocar otras capas.

**5. Coherencia con FastAPI:** FastAPI promueve este patrón de forma nativa con su sistema de `Depends()` para inyección de dependencias (sesión de DB, usuario autenticado), lo que encaja naturalmente con la separación Router/Service.

### Flujo de una petición HTTP

```
Cliente HTTP (Frontend/Telegram)
        ↓
FastAPI Router (app/routers/<dominio>.py)
  - Valida el body con Pydantic (schema)
  - Resuelve dependencias (sesión DB, usuario JWT)
        ↓
Service Layer (app/services/<dominio>_service.py)
  - Ejecuta la lógica de negocio
  - Consulta/modifica la DB a través de SQLAlchemy
        ↓
Database (MySQL 8.0)
        ↓
Service devuelve modelo ORM
        ↓
Router serializa con Pydantic y retorna JSON
```

---

## 2.3 Detalle de Endpoints

> 🔒 = Requiere header `Authorization: Bearer <token>`  
> 🌐 = Endpoint público, no requiere autenticación

---

### Módulo: Autenticación `/api/auth`

---

#### `POST /api/auth/login` 🌐

**Responsabilidad:** Autentica al usuario administrador y retorna un JWT de acceso.

**Request Body:**
```json
{
  "username": "IA1-User",
  "password": "IA1-password@_new"
}
```

**Response Body (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response Body (401 Unauthorized):**
```json
{
  "detail": "Credenciales inválidas"
}
```

**Query Params / Path Params:** Ninguno.

---

#### `POST /api/auth/logout` 🔒

**Responsabilidad:** Invalida el token JWT actual agregándolo a una blacklist en memoria del servidor, impidiendo su uso futuro aunque no haya expirado.

**Request Body:** Ninguno (el token se extrae del header `Authorization`).

**Response Body (200 OK):**
```json
{
  "mensaje": "Sesión cerrada correctamente"
}
```

**Query Params / Path Params:** Ninguno.

---

### Módulo: Categorías `/api/categorias`

---

#### `GET /api/categorias` 🌐

**Responsabilidad:** Lista todas las categorías activas disponibles en el sistema. Endpoint público usado también por el panel de preguntas para cargar el selector de filtro.

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Información General",
    "descripcion": "Preguntas sobre el sistema y la empresa",
    "activo": 1,
    "created_at": "2026-06-11T10:00:00",
    "updated_at": null
  }
]
```

**Query Params / Path Params:** Ninguno.

---

#### `GET /api/categorias/{id}` 🌐

**Responsabilidad:** Obtiene el detalle de una categoría específica por su identificador.

**Request Body:** Ninguno.

**Path Param:** `id` (integer) — identificador de la categoría.

**Response Body (200 OK):** Objeto `CategoriaResponse` (mismo esquema que el elemento del array anterior).

**Response Body (404 Not Found):**
```json
{ "detail": "Categoría no encontrada" }
```

---

#### `POST /api/categorias` 🔒

**Responsabilidad:** Crea una nueva categoría en el sistema.

**Request Body:**
```json
{
  "nombre": "Recursos Humanos",
  "descripcion": "Preguntas sobre vacaciones, permisos y nómina"
}
```

**Response Body (201 Created):** Objeto `CategoriaResponse` con el ID asignado.

**Response Body (409 Conflict):**
```json
{ "detail": "Ya existe una categoría con el nombre 'Recursos Humanos'" }
```

**Query Params / Path Params:** Ninguno.

---

#### `PUT /api/categorias/{id}` 🔒

**Responsabilidad:** Actualiza los datos de una categoría existente. Soporta actualización parcial (solo los campos enviados se modifican).

**Path Param:** `id` (integer).

**Request Body (campos opcionales):**
```json
{
  "nombre": "Nuevo nombre",
  "descripcion": "Nueva descripción",
  "activo": 1
}
```

**Response Body (200 OK):** Objeto `CategoriaResponse` actualizado con `updated_at` con fecha.

---

#### `DELETE /api/categorias/{id}` 🔒

**Responsabilidad:** Elimina una categoría mediante soft delete (marca `activo = 0`). Si la categoría tiene preguntas activas asociadas, la operación es rechazada para preservar integridad referencial.

**Path Param:** `id` (integer).

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
{ "mensaje": "Categoría eliminada correctamente" }
```

**Response Body (409 Conflict):**
```json
{ "detail": "No se puede eliminar: la categoría tiene 7 pregunta(s) activa(s)" }
```

---

### Módulo: Preguntas `/api/preguntas`

---

#### `GET /api/preguntas/buscar` 🌐

**Responsabilidad:** Endpoint público de búsqueda semántica. Busca la respuesta más adecuada para un mensaje de texto dado, usando el mismo motor de búsqueda que utiliza el bot. Ideal para probar el comportamiento del bot sin pasar por Telegram.

**Query Param:** `q` (string, requerido, mínimo 1 carácter) — texto de la consulta.

**Request Body:** Ninguno.

**Response Body (200 OK — con resultado):**
```json
{
  "encontro_respuesta": true,
  "pregunta_id": 1,
  "pregunta": "¿Cuál es el horario de atención?",
  "respuesta": "Nuestro horario de atención es de lunes a viernes..."
}
```

**Response Body (200 OK — sin resultado):**
```json
{
  "encontro_respuesta": false,
  "pregunta_id": null,
  "pregunta": null,
  "respuesta": "Lo siento, no encontré una respuesta para tu consulta..."
}
```

---

#### `GET /api/preguntas` 🔒

**Responsabilidad:** Lista las preguntas frecuentes activas con soporte de paginación y filtro por categoría.

**Query Params:**

| Parámetro | Tipo | Defecto | Descripción |
|---|---|---|---|
| `skip` | int | 0 | Registros a saltar (offset para paginación) |
| `limit` | int | 20 | Cantidad máxima de registros (máx: 100) |
| `id_categoria` | int | — | Filtrar por ID de categoría (opcional) |

**Request Body:** Ninguno.

**Response Body (200 OK):** Array de objetos `PreguntaResponse`:
```json
[
  {
    "id": 1,
    "id_categoria": 1,
    "pregunta": "¿Cuál es el horario de atención?",
    "respuesta": "Nuestro horario de atención...",
    "palabras_clave": "horario, atencion, horas",
    "activo": 1,
    "created_at": "2026-06-11T10:00:00",
    "updated_at": null
  }
]
```

---

#### `GET /api/preguntas/{id}` 🔒

**Responsabilidad:** Obtiene el detalle completo de una pregunta por su ID, incluyendo respuesta y palabras clave.

**Path Param:** `id` (integer).

**Request Body:** Ninguno.

**Response Body (200 OK):** Objeto `PreguntaResponse`.

**Response Body (404):** `{ "detail": "Pregunta no encontrada" }`

---

#### `POST /api/preguntas` 🔒

**Responsabilidad:** Crea una nueva pregunta frecuente con su respuesta y palabras clave opcionales.

**Request Body:**
```json
{
  "pregunta": "¿Cuántos usuarios puede tener mi cuenta?",
  "respuesta": "Depende del plan contratado...",
  "id_categoria": 4,
  "palabras_clave": "usuarios, cuenta, cantidad, plan"
}
```

**Response Body (201 Created):** Objeto `PreguntaResponse` con el ID asignado.

**Response Body (422 Unprocessable Entity):** Error de validación si `pregunta` o `respuesta` están vacíos.

---

#### `PUT /api/preguntas/{id}` 🔒

**Responsabilidad:** Actualiza parcialmente una pregunta existente. Solo se modifican los campos incluidos en el body.

**Path Param:** `id` (integer).

**Request Body (campos opcionales):**
```json
{
  "respuesta": "Nueva respuesta actualizada.",
  "palabras_clave": "nuevas, palabras, clave",
  "activo": 1
}
```

**Response Body (200 OK):** Objeto `PreguntaResponse` con datos actualizados.

---

#### `DELETE /api/preguntas/{id}` 🔒

**Responsabilidad:** Elimina una pregunta mediante soft delete (establece `activo = 0`). La pregunta deja de aparecer en búsquedas y listados pero se conserva en la base de datos para auditoría.

**Path Param:** `id` (integer).

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
{ "mensaje": "Pregunta eliminada correctamente" }
```

---

### Módulo: Configuración del Bot `/api/configuracion`

---

#### `GET /api/configuracion` 🔒

**Responsabilidad:** Lista todas las claves de configuración del bot almacenadas en la tabla `configuracion_bot`. Las 4 claves del sistema son: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `RESPUESTA_DEFAULT` y `BOT_ACTIVO`.

**Request Body:** Ninguno.

**Query Params / Path Params:** Ninguno.

**Response Body (200 OK):**
```json
[
  {
    "id": 1,
    "clave": "TELEGRAM_BOT_TOKEN",
    "valor": "",
    "descripcion": "Token del bot de Telegram (obtenido desde @BotFather)",
    "updated_at": null
  },
  {
    "id": 4,
    "clave": "BOT_ACTIVO",
    "valor": "1",
    "descripcion": "Habilitar (1) o deshabilitar (0) el bot",
    "updated_at": null
  }
]
```

---

#### `PUT /api/configuracion/{clave}` 🔒

**Responsabilidad:** Actualiza el valor de un parámetro de configuración del bot identificado por su clave.

**Path Param:** `clave` (string) — nombre de la clave de configuración (ej: `TELEGRAM_BOT_TOKEN`).

**Request Body:**
```json
{
  "valor": "1234567890:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

**Response Body (200 OK):** Objeto `ConfiguracionResponse` con el valor actualizado y `updated_at` con fecha.

**Response Body (404):**
```json
{ "detail": "Clave de configuración 'CLAVE_INEXISTENTE' no encontrada" }
```

---

### Módulo: Bot / Webhook `/api/bot`

---

#### `POST /api/bot/webhook` 🌐

**Responsabilidad:** Endpoint receptor del webhook de Telegram. Telegram llama automáticamente a este endpoint con un objeto `Update` cada vez que un usuario envía un mensaje al bot. El sistema procesa el mensaje, busca la respuesta, registra la consulta en el log y envía la respuesta de vuelta al usuario vía Telegram Bot API.

**Request Body (objeto Update de Telegram):**
```json
{
  "update_id": 100000001,
  "message": {
    "message_id": 1,
    "from": {
      "id": 987654321,
      "first_name": "Juan",
      "username": "juanperez"
    },
    "chat": { "id": 987654321, "type": "private" },
    "text": "horario de atención"
  }
}
```

**Response Body (200 OK):**
```json
{
  "status": "ok",
  "respuesta_enviada": "Nuestro horario de atención es de lunes a viernes..."
}
```

**Query Params / Path Params:** Ninguno.

---

#### `GET /api/bot/consulta` 🌐

**Responsabilidad:** Endpoint de prueba para verificar el motor de búsqueda del bot sin necesidad de interactuar con Telegram. Útil para pruebas en desarrollo y desde el panel administrativo.

**Query Param:** `mensaje` (string, requerido) — texto a consultar.

**Request Body:** Ninguno.

**Response Body (200 OK):** Objeto `BusquedaResponse` (igual al de `GET /api/preguntas/buscar`).

---

#### `GET /api/bot/verificar` 🔒

**Responsabilidad:** Verifica la validez del `TELEGRAM_BOT_TOKEN` configurado llamando al método `getMe` de la Telegram Bot API. Retorna la información del bot si el token es válido.

**Request Body:** Ninguno.

**Query Params / Path Params:** Ninguno.

**Response Body (200 OK — token válido):**
```json
{
  "status": "ok",
  "bot": {
    "id": 1234567890,
    "is_bot": true,
    "first_name": "SmartBot",
    "username": "SmartBotGT_bot"
  }
}
```

**Response Body (200 OK — token inválido o no configurado):**
```json
{
  "status": "error",
  "detalle": "TELEGRAM_BOT_TOKEN no está configurado..."
}
```

---

#### `POST /api/bot/registrar-webhook` 🔒

**Responsabilidad:** Registra una URL HTTPS en Telegram para que el servicio envíe automáticamente los mensajes al backend mediante webhook. La URL debe apuntar al endpoint `POST /api/bot/webhook` del backend.

**Request Body:**
```json
{
  "url_webhook": "https://mi-servidor.com/api/bot/webhook"
}
```

**Response Body (200 OK):**
```json
{
  "status": "ok",
  "telegram_response": {
    "ok": true,
    "result": true,
    "description": "Webhook was set"
  }
}
```

---

#### `GET /api/bot/info-webhook` 🔒

**Responsabilidad:** Consulta el estado actual del webhook registrado en Telegram. Retorna la URL activa, conteo de actualizaciones pendientes y datos de posibles errores.

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
{
  "status": "ok",
  "webhook": {
    "url": "https://mi-servidor.com/api/bot/webhook",
    "pending_update_count": 0,
    "last_error_message": null
  }
}
```

---

#### `DELETE /api/bot/webhook` 🔒

**Responsabilidad:** Elimina el webhook registrado en Telegram. Útil para cambiar de modo webhook a modo polling (desarrollo local) o para cambiar la URL del webhook.

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
{
  "status": "ok",
  "telegram_response": { "ok": true, "result": true, "description": "Webhook was deleted" }
}
```

---

### Módulo: Logs `/api/logs`

---

#### `GET /api/logs/consultas` 🔒

**Responsabilidad:** Lista el historial de todas las consultas recibidas por el bot, con filtros opcionales para análisis y auditoría. Permite identificar patrones de uso y consultas sin respuesta para mejorar la base de conocimiento.

**Query Params:**

| Parámetro | Tipo | Defecto | Descripción |
|---|---|---|---|
| `fecha_desde` | datetime (ISO 8601) | — | Filtrar consultas desde esta fecha |
| `fecha_hasta` | datetime (ISO 8601) | — | Filtrar consultas hasta esta fecha |
| `telegram_id` | int | — | Filtrar por ID de usuario de Telegram |
| `solo_sin_respuesta` | bool | false | Solo consultas sin coincidencia |
| `skip` | int | 0 | Offset de paginación |
| `limit` | int | 50 | Máximo de registros (máx: 200) |

**Request Body:** Ninguno.

**Response Body (200 OK):**
```json
[
  {
    "id": 1,
    "id_usuario_telegram": 1,
    "id_pregunta": 1,
    "mensaje_recibido": "horario de atención",
    "respuesta_enviada": "Nuestro horario de atención...",
    "encontro_respuesta": 1,
    "fecha_consulta": "2026-06-11T14:00:00"
  }
]
```

---

### Módulo: Estadísticas `/api/estadisticas`

---

#### `GET /api/estadisticas` 🔒

**Responsabilidad:** Retorna un resumen consolidado del uso del bot: totales globales, las 10 preguntas más consultadas, los 10 usuarios más activos y la distribución de consultas por categoría. Alimenta el dashboard principal del panel administrativo.

**Request Body:** Ninguno.

**Query Params / Path Params:** Ninguno.

**Response Body (200 OK):**
```json
{
  "total_consultas": 150,
  "consultas_sin_respuesta": 12,
  "total_usuarios_unicos": 35,
  "top_preguntas": [
    { "id": 1, "pregunta": "¿Cuál es el horario de atención?", "total_consultas": 28 }
  ],
  "top_usuarios": [
    { "telegram_id": 987654321, "nombre": "Juan Pérez", "total_consultas": 15 }
  ],
  "distribucion_categorias": [
    { "categoria": "Información General", "total_preguntas": 7, "total_consultas": 65 }
  ]
}
```

---

### Endpoint de Salud

#### `GET /` 🌐

**Responsabilidad:** Health check del servicio. Verifica que el servidor esté en ejecución.

**Response Body (200 OK):**
```json
{ "status": "ok", "servicio": "SmartBot API v1.0.0" }
```

---

## 2.4 Distribución de Carpetas

```
smartbot-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Punto de entrada: FastAPI app, CORS, routers, lifespan (polling)
│   ├── config.py                   # Configuración desde variables de entorno (Settings class)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py           # Motor SQLAlchemy, SessionLocal, Base declarativa
│   │   └── models.py               # Modelos ORM: UsuarioAdmin, Categoria, Pregunta,
│   │                               #   ConfiguracionBot, UsuarioTelegram, ConsultaLog
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                 # LoginRequest, TokenResponse, TokenPayload
│   │   ├── categorias.py           # CategoriaCreate, CategoriaUpdate, CategoriaResponse
│   │   ├── preguntas.py            # PreguntaCreate, PreguntaUpdate, PreguntaResponse, BusquedaResponse
│   │   ├── configuracion.py        # ConfiguracionResponse, ConfiguracionUpdate
│   │   ├── consultas_log.py        # ConsultaLogResponse, ConsultaLogFiltros
│   │   └── estadisticas.py         # EstadisticasResponse, TopPregunta, TopUsuario, DistribucionCategoria
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                 # POST /api/auth/login, POST /api/auth/logout
│   │   ├── categorias.py           # CRUD /api/categorias
│   │   ├── preguntas.py            # CRUD /api/preguntas + GET /api/preguntas/buscar
│   │   ├── configuracion.py        # GET + PUT /api/configuracion
│   │   ├── bot.py                  # Webhook, consulta, verificar, registro/info/eliminar webhook
│   │   ├── logs.py                 # GET /api/logs/consultas
│   │   └── estadisticas.py         # GET /api/estadisticas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Verificación de credenciales, JWT, blacklist
│   │   ├── categorias_service.py   # Lógica CRUD de categorías
│   │   ├── preguntas_service.py    # Lógica CRUD + motor de búsqueda de respuestas
│   │   ├── configuracion_service.py# Lectura y actualización de configuración del bot
│   │   ├── bot_service.py          # Orquestación del flujo completo de procesamiento de mensajes
│   │   ├── telegram_service.py     # Cliente HTTP para Telegram Bot API (httpx)
│   │   ├── estadisticas_service.py # Consultas SQL para KPIs y estadísticas
│   │   └── log_service.py          # Registro e historial de consultas
│   │
│   └── middleware/
│       ├── __init__.py
│       └── auth_middleware.py       # Dependencia FastAPI para extracción y validación del JWT
│
├── scripts/
│   └── seed_data.py                # Datos iniciales: admin, 4 categorías, 25 preguntas, config
│
├── .env.example                    # Plantilla de variables de entorno
├── requirements.txt                # Dependencias Python con versiones fijas
└── Dockerfile                      # Imagen Python 3.11-slim + uvicorn
```

---

## 2.5 Modelos de Base de Datos

El sistema tiene **seis tablas** definidas con SQLAlchemy ORM:

| Tabla | Descripción |
|---|---|
| `usuarios_admin` | Usuarios administradores del panel web (username, password_hash) |
| `categorias` | Grupos que clasifican las preguntas frecuentes |
| `preguntas` | Base de conocimiento del bot: pregunta, respuesta, palabras clave |
| `configuracion_bot` | Parámetros del bot en formato clave-valor |
| `usuarios_telegram` | Registro de usuarios de Telegram que interactúan con el bot |
| `consultas_log` | Historial de cada mensaje recibido por el bot y la respuesta enviada |

Todas las tablas con datos modificables implementan **soft delete** (campo `activo`): los registros eliminados se marcan como inactivos pero se conservan en la base de datos para mantener integridad referencial y auditoría.

---

## 2.6 Lógica de Búsqueda de Respuestas (Equivalente Prolog)

> **Nota sobre Prolog:** La arquitectura del proyecto no incluye un motor Prolog externo. La lógica de inferencia y búsqueda de respuestas está implementada directamente en Python dentro de `app/services/preguntas_service.py`, siguiendo una filosofía equivalente a la programación lógica: reglas de coincidencia ordenadas por prioridad.

### Hechos y Reglas del Sistema

El motor de búsqueda trabaja sobre los siguientes **hechos** (datos en la base de datos):

- **Hecho:** `pregunta(ID, TextoPregunta, Respuesta, PalabrasClave, Activo)` — cada fila de la tabla `preguntas`.
- **Hecho:** `configuracion(RESPUESTA_DEFAULT, TextoRespuesta)` — respuesta cuando no hay coincidencia.
- **Hecho:** `bot_activo(Estado)` — si el bot está habilitado (`1`) o deshabilitado (`0`).

Las **reglas de inferencia** implementadas son:

**Regla 1 — Normalización del mensaje:**
```
normalizar(Mensaje, MensajeNormalizado) :-
    convertir_minusculas(Mensaje, Temp),
    eliminar_puntuacion(Temp, MensajeNormalizado).
```
En Python: la función `_normalizar(texto)` convierte a minúsculas y elimina signos de puntuación con regex.

**Regla 2 — Búsqueda por coincidencia en campo pregunta (alta prioridad):**
```
buscar_respuesta(Mensaje, Respuesta) :-
    normalizar(Mensaje, MensajeNorm),
    pregunta(_, TextoPregunta, Respuesta, _, 1),
    contiene(TextoPregunta, MensajeNorm).
```
En Python: `Pregunta.pregunta.ilike(f"%{normalizado}%")` — LIKE case-insensitive sobre el texto completo de la pregunta.

**Regla 3 — Búsqueda por palabras clave (prioridad secundaria):**
```
buscar_respuesta(Mensaje, Respuesta) :-
    normalizar(Mensaje, MensajeNorm),
    palabras(MensajeNorm, Palabras),
    member(Palabra, Palabras),
    longitud(Palabra) > 2,
    pregunta(_, _, Respuesta, PalabrasClave, 1),
    contiene(PalabrasClave, Palabra).
```
En Python: para cada palabra del mensaje (con más de 2 caracteres), busca coincidencia en el campo `palabras_clave` con `ilike`.

**Regla 4 — Respuesta por defecto (cuando no hay coincidencia):**
```
buscar_respuesta(Mensaje, RespuestaDefault) :-
    \+ buscar_respuesta(Mensaje, _),
    configuracion('RESPUESTA_DEFAULT', RespuestaDefault).
```
En Python: si `buscar_respuesta()` retorna `None`, se obtiene la `RESPUESTA_DEFAULT` de la tabla `configuracion_bot`.

**Regla 5 — Bot desactivado:**
```
procesar(_, 'Bot desactivado') :-
    bot_activo('0').
```
En Python: `bot_service._bot_activo(db)` verifica `BOT_ACTIVO == "1"` antes de procesar cualquier mensaje.

### Flujo de Inferencia Completo

```
Mensaje recibido
        ↓
¿BOT_ACTIVO == "1"?  → NO → retornar "Bot desactivado"
        ↓ SÍ
Normalizar mensaje (minúsculas, sin puntuación)
        ↓
¿Coincide con campo `pregunta` (LIKE)? → SÍ → devolver respuesta
        ↓ NO
¿Alguna palabra del mensaje coincide con `palabras_clave`? → SÍ → devolver respuesta
        ↓ NO
Devolver RESPUESTA_DEFAULT de configuracion_bot
```

### Responsabilidades del Motor Lógico (Python como Prolog)

- **Inferencia basada en hechos:** Consulta los hechos almacenados en MySQL (preguntas y configuración) para inferir la respuesta correcta.
- **Reglas ordenadas por prioridad:** Las reglas se aplican en orden: primero coincidencia exacta en pregunta, luego coincidencia por palabras clave. La primera regla que se satisface detiene la búsqueda (como el corte `!` en Prolog).
- **Manejo de la negación:** Si ninguna regla positiva se satisface, se aplica la regla de fallo que devuelve la respuesta por defecto.
- **Generalización:** Las palabras clave actúan como sinónimos o variaciones que amplían la cobertura del sistema sin requerir coincidencia exacta.

---

## 2.7 Responsabilidades de Python

Python es el lenguaje que orquesta todos los componentes del backend. Sus responsabilidades se distribuyen así:

**`main.py` — Arranque y ciclo de vida:**
- Inicializa la aplicación FastAPI con su título, versión y middleware CORS.
- Crea las tablas de la base de datos al arrancar (si no existen) con `Base.metadata.create_all()`.
- Gestiona el **loop de long-polling de Telegram** como tarea asíncrona en background (`asyncio.create_task`), permitiendo recibir mensajes en entornos locales sin necesidad de URL pública para webhook.

**`config.py` — Configuración:**
- Lee variables de entorno (`DB_HOST`, `DB_USER`, `SECRET_KEY`, etc.) usando `python-dotenv`.
- Construye dinámicamente la URL de conexión a MySQL.

**`database/` — Persistencia:**
- Define el motor SQLAlchemy y la sesión de base de datos.
- Mapea las tablas de MySQL a clases Python mediante ORM declarativo.
- Gestiona las relaciones entre entidades (categorías → preguntas → consultas_log).

**`schemas/` — Contratos de API:**
- Valida automáticamente los datos de entrada (request body) con Pydantic.
- Define la estructura exacta de las respuestas JSON.
- Transforma los modelos ORM en objetos serializables.

**`routers/` — Capa HTTP:**
- Declara las rutas y métodos HTTP de cada endpoint.
- Inyecta dependencias: sesión de DB (`get_db`), usuario autenticado (`get_current_user`).
- Delega la lógica al servicio correspondiente.

**`services/` — Lógica de negocio:**
- `auth_service.py`: Verifica credenciales con bcrypt, genera y valida JWTs, gestiona blacklist de tokens para logout.
- `preguntas_service.py`: Motor de búsqueda de respuestas (normalización + LIKE + palabras clave).
- `bot_service.py`: Orquesta el flujo completo: recibir update → registrar usuario → buscar respuesta → registrar log → enviar respuesta a Telegram.
- `telegram_service.py`: Encapsula todas las llamadas HTTP a la Telegram Bot API (getMe, sendMessage, setWebhook, getWebhookInfo, deleteWebhook, getUpdates).
- `estadisticas_service.py`: Ejecuta consultas SQL agregadas para KPIs y distribuciones.
- `configuracion_service.py`: Lee y actualiza parámetros del bot desde la base de datos.
- `log_service.py`: Persiste cada interacción del bot en `consultas_log`.

**`middleware/` — Seguridad:**
- Extrae el JWT del header `Authorization: Bearer`.
- Valida firma, expiración y blacklist del token en cada petición protegida.

---

## 2.8 Pasos para Iniciar la Aplicación Backend

### Opción A: Docker Compose (Recomendado)

Este método levanta automáticamente el backend, la base de datos MySQL y el frontend.

**Requisitos previos:**
- Docker Desktop instalado y en ejecución.
- Git instalado.

**Paso 1 — Clonar el repositorio:**
```bash
git clone <URL_DEL_REPOSITORIO>
cd practica_smart_bot
```

**Paso 2 — Crear el archivo de variables de entorno:**
```bash
cp smartbot-backend/.env.example smartbot-backend/.env
```

Los valores por defecto del `.env.example` funcionan sin modificaciones con Docker Compose.

**Paso 3 — Construir y levantar todos los servicios:**
```bash
docker compose up --build
```

Este comando:
- Construye la imagen del backend (`Python 3.11-slim + uvicorn`).
- Construye la imagen del frontend (`nginx:1.25-alpine`).
- Levanta MySQL 8.0 con healthcheck.
- El backend espera a que MySQL esté listo antes de iniciar.

**Paso 4 — Insertar datos iniciales (primera vez):**

En una segunda terminal, ejecutar:
```bash
docker exec smartbot_backend python -m scripts.seed_data
```

Esto crea:
- Usuario administrador: `IA1-User` / `IA1-password@_new`
- 4 categorías de preguntas
- 25 preguntas frecuentes distribuidas
- Configuración base del bot (`TELEGRAM_BOT_TOKEN`, `RESPUESTA_DEFAULT`, etc.)

**Paso 5 — Verificar que los servicios están corriendo:**
```bash
curl http://localhost:8000/
# Respuesta esperada: {"status": "ok", "servicio": "SmartBot API v1.0.0"}
```

**URLs de acceso:**
| Servicio | URL |
|---|---|
| API Backend | `http://localhost:8000` |
| Documentación Swagger | `http://localhost:8000/docs` |
| Documentación ReDoc | `http://localhost:8000/redoc` |
| Frontend Admin | `http://localhost:3000` |
| MySQL | `localhost:3307` |

**Credenciales de acceso al panel:**
- **Usuario:** `IA1-User`
- **Contraseña:** `IA1-password@_new`

---

### Opción B: Ejecución Local sin Docker

**Requisitos previos:**
- Python 3.11+
- MySQL 8.0 corriendo localmente
- pip

**Paso 1 — Entrar al directorio del backend:**
```bash
cd practica_smart_bot/smartbot-backend
```

**Paso 2 — Crear entorno virtual e instalar dependencias:**
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

**Paso 3 — Configurar variables de entorno:**
```bash
cp .env.example .env
```

Editar `.env` con las credenciales de tu MySQL local:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=smartbot_user
DB_PASSWORD=smartbot_pass
DB_NAME=proyecto_ia
SECRET_KEY=cambia_esta_clave_secreta_en_produccion
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Paso 4 — Crear la base de datos en MySQL:**
```sql
CREATE DATABASE proyecto_ia;
CREATE USER 'smartbot_user'@'localhost' IDENTIFIED BY 'smartbot_pass';
GRANT ALL PRIVILEGES ON proyecto_ia.* TO 'smartbot_user'@'localhost';
FLUSH PRIVILEGES;
```

**Paso 5 — Insertar datos iniciales:**
```bash
python -m scripts.seed_data
```

**Paso 6 — Iniciar el servidor:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El flag `--reload` activa la recarga automática al detectar cambios en el código (útil en desarrollo).

---

### Comandos Útiles de Docker

| Comando | Descripción |
|---|---|
| `docker compose up --build` | Construye imágenes y levanta todos los servicios |
| `docker compose up -d` | Levanta en segundo plano (detached) |
| `docker compose down` | Detiene y elimina los contenedores |
| `docker compose down -v` | Detiene contenedores **y elimina los volúmenes** (borra la DB) |
| `docker compose logs -f backend` | Ver logs en tiempo real del backend |
| `docker compose logs -f db` | Ver logs de MySQL |
| `docker compose ps` | Ver estado de los contenedores |
| `docker exec smartbot_backend python -m scripts.seed_data` | Correr el seed de datos iniciales |
| `docker exec -it smartbot_db mysql -usmartbot_user -psmartbot_pass proyecto_ia` | Acceder a la consola MySQL |

---

### Configuración del Bot de Telegram

Después de levantar el backend, configurar el token del bot de Telegram:

1. Acceder al panel en `http://localhost:3000`.
2. Iniciar sesión con `IA1-User` / `IA1-password@_new`.
3. Navegar a **Configuración del Bot**.
4. Ingresar el `TELEGRAM_BOT_TOKEN` obtenido desde [@BotFather](https://t.me/BotFather).
5. Si el backend está en un servidor público, registrar el webhook desde la sección **Gestión del Bot** ingresando la URL `https://tu-servidor.com/api/bot/webhook`.
6. Si se trabaja en local, el bot usa **long-polling automático** — no es necesario configurar el webhook.

---

*Manual técnico generado para SmartBot Admin v1.0.0 — Junio 2026*
