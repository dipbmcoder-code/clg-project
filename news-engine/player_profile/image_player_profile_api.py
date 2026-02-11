from dotenv import load_dotenv
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from publication.utils import generate_gemini_image, replace_vars

def generate_player_profile_image(player, l_version, types, key, website=None):
    player_name = player['name']
    
    custom_prompt = website.get('data', {}).get('player_profile_news_image_prompt') if website else None
    
    if custom_prompt:
        prompt_vars = {
            "player_name": player_name
        }
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a player profile image with the following details:\n{prompt_text}"
    elif l_version == 'eng':
        prompt = {
            "Detail": f"I am a professional football news website. Generate a sports news style image for an player profile. \n\nImage requirements:\n- Use { player_name }’s real photo.\n- Do not write the player name as text in the image.\n- Style: professional football news graphic, dynamic sports photography style.\n- Generate a slightly different variation every time (different angles, background, or action moments).\n- Format: 16:9 horizontal for website article and 1:1 square for social media.\n"
        }

        prompt = f"Generate a player profile image with the following details:\n{prompt}"
    else:
        # Default fallback if needed
        prompt = f"Generate a player profile image for {player_name}"
        
    generate_gemini_image(prompt, key, l_version, types)