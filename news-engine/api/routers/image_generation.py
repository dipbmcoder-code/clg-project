from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import base64
import json
import os
from datetime import datetime

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str
    home_team: str
    away_team: str
    manual_news_id: Optional[str] = None

class ImageResponse(BaseModel):
    success: bool
    message: str
    image_id: Optional[str] = None
    image_url: Optional[str] = None

def build_review_image_prompt(
    home_team: str,
    away_team: str,
    home_score: int,
    away_score: int,
    league: dict,
    venue: str,
    match_date: str
) -> str:
    league_name = league.get("name", "Football League") if league else "Football League"
    venue_name = venue or "Stadium"
    formatted_date = match_date or datetime.now().strftime("%Y-%m-%d")
    
    return json.dumps({
        "league_name": league_name,
        "home_team": {
            "name": home_team,
            "goals": home_score
        },
        "away_team": {
            "name": away_team,
            "goals": away_score
        },
        "venue": venue_name,
        "match_date": formatted_date,
        "design": "modern, clean, professional sports news review graphic, bold typography, authentic sports media style, automatically fetch and display the official league logo in the top-left corner, and fetch team small logos to display beside team names and scores in small without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players. Make sure the real action photo of players from this match remains clearly visible and not covered by overlays. Do not use abstract, gradient, digital art, or poster-style backgrounds",
        "size": "1024x1024"
    })

def build_preview_image_prompt(
    home_team: str,
    away_team: str,
    league: dict,
    venue: str,
    match_date: str
) -> str:
    league_name = league.get("name", "Football League") if league else "Football League"
    venue_name = venue or "Stadium"
    formatted_date = match_date or datetime.now().strftime("%Y-%m-%d")
    
    return json.dumps({
        "league_name": league_name,
        "home_team": {
            "name": home_team
        },
        "away_team": {
            "name": away_team
        },
        "match_date": formatted_date,
        "venue": venue_name,
        "design": "modern, clean, professional sports news graphic, bold typography, authentic sports media style, use a real action photograph of players from these teams as the full background remains clearly visible and not covered by overlays, do not use abstract, gradient, digital art, or poster-style backgrounds, team logos should be automatically fetched and displayed near team names, league logo small and subtle in one corner if available, logos and text overlays should be small and not block the players without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players.",
        "size": "1024x1024"
    })

async def generate_gemini_image(prompt: str) -> str:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-website.com",
        "X-Title": "Sports News Generator"
    }
    
    payload = {
        "model": "google/gemini-2.5-flash-image-preview:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate a professional football match image based on these details:\n{prompt}\n\nReturn only the image, no additional text."
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract base64 image
        content = result.get("choices", [{}])[0].get("message", {}).get("content")
        
        if isinstance(content, list):
            for part in content:
                if part.get("type") == "image" and part.get("data"):
                    return part["data"]
        elif isinstance(content, str) and content.startswith("data:image"):
            return content.split(",")[1]
        
        # Fallback: search for base64 in response
        response_str = json.dumps(result)
        import re
        base64_match = re.search(r'"data:image/[^;]+;base64,([^"]+)"', response_str)
        if base64_match:
            return base64_match.group(1)
        
        raise Exception("No image found in response")

@router.post("/generate-image", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    try:
        base64_image = await generate_gemini_image(request.prompt)
        
        # In a real implementation, you would save the image to storage
        # and return the image URL or ID
        # For now, we'll return the base64 data as a URL
        
        image_url = f"data:image/png;base64,{base64_image}"
        
        return ImageResponse(
            success=True,
            message="Image generated successfully",
            image_url=image_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")