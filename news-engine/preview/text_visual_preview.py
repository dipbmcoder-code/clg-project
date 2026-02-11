import os
from dotenv import load_dotenv
from pathlib import Path
import datetime
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
import requests
from preview.db_preview import get_data
from publication.utils import generate_gemini_image, replace_vars

#!/opt/footballBot/football_bot/venv_new/bin/python3
def output_visual_text(fixture_match):
    from PIL import Image, ImageDraw, ImageFont
    from db_preview import get_data
    import requests
    from urllib.request import urlopen

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"        # V3 - Next {x} Fixtures to come
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_logo = requests.get(url, headers=headers, params={
        'id':f'{fixture_match}'
    })
    data_logo = req_logo.json()

    logo_team_home = data_logo['response'][0]['teams']['home']['logo']
    logo_team_away = data_logo['response'][0]['teams']['away']['logo']
    city = data_logo['response'][0]['fixture']['venue']['city']
    league_name = data_logo['response'][0]['league']['name']

    # if name_league == "Premier League":
    #     name_league = "English" + " " + name_league

    insert_query = (
        f"SELECT fixture_match, name_home_preview, name_away_preview, date_match FROM match_preview WHERE fixture_match3={fixture_match}"
    )

    r = get_data(insert_query)

    r = r[0]

    # Создание переменных по индексам результата
    #fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_home_name, topscorers_fouls_home_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_last_games_who, home_last_games_rival, home_last_games_scores, away_last_games_who, away_last_games_rival, away_last_games_scores, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away = r[0], r[1], r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[21],r[22],r[23],r[24],r[25],r[26],r[27],r[28],r[29],r[30],r[31],r[32],r[33],r[34],r[35],r[36],r[37],r[38],r[39],r[40],r[41],r[42],r[43],r[44],r[45],r[46],r[47],r[48],r[49],r[50],r[51],r[52],r[53],r[54],r[55],r[56],r[57],r[58],r[59],r[60],r[61],r[62],r[63],r[64],r[65],r[66],r[67],r[68],r[69],r[70],r[71],r[72],r[73],r[74],r[75],r[76],r[77],r[78],r[79], r[80],r[81],r[82],r[83]
    fixture_match, name_home_preview, name_away_preview, date_match = r # r[0], r[1], r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[21],r[22],r[23],r[24],r[25],r[26],r[27],r[28],r[29],r[30],r[31],r[32],r[33],r[34],r[35],r[36],r[37],r[38],r[39],r[40],r[41],r[42],r[43],r[44],r[45],r[46],r[47],r[48],r[49],r[50],r[51],r[52],r[53],r[54],r[55],r[56],r[57],r[58],r[59],r[60],r[61],r[62],r[63],r[64],r[65],r[66],r[67],r[68],r[69],r[70],r[71],r[72],r[73],r[74],r[75],r[76],r[77],r[78],r[79],r[80],r[81],r[82],r[83],r[84],r[85],r[86],r[87],r[88],r[89],r[90],r[91],r[92],r[93],r[94],r[95],r[96],r[97],r[98],r[99],r[100],r[101],r[102],r[103],r[104],r[105],r[106],r[107],r[108],r[109],r[110],r[111],r[112],r[113],r[114],r[115],r[116],r[117],r[118]

    font_for_name = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=105)
    font_for_league = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=140)
    font_for_city = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=120)
    font_for_date = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=120)
    font_for_date2 = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=140)
    font_for_preview = ImageFont.truetype(str(root_folder / 'tools' / 'fonts' / 'Kanit-SemiBoldItalic.ttf'), size=350)
    # font_for_league = ImageFont.truetype('/home/tricore23/Documents/python/FootballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=140)
    # font_for_city = ImageFont.truetype('/home/tricore23/Documents/python/FootballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=120)
    # font_for_date = ImageFont.truetype('/home/tricore23/Documents/python/FootballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=120)
    # font_for_date2 = ImageFont.truetype('/home/tricore23/Documents/python/FootballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=140)
    
    background = Image.open(root_folder / 'tools' / 'img' / 'EPL1.png')

    logo_home = Image.open(urlopen(logo_team_home))
    logo_away = Image.open(urlopen(logo_team_away))
    

    name_team = ImageDraw.Draw(background)
    # name_team.line(((725, 1500), (725, 1200)), "red") #якорь, метка откуда начинается текст
    # name_team.line(((600, 1350), (900, 1350)), "red")
    name_team.text((1700, 1350), name_home_preview, anchor="ms", font=font_for_name, fill='white')
    # name_team.line(((2825, 1500), (2825, 1200)), "red") #якорь, метка откуда начинается текст
    # name_team.line(((2725, 1350), (2925, 1350)), "red")
    name_team.text((3300, 1350), name_away_preview, anchor="ms", font=font_for_name)

    league0 = ImageDraw.Draw(background)
    # league0.line(((1775, 1640), (1775, 1580)), "red") #якорь, метка откуда начинается текст
    # league0.line(((1600, 1600), (1900, 1600)), "red")
    x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
    league0.text((2500, 1600), x.strftime('%B %d %Y'), anchor="ms", font=font_for_league, fill='white')

    # city0 = ImageDraw.Draw(background)
    # league0.line(((1775, 1640), (1775, 1580)), "red") #якорь, метка откуда начинается текст
    # league0.line(((1600, 1600), (1900, 1600)), "red")
    # city0.text((1775, 1750), city, anchor="ms", font=font_for_city, fill='white')

    date = ImageDraw.Draw(background)
    # date.line(((1775, 290), (1775, 220)), "red") #якорь
    # date.line(((1600, 240), (1900, 240)), "red")
    # x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
    date.text((2500, 400), "Preview", anchor='ms', font=font_for_preview, fill='white')
    # date.text((1775, 400), date_match[11:], anchor='ms', font=font_for_date2, fill='white')
    
    
    new_size_logo1 = logo_home.resize((550, 550))
    new_size_logo2 = logo_away.resize((550, 550))

    background.paste(new_size_logo1, (1400, 700), mask=new_size_logo1.convert('RGBA'))
    background.paste(new_size_logo2, (3000, 700), mask=new_size_logo2.convert('RGBA'))

    #Сохранение
    new_image = background.resize((1778, 1000))
    #TODO была ошибка
    new_image.save(root_folder / 'result' / 'img_match' / f'eng_{fixture_match}_preview.png')
    #background.save(f'/opt/footballBot/result/img_match/{fixture_match}_preview.png')
    
    

    #HOME



    #AWAY

