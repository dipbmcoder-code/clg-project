"""
Social Media Post DB Operations
Handles inserting scraped posts (from Reddit and X) into the database.
"""
from publication.db import get_data, insert_db, get_data_one
from datetime import datetime, timedelta
from publication.utils import sql_value
import json


def insert_social_media_post(post_data, key=None):
    """
    Insert a social media post into the database.
    Supports both Reddit and X post formats via standardized fields.
    
    Args:
        post_data: Standardized post dict (from reddit_scraper or x_scraper)
        key: Optional key for message tracking
    """
    try:
        # Use post_id (new) or twitter_id (legacy) as the unique key
        post_id = post_data.get("post_id") or post_data.get("twitter_id")
        source = post_data.get("source", "x")
        handler = post_data.get("source_handle") or post_data.get("handler", "unknown")

        # Parse timestamp
        tweeted_time = None
        raw_ts = post_data.get("timestamp")
        if raw_ts:
            try:
                tweeted_time = datetime.fromisoformat(str(raw_ts).replace("Z", "+00:00"))
            except (ValueError, TypeError):
                tweeted_time = datetime.now()

        mapped = {
            "twitter_id": post_id,
            "handler": handler,
            "tweet_text": post_data.get("tweet_text"),
            "tweeted_time": tweeted_time,
            "replies": int(post_data.get("replies", 0)),
            "retweets": int(post_data.get("retweets", 0)),
            "embedded_url": post_data.get("embedded_url"),
            "images": json.dumps(post_data.get("images")) if post_data.get("images") else None,
            "videos": json.dumps(post_data.get("videos")) if post_data.get("videos") else None,
            "scraped_time": datetime.now(),
            "source": source,
            "post_title": post_data.get("post_title"),
            "score": int(post_data.get("score", 0)),
            "permalink": post_data.get("permalink"),
        }

        # Keep only fields that are not None
        filtered = {k: v for k, v in mapped.items() if v is not None}

        columns = ", ".join(filtered.keys())
        values = ", ".join([sql_value(v) for v in filtered.values()])

        insert_query = (
            f"INSERT INTO social_media_posts ({columns}) "
            f"VALUES ({values}) "
            f"ON CONFLICT (twitter_id) DO NOTHING;"
        )
        insert_db(insert_query, key)

        # Return the inserted record
        escaped_id = str(post_id).replace("'", "''")
        db_query = f"SELECT id, twitter_id, is_posted, website_ids, handler, source FROM social_media_posts WHERE twitter_id='{escaped_id}';"
        db_post = get_data_one(db_query)
        return db_post

    except Exception as e:
        print(f"Error inserting social media post: {e}")
        return None


def current_db_social_media_posts():
    """Get recent social media posts from database (today + yesterday)."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    db_query = (
        f"SELECT id, twitter_id, is_posted, website_ids, handler, source "
        f"FROM social_media_posts "
        f"WHERE DATE(scraped_time)='{current_date}' OR DATE(scraped_time)='{yesterday_date}';"
    )
    posts = get_data(db_query)
    return posts if posts else []
     