"""
Reddit Scraper Module — PRAW Integration
Fetches posts from subreddits using Reddit's free API via PRAW.
Returns standardized post objects compatible with the social media pipeline.
"""
import os
import praw
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Reddit API credentials (free — register at reddit.com/prefs/apps)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "AINewsGenerator/1.0")


class RedditScraper:
    """Scrapes posts from Reddit subreddits using PRAW (free API)."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        self.client_id = client_id or REDDIT_CLIENT_ID
        self.client_secret = client_secret or REDDIT_CLIENT_SECRET
        self.user_agent = user_agent or REDDIT_USER_AGENT

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Reddit API credentials required. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env. "
                "Register free at https://www.reddit.com/prefs/apps/"
            )

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
        # Read-only mode — no user login needed
        self.reddit.read_only = True

    def _parse_post(self, post, subreddit_name: str) -> Dict:
        """
        Convert a PRAW Submission to our standardized post format.
        Mirrors the tweet object shape for pipeline compatibility.
        """
        # Extract images
        images = []
        videos = []

        if hasattr(post, "preview") and post.preview:
            for img in post.preview.get("images", []):
                source_url = img.get("source", {}).get("url", "")
                if source_url:
                    images.append(source_url.replace("&amp;", "&"))

        # Direct image URLs
        if hasattr(post, "url") and post.url:
            url_lower = post.url.lower()
            if any(url_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                if post.url not in images:
                    images.append(post.url)

        # Gallery posts
        if hasattr(post, "is_gallery") and post.is_gallery:
            if hasattr(post, "media_metadata") and post.media_metadata:
                for _key, media in post.media_metadata.items():
                    if media.get("status") == "valid" and "s" in media:
                        img_url = media["s"].get("u", "")
                        if img_url:
                            images.append(img_url.replace("&amp;", "&"))

        # Video content
        if hasattr(post, "is_video") and post.is_video:
            if hasattr(post, "media") and post.media:
                reddit_video = post.media.get("reddit_video", {})
                if reddit_video:
                    videos.append(
                        {
                            "type": "video",
                            "url": reddit_video.get("fallback_url", ""),
                            "preview_image_url": (
                                images[0] if images else ""
                            ),
                        }
                    )

        # Build the embedded URL (the actual linked content)
        embedded_url = None
        if not post.is_self and post.url:
            embedded_url = post.url

        # Build post text: title + selftext for self-posts, just title for links
        post_text = post.title
        if post.selftext and len(post.selftext.strip()) > 0:
            # Truncate very long self-text for pipeline processing
            selftext = post.selftext[:2000]
            post_text = f"{post.title}\n\n{selftext}"

        # Convert UTC timestamp
        created_utc = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

        return {
            # Standardized fields (compatible with existing pipeline)
            "post_id": f"reddit_{post.id}",
            "source": "reddit",
            "source_handle": f"r/{subreddit_name}",
            "post_title": post.title,
            "tweet_text": post_text,  # Keep field name for pipeline compat
            "timestamp": created_utc.isoformat(),
            "replies": post.num_comments,
            "retweets": 0,  # Reddit doesn't have retweets
            "likes": post.score,
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "images": images,
            "videos": videos,
            "embedded_url": embedded_url,
            "permalink": f"https://reddit.com{post.permalink}",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            # Legacy compatibility aliases
            "twitter_id": f"reddit_{post.id}",
            "handler": f"r/{subreddit_name}",
        }

    def get_hot_posts(
        self, subreddit_name: str, limit: int = 25, hours_ago: int = 12
    ) -> List[Dict]:
        """
        Fetch hot posts from a subreddit, filtered by time.

        Args:
            subreddit_name: Name of subreddit (without r/)
            limit: Max posts to fetch
            hours_ago: Only include posts from the last N hours

        Returns:
            List of standardized post dicts
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
            posts = []

            for post in subreddit.hot(limit=limit):
                created = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                if created >= cutoff:
                    # Skip stickied/pinned posts
                    if post.stickied:
                        continue
                    posts.append(self._parse_post(post, subreddit_name))

            print(f"✅ Fetched {len(posts)} hot posts from r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"❌ Error fetching r/{subreddit_name}: {e}")
            return []

    def get_new_posts(
        self, subreddit_name: str, limit: int = 25, hours_ago: int = 6
    ) -> List[Dict]:
        """Fetch newest posts from a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
            posts = []

            for post in subreddit.new(limit=limit):
                created = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                if created >= cutoff:
                    if post.stickied:
                        continue
                    posts.append(self._parse_post(post, subreddit_name))

            print(f"✅ Fetched {len(posts)} new posts from r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"❌ Error fetching r/{subreddit_name}: {e}")
            return []

    def get_top_posts(
        self, subreddit_name: str, limit: int = 10, time_filter: str = "day"
    ) -> List[Dict]:
        """
        Fetch top posts from a subreddit.

        Args:
            time_filter: One of 'hour', 'day', 'week', 'month', 'year', 'all'
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []

            for post in subreddit.top(time_filter=time_filter, limit=limit):
                if post.stickied:
                    continue
                posts.append(self._parse_post(post, subreddit_name))

            print(f"✅ Fetched {len(posts)} top posts from r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"❌ Error fetching r/{subreddit_name}: {e}")
            return []

    def search_subreddit(
        self, subreddit_name: str, query: str, limit: int = 15, sort: str = "relevance"
    ) -> List[Dict]:
        """Search within a subreddit for specific topics."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []

            for post in subreddit.search(query, sort=sort, limit=limit):
                posts.append(self._parse_post(post, subreddit_name))

            print(f"✅ Found {len(posts)} posts matching '{query}' in r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"❌ Error searching r/{subreddit_name}: {e}")
            return []


def fetch_reddit_data(
    subreddits: List[str],
    mode: str = "hot",
    limit: int = 25,
    hours_ago: int = 12,
) -> List[Dict]:
    """
    Main entry point — fetch posts from multiple subreddits.

    Args:
        subreddits: List of subreddit names (without r/)
        mode: 'hot', 'new', or 'top'
        limit: Max posts per subreddit
        hours_ago: Time window for hot/new modes

    Returns:
        List of standardized post dicts
    """
    try:
        scraper = RedditScraper()
        all_posts = []

        for subreddit in subreddits:
            subreddit = subreddit.strip().replace("r/", "")
            if not subreddit:
                continue

            if mode == "hot":
                posts = scraper.get_hot_posts(subreddit, limit=limit, hours_ago=hours_ago)
            elif mode == "new":
                posts = scraper.get_new_posts(subreddit, limit=limit, hours_ago=hours_ago)
            elif mode == "top":
                posts = scraper.get_top_posts(subreddit, limit=limit, time_filter="day")
            else:
                posts = scraper.get_hot_posts(subreddit, limit=limit, hours_ago=hours_ago)

            all_posts.extend(posts)

        print(f"\n📊 Total Reddit posts fetched: {len(all_posts)}")
        return all_posts

    except Exception as e:
        print(f"❌ Error in fetch_reddit_data: {e}")
        return []


if __name__ == "__main__":
    # Test usage
    test_subs = ["technology", "worldnews"]
    print(f"🚀 Fetching posts from {test_subs}")
    results = fetch_reddit_data(test_subs, mode="hot", limit=5)

    for p in results:
        print(f"  [{p['source_handle']}] {p['post_title'][:60]}... (score: {p['score']})")
