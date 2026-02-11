# Match Preview Documentation

## Overview
This module generates comprehensive match previews for upcoming football fixtures, automating:
1.  **Textual Content**: Statistical analysis, head-to-head comparisons, and form guides
2.  **Visual Content**:
    -   **Match Graphics**: AI-generated images with team logos, match details, and dynamic backgrounds
    -   **Statistical Graphs**: Pie charts comparing goal timings for both teams

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Determines search scope (specific leagues or date ranges)

### 2. Fixture Data Collection
**Using RapidAPI Football API:**
- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/fixtures`
  - **Parameters**: `league`, `season`, `date` (optional)
  - **Purpose**: Fetches upcoming fixtures for configured leagues
  - **Returns**: Fixture details (teams, venue, date, time, fixture ID)
- **Endpoint**: `GET https://api-football-v1.p.rapidapi.com/v3/leagues`
  - **Parameters**: `id`
  - **Purpose**: Get league information and current season year
  - **Returns**: League details, current season data
- Filters fixtures based on configured preview timing settings (hours before match)

### 3. Statistical Data Processing
**Database Table**: `match_preview`

**Data sources:**
- Database check for existing fixture data in `match_preview` table
- RapidAPI endpoints for comprehensive match statistics:
  
  **Team & League Data:**
  - **`GET https://api-football-v1.p.rapidapi.com/v3/standings`** - Team rankings and league standings
  - **`GET https://api-football-v1.p.rapidapi.com/v3/leagues`** - League information
  
  **Player Statistics:**
  - **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/players`** - Player statistics for the season
    - Goals, assists, saves, interceptions, duels
    - Yellow/red card records
    - Pass accuracy and key passes
  
  **Team Performance:**
  - **`GET https://api-football-v1.p.rapidapi.com/v3/teams/statistics`** - Team form (last 5 matches)
    - Biggest wins/losses (home and away)
    - Clean sheet records
    - Goal timing statistics (15-minute intervals)
  
  **Match Analysis:**
  - **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead`** - Head-to-head records between teams
  - **`GET https://api-football-v1.p.rapidapi.com/v3/predictions`** - AI-powered match predictions
    - Win probabilities for home/draw/away
    - Expected goals for both teams
  
  **Betting Data:**
  - **`GET https://api-football-v1.p.rapidapi.com/v3/odds`** - Betting odds from bookmakers
    - Top 3 bookmaker odds for comparison

### 4. Content Generation

#### Text Content
- Structures all statistical data into JSON format
- Prepares data for AI content generation

#### Visual Content
- **Match Preview Image**: Generated using Google Gemini AI
- **Statistical Graphs**: Created using Plotly (pie charts for goal timing)

### 5. AI Article Generation
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates BBC-style pyramid writing articles
- Produces 4 content paragraphs covering different aspects

### 6. Cloud Storage
**AWS S3 Integration:**
- Uploads generated images to S3 bucket
- Stores at path: `match/eng_{fixture_id}_preview.png`

### 7. Publication
- Publishes complete article to CMS
- Includes generated text and images

### 8. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to database
- Tracks failures for auto-deactivation (3 consecutive failures)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Image Generation (Google Gemini)

```
Generate a football match preview image with the following details:
{
    "league_name": [League Name],
    "home_team": { "name": [Home Team Name] },
    "away_team": { "name": [Away Team Name] },
    "match_date": [Date],
    "venue": [Venue Name],
    "design": "modern, clean, professional sports news graphic, bold typography, authentic sports media style, use a real action photograph of players from these teams as the full background remains clearly visible and not covered by overlays, do not use abstract, gradient, digital art, or poster-style backgrounds, team logos should be automatically fetched and displayed near team names, league logo small and subtle in one corner if available, logos and text overlays should be small and not block the players without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players.",
    "size": "1024x1024"
}
```

*Note: The placeholders in brackets are dynamically filled with data from the specific match.*

### Content Generation (OpenAI GPT-3.5-turbo)
The following prompts generate the article content:

#### 1. Headline Generation
```
Write a Headline using this example:
[Team A] vs [Team B], [Date]
The format of the headline must be structured for SEO and AI search discovery and must be this:
[Team A] vs [Team B]: Preview - Team News, Line-ups, Prediction and Tips | [Date] [Kickoff time in GMT]
```

