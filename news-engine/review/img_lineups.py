from review.db import insert_db, chec_in_db, check_form_review, get_one_data
import requests
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
import os
from dotenv import load_dotenv
load_dotenv()

def request_name_to_api(season, league_id, player_id, name):
    """
    Функция для изменения имени

    Получение с API or Database
    return имя
    """

    """ Проверка есть ли он в БД """
    search_user = get_one_data(
        f"SELECT name FROM players_test WHERE player_id_api = {player_id} AND season = {season} AND league_id = {league_id}")  # -> ['name']
    if search_user == []:
        """
        Если нет: 

        1. Делаем запрос в АПИ 
        2. Получаем firstname + lastname
        3. Сохраняем в переменную "name"
        """
        url = os.getenv('RAPID_API_BASE_URL')+"/players"
        querystring = {"id": str(player_id), "season": season}
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
            "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
        }
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        """ Поиск по ответу """
        try:
            full_name = response['response'][0]['player']['firstname'] + " " + response['response'][0]['player'][
                'lastname']
            if "'" in full_name: full_name = full_name.replace("'", "")

            insert_db(f"INSERT INTO players_test(player_id_api, name, season, league_id) "
                      f"VALUES ('{player_id}','{full_name}', '{season}', '{league_id}')", "add name")

            return full_name  # -> firstname + lastname
        except:
            if name != None:
                if "'" in name: name = name.replace("'", "")

                insert_db(f"INSERT INTO players_test(player_id_api, name, season, league_id) "
                          f"VALUES ('{player_id}','{name}', '{season}', '{league_id}')", "add name")

                return name
            # else:

            ...
    else:
        """
        Если в БД есть:
        Получаем существующее имя по двум 0 индексам  
        """
        return search_user[0][0]  # [('Leo Messi')] -> 'Leo Messi'


