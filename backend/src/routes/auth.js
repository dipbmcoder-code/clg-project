const express = require('express');
const AuthController = require('../controllers/authController');
const { requireAuth } = require('../middlewares/auth');
const { validate } = require('../middlewares/validation');
const { loginSchema, registerSchema } = require('../validations/authValidation');

const router = express.Router();

router.post('/login', validate(loginSchema), AuthController.login);
router.post('/register', validate(registerSchema), AuthController.register);
router.get('/me', requireAuth, AuthController.me);

module.exports = router;
