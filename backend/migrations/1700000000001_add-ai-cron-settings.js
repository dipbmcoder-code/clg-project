exports.shorthands = undefined;

exports.up = (pgm) => {
    // AI Settings — stores AI provider configuration (keys, models, etc.)
    pgm.createTable('ai_settings', {
        id: 'id',
        // Content generation
        content_provider: { type: 'varchar(50)', default: 'openai', notNull: true },
        content_api_key: { type: 'text' },
        content_model: { type: 'varchar(100)', default: 'gpt-4o-mini' },
        content_base_url: { type: 'text' },
        content_temperature: { type: 'numeric(3,2)', default: 0.7 },
        content_max_tokens: { type: 'integer', default: 2000 },
        // Image generation
        image_provider: { type: 'varchar(50)', default: 'gemini-flash-image' },
        image_api_key: { type: 'text' },
        image_model: { type: 'varchar(100)' },
        // AWS S3
        aws_access_key_id: { type: 'text' },
        aws_secret_access_key: { type: 'text' },
        aws_s3_bucket: { type: 'varchar(255)' },
        aws_region: { type: 'varchar(50)', default: 'us-east-1' },
        aws_url: { type: 'text' },
        // Misc
        sendgrid_api_key: { type: 'text' },
        sender_email: { type: 'varchar(255)' },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
        updated_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
    }, { ifNotExists: true });

    // Cron Settings — stores scheduler configuration and run status
    pgm.createTable('cron_settings', {
        id: 'id',
        cron_enabled: { type: 'boolean', default: true, notNull: true },
        cron_interval_minutes: { type: 'integer', default: 60, notNull: true },
        last_run_at: { type: 'timestamp' },
        last_run_status: { type: 'varchar(50)' },
        last_run_message: { type: 'text' },
        last_run_duration_sec: { type: 'integer' },
        next_run_at: { type: 'timestamp' },
        is_running: { type: 'boolean', default: false },
        total_runs: { type: 'integer', default: 0 },
        total_success: { type: 'integer', default: 0 },
        total_failures: { type: 'integer', default: 0 },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
        updated_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
    }, { ifNotExists: true });
};

exports.down = (pgm) => {
    pgm.dropTable('cron_settings', { ifExists: true });
    pgm.dropTable('ai_settings', { ifExists: true });
};
