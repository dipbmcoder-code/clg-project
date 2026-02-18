const { validate, Joi } = require('../middlewares/validation');

const loginSchema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().required(),
});

module.exports = {
    loginSchema,
};
