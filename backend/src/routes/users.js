const express = require('express');
const UserController = require('../controllers/userController');
const { requireAuth } = require('../middlewares/auth');
const { validate } = require('../middlewares/validation');
const { createUserSchema, updateUserSchema } = require('../validations/userValidation');

const router = express.Router();
router.use(requireAuth);

router.get('/roles/list', async (_req, res) => {
  return res.json({
    data: [
      { id: 2, name: 'Admin' },
      { id: 3, name: 'Editor' },
    ],
  });
});

router.get('/', UserController.list);
router.get('/:id', UserController.getOne);
router.post('/', validate(createUserSchema), UserController.create);
router.put('/:id', validate(updateUserSchema), UserController.update);
router.delete('/:id', UserController.delete);

module.exports = router;
