/**
 * JWT authentication middleware.
 * Verifies Bearer tokens and attaches user to req.
 */
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-change-me';

/**
 * Create a signed JWT token.
 */
function createToken(payload) {
  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '3d',
  });
}

/**
 * Verify and decode a JWT token.
 */
function verifyToken(token) {
  return jwt.verify(token, JWT_SECRET);
}

/**
 * Express middleware — require authentication.
 */
function requireAuth(req, res, next) {
  const header = req.headers.authorization || '';

  if (!header.startsWith('Bearer ')) {
    return res.status(401).json({ error: { status: 401, message: 'Missing auth token' } });
  }

  const token = header.slice(7).trim();

  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: { status: 401, message: 'Token expired' } });
    }
    return res.status(401).json({ error: { status: 401, message: 'Invalid token' } });
  }
}

module.exports = { createToken, verifyToken, requireAuth, JWT_SECRET };