#### 2. Article Template (Base Context)
```
The article must be written in the BBC style of writing articles which is the pyramid style of writing. 
Do not use fluff at the start of the paragraph or article or sentence. Go straight to the point like the BBC does in its articles.

Example: {team1} vs {team2}, {date}. please do not generate any dummy text in []

{team1} — on the {rank1}nd place in {league_name}, {team2} — {rank2}th in {league_name}. 
please do not generate any dummy text in []

{top_player_a} scored {top_home_total} goals this season for {team1}, {top_player_b} scored {top_away_total} for {team2}. 
article Must be long, SEO-friendly, with natural language to pass AI content detection. 
Last five {team1} games: {home_forms}. {team2} last five games: {away_forms}. 
please do not generate any dummy text in []
```

#### 3. Team Performance & Results
```
Using data from the respective match, write a BBC pyramid style of writing football match preview article. 
The data must also take into consideration that it is writing the preview in a football league system when that is the case. 
It must take into consideration the league table and any associated information for the competition.

Example: {team1} won at home with a biggest score — {home_biggest_win_in_home}, and away with a score — {home_biggest_win_in_away}. 
Biggest loss of the season at home — {home_biggest_lose_in_home}, away game — {home_biggest_lose_in_away}. 
This season {team1} at home: wins – {home_win_once_in_home}, draws — {home_draws_once_in_home}, losses — {home_lose_once_in_home}. 
{team2} away: wins — {away_win_once_in_away}, draws — {away_draws_once_in_away}, losses — {away_lose_once_in_away}. 
Must be words long, SEO-friendly, with natural language to pass AI content detection.
```

#### 4. Clean Sheets & Defensive Records
```
Using data from the respective match, write a BBC pyramid style of writing football match preview article. 
The data must also take into consideration that it is writing the preview in a football league system when that is the case. 
It must take into consideration the league table and any associated information for the competition.

Example: This season {team1} has played without scoring a goal {clean_home} times. 
{team2} did not conceded in {clean_away} match of the season. 
{team2} has the biggest winning score gap in the home game — {away_biggest_win_in_home}, and away with a score of — {away_biggest_win_in_away}. 
The biggest loss at home — {away_biggest_lose_in_home}, away game — {away_biggest_lose_in_away}. 
Must be words long, SEO-friendly, with natural language to pass AI content detection.
```

#### 5. Recent Form
```
Using data from the respective match, write a BBC pyramid style of writing football match preview article. 
The data must also take into consideration that it is writing the preview in a football league system when that is the case. 
It must take into consideration the league table and any associated information for the competition.

Example: Last five {team1} games: {home_forms}. {team2} last five games: {away_forms}. 
Must be words long, SEO-friendly, with natural language to pass AI content detection. 
please do not generate any dummy text in []
```

**Model Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: `1.0` (headline), `0.7` (content paragraphs)
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
1. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures`** - Retrieve fixture details including teams, venue, date
2. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics`** - Get match statistics
3. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/players`** - Fetch player statistics for the match
4. **`GET https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead`** - Retrieve head-to-head records
5. **`GET https://api-football-v1.p.rapidapi.com/v3/predictions`** - Get AI-powered match predictions
6. **`GET https://api-football-v1.p.rapidapi.com/v3/odds`** - Fetch betting odds from bookmakers
7. **`GET https://api-football-v1.p.rapidapi.com/v3/leagues`** - Get league information and current season

### Data Retrieved
- Team rankings and standings
- Top scorers (goals, assists, saves, interceptions, duels)
- Team form (last 5 matches)
- Biggest wins/losses (home and away)
- Clean sheet records
- Goal timing statistics (15-minute intervals)
- Head-to-head records
- Match predictions (win probabilities, expected goals)
- Betting odds from top bookmakers

## Configuration Scope

These settings control the operational scope of the **Match Previews** module:

### General Settings
- **Enable Match Previews**: Master switch to activate/deactivate preview generation.

### Timing & Trigger
- **Match Preview Time**: Time in hours *before* the match to trigger generation (e.g., `48` hours).
  - *Purpose*: Generates content well in advance of the fixture.

### Localization
- **Enable Match Previews Translation**: Toggles automatic translation for previews.
- **Translated Preview Languages**: Defines which languages and categories are enabled for translated previews.

### Target Scope
- **Leagues**: Select specific football leagues to generate previews for.
- **Categories**: Define specific content categories to associate with the generated previews.
