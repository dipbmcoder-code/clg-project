"""
X (Twitter) Scraper Wrapper
Uses the existing Selenium-based scraper (no paid API key needed).
Normalizes field names to match the standardized post format.
Includes retry logic with exponential backoff.
"""
import os
import sys
import time
import random
from datetime import datetime, timezone
from typing import List, Dict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from publication.social_scraper import scrap_social_media_data

# ── Constants ──
MAX_RETRIES = 2
RETRY_DELAY_BASE = 10  # seconds
BETWEEN_HANDLE_DELAY = (8, 15)  # random range in seconds


def _normalize_scraped_tweet(tweet: Dict) -> Dict:
    """
    Normalize field names from the Selenium scraper to our
    standardized post format used by the pipeline.
    
    Selenium scraper returns:
        tweeted_time, url, handler, twitter_id, tweet_text, replies, retweets, likes, images
    
    Pipeline expects:
        timestamp, embedded_url, post_id, source, source_handle, post_title, etc.
    """
    twitter_id = tweet.get("twitter_id", "")

    # Parse timestamp from various formats
    raw_time = tweet.get("tweeted_time") or tweet.get("timestamp", "")
    timestamp = raw_time
    if raw_time:
        try:
            if "Z" in str(raw_time):
                dt = datetime.fromisoformat(str(raw_time).replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(str(raw_time))
            timestamp = dt.isoformat()
        except (ValueError, TypeError):
            timestamp = datetime.now(timezone.utc).isoformat()

    handler = tweet.get("handler", "unknown")

    return {
        # Standardized fields
        "post_id": f"x_{twitter_id}" if twitter_id else None,
        "source": "x",
        "source_handle": f"@{handler}",
        "post_title": "",  # Tweets don't have titles
        "tweet_text": tweet.get("tweet_text", ""),
        "timestamp": timestamp,
        "replies": int(tweet.get("replies", 0)),
        "retweets": int(tweet.get("retweets", 0)),
        "likes": int(tweet.get("likes", 0)),
        "score": int(tweet.get("likes", 0)),  # Use likes as score
        "images": tweet.get("images", []),
        "videos": tweet.get("videos", []),
        "embedded_url": tweet.get("url") or tweet.get("embedded_url"),
        "permalink": tweet.get("url") or f"https://x.com/{handler}/status/{twitter_id}",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        # Legacy compatibility aliases
        "twitter_id": f"x_{twitter_id}" if twitter_id else None,
        "handler": handler,
    }


def _scrape_with_retry(handles: List[str]) -> List[Dict]:
    """
    Scrape X handles with retry + exponential backoff.
    Returns raw tweets list.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw_tweets = scrap_social_media_data(handles)
            if raw_tweets:
                return raw_tweets
            print(f"⚠️ X scrape attempt {attempt}/{MAX_RETRIES} returned 0 tweets")
        except Exception as e:
            print(f"⚠️ X scrape attempt {attempt}/{MAX_RETRIES} failed: {e}")

        if attempt < MAX_RETRIES:
            delay = RETRY_DELAY_BASE * attempt + random.uniform(2, 5)
            print(f"   Retrying in {delay:.0f}s...")
            time.sleep(delay)

    return []


def fetch_x_data(handles: List[str], **kwargs) -> List[Dict]:
    """
    Main entry point — fetch tweets from X/Twitter handles using Selenium scraping.
    No API key required. Includes retry logic.

    Args:
        handles: List of X/Twitter handles (without @)

    Returns:
        List of standardized post dicts
    """
    if not handles:
        print("⚠️ No X handles provided")
        return []

    # Clean handles
    clean_handles = [h.strip().replace("@", "") for h in handles if h.strip()]

    print(f"🔍 Scraping X posts for {len(clean_handles)} handles: {clean_handles}")

    try:
        raw_tweets = _scrape_with_retry(clean_handles)
        normalized = []

        for tweet in raw_tweets:
            post = _normalize_scraped_tweet(tweet)
            if post.get("post_id"):
                normalized.append(post)

        print(f"✅ Scraped {len(normalized)} posts from X")
        return normalized

    except Exception as e:
        print(f"❌ Error in fetch_x_data: {e}")
        return []


if __name__ == "__main__":
    test_handles = ["elikibaara"]
    print(f"🚀 Scraping X posts for {test_handles}")
    results = fetch_x_data(test_handles)

    for p in results:
        print(f"  [@{p['handler']}] {p['tweet_text'][:60]}... (likes: {p['likes']})")
