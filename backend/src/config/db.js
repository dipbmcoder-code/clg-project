/**
 * PostgreSQL connection pool with retry logic.
 * Shared across all route modules.
 */

const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT, 10) || 5444,
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'strapi',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('❌ Unexpected DB pool error:', err);
});

/**
 * Wait for DB to be reachable — retries with exponential backoff.
 * @param {number} maxRetries - Maximum retry attempts (default 10)
 * @param {number} baseDelay  - Initial delay in ms (default 2000)
 */
async function waitForDB(maxRetries = 10, baseDelay = 2000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const client = await pool.connect();
      await client.query('SELECT 1');
      client.release();
      console.log('✅ Database connection established');
      return true;
    } catch (err) {
      const delay = Math.min(baseDelay * Math.pow(1.5, attempt - 1), 15000);
      console.warn(
        `⏳ DB connection attempt ${attempt}/${maxRetries} failed: ${err.message}. Retrying in ${Math.round(delay / 1000)}s...`
      );
      if (attempt === maxRetries) {
        throw new Error(`Could not connect to database after ${maxRetries} attempts: ${err.message}`);
      }
      await new Promise((r) => setTimeout(r, delay));
    }
  }
}

module.exports = pool;
module.exports.waitForDB = waitForDB;
