/**
 * News Prompts Routes — single-record get/update.
 * GET /api/news-prompts
 * PUT /api/news-prompts
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// ─── GET /api/news-prompts ───
router.get('/', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM news_prompts ORDER BY id LIMIT 1');
    if (rows.length === 0) {
      return res.json({ data: {} });
    }
    const prompts = rows[0];
    return res.json({ data: { ...prompts, documentId: prompts.id } });
  } catch (err) {
    console.error('GET /news-prompts error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── PUT /api/news-prompts ───
router.put('/', async (req, res) => {
  try {
    const b = req.body;

    // Check if record exists
    const { rows: existing } = await pool.query('SELECT id FROM news_prompts ORDER BY id LIMIT 1');

    let result;
    if (existing.length > 0) {
      const { rows } = await pool.query(
        `UPDATE news_prompts SET
          social_media_news_title_prompt = COALESCE($1, social_media_news_title_prompt),
          social_media_news_image_prompt = COALESCE($2, social_media_news_image_prompt),
          social_media_news_content_prompt = COALESCE($3, social_media_news_content_prompt),
          ai_tone = COALESCE($4, ai_tone),
          ai_language = COALESCE($5, ai_language),
          ai_max_words = COALESCE($6, ai_max_words),
          updated_at = NOW()
        WHERE id = $7
        RETURNING *`,
        [
          b.social_media_news_title_prompt,
          b.social_media_news_image_prompt,
          b.social_media_news_content_prompt,
          b.ai_tone,
          b.ai_language,
          b.ai_max_words !== undefined ? parseInt(b.ai_max_words, 10) || null : null,
          existing[0].id,
        ]
      );
      result = rows[0];
    } else {
      const { rows } = await pool.query(
        `INSERT INTO news_prompts (
          social_media_news_title_prompt,
          social_media_news_image_prompt,
          social_media_news_content_prompt,
          ai_tone, ai_language, ai_max_words
        ) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
        [
          b.social_media_news_title_prompt,
          b.social_media_news_image_prompt,
          b.social_media_news_content_prompt,
          b.ai_tone || null,
          b.ai_language || 'English',
          b.ai_max_words ? parseInt(b.ai_max_words, 10) : 500,
        ]
      );
      result = rows[0];
    }

    return res.json({ data: { ...result, documentId: result.id } });
  } catch (err) {
    console.error('PUT /news-prompts error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

module.exports = router;
