from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
import httpx
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from api.api_image import generate_image
from publication.save_img_aws import save_aws, delete_img
from api.api_content import generate_content
from publication.app_test import publish
from publication.utils import check_image_exists, download_aws_image

from auth.middleware import AuthMiddleware

app = FastAPI()
app.add_middleware(AuthMiddleware)  # ✅ apply to all routes


# -------------------------
# Models
# -------------------------
class GoalScorer(BaseModel):
    player_name: str
    team: str
    minute: str

class PlayerToWatch(BaseModel):
    player_name: str
    session_goals: int
    team: str

class Category(BaseModel):
    id: int
    name: Optional[str]

class League(BaseModel):
    name: str
    id: int
    categories: Optional[List[Category]] = None

class NewsRequest(BaseModel):
    id: str
    home_team: str
    away_team: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    summary: Optional[str] = None
    goalscorers: Optional[List[GoalScorer]] = None
    league: Optional[League] = None
    match_date: Optional[str] = None
    venue: Optional[str] = None
    home_team_position: Optional[str] = None
    away_team_position: Optional[str] = None
    players_to_watch: Optional[List[PlayerToWatch]] = None
    websites_ids: Optional[List] = None

class NewsResponse2(BaseModel):
    id: str
    website_id: str
    image_url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
class NewsResponse(BaseModel):
    success: bool
    message: str
    data: Optional[List[NewsResponse2]] = None


# -------------------------
# Routes
# -------------------------
@app.post("/api/generate-news/{types}", response_model=NewsResponse)
async def generate_news(types: str, request: NewsRequest, background_tasks: BackgroundTasks):
    try:
        data = {
            "home_team": request.home_team,
            "away_team": request.away_team,
            "summary": request.summary,
            "league": request.league or League(name="", id=0),
            "match_date": request.match_date,
            "venue": request.venue,
            "websites_ids": request.websites_ids or [],
            "id": request.id
        }
        
        if types == 'preview':
            data['home_team_position'] = request.home_team_position
            data['away_team_position'] = request.away_team_position
            data['players_to_watch'] = request.players_to_watch or [],
        
        elif types == 'review':
            data['home_score'] = request.home_score
            data['away_score'] = request.away_score
            data['goalscorers'] = request.goalscorers or []
        else:
            raise HTTPException(status_code=400, detail="Unknown types")
        
        result = []
        for id in data['websites_ids']:

            # generate image
            generate_image(data, 'eng', id, types)

            # save into aws
            image_url = save_aws(f"{data['id']}_{id}", 'eng', types)
            #print("saved aws")
            title, content = generate_content(data, 'eng', id, types)
            res = {
                "website_id": id,
                "title": title,
                "content": content,
                "image_url": image_url,
                "id": data.get('id')
            }
            result.append(res)
        return NewsResponse(
            success=True,
            message="News content generated successfully",
            data=result,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating news: {str(e)}")

class WebsiteDetails(BaseModel):
    id: str
    platform_name: str
    platform_url: str
    platform_user: str
    platform_password: str
    categories: Optional[List[Category]] = None

class ContentDetails(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str] = None
    website: WebsiteDetails

class NewsPublishRequest(BaseModel):
    data: List[ContentDetails]

class NewsPublishResponse(BaseModel):
    success: bool
    message: str
    posted_websites: List[str]
    failed_websites: List[str]
    
@app.post("/api/publish-news/{types}", response_model=NewsPublishResponse)
async def publish_news(types:str, request: NewsPublishRequest, background_tasks: BackgroundTasks):
    try:
        if types in ['preview', 'review']:
            posted_websites = []
            failed_websites = []
            for data in request.data:
                id = data.id
                title = data.title
                content = data.content
                website = data.website
                image_url = data.image_url
                website_dict = website.model_dump()
                website_dict["categories"] = [cat.model_dump() for cat in website.categories]

                try: 
                    if image_url:
                        if not check_image_exists('eng',types, f"{id}_{website_dict['id']}"):
                            download_aws_image('eng',types, f"{id}_{website_dict['id']}")

                    response = publish(website_dict, '', '', '', image_url, title, content, types, f"{id}_{website_dict['id']}", 'eng', '')
                    if response:
                        delete_img(f"{id}_{website_dict['id']}", 'eng',types)
                        posted_websites.append(website_dict['id'])
                    else:
                        failed_websites.append(website_dict['id'])
                except Exception as _ex:
                    print(f"[Error] while publishing title:{title} error: {_ex}")

            return NewsPublishResponse(
                success=True,
                message="News published successfully",
                posted_websites = posted_websites,
                failed_websites= failed_websites
            )

        else:
            raise HTTPException(status_code=404)
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing news: {str(e)}")
    
