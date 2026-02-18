const crypto = require('crypto');

/**
 * Hash a password using SHA-256 (existing logic).
 * Consider upgrading to bcrypt in future.
 * @param {string} password 
 * @returns {string} Hashed password
 */
function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

module.exports = {
    hashPassword,
};
