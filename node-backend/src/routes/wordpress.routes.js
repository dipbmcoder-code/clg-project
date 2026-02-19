const router = require('express').Router();
const controller = require('../controllers/wordpress.controller');
const { authenticate } = require('../middleware/auth');

router.use(authenticate);

router.get('/:websiteId/categories', controller.getCategories);
router.post('/:websiteId/sync-categories', controller.syncCategories);
router.get('/:websiteId/health', controller.healthCheck);
router.get('/:websiteId/posts', controller.getRecentPosts);

module.exports = router;
