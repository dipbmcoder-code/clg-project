const prisma = require('../config/database');
const { decrypt } = require('../utils/helpers');
const logger = require('../config/logger');
const fetch = require('node-fetch');

/**
 * Helper: get WP auth header for a website
 */
const getWpAuth = async (websiteId) => {
  const website = await prisma.website.findUnique({ where: { id: parseInt(websiteId) } });
  if (!website) throw new Error('Website not found');

  const password = decrypt(website.platformPassword);
  const auth = Buffer.from(`${website.platformUser}:${password}`).toString('base64');
  return { auth, baseUrl: website.platformUrl };
};

const getCategories = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const categories = await prisma.wordPressCategory.findMany({
      where: { websiteId: parseInt(websiteId) },
      orderBy: { name: 'asc' },
    });

    // Build tree structure
    const tree = buildCategoryTree(categories);
    res.json({ data: { categories, tree } });
  } catch (err) {
    next(err);
  }
};

const syncCategories = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const { auth, baseUrl } = await getWpAuth(websiteId);

    // Fetch all categories from WordPress (paginated)
    let allCategories = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
      const response = await fetch(
        `${baseUrl}/wp-json/wp/v2/categories?per_page=100&page=${page}`,
        { headers: { Authorization: `Basic ${auth}` } }
      );

      if (!response.ok) {
        throw new Error(`WordPress API returned ${response.status}: ${await response.text()}`);
      }

      const cats = await response.json();
      allCategories = allCategories.concat(cats);

      const totalPages = parseInt(response.headers.get('x-wp-totalpages') || '1');
      hasMore = page < totalPages;
      page++;
    }

    // Clear existing categories for this website
    await prisma.wordPressCategory.deleteMany({
      where: { websiteId: parseInt(websiteId) },
    });

    // Insert fresh categories
    if (allCategories.length > 0) {
      await prisma.wordPressCategory.createMany({
        data: allCategories.map((cat) => ({
          wpId: cat.id,
          name: cat.name,
          slug: cat.slug,
          parentId: cat.parent || null,
          count: cat.count || 0,
          websiteId: parseInt(websiteId),
        })),
      });
    }

    logger.info(`Synced ${allCategories.length} categories for website ${websiteId}`);
    res.json({
      data: {
        message: `Successfully synced ${allCategories.length} categories`,
        count: allCategories.length,
      },
    });
  } catch (err) {
    logger.error(`Category sync failed for website ${req.params.websiteId}: ${err.message}`);
    next(err);
  }
};

const healthCheck = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const { auth, baseUrl } = await getWpAuth(websiteId);

    const start = Date.now();
    const response = await fetch(`${baseUrl}/wp-json/wp/v2/users/me`, {
      headers: { Authorization: `Basic ${auth}` },
      timeout: 10000,
    });
    const latency = Date.now() - start;

    if (response.ok) {
      const user = await response.json();
      res.json({
        data: {
          healthy: true,
          latency: `${latency}ms`,
          wpUser: user.name,
          wpRole: user.roles?.[0],
        },
      });
    } else {
      res.json({
        data: {
          healthy: false,
          latency: `${latency}ms`,
          error: `HTTP ${response.status}`,
        },
      });
    }
  } catch (err) {
    res.json({
      data: { healthy: false, error: err.message },
    });
  }
};

const getRecentPosts = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const { auth, baseUrl } = await getWpAuth(websiteId);
    const perPage = req.query.perPage || 10;

    const response = await fetch(
      `${baseUrl}/wp-json/wp/v2/posts?per_page=${perPage}&orderby=date&order=desc`,
      { headers: { Authorization: `Basic ${auth}` } }
    );

    if (!response.ok) {
      throw new Error(`WordPress API returned ${response.status}`);
    }

    const posts = await response.json();
    const total = response.headers.get('x-wp-total');

    res.json({
      data: {
        posts: posts.map((p) => ({
          wpId: p.id,
          title: p.title.rendered,
          status: p.status,
          date: p.date,
          link: p.link,
          categories: p.categories,
        })),
        total: parseInt(total || '0'),
      },
    });
  } catch (err) {
    next(err);
  }
};

/**
 * Build tree structure from flat categories list
 */
function buildCategoryTree(categories) {
  const map = {};
  const tree = [];

  categories.forEach((cat) => {
    map[cat.wpId] = { ...cat, children: [] };
  });

  categories.forEach((cat) => {
    if (cat.parentId && map[cat.parentId]) {
      map[cat.parentId].children.push(map[cat.wpId]);
    } else {
      tree.push(map[cat.wpId]);
    }
  });

  return tree;
}

module.exports = { getCategories, syncCategories, healthCheck, getRecentPosts };
