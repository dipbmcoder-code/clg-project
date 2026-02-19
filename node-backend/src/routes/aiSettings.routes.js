const router = require('express').Router();
const controller = require('../controllers/aiSettings.controller');
const { authenticate, authorize } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { aiSettingsSchema } = require('../utils/schemas');

router.use(authenticate);

router.get('/', controller.get);
router.put('/', authorize('SUPER_ADMIN', 'ADMIN'), validate(aiSettingsSchema), controller.update);
router.post('/test/:provider', authorize('SUPER_ADMIN', 'ADMIN'), controller.testConnection);

module.exports = router;
