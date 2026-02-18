const express = require('express');
const WebsiteController = require('../controllers/websiteController');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();

router.use(requireAuth);

router.get('/', WebsiteController.list);
router.get('/:id', WebsiteController.getOne);
router.post('/', WebsiteController.create);
router.put('/:id', WebsiteController.update);
router.delete('/:id', WebsiteController.delete);

module.exports = router;
