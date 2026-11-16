/**
 * Practical 05: ExpressJS Task Management Application with Server-Side Validation
 */

require('dotenv').config();
const express = require('express');
const path = require('path');
const cors = require('cors');
const { taskValidationRules, validate } = require('./validators/taskValidator');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// In-Memory Task Repository
let tasks = [
  {
    id: 'tg-exp-101',
    title: 'Express Route Handler Standardization',
    category: 'Backend',
    priority: 'High',
    dueDate: '2026-11-20',
    estimatedHours: 4,
    description: 'Implement RESTful request routing with consistent JSON error envelopes.',
    status: 'in-progress',
    createdAt: new Date().toISOString()
  },
  {
    id: 'tg-exp-102',
    title: 'express-validator Middleware Integration',
    category: 'Backend',
    priority: 'Urgent',
    dueDate: '2026-11-22',
    estimatedHours: 6,
    description: 'Bind validation chains to POST and PUT requests for input sanitization.',
    status: 'pending',
    createdAt: new Date().toISOString()
  },
  {
    id: 'tg-exp-103',
    title: 'Client-Side Real-Time Toast Notifications',
    category: 'Frontend',
    priority: 'Medium',
    dueDate: '2026-11-24',
    estimatedHours: 3,
    description: 'Render responsive feedback alerts for asynchronous Express server responses.',
    status: 'completed',
    createdAt: new Date().toISOString()
  }
];

// ==========================================
// ROUTES
// ==========================================

// GET /api/tasks - Retrieve all tasks (with optional filter)
app.get('/api/tasks', (req, res) => {
  const { status, category, search } = req.query;
  let filtered = [...tasks];

  if (status && status !== 'all') {
    filtered = filtered.filter(t => t.status === status);
  }
  if (category && category !== 'all') {
    filtered = filtered.filter(t => t.category === category);
  }
  if (search) {
    const q = search.toLowerCase();
    filtered = filtered.filter(t => t.title.toLowerCase().includes(q) || (t.description || '').toLowerCase().includes(q));
  }

  res.status(200).json({
    success: true,
    count: filtered.length,
    data: filtered
  });
});

// GET /api/tasks/:id - Retrieve single task
app.get('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) {
    return res.status(404).json({
      success: false,
      message: `Task with id '${req.params.id}' was not found.`
    });
  }
  res.status(200).json({ success: true, data: task });
});

// POST /api/tasks - Create task with validation chain
app.post('/api/tasks', taskValidationRules(), validate, (req, res) => {
  const { title, category, priority, dueDate, estimatedHours, description } = req.body;

  const newTask = {
    id: 'tg-exp-' + Date.now().toString().slice(-4),
    title: title.trim(),
    category,
    priority,
    dueDate,
    estimatedHours: Number(estimatedHours),
    description: (description || '').trim(),
    status: 'pending',
    createdAt: new Date().toISOString()
  };

  tasks.unshift(newTask);

  res.status(201).json({
    success: true,
    message: 'Task validated and created successfully by Express server.',
    data: newTask
  });
});

// PATCH /api/tasks/:id/status - Toggle/Update task status
app.patch('/api/tasks/:id/status', (req, res) => {
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) {
    return res.status(404).json({ success: false, message: 'Task not found' });
  }

  const { status } = req.body;
  const validStatuses = ['pending', 'in-progress', 'completed'];

  if (status && validStatuses.includes(status)) {
    task.status = status;
  } else {
    // Cycle automatically
    task.status = task.status === 'pending'
      ? 'in-progress'
      : task.status === 'in-progress'
        ? 'completed'
        : 'pending';
  }

  res.status(200).json({
    success: true,
    message: `Task status updated to '${task.status}'`,
    data: task
  });
});

// DELETE /api/tasks/:id - Delete a task
app.delete('/api/tasks/:id', (req, res) => {
  const index = tasks.findIndex(t => t.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ success: false, message: 'Task not found' });
  }

  const removed = tasks.splice(index, 1)[0];
  res.status(200).json({
    success: true,
    message: `Task '${removed.title}' removed successfully.`,
    data: removed
  });
});

// GET /api/stats - Aggregated Metrics
app.get('/api/stats', (req, res) => {
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'completed').length;
  const inProgress = tasks.filter(t => t.status === 'in-progress').length;
  const pending = tasks.filter(t => t.status === 'pending').length;

  res.status(200).json({
    success: true,
    stats: {
      total,
      completed,
      inProgress,
      pending,
      velocity: total > 0 ? Math.round((completed / total) * 100) : 0
    }
  });
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('[Express Error]', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: err.message
  });
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`[TaskGravity Express Server] Running on http://localhost:${PORT}`);
  });
}

module.exports = app;
