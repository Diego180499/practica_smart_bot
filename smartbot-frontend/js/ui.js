export function escapeHtml(str) {
  if (str == null) return '';
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

export function formatDate(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleString('es-GT', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  });
}

export function truncate(str, max = 60) {
  if (!str) return '';
  return str.length > max ? str.slice(0, max) + '…' : str;
}

export function showLoader(show = true) {
  const loader = document.getElementById('loader');
  if (loader) loader.classList.toggle('hidden', !show);
}

export function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => toast.remove(), 3000);
}

export function formatErrorDetail(detail) {
  if (!detail) return 'Error desconocido';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map(e => e.msg || JSON.stringify(e)).join('. ');
  }
  return String(detail);
}

let modalConfirmHandler = null;

export function openModal({ title, bodyHtml, confirmText = 'Guardar', onConfirm, danger = false }) {
  const modal = document.getElementById('modal');
  const titleEl = document.getElementById('modal-title');
  const bodyEl = document.getElementById('modal-body');
  const confirmBtn = document.getElementById('modal-confirm');

  titleEl.textContent = title;
  bodyEl.innerHTML = bodyHtml;
  confirmBtn.textContent = confirmText;
  confirmBtn.className = danger ? 'btn btn--danger' : 'btn btn--primary';

  modalConfirmHandler = onConfirm;
  modal.classList.remove('hidden');
}

export function closeModal() {
  const modal = document.getElementById('modal');
  modal.classList.add('hidden');
  modalConfirmHandler = null;
  document.getElementById('modal-body').innerHTML = '';
}

export function initModalListeners() {
  document.getElementById('modal-close')?.addEventListener('click', closeModal);
  document.getElementById('modal-cancel')?.addEventListener('click', closeModal);
  document.querySelector('.modal__overlay')?.addEventListener('click', closeModal);

  document.getElementById('modal-confirm')?.addEventListener('click', async () => {
    if (modalConfirmHandler) {
      await modalConfirmHandler();
    }
  });
}

export function renderTable(container, columns, rows, emptyMessage = 'No hay datos') {
  if (!container) return;

  if (!rows || rows.length === 0) {
    container.innerHTML = `<div class="empty-state">${escapeHtml(emptyMessage)}</div>`;
    return;
  }

  const thead = columns.map(col =>
    `<th>${escapeHtml(col.label)}</th>`
  ).join('');

  const tbody = rows.map(row => {
    const cells = columns.map(col => {
      const value = col.render ? col.render(row) : escapeHtml(row[col.key]);
      return `<td${col.class ? ` class="${col.class}"` : ''}>${value}</td>`;
    }).join('');
    return `<tr>${cells}</tr>`;
  }).join('');

  container.innerHTML = `
    <table>
      <thead><tr>${thead}</tr></thead>
      <tbody>${tbody}</tbody>
    </table>
  `;
}

export function statusBadge(activo) {
  const isActive = activo === 1 || activo === true;
  return isActive
    ? '<span class="badge badge--success">Activo</span>'
    : '<span class="badge badge--danger">Inactivo</span>';
}

export function foundBadge(encontro) {
  const found = encontro === 1 || encontro === true;
  return found
    ? '<span class="badge badge--success">Sí</span>'
    : '<span class="badge badge--danger">No</span>';
}
