/**
 * AI Settings Routes — single-record get/update.
 * GET  /api/ai-settings
 * PUT  /api/ai-settings
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// Fields allowed in updates (whitelist to prevent injection)
const ALLOWED_FIELDS = [
  'content_provider', 'content_api_key', 'content_model', 'content_base_url',
  'content_temperature', 'content_max_tokens',
  'image_provider', 'image_api_key', 'image_model',
  'aws_access_key_id', 'aws_secret_access_key', 'aws_s3_bucket', 'aws_region', 'aws_url',
  'sendgrid_api_key', 'sender_email',
];

// Mask sensitive fields for API responses
function maskSecrets(row) {
  if (!row) return row;
  const masked = { ...row };
  const secretFields = ['content_api_key', 'image_api_key', 'aws_access_key_id', 'aws_secret_access_key', 'sendgrid_api_key'];
  for (const f of secretFields) {
    if (masked[f]) {
      const val = masked[f];
      masked[f] = val.length > 8 ? val.slice(0, 4) + '••••' + val.slice(-4) : '••••••••';
    }
  }
  return masked;
}

// ─── GET /api/ai-settings ───
router.get('/', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM ai_settings ORDER BY id LIMIT 1');
    if (rows.length === 0) {
      return res.json({ data: {} });
    }
    return res.json({ data: { ...maskSecrets(rows[0]), documentId: rows[0].id } });
  } catch (err) {
    console.error('GET /ai-settings error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── PUT /api/ai-settings ───
router.put('/', async (req, res) => {
  try {
    const b = req.body;
    const { rows: existing } = await pool.query('SELECT id FROM ai_settings ORDER BY id LIMIT 1');

    // Build dynamic SET clause from allowed fields only
    const setClauses = [];
    const values = [];
    let idx = 1;

    for (const field of ALLOWED_FIELDS) {
      if (b[field] !== undefined) {
        // Skip masked values (don't overwrite with mask)
        if (typeof b[field] === 'string' && b[field].includes('••••')) continue;

        setClauses.push(`${field} = $${idx++}`);
        values.push(b[field] === '' ? null : b[field]);
      }
    }

    let result;
    if (existing.length > 0) {
      if (setClauses.length === 0) {
        return res.json({ data: { ...maskSecrets(existing[0]), documentId: existing[0].id } });
      }
      values.push(existing[0].id);
      const { rows } = await pool.query(
        `UPDATE ai_settings SET ${setClauses.join(', ')}, updated_at = NOW() WHERE id = $${idx} RETURNING *`,
        values
      );
      result = rows[0];
    } else {
      // Insert new row with provided values
      const insertFields = [];
      const insertPlaceholders = [];
      const insertValues = [];
      let iIdx = 1;

      for (const field of ALLOWED_FIELDS) {
        if (b[field] !== undefined && !(typeof b[field] === 'string' && b[field].includes('••••'))) {
          insertFields.push(field);
          insertPlaceholders.push(`$${iIdx++}`);
          insertValues.push(b[field] === '' ? null : b[field]);
        }
      }

      const q = insertFields.length > 0
        ? `INSERT INTO ai_settings (${insertFields.join(',')}) VALUES (${insertPlaceholders.join(',')}) RETURNING *`
        : 'INSERT INTO ai_settings DEFAULT VALUES RETURNING *';

      const { rows } = await pool.query(q, insertValues);
      result = rows[0];
    }

    return res.json({ data: { ...maskSecrets(result), documentId: result.id } });
  } catch (err) {
    console.error('PUT /ai-settings error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

module.exports = router;
