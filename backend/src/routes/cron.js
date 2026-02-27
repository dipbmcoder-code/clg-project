/**
 * Cron Settings & Trigger Routes.
 * GET  /api/cron/settings       — get cron config + status
 * PUT  /api/cron/settings       — update cron config
 * POST /api/cron/trigger        — manually trigger the pipeline
 * GET  /api/cron/history        — recent cron run history from news_logs
 */
const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');
const logger = require('../config/logger');

const router = express.Router();
router.use(requireAuth);

// Track manual trigger in-memory (prevents multiple simultaneous triggers)
let triggerProcess = null;

// ─── GET /api/cron/settings ───
router.get('/settings', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM cron_settings ORDER BY id LIMIT 1');
    if (rows.length === 0) {
      // Return defaults if no settings exist
      return res.json({
        data: {
          cron_enabled: true,
          cron_interval_minutes: 60,
          is_running: false,
          total_runs: 0,
          total_success: 0,
          total_failures: 0,
        },
      });
    }
    const settings = rows[0];
    return res.json({ data: { ...settings, documentId: settings.id } });
  } catch (err) {
    console.error('GET /cron/settings error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── PUT /api/cron/settings ───
router.put('/settings', async (req, res) => {
  try {
    const { cron_enabled, cron_interval_minutes } = req.body;
    const { rows: existing } = await pool.query('SELECT id FROM cron_settings ORDER BY id LIMIT 1');

    let result;
    if (existing.length > 0) {
      const { rows } = await pool.query(
        `UPDATE cron_settings SET
          cron_enabled = COALESCE($1, cron_enabled),
          cron_interval_minutes = COALESCE($2, cron_interval_minutes),
          updated_at = NOW()
        WHERE id = $3 RETURNING *`,
        [cron_enabled, cron_interval_minutes, existing[0].id]
      );
      result = rows[0];
    } else {
      const { rows } = await pool.query(
        `INSERT INTO cron_settings (cron_enabled, cron_interval_minutes)
         VALUES ($1, $2) RETURNING *`,
        [cron_enabled ?? true, cron_interval_minutes ?? 60]
      );
      result = rows[0];
    }

    return res.json({ data: { ...result, documentId: result.id } });
  } catch (err) {
    console.error('PUT /cron/settings error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── POST /api/cron/trigger ───
router.post('/trigger', async (req, res) => {
  try {
    // Check if already running
    if (triggerProcess) {
      return res.status(409).json({
        error: { status: 409, message: 'Pipeline is already running. Wait for it to finish.' },
      });
    }

    // Mark as running in DB
    await pool.query(
      `UPDATE cron_settings SET is_running = true, updated_at = NOW()
       WHERE id = (SELECT id FROM cron_settings ORDER BY id LIMIT 1)`
    );

    const newsEnginePath = path.resolve(__dirname, '../../../news-engine');
    const pythonScript = path.join(newsEnginePath, 'social_media/main_social_media.py');

    // Detect python executable (venv or system)
    const venvPython = path.join(newsEnginePath, '.venv/bin/python3');
    const pythonCmd = require('fs').existsSync(venvPython) ? venvPython : 'python3';

    logger.info(`🔄 Manual trigger: ${pythonCmd} ${pythonScript}`);

    const startTime = Date.now();

    triggerProcess = exec(
      `cd "${newsEnginePath}" && "${pythonCmd}" "${pythonScript}"`,
      {
        cwd: newsEnginePath,
        timeout: 3600000, // 1 hour
        maxBuffer: 10 * 1024 * 1024, // 10MB
        env: { ...process.env, PYTHONUNBUFFERED: '1' },
      },
      async (error, stdout, stderr) => {
        const durationSec = Math.round((Date.now() - startTime) / 1000);
        const status = error ? 'failed' : 'success';
        const message = error
          ? (error.killed ? 'Timed out after 1 hour' : error.message)
          : `Completed in ${durationSec}s`;

        try {
          await pool.query(
            `UPDATE cron_settings SET
              is_running = false,
              last_run_at = NOW(),
              last_run_status = $1,
              last_run_message = $2,
              last_run_duration_sec = $3,
              total_runs = total_runs + 1,
              total_success = total_success + $4,
              total_failures = total_failures + $5,
              updated_at = NOW()
            WHERE id = (SELECT id FROM cron_settings ORDER BY id LIMIT 1)`,
            [status, message, durationSec, status === 'success' ? 1 : 0, status === 'failed' ? 1 : 0]
          );
        } catch (dbErr) {
          logger.error('Failed to update cron_settings after run:', dbErr);
        }

        if (stdout) logger.info(`Pipeline stdout:\n${stdout.slice(-2000)}`);
        if (stderr) logger.warn(`Pipeline stderr:\n${stderr.slice(-1000)}`);

        triggerProcess = null;
      }
    );

    return res.json({
      data: {
        message: 'Pipeline triggered successfully',
        status: 'running',
        triggered_at: new Date().toISOString(),
      },
    });
  } catch (err) {
    triggerProcess = null;
    console.error('POST /cron/trigger error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

// ─── GET /api/cron/history ───
router.get('/history', async (req, res) => {
  try {
    const limit = Math.min(50, parseInt(req.query.limit, 10) || 20);
    const { rows } = await pool.query(
      `SELECT id, news_type, title, website_name, image_generated, news_status, log_time, created_at
       FROM news_logs ORDER BY log_time DESC LIMIT $1`,
      [limit]
    );
    return res.json({ data: rows });
  } catch (err) {
    console.error('GET /cron/history error:', err);
    return res.status(500).json({ error: { status: 500, message: err.message } });
  }
});

module.exports = router;
