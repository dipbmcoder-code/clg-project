const Website = require('../models/Website');
const { parsePagination, paginatedResponse, safeOrderBy } = require('../utils/route-helpers');

class WebsiteController {

    static async list(req, res) {
        try {
            const { page, pageSize, sort, search } = parsePagination(req.query, 'created_at:desc');

            const conditions = [];
            const params = [];
            let idx = 1;

            if (req.query.active !== undefined) {
                conditions.push(`active = $${idx++}`);
                params.push(req.query.active === 'true');
            }
            if (search) {
                conditions.push(`(platform_name ILIKE $${idx} OR platform_url ILIKE $${idx})`);
                params.push(`%${search}%`);
                idx++;
            }

            const whereClause = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
            const [sortField, sortDir] = sort.split(':');

            const count = await Website.count({ whereClause, params });
            const rows = await Website.findAll({ whereClause, params, sortField, sortDir, limit: pageSize, offset: (page - 1) * pageSize });

            return res.json(paginatedResponse(rows, parseInt(count), page, pageSize));
        } catch (err) {
            console.error('GET /websites error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async getOne(req, res) {
        try {
            const website = await Website.findById(req.params.id);
            if (!website) {
                return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
            }
            return res.json({ data: { ...website, documentId: website.id } });
        } catch (err) {
            console.error('GET /websites/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async create(req, res) {
        try {
            if (!req.body.platform_name) {
                return res.status(400).json({ error: { status: 400, message: 'platform_name is required' } });
            }

            const website = await Website.create(req.body);
            return res.status(201).json({ data: { ...website, documentId: website.id } });
        } catch (err) {
            console.error('POST /websites error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async update(req, res) {
        try {
            const updated = await Website.update(req.params.id, req.body);

            if (!updated) {
                // If update returned null (no fields) or undefined (not found/updated)
                // need better distinction or assume not found if keys present in body
                const keys = Object.keys(req.body);
                if (keys.length === 0) return res.status(400).json({ error: { status: 400, message: 'No fields to update' } });

                // Assuming update returns null if no rows updated (id not found)? 
                // My Website.update returns rows[0]. If no rows, returns undefined.
                return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
            }

            return res.json({ data: { ...updated, documentId: updated.id } });
        } catch (err) {
            console.error('PUT /websites/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async delete(req, res) {
        try {
            const deleted = await Website.delete(req.params.id);
            if (!deleted) {
                return res.status(404).json({ error: { status: 404, message: 'Website not found' } });
            }
            return res.json({ data: { id: deleted.id } });
        } catch (err) {
            console.error('DELETE /websites/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }
}

module.exports = WebsiteController;
