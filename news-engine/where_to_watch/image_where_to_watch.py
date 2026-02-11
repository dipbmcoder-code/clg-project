from dotenv import load_dotenv
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from publication.utils import generate_gemini_image, replace_vars

def generate_where_to_watch_image(league, id, l_version, types, website=None):
    custom_prompt = website.get('data', {}).get('where_to_watch_news_image_prompt') if website else None
    
    if custom_prompt:
        prompt_vars = {
            "league_name": league['league']['name'],
            "start_date": league['seasons'][0]['start'],
            "end_date": league['seasons'][0]['end'],
            "season_year": league['seasons'][0]['year'],
            "country_name": league['country']['name'],
            "league_country": league['country']['name'] # alias
        }
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a where to watch image with the following details:\n{prompt_text}"
    elif l_version == 'eng':
        prompt = {
            "league_name": league['league']['name'],
            "start_date": league['seasons'][0]['start'],
            "league_country": league['country']['name'],
            "logo": league['league']['logo'],
            "design": "A modern, clean, professional sports news graphic where we can watch this league. League's logos should be automatically fetched and displayed thier name, country and start date. Show some popular player's action photo should be clearly visible, not an illustration. Full realistic background should remain clearly visible (such as stadium, press conference, or training ground), without abstract, gradient, digital art, or poster-style effects. Designed in authentic sports media style.",
            "size": "1024x1024"
        }

        prompt = f"Generate a where to watch image with the following details:\n{prompt}"
    else:
        # Fallback
        prompt = f"Generate a where to watch image for {league['league']['name']}"

    generate_gemini_image(prompt, id, l_version, types)