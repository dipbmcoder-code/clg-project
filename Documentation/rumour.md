# Transfer Rumours Documentation

## Overview
This module generates news articles about player transfer rumours and speculation, automating:
1. **Data Collection**: Scrapes latest transfer rumour data from Transfermarkt
2. **Visual Content**: AI-generated images featuring player photos and potential club logos
3. **Article Generation**: BBC-style transfer rumour articles

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if rumour module is enabled for any website
- Retrieves configured websites and their target countries

### 2. Rumour Data Collection
**Database Table**: `rumours`

**Using Transfermarkt Web Scraping:**
- **Source URL**: `https://www.transfermarkt.com/geruechte/aktuellegeruechte/statistik?plus=1`
- Scrapes current date transfer rumour data
- Filters by configured country preferences
- **Data Retrieved**:
  - Player information (ID, name, position, nationality, date of birth)
  - Rumour details (from club, to club, to league, to country)
  - Market value and probability percentage
  - Rumour metadata (source, date, reliability)
  - Player statistics and career history

### 3. Data Processing
- Checks if rumour already exists in database by player ID and rumour details
- Inserts new rumour records into `rumours` table
- Matches player nationalities with website country configurations
- Filters rumours relevant to each website's target audience

### 4. Content Generation

#### Visual Content
- **Rumour Image**: Generated using Google Gemini AI
  - Player photo
  - Club logos (current club and linked club)
  - Rumour details and probability overlay
  - Professional sports news graphic design with "rumour" branding

#### Text Content
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates BBC-style transfer rumour article
- Emphasizes speculative nature while maintaining journalistic standards

### 5. Cloud Storage
**AWS S3 Integration:**
- Uploads generated images to S3 bucket
- Stores at path: `match/{l_version}_{player_id}_{website_id}_{rumour_id}_rumour.png`

### 6. Publication
- Publishes complete article to CMS
- Includes generated text and images
- Updates rumour record with posted website IDs

### 7. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to `news_log` table
- Tracks failures for auto-deactivation (3 consecutive failures)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Image Generation (Google Gemini)

```
A high-resolution, photorealistic, modern sports news graphic announcing a **FOOTBALL TRANSFER RUMOUR** involving **{player_name}** potentially moving from **{from_club_name}** to **{to_club_name}**.

**Visual Requirements:**
* **Player:** The graphic must feature a **real, clear photograph** of **{player_name}** (not an illustration, painting, or digital art effect).
* **Background:** The background must be a **full, realistic, and clearly visible scene** of a professional football setting (e.g., stadium pitch, press conference, training ground, or general football backdrop). **Strictly no abstract, gradient, digital art, cartoon, poster, or illustrated style effects.**
* **Design:** Modern, clean, professional sports media style. Use bold, clear text for the player and club names. The graphic should clearly convey that this is a **rumour or speculation**, possibly using a question mark, "Link," or "Reported" text, but still maintaining a professional aesthetic.
* **Clubs:** Visually incorporate the **official club logos** for both **{from_club_name}** and **{to_club_name}** near their respective names.

**Format/Composition:** A dynamic, authentic layout suitable for major sports news outlets (e.g., Sky Sports, ESPN, BBC Sport) but adapted to signal speculation.
```

*Note: The placeholders in braces are dynamically filled with actual rumour data.*

### Content Generation (OpenAI GPT-3.5-turbo)

#### 1. Headline Generation
```
Write a bold and attention-grabbing headline for the article in the BBC style of writing headlines. 
The headline must be structured for SEO and AI search discovery: 
'player - {player_name}, player position - {position}, linked with club name - {to_club}, country - {to_country}'. 

You must follow the BBC style for writing headlines as not all words in the headline are capped. 

Examples of the BBC writes its headlines with necessary places for caps are below:

Thomas Partey: Ghanaian midfielder leaves Arsenal to join Atletico Madrid.
Mohammed Kudus: Tottenham star on the verge of joining Barcelona.
Isak in but no Gyokeres in Potter's Sweden squad.
Palace ask for Leeds game to be moved in fixture pile-up.

How Athletic Club's unique player policy drives success
```

