import api from './api.js';
import {
  showLoader, showToast, openModal, closeModal,
  escapeHtml, formatErrorDetail,
} from './ui.js';

export function initBot() {
  document.getElementById('btn-verificar-bot')?.addEventListener('click', verificarBot);
  document.getElementById('btn-registrar-webhook')?.addEventListener('click', registrarWebhook);
  document.getElementById('btn-info-webhook')?.addEventListener('click', infoWebhook);
  document.getElementById('btn-eliminar-webhook')?.addEventListener('click', confirmEliminarWebhook);
  document.getElementById('btn-consultar')?.addEventListener('click', consultaDirecta);

  document.getElementById('mensaje-prueba')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') consultaDirecta();
  });
}

async function verificarBot() {
  const container = document.getElementById('resultado-verificar');
  showLoader(true);
  try {
    const data = await api.get('/api/bot/verificar');
    if (data.status === 'ok' && data.bot) {
      container.innerHTML = `
        <div class="result-panel result-panel--success" style="margin-top:12px">
          <span class="badge badge--success">Token válido</span>
          <p><strong>${escapeHtml(data.bot.first_name)}</strong> (@${escapeHtml(data.bot.username)})</p>
          <p>ID: ${data.bot.id}</p>
        </div>
      `;
    } else {
      container.innerHTML = `
        <div class="result-panel result-panel--error" style="margin-top:12px">
          <span class="badge badge--danger">Error</span>
          <p>${escapeHtml(data.detalle || 'Token no configurado o inválido')}</p>
        </div>
      `;
    }
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

async function registrarWebhook() {
  const url = document.getElementById('url-webhook')?.value.trim();
  if (!url) {
    showToast('Ingresa la URL del webhook', 'warning');
    return;
  }

  showLoader(true);
  try {
    const data = await api.post('/api/bot/registrar-webhook', { url_webhook: url });
    const container = document.getElementById('resultado-webhook');
    if (data.status === 'ok') {
      showToast('Webhook registrado correctamente');
      container.innerHTML = `<div class="result-panel result-panel--success"><p>Webhook registrado en: ${escapeHtml(url)}</p></div>`;
    } else {
      showToast(data.detalle || 'Error al registrar webhook', 'error');
    }
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

async function infoWebhook() {
  showLoader(true);
  try {
    const data = await api.get('/api/bot/info-webhook');
    const container = document.getElementById('resultado-webhook');

    if (data.status === 'ok' && data.webhook) {
      const w = data.webhook;
      container.innerHTML = `
        <div class="table-wrapper" style="margin-top:12px">
          <table>
            <tbody>
              <tr><td><strong>URL</strong></td><td>${escapeHtml(w.url || '—')}</td></tr>
              <tr><td><strong>Updates pendientes</strong></td><td>${w.pending_update_count ?? '—'}</td></tr>
              <tr><td><strong>Último error</strong></td><td>${escapeHtml(w.last_error_message || 'Ninguno')}</td></tr>
              <tr><td><strong>IP</strong></td><td>${escapeHtml(w.ip_address || '—')}</td></tr>
            </tbody>
          </table>
        </div>
      `;
    } else {
      container.innerHTML = `
        <div class="result-panel result-panel--error" style="margin-top:12px">
          <p>${escapeHtml(data.detalle || 'No se pudo obtener información del webhook')}</p>
        </div>
      `;
    }
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

function confirmEliminarWebhook() {
  openModal({
    title: 'Eliminar Webhook',
    bodyHtml: '<p>¿Eliminar el webhook registrado en Telegram? El bot dejará de recibir mensajes automáticamente.</p>',
    confirmText: 'Eliminar',
    danger: true,
    onConfirm: async () => {
      showLoader(true);
      try {
        await api.delete('/api/bot/webhook');
        showToast('Webhook eliminado');
        closeModal();
        document.getElementById('resultado-webhook').innerHTML = '';
      } catch (err) {
        showToast(formatErrorDetail(err.detail), 'error');
      } finally {
        showLoader(false);
      }
    },
  });
}

async function consultaDirecta() {
  const mensaje = document.getElementById('mensaje-prueba')?.value.trim();
  if (!mensaje) {
    showToast('Escribe un mensaje de prueba', 'warning');
    return;
  }

  showLoader(true);
  try {
    const data = await api.get(
      `/api/bot/consulta?mensaje=${encodeURIComponent(mensaje)}`,
      false
    );
    const container = document.getElementById('resultado-consulta');
    const found = data.encontro_respuesta;

    container.innerHTML = `
      <div class="result-panel ${found ? 'result-panel--success' : 'result-panel--error'}" style="margin-top:12px">
        <span class="badge ${found ? 'badge--success' : 'badge--danger'}">
          ${found ? 'Respuesta encontrada' : 'Sin coincidencia'}
        </span>
        ${found && data.pregunta ? `<p><strong>Pregunta:</strong> ${escapeHtml(data.pregunta)}</p>` : ''}
        <p><strong>Respuesta:</strong> ${escapeHtml(data.respuesta)}</p>
      </div>
    `;
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}
