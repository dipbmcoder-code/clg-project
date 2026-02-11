# News Rewriting Documentation

## Overview
This module automates the aggregation and rewriting of football news from various external sources. It:
1. **Scrapes** articles from configured new websites
2. **Rewrites** content using AI to maintain facts but change style
3. **Generates** unique visual content
4. **Publishes** to the CMS as fresh content

## Workflow

### 1. Initialization
- Validates API quota availability for Gemini API
- Retrieves websites configured with `Rewriting` module enabled
- Extracts target URLs to scrape from these configurations

### 2. Article Scraping
**Component**: `scrape_articles_api.py`

- **Multi-threaded Scraping**: Uses concurrent workers to process multiple sites
- **Link Extraction**: Identifies article links while ignoring non-article pages (categories, authors, tags)
- **Content Fetching**:
  - Validates publication date (ensures articles are from today)
  - Extracts title and main content using multiple CSS selectors
  - Saves raw article data to local JSON logs

### 3. Data Processing
**Database Table**: `rewritten_articles`

- Checks if article URL already exists in database
- Inserts new scraped articles with:
  - Original title and content
  - Source website name
  - Original URL
- Filters articles based on daily relevance

### 4. Content Generation

#### Visual Content
**Component**: `image_rewriting_api.py`
- **Engine**: Google Gemini
- **Style**: Professional news broadcast/editorial aesthetic
- **Requirements**:
  - No specific identifiable faces (privacy/copyright safety)
  - Abstract or symbolic representation of the topic
  - High-quality, realistic, modern design
  - 16:9 Landscape orientation

#### Text Rewriting
**Component**: `main_rewriting.py`
- **Engine**: OpenAI (via `generate_openai_content`)
- **Style**: BBC Sport Journalism
- **Process**:
  - Takes original title and content
  - Rewrites in inverted pyramid structure
  - Generates SEO-optimized headline
  - Ensures content is unique yet factually accurate
  - Output format: JSON with `title` and `content`

### 5. Cloud Storage
**AWS S3 Integration:**
- Uploads generated featured images
- Stores at path: `match/{article_id}_{website_id}_{timestamp}_rewriting.png`

### 6. Publication
- Publishes rewritten article to CMS
- linking generated image and rewritten text
- Updates `rewritten_articles` table with `website_ids` where posted
- Logs success/failure for monitoring

### 7. Cleanup & Logging
- Removes local temporary images
- Logs detailed status to `news_log` table (JSON format)
- Tracks module failures (auto-deactivates after 3 consecutive failures)

## AI Prompts

### Image Generation (Google Gemini)

```
Create a professional, modern news article featured image for:

Title: {title}
Context: {first_paragraph}

VISUAL ELEMENTS:
- Modern news/journalism aesthetic
- Clean, professional design
- Relevant imagery based on article topic
- High-quality, realistic style
- News broadcast or editorial style

DESIGN REQUIREMENTS:
- 16:9 landscape orientation
- High resolution, publication-ready
- Professional color scheme
- Typography: Bold, readable headline overlay (optional)
- Style: BBC News, Reuters, or AP News aesthetic

CONTENT FOCUS:
- Abstract or symbolic representation of the article topic
- NO identifiable people or faces
- Professional stock photo quality
- Suitable for news publication

Create a compelling, professional featured image that would attract readers to this news article.
```

### Content Rewriting (OpenAI)

```
You are a professional news editor and journalist. Rewrite the following news article in a fresh, engaging style while maintaining all facts and key information.

Original Title: {article_data['original_title']}

Original Content:
{article_data['original_content']}

Requirements:
1. Write in BBC Sport journalism style (inverted pyramid structure)
2. Create a compelling, SEO-optimized headline
3. Rewrite the content to be natural and human-like (must pass AI detection)
4. Maintain all facts, quotes, and key information
5. Improve readability and engagement
6. Keep the same tone and professionalism

Return ONLY valid JSON with this structure:
{
  "title": "Rewritten headline",
  "content": "Full rewritten article content with proper paragraphs"
}
```

## Data Sources

### Web Scraping
- **Targets**: Dynamically configured via CMS (Websites marked for 'Rewriting')
- **Method**: Custom `ArticleScraper` class with `BeautifulSoup`
- **Filtering**:
  - Domain matching
  - Date verification (Today's news only)
  - Content length validation

### Database Schema
**Table**: `rewritten_articles`
- `id`: Unique identifier
- `original_url`: Source URL (Unique constraint)
- `source_website`: Name of source domain
- `original_title`: Raw title from scraper
- `original_content`: Raw content from scraper
- `is_posted`: Boolean status
- `website_ids`: JSON array of websites where published
- `created_at`: Timestamp

## Configuration Scope

These settings control the operational scope of the **News Rewriting** module:

### General Settings
- **Enable News Scrap and Rewrite**: Master switch to activate/deactivate the scraping and rewriting of external news.

### Source & Target
- **News Rewriting Sources**: Configure specific external websites to scrape from.
  - **URL**: The source website URL (e.g., `https://www.ghanaweb.com`).
  - **Categories**: Define specific content categories to associate with the rewritten articles.
