require('dotenv').config();

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const logger = require('./config/logger');

// ─── Route modules ───
const authRoutes = require('./routes/auth');
const websitesRoutes = require('./routes/websites');
const promptsRoutes = require('./routes/prompts');
const logsRoutes = require('./routes/logs');
const postsRoutes = require('./routes/posts');
const dashboardRoutes = require('./routes/dashboard');
const usersRoutes = require('./routes/users');
const wordpressRoutes = require('./routes/wordpress');

const app = express();

// ─── Middleware ───
app.use(cors({
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true,
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// ─── Request logger (dev & prod) ───
app.use(morgan('combined', { stream: logger.stream }));

// ─── Health check ───
app.get('/health', (_req, res) => {
    res.json({ status: 'ok', service: 'ai-news-backend', timestamp: new Date().toISOString() });
});

// ─── API Routes ───
app.use('/api/auth', authRoutes);
app.use('/api/websites', websitesRoutes);
app.use('/api/news-prompts', promptsRoutes);
app.use('/api/news-logs', logsRoutes);
app.use('/api/social-posts', postsRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/users', usersRoutes);
app.use('/api/wordpress', wordpressRoutes);

// ─── 404 handler ───
app.use((_req, res) => {
    res.status(404).json({ error: { status: 404, message: 'Route not found' } });
});

// ─── Global error handler ───
app.use((err, req, res, next) => {
    logger.error(err.message, { stack: err.stack }); // Log error with stack trace

    const status = err.status || 500;
    res.status(status).json({
        error: { status, message: status === 500 ? 'Internal server error' : err.message },
    });
});

module.exports = app;
