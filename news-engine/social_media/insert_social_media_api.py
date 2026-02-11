from publication.db import get_data, insert_db, get_data_one
from datetime import datetime, timedelta
from publication.utils import sql_value
import json
def insert_social_media_post(post_data, key=None):
    """Insert social media post into database
    
    Args:
        post_data: Dictionary containing tweet data
        key: Optional key for message tracking
    """
    try:
        # website_ids = f"'{json.dumps(website_ids)}'::jsonb"
 
        mapped = {
            "twitter_id": post_data.get('twitter_id'),
            "handler": post_data.get('handler'),
            # "website_ids": website_ids,
            "tweet_text": post_data.get('tweet_text'),
            "tweeted_time": (
                datetime.fromisoformat(post_data['timestamp'].replace('Z', '+00:00'))
                if post_data.get('timestamp') else None
            ),
            "replies": int(post_data.get('replies', 0)),
            "retweets": int(post_data.get('retweets', 0)),
            "embedded_url": post_data.get('embedded_url'),
            "images": json.dumps(post_data.get('images')) if post_data.get('images') else None,
            "videos": json.dumps(post_data.get('videos')) if post_data.get('videos') else None,
            "scraped_time": datetime.now()
        }

        # Keep only fields that are not None
        filtered = {k: v for k, v in mapped.items() if v is not None}

        # Build dynamic SQL string
        columns = ", ".join(filtered.keys())
        values = ", ".join([sql_value(v) for v in filtered.values()])

        insert_query = (
            f"INSERT INTO social_media_posts ({columns}) "
            f"VALUES ({values}) "
            f"ON CONFLICT (twitter_id) DO NOTHING;"
        )
        insert_db(insert_query, key)  # Pass key for message tracking

        # Return the inserted record
        db_query = f"SELECT id, twitter_id, is_posted, website_ids, handler FROM social_media_posts WHERE twitter_id='{post_data.get('twitter_id')}';"
        db_post = get_data_one(db_query)
        return db_post
        
    except Exception as e:
        print(f"Error inserting social media post: {e}")
        return None

def current_db_social_media_posts():
    """Get current date social media posts from database"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    db_query = (
        f"SELECT id, twitter_id, is_posted, website_ids, handler FROM social_media_posts WHERE DATE(scraped_time)='{current_date}' OR DATE(scraped_time)='{yesterday_date}';"
    )
    posts = get_data(db_query)
    return posts if posts else []
     