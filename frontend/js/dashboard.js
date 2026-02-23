// ── dashboard.js ──────────────────────────────────────────────────

async function loadEmployees() {
  const tbody = document.getElementById("employeeBody");
  const errEl = document.getElementById("errorMsg");

  // Init Auth0 — this will redirect to login if not authenticated
  const isAuthenticated = await initAuth0();

  // If initAuth0 triggered a redirect, stop here
  if (!isAuthenticated) return;

  // Set nav user from real Auth0 identity
  try {
    const user = await getCurrentUser();
    const navUser = document.getElementById("navUser");
    if (navUser) navUser.textContent = `${user.name} (${user.role})`;
  } catch (e) {
    console.error("Could not get user:", e);
  }

  // Fetch employees with JWT attached
  try {
    const employees = await apiFetch("/employees/");
    tbody.innerHTML = "";

    employees.forEach(emp => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${emp.id}</td>
        <td>${emp.name}</td>
        <td>${emp.email}</td>
        <td>${emp.department}</td>
        <td><span class="badge badge-${emp.role}">${emp.role.replace("_", " ")}</span></td>
        <td>
          <button class="btn btn-sm" onclick="viewSensitive(${emp.id})">
            View Sensitive 🔒
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    errEl.textContent = `Failed to load employees: ${e.message}`;
    errEl.classList.remove("hidden");
    tbody.innerHTML = `<tr><td colspan="6" class="loading">Error loading data.</td></tr>`;
  }
}

async function viewSensitive(empId) {
  try {
    const data = await apiFetch(`/employees/${empId}/sensitive`);
    alert(`Salary: $${Number(data.salary).toLocaleString()}\nNational ID: ${data.national_id}`);
  } catch (e) {
    alert(`Access denied: ${e.message}`);
  }
}

loadEmployees();