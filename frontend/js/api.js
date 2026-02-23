
// ── api.js ────────────────────────────────────────────────────────
// Central fetch wrapper. Phase 2: will attach Auth0 JWT automatically.

const API_BASE = "/api";  // proxied through NGINX → FastAPI

async function apiFetch(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  // Phase 2: headers["Authorization"] = `Bearer ${await getToken()}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}