def start_img_review_lineups(fixture_match):
    import requests
    from PIL import Image, ImageDraw, ImageFont
    from urllib.request import urlopen

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"          
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_all = requests.get(url, headers=headers, params={
        "id":fixture_match
    })

    data_all = req_all.json()
   
    name_home_review = data_all['response'][0]['teams']['home']['name']
    name_away_review = data_all['response'][0]['teams']['away']['name']
    id_team_home_review = data_all['response'][0]['teams']['home']['id']
    id_team_away_review = data_all['response'][0]['teams']['away']['id']
    season = data_all['response'][0]['league']['season']
    league_id = data_all['response'][0]['league']['id']
    logo_team1 = data_all['response'][0]['teams']['home']['logo']
    logo_team2 = data_all['response'][0]['teams']['away']['logo']
    logo_home = Image.open(urlopen(logo_team1))
    logo_away = Image.open(urlopen(logo_team2))
    font_path = root_folder / 'tools/fonts/BebasNeue-Regular.ttf'
    font_number = ImageFont.truetype(str(font_path), size=48)
    font_player = ImageFont.truetype(str(font_path), size=18)
    background = ''
    new_size_logo1 = logo_home.resize((95, 95))
    new_size_logo2 = logo_away.resize((95, 95))

    # Initialize default values in case lineups data is missing
    plan_home = '4-3-3'  # Default formation
    plan_away = '4-3-3'  # Default formation
    lineups_home = [" "] * 11
    lineups_away = [" "] * 11
    lineups_home_pos = [" "] * 11  
    lineups_away_pos = [" "] * 11
    lineups_home_number = ["0"] * 11
    lineups_away_number = ["0"] * 11

    # Check if lineups data exists
    if ('lineups' in data_all['response'][0] and 
        data_all['response'][0]['lineups'] and 
        len(data_all['response'][0]['lineups']) >= 2):
        
        plan_home = data_all['response'][0]['lineups'][0]['formation']
        plan_away = data_all['response'][0]['lineups'][1]['formation']

        # Reset arrays since we'll be filling them
        lineups_home = []
        lineups_away = []
        lineups_home_pos = []
        lineups_away_pos = []
        lineups_home_number = []
        lineups_away_number = []

        # --- SAFE GET FOR LINEUPS (no KeyError) ---
        lineups = data_all['response'][0].get('lineups', [])

        lineup0 = lineups[0] if len(lineups) > 0 else {}
        lineup1 = lineups[1] if len(lineups) > 1 else {}

        start_xi_0 = lineup0.get('startXI') or []
        start_xi_1 = lineup1.get('startXI') or []

        team0_name = lineup0.get('team', {}).get('name')
        team1_name = lineup1.get('team', {}).get('name')

        # Determine which lineup is home/away
        if team0_name == name_home_review:
            home_xi = start_xi_0
            away_xi = start_xi_1
        else:
            home_xi = start_xi_1
            away_xi = start_xi_0

        # --- MAIN LOOP (SAFE, NO ERROR, NO DUPLICATION) ---
        for line in range(11):

            # ---- HOME ----
            p = {}
            if len(home_xi) > line:
                p = home_xi[line].get('player') or {}

            pid = p.get("id")
            if pid:
                lineups_home.append(request_name_to_api(season, league_id, pid, p.get("name")))
                lineups_home_pos.append(p.get("pos", " "))
                lineups_home_number.append(str(p.get("number", 0)))
            else:
                lineups_home.append(" ")
                lineups_home_pos.append(" ")
                lineups_home_number.append("0")

            # ---- AWAY ----
            p = {}
            if len(away_xi) > line:
                p = away_xi[line].get('player') or {}

            pid = p.get("id")
            if pid:
                lineups_away.append(request_name_to_api(season, league_id, pid, p.get("name")))
                lineups_away_pos.append(p.get("pos", " "))
                lineups_away_number.append(str(p.get("number", 0)))
            else:
                lineups_away.append(" ")
                lineups_away_pos.append(" ")
                lineups_away_number.append("0")

        # for line in range(11):
        #     if data_all['response'][0]['lineups'][0]['team']['name'] == name_home_review:
        #         if data_all['response'][0]['lineups'][0]['startXI'][line]['player']['id'] != None:
        #             lineups_home.append(request_name_to_api(season, league_id, data_all['response'][0]['lineups'][0]['startXI'][line]['player']['id'], data_all['response'][0]['lineups'][0]['startXI'][line]['player']['name']))
        #             lineups_home_pos.append(data_all['response'][0]['lineups'][0]['startXI'][line]['player']['pos'])
        #             lineups_home_number.append(str(data_all['response'][0]['lineups'][0]['startXI'][line]['player']['number']))
        #         else:
        #             lineups_home.append(" ")
        #             lineups_home_pos.append(" ")
        #             lineups_home_number.append("0")
        #     else:
        #         if data_all['response'][0]['lineups'][1]['startXI'][line]['player']['id'] != None:
        #             lineups_home.append(request_name_to_api(season, league_id, data_all['response'][0]['lineups'][1]['startXI'][line]['player']['id'], data_all['response'][0]['lineups'][1]['startXI'][line]['player']['name']))
        #             lineups_home_pos.append(data_all['response'][0]['lineups'][1]['startXI'][line]['player']['pos'])
        #             lineups_home_number.append(str(data_all['response'][0]['lineups'][1]['startXI'][line]['player']['number']))
        #         else:
        #             lineups_home.append(" ")
        #             lineups_home_pos.append(" ")
        #             lineups_home_number.append("0")

        #     if data_all['response'][0]['lineups'][0]['team']['name'] == name_away_review:
        #         if data_all['response'][0]['lineups'][0]['startXI'][line]['player']['id'] != None:
        #             lineups_away.append(request_name_to_api(season, league_id, data_all['response'][0]['lineups'][0]['startXI'][line]['player']['id'], data_all['response'][0]['lineups'][0]['startXI'][line]['player']['name']))
        #             lineups_away_pos.append(data_all['response'][0]['lineups'][0]['startXI'][line]['player']['pos'])
        #             lineups_away_number.append(str(data_all['response'][0]['lineups'][0]['startXI'][line]['player']['number']))
        #         else:
        #             lineups_away.append(" ")
        #             lineups_away_pos.append(" ")
        #             lineups_away_number.append("0")
        #     else:
        #         if data_all['response'][0]['lineups'][1]['startXI'][line]['player']['id'] != None:
        #             lineups_away.append(request_name_to_api(season, league_id, data_all['response'][0]['lineups'][1]['startXI'][line]['player']['id'], data_all['response'][0]['lineups'][1]['startXI'][line]['player']['name']))
        #             lineups_away_pos.append(data_all['response'][0]['lineups'][1]['startXI'][line]['player']['pos'])
        #             lineups_away_number.append(str(data_all['response'][0]['lineups'][1]['startXI'][line]['player']['number']))
        #         else:
        #             lineups_away.append(" ")
        #             lineups_away_pos.append(" ")
        #             lineups_away_number.append("0")

        # Process forwards positions if lineups exist
        for i in range(len(lineups_home_pos)):
            if lineups_home_pos[i] == 'F':
                lineups_home_pos.append(lineups_home_pos[i])
                lineups_home.append(lineups_home[i])
                lineups_home_number.append(lineups_home_number[i])
                del lineups_home_pos[i], lineups_home[i], lineups_home_number[i]

        for k in range(len(lineups_away_pos)):
            if lineups_away_pos[k] == 'F':
                lineups_away_pos.append(lineups_away_pos[k])
                lineups_away.append(lineups_away[k])
                lineups_away_number.append(lineups_away_number[k])
                del lineups_away_pos[k], lineups_away[k], lineups_away_number[k]

    if plan_home == '4-3-3' and plan_away == '4-3-3':
        background = Image.open(root_folder / 'tools/img/ligue_11.png')
        background.paste(new_size_logo1, (20, 8),  mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (1350, 8),  mask=new_size_logo2.convert('RGBA'))


        goalkeeper_home = ImageDraw.Draw(background)
        # goalkeeper_home.line(((230, 400), (230, 550)), "red") #якорь
        # goalkeeper_home.line(((180, 470), (280, 470)), "red")
       
        goalkeeper_home.text((230, 470), lineups_home_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_home.text((230, 510), lineups_home[0], anchor='ms', fill='white', font=font_player)

        defender1_home = ImageDraw.Draw(background)
        # defender1_home.line(((340, 130), (340, 200)), "red") #якорь
        # defender1_home.line(((380, 160), (290, 160)), "red")
        defender1_home.text((340, 160), lineups_home_number[1], anchor='ms', fill='white', font=font_number)
        defender1_home.text((340, 200), lineups_home[1], anchor='ms', fill='white', font=font_player)

        defender2_home = ImageDraw.Draw(background)
        # defender2_home.line(((340, 320), (340, 390)), "red") #якорь
        # defender2_home.line(((380, 360), (290, 360)), "red")
        defender2_home.text((340, 360), lineups_home_number[2], anchor='ms', fill='white', font=font_number)
        defender2_home.text((340, 400), lineups_home[2], anchor='ms', fill='white', font=font_player)

        defender3_home = ImageDraw.Draw(background)
        # defender3_home.line(((340, 550), (340, 620)), "red") #якорь
        # defender3_home.line(((380, 590), (290, 590)), "red")
        defender3_home.text((340, 590), lineups_home_number[3], anchor='ms', fill='white', font=font_number)
        defender3_home.text((340, 630), lineups_home[3], anchor='ms', fill='white', font=font_player)

        defender4_home = ImageDraw.Draw(background)
        # defender4_home.line(((340, 730), (340, 800)), "red") #якорь
        # defender4_home.line(((380, 770), (290, 770)), "red")
        defender4_home.text((340, 770), lineups_home_number[4], anchor='ms', fill='white', font=font_number)
        defender4_home.text((340, 810), lineups_home[4], anchor='ms', fill='white', font=font_player)

        midfielder1_home = ImageDraw.Draw(background)
        # midfielder1_home.line(((460, 220), (460, 300)), "red") #якорь
        # midfielder1_home.line(((500, 260), (410, 260)), "red")
        midfielder1_home.text((460, 260), lineups_home_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_home.text((460, 300), lineups_home[5], anchor='ms', fill='white', font=font_player)

        midfielder2_home = ImageDraw.Draw(background)
        # midfielder2_home.line(((460, 450), (460, 530)), "red") #якорь
        # midfielder2_home.line(((500, 480), (410, 480)), "red")
        midfielder2_home.text((460, 480), lineups_home_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_home.text((460, 520), lineups_home[6], anchor='ms', fill='white', font=font_player)

        midfielder3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((460, 650), (460, 730)), "red") #якорь
        # midfielder3_home.line(((500, 680), (410, 680)), "red")
        midfielder3_home.text((460, 680), lineups_home_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_home.text((460, 720), lineups_home[7], anchor='ms', fill='white', font=font_player)

        forward1_home = ImageDraw.Draw(background)
        # forward1_home.line(((620, 220), (620, 300)), "red") #якорь
        # forward1_home.line(((660, 260), (570, 260)), "red")
        forward1_home.text((620, 260), lineups_home_number[8], anchor='ms', fill='white', font=font_number)
        forward1_home.text((620, 300), lineups_home[8], anchor='ms', fill='white', font=font_player)

        forward2_home = ImageDraw.Draw(background)
        # forward2_home.line(((620, 450), (620, 530)), "red") #якорь
        # forward2_home.line(((660, 480), (570, 480)), "red")
        forward2_home.text((620, 480), lineups_home_number[9], anchor='ms', fill='white', font=font_number)
        forward2_home.text((620, 520), lineups_home[9], anchor='ms', fill='white', font=font_player)

        forward3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((620, 650), (620, 730)), "red") #якорь
        # midfielder3_home.line(((660, 680), (570, 680)), "red")
        forward3_home.text((620, 680), lineups_home_number[10], anchor='ms', fill='white', font=font_number)
        forward3_home.text((620, 720), lineups_home[10], anchor='ms', fill='white', font=font_player)

        goalkeeper_away = ImageDraw.Draw(background)
        # goalkeeper_away.line(((1225, 420), (1225, 520)), "red") #якорь
        # goalkeeper_away.line(((1275, 470), (1175, 470)), "red")
        goalkeeper_away.text((1225, 470), lineups_away_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_away.text((1225, 510), lineups_away[0], anchor='ms', fill='white', font=font_player)

        defender1_away = ImageDraw.Draw(background)
        # defender1_away.line(((1100, 130), (1100, 200)), "red") #якорь
        # defender1_away.line(((1150, 160), (1050, 160)), "red")
        defender1_away.text((1100, 160), lineups_away_number[1], anchor='ms', fill='white', font=font_number)
        defender1_away.text((1100, 200), lineups_away[1], anchor='ms', fill='white', font=font_player)
    #
        defender2_away = ImageDraw.Draw(background)
        # defender2_away.line(((1100, 320), (1100, 390)), "red") #якорь
        # defender2_away.line(((1150, 360), (1050, 360)), "red")
        defender2_away.text((1100, 360), lineups_away_number[2], anchor='ms', fill='white', font=font_number)
        defender2_away.text((1100, 400), lineups_away[2], anchor='ms', fill='white', font=font_player)
    #
        defender3_away = ImageDraw.Draw(background)
        # defender3_away.line(((1100, 550), (1100, 620)), "red") #якорь
        # defender3_away.line(((1150, 590), (1050, 590)), "red")
        defender3_away.text((1100, 590), lineups_away_number[3], anchor='ms', fill='white', font=font_number)
        defender3_away.text((1100, 630), lineups_away[3], anchor='ms', fill='white', font=font_player)
    #
        defender4_away = ImageDraw.Draw(background)
        # defender4_away.line(((1100, 730), (1100, 800)), "red") #якорь
        # defender4_away.line(((1150, 770), (1050, 770)), "red")
        defender4_away.text((1100, 770), lineups_away_number[4], anchor='ms', fill='white', font=font_number)
        defender4_away.text((1100, 810), lineups_away[4], anchor='ms', fill='white', font=font_player)
    #
        midfielder1_away = ImageDraw.Draw(background)
        # midfielder1_away.line(((990, 220), (990, 300)), "red") #якорь
        # midfielder1_away.line(((1050, 260), (950, 260)), "red")
        midfielder1_away.text((990, 260), lineups_away_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_away.text((990, 300), lineups_away[5], anchor='ms', fill='white', font=font_player)
    #
        midfielder2_away = ImageDraw.Draw(background)
        # midfielder2_away.line(((990, 450), (990, 530)), "red") #якорь
        # midfielder2_away.line(((1050, 480), (950, 480)), "red")
        midfielder2_away.text((990, 480), lineups_away_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_away.text((990, 520), lineups_away[6], anchor='ms', fill='white', font=font_player)
    #
        midfielder3_away = ImageDraw.Draw(background)
        # midfielder3_away.line(((990, 650), (990, 730)), "red") #якорь
        # midfielder3_away.line(((1050, 680), (950, 680)), "red")
        midfielder3_away.text((990, 680), lineups_away_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_away.text((990, 720), lineups_away[7], anchor='ms', fill='white', font=font_player)
    #
        forward1_away = ImageDraw.Draw(background)
        # forward1_away.line(((840, 220), (840, 300)), "red") #якорь
        # forward1_away.line(((860, 260), (810, 260)), "red")
        forward1_away.text((840, 260), lineups_away_number[8], anchor='ms', fill='white', font=font_number)
        forward1_away.text((840, 300), lineups_away[8], anchor='ms', fill='white', font=font_player)

        forward2_away = ImageDraw.Draw(background)
        # forward2_away.line(((840, 450), (840, 530)), "red") #якорь
        # forward2_away.line(((860, 480), (810, 480)), "red")
        forward2_away.text((840, 480), lineups_away_number[9], anchor='ms', fill='white', font=font_number)
        forward2_away.text((840, 520), lineups_away[9], anchor='ms', fill='white', font=font_player)
    #
        forward3_away = ImageDraw.Draw(background)
        # forward3_away.line(((840, 650), (840, 730)), "red") #якорь
        # forward3_away.line(((860, 680), (810, 680)), "red")
        forward3_away.text((840, 680), lineups_away_number[10], anchor='ms', fill='white', font=font_number)
        forward3_away.text((840, 720), lineups_away[10], anchor='ms', fill='white', font=font_player)

    elif plan_home == '4-2-3-1' and plan_away == '4-2-3-1':
        background = Image.open(root_folder / 'tools/img/ligue_11.png')
        background.paste(new_size_logo1, (20, 8),  mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (1350, 8),  mask=new_size_logo2.convert('RGBA'))


        goalkeeper_home = ImageDraw.Draw(background)
        # goalkeeper_home.line(((230, 400), (230, 550)), "red") #якорь
        # goalkeeper_home.line(((180, 470), (280, 470)), "red")
        goalkeeper_home.text((230, 470), lineups_home_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_home.text((230, 510), lineups_home[0], anchor='ms', fill='white', font=font_player)

        defender1_home = ImageDraw.Draw(background)
        # defender1_home.line(((340, 130), (340, 200)), "red") #якорь
        # defender1_home.line(((380, 160), (290, 160)), "red")
        defender1_home.text((340, 160), lineups_home_number[1], anchor='ms', fill='white', font=font_number)
        defender1_home.text((340, 200), lineups_home[1], anchor='ms', fill='white', font=font_player)

        defender2_home = ImageDraw.Draw(background)
        # defender2_home.line(((340, 320), (340, 390)), "red") #якорь
        # defender2_home.line(((380, 360), (290, 360)), "red")
        defender2_home.text((340, 360), lineups_home_number[2], anchor='ms', fill='white', font=font_number)
        defender2_home.text((340, 400), lineups_home[2], anchor='ms', fill='white', font=font_player)

        defender3_home = ImageDraw.Draw(background)
        # defender3_home.line(((340, 550), (340, 620)), "red") #якорь
        # defender3_home.line(((380, 590), (290, 590)), "red")
        defender3_home.text((340, 590), lineups_home_number[3], anchor='ms', fill='white', font=font_number)
        defender3_home.text((340, 630), lineups_home[3], anchor='ms', fill='white', font=font_player)

        defender4_home = ImageDraw.Draw(background)
        # defender4_home.line(((340, 730), (340, 800)), "red") #якорь
        # defender4_home.line(((380, 770), (290, 770)), "red")
        defender4_home.text((340, 770), lineups_home_number[4], anchor='ms', fill='white', font=font_number)
        defender4_home.text((340, 810), lineups_home[4], anchor='ms', fill='white', font=font_player)

        midfielder1_home = ImageDraw.Draw(background)
        # midfielder1_home.line(((460, 220), (460, 300)), "red") #якорь
        # midfielder1_home.line(((500, 260), (410, 260)), "red")
        midfielder1_home.text((460, 260), lineups_home_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_home.text((460, 300), lineups_home[5], anchor='ms', fill='white', font=font_player)

        midfielder2_home = ImageDraw.Draw(background)
        # midfielder2_home.line(((460, 650), (460, 730)), "red") #якорь
        # midfielder2_home.line(((500, 680), (410, 680)), "red")
        midfielder2_home.text((460, 680), lineups_home_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_home.text((460, 720), lineups_home[6], anchor='ms', fill='white', font=font_player)

        midfielder3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((540, 130), (540, 200)), "red") #якорь
        # midfielder3_home.line(((600, 160), (510, 160)), "red")
        midfielder3_home.text((540, 160), lineups_home_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_home.text((540, 200), lineups_home[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_home = ImageDraw.Draw(background)
        # midfielder4_home.line(((520, 400), (520, 550)), "red") #якорь
        # midfielder4_home.line(((580, 470), (490, 470)), "red")
        midfielder4_home.text((520, 470), lineups_home_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_home.text((520, 510), lineups_home[8], anchor='ms', fill='white', font=font_player)
        #
        midfielder5_home = ImageDraw.Draw(background)
        # midfielder5_home.line(((540, 730), (540, 800)), "red") #якорь
        # midfielder5_home.line(((600, 770), (510, 770)), "red")
        midfielder5_home.text((540, 770), lineups_home_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_home.text((540, 810), lineups_home[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_home = ImageDraw.Draw(background)
        # midfielder4_home.line(((650, 400), (650, 550)), "red") #якорь
        # midfielder4_home.line(((700, 470), (610, 470)), "red")
        forward1_home.text((650, 470), lineups_home_number[10], anchor='ms', fill='white', font=font_number)
        forward1_home.text((650, 510), lineups_home[10], anchor='ms', fill='white', font=font_player)


        goalkeeper_away = ImageDraw.Draw(background)
        # goalkeeper_away.line(((1225, 420), (1225, 520)), "red") #якорь
        # goalkeeper_away.line(((1275, 470), (1175, 470)), "red")
        goalkeeper_away.text((1225, 470), lineups_away_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_away.text((1225, 510), lineups_away[0], anchor='ms', fill='white', font=font_player)
        #
        defender1_away = ImageDraw.Draw(background)
        # defender1_away.line(((1100, 130), (1100, 200)), "red") #якорь
        # defender1_away.line(((1150, 160), (1050, 160)), "red")
        defender1_away.text((1100, 160), lineups_away_number[1], anchor='ms', fill='white', font=font_number)
        defender1_away.text((1100, 200), lineups_away[1], anchor='ms', fill='white', font=font_player)

        defender2_away = ImageDraw.Draw(background)
        # defender2_away.line(((1100, 320), (1100, 390)), "red") #якорь
        # defender2_away.line(((1150, 360), (1050, 360)), "red")
        defender2_away.text((1100, 360), lineups_away_number[2], anchor='ms', fill='white', font=font_number)
        defender2_away.text((1100, 400), lineups_away[2], anchor='ms', fill='white', font=font_player)

        defender3_away = ImageDraw.Draw(background)
        # defender3_away.line(((1100, 550), (1100, 620)), "red") #якорь
        # defender3_away.line(((1150, 590), (1050, 590)), "red")
        defender3_away.text((1100, 590), lineups_away_number[3], anchor='ms', fill='white', font=font_number)
        defender3_away.text((1100, 630), lineups_away[3], anchor='ms', fill='white', font=font_player)

        defender4_away = ImageDraw.Draw(background)
        # defender4_away.line(((1100, 730), (1100, 800)), "red") #якорь
        # defender4_away.line(((1150, 770), (1050, 770)), "red")
        defender4_away.text((1100, 770), lineups_away_number[4], anchor='ms', fill='white', font=font_number)
        defender4_away.text((1100, 810), lineups_away[4], anchor='ms', fill='white', font=font_player)

        midfielder1_away = ImageDraw.Draw(background)
        # midfielder1_away.line(((990, 220), (990, 300)), "red") #якорь
        # midfielder1_away.line(((1050, 260), (950, 260)), "red")
        midfielder1_away.text((990, 260), lineups_away_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_away.text((990, 300), lineups_away[5], anchor='ms', fill='white', font=font_player)
    #
        midfielder2_away = ImageDraw.Draw(background)
        # midfielder2_away.line(((990, 650), (990, 730)), "red") #якорь
        # midfielder2_away.line(((1050, 680), (950, 680)), "red")
        midfielder2_away.text((990, 680), lineups_away_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_away.text((990, 720), lineups_away[6], anchor='ms', fill='white', font=font_player)
        #
        midfielder3_away = ImageDraw.Draw(background)
        # midfielder3_away.line(((910, 130), (910, 200)), "red") #якорь
        # midfielder3_away.line(((950, 160), (850, 160)), "red")
        midfielder3_away.text((910, 160), lineups_away_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_away.text((910, 200), lineups_away[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_away = ImageDraw.Draw(background)
        # midfielder4_away.line(((930, 400), (930, 550)), "red") #якорь
        # midfielder4_away.line(((950, 470), (850, 470)), "red")
        midfielder4_away.text((930, 470), lineups_away_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_away.text((930, 510), lineups_away[8], anchor='ms', fill='white', font=font_player)

        midfielder5_away = ImageDraw.Draw(background)
        # midfielder5_away.line(((910, 730), (910, 800)), "red") #якорь
        # midfielder5_away.line(((950, 770), (850, 770)), "red")
        midfielder5_away.text((910, 770), lineups_away_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_away.text((910, 810), lineups_away[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_away = ImageDraw.Draw(background)
        # forward1_away.line(((800, 400), (800, 550)), "red") #якорь
        # forward1_away.line(((840, 470), (740, 470)), "red")
        forward1_away.text((800, 470), lineups_away_number[10], anchor='ms', fill='white', font=font_number)
        forward1_away.text((800, 510), lineups_away[10], anchor='ms', fill='white', font=font_player)

    elif plan_home == '4-3-3' and plan_away == '4-2-3-1':
        background = Image.open(root_folder / 'tools/img/ligue_11.png')
        background.paste(new_size_logo1, (20, 8),  mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (1350, 8),  mask=new_size_logo2.convert('RGBA'))


        goalkeeper_home = ImageDraw.Draw(background)
        # goalkeeper_home.line(((230, 400), (230, 550)), "red") #якорь
        # goalkeeper_home.line(((180, 470), (280, 470)), "red")
        goalkeeper_home.text((230, 470), lineups_home_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_home.text((230, 510), lineups_home[0], anchor='ms', fill='white', font=font_player)

        defender1_home = ImageDraw.Draw(background)
        # defender1_home.line(((340, 130), (340, 200)), "red") #якорь
        # defender1_home.line(((380, 160), (290, 160)), "red")
        defender1_home.text((340, 160), lineups_home_number[1], anchor='ms', fill='white', font=font_number)
        defender1_home.text((340, 200), lineups_home[1], anchor='ms', fill='white', font=font_player)

        defender2_home = ImageDraw.Draw(background)
        # defender2_home.line(((340, 320), (340, 390)), "red") #якорь
        # defender2_home.line(((380, 360), (290, 360)), "red")
        defender2_home.text((340, 360), lineups_home_number[2], anchor='ms', fill='white', font=font_number)
        defender2_home.text((340, 400), lineups_home[2], anchor='ms', fill='white', font=font_player)

        defender3_home = ImageDraw.Draw(background)
        # defender3_home.line(((340, 550), (340, 620)), "red") #якорь
        # defender3_home.line(((380, 590), (290, 590)), "red")
        defender3_home.text((340, 590), lineups_home_number[3], anchor='ms', fill='white', font=font_number)
        defender3_home.text((340, 630), lineups_home[3], anchor='ms', fill='white', font=font_player)

        defender4_home = ImageDraw.Draw(background)
        # defender4_home.line(((340, 730), (340, 800)), "red") #якорь
        # defender4_home.line(((380, 770), (290, 770)), "red")
        defender4_home.text((340, 770), lineups_home_number[4], anchor='ms', fill='white', font=font_number)
        defender4_home.text((340, 810), lineups_home[4], anchor='ms', fill='white', font=font_player)

        midfielder1_home = ImageDraw.Draw(background)
        # midfielder1_home.line(((460, 220), (460, 300)), "red") #якорь
        # midfielder1_home.line(((500, 260), (410, 260)), "red")
        midfielder1_home.text((460, 260), lineups_home_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_home.text((460, 300), lineups_home[5], anchor='ms', fill='white', font=font_player)

        midfielder2_home = ImageDraw.Draw(background)
        # midfielder2_home.line(((460, 450), (460, 530)), "red") #якорь
        # midfielder2_home.line(((500, 480), (410, 480)), "red")
        midfielder2_home.text((460, 480), lineups_home_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_home.text((460, 520), lineups_home[6], anchor='ms', fill='white', font=font_player)

        midfielder3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((460, 650), (460, 730)), "red") #якорь
        # midfielder3_home.line(((500, 680), (410, 680)), "red")
        midfielder3_home.text((460, 680), lineups_home_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_home.text((460, 720), lineups_home[7], anchor='ms', fill='white', font=font_player)

        forward1_home = ImageDraw.Draw(background)
        # forward1_home.line(((620, 220), (620, 300)), "red") #якорь
        # forward1_home.line(((660, 260), (570, 260)), "red")
        forward1_home.text((620, 260), lineups_home_number[8], anchor='ms', fill='white', font=font_number)
        forward1_home.text((620, 300), lineups_home[8], anchor='ms', fill='white', font=font_player)

        forward2_home = ImageDraw.Draw(background)
        # forward2_home.line(((620, 450), (620, 530)), "red") #якорь
        # forward2_home.line(((660, 480), (570, 480)), "red")
        forward2_home.text((620, 480), lineups_home_number[9], anchor='ms', fill='white', font=font_number)
        forward2_home.text((620, 520), lineups_home[9], anchor='ms', fill='white', font=font_player)

        forward3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((620, 650), (620, 730)), "red") #якорь
        # midfielder3_home.line(((660, 680), (570, 680)), "red")
        forward3_home.text((620, 680), lineups_home_number[10], anchor='ms', fill='white', font=font_number)
        forward3_home.text((620, 720), lineups_home[10], anchor='ms', fill='white', font=font_player)


        goalkeeper_away = ImageDraw.Draw(background)
        # goalkeeper_away.line(((1225, 420), (1225, 520)), "red") #якорь
        # goalkeeper_away.line(((1275, 470), (1175, 470)), "red")
        goalkeeper_away.text((1225, 470), lineups_away_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_away.text((1225, 510), lineups_away[0], anchor='ms', fill='white', font=font_player)
        #
        defender1_away = ImageDraw.Draw(background)
        # defender1_away.line(((1100, 130), (1100, 200)), "red") #якорь
        # defender1_away.line(((1150, 160), (1050, 160)), "red")
        defender1_away.text((1100, 160), lineups_away_number[1], anchor='ms', fill='white', font=font_number)
        defender1_away.text((1100, 200), lineups_away[1], anchor='ms', fill='white', font=font_player)

        defender2_away = ImageDraw.Draw(background)
        # defender2_away.line(((1100, 320), (1100, 390)), "red") #якорь
        # defender2_away.line(((1150, 360), (1050, 360)), "red")
        defender2_away.text((1100, 360), lineups_away_number[2], anchor='ms', fill='white', font=font_number)
        defender2_away.text((1100, 400), lineups_away[2], anchor='ms', fill='white', font=font_player)

        defender3_away = ImageDraw.Draw(background)
        # defender3_away.line(((1100, 550), (1100, 620)), "red") #якорь
        # defender3_away.line(((1150, 590), (1050, 590)), "red")
        defender3_away.text((1100, 590), lineups_away_number[3], anchor='ms', fill='white', font=font_number)
        defender3_away.text((1100, 630), lineups_away[3], anchor='ms', fill='white', font=font_player)

        defender4_away = ImageDraw.Draw(background)
        # defender4_away.line(((1100, 730), (1100, 800)), "red") #якорь
        # defender4_away.line(((1150, 770), (1050, 770)), "red")
        defender4_away.text((1100, 770), lineups_away_number[4], anchor='ms', fill='white', font=font_number)
        defender4_away.text((1100, 810), lineups_away[4], anchor='ms', fill='white', font=font_player)

        midfielder1_away = ImageDraw.Draw(background)
        # midfielder1_away.line(((990, 220), (990, 300)), "red") #якорь
        # midfielder1_away.line(((1050, 260), (950, 260)), "red")
        midfielder1_away.text((990, 260), lineups_away_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_away.text((990, 300), lineups_away[5], anchor='ms', fill='white', font=font_player)
        #
        midfielder2_away = ImageDraw.Draw(background)
        # midfielder2_away.line(((990, 650), (990, 730)), "red") #якорь
        # midfielder2_away.line(((1050, 680), (950, 680)), "red")
        midfielder2_away.text((990, 680), lineups_away_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_away.text((990, 720), lineups_away[6], anchor='ms', fill='white', font=font_player)
        #
        midfielder3_away = ImageDraw.Draw(background)
        # midfielder3_away.line(((910, 130), (910, 200)), "red") #якорь
        # midfielder3_away.line(((950, 160), (850, 160)), "red")
        midfielder3_away.text((910, 160), lineups_away_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_away.text((910, 200), lineups_away[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_away = ImageDraw.Draw(background)
        # midfielder4_away.line(((930, 400), (930, 550)), "red") #якорь
        # midfielder4_away.line(((950, 470), (850, 470)), "red")
        midfielder4_away.text((930, 470), lineups_away_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_away.text((930, 510), lineups_away[8], anchor='ms', fill='white', font=font_player)

        midfielder5_away = ImageDraw.Draw(background)
        # midfielder5_away.line(((910, 730), (910, 800)), "red") #якорь
        # midfielder5_away.line(((950, 770), (850, 770)), "red")
        midfielder5_away.text((910, 770), lineups_away_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_away.text((910, 810), lineups_away[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_away = ImageDraw.Draw(background)
        # forward1_away.line(((800, 400), (800, 550)), "red") #якорь
        # forward1_away.line(((840, 470), (740, 470)), "red")
        forward1_away.text((800, 470), lineups_away_number[10], anchor='ms', fill='white', font=font_number)
        forward1_away.text((800, 510), lineups_away[10], anchor='ms', fill='white', font=font_player)

    elif plan_home == '4-2-3-1' and plan_away == '4-3-3':
        background = Image.open(root_folder / 'tools/img/ligue_11.png')
        background.paste(new_size_logo1, (20, 8),  mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (1350, 8),  mask=new_size_logo2.convert('RGBA'))


        goalkeeper_home = ImageDraw.Draw(background)
        # goalkeeper_home.line(((230, 400), (230, 550)), "red") #якорь
        # goalkeeper_home.line(((180, 470), (280, 470)), "red")
        goalkeeper_home.text((230, 470), lineups_home_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_home.text((230, 510), lineups_home[0], anchor='ms', fill='white', font=font_player)

        defender1_home = ImageDraw.Draw(background)
        # defender1_home.line(((340, 130), (340, 200)), "red") #якорь
        # defender1_home.line(((380, 160), (290, 160)), "red")
        defender1_home.text((340, 160), lineups_home_number[1], anchor='ms', fill='white', font=font_number)
        defender1_home.text((340, 200), lineups_home[1], anchor='ms', fill='white', font=font_player)

        defender2_home = ImageDraw.Draw(background)
        # defender2_home.line(((340, 320), (340, 390)), "red") #якорь
        # defender2_home.line(((380, 360), (290, 360)), "red")
        defender2_home.text((340, 360), lineups_home_number[2], anchor='ms', fill='white', font=font_number)
        defender2_home.text((340, 400), lineups_home[2], anchor='ms', fill='white', font=font_player)

        defender3_home = ImageDraw.Draw(background)
        # defender3_home.line(((340, 550), (340, 620)), "red") #якорь
        # defender3_home.line(((380, 590), (290, 590)), "red")
        defender3_home.text((340, 590), lineups_home_number[3], anchor='ms', fill='white', font=font_number)
        defender3_home.text((340, 630), lineups_home[3], anchor='ms', fill='white', font=font_player)

        defender4_home = ImageDraw.Draw(background)
        # defender4_home.line(((340, 730), (340, 800)), "red") #якорь
        # defender4_home.line(((380, 770), (290, 770)), "red")
        defender4_home.text((340, 770), lineups_home_number[4], anchor='ms', fill='white', font=font_number)
        defender4_home.text((340, 810), lineups_home[4], anchor='ms', fill='white', font=font_player)

        midfielder1_home = ImageDraw.Draw(background)
        # midfielder1_home.line(((460, 220), (460, 300)), "red") #якорь
        # midfielder1_home.line(((500, 260), (410, 260)), "red")
        midfielder1_home.text((460, 260), lineups_home_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_home.text((460, 300), lineups_home[5], anchor='ms', fill='white', font=font_player)

        midfielder2_home = ImageDraw.Draw(background)
        # midfielder2_home.line(((460, 650), (460, 730)), "red") #якорь
        # midfielder2_home.line(((500, 680), (410, 680)), "red")
        midfielder2_home.text((460, 680), lineups_home_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_home.text((460, 720), lineups_home[6], anchor='ms', fill='white', font=font_player)

        midfielder3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((540, 130), (540, 200)), "red") #якорь
        # midfielder3_home.line(((600, 160), (510, 160)), "red")
        midfielder3_home.text((540, 160), lineups_home_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_home.text((540, 200), lineups_home[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_home = ImageDraw.Draw(background)
        # midfielder4_home.line(((520, 400), (520, 550)), "red") #якорь
        # midfielder4_home.line(((580, 470), (490, 470)), "red")
        midfielder4_home.text((520, 470), lineups_home_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_home.text((520, 510), lineups_home[8], anchor='ms', fill='white', font=font_player)
        #
        midfielder5_home = ImageDraw.Draw(background)
        # midfielder5_home.line(((540, 730), (540, 800)), "red") #якорь
        # midfielder5_home.line(((600, 770), (510, 770)), "red")
        midfielder5_home.text((540, 770), lineups_home_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_home.text((540, 810), lineups_home[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_home = ImageDraw.Draw(background)
        # midfielder4_home.line(((650, 400), (650, 550)), "red") #якорь
        # midfielder4_home.line(((700, 470), (610, 470)), "red")
        forward1_home.text((650, 470), lineups_home_number[10], anchor='ms', fill='white', font=font_number)
        forward1_home.text((650, 510), lineups_home[10], anchor='ms', fill='white', font=font_player)


        goalkeeper_away = ImageDraw.Draw(background)
        # goalkeeper_away.line(((1225, 420), (1225, 520)), "red") #якорь
        # goalkeeper_away.line(((1275, 470), (1175, 470)), "red")
        goalkeeper_away.text((1225, 470), lineups_away_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_away.text((1225, 510), lineups_away[0], anchor='ms', fill='white', font=font_player)

        defender1_away = ImageDraw.Draw(background)
        # defender1_away.line(((1100, 130), (1100, 200)), "red") #якорь
        # defender1_away.line(((1150, 160), (1050, 160)), "red")
        defender1_away.text((1100, 160), lineups_away_number[1], anchor='ms', fill='white', font=font_number)
        defender1_away.text((1100, 200), lineups_away[1], anchor='ms', fill='white', font=font_player)
        #
        defender2_away = ImageDraw.Draw(background)
        # defender2_away.line(((1100, 320), (1100, 390)), "red") #якорь
        # defender2_away.line(((1150, 360), (1050, 360)), "red")
        defender2_away.text((1100, 360), lineups_away_number[2], anchor='ms', fill='white', font=font_number)
        defender2_away.text((1100, 400), lineups_away[2], anchor='ms', fill='white', font=font_player)

        defender3_away = ImageDraw.Draw(background)
        # defender3_away.line(((1100, 550), (1100, 620)), "red") #якорь
        # defender3_away.line(((1150, 590), (1050, 590)), "red")
        defender3_away.text((1100, 590), lineups_away_number[3], anchor='ms', fill='white', font=font_number)
        defender3_away.text((1100, 630), lineups_away[3], anchor='ms', fill='white', font=font_player)

        defender4_away = ImageDraw.Draw(background)
        # defender4_away.line(((1100, 730), (1100, 800)), "red") #якорь
        # defender4_away.line(((1150, 770), (1050, 770)), "red")
        defender4_away.text((1100, 770), lineups_away_number[4], anchor='ms', fill='white', font=font_number)
        defender4_away.text((1100, 810), lineups_away[4], anchor='ms', fill='white', font=font_player)

        midfielder1_away = ImageDraw.Draw(background)
        # midfielder1_away.line(((990, 220), (990, 300)), "red") #якорь
        # midfielder1_away.line(((1050, 260), (950, 260)), "red")
        midfielder1_away.text((990, 260), lineups_away_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_away.text((990, 300), lineups_away[5], anchor='ms', fill='white', font=font_player)
        #
        midfielder2_away = ImageDraw.Draw(background)
        # midfielder2_away.line(((990, 650), (990, 730)), "red") #якорь
        # midfielder2_away.line(((1050, 680), (950, 680)), "red")
        midfielder2_away.text((990, 680), lineups_away_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_away.text((990, 720), lineups_away[6], anchor='ms', fill='white', font=font_player)
        #
        midfielder3_away = ImageDraw.Draw(background)
        # midfielder3_away.line(((910, 130), (910, 200)), "red") #якорь
        # midfielder3_away.line(((950, 160), (850, 160)), "red")
        midfielder3_away.text((910, 160), lineups_away_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_away.text((910, 200), lineups_away[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_away = ImageDraw.Draw(background)
        # midfielder4_away.line(((930, 400), (930, 550)), "red") #якорь
        # midfielder4_away.line(((950, 470), (850, 470)), "red")
        midfielder4_away.text((930, 470), lineups_away_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_away.text((930, 510), lineups_away[8], anchor='ms', fill='white', font=font_player)

        midfielder5_away = ImageDraw.Draw(background)
        # midfielder5_away.line(((910, 730), (910, 800)), "red") #якорь
        # midfielder5_away.line(((950, 770), (850, 770)), "red")
        midfielder5_away.text((910, 770), lineups_away_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_away.text((910, 810), lineups_away[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_away = ImageDraw.Draw(background)
        # forward1_away.line(((800, 400), (800, 550)), "red") #якорь
        # forward1_away.line(((840, 470), (740, 470)), "red")
        forward1_away.text((800, 470), lineups_away_number[10], anchor='ms', fill='white', font=font_number)
        forward1_away.text((800, 510), lineups_away[10], anchor='ms', fill='white', font=font_player)

    else:
        background = Image.open(root_folder / 'tools/img/ligue_11.png')
        background.paste(new_size_logo1, (20, 8),  mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (1350, 8),  mask=new_size_logo2.convert('RGBA'))


        goalkeeper_home = ImageDraw.Draw(background)
        # goalkeeper_home.line(((230, 400), (230, 550)), "red") #якорь
        # goalkeeper_home.line(((180, 470), (280, 470)), "red")
        goalkeeper_home.text((230, 470), lineups_home_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_home.text((230, 510), lineups_home[0], anchor='ms', fill='white', font=font_player)

        defender1_home = ImageDraw.Draw(background)
        # defender1_home.line(((340, 130), (340, 200)), "red") #якорь
        # defender1_home.line(((380, 160), (290, 160)), "red")
        defender1_home.text((340, 160), lineups_home_number[1], anchor='ms', fill='white', font=font_number)
        defender1_home.text((340, 200), lineups_home[1], anchor='ms', fill='white', font=font_player)

        defender2_home = ImageDraw.Draw(background)
        # defender2_home.line(((340, 320), (340, 390)), "red") #якорь
        # defender2_home.line(((380, 360), (290, 360)), "red")
        defender2_home.text((340, 360), lineups_home_number[2], anchor='ms', fill='white', font=font_number)
        defender2_home.text((340, 400), lineups_home[2], anchor='ms', fill='white', font=font_player)

        defender3_home = ImageDraw.Draw(background)
        # defender3_home.line(((340, 550), (340, 620)), "red") #якорь
        # defender3_home.line(((380, 590), (290, 590)), "red")
        defender3_home.text((340, 590), lineups_home_number[3], anchor='ms', fill='white', font=font_number)
        defender3_home.text((340, 630), lineups_home[3], anchor='ms', fill='white', font=font_player)

        defender4_home = ImageDraw.Draw(background)
        # defender4_home.line(((340, 730), (340, 800)), "red") #якорь
        # defender4_home.line(((380, 770), (290, 770)), "red")
        defender4_home.text((340, 770), lineups_home_number[4], anchor='ms', fill='white', font=font_number)
        defender4_home.text((340, 810), lineups_home[4], anchor='ms', fill='white', font=font_player)

        midfielder1_home = ImageDraw.Draw(background)
        # midfielder1_home.line(((460, 220), (460, 300)), "red") #якорь
        # midfielder1_home.line(((500, 260), (410, 260)), "red")
        midfielder1_home.text((460, 260), lineups_home_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_home.text((460, 300), lineups_home[5], anchor='ms', fill='white', font=font_player)

        midfielder2_home = ImageDraw.Draw(background)
        # midfielder2_home.line(((460, 450), (460, 530)), "red") #якорь
        # midfielder2_home.line(((500, 480), (410, 480)), "red")
        midfielder2_home.text((460, 480), lineups_home_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_home.text((460, 520), lineups_home[6], anchor='ms', fill='white', font=font_player)

        midfielder3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((460, 650), (460, 730)), "red") #якорь
        # midfielder3_home.line(((500, 680), (410, 680)), "red")
        midfielder3_home.text((460, 680), lineups_home_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_home.text((460, 720), lineups_home[7], anchor='ms', fill='white', font=font_player)

        forward1_home = ImageDraw.Draw(background)
        # forward1_home.line(((620, 220), (620, 300)), "red") #якорь
        # forward1_home.line(((660, 260), (570, 260)), "red")
        forward1_home.text((620, 260), lineups_home_number[8], anchor='ms', fill='white', font=font_number)
        forward1_home.text((620, 300), lineups_home[8], anchor='ms', fill='white', font=font_player)

        forward2_home = ImageDraw.Draw(background)
        # forward2_home.line(((620, 450), (620, 530)), "red") #якорь
        # forward2_home.line(((660, 480), (570, 480)), "red")
        forward2_home.text((620, 480), lineups_home_number[9], anchor='ms', fill='white', font=font_number)
        forward2_home.text((620, 520), lineups_home[9], anchor='ms', fill='white', font=font_player)

        forward3_home = ImageDraw.Draw(background)
        # midfielder3_home.line(((620, 650), (620, 730)), "red") #якорь
        # midfielder3_home.line(((660, 680), (570, 680)), "red")
        forward3_home.text((620, 680), lineups_home_number[10], anchor='ms', fill='white', font=font_number)
        forward3_home.text((620, 720), lineups_home[10], anchor='ms', fill='white', font=font_player)


        goalkeeper_away = ImageDraw.Draw(background)
        # goalkeeper_away.line(((1225, 420), (1225, 520)), "red") #якорь
        # goalkeeper_away.line(((1275, 470), (1175, 470)), "red")
        goalkeeper_away.text((1225, 470), lineups_away_number[0], anchor='ms', fill='white', font=font_number)
        goalkeeper_away.text((1225, 510), lineups_away[0], anchor='ms', fill='white', font=font_player)
        #
        defender1_away = ImageDraw.Draw(background)
        # defender1_away.line(((1100, 130), (1100, 200)), "red") #якорь
        # defender1_away.line(((1150, 160), (1050, 160)), "red")
        defender1_away.text((1100, 160), lineups_away_number[1], anchor='ms', fill='white', font=font_number)
        defender1_away.text((1100, 200), lineups_away[1], anchor='ms', fill='white', font=font_player)

        defender2_away = ImageDraw.Draw(background)
        # defender2_away.line(((1100, 320), (1100, 390)), "red") #якорь
        # defender2_away.line(((1150, 360), (1050, 360)), "red")
        defender2_away.text((1100, 360), lineups_away_number[2], anchor='ms', fill='white', font=font_number)
        defender2_away.text((1100, 400), lineups_away[2], anchor='ms', fill='white', font=font_player)

        defender3_away = ImageDraw.Draw(background)
        # defender3_away.line(((1100, 550), (1100, 620)), "red") #якорь
        # defender3_away.line(((1150, 590), (1050, 590)), "red")
        defender3_away.text((1100, 590), lineups_away_number[3], anchor='ms', fill='white', font=font_number)
        defender3_away.text((1100, 630), lineups_away[3], anchor='ms', fill='white', font=font_player)

        defender4_away = ImageDraw.Draw(background)
        # defender4_away.line(((1100, 730), (1100, 800)), "red") #якорь
        # defender4_away.line(((1150, 770), (1050, 770)), "red")
        defender4_away.text((1100, 770), lineups_away_number[4], anchor='ms', fill='white', font=font_number)
        defender4_away.text((1100, 810), lineups_away[4], anchor='ms', fill='white', font=font_player)

        midfielder1_away = ImageDraw.Draw(background)
        # midfielder1_away.line(((990, 220), (990, 300)), "red") #якорь
        # midfielder1_away.line(((1050, 260), (950, 260)), "red")
        midfielder1_away.text((990, 260), lineups_away_number[5], anchor='ms', fill='white', font=font_number)
        midfielder1_away.text((990, 300), lineups_away[5], anchor='ms', fill='white', font=font_player)
        #
        midfielder2_away = ImageDraw.Draw(background)
        # midfielder2_away.line(((990, 650), (990, 730)), "red") #якорь
        # midfielder2_away.line(((1050, 680), (950, 680)), "red")
        midfielder2_away.text((990, 680), lineups_away_number[6], anchor='ms', fill='white', font=font_number)
        midfielder2_away.text((990, 720), lineups_away[6], anchor='ms', fill='white', font=font_player)
        #
        midfielder3_away = ImageDraw.Draw(background)
        # midfielder3_away.line(((910, 130), (910, 200)), "red") #якорь
        # midfielder3_away.line(((950, 160), (850, 160)), "red")
        midfielder3_away.text((910, 160), lineups_away_number[7], anchor='ms', fill='white', font=font_number)
        midfielder3_away.text((910, 200), lineups_away[7], anchor='ms', fill='white', font=font_player)
        #
        midfielder4_away = ImageDraw.Draw(background)
        # midfielder4_away.line(((930, 400), (930, 550)), "red") #якорь
        # midfielder4_away.line(((950, 470), (850, 470)), "red")
        midfielder4_away.text((930, 470), lineups_away_number[8], anchor='ms', fill='white', font=font_number)
        midfielder4_away.text((930, 510), lineups_away[8], anchor='ms', fill='white', font=font_player)

        midfielder5_away = ImageDraw.Draw(background)
        # midfielder5_away.line(((910, 730), (910, 800)), "red") #якорь
        # midfielder5_away.line(((950, 770), (850, 770)), "red")
        midfielder5_away.text((910, 770), lineups_away_number[9], anchor='ms', fill='white', font=font_number)
        midfielder5_away.text((910, 810), lineups_away[9], anchor='ms', fill='white', font=font_player)
        #
        forward1_away = ImageDraw.Draw(background)
        # forward1_away.line(((800, 400), (800, 550)), "red") #якорь
        # forward1_away.line(((840, 470), (740, 470)), "red")
        forward1_away.text((800, 470), lineups_away_number[10], anchor='ms', fill='white', font=font_number)
        forward1_away.text((800, 510), lineups_away[10], anchor='ms', fill='white', font=font_player)

    # background.show()
    output_path = root_folder / f'result/img_match/{fixture_match}_lineups_review.png'
    background.save(output_path)


# start_img_review_lineups('881870')