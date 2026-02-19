const router = require('express').Router();
const controller = require('../controllers/manualNews.controller');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { manualNewsSchema } = require('../utils/schemas');

router.use(authenticate);

router.get('/', controller.list);
router.get('/:id', controller.getOne);
router.post('/', validate(manualNewsSchema), controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.remove);

module.exports = router;
