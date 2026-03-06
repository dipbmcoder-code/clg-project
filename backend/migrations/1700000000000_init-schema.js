exports.shorthands = undefined;

exports.up = (pgm) => {
    // Websites
    pgm.createTable('websites', {
        id: 'id',
        platform_name: { type: 'varchar(255)', notNull: true },
        platform_url: { type: 'varchar(500)' },
        platform_user: { type: 'varchar(255)' },
        platform_password: { type: 'text' },
        active: { type: 'boolean', default: true },
        is_validated: { type: 'boolean', default: false },
        post_status: { type: 'varchar(50)', default: 'draft' },
        l_version: { type: 'varchar(10)', default: 'eng' },
        topic_niche: { type: 'varchar(255)', default: 'general' },
        enable_social_media: { type: 'boolean', default: false },
        twitter_handles: { type: 'jsonb', default: '[]' },
        reddit_subreddits: { type: 'jsonb', default: '[]' },
        social_media_categories: { type: 'jsonb', default: '[]' },
        reddit_mode: { type: 'varchar(20)', default: 'hot' },
        reddit_categories: { type: 'jsonb', default: '[]' },
        reddit_min_score: { type: 'integer', default: 0 },
        enable_reddit: { type: 'boolean', default: false },
        website_author: { type: 'jsonb', default: '{}' },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
        updated_at: { type: 'timestamp', default: pgm.func('current_timestamp') }
    }, { ifNotExists: true });

    // News Prompts
    pgm.createTable('news_prompts', {
        id: 'id',
        social_media_news_title_prompt: { type: 'text' },
        social_media_news_image_prompt: { type: 'text' },
        social_media_news_content_prompt: { type: 'text' },
        ai_tone: { type: 'text' },
        ai_language: { type: 'varchar(100)', default: 'English' },
        ai_max_words: { type: 'integer', default: 500 },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
        updated_at: { type: 'timestamp', default: pgm.func('current_timestamp') }
    }, { ifNotExists: true });

    // News Logs
    pgm.createTable('news_logs', {
        id: 'id',
        news_type: { type: 'varchar(100)' },
        title: { type: 'varchar(500)' },
        website_name: { type: 'varchar(255)' },
        image_generated: { type: 'boolean', default: false },
        news_status: { type: 'varchar(50)' },
        log_message: { type: 'jsonb' },
        log_time: { type: 'timestamp', default: pgm.func('current_timestamp') },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') }
    }, { ifNotExists: true });

    // Users
    pgm.createTable('users', {
        id: 'id',
        firstname: { type: 'varchar(255)' },
        lastname: { type: 'varchar(255)' },
        email: { type: 'varchar(255)', notNull: true, unique: true },
        password_hash: { type: 'varchar(500)', notNull: true },
        role: { type: 'varchar(50)', default: 'Admin' },
        is_active: { type: 'boolean', default: true },
        created_at: { type: 'timestamp', default: pgm.func('current_timestamp') },
        updated_at: { type: 'timestamp', default: pgm.func('current_timestamp') }
    }, { ifNotExists: true });

    // Social Media Posts
    pgm.createTable('social_media_posts', {
        id: 'id',
        twitter_id: { type: 'varchar(255)', unique: true },
        handler: { type: 'varchar(255)' },
        tweet_text: { type: 'text' },
        tweeted_time: { type: 'timestamp' },
        replies: { type: 'integer', default: 0 },
        retweets: { type: 'integer', default: 0 },
        likes: { type: 'integer', default: 0 },
        embedded_url: { type: 'text' },
        images: { type: 'text' },
        videos: { type: 'text' },
        is_posted: { type: 'boolean', default: false },
        website_ids: { type: 'jsonb', default: '[]' },
        posted_datetime: { type: 'timestamp' },
        scraped_time: { type: 'timestamp', default: pgm.func('current_timestamp') },
        source: { type: 'varchar(20)', default: 'x' },
        post_title: { type: 'text' },
        score: { type: 'integer', default: 0 },
        permalink: { type: 'text' }
    }, { ifNotExists: true });
};

exports.down = (pgm) => {
    pgm.dropTable('social_media_posts', { ifExists: true });
    pgm.dropTable('users', { ifExists: true });
    pgm.dropTable('news_logs', { ifExists: true });
    pgm.dropTable('news_prompts', { ifExists: true });
    pgm.dropTable('websites', { ifExists: true });
};
