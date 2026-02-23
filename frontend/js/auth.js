// ── auth.js ───────────────────────────────────────────────────────
// Phase 1: stub — Phase 2 will replace with Auth0 SDK

function getCurrentUser() {
  // Phase 2: return decoded JWT claims from Auth0
  return { name: "Guest", role: "guest" };
}

const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.addEventListener("click", () => {
    // Phase 2: auth0Client.loginWithRedirect()
    window.location.href = "dashboard.html";
  });
}