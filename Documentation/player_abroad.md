# Player Abroad Documentation

## Overview
This module generates news articles about players competing outside their home countries, automating:
1. **Data Collection**: Tracks match events for players playing abroad
2. **Visual Content**: AI-generated images featuring player photos and match highlights
3. **Article Generation**: BBC-style articles about abroad player performances

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if player_abroad module is enabled for any website
- Retrieves configured leagues and target countries

### 2. Match Data Collection
**Database Table**: `player_abroad`

**Using RapidAPI Football API:**
- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/fixtures`
  - **Parameters**: `league`, `season`, `date`, `status=FT` (finished matches)
  - **Purpose**: Get completed fixtures from today
  - **Returns**: Fixture details for finished matches

- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/fixtures/events`
  - **Parameters**: `fixture` (fixture ID)
  - **Purpose**: Get match events (goals, assists, cards)
  - **Returns**: Player-specific events

- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/fixtures/players`
  - **Parameters**: `fixture` (fixture ID)
  - **Purpose**: Get player statistics and ratings
  - **Returns**: Detailed player performance data

### 3. Player Filtering
**Criteria for "abroad" players:**
- Player nationality different from league country
- Player participated in match events (goal, assist, card, etc.)
- Player's home country matches configured website countries
- League matches configured website leagues

### 4. Content Generation

#### Visual Content
- **Player Performance Image** (Gemini AI):
  - Player photo
  - Match details (teams, score)
  - Event highlights (goals, assists, cards)
  - League and team logos

#### Text Content
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates detailed performance article
- Emphasizes "abroad" context (playing outside home country)

### 5. Cloud Storage
**AWS S3 Integration:**
- Uploads generated images to S3 bucket
- Stores at path: `match/{l_version}_{fixture_id}_{player_id}_{event_type}_{event_detail}_player_abroad.png`

### 6. Publication
- Publishes complete article to CMS
- Includes generated text and images
- Updates player_abroad record with posted website IDs

### 7. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to `news_log` table
- Tracks failures for auto-deactivation (3 consecutive failures)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Content Generation (OpenAI GPT-3.5-turbo)

#### 1. Headline Generation
```
Write a bold and attention-grabbing sports news headline for an abroad player. 
The headline must be structured for SEO and AI search discovery: 
'player - {player_name}, team name - {team_name}, event type - {event_type}, event detail - {event_detail}', country - {league_country}. 

The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. 
Avoid clichés and make it engaging.
```

#### 2. Article Content
```
You are a professional sports journalist.

Write a detailed news article between 500 and 700 words about the following football match and the performance of an abroad player (a player competing outside his home country).

Match Data (JSON):
{json.dumps(data)}

Guidelines:
- Generate a natural, human-like article — not formulaic.
- Vary writing style, sentence structure, and vocabulary in every article.
- Each time you generate, the article should feel like it comes from a different journalist.
- Use different tones: sometimes analytical, sometimes emotional, sometimes focused on history, sometimes focused on tactics.
- Emphasize that the player is an abroad player (playing in {league_name} in {league_country} instead of his home country {nationality}.
- Include match details: teams, date, score, and player performance (goals, assists, cards, minutes).
- Add season context: appearances, stats, contributions so far.
- Provide local vs international perspective: how foreign fans, local supporters, or media might see this performance.
- End with a forward-looking statement about the player's career, reputation, or potential.

Requirements:
- Length: 500–700 words.
- Do not repeat the same sentence structures in multiple articles.
- Avoid robotic transitions like "Firstly," "Secondly," or "In conclusion."
- Make sure the output is continuous prose, not bullet points.

Output:
Write only the full news article. No extra explanation.
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
1. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures`** - Get completed matches
   - Parameters: `league`, `season`, `date`, `status=FT`
2. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/events`** - Match events timeline
   - Parameters: `fixture`
3. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/players`** - Player statistics
   - Parameters: `fixture`

### Database Schema
**Table**: `player_abroad`
- `id` - Unique record ID
- `player_id` - Player identifier
- `player_name` - Player full name
- `nationality` - Player nationality
- `fixture_id` - Match fixture ID
- `team` - Player's team
- `event_type` - Event type (Goal, Card, Assist, etc.)
- `event_detail` - Event details (Normal Goal, Yellow Card, etc.)
- `league` - League name
- `league_country` - League country
- `home_team` - Home team name
- `away_team` - Away team name
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Key Features
- **Automatic Detection**: Identifies players playing outside their home country
- **Event-Based**: Triggers on specific match events (goals, assists, cards)
- **Country Matching**: Filters by player nationality and website target countries
- **Real-Time**: Processes matches immediately after completion

## Configuration Scope

These settings control the operational scope of the **Player Abroad** module:

### General Settings
- **Enable Player Abroad**: Master switch to activate/deactivate abroad player tracking and news generation.

### Content Customization
- **Player Abroad Prompt**: Custom instruction or prompt used to guide the AI article generation.

### Localization
- **Enable Player Abroad Translation**: Toggles automatic translation for player abroad news.
- **Translated Player Abroad Languages**: Defines which languages and categories are enabled for translated articles.

### Target Scope
- **Player Abroad Categories**: Define specific content categories to associate with the generated articles.
- **Countries**: Select specific target countries to track players from (e.g., `Zimbabwe`, `Zambia`).
