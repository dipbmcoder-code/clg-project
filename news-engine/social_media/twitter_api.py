"""
X (Twitter) API Integration Module
Handles fetching user data and tweets using X API v2
"""
import os
import json
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get the root directory for storing JSON files
ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "result" / "json" / "twitter_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# X API Bearer Token from environment
BEARER_TOKEN = os.getenv("X_API_BEARER_TOKEN")

class TwitterAPIClient:
    """Client for interacting with X (Twitter) API v2"""
    
    def __init__(self, bearer_token=None):
        """
        Initialize the Twitter API client
        
        Args:
            bearer_token: X API Bearer Token (defaults to env variable)
        """
        self.bearer_token = bearer_token or BEARER_TOKEN
        if not self.bearer_token:
            raise ValueError("X API Bearer Token is required. Set X_API_BEARER_TOKEN in .env file")
        
        self.base_url = "https://api.x.com/2"
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        
        # Cache file paths
        self.users_cache_file = CACHE_DIR / "users_cache.json"
        self.tweets_cache_file = CACHE_DIR / "tweets_last_2h.json"
        
        # Load existing cache
        self.users_cache = self._load_json_cache(self.users_cache_file)
        self.tweets_cache = self._load_json_cache(self.tweets_cache_file)
    
    def _load_json_cache(self, filepath):
        """Load JSON cache from file"""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cache from {filepath}: {e}")
        return {}
    
    def _save_json_cache(self, data, filepath):
        """Save JSON cache to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Cache saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error saving cache to {filepath}: {e}")
            return False
    
    def get_users_by_usernames(self, usernames):
        """
        Fetch user data by Twitter usernames (handles)
        Uses cache to avoid repeated API calls
        
        Args:
            usernames: List of Twitter usernames (without @)
            
        Returns:
            dict: Mapping of username to user data
        """
        if not usernames:
            print("⚠️ No usernames provided")
            return {}
        
        # Check cache first
        uncached_usernames = []
        for username in usernames:
            if username not in self.users_cache:
                uncached_usernames.append(username)
        
        # Fetch uncached users from API
        if uncached_usernames:
            print(f"🔍 Fetching {len(uncached_usernames)} users from X API: {uncached_usernames}")
            
            # API endpoint: GET /2/users/by?usernames={usernames}
            url = f"{self.base_url}/users/by"
            params = {
                "usernames": ",".join(uncached_usernames),
                "user.fields": "id,name,username,created_at,description,public_metrics,profile_image_url,verified"
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if "data" in data:
                    for user in data["data"]:
                        username = user["username"]
                        self.users_cache[username] = {
                            "id": user["id"],
                            "name": user["name"],
                            "username": user["username"],
                            "created_at": user.get("created_at"),
                            "description": user.get("description"),
                            "followers_count": user.get("public_metrics", {}).get("followers_count", 0),
                            "following_count": user.get("public_metrics", {}).get("following_count", 0),
                            "tweet_count": user.get("public_metrics", {}).get("tweet_count", 0),
                            "profile_image_url": user.get("profile_image_url"),
                            "verified": user.get("verified", False),
                            "cached_at": datetime.now().isoformat()
                        }
                        print(f"✅ Cached user: @{username} (ID: {user['id']})")
                    
                    # Save updated cache
                    self._save_json_cache(self.users_cache, self.users_cache_file)
                
                if "errors" in data:
                    for error in data["errors"]:
                        print(f"⚠️ API Error: {error.get('detail', 'Unknown error')}")
                        
            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching users from X API: {e}")
                return {username: self.users_cache.get(username) for username in usernames if username in self.users_cache}
        else:
            print(f"✅ All {len(usernames)} users found in cache")
        
        # Return user data (from cache)
        return {username: self.users_cache.get(username) for username in usernames if username in self.users_cache}
    
    def get_user_tweets_last_2h(self, user_id):
        """
        Fetch tweets for a specific user from the last 2 hours
        
        Args:
            user_id: Twitter user ID
            
        Returns:
            list: List of tweet objects
        """
        # Calculate cache key based on current hour
        current_time = datetime.now(timezone.utc)
        cache_key = f"{user_id}"
        
        print(f"🔍 Fetching tweets for user {user_id} from last 2 hours from X API")
        
        # Calculate start and end time for the last 2 hours
        end_time = current_time
        start_time = current_time - timedelta(hours=7)
        
        # Format times in ISO 8601 format required by X API
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # API endpoint: GET /2/users/{id}/tweets
        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "start_time": start_time_str,
            "end_time": end_time_str,
            "max_results": 100,  # Maximum allowed per request
            "tweet.fields": "id,text,created_at,public_metrics,entities,referenced_tweets",
            "expansions": "attachments.media_keys",
            "media.fields": "url,preview_image_url,type"
        }
        
        tweets = []
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "data" in data:
                media_map = {}
                if "includes" in data and "media" in data["includes"]:
                    for media in data["includes"]["media"]:
                        media_map[media["media_key"]] = media
                
                for tweet in data["data"]:
                    # Extract media URLs (photos and videos)
                    images = []
                    videos = []
                    if "attachments" in tweet and "media_keys" in tweet["attachments"]:
                        print("attachment", tweet["attachments"])
                        for media_key in tweet["attachments"]["media_keys"]:
                            if media_key in media_map:
                                media = media_map[media_key]
                                if media["type"] == "photo":
                                    images.append(media.get("url"))
                                elif media["type"] == "video" or media["type"] == "animated_gif":
                                    video_obj = {
                                        "type": media["type"],
                                        "preview_image_url": media.get("preview_image_url")
                                    }
                                    videos.append(video_obj)
                    
                    # Extract embedded URLs
                    embedded_url = None
                    if "entities" in tweet and "urls" in tweet["entities"]:
                        urls = tweet["entities"]["urls"]
                        if urls:
                            embedded_url = urls[0].get("expanded_url")
                    
                    tweet_obj = {
                        "twitter_id": tweet["id"],
                        "tweet_text": tweet["text"],
                        "timestamp": tweet["created_at"],
                        "replies": tweet.get("public_metrics", {}).get("reply_count", 0),
                        "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0),
                        "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                        "images": images,
                        "videos": videos,
                        "embedded_url": embedded_url,
                        "scraped_at": datetime.now().isoformat()
                    }
                    tweets.append(tweet_obj)
                    print(f"✅ Fetched tweet: {tweet['id']}")
                
                # Cache the tweets
                self.tweets_cache[cache_key] = tweets
                
                print(f"✅ Fetched {len(tweets)} tweets for user {user_id} from last 2 hours")
            else:
                print(f"ℹ️ No tweets found for user {user_id} in last 2 hours")
            
            if "errors" in data:
                for error in data["errors"]:
                    print(f"⚠️ API Error: {error.get('detail', 'Unknown error')}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching tweets from X API: {e}")
        
        return tweets
    
    def get_tweets_for_multiple_users(self, usernames):
        """
        Fetch tweets for multiple users from the last 2 hours
        
        Args:
            usernames: List of Twitter usernames
            
        Returns:
            list: List of all tweets with handler information
        """
        # First, get user data (with caching)
        users_data = self.get_users_by_usernames(usernames)
        
        all_tweets = []
        
        for username, user_data in users_data.items():
            if not user_data:
                print(f"⚠️ No data found for user: {username}")
                continue
            
            user_id = user_data["id"]
            tweets = self.get_user_tweets_last_2h(user_id)
            
            # Add handler information to each tweet
            for tweet in tweets:
                tweet["handler"] = username
                all_tweets.append(tweet)
        
        self._save_json_cache(self.tweets_cache, self.tweets_cache_file)
        return all_tweets


def fetch_twitter_data(usernames):
    """
    Main function to fetch Twitter data for multiple users from the last 2 hours
    
    Args:
        usernames: List of Twitter usernames (without @)
        
    Returns:
        list: List of tweet objects with handler information
    """
    try:
        client = TwitterAPIClient()
        tweets = client.get_tweets_for_multiple_users(usernames)
        print(f"\n📊 Total tweets fetched: {len(tweets)}")
        return tweets
    except Exception as e:
        print(f"❌ Error in fetch_twitter_data: {e}")
        return []


# Example usage
if __name__ == "__main__":
    # Test with a few handles
    test_handles = ["FabrizioRomano", "David_Ornstein"]
    
    print(f"🚀 Fetching tweets for {test_handles} from last 2 hours")
    tweets = fetch_twitter_data(test_handles)
    
    print(f"\n📋 Results:")
    for tweet in tweets:
        print(f"  - @{tweet['handler']}: {tweet['tweet_text'][:50]}...")
