import { isAuthenticated, logout } from './auth.js';
import { initModalListeners } from './ui.js';
import { loadEstadisticas, initEstadisticas } from './estadisticas.js';
import { loadCategorias, initCategorias } from './categorias.js';
import { loadPreguntas, initPreguntas } from './preguntas.js';
import { loadConfiguracion, initConfiguracion } from './configuracion.js';
import { initBot } from './bot.js';
import { loadLogs, initLogs } from './logs.js';

const SECTION_TITLES = {
  estadisticas: 'Dashboard',
  categorias: 'Categorías',
  preguntas: 'Preguntas Frecuentes',
  configuracion: 'Configuración del Bot',
  bot: 'Gestión del Bot',
  logs: 'Logs de Consultas',
};

const sectionLoaders = {
  estadisticas: loadEstadisticas,
  categorias: loadCategorias,
  preguntas: loadPreguntas,
  configuracion: loadConfiguracion,
  logs: loadLogs,
};

let currentSection = 'estadisticas';

function navigateTo(section) {
  if (!SECTION_TITLES[section]) return;

  currentSection = section;

  document.querySelectorAll('.section').forEach(el => el.classList.add('hidden'));
  document.getElementById(`section-${section}`)?.classList.remove('hidden');

  document.querySelectorAll('.sidebar__nav a').forEach(link => {
    link.classList.toggle('active', link.dataset.section === section);
  });

  document.getElementById('section-title').textContent = SECTION_TITLES[section];
  window.location.hash = section;

  if (sectionLoaders[section]) {
    sectionLoaders[section]();
  }

  closeSidebarMobile();
}

function closeSidebarMobile() {
  document.getElementById('sidebar')?.classList.remove('open');
  document.getElementById('sidebar-overlay')?.classList.remove('visible');
}

function initRouter() {
  document.querySelectorAll('.sidebar__nav a').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      navigateTo(link.dataset.section);
    });
  });

  const hash = window.location.hash.replace('#', '');
  navigateTo(SECTION_TITLES[hash] ? hash : 'estadisticas');
}

function initSidebar() {
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');

  toggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
    overlay?.classList.toggle('visible');
  });

  overlay?.addEventListener('click', closeSidebarMobile);
}

function init() {
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  initModalListeners();
  initEstadisticas();
  initCategorias();
  initPreguntas();
  initConfiguracion();
  initBot();
  initLogs();
  initSidebar();
  initRouter();

  document.getElementById('btn-logout')?.addEventListener('click', logout);
}

init();
