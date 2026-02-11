# Transfer News Documentation

## Overview
This module generates news articles about confirmed player transfers, automating:
1. **Data Collection**: Scrapes latest transfer data from Transfermarkt
2. **Visual Content**: AI-generated images featuring player photos and club logos
3. **Article Generation**: BBC-style transfer news articles

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Checks if transfer module is enabled for any website
- Retrieves configured websites and their target countries

### 2. Transfer Data Collection
**Database Table**: `transfers`

**Using Transfermarkt Web Scraping:**
- **Source URL**: `https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=alle&land_id=&selectedOptionInternalType=nothingSelected&minMarktwert=0&maxMarktwert=500.000.000&minAbloese=0&maxAbloese=500.000.000&yt0=Show`
- Scrapes current date transfer data
- Filters by configured country preferences
- **Data Retrieved**:
  - Player information (ID, name, position, nationality, date of birth)
  - Transfer details (from club, to club, to league, to country)
  - Market value and transfer fee
  - Transfer date and contract details
  - Player statistics and previous clubs
  - Transfer history and market value history

### 3. Data Processing
- Checks if transfer already exists in database by player ID
- Inserts new transfer records into `transfers` table
- Matches player nationalities with website country configurations
- Filters transfers relevant to each website's target audience

### 4. Content Generation

#### Visual Content
- **Transfer Image**: Generated using Google Gemini AI
  - Player photo
  - Club logos (from club and to club)
  - Transfer details overlay
  - Professional sports news graphic design

#### Text Content
**Using OpenAI GPT-3.5-turbo:**
- Generates SEO-optimized headline
- Creates BBC-style confirmed transfer article
- Includes player background and transfer context

### 5. Cloud Storage
**AWS S3 Integration:**
- Uploads generated images to S3 bucket
- Stores at path: `match/{l_version}_{player_id}_{website_id}_{date}_transfer.png`

### 6. Publication
- Publishes complete article to CMS
- Includes generated text and images
- Updates transfer record with posted website IDs

### 7. Cleanup & Logging
- Deletes local image files after successful upload
- Logs all operations to `news_log` table
- Tracks failures for auto-deactivation (3 consecutive failures)

## AI Prompts

> **Note**: The prompts below represent the default logic. Custom prompts configured in the Admin Dashboard (News Prompts section) will take precedence over these defaults.

### Image Generation (Google Gemini)

```
A high-resolution, photorealistic sports news graphic announcing the completed transfer of **{player_name}** from **{from_club_name}** to **{to_club_name}**.

**Visual Requirements:**
* **Player:** The graphic must feature a **real, clear photograph** of **{player_name}** (not an illustration, painting, or digital art effect).
* **Background:** The background must be a **full, realistic, and clearly visible scene** of a professional football setting (e.g., stadium pitch, press conference, training ground, or player signing a contract). **Strictly no abstract, gradient, digital art, cartoon, poster, or illustrated style effects.**
* **Design:** Modern, clean, professional sports media style. Use bold, clear text for the player and club names.
* **Clubs:** Visually incorporate the **official club logos** for both **{from_club_name}** and **{to_club_name}** near their respective names. Clearly indicate the **"Transfer Completed"** status.

**Format/Composition:** A dynamic, authentic layout suitable for major sports news outlets (e.g., Sky Sports, ESPN, BBC Sport).
```

*Note: The placeholders in braces are dynamically filled with actual transfer data.*

### Content Generation (OpenAI GPT-3.5-turbo)

#### 1. Headline Generation
```
The headline must be written in the same format as the BBC writes its catchy headlines. 
The headline must be structured for SEO and AI search discovery: 
'player - {player_name}, player position - {position}, linked with club name - {to_club}, country - {to_country}. 

Examples of the BBC writes its headlines with necessary places for caps are below:

Thomas Partey: Ghanaian midfielder leaves Arsenal to join Atletico Madrid.
Mohammed Kudus: Tottenham star on the verge of joining Barcelona.
Isak in but no Gyokeres in Potter's Sweden squad.
Palace ask for Leeds game to be moved in fixture-pile-up.

How Athletic Club's unique player policy drives success. 

You must follow the BBC style for writing headlines as not all words in the headline are capped. 
The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. 
Avoid clichés and make it engaging.
```

#### 2. Article Content
```
Using information from the data provided, write a BBC-written transfer news. 
The article must be written in the inverted pyramid style of writing articles. 
Go straight to the article and avoid using redundant words to start the article.

Note that these are confirmed transfers so it must be written as such. 
And you can find the dates for the start of the contract and the end of the contract. 
So do not write it like a rumour but a confirmed and completed transfer. 
Do not put dates in the article. Only put dates for the start of the transfer and end of the contract.

Player data: {json.dumps(data)}

Report the article as fact and not reportedly or a speculation. 
Also note that it is transfer news therefore there is a possibility of someone becoming a free agent based on the information you receive from the data. 

Use the rest of the player's data like his market value, date of birth, previous clubs, leagues he has played in nationality or players nationalities (if the players has dual nationality), positions he can play in, previous clubs to enhance the lower parts of article.

Do not invent facts for the article. Do not add quotes. Report only on facts from the data. 
If the data is not sufficient to write up to the word limit, ignore the word limit.

Write a detailed football news article (300–500 words) about {player_name}, a {nationality} {position}, 
who is currently transfer to be linked with a move from {from_club} to {to_club}. 

Follow these rules:
- Make the article sound natural and human, not formulaic.
- Vary writing style, vocabulary, and sentence structure, as if written by different journalists each time.
- Use different tones (analytical, emotional, historical, tactical) across different articles.
- Emphasize that {player_name} could be playing abroad, potentially competing in the {to_league} in {to_country} instead of his home country {nationality}.
- Mention the reported transfer date ({transfer_date}), estimated transfer fee ({fee}), and the player's market value ({market_value}) in the context of speculation.
- Include specific recent match details: opponent, date, scoreline, and {player_name}'s performance
- Add season context: appearances, stats, and contributions so far.
- Provide both local and international perspectives: how home-country fans, local supporters, and media are reacting to the rumors and potential move.
- End with a forward-looking statement about how this possible transfer could shape his career, reputation, or potential if it happens.

The article must be written in continuous prose, no bullet points, and should feel like authentic sports journalism.
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
- **Data Type**: Confirmed transfers
- **Update Frequency**: Daily (cron job)
- **Filtering**: By player nationality and configured countries

### Database Schema
**Table**: `transfers`
- `id` - Unique transfer record ID
- `player_id` - Player identifier
- `player_name` - Player full name
- `position` - Playing position
- `nationality` - Player nationality/nationalities
- `from_club` - Departing club
- `to_club` - Destination club
- `to_league` - Destination league
- `to_country` - Destination country
- `market_value` - Player market value
- `fee` - Transfer fee
- `transfer_date` - Date of transfer
- `is_posted` - Publication status
- `website_ids` - Array of website IDs where posted
- `created_at` - Record creation timestamp

## Configuration Scope

These settings control the operational scope of the **Transfer News** module:

### General Settings
- **Enable Transfer & Rumors**: Master switch to activate/deactivate both transfer and rumour news generation.

### Localization
- **Enable Transfer & Rumors Translation**: Toggles automatic translation for consolidated transfer and rumour news.
- **Translated Transfer & Rumors Languages**: Defines which languages and categories are enabled for translated content.

### Target Scope
- **Transfer Categories**: Define specific content categories to associate with confirmed transfer articles.
- **Countries**: Select specific target countries to filter transfers by player nationality or league.
