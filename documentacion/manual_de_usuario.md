# Manual de Usuario — SmartBot Admin

> **Versión:** 1.0.0  
> **Fecha:** Junio 2026  
> **Aplicación:** Panel de Administración del Bot de Telegram SmartBot

---

## Tabla de Contenido

1. [Introducción](#1-introducción)
2. [Requisitos para Usar la Aplicación](#2-requisitos-para-usar-la-aplicación)
3. [Acceso al Sistema — Inicio de Sesión](#3-acceso-al-sistema--inicio-de-sesión)
4. [Estructura General del Panel](#4-estructura-general-del-panel)
5. [Sección: Dashboard — Estadísticas](#5-sección-dashboard--estadísticas)
6. [Sección: Categorías](#6-sección-categorías)
7. [Sección: Preguntas Frecuentes](#7-sección-preguntas-frecuentes)
8. [Sección: Configuración del Bot](#8-sección-configuración-del-bot)
9. [Sección: Gestión del Bot](#9-sección-gestión-del-bot)
10. [Sección: Logs de Consultas](#10-sección-logs-de-consultas)
11. [Referencia de Botones](#11-referencia-de-botones)
12. [Indicadores Visuales: Badges](#12-indicadores-visuales-badges)
13. [Notificaciones del Sistema: Toasts](#13-notificaciones-del-sistema-toasts)
14. [Preguntas Frecuentes del Usuario](#14-preguntas-frecuentes-del-usuario)

---

## 1. Introducción

**SmartBot Admin** es el panel de administración web que permite gestionar de forma completa el bot de respuestas automáticas de Telegram. Desde este panel el administrador puede:

- Consultar estadísticas de uso del bot en tiempo real.
- Administrar las categorías y preguntas frecuentes que el bot usa para responder.
- Configurar el token del bot y su comportamiento.
- Controlar el webhook de Telegram.
- Probar el motor de búsqueda del bot sin necesidad de abrir Telegram.
- Revisar el historial de todas las conversaciones del bot con usuarios.

La aplicación corre en el navegador web y no requiere instalación adicional.

---

## 2. Requisitos para Usar la Aplicación

- Navegador web moderno: **Google Chrome**, Mozilla Firefox, Microsoft Edge o Safari (versiones recientes).
- Conexión a internet o acceso a la red local donde está desplegado el sistema.
- Credenciales de acceso al panel (usuario y contraseña proporcionados por el administrador del sistema).

> **URL de acceso por defecto:** `http://localhost:3000`

---

## 3. Acceso al Sistema — Inicio de Sesión

### Cómo iniciar sesión

1. Abrir el navegador e ingresar la URL del sistema.
2. Se mostrará la pantalla de inicio de sesión con el logo de **SmartBot Admin**.
3. Ingresar el **Usuario** y la **Contraseña** en los campos correspondientes.
4. Hacer clic en el botón **Iniciar Sesión**.
5. Si las credenciales son correctas, el sistema redirige automáticamente al panel principal (Dashboard).

**Credenciales por defecto (entorno de prueba):**
- Usuario: `IA1-User`
- Contraseña: `IA1-password@_new`

### Mostrar/ocultar contraseña

En el campo de contraseña hay un botón con el ícono 👁. Al hacer clic en él, la contraseña se muestra en texto legible. Al hacer clic nuevamente, vuelve a ocultarse (cambia a 🙈).

### Mensajes de error en el login

Si el usuario o contraseña son incorrectos, aparece un mensaje de error en rojo debajo del título del formulario indicando **"Credenciales inválidas"**. En este caso verificar que no haya errores tipográficos y volver a intentarlo.

### Cómo cerrar sesión

En la barra lateral izquierda (sidebar), al fondo, se encuentra el botón **Cerrar Sesión**. Al hacer clic, el sistema invalida la sesión actual y redirige a la pantalla de login. La sesión también se cierra automáticamente al cerrar la pestaña del navegador.

---

## 4. Estructura General del Panel

Una vez iniciada la sesión, el panel muestra la siguiente estructura:

```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR (izquierda)    │  CONTENIDO PRINCIPAL           │
│  ─────────────────────  │  ─────────────────────────     │
│  SmartBot Admin         │  [Barra superior con título]   │
│                         │                                 │
│  📊 Dashboard           │  [Sección activa renderizada]  │
│  🗂 Categorías          │                                 │
│  ❓ Preguntas           │                                 │
│  ⚙️ Configuración Bot   │                                 │
│  🤖 Gestión Bot         │                                 │
│  📋 Logs                │                                 │
│                         │                                 │
│  [Cerrar Sesión]        │                                 │
└─────────────────────────────────────────────────────────┘
```

### Sidebar (Menú lateral)

El sidebar es el menú de navegación principal. Cada ítem del menú lleva a una sección diferente del panel. La sección activa se resalta con un color diferente.

### Barra Superior (Topbar)

Muestra el nombre de la sección activa. En dispositivos móviles o pantallas pequeñas, el botón ☰ (menú hamburguesa) ubicado en la esquina superior izquierda abre o cierra el sidebar.

### Navegación entre secciones

Hacer clic en cualquier ítem del sidebar carga la sección correspondiente. La URL del navegador se actualiza con un hash (ej: `#categorias`) para que la navegación con el botón "Atrás" del navegador funcione correctamente.

---

## 5. Sección: Dashboard — Estadísticas

**Acceso:** Hacer clic en **📊 Dashboard** en el sidebar.

Esta sección muestra un resumen del uso del bot en tiempo real. Es la primera sección que se ve al ingresar al panel.

### Tarjetas KPI (Indicadores clave)

Al cargar la sección aparecen cuatro tarjetas con métricas generales:

| Tarjeta | Qué muestra |
|---|---|
| **Total Consultas** | Número total de mensajes recibidos por el bot desde que está en funcionamiento |
| **Sin Respuesta** | Cantidad de mensajes para los cuales el bot no encontró una respuesta en su base de conocimiento |
| **Usuarios Únicos** | Número total de usuarios de Telegram distintos que han interactuado con el bot |
| **% Resolución** | Porcentaje de consultas que sí fueron respondidas exitosamente |

### Tabla: Top Preguntas

Muestra las 10 preguntas más consultadas por los usuarios del bot, ordenadas de mayor a menor número de consultas. Permite identificar qué temas generan más dudas.

### Tabla: Top Usuarios

Muestra los 10 usuarios de Telegram que más veces han interactuado con el bot, con su nombre y Telegram ID.

### Tabla: Distribución por Categoría

Muestra cuántas preguntas hay registradas en cada categoría y cuántas veces se han consultado esas preguntas, lo que permite identificar qué categorías tienen más actividad.

### Botón: ↻ Actualizar

Ubicado en la parte superior derecha de la sección. Al hacer clic recarga todos los datos del dashboard consultando la información más reciente al servidor.

---

## 6. Sección: Categorías

**Acceso:** Hacer clic en **🗂 Categorías** en el sidebar.

Las categorías son grupos temáticos que organizan las preguntas frecuentes. Cada pregunta pertenece a una categoría.

### Ver categorías

Al ingresar a la sección se carga automáticamente la tabla de categorías con las columnas:

| Columna | Descripción |
|---|---|
| **ID** | Identificador numérico único de la categoría |
| **Nombre** | Nombre de la categoría |
| **Descripción** | Texto breve que describe de qué trata la categoría |
| **Estado** | Badge verde **Activo** o rojo **Inactivo** |
| **Creado** | Fecha y hora en que se creó la categoría |
| **Acciones** | Botones de editar ✏️ y eliminar 🗑 |

### Crear una nueva categoría

1. Hacer clic en el botón **+ Nueva Categoría** (esquina superior derecha de la sección).
2. Se abre un modal con el formulario de creación.
3. Completar los campos:
   - **Nombre** *(requerido)*: Nombre único de la categoría (ej: "Recursos Humanos").
   - **Descripción** *(opcional)*: Texto que explica el propósito de la categoría.
4. Hacer clic en **Guardar**.
5. Si el nombre ya existe, aparece un mensaje de error indicándolo. En ese caso cambiar el nombre e intentar de nuevo.
6. Si se crea exitosamente, aparece una notificación verde "Categoría creada" y la tabla se actualiza.

### Editar una categoría

1. En la tabla, hacer clic en el botón ✏️ (lápiz) de la fila que se desea editar.
2. Se abre el modal con los datos actuales de la categoría precargados.
3. Modificar los campos deseados (Nombre y/o Descripción).
4. Hacer clic en **Guardar**.
5. Al guardarse correctamente aparece la notificación "Categoría actualizada" y la tabla se actualiza.

### Eliminar una categoría

1. En la tabla, hacer clic en el botón 🗑 (basurero) de la fila que se desea eliminar.
2. Aparece un modal de confirmación con el mensaje "¿Eliminar la categoría [nombre]? Esta acción no se puede deshacer."
3. Hacer clic en el botón rojo **Eliminar** para confirmar, o en **Cancelar** para cancelar la operación.
4. **Importante:** No es posible eliminar una categoría que tenga preguntas activas asociadas. En ese caso aparece un mensaje de error indicando cuántas preguntas activas tiene. Se deben eliminar primero las preguntas de esa categoría.

### Botones del modal de categoría

| Botón | Función |
|---|---|
| **Guardar** | Guarda los cambios (crea o actualiza la categoría) |
| **Cancelar** | Cierra el modal sin guardar ningún cambio |
| **×** (esquina superior) | Cierra el modal sin guardar ningún cambio |

---

## 7. Sección: Preguntas Frecuentes

**Acceso:** Hacer clic en **❓ Preguntas** en el sidebar.

Esta es la sección más importante del panel. Aquí se gestiona la **base de conocimiento del bot**: el conjunto de preguntas y respuestas que el bot utiliza para responder a los usuarios de Telegram.

### Ver preguntas

La tabla muestra 15 preguntas por página con las columnas:

| Columna | Descripción |
|---|---|
| **ID** | Identificador numérico |
| **Categoría** | Categoría a la que pertenece la pregunta |
| **Pregunta** | Texto de la pregunta (truncado a 60 caracteres; el texto completo se ve al editar) |
| **Palabras clave** | Palabras clave asociadas (truncado a 40 caracteres) |
| **Estado** | Badge **Activo** o **Inactivo** |
| **Acciones** | Botones de editar ✏️ y eliminar 🗑 |

### Filtrar por categoría

En la barra de filtros sobre la tabla, el selector **"Filtrar por categoría"** permite mostrar únicamente las preguntas que pertenecen a una categoría específica. Seleccionar una categoría del desplegable actualiza la tabla automáticamente. Seleccionar "Todas las categorías" vuelve a mostrar todas.

### Búsqueda rápida en la tabla

El campo **"Búsqueda rápida"** filtra los resultados visibles en la tabla de forma instantánea mientras se escribe. Busca en el texto de la pregunta, las palabras clave y el nombre de la categoría. Esta búsqueda aplica sobre los resultados ya cargados en pantalla.

### Paginación

Debajo de la tabla hay controles de paginación:
- **Anterior**: Carga la página anterior (deshabilitado si se está en la primera página).
- **Siguiente**: Carga la siguiente página (deshabilitado si no hay más resultados).
- El texto al centro indica el rango de registros que se están mostrando (ej: "Mostrando 1–15").

### Crear una nueva pregunta

1. Hacer clic en el botón **+ Nueva Pregunta** (esquina superior derecha).
2. Se abre el modal con el formulario:
   - **Categoría** *(requerido)*: Seleccionar del desplegable la categoría a la que pertenece.
   - **Pregunta** *(requerido)*: Escribir el texto completo de la pregunta (ej: "¿Cuál es el horario de atención?").
   - **Respuesta** *(requerido)*: Escribir la respuesta que el bot enviará cuando detecte esta pregunta.
   - **Palabras clave** *(opcional)*: Lista de palabras separadas por coma que el bot también usa para identificar esta pregunta (ej: "horario, atencion, horas, apertura"). Las palabras clave amplían la capacidad de detección del bot.
3. Hacer clic en **Guardar**.
4. Al crearse exitosamente aparece la notificación "Pregunta creada" y la tabla se actualiza.

> **Consejo:** Las palabras clave son muy importantes para el funcionamiento del bot. Si un usuario escribe "horas" o "apertura" en lugar de "horario de atención", el bot igualmente encontrará la respuesta gracias a las palabras clave. Se recomienda incluir sinónimos y variantes del término principal.

### Editar una pregunta

1. En la tabla, hacer clic en el botón ✏️ de la fila que se desea modificar.
2. El modal se abre con todos los datos actuales precargados.
3. Modificar los campos necesarios (categoría, pregunta, respuesta y/o palabras clave).
4. Hacer clic en **Guardar**.
5. Al guardarse correctamente aparece la notificación "Pregunta actualizada".

### Eliminar una pregunta

1. Hacer clic en el botón 🗑 de la fila que se desea eliminar.
2. Aparece un modal de confirmación: "¿Eliminar esta pregunta? Esta acción no se puede deshacer."
3. Hacer clic en **Eliminar** para confirmar.
4. La pregunta se elimina (queda marcada como inactiva) y desaparece de la tabla y del motor de búsqueda del bot.

---

## 8. Sección: Configuración del Bot

**Acceso:** Hacer clic en **⚙️ Configuración Bot** en el sidebar.

Esta sección permite configurar los parámetros esenciales del bot de Telegram. Cada parámetro se muestra en una tarjeta independiente con su descripción y un botón para guardar.

### Parámetro: Token del Bot de Telegram

El **token** es el identificador secreto que conecta el backend con el bot de Telegram. Se obtiene desde [@BotFather](https://t.me/BotFather) en Telegram.

**Cómo configurarlo:**
1. Pegar el token en el campo de texto (el campo es de tipo contraseña para proteger el valor).
2. Para ver el valor ingresado, hacer clic en el ícono 👁 al final del campo.
3. Hacer clic en **Guardar**.

> **Importante:** Sin este token el bot no puede conectarse a Telegram ni enviar ni recibir mensajes.

### Parámetro: Chat ID de Telegram

Identificador numérico del chat o grupo de Telegram donde el bot puede enviar mensajes por iniciativa propia. Se usa principalmente en integraciones avanzadas.

**Cómo configurarlo:**
1. Ingresar el ID numérico del chat en el campo de texto.
2. Hacer clic en **Guardar**.

### Parámetro: Respuesta por Defecto

Es el mensaje que el bot envía cuando un usuario le escribe algo para lo cual no existe una pregunta ni palabras clave coincidentes en la base de conocimiento.

**Cómo configurarlo:**
1. El campo es un área de texto multilínea.
2. Editar el mensaje deseado (ej: "Lo siento, no encontré una respuesta. Por favor escríbenos a soporte@empresa.com").
3. Hacer clic en **Guardar**.

> **Recomendación:** Incluir en este mensaje una forma de contacto alternativa (correo, teléfono, horario de atención) para que el usuario no quede sin información.

### Parámetro: Bot Activo

Un interruptor (toggle) que habilita o deshabilita el bot completamente.

- **Encendido (verde):** El bot procesa y responde todos los mensajes que recibe.
- **Apagado (gris):** El bot ignora todos los mensajes entrantes. Útil para mantenimiento o cuando se necesita pausar el servicio sin apagarlo.

**Cómo cambiarlo:**
1. Hacer clic en el toggle para cambiar el estado.
2. Hacer clic en **Guardar** para aplicar el cambio.

### Botón: Guardar (por parámetro)

Cada tarjeta de configuración tiene su propio botón **Guardar** verde. Los cambios de cada parámetro se guardan de forma independiente: cambiar el token y hacer clic en Guardar solo actualiza el token, sin afectar los demás parámetros.

---

## 9. Sección: Gestión del Bot

**Acceso:** Hacer clic en **🤖 Gestión Bot** en el sidebar.

Esta sección centraliza las herramientas de control operativo del bot de Telegram: verificar que esté correctamente configurado, gestionar el webhook y probar su motor de búsqueda.

---

### Subsección: Estado del Bot

#### Botón: Verificar Token

**Función:** Comprueba si el token de Telegram configurado es válido consultando directamente a los servidores de Telegram.

**Cómo usarlo:**
1. Hacer clic en **Verificar Token**.
2. El resultado aparece debajo del botón:
   - ✅ **Token válido:** Muestra el nombre y username del bot (ej: "SmartBot @SmartBotGT_bot") con un badge verde.
   - ❌ **Error:** Muestra el mensaje de error con un badge rojo. En este caso revisar que el token esté correctamente configurado en la sección Configuración del Bot.

---

### Subsección: Webhook

El **webhook** es la URL que se registra en Telegram para que el servicio envíe automáticamente los mensajes al backend cada vez que un usuario escriba al bot. Es necesario cuando el servidor backend está en una URL pública accesible desde internet.

> **Nota:** Si se trabaja en un entorno local (localhost), el webhook no es necesario porque el sistema usa **long-polling automático** en segundo plano.

#### Campo: URL del Webhook

Campo de texto donde se ingresa la URL pública HTTPS del backend. Debe terminar en `/api/bot/webhook`.

Ejemplo: `https://mi-servidor.com/api/bot/webhook`

#### Botón: Registrar Webhook

**Función:** Envía la URL ingresada en el campo a Telegram para que empiece a reenviar los mensajes al backend.

**Cómo usarlo:**
1. Ingresar la URL HTTPS del backend en el campo "URL del Webhook".
2. Hacer clic en **Registrar Webhook**.
3. Si el registro es exitoso, aparece una notificación verde y el panel muestra la URL registrada.
4. Si hay un error (URL inválida, token incorrecto), aparece una notificación de error.

> **Requisito:** La URL debe ser HTTPS (no funciona con HTTP). En desarrollo local se puede usar una herramienta como ngrok para obtener una URL pública temporal.

#### Botón: Ver Info

**Función:** Consulta el estado actual del webhook registrado en Telegram y muestra la información en una tabla.

**Información que muestra:**
- **URL:** La URL del webhook actualmente registrada.
- **Updates pendientes:** Mensajes que Telegram aún no ha podido enviar al backend.
- **Último error:** Mensaje del último error que ocurrió al intentar enviar un update (útil para depuración).
- **IP:** Dirección IP del servidor donde apunta el webhook.

**Cómo usarlo:**
1. Hacer clic en **Ver Info**.
2. La tabla con la información aparece debajo de los botones.

#### Botón: Eliminar Webhook

**Función:** Elimina el webhook registrado en Telegram. Después de esto el bot deja de recibir mensajes vía webhook y el sistema puede volver al modo polling automático.

**Cuándo usarlo:**
- Cuando se cambia la URL del servidor y es necesario registrar un nuevo webhook.
- Cuando se quiere volver al modo de desarrollo local (polling).

**Cómo usarlo:**
1. Hacer clic en **Eliminar Webhook**.
2. Aparece un modal de confirmación: "¿Eliminar el webhook registrado en Telegram? El bot dejará de recibir mensajes automáticamente."
3. Hacer clic en el botón rojo **Eliminar** para confirmar.
4. Al eliminarse correctamente aparece la notificación "Webhook eliminado".

---

### Subsección: Prueba de Consulta Directa

Permite probar el motor de búsqueda del bot directamente desde el panel, sin necesidad de abrir Telegram ni enviar mensajes reales.

#### Campo: Escribe un mensaje de prueba

Campo de texto donde se ingresa el mensaje que se desea probar. Simula exactamente lo que un usuario escribiría al bot en Telegram.

#### Botón: Consultar

**Función:** Envía el texto ingresado al motor de búsqueda del bot y muestra la respuesta que el bot devolvería.

**Cómo usarlo:**
1. Escribir el mensaje de prueba en el campo (ej: "horario de atención").
2. Hacer clic en **Consultar** o presionar la tecla **Enter**.
3. El resultado aparece debajo del botón:
   - ✅ **Respuesta encontrada (badge verde):** Muestra la pregunta que coincidió y la respuesta que el bot enviaría.
   - ❌ **Sin coincidencia (badge rojo):** Muestra la respuesta por defecto configurada. Indica que no hay ninguna pregunta registrada que coincida con ese texto.

**Casos de uso:**
- Verificar que una nueva pregunta recién creada funciona correctamente antes de que llegue un usuario real.
- Probar diferentes formas de escribir una consulta para evaluar si el bot las detecta.
- Confirmar que la respuesta por defecto está correctamente configurada.

---

## 10. Sección: Logs de Consultas

**Acceso:** Hacer clic en **📋 Logs** en el sidebar.

Esta sección muestra el historial completo de interacciones del bot con los usuarios de Telegram. Cada fila en la tabla representa un mensaje que el bot recibió y procesó.

### Tabla de Logs

Las columnas de la tabla son:

| Columna | Descripción |
|---|---|
| **ID** | Número identificador del registro |
| **Usuario TG** | ID interno del usuario de Telegram que envió el mensaje |
| **Mensaje Recibido** | Texto que el usuario escribió al bot (truncado; el mensaje completo se ve en la base de datos) |
| **Respuesta Enviada** | Respuesta que el bot envió de vuelta (truncada) |
| **¿Encontró?** | Badge **Sí** (verde) si el bot encontró una respuesta, **No** (rojo) si usó la respuesta por defecto |
| **Fecha** | Fecha y hora en que ocurrió la consulta |

### Filtros disponibles

Encima de la tabla hay una barra de filtros para acotar los resultados:

#### Campo: Desde

Fecha y hora de inicio del rango de búsqueda. Al hacer clic se abre el selector de fecha y hora nativo del navegador. Solo se muestran los logs a partir de esta fecha.

#### Campo: Hasta

Fecha y hora de fin del rango de búsqueda. Solo se muestran los logs anteriores a esta fecha.

#### Campo: Telegram ID

Número identificador de un usuario específico de Telegram. Al llenarlo, la tabla muestra únicamente las consultas realizadas por ese usuario. Útil para rastrear el historial de un usuario en particular.

#### Checkbox: Solo sin respuesta

Al activar esta casilla, la tabla muestra únicamente las consultas para las que el bot **no encontró respuesta** (aquellas donde se usó la respuesta por defecto). Muy útil para identificar qué preguntas frecuentes faltan en la base de conocimiento y deben agregarse.

#### Botón: Aplicar

Ejecuta la consulta con los filtros activos y actualiza la tabla. Los filtros no se aplican automáticamente al cambiarlos; es necesario hacer clic en **Aplicar** para ver los resultados filtrados.

#### Botón: Limpiar

Limpia todos los filtros (borra las fechas, el Telegram ID y desmarca el checkbox) y recarga la tabla mostrando todos los logs desde el principio.

### Paginación de Logs

- **Anterior:** Carga la página anterior (50 registros anteriores).
- **Siguiente:** Carga la siguiente página (50 registros siguientes).
- El texto central indica el rango de registros mostrados (ej: "Mostrando 1–50 registros").

### Cómo usar los logs para mejorar el bot

1. Ir a la sección **📋 Logs**.
2. Activar el checkbox **"Solo sin respuesta"** y hacer clic en **Aplicar**.
3. Revisar los mensajes recibidos que el bot no pudo responder.
4. Identificar patrones: si muchos usuarios preguntan lo mismo y el bot no responde, significa que falta agregar esa pregunta.
5. Ir a la sección **❓ Preguntas** y crear la pregunta faltante con su respuesta y palabras clave.

---

## 11. Referencia de Botones

Listado completo de todos los botones del sistema con su función:

### Pantalla de Login

| Botón | Función |
|---|---|
| **Iniciar Sesión** | Envía las credenciales al servidor y, si son válidas, redirige al panel |
| **👁** (ojo) junto a contraseña | Muestra u oculta el texto de la contraseña |

### Panel Principal — Sidebar

| Botón/Ítem | Función |
|---|---|
| **☰** (menú hamburguesa, topbar) | Abre o cierra el sidebar en pantallas pequeñas |
| **📊 Dashboard** | Navega a la sección de estadísticas |
| **🗂 Categorías** | Navega a la sección de categorías |
| **❓ Preguntas** | Navega a la sección de preguntas frecuentes |
| **⚙️ Configuración Bot** | Navega a la sección de configuración |
| **🤖 Gestión Bot** | Navega a la sección de gestión del bot |
| **📋 Logs** | Navega a la sección de logs de consultas |
| **Cerrar Sesión** | Invalida la sesión actual y redirige al login |

### Sección Dashboard

| Botón | Función |
|---|---|
| **↻ Actualizar** | Recarga todas las estadísticas con datos frescos del servidor |

### Sección Categorías

| Botón | Función |
|---|---|
| **+ Nueva Categoría** | Abre el modal para crear una nueva categoría |
| **✏️** (por fila) | Abre el modal para editar la categoría de esa fila |
| **🗑** (por fila) | Abre el modal de confirmación para eliminar la categoría de esa fila |

### Sección Preguntas

| Botón | Función |
|---|---|
| **+ Nueva Pregunta** | Abre el modal para crear una nueva pregunta frecuente |
| **✏️** (por fila) | Abre el modal para editar la pregunta de esa fila |
| **🗑** (por fila) | Abre el modal de confirmación para eliminar la pregunta de esa fila |
| **Anterior** (paginación) | Carga la página anterior de preguntas |
| **Siguiente** (paginación) | Carga la siguiente página de preguntas |

### Sección Configuración Bot

| Botón | Función |
|---|---|
| **👁** junto al Token | Muestra u oculta el token del bot |
| **Guardar** (Token del Bot) | Guarda el token de Telegram configurado |
| **Guardar** (Chat ID) | Guarda el Chat ID configurado |
| **Guardar** (Respuesta por Defecto) | Guarda el texto de la respuesta por defecto |
| **Toggle Bot Activo** | Activa o desactiva el bot (encendido/apagado) |
| **Guardar** (Bot Activo) | Guarda el estado de activación del bot |

### Sección Gestión Bot

| Botón | Función |
|---|---|
| **Verificar Token** | Verifica con Telegram si el token configurado es válido |
| **Registrar Webhook** | Registra la URL del campo en Telegram como webhook |
| **Ver Info** | Consulta y muestra el estado del webhook activo en Telegram |
| **Eliminar Webhook** | Elimina el webhook registrado (abre modal de confirmación) |
| **Consultar** | Busca una respuesta para el mensaje de prueba ingresado |

### Sección Logs

| Botón | Función |
|---|---|
| **Aplicar** | Aplica los filtros seleccionados y actualiza la tabla |
| **Limpiar** | Limpia todos los filtros y recarga la tabla completa |
| **Anterior** (paginación) | Carga la página anterior de logs |
| **Siguiente** (paginación) | Carga la siguiente página de logs |

### Modal (ventana emergente)

| Botón | Función |
|---|---|
| **Guardar** | Confirma y ejecuta la acción del modal (crear o editar) |
| **Cancelar** | Cierra el modal sin realizar ningún cambio |
| **Eliminar** (modal rojo) | Confirma la eliminación del elemento |
| **×** (esquina superior del modal) | Cierra el modal sin realizar ningún cambio |

---

## 12. Indicadores Visuales: Badges

Los badges son etiquetas de colores que aparecen en las tablas para comunicar el estado de un registro de forma rápida:

| Badge | Color | Significado |
|---|---|---|
| **Activo** | Verde | La categoría o pregunta está habilitada y es usada por el bot |
| **Inactivo** | Rojo | La categoría o pregunta fue desactivada y el bot no la usa |
| **Sí** | Verde | El bot encontró una respuesta para esa consulta |
| **No** | Rojo | El bot no encontró respuesta; usó la respuesta por defecto |
| **Token válido** | Verde | El token de Telegram está correctamente configurado |
| **Error** | Rojo | El token es inválido o no está configurado |
| **Respuesta encontrada** | Verde | La prueba de consulta directa encontró una respuesta |
| **Sin coincidencia** | Rojo | La prueba de consulta directa no encontró respuesta |

---

## 13. Notificaciones del Sistema: Toasts

Los **toasts** son mensajes de notificación que aparecen brevemente en la esquina inferior derecha de la pantalla y desaparecen solos después de 3 segundos. No requieren ninguna acción por parte del usuario.

| Color del Toast | Tipo | Cuándo aparece |
|---|---|---|
| 🟢 Verde | Éxito | Cuando una operación se completó correctamente (crear, editar, guardar, eliminar) |
| 🔴 Rojo | Error | Cuando ocurre un error al procesar una operación |
| 🟡 Amarillo/naranja | Advertencia | Cuando falta ingresar un dato antes de ejecutar una acción |

**Ejemplos de toasts:**
- "Categoría creada" → verde al crear una categoría exitosamente.
- "Pregunta actualizada" → verde al editar una pregunta.
- "Webhook eliminado" → verde al eliminar el webhook.
- "Ingresa la URL del webhook" → amarillo si se hace clic en "Registrar Webhook" sin haber ingresado la URL.
- "Error desconocido" o mensaje de error del servidor → rojo cuando falla una operación.

---

## 14. Preguntas Frecuentes del Usuario

**¿Qué hago si el bot no responde a ciertos mensajes?**

Ir a **📋 Logs**, activar "Solo sin respuesta" y hacer clic en Aplicar. Revisar los mensajes sin respuesta. Luego ir a **❓ Preguntas** y crear las preguntas que faltan con buenas palabras clave.

---

**¿Puedo deshabilitar el bot temporalmente sin perder la configuración?**

Sí. Ir a **⚙️ Configuración Bot**, deslizar el toggle **Bot Activo** hacia apagado y hacer clic en **Guardar**. El bot dejará de procesar mensajes hasta que se vuelva a activar.

---

**¿Qué es la "Respuesta por Defecto" y cuándo se usa?**

Es el mensaje que el bot envía cuando un usuario escribe algo para lo cual no existe ninguna pregunta ni palabra clave coincidente. Se recomienda incluir información de contacto alternativa para que el usuario pueda resolver su duda.

---

**¿Puedo recuperar una categoría o pregunta eliminada?**

No desde el panel. El sistema realiza un "soft delete" (desactivación), por lo que el registro no se borra físicamente de la base de datos, pero no es recuperable desde la interfaz web sin acceso directo a la base de datos.

---

**¿Cómo sé si el bot está funcionando correctamente?**

1. Ir a **🤖 Gestión Bot** y hacer clic en **Verificar Token**. Si el badge es verde, el bot está conectado a Telegram.
2. Usar la **Prueba de Consulta Directa** para verificar que el motor de búsqueda devuelve respuestas correctas.
3. Revisar la sección **📊 Dashboard** para ver si hay actividad reciente en las estadísticas.

---

**¿Qué diferencia hay entre "Filtro por categoría" y "Búsqueda rápida" en la sección de Preguntas?**

- **Filtro por categoría:** Hace una consulta al servidor y trae únicamente las preguntas de esa categoría. Cambia los datos que se muestran.
- **Búsqueda rápida:** Filtra visualmente las filas ya cargadas en pantalla sin hacer una nueva consulta al servidor. Es instantáneo pero solo actúa sobre los registros de la página actual.

---

**¿Por qué el botón "Siguiente" de la paginación está deshabilitado?**

Porque la página actual tiene menos registros que el límite de la página (15 para preguntas, 50 para logs), lo que indica que ya no hay más datos para mostrar.

---

**¿El webhook es obligatorio para que el bot funcione?**

No en entornos de desarrollo local. El sistema incluye un modo de **long-polling automático** que funciona en segundo plano sin necesidad de configurar un webhook. El webhook sí es necesario cuando el servidor está en producción (URL pública en internet).

---

*Manual de Usuario — SmartBot Admin v1.0.0 — Junio 2026*
