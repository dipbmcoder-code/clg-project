-- CreateEnum
CREATE TYPE "Role" AS ENUM ('SUPER_ADMIN', 'ADMIN', 'AGENT');

-- CreateTable
CREATE TABLE "users" (
    "id" SERIAL NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "role" "Role" NOT NULL DEFAULT 'AGENT',
    "is_active" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "websites" (
    "id" SERIAL NOT NULL,
    "platform_name" TEXT NOT NULL,
    "platform_url" TEXT NOT NULL,
    "platform_user" TEXT NOT NULL,
    "platform_password" TEXT NOT NULL,
    "website_author" TEXT,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "is_validated" BOOLEAN NOT NULL DEFAULT false,
    "type_status" TEXT NOT NULL DEFAULT 'draft',
    "featured_image" TEXT NOT NULL DEFAULT 'upload',
    "l_version" TEXT NOT NULL DEFAULT 'eng',
    "enable_match_reviews" BOOLEAN NOT NULL DEFAULT false,
    "enable_match_previews" BOOLEAN NOT NULL DEFAULT false,
    "enable_social_media" BOOLEAN NOT NULL DEFAULT false,
    "enabled_player_abroad" BOOLEAN NOT NULL DEFAULT false,
    "enable_player_profiles" BOOLEAN NOT NULL DEFAULT false,
    "enable_transfer_rumors" BOOLEAN NOT NULL DEFAULT false,
    "enabled_where_to_watch" BOOLEAN NOT NULL DEFAULT false,
    "match_reviews_time" INTEGER,
    "match_previews_time" INTEGER,
    "where_to_watch_days" INTEGER,
    "website_leagues" JSONB,
    "platform_countries" JSONB,
    "twitter_handles" JSONB,
    "social_media_categories" JSONB,
    "player_abroad_countries" JSONB,
    "player_abroad_categories" JSONB,
    "player_profiles" JSONB,
    "player_profiles_categories" JSONB,
    "transfer_categories" JSONB,
    "rumors_categories" JSONB,
    "transfer_rumour_countries" JSONB,
    "where_to_watch_countries" JSONB,
    "where_to_watch_categories" JSONB,
    "manual_preview_categories" JSONB,
    "manual_review_categories" JSONB,
    "openai_prompt" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "websites_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "news_prompts" (
    "id" SERIAL NOT NULL,
    "preview_news_image_prompt" TEXT,
    "preview_news_title_prompt" TEXT,
    "preview_news_content_prompt" TEXT,
    "review_news_image_prompt" TEXT,
    "review_news_title_prompt" TEXT,
    "review_news_content_prompt" TEXT,
    "social_media_news_image_prompt" TEXT,
    "social_media_news_title_prompt" TEXT,
    "social_media_news_content_prompt" TEXT,
    "player_abroad_news_image_prompt" TEXT,
    "player_abroad_news_title_prompt" TEXT,
    "player_abroad_news_content_prompt" TEXT,
    "player_profile_news_image_prompt" TEXT,
    "player_profile_news_title_prompt" TEXT,
    "player_profile_news_content_prompt" TEXT,
    "transfer_news_image_prompt" TEXT,
    "transfer_news_title_prompt" TEXT,
    "transfer_news_content_prompt" TEXT,
    "rumor_news_image_prompt" TEXT,
    "rumor_news_title_prompt" TEXT,
    "rumor_news_content_prompt" TEXT,
    "where_to_watch_news_image_prompt" TEXT,
    "where_to_watch_news_title_prompt" TEXT,
    "where_to_watch_news_content_prompt" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "news_prompts_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "manual_news" (
    "id" SERIAL NOT NULL,
    "news_type" TEXT NOT NULL,
    "home_team" TEXT,
    "away_team" TEXT,
    "home_score" INTEGER,
    "away_score" INTEGER,
    "home_pos" INTEGER,
    "away_pos" INTEGER,
    "league" JSONB,
    "summary" TEXT,
    "goalscorers" JSONB,
    "venue" TEXT,
    "match_date" TIMESTAMP(3),
    "players_to_watch" JSONB,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "manual_news_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "manual_news_websites" (
    "id" SERIAL NOT NULL,
    "manual_news_id" INTEGER NOT NULL,
    "website_id" INTEGER NOT NULL,

    CONSTRAINT "manual_news_websites_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "website_news" (
    "id" SERIAL NOT NULL,
    "title" TEXT,
    "content" TEXT,
    "image_url" TEXT,
    "regenerated" BOOLEAN NOT NULL DEFAULT false,
    "manual_news_id" INTEGER,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "website_news_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "news_logs" (
    "id" SERIAL NOT NULL,
    "news_type" TEXT NOT NULL,
    "title" TEXT,
    "website_name" TEXT,
    "news_status" TEXT NOT NULL DEFAULT 'Published',
    "log_time" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "image_generated" BOOLEAN NOT NULL DEFAULT false,
    "log_message" JSONB,
    "website_id" INTEGER,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "news_logs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ai_settings" (
    "id" SERIAL NOT NULL,
    "openai_api_key" TEXT,
    "openai_model" TEXT NOT NULL DEFAULT 'gpt-4',
    "openrouter_api_key" TEXT,
    "openrouter_model" TEXT,
    "gemini_api_key" TEXT,
    "gemini_model" TEXT NOT NULL DEFAULT 'gemini-pro',
    "content_service" TEXT NOT NULL DEFAULT 'openai',
    "image_service" TEXT NOT NULL DEFAULT 'gemini',
    "rapidapi_key" TEXT,
    "aws_access_key" TEXT,
    "aws_secret_key" TEXT,
    "aws_s3_bucket" TEXT,
    "aws_region" TEXT,
    "sendgrid_api_key" TEXT,
    "alert_email" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "ai_settings_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "social_media_configs" (
    "id" SERIAL NOT NULL,
    "website_id" INTEGER NOT NULL,
    "twitter_enabled" BOOLEAN NOT NULL DEFAULT false,
    "twitter_api_key" TEXT,
    "twitter_api_secret" TEXT,
    "twitter_access_token" TEXT,
    "twitter_access_secret" TEXT,
    "twitter_bearer_token" TEXT,
    "reddit_enabled" BOOLEAN NOT NULL DEFAULT false,
    "reddit_client_id" TEXT,
    "reddit_client_secret" TEXT,
    "reddit_username" TEXT,
    "reddit_password" TEXT,
    "reddit_subreddits" JSONB,
    "auto_post_on_publish" BOOLEAN NOT NULL DEFAULT true,
    "post_template" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "social_media_configs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "wordpress_categories" (
    "id" SERIAL NOT NULL,
    "wp_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "parent_id" INTEGER,
    "count" INTEGER NOT NULL DEFAULT 0,
    "website_id" INTEGER NOT NULL,
    "synced_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "wordpress_categories_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "social_media_posts" (
    "id" SERIAL NOT NULL,
    "platform" TEXT NOT NULL,
    "post_id" TEXT,
    "post_url" TEXT,
    "title" TEXT,
    "content" TEXT,
    "article_url" TEXT,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "error" TEXT,
    "website_id" INTEGER,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "social_media_posts_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE UNIQUE INDEX "manual_news_websites_manual_news_id_website_id_key" ON "manual_news_websites"("manual_news_id", "website_id");

-- CreateIndex
CREATE UNIQUE INDEX "social_media_configs_website_id_key" ON "social_media_configs"("website_id");

-- CreateIndex
CREATE UNIQUE INDEX "wordpress_categories_website_id_wp_id_key" ON "wordpress_categories"("website_id", "wp_id");

-- AddForeignKey
ALTER TABLE "manual_news_websites" ADD CONSTRAINT "manual_news_websites_manual_news_id_fkey" FOREIGN KEY ("manual_news_id") REFERENCES "manual_news"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "manual_news_websites" ADD CONSTRAINT "manual_news_websites_website_id_fkey" FOREIGN KEY ("website_id") REFERENCES "websites"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "website_news" ADD CONSTRAINT "website_news_manual_news_id_fkey" FOREIGN KEY ("manual_news_id") REFERENCES "manual_news"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "news_logs" ADD CONSTRAINT "news_logs_website_id_fkey" FOREIGN KEY ("website_id") REFERENCES "websites"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "social_media_configs" ADD CONSTRAINT "social_media_configs_website_id_fkey" FOREIGN KEY ("website_id") REFERENCES "websites"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "wordpress_categories" ADD CONSTRAINT "wordpress_categories_website_id_fkey" FOREIGN KEY ("website_id") REFERENCES "websites"("id") ON DELETE CASCADE ON UPDATE CASCADE;
