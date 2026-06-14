import api from './api.js';
import { fetchCategoriasForSelect } from './categorias.js';
import {
  showLoader, showToast, renderTable, openModal, closeModal,
  truncate, statusBadge, escapeHtml, formatErrorDetail,
} from './ui.js';

const PAGE_SIZE = 15;
let currentSkip = 0;
let currentCategoriaId = '';
let allPreguntas = [];
let categoriasMap = {};

export async function loadPreguntas() {
  showLoader(true);
  try {
    const cats = await fetchCategoriasForSelect();
    categoriasMap = Object.fromEntries(cats.map(c => [c.id, c.nombre]));
    populateCategoriaSelect(cats);

    let path = `/api/preguntas?skip=${currentSkip}&limit=${PAGE_SIZE}`;
    if (currentCategoriaId) path += `&id_categoria=${currentCategoriaId}`;

    allPreguntas = await api.get(path) || [];
    renderPreguntasTable(allPreguntas);
    updatePagination(allPreguntas.length);
  } catch (err) {
    showToast(formatErrorDetail(err.detail), 'error');
  } finally {
    showLoader(false);
  }
}

function populateCategoriaSelect(categorias) {
  const select = document.getElementById('filtro-categoria');
  if (!select) return;

  const current = select.value;
  select.innerHTML = '<option value="">Todas las categorías</option>';
  categorias.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat.id;
    opt.textContent = cat.nombre;
    select.appendChild(opt);
  });
  select.value = current;
}

function renderPreguntasTable(preguntas) {
  const searchTerm = document.getElementById('filtro-busqueda')?.value.toLowerCase() || '';
  const filtered = searchTerm
    ? preguntas.filter(p =>
        p.pregunta.toLowerCase().includes(searchTerm) ||
        (p.palabras_clave || '').toLowerCase().includes(searchTerm) ||
        (categoriasMap[p.id_categoria] || '').toLowerCase().includes(searchTerm)
      )
    : preguntas;

  renderTable(
    document.getElementById('table-preguntas'),
    [
      { key: 'id', label: 'ID' },
      {
        key: 'id_categoria', label: 'Categoría',
        render: (row) => escapeHtml(categoriasMap[row.id_categoria] || '—'),
      },
      {
        key: 'pregunta', label: 'Pregunta', class: 'td-truncate',
        render: (row) => escapeHtml(truncate(row.pregunta, 60)),
      },
      {
        key: 'palabras_clave', label: 'Palabras clave', class: 'td-truncate',
        render: (row) => escapeHtml(truncate(row.palabras_clave || '—', 40)),
      },
      {
        key: 'activo', label: 'Estado',
        render: (row) => statusBadge(row.activo),
      },
      {
        key: 'actions', label: 'Acciones',
        render: (row) => `
          <div class="td-actions">
            <button class="btn btn--ghost btn--sm btn--icon btn-editar-preg" data-id="${row.id}" title="Editar">✏️</button>
            <button class="btn btn--danger btn--sm btn--icon btn-eliminar-preg" data-id="${row.id}" title="Eliminar">🗑</button>
          </div>
        `,
      },
    ],
    filtered,
    'No hay preguntas registradas'
  );

  document.querySelectorAll('.btn-editar-preg').forEach(btn => {
    btn.addEventListener('click', () => openPreguntaModal(Number(btn.dataset.id)));
  });

  document.querySelectorAll('.btn-eliminar-preg').forEach(btn => {
    btn.addEventListener('click', () => confirmEliminarPregunta(Number(btn.dataset.id)));
  });
}

function updatePagination(count) {
  const info = document.getElementById('pagination-preguntas-info');
  const btnPrev = document.getElementById('btn-preg-anterior');
  const btnNext = document.getElementById('btn-preg-siguiente');

  const from = currentSkip + 1;
  const to = currentSkip + count;
  info.textContent = count > 0 ? `Mostrando ${from}–${to}` : 'Sin registros';

  btnPrev.disabled = currentSkip === 0;
  btnNext.disabled = count < PAGE_SIZE;
}

