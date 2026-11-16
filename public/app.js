/**
 * Practical 05: Frontend Client for ExpressJS Task Application
 */

const form = document.getElementById('expressTaskForm');
const alertSuccess = document.getElementById('alertSuccess');
const alertDanger = document.getElementById('alertDanger');
const taskListContainer = document.getElementById('taskList');

const statTotal = document.getElementById('statTotal');
const statInProgress = document.getElementById('statInProgress');
const statPending = document.getElementById('statPending');
const statVelocity = document.getElementById('statVelocity');

const errorFields = ['title', 'category', 'priority', 'dueDate', 'estimatedHours', 'description'];

document.addEventListener('DOMContentLoaded', () => {
  fetchTasks();
  fetchStats();
});

async function fetchTasks() {
  try {
    const res = await fetch('/api/tasks');
    const json = await res.json();
    if (json.success) {
      renderTasks(json.data);
    }
  } catch (err) {
    console.error('Failed to load tasks from Express server:', err);
  }
}

async function fetchStats() {
  try {
    const res = await fetch('/api/stats');
    const json = await res.json();
    if (json.success && json.stats) {
      statTotal.textContent = json.stats.total;
      statInProgress.textContent = json.stats.inProgress;
      statPending.textContent = json.stats.pending;
      statVelocity.textContent = `${json.stats.velocity}%`;
    }
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

function clearErrors() {
  errorFields.forEach(f => {
    const el = document.getElementById(`err_${f}`);
    if (el) {
      el.textContent = '';
      el.classList.remove('visible');
    }
    const input = document.getElementById(f === 'estimatedHours' ? 'taskHours' : `task${f.charAt(0).toUpperCase() + f.slice(1)}`);
    if (input) input.classList.remove('is-invalid');
  });
  alertDanger.style.display = 'none';
  alertSuccess.style.display = 'none';
}

function showErrors(errors) {
  Object.keys(errors).forEach(key => {
    const errorEl = document.getElementById(`err_${key}`);
    const inputId = key === 'estimatedHours' ? 'taskHours' : `task${key.charAt(0).toUpperCase() + key.slice(1)}`;
    const inputEl = document.getElementById(inputId);

    if (errorEl) {
      errorEl.textContent = errors[key];
      errorEl.classList.add('visible');
    }
    if (inputEl) {
      inputEl.classList.add('is-invalid');
    }
  });

  alertDanger.textContent = 'Server-side validation failed. Please address the errors highlighted.';
  alertDanger.style.display = 'block';
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearErrors();

  const payload = {
    title: document.getElementById('taskTitle').value,
    category: document.getElementById('taskCategory').value,
    priority: document.getElementById('taskPriority').value,
    dueDate: document.getElementById('taskDueDate').value,
    estimatedHours: document.getElementById('taskHours').value,
    description: document.getElementById('taskDesc').value
  };

  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (res.status === 201 && result.success) {
      alertSuccess.textContent = `Success (HTTP 201): "${result.data.title}" saved via Express middleware.`;
      alertSuccess.style.display = 'block';
      form.reset();
      fetchTasks();
      fetchStats();
      setTimeout(() => { alertSuccess.style.display = 'none'; }, 4000);
    } else if (res.status === 400 && result.errors) {
      showErrors(result.errors);
    } else {
      alertDanger.textContent = result.message || 'Error occurred.';
      alertDanger.style.display = 'block';
    }
  } catch (err) {
    alertDanger.textContent = 'Connection error: ' + err.message;
    alertDanger.style.display = 'block';
  }
});

async function cycleStatus(id) {
  try {
    const res = await fetch(`/api/tasks/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' }
    });
    if (res.ok) {
      fetchTasks();
      fetchStats();
    }
  } catch (err) {
    console.error('Failed to cycle status:', err);
  }
}

async function deleteTask(id) {
  if (!confirm('Are you sure you want to remove this task?')) return;
  try {
    const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    if (res.ok) {
      fetchTasks();
      fetchStats();
    }
  } catch (err) {
    console.error('Failed to delete task:', err);
  }
}

function renderTasks(tasks) {
  if (!tasks || tasks.length === 0) {
    taskListContainer.innerHTML = `
      <div style="text-align: center; padding: 2rem; background: #fff; border: 1px dashed #e2e8f0; border-radius: 6px; color: #64748b;">
        No active tasks found in Express registry.
      </div>
    `;
    return;
  }

  taskListContainer.innerHTML = tasks.map(t => {
    const priorityClass = `badge-${t.priority.toLowerCase()}`;
    const statusClass = `badge-${t.status}`;
    return `
      <article class="task-card">
        <div class="task-header">
          <span class="task-title">${escapeHTML(t.title)}</span>
          <div style="display: flex; gap: 4px;">
            <span class="badge ${priorityClass}">${t.priority}</span>
            <span class="badge ${statusClass}">${t.status}</span>
          </div>
        </div>
        ${t.description ? `<p class="task-desc">${escapeHTML(t.description)}</p>` : ''}
        <div class="task-meta">
          <div>
            <span class="badge badge-category">${t.category}</span>
            <span style="margin-left: 8px;">Due: <strong>${t.dueDate}</strong></span>
            <span style="margin-left: 8px;">Est: <strong>${t.estimatedHours}h</strong></span>
          </div>
          <div style="display: flex; gap: 4px;">
            <button class="btn btn-secondary btn-sm" onclick="cycleStatus('${t.id}')">Cycle Status</button>
            <button class="btn btn-sm" style="background: transparent; color: #dc2626;" onclick="deleteTask('${t.id}')">Delete</button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
