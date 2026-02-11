from dotenv import load_dotenv
from pathlib import Path
import json
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from publication.utils import generate_gemini_image, replace_vars

def generate_transfer_image(transfer, key, l_version, types, website):
    if l_version == 'eng':
        # prompt = {
        #     "player_name": transfer['player']['name'],
        #     "old_club_name": transfer['transfer']['from_club']['name'],
        #     "new_club_name": transfer['transfer']['to_club']['name'],
        #     "design": "A modern, clean, professional sports news graphic announcing a football player transfer. This is a completed transfer so it must be reflected in the generated graphic. Clubs logos should be automatically fetched and displayed near club's names. The player's actual photo should be clearly visible, not an illustration. So you must generate the real photo of the player. Full realistic background should remain clearly visible (such as stadium, press conference, or training ground), without abstract, gradient, digital art, or poster-style effects. Designed in authentic sports media style."
        # }
        custom_prompt = website.get('data', {}).get('transfer_news_image_prompt') if website else None
        if custom_prompt:
            prompt_vars = {
                "player_name": transfer['player']['name'],
                "position": transfer['player']['position'],
                "from_club": transfer['transfer']['from_club']['name'],
                "to_club": transfer['transfer']['to_club']['name'],
                "from_country": transfer['transfer']['from_club']['flag'],
                "to_country": transfer['transfer']['to_club']['flag'],
                "to_league": transfer['transfer']['to_league']['name'],
                "from_league": transfer['transfer']['from_league']['name'],
                "transfer_date": transfer['transfer']['date'],
                "transfer_fee": transfer['transfer']['fee'],
                "market_value": transfer['transfer']['market_value'],
                "nationality": transfer['player']['nationality'],
            }

            # Replace variables with values
            prompt_text = replace_vars(custom_prompt, prompt_vars)
        else:
            prompt_text = f"""
                POLICY: NO identifiable people or player faces. Use abstract football imagery, club branding, and typography only.

                Create a professional football transfer graphic:
                Player: {transfer['player']['name']}
                FROM: {transfer['transfer']['from_club']['name']} → TO: {transfer['transfer']['to_club']['name']}
                Status: TRANSFER COMPLETED ✓

                VISUAL ELEMENTS:
                - Abstract football imagery: ball, stadium, pitch patterns, goal nets
                - Generic silhouettes (no faces), motion graphics
                - Stadium background: empty pitch, seating, floodlights, grass texture
                - Modern gradient with {transfer['transfer']['to_club']['name']} club colors
                - Bokeh/depth effect

                CLUB BRANDING (Primary Focus):
                - {transfer['transfer']['to_club']['name']} logo prominent
                - {transfer['transfer']['from_club']['name']} logo smaller
                - Directional arrow between clubs
                - Club colors throughout

                TYPOGRAPHY (Critical):
                - "{transfer['player']['name']}" - LARGE, BOLD, PRIMARY
                - "TRANSFER COMPLETED" or "OFFICIAL" banner
                - "{transfer['transfer']['from_club']['name']}" → "{transfer['transfer']['to_club']['name']}"
                - Modern sans-serif fonts (Sky Sports/ESPN style)
                - High contrast white/black text

                DESIGN:
                - "CONFIRMED" badge, checkmark (✓)
                - Geometric shapes, borders, broadcast-style banners
                - 16:9 landscape, high resolution
                - Professional sports broadcast aesthetic (Sky Sports, ESPN, BBC Sport)
            """

        prompt = f"Generate a transfer player image with the following details:\n{prompt_text}"

        generate_gemini_image(prompt, key, l_version, types)