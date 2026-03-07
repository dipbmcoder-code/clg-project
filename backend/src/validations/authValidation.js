const { validate, Joi } = require('../middlewares/validation');

const loginSchema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().required(),
});

const registerSchema = Joi.object({
    firstname: Joi.string().trim().min(1).max(100).required().messages({
        'string.empty': 'First name is required',
        'any.required': 'First name is required',
    }),
    lastname: Joi.string().trim().min(1).max(100).required().messages({
        'string.empty': 'Last name is required',
        'any.required': 'Last name is required',
    }),
    email: Joi.string().email().required().messages({
        'string.email': 'Must be a valid email address',
        'any.required': 'Email is required',
    }),
    password: Joi.string().min(6).max(128).required().messages({
        'string.min': 'Password must be at least 6 characters',
        'any.required': 'Password is required',
    }),
});

module.exports = {
    loginSchema,
    registerSchema,
};
