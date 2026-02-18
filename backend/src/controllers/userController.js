const User = require('../models/User');
const { hashPassword } = require('../utils/security');

class UserController {
    /**
     * Helper: Format user for response
     */
    static formatUser(user) {
        if (!user) return null;
        return {
            ...user,
            documentId: user.id,
            roles: [{ id: user.role === 'Super Admin' ? 1 : 2, name: user.role }],
            blocked: !user.is_active,
            isActive: user.is_active,
            // Remove password_hash if present
            password_hash: undefined,
        };
    }

    /**
     * Helper: Paginated response
     */
    static paginatedResponse(results, total, page, pageSize) {
        return {
            results: results.map(UserController.formatUser),
            pagination: {
                page,
                pageSize,
                total,
                pageCount: Math.ceil(total / pageSize),
            },
        };
    }

    static async list(req, res) {
        try {
            const page = Math.max(1, parseInt(req.query.page, 10) || 1);
            const pageSize = Math.min(100, Math.max(1, parseInt(req.query.pageSize, 10) || 25));
            const sort = req.query.sort || 'id:desc';
            const search = req.query._q || '';

            const allowedFields = ['id', 'firstname', 'lastname', 'email', 'role', 'is_active', 'created_at'];
            const [sortField, sortDir] = sort.split(':');
            const safeField = allowedFields.includes(sortField) ? sortField : 'id';
            const safeDir = sortDir?.toLowerCase() === 'asc' ? 'ASC' : 'DESC';

            // Build WHERE clause
            const conditions = [];
            const params = [];
            let idx = 1;

            if (search) {
                conditions.push(`(firstname ILIKE $${idx} OR lastname ILIKE $${idx} OR email ILIKE $${idx})`);
                params.push(`%${search}%`);
                idx++;
            }

            const whereClause = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';

            // Count total
            const total = await User.count(whereClause, params); // Need to implement count with where+params correctly in User model

            // Fetch
            // Wait, User.findAll signature: (whereClause, params, sortField, sortDir, limit, offset)
            // Actually my model implementation was slightly different: static async findAll(whereClause = '', params = [], ...
            // I should align with User.js implementation.
            // User.js: findAll(whereClause, params, sortField, sortDir, limit, offset)

            const offset = (page - 1) * pageSize;
            const rows = await User.findAll(whereClause, params, safeField, safeDir, pageSize, offset);

            // Wait, the User.findAll expects `params` to be passed for placeholders in `whereClause`.
            // The implementation in User.js does: `const query = ... LIMIT $${idx++} OFFSET $${idx++}`
            // And executes with `[...params, limit, offset]`.
            // The `idx` inside `findAll` starts as `params.length + 1`.
            // If `params` has 1 item ($1), `limit` becomes $2, `offset` becomes $3.
            // The `whereClause` uses $1.
            // This is consistent.

            return res.json(UserController.paginatedResponse(rows, parseInt(total), page, pageSize));
        } catch (err) {
            console.error('GET /users error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async getOne(req, res) {
        try {
            const user = await User.findById(req.params.id);
            if (!user) {
                return res.status(404).json({ error: { status: 404, message: 'User not found' } });
            }
            return res.json({ data: UserController.formatUser(user) });
        } catch (err) {
            console.error('GET /users/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async create(req, res) {
        try {
            const { firstname, lastname, email, password, role, roles, is_active } = req.body;

            if (!email || !password) {
                return res.status(400).json({ error: { status: 400, message: 'Email and password are required' } });
            }

            const existing = await User.findByEmail(email);
            if (existing) {
                return res.status(409).json({ error: { status: 409, message: 'Email already exists' } });
            }

            // Role logic
            let finalRole = role || 'Admin';
            if (!role && roles) {
                if (typeof roles === 'string') finalRole = roles;
                else if (roles.name) finalRole = roles.name;
                else if (Array.isArray(roles) && roles[0]?.name) finalRole = roles[0].name;
            }

            const pwHash = hashPassword(password);

            const newUser = await User.create({
                firstname,
                lastname,
                email,
                password_hash: pwHash,
                role: finalRole,
                is_active: is_active ?? true,
            });

            return res.status(201).json({ data: UserController.formatUser(newUser) });
        } catch (err) {
            console.error('POST /users error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async update(req, res) {
        try {
            const b = req.body;
            const id = req.params.id;

            const updates = {};
            if (b.firstname !== undefined) updates.firstname = b.firstname;
            if (b.lastname !== undefined) updates.lastname = b.lastname;
            if (b.email !== undefined) updates.email = b.email;

            // Role logic
            if (b.role !== undefined) {
                updates.role = b.role;
            } else if (b.roles !== undefined) {
                let role;
                if (typeof b.roles === 'string') role = b.roles;
                else if (b.roles?.name) role = b.roles.name;
                else if (Array.isArray(b.roles) && b.roles[0]?.name) role = b.roles[0].name;
                if (role) updates.role = role;
            }

            // is_active logic
            const activeVal = b.is_active !== undefined ? b.is_active : b.isActive;
            if (activeVal !== undefined) updates.is_active = activeVal;

            if (b.password) {
                updates.password_hash = hashPassword(b.password);
            }

            const updatedUser = await User.update(id, updates);

            if (!updatedUser) {
                // Can fail if user not found or no updates provided (but if no updates provided, my generic update returns null immediately)
                // If updates empty, return 400
                if (Object.keys(updates).length === 0) {
                    return res.status(400).json({ error: { status: 400, message: 'No fields to update' } });
                }
                return res.status(404).json({ error: { status: 404, message: 'User not found' } });
            }

            return res.json({ data: UserController.formatUser(updatedUser) });
        } catch (err) {
            console.error('PUT /users/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }

    static async delete(req, res) {
        try {
            const deletedUser = await User.delete(req.params.id);
            if (!deletedUser) {
                return res.status(404).json({ error: { status: 404, message: 'User not found' } });
            }
            return res.json({ data: { id: deletedUser.id } });
        } catch (err) {
            console.error('DELETE /users/:id error:', err);
            return res.status(500).json({ error: { status: 500, message: err.message } });
        }
    }
}

module.exports = UserController;
