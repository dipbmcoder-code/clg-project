const router = require('express').Router();
const controller = require('../controllers/socialMedia.controller');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { socialMediaConfigSchema, socialMediaPostSchema } = require('../utils/schemas');

router.use(authenticate);

// Config management
router.get('/config/:websiteId', controller.getConfig);
router.put('/config/:websiteId', validate(socialMediaConfigSchema), controller.updateConfig);

// Posting
router.post('/post', validate(socialMediaPostSchema), controller.postToSocial);

// Post logs
router.get('/posts', controller.listPosts);
router.get('/posts/:websiteId', controller.listPostsByWebsite);

module.exports = router;
