const Joi = require('joi');

const validate = (schema) => {
    return (req, res, next) => {
        const { error } = schema.validate(req.body, { abortEarly: false });
        if (error) {
            const messages = error.details.map((detail) => detail.message);
            return res.status(400).json({ error: { status: 400, message: 'Validation Error', details: messages } });
        }
        next();
    };
};

module.exports = { validate, Joi };
