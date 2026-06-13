import api from './api.js';
import {
  showLoader, showToast, renderTable,
  formatDate, foundBadge, truncate, escapeHtml, formatErrorDetail,
} from './ui.js';

const PAGE_SIZE = 50;
let currentSkip = 0;
let lastCount = 0;

function buildQueryParams() {
  const params = new URLSearchParams();
  params.set('skip', currentSkip);
  params.set('limit', PAGE_SIZE);

  const desde = document.getElementById('log-desde')?.value;
  const hasta = document.getElementById('log-hasta')?.value;
  const telegramId = document.getElementById('log-telegram-id')?.value;
  const sinRespuesta = document.getElementById('log-sin-respuesta')?.checked;

  if (desde) params.set('fecha_desde', new Date(desde).toISOString());
  if (hasta) params.set('fecha_hasta', new Date(hasta).toISOString());
  if (telegramId) params.set('telegram_id', telegramId);
  if (sinRespuesta) params.set('solo_sin_respuesta', 'true');

  return params.toString();
}

export async function loadLogs() {
  showLoader(true);
  try {
    const logs = await api.get(`/api/logs/consultas?${buildQueryParams()}`) || [];
    lastCount = logs.length;

    renderTable(
      document.getElementById('table-logs'),
      [
        { key: 'id', label: 'ID' },
        {
          key: 'id_usuario_telegram', label: 'Usuario TG',
          render: (row) => escapeHtml(row.id_usuario_telegram ?? '—'),
        },
        {
          key: 'mensaje_recibido', label: 'Mensaje Recibido', class: 'td-truncate',
          render: (row) => escapeHtml(truncate(row.mensaje_recibido, 50)),
        },
        {
          key: 'respuesta_enviada', label: 'Respuesta Enviada', class: 'td-truncate',
          render: (row) => escapeHtml(truncate(row.respuesta_enviada, 50)),
        },
        {
          key: 'encontro_respuesta', label: '¿Encontró?',
          render: (row) => foundBadge(row.encontro_respuesta),
        },
        {
          key: 'fecha_consulta', label: 'Fecha',
          render: (row) => escapeHtml(formatDate(row.fecha_consulta)),
        },
      ],
      logs,
      'No hay logs de consultas'
    );

    updatePagination();
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

function updatePagination() {
  const info = document.getElementById('pagination-logs-info');
  const btnPrev = document.getElementById('btn-log-anterior');
  const btnNext = document.getElementById('btn-log-siguiente');

  const from = lastCount > 0 ? currentSkip + 1 : 0;
  const to = currentSkip + lastCount;
  info.textContent = lastCount > 0
    ? `Mostrando ${from}–${to} registros`
    : 'Sin registros';

  btnPrev.disabled = currentSkip === 0;
  btnNext.disabled = lastCount < PAGE_SIZE;
}

function limpiarFiltros() {
  document.getElementById('log-desde').value = '';
  document.getElementById('log-hasta').value = '';
  document.getElementById('log-telegram-id').value = '';
  document.getElementById('log-sin-respuesta').checked = false;
  currentSkip = 0;
  loadLogs();
}

export function initLogs() {
  document.getElementById('btn-aplicar-filtros')?.addEventListener('click', () => {
    currentSkip = 0;
    loadLogs();
  });

  document.getElementById('btn-limpiar-filtros')?.addEventListener('click', limpiarFiltros);

  document.getElementById('btn-log-anterior')?.addEventListener('click', () => {
    currentSkip = Math.max(0, currentSkip - PAGE_SIZE);
    loadLogs();
  });

  document.getElementById('btn-log-siguiente')?.addEventListener('click', () => {
    currentSkip += PAGE_SIZE;
    loadLogs();
  });
}
