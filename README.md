# Practical 05: ExpressJS Web Application with Server-Side Validation

## TaskGravity — Express.js Framework, Middleware Chains, express-validator, and Dynamic Response Handling

### 1. Overview
Practical 05 develops the TaskGravity platform using the industry-standard Express.js framework, demonstrating middleware composition, robust input validation chains, and structured REST responses.

### 2. Architecture & Middleware Pipeline
- **Express.js Framework**: Modern routing architecture (`GET`, `POST`, `PATCH`, `DELETE`).
- **Validation Middleware (`validators/taskValidator.js`)**:
  - Implements `express-validator` schema rules with pure JavaScript fallback if dependencies are uninstalled.
  - Validates `title` (3-80 chars), `category` whitelist, `priority` whitelist, `dueDate` (ISO8601 & future date verification), and `estimatedHours` (0.5 to 100).
- **RESTful Endpoints**:
  - `GET /api/tasks`: List all tasks with optional query filters.
  - `GET /api/tasks/:id`: Retrieve single task by ID.
  - `POST /api/tasks`: Validates body and creates a task with HTTP 201 Created.
  - `PATCH /api/tasks/:id/status`: Updates/cycles task status.
  - `DELETE /api/tasks/:id`: Removes task by ID.
  - `GET /api/stats`: Dynamic KPI aggregation.
- **Frontend Client**: Minimalist, flat TaskGravity interface communicating via Fetch API.

### 3. Execution
```bash
cd Practical5
npm install
npm start
```
Server boots on `http://localhost:5000`.
