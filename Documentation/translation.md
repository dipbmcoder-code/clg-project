# Translation Module Documentation

## Overview
The Translation Module (`news-engine/translation/`) automates the process of fetching news articles from configured source websites, translating them into multiple target languages using AI (Gemini/OpenAI), and publishing them to destination websites.

## Workflow

1.  **Initialization**:
    *   The cron job starts via `main_translation.py`.
    *   It checks API quotas (OpenAI/Gemini) to ensure sufficient resources.
    *   It retrieves websites configured for 'Translation' from the CMS.

2.  **Article Scraping**:
    *   The module fetches source URLs from the `website_news_rewriting_and_translation` configuration field of enabled websites.
    *   It scrapes articles from these sources using the `scrape_articles` API.

3.  **Article Processing**:
    *   For each scraped article:
        *   It stores the original article in the `translated_articles` database table.
        *   It identifies all target languages configured for this article's source across all websites.

4.  **Translation & Content Generation**:
    *   For each target language:
        *   **Translation**: The article title and content are translated using AI prompts designed to maintain journalistic tone and accuracy.
        *   **Image Generation**: A relevant image is generated based on the translated content using the configured image provider (Gemini/Imagen/OpenRouter).
        *   **AWS Upload**: The generated image is uploaded to AWS S3.

5.  **Publication**:
    *   The module iterates through all enabled destination websites.
    *   It checks if the destination website is configured to receive this article (matching source URL and language).
    *   It verifies if the article has already been posted to this website in this specific language.
    *   If eligible, it publishes the translated article using `main_publication2`.

6.  **Tracking & Logging**:
    *   The module tracks the `website_ids` and specific languages posted for each article to prevent duplicates.
    *   Detailed logs are created for every step (translation, image generation, publication) and saved to the CMS logs.
    *   Module failures are tracked, and the module is automatically disabled after consecutive failures.

## Configuration
The module relies on the `website_news_rewriting_and_translation` field in the website object, which must contain:
*   `news_type`: Must be set to 'Translation'.
*   `website_url`: The source URL to scrape/match.
*   `languages`: A list of target languages (e.g., `['en', 'es', 'fr']`) for this source.

## Database
*   **Table**: `translated_articles`
*   **Key Fields**:
    *   `website_ids`: Stores a JSON array of objects tracking posted websites and languages, e.g., `[{"id": 1, "lang": ["en", "es"]}]`.
    *   `original_title`, `original_content`: Source content.
    *   `translated_title`, `translated_content`: Temporarily holds translated content during processing.

## Key Files
*   `translation/main_translation.py`: Main orchestration script.
*   `publication/cms_db.py`: Database utility functions (fetching configs, websites).
*   `publication/utils.py`: Shared utilities (image generation, API quota checks, publication status checks).
*   `publication/app_test.py`: Core publication logic (`main_publication2`).

## Configuration Scope

These settings control the operational scope of the **News Translation** module (general news scraping & translation):

### General Settings
- **Enable News Scrap and Translate**: Master switch to activate/deactivate the scraping and translation of external news.

### Source & Target
- **News Translation Sources**: Configure specific external websites to scrape and translate.
  - **URL**: The source website URL (e.g., `https://citisportsonline.com`).
  - **Languages**: Select target languages for translation (e.g., `Spanish`, `Arabic`, `Russian`).
  - **Categories**: Define specific content categories to associate with the translated articles.
