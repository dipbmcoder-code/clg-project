const router = require('express').Router();
const controller = require('../controllers/newsPrompt.controller');
const { authenticate } = require('../middleware/auth');

router.use(authenticate);

router.get('/', controller.get);
router.put('/', controller.update);

module.exports = router;
