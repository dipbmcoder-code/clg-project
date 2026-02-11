# Where to Watch Documentation

## Overview
This module generates articles about where fans can watch football leagues globally, automating:
1. **Data Collection**: Fetches TV broadcast information from RapidAPI
2. **Visual Content**: AI-generated images with league logos and broadcast details
3. **Article Generation**: Comprehensive viewing guides for different countries

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if where_to_watch module is enabled for any website
- Calculates target publish dates based on configured days offset

### 2. League Data Collection
**Database Table**: `where_to_watch`

**Using RapidAPI Football API:**
- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/leagues`
  - **Parameters**: `id`, `season`
  - **Purpose**: Get league information and current season
  - **Returns**: League details, season dates, country

- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/leagues/seasons`
  - **Purpose**: Get available seasons for league
  - **Returns**: Season years and dates

### 3. Broadcast Data Collection
**Using Flashscore Web Scraping:**
- **Source URL**: `https://www.flashscore.com/football`
- Scrapes TV broadcast information by country
- **Data Retrieved**:
  - TV channels by country code (ISO 3166-1 alpha-3)
  - Broadcaster names
  - Coverage details (live, highlights, etc.)
  - Streaming platforms

### 4. Data Processing
- Filters broadcast data by configured website countries
- Matches league start dates with target publish dates
- Groups channels by country for each website
- Only includes countries relevant to each website's audience

### 5. Content Generation

#### Visual Content
- **Where to Watch Image** (Gemini AI):
  - League logo
  - Season information
  - Featured broadcasters
  - Professional guide design

#### Text Content
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates comprehensive viewing guide
- Lists broadcasters by country

### 6. Cloud Storage
**AWS S3 Integration:**
- Uploads generated images to S3 bucket
- Stores at path: `match/{l_version}_{league_id}_{season_year}_{website_id}_where_to_watch.png`

### 7. Publication
- Publishes complete article to CMS
- Includes generated text and images
- Updates where_to_watch record with posted website IDs

### 8. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to `news_log` table

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Content Generation (OpenAI GPT-3.5-turbo)

#### 1. Headline Generation
```
Write a bold and attention-grabbing sports news headline for a where to watch league. 
The headline must be structured for SEO and AI search discovery: 
'league name - {league_name}, league country - {country_name}, start date - {start_date}'. 

The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. 
Avoid cliches and make it engaging.
```

#### 2. Article Content
```
You are a professional sports journalist.

Write a detailed, natural-sounding news article (500–700 words) about where fans around the world can watch a football league.

Use the following JSON data as your factual source:
{json.dumps(data, indent=2)}

Guidelines:
- Write the article as if published by a reputable sports outlet — rich in storytelling, tone, and journalistic flow.
- Include the following naturally within the text: 
  - League name
  - Country of origin
  - Start date and end date
  - Broadcast details for each country, smoothly integrated into the narrative.
- Avoid bullet points — use continuous, engaging prose.
- Vary tone and style: sometimes analytical, sometimes emotional, sometimes focused on broadcast innovation or fan culture.
- Avoid repetitive sentence structures and robotic phrasing (no 'Firstly,' or 'In conclusion').
- Make the reader feel the excitement of the new season and the ease of global accessibility through TV and streaming.
```

**Model Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: `1.0` (headline), `0.7` (content)
- Max Tokens: `500`
- Top P: `1`
- Frequency Penalty: `0`
- Presence Penalty: `0`

## RapidAPI Integration

### Endpoints Used
1. **`GET /leagues`** - League information
   - Parameters: `id`, `season`
2. **`GET /leagues/seasons`** - Available seasons

### Database Schema
**Table**: `where_to_watch`
- `id` - Unique record ID
- `league_id` - League identifier
- `league_name` - League name
- `season_year` - Season year
- `country` - League country
- `start_date` - Season start date
- `end_date` - Season end date
- `tv_channels` - JSON object with broadcast data by country code
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Configuration Scope

These settings control the operational scope of the **Where to Watch** module:

### General Settings
- **Enable Where to Watch**: Master switch to activate/deactivate viewing guide generation.

### Timing & Trigger
- **News Publish Time**: Number of days *before* the league start date to generate the guide (e.g., `0` for same day, `2` for 2 days prior).
  - *Purpose*: Publish viewing guides in advance of the season start.

### Localization
- **Enable Where to Watch Translation**: Toggles automatic translation for viewing guides.
- **Translated Where to Watch Languages**: Defines which languages and categories are enabled for translated guides.

### Target Scope
- **Where to Watch Categories**: Define specific content categories to associate with the viewing guides.
- **Countries**: Select specific target countries to curate broadcast information for (e.g., showing only channels relevant to Zimbabwe).
