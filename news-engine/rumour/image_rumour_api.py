from dotenv import load_dotenv
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from publication.utils import generate_gemini_image, replace_vars
import json

def generate_rumours_image(rumour, key, l_version, types, website):
    if l_version == 'eng':
        custom_prompt = website.get('data', {}).get('rumor_news_image_prompt')
        if custom_prompt:
            prompt_vars = {
                "player_name": rumour['player']['name'],
                "position": rumour['player']['position'],
                "from_club": rumour['rumour']['from_club']['name'],
                "to_club": rumour['rumour']['to_club']['name'],
                "from_country": rumour['rumour']['from_club']['flag'],
                "to_country": rumour['rumour']['to_club']['flag'],
                "to_league": rumour['rumour']['to_league']['name'],
                "from_league": rumour['rumour']['from_league']['name'],
                "rumor_date": rumour['rumour']['date'],
                "market_value": rumour['rumour']['market_value'],
                "nationality": rumour['player']['nationality'],
            }
            prompt_text = replace_vars(custom_prompt, prompt_vars)
        else:
            prompt_text = f"""
                POLICY: NO identifiable people or player faces. Use abstract football imagery, dual club branding, and typography with rumour indicators.

                Create a professional football transfer RUMOUR graphic:
                Player: {rumour['player']['name']}
                FROM: {rumour['rumour']['from_club']['name']} ⟷ TO: {rumour['rumour']['to_club']['name']}
                Status: TRANSFER RUMOUR / SPECULATION

                VISUAL ELEMENTS:
                - Abstract football imagery: ball, stadium, pitch patterns, goal nets
                - Generic silhouettes (no faces), motion graphics
                - Question mark (?) symbols integrated
                - Stadium background: empty pitch, seating, floodlights
                - Split-screen or dual-tone background (both clubs' colors)
                - Dashed lines, question mark motifs
                - Bokeh/depth effect, energetic breaking news feel

                DUAL CLUB BRANDING (Primary Focus):
                - BOTH logos prominent: {rumour['rumour']['from_club']['name']} (LEFT) + {rumour['rumour']['to_club']['name']} (RIGHT)
                - Dashed arrow (→) or (?→) between clubs
                - "VS" or "TO" text between logos
                - Split-screen design, equal prominence

                TYPOGRAPHY (Critical):
                - "{rumour['player']['name']}" - LARGE, BOLD, PRIMARY
                - RUMOUR INDICATORS: "TRANSFER RUMOUR", "LINKED WITH", "BREAKING", "LATEST"
                - Question mark (?) symbol prominent
                - "SPECULATION" watermark
                - "{rumour['rumour']['from_club']['name']}" ⟷ "{rumour['rumour']['to_club']['name']}"
                - Modern sans-serif fonts (Sky Sports/ESPN style)
                - High contrast white/black text

                COLOR SCHEME:
                - Dual-tone: {rumour['rumour']['from_club']['name']} colors (left) + {rumour['rumour']['to_club']['name']} colors (right)
                - Yellow/orange accents for "BREAKING"/"RUMOUR"
                - Vibrant, eye-catching but credible

                DESIGN:
                - Question mark (?) watermark/icon
                - Dashed arrows, "RUMOUR" overlay, "LINKED" badge
                - Breaking news banners, geometric shapes
                - 16:9 landscape, high resolution
                - Professional sports broadcast aesthetic (Sky Sports Transfer Centre, ESPN FC, BBC Sport)
                - Balance: dynamic/speculative yet professional/trustworthy
            """

        prompt = f"Generate a rumour player image with the following details:\n{prompt_text}"

        generate_gemini_image(prompt, key, l_version, types)