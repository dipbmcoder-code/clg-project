const Joi = require('joi');

const createUserSchema = Joi.object({
    firstname: Joi.string().allow('', null),
    lastname: Joi.string().allow('', null),
    email: Joi.string().email().required(),
    password: Joi.string().min(6).required(),
    role: Joi.string().valid('Admin', 'Editor', 'Author').allow(null),
    roles: Joi.any().allow(null), // For frontend compatibility
    is_active: Joi.boolean().default(true),
});

const updateUserSchema = Joi.object({
    firstname: Joi.string().allow('', null),
    lastname: Joi.string().allow('', null),
    email: Joi.string().email(),
    password: Joi.string().min(6).allow(null, ''),
    role: Joi.string().valid('Admin', 'Editor', 'Author').allow(null),
    roles: Joi.any().allow(null),
    is_active: Joi.boolean(),
    isActive: Joi.boolean(), // For frontend compatibility
});

module.exports = {
    createUserSchema,
    updateUserSchema,
};