#### 2. Article Content
```
Using information from the data provided, write a BBC-written transfer rumour news article. 
The article must be written in the inverted pyramid style of writing articles. 
Go straight to the article. Avoid using redundant words at the start of the opening sentence that makes it took robotic. 

Note that these are transfers rumours so it must be written as such. 
Since this is not a confirmed transfer yet, do not state dates for the start of the contract and the end of the contract. 
So do not write it like a confirmed or completed transfer but a transfer rumour. 
You must write the article in UK English and not American English.

player data: {json.dumps(data)}

Report the article as a rumour. Also note that it is transfer news therefore it must there is a possibility of someone becoming a free agent based on the information you receive from the data. 

Use the rest of the player's data like his market value, date of birth, previous clubs, leagues he has played in nationality or players nationalities (if the players has dual nationality), positions he can play in, previous clubs to enhance the lower parts of article. 

Bold the first sentence of the article.

Do not invent facts for the article. Do not add quotes. Report only on facts from the data.

Write the detailed football news article (maximum 300 words) about {player_name}, a {nationality} {position}, 
who is currently transfer to be linked with a move from {from_club} to {to_club}.

Follow these rules:
- Make the article sound natural and human, not formulaic.
- Vary writing style, vocabulary, and sentence structure, as if written by different journalists each time.
- Use different tones (analytical, emotional, historical, tactical) across different articles.
- Mention the player's market value ({market_value}) in the context of speculation.
- Include specific recent match details: opponent, date, scoreline, and {player_name}'s performance
- If available, include the reported probability of the move happening (e.g., {probability}).
- End with a forward-looking statement about how this possible transfer could shape his career, reputation, or potential if it happens.

The article must be written in continuous prose, not bullet points, and should feel like authentic sports journalism.
```

**Model Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: `1.0` (headline), `0.7` (content)
- Max Tokens: `500`
- Top P: `1`
- Frequency Penalty: `0`
- Presence Penalty: `0`

## Data Sources

### Transfermarkt Web Scraping
- **Source**: Transfermarkt.com
- **Data Type**: Transfer rumours and speculation
- **Update Frequency**: Daily (cron job)
- **Filtering**: By player nationality and configured countries
- **Reliability**: Includes probability/reliability indicators

### Database Schema
**Table**: `rumours`
- `id` - Unique rumour record ID
- `player_id` - Player identifier
- `player_name` - Player full name
- `position` - Playing position
- `nationality` - Player nationality/nationalities
- `from_club` - Current club
- `to_club` - Linked club
- `to_league` - Potential destination league
- `to_country` - Potential destination country
- `market_value` - Player market value
- `probability` - Rumour probability percentage
- `rumour_details` - Rumour-specific information
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Key Differences from Transfer Module
- **Content Tone**: Speculative vs. factual
- **Data Source**: Rumours vs. confirmed transfers
- **Article Style**: Emphasizes "linked with", "reportedly", "speculation"
- **Probability**: Includes likelihood percentage when available
- **Visual Branding**: Marked as "rumour" to distinguish from confirmed news

## Configuration Scope

These settings control the operational scope of the **Transfer Rumours** module:

### General Settings
- **Enable Transfer & Rumors**: Master switch to activate/deactivate both transfer and rumour news generation.

### Localization
- **Enable Transfer & Rumors Translation**: Toggles automatic translation for consolidated transfer and rumour news.
- **Translated Transfer & Rumors Languages**: Defines which languages and categories are enabled for translated content.

### Target Scope
- **Rumors Categories**: Define specific content categories to associate with rumour articles.
- **Countries**: Select specific target countries to filter rumours by player nationality or league.
