# Installation Guide

## 1. Install Python

### For Linux:
To install Python on Linux, open the terminal and run the following commands:
```bash
sudo apt update
sudo apt install python3
```

### For Windows:
You can download and install Python from the official Python website by following these steps: [Python Downloads](https://www.python.org/downloads/)


## 2. Install Dependencies

Once Python is installed, the next step is to install the required dependencies. The required packages and libraries are listed in the `requirements.txt` file. To install them, execute the following command in your terminal or command prompt:

```bash
pip install -r requirements.txt
```

# How It Works

## 1. Preview Bot

The **Preview Bot** fetches upcoming fixture details and generates a preview for matches. It retrieves match schedules from **RapidAPI** and processes the data before sending it to **OpenAI** for content generation.

### Run the Preview Bot
To execute the Preview Bot, use the following command:
```bash
python3 preview/main_preview.py
```

### League IDs:
The bot fetches fixtures for the following league IDs:
```python
list_league_id = ['39', '61', '78', '140', '135', '94', '253', '307']
```

### Fixture Retrieval:
- If `search_method` is set to `'future'`, the bot fetches upcoming fixtures by date from **RapidAPI**.
- If `search_method` is set to `'all_day'`, the bot retrieves fixtures scheduled for the current date from **RapidAPI**.

### Example Data from RapidAPI:
The bot interacts with **RapidAPI** and retrieves fixture data such as:
- Fixture
- Venue
- Status
- League
- Teams
- Away Goals, etc.


### Data Processing with OpenAI

1. The bot formats the retrieved fixture data into a structured layout.
2. The formatted data is then sent to **OpenAI** for generating a preview article or summary.
3. The generated content can be utilized for **website publishing** or **media posts**.


## 2. Review Bot

The **Review Bot** performs match reviews similar to the Preview Bot. It fetches fixture data from the database, checks if the current date is greater than the match date, and generates reviews for completed matches using **RapidAPI** and **OpenAI**.

### Run the Review Bot
To execute the Review Bot, use the following command:
```bash
python3 review/main_review.py
```

### Fixture List:
The bot retrieves fixtures from the following match IDs:
```python
list_fixture_match = [1208288, 1208284, 1208289, 1208290, 1252616, 1252610, 1252609, 1252613, 1208286, 1208283, 1208285, 1208291, 1252612, 1252611, 1252614, 1208292]
```

### Match Review Process:
1. **Fixture Retrieval**:
   - The bot checks the database for fixture data and compares the current date with the match date.
   - If the current date is greater than the match date, the bot generates the review for that match.

2. **Data Fetching from RapidAPI**:
   - The bot calls the **RapidAPI** service to fetch detailed match information (team names, scores, goals, events, etc.).

3. **Data Formatting**:
   - Once the data is fetched, the bot formats it for review generation.

4. **Review Generation with OpenAI**:
   - The bot sends a prompt to **OpenAI** to generate a review based on match details.
   - The output is a review article providing insights, analysis, and summary of the match.

5. **Output for Website Posting**:
   - The bot generates content ready to be posted on websites.

# Configuration & Prompts

All AI generation prompts (Headlines, Articles, and Images) are now **dynamically configurable** via the Admin Dashboard.

- **Source**: Prompts are fetched from the CMS endpoint `api::news-prompt.news-prompt`.
- **Customization**: You can modify the phrasing, tone, and structure of news generation without altering the codebase.
- **Variables**: The dashboard supports dynamic placeholders (e.g., `{player_name}`, `{team1}`, `{match_date}`) which are replaced at runtime with actual data.

If no custom prompt is set in the dashboard, the system automatically falls back to the default hardcoded logic.