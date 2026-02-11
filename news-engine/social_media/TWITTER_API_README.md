# X (Twitter) API Integration

This module provides integration with X (Twitter) API v2 to fetch user data and tweets.

## Features

- ✅ Fetch user data by Twitter handles using `/2/users/by?usernames={usernames}`
- ✅ Fetch tweets from the last 24 hours using `/2/users/{id}/tweets`
- ✅ Automatic caching to minimize API calls
- ✅ JSON storage for user data and hourly tweet cache
- ✅ Error handling and retry logic

## Setup

### 1. Get X API Bearer Token

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app (or use existing)
3. Generate a Bearer Token
4. Copy the Bearer Token

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
X_API_BEARER_TOKEN=your_bearer_token_here
```

## Usage

### Basic Usage

```python
from social_media.twitter_api import fetch_twitter_data

# Fetch tweets from the last 24 hours
handles = ["FabrizioRomano", "David_Ornstein"]
tweets = fetch_twitter_data(handles)
```

### Advanced Usage

```python
from social_media.twitter_api import TwitterAPIClient

# Initialize client
client = TwitterAPIClient()

# Get user data (cached automatically)
users = client.get_users_by_usernames(["FabrizioRomano", "David_Ornstein"])

# Get tweets for a specific user ID from last 24 hours
user_id = users["FabrizioRomano"]["id"]
tweets = client.get_user_tweets_last_24h(user_id)

# Get tweets for multiple users from last 24 hours
all_tweets = client.get_tweets_for_multiple_users(
    ["FabrizioRomano", "David_Ornstein"]
)
```

## API Endpoints Used

### 1. Get Users by Usernames
- **Endpoint**: `GET https://api.x.com/2/users/by?usernames={usernames}`
- **Purpose**: Fetch user profile data including user ID
- **Caching**: User data is cached in `result/json/twitter_cache/users_cache.json`

### 2. Get User Tweets
- **Endpoint**: `GET https://api.x.com/2/users/{id}/tweets`
- **Purpose**: Fetch tweets for a specific user from the last 24 hours
- **Caching**: Tweets are cached hourly in `result/json/twitter_cache/tweets_last_24h_YYYY-MM-DD_HH.json`

## Data Structure

### User Data
```json
{
  "username": {
    "id": "123456789",
    "name": "Display Name",
    "username": "username",
    "created_at": "2010-01-01T00:00:00.000Z",
    "description": "Bio text",
    "followers_count": 1000000,
    "following_count": 500,
    "tweet_count": 50000,
    "profile_image_url": "https://...",
    "verified": true,
    "cached_at": "2025-12-03T16:19:55"
  }
}
```

### Tweet Data
```json
{
  "twitter_id": "1234567890",
  "handler": "username",
  "tweet_text": "Tweet content...",
  "timestamp": "2025-12-03T10:30:00.000Z",
  "replies": 10,
  "retweets": 50,
  "likes": 200,
  "images": ["https://..."],
  "embedded_url": "https://...",
  "scraped_at": "2025-12-03T16:19:55"
}
```

## Cache Management

### Cache Locations
- **User Cache**: `result/json/twitter_cache/users_cache.json`
- **Tweet Cache**: `result/json/twitter_cache/tweets_last_24h_YYYY-MM-DD_HH.json`

### Cache Behavior
- User data is cached permanently (until manually cleared)
- Tweet data is cached per hour (refreshes every hour)
- API calls are only made for uncached data

### Clear Cache
To clear the cache, simply delete the cache files:
```bash
rm -rf result/json/twitter_cache/
```

## Integration with Existing System

To integrate with the existing `main_social_media.py`:

```python
# Replace the existing scraper import
# from publication.social_scraper import scrap_social_media_data

# Use the new API-based approach
from twitter_api import fetch_twitter_data

# In your main script
unique_handles = get_unique_field(websites, "twitter_handles")
scraped_posts = fetch_twitter_data(unique_handles)  # Uses X API instead of scraping
```

## Error Handling

The module includes comprehensive error handling:
- Network errors are caught and logged
- Missing API tokens raise clear error messages
- API errors are logged with details
- Cache failures don't stop execution

## Rate Limits

X API v2 rate limits (Free tier):
- User lookup: 300 requests per 15 minutes
- User tweets: 1,500 requests per 15 minutes

The caching system helps minimize API calls and stay within rate limits.

## Testing

Run the module directly to test:
```bash
cd social_media
python twitter_api.py
```

This will fetch tweets for test handles and display the results.
