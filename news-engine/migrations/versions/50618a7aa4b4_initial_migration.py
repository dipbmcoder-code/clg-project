"""initial migration

Revision ID: 50618a7aa4b4
Revises: 
Create Date: 2025-10-13 17:21:10.222827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50618a7aa4b4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
    CREATE TABLE IF NOT EXISTS "public"."match_preview" (
        "fixture_match" integer,
        "name_home_preview" text,
        "name_away_preview" text,
        "date_match" text,
        "venue" text,
        "id_team_home_preview" text,
        "id_team_away_preview" text,
        "league" text,
        "season" text,
        "rank_team_home" text,
        "rank_team_away" text,
        "players_a_name" text,
        "players_a_goals_total" text,
        "players_b_name" text,
        "players_b_goals_total" text,
        "topscorers_assists_home_name" text,
        "topscorers_assists_home_amount" text,
        "topscorers_assists_away_name" text,
        "topscorers_assists_away_amount" text,
        "topscorers_interceptions_home_name" text,
        "topscorers_interceptions_home_amount" text,
        "topscorers_interceptions_away_name" text,
        "topscorers_interceptions_away_amount" text,
        "topscorers_duels_home_name" text,
        "topscorers_duels_home_amount" text,
        "topscorers_duels_away_name" text,
        "topscorers_duels_away_amount" text,
        "topscorers_saves_home_name" text,
        "topscorers_saves_home_amount" text,
        "topscorers_saves_away_name" text,
        "topscorers_saves_away_amount" text,
        "fixture_match3" integer,
        "date_match2" integer,
        "topscorer_name_in_league_1" text,
        "topscorer_name_in_league_2" text,
        "topscorer_name_in_league_3" text,
        "topscorer_amount_in_league_1" text,
        "topscorer_amount_in_league_2" text,
        "topscorer_amount_in_league_3" text,
        "topscorer_team_in_league_1" text,
        "topscorer_team_in_league_2" text,
        "topscorer_team_in_league_3" text,
        "home_play_clean_sheet" text,
        "home_biggest_win_in_home" text,
        "home_biggest_win_in_away" text,
        "home_biggest_lose_in_home" text,
        "home_biggest_lose_in_away" text,
        "away_play_clean_sheet" text,
        "away_biggest_win_in_home" text,
        "away_biggest_win_in_away" text,
        "away_biggest_lose_in_home" text,
        "away_biggest_lose_in_away" text,
        "home_win_once_in_home" text,
        "home_lose_once_in_home" text,
        "home_draws_once_in_home" text,
        "away_win_once_in_away" text,
        "away_lose_once_in_away" text,
        "away_draws_once_in_away" text,
        "list_minute" text,
        "list_minute_for_goals_home" text,
        "list_for_goal_home" text,
        "list_minute_missed_goals_home" text,
        "list_missed_goal_home" text,
        "list_minute_for_goals_away" text,
        "list_for_goal_away" text,
        "list_minute_missed_goals_away" text,
        "list_missed_goal_away" text,
        "predictions_percent_home" text,
        "predictions_percent_away" text,
        "predictions_percent_draw" text,
        "predictions_goals_home" text,
        "predictions_goals_away" text,
        "form_home" text,
        "form_away" text,
        "bk_coef_name" text,
        "bk_coef_home" text,
        "bk_coef_draw" text,
        "bk_coef_away" text,
        "h2h_home_total_games" text,
        "h2h_home_total_wins_in_home" text,
        "h2h_home_total_wins_in_away" text,
        "h2h_home_total_draws_in_home" text,
        "h2h_home_total_draws_in_away" text,
        "h2h_home_total_loses_in_home" text,
        "h2h_home_total_loses_in_away" text,
        "h2h_away_total_games" text,
        "h2h_away_total_wins_home" text,
        "h2h_away_total_wins_away" text,
        "h2h_away_total_draws_in_home" text,
        "h2h_away_total_draws_in_away" text,
        "h2h_away_total_loses_in_home" text,
        "h2h_away_total_loses_in_away" text,
        "comparison_total_home" text,
        "comparison_att_home" text,
        "comparison_def_home" text,
        "comparison_h2h_home" text,
        "comparison_goals_home" text,
        "comparison_total_away" text,
        "comparison_att_away" text,
        "comparison_def_away" text,
        "comparison_h2h_away" text,
        "comparison_goals_away" text,
        "name_league" text,
        "topscorer_name_in_league_4" text,
        "topscorer_name_in_league_5" text,
        "topscorer_amount_in_league_4" text,
        "topscorer_amount_in_league_5" text,
        "topscorer_team_in_league_4" text,
        "topscorer_team_in_league_5" text,
        "name_home_top_fouls_yel_card" text,
        "amount_home_fouls_yel_card" text,
        "name_away_top_fouls_yel_card" text,
        "amount_away_fouls_yel_card" text,
        "name_home_top_fouls_red_card" text,
        "amount_home_fouls_red_card" text,
        "name_away_top_fouls_red_card" text,
        "amount_away_fouls_red_card" text,
        "round" text,
        "fixture_last_game_home" text,
        "fixture_last_game_away" text,
        "topscorers_blocks_home_name" text,
        "topscorers_blocks_home_amount" text,
        "topscorers_blocks_away_name" text,
        "topscorers_blocks_away_amount" text,
        "topscorers_fouls_home_name" text,
        "topscorers_fouls_home_amount" text,
        "topscorers_fouls_away_name" text,
        "topscorers_fouls_away_amount" text,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamp,
        "website_ids" jsonb
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."match_review" (
        "fixture_match" text,
        "name_home_review" text,
        "name_away_review" text,
        "lineups_home" text,
        "lineups_away" text,
        "gone_player_home" text,
        "gone_player_away" text,
        "came_player_home" text,
        "came_player_away" text,
        "time_subst_home" text,
        "time_subst_away" text,
        "time_home_goal" text,
        "player_home_goal" text,
        "time_away_goal" text,
        "player_away_goal" text,
        "time_home_yellow" text,
        "player_home_yellow" text,
        "time_away_yellow" text,
        "player_away_yellow" text,
        "time_home_red" text,
        "player_home_red" text,
        "time_away_red" text,
        "player_away_red" text,
        "name_home_top_shots" text,
        "name_away_top_shots" text,
        "name_home_top_block" text,
        "name_away_top_block" text,
        "name_home_top_interceptions" text,
        "name_away_top_interceptions" text,
        "ball_possession_home" text,
        "ball_possession_away" text,
        "name_home_top_duels" text,
        "name_away_top_duels" text,
        "home_next_match_rival" text,
        "home_date_match_vs_rival" text,
        "home_next_venue_vs_rival" text,
        "away_next_match_rival" text,
        "away_date_match_vs_rival" text,
        "away_venue_vs_rival" text,
        "topscorer_name_in_league_1" text,
        "topscorer_name_in_league_2" text,
        "topscorer_name_in_league_3" text,
        "topscorer_amount_in_league_1" text,
        "topscorer_amount_in_league_2" text,
        "topscorer_amount_in_league_3" text,
        "topscorer_team_in_league_1" text,
        "topscorer_team_in_league_2" text,
        "topscorer_team_in_league_3" text,
        "fixture_match_for_check" integer,
        "goals_home" text,
        "goals_away" text,
        "shots_on_goal_home" text,
        "shots_off_goal_home" text,
        "amount_home_shots" text,
        "amount_away_shots" text,
        "total_assists_home" text,
        "total_assists_away" text,
        "total_shots_home" text,
        "total_shots_away" text,
        "total_shots_on" text,
        "total_shots_off" text,
        "total_blocks_home" text,
        "amount_home_block" text,
        "total_blocks_away" text,
        "amount_away_block" text,
        "total_interceptions_home" text,
        "amount_home_interceptions" text,
        "total_interceptions_away" text,
        "amount_away_interceptions" text,
        "amount_home_duels" text,
        "amount_away_duels" text,
        "shots_on_goal_away" text,
        "shots_off_goal_away" text,
        "name_home_top_goals" text,
        "amount_home_goals" text,
        "name_away_top_goals" text,
        "amount_away_goals" text,
        "name_home_top_assists" text,
        "amount_home_assists" text,
        "name_away_top_assists" text,
        "amount_away_assists" text,
        "name_home_top_saves" text,
        "amount_home_saves" text,
        "name_away_top_saves" text,
        "amount_away_saves" text,
        "id_team_home_review" integer,
        "id_team_away_review" integer,
        "league" text,
        "venue" text,
        "date_match3" text,
        "player_home_penalti" text,
        "time_home_penalti" text,
        "player_away_penalti" text,
        "time_away_penalti" text,
        "form_home" text,
        "form_away" text,
        "topscorer_name_in_league_4" text,
        "topscorer_amount_in_league_4" text,
        "topscorer_team_in_league_4" text,
        "topscorer_name_in_league_5" text,
        "topscorer_amount_in_league_5" text,
        "topscorer_team_in_league_5" text,
        "rank_for_table" text,
        "name_table_team" text,
        "form_table" text,
        "all_matches_table" text,
        "win_matches_table" text,
        "draw_matches_table" text,
        "lose_matches_table" text,
        "goals_scored_for_table" text,
        "goals_missed_for_table" text,
        "goals_diff_table" text,
        "points_for_table" text,
        "logo_for_table" text,
        "league_name" text,
        "name_home_top_fouls_yel_card" text,
        "amount_home_fouls_yel_card" text,
        "name_away_top_fouls_yel_card" text,
        "amount_away_fouls_yel_card" text,
        "name_home_top_fouls_red_card" text,
        "amount_home_fouls_red_card" text,
        "name_away_top_fouls_red_card" text,
        "amount_away_fouls_red_card" text,
        "name_home_top_pass_accuracy" text,
        "top__home_precent_accuracy" text,
        "top__home_total_passes" text,
        "name_away_top_pass_accuracy" text,
        "top__away_precent_accuracy" text,
        "top__away_total_passes" text,
        "name_home_top_pass_key" text,
        "top__home_amount_key" text,
        "name_away_top_pass_key" text,
        "top__away_amount_key" text,
        "round" text,
        "team_home_passes_accurate" text,
        "team_away_passes_accurate" text,
        "team_home_percent_passes_accurate" text,
        "team_away_percent_passes_accurate" text,
        "team_home_total_passes" text,
        "team_away_total_passes" text,
        "injuries_count" text,
        "total_cards_in_game" text,
        "count_yel_card" text,
        "count_red_card" text,
        "match_lasted" text,
        "referee_time" text,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamp,
        "website_ids" jsonb
    ) WITH (oids = false);

    CREATE SEQUENCE IF NOT EXISTS player_abroads_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

    CREATE TABLE IF NOT EXISTS "public"."player_abroads" (
        "id" integer DEFAULT nextval('player_abroads_id_seq') NOT NULL,
        "fixture_id" bigint,
        "match_date" timestamptz,
        "venue" text,
        "city" text,
        "league_id" bigint,
        "league_name" text,
        "league_country" text,
        "league_season" integer,
        "home_team" text,
        "away_team" text,
        "home_score" integer,
        "away_score" integer,
        "player_id" bigint,
        "player_name" text,
        "event_type" text,
        "event_detail" text,
        "team_name" text,
        "team_id" bigint,
        "minutes_played" integer,
        "goals_count" integer,
        "firstname" text,
        "lastname" text,
        "age" integer,
        "birth_date" date,
        "birth_place" text,
        "birth_country" text,
        "nationality" text,
        "height" text,
        "weight" text,
        "injured" boolean,
        "photo" text,
        "statistics" jsonb,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamptz,
        "create_datetime" timestamptz,
        "website_ids" jsonb,
        CONSTRAINT "player_abroads_pkey" PRIMARY KEY ("id")
    ) WITH (oids = false);

    CREATE SEQUENCE IF NOT EXISTS player_profiles_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1;

    CREATE TABLE IF NOT EXISTS "public"."player_profiles" (
        "id" bigint DEFAULT nextval('player_profiles_id_seq') NOT NULL,
        "player_id" bigint NOT NULL,
        "name" text,
        "firstname" text,
        "lastname" text,
        "age" integer,
        "birth_date" date,
        "birth_place" text,
        "birth_country" text,
        "nationality" text,
        "height" text,
        "weight" text,
        "number" integer,
        "position" text,
        "photo" text,
        "injured" boolean,
        "statistics" jsonb,
        "transfers" jsonb,
        "trophies" jsonb,
        "website_ids" jsonb,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamptz,
        "create_datetime" timestamptz DEFAULT now(),
        "last_updated_transfer" timestamptz,
        CONSTRAINT "player_profiles_pkey" PRIMARY KEY ("id")
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."players" (
        "name" text,
        "team_id" integer,
        "league_id" integer,
        "goals" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."players_round" (
        "player_id_api" integer,
        "name" character varying(255),
        "league_id" integer,
        "team_id" integer,
        "round" integer,
        "fixture_match" integer,
        "goalsassists" integer,
        "y_cards" integer,
        "r_cards" integer,
        "blocks" integer,
        "interceptions" integer,
        "saves" integer,
        "duels" integer,
        "conceded" integer,
        "injuries" integer,
        "fast_goal" integer,
        "penalty" integer,
        "season" integer,
        "goals" integer,
        "assists" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."players_test" (
        "player_id_api" integer,
        "name" text,
        "league_id" integer,
        "team_id" integer,
        "season" integer,
        "goals" integer,
        "assists" integer,
        "y_cards" integer,
        "r_cards" integer,
        "blocks" integer,
        "interceptions" integer,
        "saves" integer,
        "duels" integer,
        "conceded" integer,
        "injuries" integer,
        "fast_goal" integer,
        "penalty" integer,
        "fixture_match_for_fast_goal" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."post_preview" (
        "fixture_match" integer,
        "website_ids" jsonb
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."post_review" (
        "fixture_match" integer,
        "website_ids" jsonb
    ) WITH (oids = false);

    CREATE SEQUENCE IF NOT EXISTS rumours_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

    CREATE TABLE IF NOT EXISTS "public"."rumours" (
        "player_id" bigint NOT NULL,
        "player_name" character varying(255),
        "profile_url" text,
        "position" character varying(100),
        "age" integer,
        "nationality" character varying(100),
        "current_club" character varying(255),
        "date_of_birth_text" character varying(50),
        "date_of_birth" date,
        "calculated_age" integer,
        "place_of_birth" character varying(255),
        "height" character varying(50),
        "nationalities" text[],
        "main_position" character varying(100),
        "preferred_foot" character varying(50),
        "national_team" character varying(255),
        "date_of_joined" date,
        "social_media" jsonb,
        "market_value" character varying(100),
        "current_rumour" jsonb,
        "mv_history" jsonb,
        "transfer_history" jsonb,
        "scraped_timestamp" timestamp,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamp,
        "posted_wordpress_urls" text[],
        "contract_expires" date,
        "last_update_mv" date,
        "website_ids" jsonb,
        "last_reply_time" timestamp,
        "id" integer DEFAULT nextval('rumours_id_seq') NOT NULL,
        CONSTRAINT "rumours_pkey" PRIMARY KEY ("id")
    ) WITH (oids = false);

    CREATE SEQUENCE IF NOT EXISTS social_media_posts_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

    CREATE TABLE IF NOT EXISTS "public"."social_media_posts" (
        "id" integer DEFAULT nextval('social_media_posts_id_seq') NOT NULL,
        "twitter_id" character varying(100),
        "handler" character varying(100),
        "tweet_text" text,
        "tweeted_time" timestamp,
        "replies" integer DEFAULT '0',
        "retweets" integer DEFAULT '0',
        "embedded_url" text,
        "scraped_time" timestamp DEFAULT CURRENT_TIMESTAMP,
        "is_posted" boolean DEFAULT false,
        "post_datetime" timestamp,
        "posted_wordpress_url" text,
        "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
        "updated_at" timestamp DEFAULT CURRENT_TIMESTAMP,
        "website_ids" jsonb,
        "images" jsonb,
        "videos" jsonb,
        CONSTRAINT "social_media_posts_pkey" PRIMARY KEY ("id"),
        CONSTRAINT "social_media_posts_twitter_id_key" UNIQUE ("twitter_id")
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."subscribe" (
        "id_user" integer,
        "type_subscribe" text
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."teams" (
        "team_id_api" integer DEFAULT '0',
        "wins" integer DEFAULT '0',
        "loses" integer DEFAULT '0',
        "draws" integer DEFAULT '0',
        "clean_sheet_count" integer DEFAULT '0',
        "goals" integer DEFAULT '0',
        "without_scored_count" integer DEFAULT '0',
        "conceded_goals" integer DEFAULT '0',
        "conceded_goals_count" integer DEFAULT '0',
        "injuries_count" integer DEFAULT '0',
        "name" character varying(255) NOT NULL,
        "season" integer DEFAULT '0',
        "league_id" integer NOT NULL,
        "destroyer_total" integer,
        "creator_total" integer,
        "interceptions" integer,
        "blocks" integer,
        "saves" integer,
        "tackles" integer,
        "duels" integer,
        "shots_on_target" integer,
        "shots_of_target" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."teams_cup" (
        "id" integer NOT NULL,
        "name" character(1),
        "team_id_api" integer,
        "season" integer,
        "wins" integer,
        "teams_round" integer,
        "form" character(1),
        "loses" integer,
        "draws" integer,
        "clean_sheet_count" integer,
        "goals" integer,
        "without_scored_count" integer,
        "conceded_goals" integer,
        "conceded_goals_count" integer,
        "injuries_count" integer,
        "league_id" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."teams_round" (
        "team_id_api" integer DEFAULT '0',
        "wins" integer DEFAULT '0',
        "loses" integer DEFAULT '0',
        "draws" integer DEFAULT '0',
        "clean_sheet_count" integer DEFAULT '0',
        "goals" integer DEFAULT '0',
        "without_scored_count" integer DEFAULT '0',
        "conceded_goals" integer DEFAULT '0',
        "conceded_goals_count" integer DEFAULT '0',
        "injuries_count" integer DEFAULT '0',
        "name" character varying(255) NOT NULL,
        "season" integer DEFAULT '0',
        "league_id" integer NOT NULL,
        "round" integer NOT NULL,
        "interceptions" integer,
        "precent_accuracy" integer,
        "blocks" integer,
        "saves" integer,
        "duels" integer,
        "shots_on_target" integer,
        "shots_of_target" integer,
        "tackles" integer,
        "destroyer_total" integer,
        "creator_total" integer
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."teams_test" (
        "id" integer NOT NULL,
        "name" character(1),
        "team_id_api" integer,
        "season" integer,
        "wins" integer,
        "teams_round" integer,
        "form" character(1),
        "loses" integer,
        "draws" integer,
        "clean_sheet_count" integer,
        "goals" integer,
        "without_scored_count" integer,
        "conceded_goals" integer,
        "conceded_goals_count" integer,
        "injuries_count" integer,
        "league_id" integer,
        CONSTRAINT "teams_test_pkey" PRIMARY KEY ("id")
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."test" (
        "id" integer NOT NULL,
        "player_name" character varying(255)
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."transfers" (
        "player_id" bigint NOT NULL,
        "player_name" character varying(255),
        "profile_url" text,
        "position" character varying(100),
        "age" integer,
        "nationality" character varying(100),
        "current_club" character varying(255),
        "date_of_birth_text" character varying(50),
        "date_of_birth" date,
        "calculated_age" integer,
        "place_of_birth" character varying(255),
        "height" character varying(50),
        "nationalities" text[],
        "main_position" character varying(100),
        "preferred_foot" character varying(50),
        "national_team" character varying(255),
        "date_of_joined" date,
        "social_media" jsonb,
        "market_value" character varying(100),
        "current_transfer" jsonb,
        "mv_history" jsonb,
        "transfer_history" jsonb,
        "scraped_timestamp" timestamp,
        "is_posted" boolean DEFAULT false,
        "posted_datetime" timestamp,
        "posted_wordpress_urls" text[],
        "contract_expires" date,
        "last_update_mv" date,
        "website_ids" jsonb,
        CONSTRAINT "transfers_pkey" PRIMARY KEY ("player_id")
    ) WITH (oids = false);

    CREATE TABLE IF NOT EXISTS "public"."update_fixture" (
        "fixture_match" integer
    ) WITH (oids = false);

        
    ''')
    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
    DROP TABLE IF EXISTS "match_preview";
    DROP TABLE IF EXISTS "match_review";
    DROP TABLE IF EXISTS "player_abroads";
    DROP SEQUENCE IF EXISTS player_abroads_id_seq;
    DROP TABLE IF EXISTS "player_profiles";
    DROP SEQUENCE IF EXISTS player_profiles_id_seq;
    DROP TABLE IF EXISTS "players";
    DROP TABLE IF EXISTS "players_round";
    DROP TABLE IF EXISTS "players_test";
    DROP TABLE IF EXISTS "post_preview";
    DROP TABLE IF EXISTS "post_review";
    DROP TABLE IF EXISTS "rumours";
    DROP SEQUENCE IF EXISTS rumours_id_seq;
    DROP TABLE IF EXISTS "social_media_posts";
    DROP SEQUENCE IF EXISTS social_media_posts_id_seq;
    DROP TABLE IF EXISTS "subscribe";
    DROP TABLE IF EXISTS "teams";
    DROP TABLE IF EXISTS "teams_cup";
    DROP TABLE IF EXISTS "teams_round";
    DROP TABLE IF EXISTS "teams_test";
    DROP TABLE IF EXISTS "transfers";
    DROP TABLE IF EXISTS "update_fixture";
    ''')
