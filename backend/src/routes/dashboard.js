/**
 * Dashboard Stats Route.
 * GET /api/dashboard/stats
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// ─── GET /api/dashboard/stats ───
router.get('/stats', async (req, res) => {
  const client = await pool.connect();
  try {
    const stats = {};

    // Check if social_media_posts table exists
    const { rows: tableCheck } = await client.query(
      "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'social_media_posts') AS exists"
    );
    const postsTableExists = tableCheck[0].exists;

    // Total websites
    const { rows: wTotal } = await client.query('SELECT COUNT(*)::int AS count FROM websites');
    stats.total_websites = wTotal[0].count;

    // Active scrapers (active + social media enabled)
    const { rows: wActive } = await client.query(
      'SELECT COUNT(*)::int AS count FROM websites WHERE active = true AND (enable_social_media = true OR enable_reddit = true)'
    );
    stats.active_scrapers = wActive[0].count;

    if (postsTableExists) {
      // Posts scraped today
      const { rows: pToday } = await client.query(
        "SELECT COUNT(*)::int AS count FROM social_media_posts WHERE DATE(scraped_time) = CURRENT_DATE"
      );
      stats.posts_today = pToday[0].count;

      // Posts published today
      const { rows: pubToday } = await client.query(
        "SELECT COUNT(*)::int AS count FROM social_media_posts WHERE is_posted = true AND DATE(scraped_time) = CURRENT_DATE"
      );
      stats.published_today = pubToday[0].count;

      // Total posts ever
      const { rows: pTotal } = await client.query('SELECT COUNT(*)::int AS count FROM social_media_posts');
      stats.total_posts = pTotal[0].count;

      // Posts by source
      const { rows: bySource } = await client.query(
        "SELECT COALESCE(source, 'x') AS source, COUNT(*)::int AS count FROM social_media_posts GROUP BY source ORDER BY count DESC"
      );
      stats.posts_by_source = bySource;
    } else {
      stats.posts_today = 0;
      stats.published_today = 0;
      stats.total_posts = 0;
      stats.posts_by_source = [];
    }

    // Failures today
    const { rows: failToday } = await client.query(
      "SELECT COUNT(*)::int AS count FROM news_logs WHERE news_status = 'Failed' AND DATE(log_time) = CURRENT_DATE"
    );
    stats.failures_today = failToday[0].count;

    // Recent activity (last 10 logs)
    const { rows: recent } = await client.query(
      'SELECT * FROM news_logs ORDER BY log_time DESC LIMIT 10'
    );
    stats.recent_activity = recent.map((r) => ({ ...r, documentId: r.id }));

    return res.json({ data: stats });
  } catch (err) {
    console.error('GET /dashboard/stats error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  } finally {
    client.release();
  }
});

module.exports = router;
