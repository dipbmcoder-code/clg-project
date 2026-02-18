const User = require('../models/User');
const { createToken } = require('../middlewares/auth');
const { hashPassword } = require('../utils/security');

class AuthController {

    /**
     * Login user and generate token.
     */
    static async login(req, res) {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ error: { status: 400, message: 'Email and password are required' } });
        }

        try {
            const user = await User.findByEmail(email);

            if (!user) {
                return res.status(401).json({ error: { status: 401, message: 'Invalid email or password' } });
            }

            const pwHash = hashPassword(password);
            if (user.password_hash !== pwHash) {
                return res.status(401).json({ error: { status: 401, message: 'Invalid email or password' } });
            }

            if (!user.is_active) {
                return res.status(403).json({ error: { status: 403, message: 'Account is deactivated' } });
            }

            const token = createToken({
                user_id: user.id,
                email: user.email,
                role: user.role,
            });

            return res.json({
                data: {
                    token,
                    user: {
                        id: user.id,
                        firstname: user.firstname,
                        lastname: user.lastname,
                        email: user.email,
                        roles: [{ name: user.role }],
                    },
                },
            });
        } catch (err) {
            console.error('Login error:', err);
            return res.status(500).json({ error: { status: 500, message: 'Internal server error' } });
        }
    }

    /**
     * Get current authenticated user profile.
     */
    static async me(req, res) {
        try {
            const user = await User.findById(req.user.user_id);

            if (!user) {
                return res.status(404).json({ error: { status: 404, message: 'User not found' } });
            }

            return res.json({
                data: {
                    id: user.id,
                    firstname: user.firstname,
                    lastname: user.lastname,
                    email: user.email,
                    roles: [{ name: user.role }],
                },
            });
        } catch (err) {
            console.error('Auth/me error:', err);
            return res.status(500).json({ error: { status: 500, message: 'Internal server error' } });
        }
    }
}

module.exports = AuthController;
