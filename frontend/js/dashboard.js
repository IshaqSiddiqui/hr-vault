
// ── dashboard.js ──────────────────────────────────────────────────

async function loadEmployees() {
  const tbody = document.getElementById("employeeBody");
  const errEl = document.getElementById("errorMsg");

  // Set nav user
  const user = getCurrentUser();
  const navUser = document.getElementById("navUser");
  if (navUser) navUser.textContent = `${user.name} (${user.role})`;

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
  // Phase 3: will check role
  // Phase 4: will trigger Auth0 step-up MFA if acr != 'mfa'
  try {
    const data = await apiFetch(`/employees/${empId}/sensitive`);
    alert(`Salary: $${Number(data.salary).toLocaleString()}\nNational ID: ${data.national_id}`);
  } catch (e) {
    alert(`Access denied: ${e.message}`);
  }
}

// Kick off on page load
loadEmployees();