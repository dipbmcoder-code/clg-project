const pool = require('../config/db');

class User {
    static async findByEmail(email) {
        const { rows } = await pool.query(
            'SELECT id, firstname, lastname, email, role, is_active, password_hash FROM users WHERE email = $1',
            [email]
        );
        return rows[0];
    }

    static async findById(id) {
        const { rows } = await pool.query(
            'SELECT id, firstname, lastname, email, role, is_active, created_at, updated_at FROM users WHERE id = $1',
            [id]
        );
        return rows[0];
    }

    static async create({ firstname, lastname, email, password_hash, role, is_active }) {
        const { rows } = await pool.query(
            `INSERT INTO users (firstname, lastname, email, password_hash, role, is_active)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, firstname, lastname, email, role, is_active, created_at, updated_at`,
            [firstname || '', lastname || '', email, password_hash, role, is_active ?? true]
        );
        return rows[0];
    }

    /**
     * Update user fields dynamically.
     * @param {number} id - User ID
     * @param {object} data - Key-value pairs of fields to update
     */
    static async update(id, data) {
        const fields = [];
        const values = [];
        let idx = 1;

        for (const [key, value] of Object.entries(data)) {
            fields.push(`${key} = $${idx++}`);
            values.push(value);
        }

        if (fields.length === 0) return null;

        // Add updated_at if not present in data, or handled by DB trigger? 
        // Usually handled explicitly here
        // But updated_at is usually automatic if using ORM. Here we do it manually.
        // Let's add updated_at = NOW() to the query string if not passed.

        values.push(id);
        const query = `
      UPDATE users 
      SET ${fields.join(', ')}, updated_at = NOW() 
      WHERE id = $${idx}
      RETURNING id, firstname, lastname, email, role, is_active, created_at, updated_at
    `;

        const { rows } = await pool.query(query, values);
        return rows[0];
    }

    static async delete(id) {
        const { rows } = await pool.query('DELETE FROM users WHERE id = $1 RETURNING id', [id]);
        return rows[0];
    }

    static async count(whereClause = '', params = []) {
        const { rows } = await pool.query(`SELECT COUNT(*)::int AS count FROM users ${whereClause}`, params);
        return rows[0].count;
    }

    static async findAll(whereClause = '', params = [], sortField = 'id', sortDir = 'DESC', limit = 25, offset = 0) {
        // Check sort safety
        const allowedFields = ['id', 'firstname', 'lastname', 'email', 'role', 'is_active', 'created_at'];
        const safeField = allowedFields.includes(sortField) ? sortField : 'id';
        const safeDir = sortDir?.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';

        // Current params length
        let idx = params.length + 1;

        const query = `
      SELECT id, firstname, lastname, email, role, is_active, created_at, updated_at
      FROM users ${whereClause}
      ORDER BY ${safeField} ${safeDir}
      LIMIT $${idx++} OFFSET $${idx++}
    `;

        const { rows } = await pool.query(query, [...params, limit, offset]);
        return rows;
    }
}

module.exports = User;
