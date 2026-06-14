import api from './api.js';
import { showLoader, showToast, renderTable, formatErrorDetail } from './ui.js';

export async function loadEstadisticas() {
  showLoader(true);
  try {
    const data = await api.get('/api/estadisticas');
    if (!data) return;

    const total = data.total_consultas || 0;
    const sinRespuesta = data.consultas_sin_respuesta || 0;
    const resolucion = total > 0
      ? Math.round(((total - sinRespuesta) / total) * 100)
      : 0;

    document.getElementById('kpi-grid').innerHTML = `
      <div class="card">
        <div class="card__title">Total Consultas</div>
        <div class="card__value">${total}</div>
      </div>
      <div class="card">
        <div class="card__title">Sin Respuesta</div>
        <div class="card__value">${sinRespuesta}</div>
      </div>
      <div class="card">
        <div class="card__title">Usuarios Únicos</div>
        <div class="card__value">${data.total_usuarios_unicos || 0}</div>
      </div>
      <div class="card">
        <div class="card__title">% Resolución</div>
        <div class="card__value">${resolucion}%</div>
      </div>
    `;

    renderTable(
      document.getElementById('table-top-preguntas'),
      [
        { key: 'pregunta', label: 'Pregunta' },
        { key: 'total_consultas', label: 'Consultas' },
      ],
      data.top_preguntas || [],
      'Sin datos de preguntas'
    );

    renderTable(
      document.getElementById('table-top-usuarios'),
      [
        { key: 'nombre', label: 'Nombre' },
        { key: 'telegram_id', label: 'Telegram ID' },
        { key: 'total_consultas', label: 'Consultas' },
      ],
      data.top_usuarios || [],
      'Sin datos de usuarios'
    );

    renderTable(
      document.getElementById('table-distribucion'),
      [
        { key: 'categoria', label: 'Categoría' },
        { key: 'total_preguntas', label: 'Preguntas' },
        { key: 'total_consultas', label: 'Consultas' },
      ],
      data.distribucion_categorias || [],
      'Sin datos de categorías'
    );
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

export function initEstadisticas() {
  document.getElementById('btn-refresh-stats')?.addEventListener('click', loadEstadisticas);
}
