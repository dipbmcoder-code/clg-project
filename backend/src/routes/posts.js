/**
 * Social Media Posts Routes.
 * GET /api/social-posts — list (paginated, filterable)
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// ─── GET /api/social-posts ───
router.get('/', async (req, res) => {
  try {
    // Check if table exists (created by Python scraper)
    const { rows: tableCheck } = await pool.query(
      "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'social_media_posts') AS exists"
    );
    if (!tableCheck[0].exists) {
      return res.json({
        results: [],
        pagination: { page: 1, pageSize: 25, total: 0, pageCount: 0 },
      });
    }

    const page = Math.max(1, parseInt(req.query.page, 10) || 1);
    const pageSize = Math.min(100, Math.max(1, parseInt(req.query.pageSize, 10) || 25));
    const sort = req.query.sort || 'scraped_time:desc';
    const search = req.query._q || '';

    const conditions = [];
    const params = [];
    let idx = 1;

    if (req.query.source) {
      conditions.push(`source = $${idx++}`);
      params.push(req.query.source);
    }
    if (req.query.is_posted !== undefined) {
      conditions.push(`is_posted = $${idx++}`);
      params.push(req.query.is_posted === 'true');
    }
    if (search) {
      conditions.push(`(post_title ILIKE $${idx} OR tweet_text ILIKE $${idx})`);
      params.push(`%${search}%`);
      idx++;
    }

    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';

    // Count
    const countRes = await pool.query(`SELECT COUNT(*)::int AS count FROM social_media_posts ${where}`, params);
    const total = countRes.rows[0].count;

    // Sort
    const [sortField, sortDir] = sort.split(':');
    const allowedFields = ['id', 'source', 'post_title', 'tweet_text', 'is_posted', 'scraped_time', 'score'];
    const safeField = allowedFields.includes(sortField) ? sortField : 'scraped_time';
    const safeDir = sortDir?.toLowerCase() === 'asc' ? 'ASC' : 'DESC';

    // Fetch
    const offset = (page - 1) * pageSize;
    const dataParams = [...params, pageSize, offset];
    const { rows } = await pool.query(
      `SELECT * FROM social_media_posts ${where} ORDER BY ${safeField} ${safeDir} LIMIT $${idx++} OFFSET $${idx++}`,
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
    console.error('GET /social-posts error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

module.exports = router;
