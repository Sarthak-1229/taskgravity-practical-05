/**
 * Express Server-Side Validation Middleware
 * Supports express-validator rules with robust built-in fallback.
 */

let body, validationResult;
try {
  const ev = require('express-validator');
  body = ev.body;
  validationResult = ev.validationResult;
} catch (e) {
  // Graceful fallback if npm install hasn't been executed yet
}

const VALID_CATEGORIES = ['Frontend', 'Backend', 'Database', 'DevOps', 'Testing', 'UI/UX'];
const VALID_PRIORITIES = ['Low', 'Medium', 'High', 'Urgent'];

const taskValidationRules = () => {
  if (body) {
    return [
      body('title')
        .trim()
        .notEmpty().withMessage('Task title is required.')
        .isLength({ min: 3, max: 80 }).withMessage('Task title must be between 3 and 80 characters.'),

      body('category')
        .trim()
        .notEmpty().withMessage('Category is required.')
        .isIn(VALID_CATEGORIES).withMessage(`Category must be one of: ${VALID_CATEGORIES.join(', ')}.`),

      body('priority')
        .trim()
        .notEmpty().withMessage('Priority is required.')
        .isIn(VALID_PRIORITIES).withMessage(`Priority must be one of: ${VALID_PRIORITIES.join(', ')}.`),

      body('dueDate')
        .notEmpty().withMessage('Target deadline date is required.')
        .isISO8601().withMessage('Invalid deadline date format (YYYY-MM-DD required).')
        .custom((val) => {
          const d = new Date(val);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          if (d < today) {
            throw new Error('Deadline cannot be scheduled in the past.');
          }
          return true;
        }),

      body('estimatedHours')
        .notEmpty().withMessage('Estimated effort (hours) is required.')
        .isFloat({ min: 0.5, max: 100 }).withMessage('Effort must be a numeric value between 0.5 and 100 hours.'),

      body('description')
        .optional({ checkFalsy: true })
        .trim()
        .isLength({ max: 300 }).withMessage('Scope description cannot exceed 300 characters.')
    ];
  }

  // Built-in Pure Middleware Fallback
  return [(req, res, next) => next()];
};

// Validation Result Middleware Handler
const validate = (req, res, next) => {
  if (validationResult) {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      const formattedErrors = {};
      errors.array().forEach(err => {
        if (!formattedErrors[err.path]) {
          formattedErrors[err.path] = err.msg;
        }
      });

      return res.status(400).json({
        success: false,
        message: 'Validation failed on server.',
        errors: formattedErrors
      });
    }
    return next();
  }

  // Pure JS validation fallback
  const { title, category, priority, dueDate, estimatedHours, description } = req.body;
  const errors = {};

  if (!title || title.trim().length < 3 || title.trim().length > 80) {
    errors.title = 'Task title must be between 3 and 80 characters.';
  }
  if (!category || !VALID_CATEGORIES.includes(category)) {
    errors.category = 'Valid category selection required.';
  }
  if (!priority || !VALID_PRIORITIES.includes(priority)) {
    errors.priority = 'Valid priority selection required.';
  }
  if (!dueDate || isNaN(new Date(dueDate).getTime())) {
    errors.dueDate = 'Valid deadline date required.';
  } else {
    const d = new Date(dueDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (d < today) errors.dueDate = 'Deadline cannot be in the past.';
  }
  const h = Number(estimatedHours);
  if (isNaN(h) || h < 0.5 || h > 100) {
    errors.estimatedHours = 'Effort must be between 0.5 and 100 hours.';
  }
  if (description && description.length > 300) {
    errors.description = 'Description cannot exceed 300 characters.';
  }

  if (Object.keys(errors).length > 0) {
    return res.status(400).json({
      success: false,
      message: 'Validation failed on server.',
      errors
    });
  }

  next();
};

module.exports = {
  taskValidationRules,
  validate
};
