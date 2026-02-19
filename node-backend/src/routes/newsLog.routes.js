const router = require('express').Router();
const controller = require('../controllers/newsLog.controller');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { newsLogSchema } = require('../utils/schemas');

router.use(authenticate);

router.get('/', controller.list);
router.post('/', validate(newsLogSchema), controller.create);

module.exports = router;
