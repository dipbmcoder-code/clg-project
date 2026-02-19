const router = require('express').Router();
const controller = require('../controllers/website.controller');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { websiteSchema, websiteUpdateSchema } = require('../utils/schemas');

router.use(authenticate);

router.get('/', controller.list);
router.get('/:id', controller.getOne);
router.post('/', validate(websiteSchema), controller.create);
router.put('/:id', validate(websiteUpdateSchema), controller.update);
router.delete('/:id', controller.remove);
router.post('/:id/validate', controller.validateConnection);

module.exports = router;
