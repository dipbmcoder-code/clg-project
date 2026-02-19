const router = require('express').Router();
const controller = require('../controllers/rapidapi.controller');
const { authenticate } = require('../middleware/auth');

router.use(authenticate);

router.get('/leagues', controller.getLeagues);
router.get('/players/profiles', controller.getPlayerProfiles);

module.exports = router;
