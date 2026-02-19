const CryptoJS = require('crypto-js');

const SECRET_KEY = process.env.PASSWORD_SECRET_KEY;

/**
 * Encrypt a string using AES-256
 */
const encrypt = (text) => {
  return CryptoJS.AES.encrypt(text, SECRET_KEY).toString();
};

/**
 * Decrypt an AES-256 encrypted string
 */
const decrypt = (ciphertext) => {
  const bytes = CryptoJS.AES.decrypt(ciphertext, SECRET_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
};

/**
 * Build pagination params from query
 */
const getPagination = (query) => {
  const page = Math.max(1, parseInt(query.page) || 1);
  const pageSize = Math.min(100, Math.max(1, parseInt(query.pageSize) || 25));
  const skip = (page - 1) * pageSize;
  return { skip, take: pageSize, page, pageSize };
};

/**
 * Format paginated response
 */
const paginatedResponse = (data, total, pagination) => ({
  data,
  meta: {
    pagination: {
      page: pagination.page,
      pageSize: pagination.pageSize,
      pageCount: Math.ceil(total / pagination.pageSize),
      total,
    },
  },
});

module.exports = { encrypt, decrypt, getPagination, paginatedResponse };
