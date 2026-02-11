from dotenv import load_dotenv
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from publication.utils import generate_gemini_image, replace_vars

def generate_player_abroad_image(player, l_version, types, key, website=None):
    player_id = player['playerId']
    player_name = player['playerName']
    fixture_id = player['fixtureId']
    event_type = player['eventType']
    event_detail = player['eventDetail']
    league_name = player['league']
    team_name = player['team']
    nationality = player['nationality']
    league_country = player['leagueCountry']

    custom_prompt = website.get('data', {}).get('player_abroad_news_image_prompt') if website else None

    if custom_prompt:
        prompt_vars = {
            "event_type": event_type,
            "league_name": league_name,
            "player_name": player_name,
            "event_detail": event_detail,
            "team_name": team_name,
            "nationality": nationality,
            "league_country": league_country
        }
        # Replace variables with values
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a abroad player image with the following details:\n{prompt_text}"
    else:
        if l_version == 'eng':
            prompt_content = f"I am a top level professional soccer news website. Generate a sports news style image for an abroad player highlight. The generated image must be the real image of the player. \n\nDetails:\n- Player: { player_name }\n- Event: { event_type } \n- League: { league_name }\n\nImage requirements:\n- Use { player_name }’s real photo in action from the match.\n- Include the official { league_name } logo in the design.\n- Clearly show the event { event_type } visually (celebration if goal, referee showing red card if red card).\n- Do not write the player name, event type, or league name as text in the image.\n- Style: professional football news graphic, dynamic sports photography style.\n- Generate a slightly different variation every time (different angles, background, or action moments).\n- Format: 16:9 horizontal for website article and 1:1 square for social media.\n"
            prompt = f"Generate a abroad player image with the following details:\n{prompt_content}"
        else:
            # Handle other languages or default case if needed
            return

    generate_gemini_image(prompt, key, l_version, types)