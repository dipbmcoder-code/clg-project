from publication.utils import generate_gemini_image
from datetime import datetime

def generate_image(data, l_version, id, types):
    print(f"types:{types}")
    match_date = data.get('match_date')
    dt = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
    formatted_date = dt.strftime("%d %B %Y")
    if types == 'preview':
        if l_version == 'eng':
            prompt = {
                "league_name": data['league'].name,
                "home_team": data.get('home_team'),
                "away_team": data.get('away_team'),
                "match_date": formatted_date,
                "venue": data.get('venue',''),
                "design": "modern, clean, professional sports news graphic, bold typography, authentic sports media style, use a real action photograph of players from these teams as the full background remains clearly visible and not covered by overlays, do not use abstract, gradient, digital art, or poster-style backgrounds, team logos should be automatically fetched and displayed near team names, league logo small and subtle in one corner if available, logos and text overlays should be small and not block the players without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players.",
                "size": "1024x1024"
            }

            prompt = f"Generate a football match preview image with the following details:\n{prompt}"
        
    elif types == 'review':
        if l_version == 'eng':
            prompt = {
                "league_name": data['league'].name,
                "home_team": {
                    "name": data.get('home_team'),
                    "goals": data.get('home_score'),
                },
                "away_team": {
                    "name": data.get('away_team'),
                    "goals": data.get('away_score'),
                },
                "venue": data.get('venue',''),
                "match_date": formatted_date,
                "design": "modern, clean, professional sports news review graphic, bold typography, authentic sports media style, automatically fetch and display the official league logo in the top-left corner, and fetch team small logos to display beside team names and scores in small without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players. Make sure the real action photo of players from this match remains clearly visible and not covered by overlays. Do not use abstract, gradient, digital art, or poster-style backgrounds",
                "size": "1024x1024",
            }
            prompt = f"Generate a football match review image with the following details:\n{prompt}"
    generate_gemini_image(prompt, f"{data['id']}_{id}", l_version, types)