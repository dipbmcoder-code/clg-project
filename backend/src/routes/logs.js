/**
 * News Logs Routes.
 * GET /api/news-logs      — list (paginated)
 * GET /api/news-logs/:id  — single log detail
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// ─── GET /api/news-logs ───
router.get('/', async (req, res) => {
  try {
    const page = Math.max(1, parseInt(req.query.page, 10) || 1);
    const pageSize = Math.min(100, Math.max(1, parseInt(req.query.pageSize, 10) || 25));
    const sort = req.query.sort || 'log_time:desc';
    const search = req.query._q || '';

    const conditions = [];
    const params = [];
    let idx = 1;

    if (req.query.news_type) {
      conditions.push(`news_type = $${idx++}`);
      params.push(req.query.news_type);
    }
    if (req.query.news_status) {
      conditions.push(`news_status = $${idx++}`);
      params.push(req.query.news_status);
    }
    if (search) {
      conditions.push(`(title ILIKE $${idx} OR website_name ILIKE $${idx})`);
      params.push(`%${search}%`);
      idx++;
    }

    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';

    // Count
    const countRes = await pool.query(`SELECT COUNT(*)::int AS count FROM news_logs ${where}`, params);
    const total = countRes.rows[0].count;

    // Sort
    const [sortField, sortDir] = sort.split(':');
    const allowedFields = ['id', 'news_type', 'title', 'website_name', 'log_time', 'news_status', 'created_at'];
    const safeField = allowedFields.includes(sortField) ? sortField : 'log_time';
    const safeDir = sortDir?.toLowerCase() === 'asc' ? 'ASC' : 'DESC';

    // Fetch
    const offset = (page - 1) * pageSize;
    const dataParams = [...params, pageSize, offset];
    const { rows } = await pool.query(
      `SELECT * FROM news_logs ${where} ORDER BY ${safeField} ${safeDir} LIMIT $${idx++} OFFSET $${idx++}`,
      dataParams
    );

    const results = rows.map((r) => ({ ...r, documentId: r.id }));

    return res.json({
      results,
      pagination: {
        page,
        pageSize,
        total,
        pageCount: Math.ceil(total / pageSize),
      },
    });
  } catch (err) {
    console.error('GET /news-logs error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── GET /api/news-logs/:id ───
router.get('/:id', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM news_logs WHERE id = $1', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: { status: 404, message: 'Log not found' } });
    }
    const log = rows[0];
    return res.json({ data: { ...log, documentId: log.id } });
  } catch (err) {
    console.error('GET /news-logs/:id error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

module.exports = router;
