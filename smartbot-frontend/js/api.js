const API_BASE = 'http://localhost:8000';
const TOKEN_KEY = 'smartbot_token';

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated() {
  return !!getToken();
}

async function request(method, path, body = null, requiresAuth = true) {
  const headers = { 'Content-Type': 'application/json' };

  if (requiresAuth) {
    const token = getToken();
    if (!token) {
      window.location.href = 'index.html';
      return null;
    }
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body !== null) options.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(`${API_BASE}${path}`, options);
  } catch {
    throw { status: 0, detail: 'No se puede conectar con el servidor' };
  }

  if (res.status === 401 || res.status === 403) {
    clearToken();
    window.location.href = 'index.html';
    return null;
  }

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw { status: res.status, detail: data?.detail || 'Error desconocido' };
  }

  return data;
}

const api = {
  get: (path, auth = true) => request('GET', path, null, auth),
  post: (path, body, auth = true) => request('POST', path, body, auth),
  put: (path, body, auth = true) => request('PUT', path, body, auth),
  delete: (path, auth = true) => request('DELETE', path, null, auth),
};

export default api;
