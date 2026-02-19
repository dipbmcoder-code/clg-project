const router = require('express').Router();
const authController = require('../controllers/auth.controller');
const { authenticate } = require('../middleware/auth');
const { authLimiter } = require('../middleware/rateLimiter');
const { validate } = require('../middleware/validate');
const { loginSchema, registerSchema } = require('../utils/schemas');

router.post('/login', authLimiter, validate(loginSchema), authController.login);
router.get('/me', authenticate, authController.me);
router.post('/register', authenticate, validate(registerSchema), authController.register);
router.get('/users', authenticate, authController.listUsers);
router.put('/users/:id', authenticate, authController.updateUser);
router.delete('/users/:id', authenticate, authController.deleteUser);

module.exports = router;
