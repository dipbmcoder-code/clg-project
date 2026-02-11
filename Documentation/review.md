# Match Review Documentation

## Overview
This module generates post-match review articles for completed football fixtures, automating:
1. **Data Collection**: Fetches match results and statistics from RapidAPI
2. **Visual Content**: Multiple AI-generated images (match summary, statistics graphs, lineups)
3. **Article Generation**: BBC-style match review articles with detailed analysis

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if review module is enabled for any website
- Retrieves fixtures scheduled for today or specified dates

### 2. Match Data Collection
**Database Table**: `match_review`

**Using RapidAPI Football API:**
- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/fixtures`
  - **Parameters**: `id` (fixture ID)
  - **Purpose**: Check match status
  - **Returns**: Match status ("Match Finished", "In Progress", etc.)

- Waits for match completion (current time >= match time + configured minutes)
- Only processes matches with status "Match Finished"

### 3. Statistical Data Processing
**RapidAPI endpoints for match review:**

**Match Statistics:**
- **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics`** - Team statistics
  - Possession, shots, passes, fouls
  - Corners, offsides, yellow/red cards
  
**Player Performance:**
- **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/players`** - Player ratings and statistics
  - Goals, assists, shots on target
  - Pass accuracy, duels won
  - Defensive actions (tackles, interceptions, blocks)

**Match Events:**
- **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/events`** - Goals, cards, substitutions timeline

**Lineups:**
- **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups`** - Starting XI and formations

**Head-to-Head:**
- **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead`** - Historical matchups

### 4. Content Generation

#### Visual Content
Multiple images generated:

1. **Match Summary Image** (Gemini AI):
   - Final score
   - Team logos
   - Key match statistics
   - Professional sports news graphic

2. **Statistics Graphs** (Plotly):
   - Possession comparison
   - Shots comparison
   - Pass accuracy charts

3. **Lineup Visualization**:
   - Formation diagrams
   - Player positions
   - Substitutions

#### Text Content
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates BBC-style match review article
- Includes match events, player performances, and tactical analysis

### 5. Cloud Storage
**AWS S3 Integration:**
- Uploads all generated images to S3 bucket
- Stores at paths:
  - `match/eng_{fixture_id}_review.png` (main image)
  - `match/graph_{fixture_id}_review.png` (statistics)
  - `match/lineups_{fixture_id}_review.png` (formations)

### 6. Publication
- Publishes complete article to CMS
- Includes all generated images and text
- Updates match_review record with posted website IDs

### 7. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to `news_log` table
- Tracks failures for auto-deactivation (3 consecutive failures)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Content Generation (OpenAI GPT-3.5-turbo)

#### Article Content
*Prompts are dynamically generated based on match data, including:*
- Match result and scoreline
- Goal scorers and assist providers
- Key player performances
- Tactical analysis
- Match statistics comparison
- Post-match implications (league standings, etc.)

**Model Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: `1.0` (headline), `0.7` (content)
- Max Tokens: `500`
- Top P: `1`
- Frequency Penalty: `0`
- Presence Penalty: `0`

## RapidAPI Integration

### API Details
- **Service**: API-Football (RapidAPI)
- **Base URL**: `https://api-football-v1.p.rapidapi.com/v3`
- **Authentication**: API Key via `X-RapidAPI-Key` header

### Endpoints Used
1. **`GET /fixtures`** - Match details and status
2. **`GET /fixtures/statistics`** - Team statistics
3. **`GET /fixtures/players`** - Player ratings and stats
4. **`GET /fixtures/events`** - Match events timeline
5. **`GET /fixtures/lineups`** - Team formations and lineups
6. **`GET /fixtures/headtohead`** - Historical records

### Database Schema
**Table**: `match_review`
- `id` - Unique review record ID
- `fixture_match` - Fixture identifier
- `date_match` - Match date and time
- `league_id` - League identifier
- `home_team` - Home team name
- `away_team` - Away team name
- `home_score` - Home team goals
- `away_score` - Away team goals
- `match_status` - Match status
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Configuration Scope

These settings control the operational scope of the **Match Reviews** module:

### General Settings
- **Enable Match Reviews**: Master switch to activate/deactivate review generation.

### Timing & Trigger
- **Match Review Time**: Time in minutes after kickoff to trigger generation (e.g., `90` minutes).
  - *Purpose*: Ensures the match is finished and data is available before generation.

### Localization
- **Enable Match Reviews Translation**: Toggles automatic translation for reviews.
- **Translated Review Languages**: Defines which languages and categories are enabled for translated reviews.

### Target Scope
- **Leagues**: Select specific football leagues to generate reviews for.
- **Categories**: Define specific content categories to associate with the published reviews.
