/**
 * Database Seeder — seeds default data if tables are empty.
 */
const pool = require('./db');
const { hashPassword } = require('../utils/security');
const logger = require('./logger');

// ─── Seed Defaults ───

async function seedDefaults() {
  const client = await pool.connect();
  try {
    // Seed default prompts
    try {
      const { rows: promptRows } = await client.query('SELECT COUNT(*)::int AS count FROM news_prompts');
      if (promptRows[0].count === 0) {
        await client.query(`
          INSERT INTO news_prompts (
            social_media_news_title_prompt,
            social_media_news_image_prompt,
            social_media_news_content_prompt
          ) VALUES (
            'Write a compelling, click-worthy news headline based on this social media post. Topic: {topic_niche}. Post: {tweet_text}. Keep it under 80 characters, professional tone.',
            'Generate a professional, photorealistic news thumbnail image for this headline: {tweet_text}. Style: modern digital news media, clean composition, 1:1 aspect ratio.',
            'Write a professional news article based on this social media post. Topic focus: {topic_niche}. Source: {source} ({source_handle}). Post content: {tweet_text}. Write 300-500 words in a neutral, journalistic tone. Include context and analysis. Do not fabricate quotes or facts.'
          )
        `);
        logger.info('✅ Default news prompts seeded');
      }
    } catch (err) {
      if (err.code === '42P01') {
        logger.warn('⚠️ news_prompts table does not exist. Skipping seed.');
      } else {
        throw err;
      }
    }

    // Seed default admin user
    try {
      const { rows: userRows } = await client.query('SELECT COUNT(*)::int AS count FROM users');
      if (userRows[0].count === 0) {
        const pwHash = hashPassword('admin123'); // Use central security utils
        await client.query(
          `INSERT INTO users (firstname, lastname, email, password_hash, role)
           VALUES ('Admin', 'User', 'admin@ainews.com', $1, 'Super Admin')`,
          [pwHash]
        );
        logger.info('✅ Default admin user created (admin@ainews.com / admin123)');
      }
    } catch (err) {
      if (err.code === '42P01') {
        logger.warn('⚠️ users table does not exist. Skipping seed.');
      } else {
        throw err;
      }
    }

  } catch (err) {
    logger.error('⚠️ Seed error: ' + err.message);
  } finally {
    client.release();
  }
}

// ─── Legacy Init (now handled by Migrations) ───
async function initDatabase() {
  // Deprecated: Schema creation is now handled by node-pg-migrate.
  // Kept empty to satisfy existing imports without breaking imports.
  logger.info('ℹ️ Database schema management is handled by migrations.');
}

// Run if called directly
if (require.main === module) {
  (async () => {
    await seedDefaults();
    process.exit(0);
  })();
}

module.exports = { initDatabase, seedDefaults };
