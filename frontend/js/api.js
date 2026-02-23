// ── api.js ────────────────────────────────────────────────────────
// Central fetch wrapper — attaches Auth0 JWT on every request

const API_BASE = "/api";

async function apiFetch(path, options = {}) {
  // Get fresh token from Auth0 (auto-refreshes if expired)
  const token = await getToken();

  const headers = {
    "Content-Type":  "application/json",
    "Authorization": `Bearer ${token}`,
    ...(options.headers || {})
  };

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    // Token invalid — force re-login
    await auth0Client.loginWithRedirect();
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}