async function openPreguntaModal(id = null) {
  const cats = await fetchCategoriasForSelect();
  const options = cats.map(c =>
    `<option value="${c.id}">${escapeHtml(c.nombre)}</option>`
  ).join('');

  let pregunta = null;
  if (id) {
    showLoader(true);
    try {
      pregunta = await api.get(`/api/preguntas/${id}`);
    } catch (err) {
      showToast(formatErrorDetail(err.detail), 'error');
      showLoader(false);
      return;
    }
    showLoader(false);
  }

  openModal({
    title: id ? 'Editar Pregunta' : 'Nueva Pregunta',
    bodyHtml: `
      <div class="form-group">
        <label for="preg-categoria">Categoría *</label>
        <select id="preg-categoria" class="form-control" required>
          <option value="">Seleccionar categoría</option>
          ${options}
        </select>
        <div id="preg-categoria-error" class="form-error hidden"></div>
      </div>
      <div class="form-group">
        <label for="preg-pregunta">Pregunta *</label>
        <textarea id="preg-pregunta" class="form-control" rows="2" required>${escapeHtml(pregunta?.pregunta || '')}</textarea>
        <div id="preg-pregunta-error" class="form-error hidden"></div>
      </div>
      <div class="form-group">
        <label for="preg-respuesta">Respuesta *</label>
        <textarea id="preg-respuesta" class="form-control" rows="4" required>${escapeHtml(pregunta?.respuesta || '')}</textarea>
        <div id="preg-respuesta-error" class="form-error hidden"></div>
      </div>
      <div class="form-group">
        <label for="preg-palabras">Palabras clave (separadas por coma)</label>
        <input type="text" id="preg-palabras" class="form-control" value="${escapeHtml(pregunta?.palabras_clave || '')}">
      </div>
    `,
    onConfirm: async () => {
      const id_categoria = Number(document.getElementById('preg-categoria').value);
      const preguntaText = document.getElementById('preg-pregunta').value.trim();
      const respuesta = document.getElementById('preg-respuesta').value.trim();
      const palabras_clave = document.getElementById('preg-palabras').value.trim();

      let valid = true;
      ['preg-categoria', 'preg-pregunta', 'preg-respuesta'].forEach(field => {
        const el = document.getElementById(`${field}-error`);
        el.classList.add('hidden');
      });

      if (!id_categoria) {
        document.getElementById('preg-categoria-error').textContent = 'Selecciona una categoría';
        document.getElementById('preg-categoria-error').classList.remove('hidden');
        valid = false;
      }
      if (!preguntaText) {
        document.getElementById('preg-pregunta-error').textContent = 'La pregunta es requerida';
        document.getElementById('preg-pregunta-error').classList.remove('hidden');
        valid = false;
      }
      if (!respuesta) {
        document.getElementById('preg-respuesta-error').textContent = 'La respuesta es requerida';
        document.getElementById('preg-respuesta-error').classList.remove('hidden');
        valid = false;
      }
      if (!valid) return;

      showLoader(true);
      try {
        const body = { pregunta: preguntaText, respuesta, id_categoria, palabras_clave };
        if (id) {
          await api.put(`/api/preguntas/${id}`, body);
          showToast('Pregunta actualizada');
        } else {
          await api.post('/api/preguntas', body);
          showToast('Pregunta creada');
        }
        closeModal();
        await loadPreguntas();
      } catch (err) {
        showToast(formatErrorDetail(err.detail), 'error');
      } finally {
        showLoader(false);
      }
    },
  });

  if (pregunta) {
    document.getElementById('preg-categoria').value = pregunta.id_categoria;
  }
}

function confirmEliminarPregunta(id) {
  openModal({
    title: 'Confirmar eliminación',
    bodyHtml: '<p>¿Eliminar esta pregunta? Esta acción no se puede deshacer.</p>',
    confirmText: 'Eliminar',
    danger: true,
    onConfirm: async () => {
      showLoader(true);
      try {
        await api.delete(`/api/preguntas/${id}`);
        showToast('Pregunta eliminada');
        closeModal();
        await loadPreguntas();
      } catch (err) {
        showToast(formatErrorDetail(err.detail), 'error');
      } finally {
        showLoader(false);
      }
    },
  });
}

export function initPreguntas() {
  document.getElementById('btn-nueva-pregunta')?.addEventListener('click', () => openPreguntaModal());

  document.getElementById('filtro-categoria')?.addEventListener('change', (e) => {
    currentCategoriaId = e.target.value;
    currentSkip = 0;
    loadPreguntas();
  });

  document.getElementById('filtro-busqueda')?.addEventListener('input', () => {
    renderPreguntasTable(allPreguntas);
  });

  document.getElementById('btn-preg-anterior')?.addEventListener('click', () => {
    currentSkip = Math.max(0, currentSkip - PAGE_SIZE);
    loadPreguntas();
  });

  document.getElementById('btn-preg-siguiente')?.addEventListener('click', () => {
    currentSkip += PAGE_SIZE;
    loadPreguntas();
  });
}
