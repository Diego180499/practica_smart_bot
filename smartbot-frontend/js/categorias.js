import api from './api.js';
import {
  showLoader, showToast, renderTable, openModal, closeModal,
  formatDate, statusBadge, escapeHtml, formatErrorDetail,
} from './ui.js';

let categoriasData = [];

export async function loadCategorias() {
  showLoader(true);
  try {
    categoriasData = await api.get('/api/categorias', false) || [];

    renderTable(
      document.getElementById('table-categorias'),
      [
        { key: 'id', label: 'ID' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'descripcion', label: 'Descripción', class: 'td-truncate' },
        {
          key: 'activo', label: 'Estado',
          render: (row) => statusBadge(row.activo),
        },
        {
          key: 'created_at', label: 'Creado',
          render: (row) => escapeHtml(formatDate(row.created_at)),
        },
        {
          key: 'actions', label: 'Acciones',
          render: (row) => `
            <div class="td-actions">
              <button class="btn btn--ghost btn--sm btn--icon btn-editar-cat" data-id="${row.id}" title="Editar">✏️</button>
              <button class="btn btn--danger btn--sm btn--icon btn-eliminar-cat" data-id="${row.id}" title="Eliminar">🗑</button>
            </div>
          `,
        },
      ],
      categoriasData,
      'No hay categorías registradas'
    );

    bindTableActions();
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

function bindTableActions() {
  document.querySelectorAll('.btn-editar-cat').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = categoriasData.find(c => c.id === Number(btn.dataset.id));
      if (cat) openCategoriaModal(cat);
    });
  });

  document.querySelectorAll('.btn-eliminar-cat').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = categoriasData.find(c => c.id === Number(btn.dataset.id));
      if (cat) confirmEliminar(cat.id, cat.nombre);
    });
  });
}

function openCategoriaModal(categoria = null) {
  const isEdit = !!categoria;
  openModal({
    title: isEdit ? 'Editar Categoría' : 'Nueva Categoría',
    bodyHtml: `
      <div class="form-group">
        <label for="cat-nombre">Nombre *</label>
        <input type="text" id="cat-nombre" class="form-control" value="${escapeHtml(categoria?.nombre || '')}" required>
        <div id="cat-nombre-error" class="form-error hidden"></div>
      </div>
      <div class="form-group">
        <label for="cat-descripcion">Descripción</label>
        <textarea id="cat-descripcion" class="form-control" rows="3">${escapeHtml(categoria?.descripcion || '')}</textarea>
      </div>
    `,
    onConfirm: async () => {
      const nombre = document.getElementById('cat-nombre').value.trim();
      const descripcion = document.getElementById('cat-descripcion').value.trim();
      const errorEl = document.getElementById('cat-nombre-error');

      if (!nombre) {
        errorEl.textContent = 'El nombre es requerido';
        errorEl.classList.remove('hidden');
        return;
      }
      errorEl.classList.add('hidden');

      showLoader(true);
      try {
        if (isEdit) {
          await api.put(`/api/categorias/${categoria.id}`, { nombre, descripcion });
          showToast('Categoría actualizada');
        } else {
          await api.post('/api/categorias', { nombre, descripcion });
          showToast('Categoría creada');
        }
        closeModal();
        await loadCategorias();
      } catch (err) {
        if (err.status === 409) {
          errorEl.textContent = formatErrorDetail(err.detail);
          errorEl.classList.remove('hidden');
        } else {
          showToast(formatErrorDetail(err.detail), 'error');
        }
      } finally {
        showLoader(false);
      }
    },
  });
}

function confirmEliminar(id, nombre) {
  openModal({
    title: 'Confirmar eliminación',
    bodyHtml: `<p>¿Eliminar la categoría <strong>${escapeHtml(nombre)}</strong>? Esta acción no se puede deshacer.</p>`,
    confirmText: 'Eliminar',
    danger: true,
    onConfirm: async () => {
      showLoader(true);
      try {
        await api.delete(`/api/categorias/${id}`);
        showToast('Categoría eliminada');
        closeModal();
        await loadCategorias();
      } catch (err) {
        closeModal();
        showToast(formatErrorDetail(err.detail), 'error');
      } finally {
        showLoader(false);
      }
    },
  });
}

export function initCategorias() {
  document.getElementById('btn-nueva-categoria')?.addEventListener('click', () => openCategoriaModal());
}

export function getCategoriasData() {
  return categoriasData;
}

export async function fetchCategoriasForSelect() {
  try {
    categoriasData = await api.get('/api/categorias', false) || [];
    return categoriasData;
  } catch {
    return [];
  }
}
