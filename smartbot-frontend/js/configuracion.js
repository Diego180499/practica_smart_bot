import api from './api.js';
import { showLoader, showToast, escapeHtml, formatErrorDetail } from './ui.js';

const CONFIG_KEYS = [
  { clave: 'TELEGRAM_BOT_TOKEN', type: 'password', label: 'Token del Bot de Telegram' },
  { clave: 'TELEGRAM_CHAT_ID', type: 'text', label: 'Chat ID de Telegram' },
  { clave: 'RESPUESTA_DEFAULT', type: 'textarea', label: 'Respuesta por Defecto' },
  { clave: 'BOT_ACTIVO', type: 'toggle', label: 'Bot Activo' },
];

export async function loadConfiguracion() {
  showLoader(true);
  try {
    const configs = await api.get('/api/configuracion') || [];
    renderConfig(configs);
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

function renderConfig(configs) {
  const container = document.getElementById('config-container');
  if (!container) return;

  const configMap = Object.fromEntries(configs.map(c => [c.clave, c]));

  container.innerHTML = CONFIG_KEYS.map(({ clave, type, label }) => {
    const config = configMap[clave] || { valor: '', descripcion: '' };
    const id = `config-${clave}`;

    let inputHtml = '';
    if (type === 'password') {
      inputHtml = `
        <div class="input-group">
          <input type="password" id="${id}" class="form-control" value="${escapeHtml(config.valor || '')}">
          <button type="button" class="toggle-password" data-target="${id}" aria-label="Mostrar">👁</button>
        </div>
      `;
    } else if (type === 'textarea') {
      inputHtml = `<textarea id="${id}" class="form-control" rows="3">${escapeHtml(config.valor || '')}</textarea>`;
    } else if (type === 'toggle') {
      const checked = config.valor === '1' ? 'checked' : '';
      inputHtml = `
        <label class="toggle">
          <input type="checkbox" id="${id}" ${checked}>
          <span class="toggle__slider"></span>
        </label>
      `;
    } else {
      inputHtml = `<input type="text" id="${id}" class="form-control" value="${escapeHtml(config.valor || '')}">`;
    }

    return `
      <div class="card config-row" data-clave="${clave}">
        <div class="config-row__header">
          <div>
            <h3>${escapeHtml(label)}</h3>
            <p class="config-row__desc">${escapeHtml(config.descripcion || clave)}</p>
          </div>
        </div>
        ${inputHtml}
        <div class="config-row__actions">
          <button class="btn btn--primary btn--sm btn-guardar-config" data-clave="${clave}" data-type="${type}">Guardar</button>
        </div>
      </div>
    `;
  }).join('');

  container.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      btn.textContent = isPassword ? '🙈' : '👁';
    });
  });

  container.querySelectorAll('.btn-guardar-config').forEach(btn => {
    btn.addEventListener('click', () => saveConfig(btn.dataset.clave, btn.dataset.type));
  });
}

async function saveConfig(clave, type) {
  const input = document.getElementById(`config-${clave}`);
  if (!input) return;

  let valor;
  if (type === 'toggle') {
    valor = input.checked ? '1' : '0';
  } else {
    valor = input.value;
  }

  showLoader(true);
  try {
    await api.put(`/api/configuracion/${clave}`, { valor });
    showToast(`${clave} guardado correctamente`);
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

export function initConfiguracion() {
  // Listeners se registran al renderizar
}
