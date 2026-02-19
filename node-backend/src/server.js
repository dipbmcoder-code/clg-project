require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
const logger = require('./config/logger');
const prisma = require('./config/database');
const { apiLimiter } = require('./middleware/rateLimiter');

// ─── Startup checks ─────────────────────────────────────────
if (!process.env.JWT_SECRET) {
  console.error('FATAL: JWT_SECRET environment variable is required');
  process.exit(1);
}
if (!process.env.PASSWORD_SECRET_KEY) {
  console.error('FATAL: PASSWORD_SECRET_KEY environment variable is required');
  process.exit(1);
}

// Import routes
const authRoutes = require('./routes/auth.routes');
const websiteRoutes = require('./routes/website.routes');
const newsPromptRoutes = require('./routes/newsPrompt.routes');
const manualNewsRoutes = require('./routes/manualNews.routes');
const newsLogRoutes = require('./routes/newsLog.routes');
const aiSettingsRoutes = require('./routes/aiSettings.routes');
const socialMediaRoutes = require('./routes/socialMedia.routes');
const wordpressRoutes = require('./routes/wordpress.routes');
const rapidapiRoutes = require('./routes/rapidapi.routes');
const uploadRoutes = require('./routes/upload.routes');
const healthRoutes = require('./routes/health.routes');

const app = express();
const PORT = process.env.PORT || 4000;

// ─── Middleware ───────────────────────────────────────────────
app.use(helmet({ crossOriginResourcePolicy: { policy: 'cross-origin' } }));
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3033',
  credentials: true,
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(morgan('combined', { stream: { write: (msg) => logger.info(msg.trim()) } }));

// ─── Static files (uploads) ─────────────────────────────────
app.use('/uploads', express.static(path.join(__dirname, '..', process.env.UPLOAD_DIR || 'uploads')));

// ─── API rate limiter ────────────────────────────────────────
app.use('/api', apiLimiter);

// ─── Routes ──────────────────────────────────────────────────
app.use('/api/auth', authRoutes);
app.use('/api/websites', websiteRoutes);
app.use('/api/news-prompts', newsPromptRoutes);
app.use('/api/manual-news', manualNewsRoutes);
app.use('/api/news-logs', newsLogRoutes);
app.use('/api/ai-settings', aiSettingsRoutes);
app.use('/api/social-media', socialMediaRoutes);
app.use('/api/wordpress', wordpressRoutes);
app.use('/api/rapidapi', rapidapiRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/health', healthRoutes);

// ─── 404 handler ─────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({ error: { message: `Route ${req.originalUrl} not found` } });
});

// ─── Error handler ───────────────────────────────────────────
app.use((err, req, res, _next) => {
  logger.error(`${err.status || 500} - ${err.message} - ${req.originalUrl}`);
  res.status(err.status || 500).json({
    error: {
      message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message,
      ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
    },
  });
});

// ─── Start server ────────────────────────────────────────────
const server = app.listen(PORT, () => {
  logger.info(`AI News Generator Backend running on port ${PORT}`);
  logger.info(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

// ─── Graceful shutdown ───────────────────────────────────────
const gracefulShutdown = async (signal) => {
  logger.info(`${signal} received. Shutting down gracefully...`);
  server.close(async () => {
    await prisma.$disconnect();
    logger.info('Server shut down.');
    process.exit(0);
  });
};
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

module.exports = app;
