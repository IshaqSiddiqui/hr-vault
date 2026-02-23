// ── auth.js ───────────────────────────────────────────────────────
// Auth0 SPA SDK integration

const AUTH0_DOMAIN    = "dev-w0igowxm.us.auth0.com";
const AUTH0_CLIENT_ID = "sCpq5bb65QYIqUS9OEnN4Yaf54q9ut07";
const AUTH0_AUDIENCE  = "https://hr-vault-api";

let auth0Client = null;

async function initAuth0() {
  // Create Auth0 client if not already created
  if (!auth0Client) {
    auth0Client = await auth0.createAuth0Client({
      domain:   AUTH0_DOMAIN,
      clientId: AUTH0_CLIENT_ID,
      authorizationParams: {
        audience:     AUTH0_AUDIENCE,
        redirect_uri: window.location.origin + "/dashboard.html",
      }
    });
  }

  // Handle redirect callback after Auth0 login
  if (window.location.search.includes("code=") ||
      window.location.search.includes("error=")) {
    await auth0Client.handleRedirectCallback();
    window.history.replaceState({}, document.title, window.location.pathname);
  }

  const isAuthenticated = await auth0Client.isAuthenticated();

  // If on dashboard and not authenticated → redirect to Auth0 login
  if (!isAuthenticated && window.location.pathname.includes("dashboard")) {
    await auth0Client.loginWithRedirect();
    return false;
  }

  // If on login page and already authenticated → go to dashboard
  if (isAuthenticated && (
    window.location.pathname === "/" ||
    window.location.pathname.includes("index")
  )) {
    window.location.href = "/dashboard.html";
    return true;
  }

  return isAuthenticated;
}

async function getToken() {
  return await auth0Client.getTokenSilently();
}

async function getCurrentUser() {
  const user  = await auth0Client.getUser();
  const token = await getToken();
  const payload = JSON.parse(atob(token.split(".")[1]));
  const role  = payload["https://hr-vault/role"] || "employee";
  return { name: user.name, email: user.email, role };
}

async function logout() {
  await auth0Client.logout({
    logoutParams: { returnTo: window.location.origin + "/index.html" }
  });
}

// Login button on index.html
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.addEventListener("click", async () => {
    if (!auth0Client) await initAuth0();
    await auth0Client.loginWithRedirect();
  });
}

// Logout button on dashboard.html
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) logoutBtn.addEventListener("click", logout);