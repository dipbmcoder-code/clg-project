const pool = require('../config/db');

class Website {
    static async findAll({ whereClause = '', params = [], sortField = 'created_at', sortDir = 'DESC', limit = 25, offset = 0 }) {
        // Check sort safety
        const allowedFields = ['id', 'platform_name', 'platform_url', 'active', 'is_validated', 'created_at', 'updated_at'];
        const safeField = allowedFields.includes(sortField) ? sortField : 'created_at';
        const safeDir = sortDir?.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';

        let idx = params.length + 1;
        const query = `
      SELECT * FROM websites
      ${whereClause}
      ORDER BY ${safeField} ${safeDir}
      LIMIT $${idx++} OFFSET $${idx++}
    `;

        const { rows } = await pool.query(query, [...params, limit, offset]);
        return rows;
    }

    static async count({ whereClause = '', params = [] }) {
        const { rows } = await pool.query(`SELECT COUNT(*)::int AS count FROM websites ${whereClause}`, params);
        return rows[0].count;
    }

    static async findById(id) {
        const { rows } = await pool.query('SELECT * FROM websites WHERE id = $1', [id]);
        return rows[0];
    }

    static async create(data) {
        // Map data fields to columns
        const columns = [
            'platform_name', 'platform_url', 'platform_user', 'platform_password',
            'active', 'is_validated', 'post_status', 'l_version', 'topic_niche',
            'enable_social_media', 'twitter_handles', 'reddit_subreddits',
            'social_media_categories', 'reddit_mode', 'reddit_categories',
            'reddit_min_score', 'enable_reddit', 'website_author'
        ];

        // Prepare values array based on columns
        const values = columns.map(col => {
            const val = data[col];
            if (['twitter_handles', 'reddit_subreddits', 'social_media_categories', 'reddit_categories', 'website_author'].includes(col)) {
                return JSON.stringify(val || (col === 'website_author' ? {} : []));
            }
            if (col === 'active') return val ?? true;
            if (col === 'is_validated') return val ?? false;
            if (col === 'post_status') return val || 'draft';
            if (col === 'l_version') return val || 'eng';
            if (col === 'topic_niche') return val || 'general';
            if (col === 'enable_social_media') return val ?? false;
            if (col === 'enable_reddit') return val ?? false;
            if (col === 'reddit_mode') return val || 'hot';
            if (col === 'reddit_min_score') return val ?? 0;
            return val || null;
        });

        const placeholders = values.map((_, i) => `$${i + 1}`).join(',');

        const query = `INSERT INTO websites (${columns.join(',')}) VALUES (${placeholders}) RETURNING *`;
        const { rows } = await pool.query(query, values);
        return rows[0];
    }

    static async update(id, data) {
        const fields = [];
        const values = [];
        let idx = 1;

        for (const [key, value] of Object.entries(data)) {
            fields.push(`${key} = $${idx++}`);

            // Handle JSON stringification if needed
            if (['twitter_handles', 'reddit_subreddits', 'social_media_categories', 'reddit_categories', 'website_author'].includes(key) && typeof value !== 'string') {
                values.push(JSON.stringify(value));
            } else {
                values.push(value);
            }
        }

        if (fields.length === 0) return null;

        values.push(id);
        const query = `
      UPDATE websites 
      SET ${fields.join(', ')}, updated_at = NOW() 
      WHERE id = $${idx}
      RETURNING *
    `;

        const { rows } = await pool.query(query, values);
        return rows[0];
    }

    static async delete(id) {
        const { rows } = await pool.query('DELETE FROM websites WHERE id = $1 RETURNING id', [id]);
        return rows[0];
    }
}

module.exports = Website;
