import api, { setToken, clearToken, isAuthenticated } from './api.js';
import { showLoader, showToast, formatErrorDetail } from './ui.js';

function redirectIfAuthenticated() {
  if (isAuthenticated()) {
    window.location.href = 'dashboard.html';
  }
}

async function handleLogin(e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const errorEl = document.getElementById('login-error');
  const btnLogin = document.getElementById('btn-login');

  errorEl.classList.add('hidden');
  btnLogin.disabled = true;
  showLoader(true);

  try {
    const data = await api.post('/api/auth/login', { username, password }, false);
    if (data?.access_token) {
      setToken(data.access_token);
      window.location.href = 'dashboard.html';
    }
  } catch (err) {
    errorEl.textContent = formatErrorDetail(err.detail) || 'Credenciales inválidas';
    errorEl.classList.remove('hidden');
  } finally {
    btnLogin.disabled = false;
    showLoader(false);
  }
}

function initPasswordToggle() {
  const toggle = document.getElementById('toggle-password');
  const input = document.getElementById('password');
  if (!toggle || !input) return;

  toggle.addEventListener('click', () => {
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    toggle.textContent = isPassword ? '🙈' : '👁';
  });
}

export async function logout() {
  showLoader(true);
  try {
    await api.post('/api/auth/logout', {});
  } catch {
    // Redirigir aunque falle el logout en servidor
  } finally {
    clearToken();
    showLoader(false);
    window.location.href = 'index.html';
  }
}

// Login page init
if (document.getElementById('login-form')) {
  redirectIfAuthenticated();
  initPasswordToggle();
  document.getElementById('login-form').addEventListener('submit', handleLogin);
}

export { isAuthenticated };
