const app = require('./app');
const { waitForDB } = require('./config/db');
const { seedDefaults } = require('./config/seeder');
const logger = require('./config/logger');

const PORT = parseInt(process.env.PORT, 10) || 4000;

// ─── Graceful shutdown ───
function setupGracefulShutdown(server) {
    const shutdown = (signal) => {
        logger.info(`\n${signal} received. Shutting down gracefully...`);
        server.close(() => {
            logger.info('HTTP server closed.');
            const pool = require('./config/db');
            pool.end().then(() => {
                logger.info('DB pool closed.');
                process.exit(0);
            });
        });
        setTimeout(() => process.exit(1), 10000);
    };
    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));
}

// ─── Start server ───
async function start() {
    try {
        // Wait for DB to be reachable
        await waitForDB();

        // Seed defaults
        await seedDefaults();

        const server = app.listen(PORT, '0.0.0.0', () => {
            logger.info(`\n🚀 AI News Backend running on http://localhost:${PORT}`);
            logger.info(`   Health: http://localhost:${PORT}/health\n`);
        });

        setupGracefulShutdown(server);
    } catch (err) {
        logger.error('❌ Failed to start server: ' + err.message);
        process.exit(1);
    }
}

start();