def output_visual_gemini_text(fixture_match, l_version, types, website=None):

    # ...existing code to get match info...
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"        # V3 - Next {x} Fixtures to come
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_logo = requests.get(url, headers=headers, params={
        'id':f'{fixture_match}'
    })
    data_logo = req_logo.json()

    logo_team_home = data_logo['response'][0]['teams']['home']['logo']
    logo_team_away = data_logo['response'][0]['teams']['away']['logo']
    city = data_logo['response'][0]['fixture']['venue']['city']
    venue = data_logo['response'][0]['fixture']['venue']['name']
    league_name = data_logo['response'][0]['league']['name']
    league_logo = data_logo['response'][0]['league']['logo']

    insert_query = (
        f"SELECT fixture_match, name_home_preview, name_away_preview, date_match FROM match_preview WHERE fixture_match3={fixture_match}"
    )

    r = get_data(insert_query)

    r = r[0]

    fixture_match, name_home_preview, name_away_preview, date_match = r

    x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
    x = x.strftime('%B %d %Y')

    custom_prompt = website.get('data', {}).get('preview_news_image_prompt') if website else None
    
    if custom_prompt:
        prompt_vars = {
            "team1": name_home_preview,
            "team2": name_away_preview,
            "league_name1": league_name,
            "venue": venue or "Stadium",
            "new_date": x,
            "league_name": league_name, # alias
            "home_team": name_home_preview,
            "away_team": name_away_preview,
            "match_date": x
        }
        # Replace variables
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a football match preview image with the following details:\n{prompt_text}"
    else:
        prompt = {
            "league_name": league_name,
            "home_team": {
                "name": name_home_preview,
            },
            "away_team": {
                "name": name_away_preview,
            },
            "match_date": x,
            "venue": venue,
            "design": "modern, clean, professional sports news graphic, bold typography, authentic sports media style, use a real action photograph of players from these teams as the full background remains clearly visible and not covered by overlays, do not use abstract, gradient, digital art, or poster-style backgrounds, team logos should be automatically fetched and displayed near team names, league logo small and subtle in one corner if available, logos and text overlays should be small and not block the players without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players.",
            "size": "1024x1024"
        }
        prompt = f"Generate a football match preview image with the following details:\n{prompt}"

    generate_gemini_image(prompt, fixture_match, l_version, types)
    
