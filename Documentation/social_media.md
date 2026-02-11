# Social Media News Documentation

## Overview
This module generates news articles from football-related social media posts (Twitter/X), automating:
1. **Data Collection**: Scrapes tweets from configured Twitter handles
2. **Article Generation**: Converts tweets into professional news articles
3. **Publication**: No image generation - uses embedded tweet

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if social_media module is enabled for any website
- Retrieves configured Twitter handles from websites

### 2. Social Media Data Collection
**Database Table**: `social_media`

**Using Twitter/X API Scraping:**
- Scrapes tweets from configured handles
- **Data Retrieved**:
  - Tweet text content
  - Handler/username
  - Tweet ID
  - Posted time
  - Engagement metrics (likes, retweets, replies)
  - Tweet URL

### 3. Data Processing
- Checks if tweet already exists in database by Twitter ID
- Inserts new tweet records into `social_media` table
- Filters tweets relevant to each website's configured handles

### 4. Content Generation

#### Text Content Only
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates professional news article from tweet content
- Embeds original tweet at end of article

**No Image Generation:**
- Uses embedded tweet as visual content
- Twitter embed code automatically included

### 5. Publication
- Publishes complete article to CMS
- Includes generated text and embedded tweet
- Updates social_media record with posted website IDs

### 6. Logging
- Logs all operations to `news_log` table
- No image cleanup (no images generated)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Content Generation (OpenAI GPT-3.5-turbo)

#### 1. Headline Generation
```
Write a bold and attention-grabbing headline for a football-related social media post.
The headline must be structured for SEO and AI search discovery: 
'Tweet by {handler} - {tweet_text[:80]}'.

The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication.
```

#### 2. Article Content
```
You are a professional football journalist.

Based on the following social media post from {handler}, generate a sports news article.

TWEET CONTENT:
"{tweet_text}"

ADDITIONAL INFO:
- Posted by: {handler}
- Posted at: {tweeted_time}
- Engagement: {likes} likes, {retweets} retweets, {replies} replies
- Tweet URL: {url}

Requirements:
- Headline: 8-12 words, engaging and clear.
- First paragraph: summarize the main news from the tweet.
- Always mention that the information comes from {handler}, who shared it on Twitter (or X).
- Expand with details: who, what, when, where, why (if available).
- Add relevant football context (performances, rivalries, tournament standings, history, implications).
- Tone: objective, factual, journalistic.
- Length: 300-400 words.
- Conclude with a neutral statement (next steps, upcoming matches, confirmation).

Write only the full news article. No extra explanation.
```

**Tweet Embed Code:**
```html
<blockquote class="twitter-tweet">
  <p lang="en" dir="ltr">{tweet_text}</p>
  &mdash; {handler} (@{handler}) 
  <a href="{url}">{tweeted_time[:10]}</a>
</blockquote> 
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
```

**Model Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: `1.0` (headline), `0.7` (content)
- Max Tokens: `500`
- Top P: `1`
- Frequency Penalty: `0`
- Presence Penalty: `0`

## Data Sources

### Twitter/X Scraping
- **Source**: Twitter/X API or web scraping
- **Data Type**: Football-related tweets
- **Filtering**: By configured Twitter handles
- **Update Frequency**: Real-time or periodic (cron job)

### Database Schema
**Table**: `social_media`
- `id` - Unique record ID
- `twitter_id` - Tweet ID
- `handler` - Twitter handle/username
- `tweet_text` - Tweet content
- `tweeted_time` - Tweet timestamp
- `likes` - Like count
- `retweets` - Retweet count
- `replies` - Reply count
- `url` - Tweet URL
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Key Features
- **No Image Generation**: Uses embedded tweets as visual content
- **Real-Time News**: Converts breaking news tweets into articles
- **Source Attribution**: Always credits original Twitter source
- **Engagement Metrics**: Includes social proof (likes, retweets)
- **Handle-Based Filtering**: Only processes tweets from configured accounts

## Configuration Scope

These settings control the operational scope of the **Social Media** module:

### General Settings
- **Enable Social Media**: Master switch to activate/deactivate social media news generation.

### Source Control
- **X (Twitter) Handles**: List of Twitter/X handles to scrape tweets from (e.g., `premierleague`, `FabrizioRomano`).

### Localization
- **Enable Social Media Translation**: Toggles automatic translation for social media news.
- **Translated Social Media Languages**: Defines which languages and categories are enabled for translated articles.

### Target Scope
- **Social Media Categories**: Define specific content categories to associate with the generated articles.
