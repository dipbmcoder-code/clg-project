/**
 * WordPress Integration Routes.
 *
 * Communicates with remote WordPress sites via the WP REST API
 * using Application Passwords (WordPress 5.6+).
 *
 * POST /api/wordpress/validate     — validate WP credentials
 * GET  /api/wordpress/categories   — fetch categories from a WP site
 * GET  /api/wordpress/authors      — fetch authors from a WP site
 * POST /api/wordpress/publish      — publish a post to a WP site
 */
const express = require('express');
const pool = require('../config/db');
const { requireAuth } = require('../middlewares/auth');

const router = express.Router();
router.use(requireAuth);

// ─── Helpers ───

/**
 * Build Basic Auth header for WP Application Passwords.
 * WordPress expects `user:application_password` in Base64.
 */
function wpAuthHeader(user, password) {
  const token = Buffer.from(`${user}:${password}`).toString('base64');
  return `Basic ${token}`;
}

/**
 * Make a request to a WordPress REST API endpoint.
 */
async function wpFetch(siteUrl, path, { user, password, method = 'GET', body = null } = {}) {
  // Normalize URL
  const base = siteUrl.replace(/\/+$/, '');
  const url = `${base}/wp-json/wp/v2${path}`;

  const headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'AINewsGenerator/2.0',
  };

  if (user && password) {
    headers['Authorization'] = wpAuthHeader(user, password);
  }

  const opts = { method, headers };
  if (body && method !== 'GET') {
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(url, opts);
  const text = await res.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }

  if (!res.ok) {
    const msg = data?.message || data?.raw || `HTTP ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return { data, headers: res.headers };
}

// ─── POST /api/wordpress/validate ───
// Validates WP credentials and marks the website as validated.
router.post('/validate', async (req, res) => {
  try {
    const { website_id } = req.body;

    if (!website_id) {
      return res.status(400).json({ error: { status: 400, message: 'website_id is required' } });
    }

    // Get website from DB
    const { rows } = await pool.query('SELECT * FROM websites WHERE id = $1', [website_id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
    }

    const site = rows[0];
    if (!site.platform_url || !site.platform_user || !site.platform_password) {
      return res.status(400).json({
        error: { status: 400, message: 'Website URL, user, and password are required for validation' },
      });
    }

    // Try to fetch current user from WP — this validates credentials
    const { data: wpUser } = await wpFetch(site.platform_url, '/users/me?context=edit', {
      user: site.platform_user,
      password: site.platform_password,
    });

    // Mark as validated
    await pool.query('UPDATE websites SET is_validated = true, updated_at = NOW() WHERE id = $1', [website_id]);

    return res.json({
      data: {
        validated: true,
        wp_user: {
          id: wpUser.id,
          name: wpUser.name,
          slug: wpUser.slug,
          roles: wpUser.roles,
        },
      },
    });
  } catch (err) {
    console.error('WP validate error:', err.message);

    // Mark as NOT validated on auth failure
    if (req.body.website_id) {
      await pool.query('UPDATE websites SET is_validated = false, updated_at = NOW() WHERE id = $1', [
        req.body.website_id,
      ]).catch(() => {});
    }

    const status = err.status === 401 || err.status === 403 ? 401 : 500;
    return res.status(status).json({
      error: {
        status,
        message: status === 401 ? 'Invalid WordPress credentials' : err.message,
      },
    });
  }
});

// ─── GET /api/wordpress/categories?website_id=X ───
router.get('/categories', async (req, res) => {
  try {
    const { website_id } = req.query;
    if (!website_id) {
      return res.status(400).json({ error: { status: 400, message: 'website_id is required' } });
    }

    const { rows } = await pool.query('SELECT * FROM websites WHERE id = $1', [website_id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
    }

    const site = rows[0];
    if (!site.platform_url || !site.platform_user || !site.platform_password) {
      return res.status(400).json({ error: { status: 400, message: 'Website credentials incomplete' } });
    }

    // Fetch all categories (paginate — WP default max is 100)
    let allCategories = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
      const { data: cats, headers: respHeaders } = await wpFetch(
        site.platform_url,
        `/categories?per_page=100&page=${page}`,
        { user: site.platform_user, password: site.platform_password }
      );

      allCategories = allCategories.concat(
        cats.map((c) => ({
          id: c.id,
          name: c.name,
          slug: c.slug,
          count: c.count,
          parent: c.parent,
        }))
      );

      const totalPages = parseInt(respHeaders.get('x-wp-totalpages') || '1', 10);
      hasMore = page < totalPages;
      page++;
    }

    return res.json({ data: allCategories });
  } catch (err) {
    console.error('WP categories error:', err.message);
    return res.status(err.status || 500).json({
      error: { status: err.status || 500, message: err.message },
    });
  }
});

// ─── GET /api/wordpress/authors?website_id=X ───
router.get('/authors', async (req, res) => {
  try {
    const { website_id } = req.query;
    if (!website_id) {
      return res.status(400).json({ error: { status: 400, message: 'website_id is required' } });
    }

    const { rows } = await pool.query('SELECT * FROM websites WHERE id = $1', [website_id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
    }

    const site = rows[0];
    if (!site.platform_url || !site.platform_user || !site.platform_password) {
      return res.status(400).json({ error: { status: 400, message: 'Website credentials incomplete' } });
    }

    const { data: authors } = await wpFetch(
      site.platform_url,
      '/users?per_page=100&roles=administrator,editor,author',
      { user: site.platform_user, password: site.platform_password }
    );

    return res.json({
      data: authors.map((a) => ({
        id: a.id,
        name: a.name,
        slug: a.slug,
      })),
    });
  } catch (err) {
    console.error('WP authors error:', err.message);
    return res.status(err.status || 500).json({
      error: { status: err.status || 500, message: err.message },
    });
  }
});

// ─── POST /api/wordpress/publish ───
router.post('/publish', async (req, res) => {
  try {
    const { website_id, title, content, status = 'draft', categories = [], featured_media, author } = req.body;

    if (!website_id || !title || !content) {
      return res.status(400).json({
        error: { status: 400, message: 'website_id, title, and content are required' },
      });
    }

    const { rows } = await pool.query('SELECT * FROM websites WHERE id = $1', [website_id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
    }

    const site = rows[0];

    const postBody = {
      title,
      content,
      status: site.post_status || status,
    };

    if (categories.length > 0) postBody.categories = categories;
    if (featured_media) postBody.featured_media = featured_media;
    if (author) postBody.author = author;

    const { data: wpPost } = await wpFetch(site.platform_url, '/posts', {
      user: site.platform_user,
      password: site.platform_password,
      method: 'POST',
      body: postBody,
    });

    return res.json({
      data: {
        id: wpPost.id,
        link: wpPost.link,
        status: wpPost.status,
        title: wpPost.title?.rendered,
      },
    });
  } catch (err) {
    console.error('WP publish error:', err.message);
    return res.status(err.status || 500).json({
      error: { status: err.status || 500, message: err.message },
    });
  }
});

module.exports = router;
