from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
import os
from dotenv import load_dotenv
load_dotenv()
def start_review_image(fixture_match):
    '''Создаю ревью картинку'''
    import requests
    from review.db import get_data
    from PIL import Image, ImageDraw, ImageFont
    from urllib.request import \
        urlopen  # Сохраняет лого по ссылке и вставляет в код #Добавил эту библиотеку, дольше выводить стало
    import datetime
    from time import sleep
    import os
    import json

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_logo = requests.get(url, headers=headers, params={
        'id': f'{fixture_match}'
    })
    data = req_logo.json()

    logo_team_home = data['response'][0]['teams']['home']['logo']
    logo_team_away = data['response'][0]['teams']['away']['logo']
    league_name = data['response'][0]['league']['name']
    venue = data['response'][0]['fixture']['venue']['name']
    date_match = data['response'][0]['fixture']['date']
    logo_leag = data['response'][0]['league']['logo']

    # Запрос в бд
    insert_query = (
        f"SELECT fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time FROM match_review WHERE fixture_match_for_check={fixture_match}"
    )

    index = get_data(insert_query)

    index = index[0]
    # fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away= index[0],index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],index[14],index[15],index[16],index[17],index[18],index[19],index[20],index[21],index[22],index[23],index[24],index[25],index[26],index[27],index[28],index[29],index[30],index[31],index[32],index[33],index[34],index[35],index[36],index[37],index[38],index[39],index[40],index[41],index[42],index[43],index[44],index[45],index[46],index[47],index[48],index[49],index[50],index[51],index[52],index[53],index[54],index[55],index[56],index[57],index[58],index[59],index[60],index[61],index[62],index[63],index[64],index[65],index[66],index[67],index[68],index[69],index[70],index[71],index[72]
    # fixture_match, name_home_review, name_away_review, lineups_home, lineups_away, gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card =  index[0],index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],index[14],index[15],index[16],index[17],index[18],index[19],index[20],index[21],index[22],index[23],index[24],index[25],index[26],index[27],index[28],index[29],index[30],index[31],index[32],index[33],index[34],index[35],index[36],index[37],index[38],index[39],index[40],index[41],index[42],index[43],index[44],index[45],index[46],index[47],index[48],index[49],index[50],index[51],index[52],index[53],index[54],index[55],index[56],index[57],index[58],index[59],index[60],index[61],index[62],index[63],index[64],index[65],index[66],index[67], index[68],index[69],index[70],index[71],index[72],index[73],index[74],index[75],index[76],index[77],index[78],index[79],index[80],index[81],index[82],index[83],index[84],index[85],index[86],index[87],index[88],index[89],index[90],index[91],index[92],index[93],index[94],index[95],index[96],index[97],index[98],index[99],index[100],index[101],index[102],index[103],index[104],index[105],index[106],index[107],index[108],index[109],index[110],index[111],index[112],index[113],index[114],index[115],index[116],index[117],index[118],index[119],index[120],index[121],index[122]
    fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time = index
    # goals_home, time_home_goal, player_home_goal, goals_away, time_away_goal, player_away_goal
    time_home_goal = time_home_goal.split()
    time_away_goal = time_away_goal.split()
    player_home_goal = str(player_home_goal).replace("+", " ")
    player_home_goal = player_home_goal.replace("_", "")
    player_away_goal = str(player_away_goal).replace("+", " ")
    player_away_goal = player_away_goal.replace("_", "")
    player_away_goal = player_away_goal.split()
    player_home_goal = player_home_goal.split()

    # Добавляю объекты
    font_path = root_folder / 'tools/fonts'
    font_for_name = ImageFont.truetype(str(font_path / 'BebasNeue-Regular.ttf'), size=70)
    font_for_league = ImageFont.truetype(str(font_path / 'BebasNeue-Regular.ttf'), size=120)
    font_for_arena = ImageFont.truetype(str(font_path / 'BebasNeue-Regular.ttf'), size=55)
    font_for_date = ImageFont.truetype(str(font_path / 'days2.ttf'), size=85)
    font_for_points = ImageFont.truetype(str(font_path / 'days2.ttf'), size=270)
    font_for_goal = ImageFont.truetype(str(font_path / 'BebasNeue-Regular.ttf'), size=50)

    logo_team1 = Image.open(urlopen(logo_team_home))
    logo_team2 = Image.open(urlopen(logo_team_away))

    league_logo_path = root_folder / 'tools/img'
    if league_name == "World Cup":
        league_logo = Image.open(league_logo_path / 'la_liga_logo.png')
    elif league_name == 'Ligue 1':
        league_logo = Image.open(league_logo_path / 'la_liga_logo.png')
    elif league_name == 'Primeira Liga':
        league_logo = Image.open(league_logo_path / 'la_liga_logo.png')
    elif league_name == 'La Liga':
        league_logo = Image.open(league_logo_path / 'la_liga_logo.png')
    else:
        league_logo = Image.open(urlopen(logo_leag))

    # background = Image.open('/opt/footballBot/tools/img/gradient.png')
    list_l = ['eng', 'ru']

    background = ''
    background_path = root_folder / 'tools/img'
    # print("league_name")
    # print(league_name)
    # print("league_name")
    if league_name == 'English Premier League':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'Bundesliga':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'Ligue 1':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'La Liga':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'Serie A':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'Primeira Liga':
        background = Image.open(background_path / 'EPL1.png')
    elif league_name == 'World Cup':
        background = Image.open(background_path / 'EPL1.png')
    else:
        background = Image.open(background_path / 'EPL1.png')

    for i in range(len(list_l)):


        # Статистика
        goals_home1 = ImageDraw.Draw(background)
        goals_home1.text((1700, 1570), str(goals_home), anchor='ms', font=font_for_points, fill='white')
        dash = ImageDraw.Draw(background)
        dash.text((2200, 1300), '-', font=font_for_points, fill='white')
        goals_away1 = ImageDraw.Draw(background)
        goals_away1.text((2800, 1570), str(goals_away), anchor='ms', font=font_for_points, fill='white')

        # # Кто забил и на какой минуте
        # #HomeTeam
        # index_home = 0
        # coordinate_home = 600
        # if len(player_home_goal) >= 1:
        #     while index_home != len(player_home_goal):
        #         home_goal_time = ImageDraw.Draw(background)
        #         home_goal_time.text((680, coordinate_home), f"({time_home_goal[index_home]}')  {player_home_goal[index_home]}", font=font_for_goal, fill='white')
        #         coordinate_home += 70
        #         index_home += 1
        # #AwayTeam
        # index_away = 0
        # coordinate_away = 650
        # if len(player_away_goal) >= 1:
        #     while index_away != len(player_away_goal):
        #         away_goal_time = ImageDraw.Draw(background)
        #         # away_goal_time.line(((2870, 800), (2870, 400)), "red") #якорь, метка откуда начинается текст
        #         # away_goal_time.line(((600, 650), (3100, 650)), "red")
        #         away_goal_time.text((2900, coordinate_away), f"({time_away_goal[index_away]}')  {player_away_goal[index_away]}", anchor='rs', font=font_for_goal, fill='white')
        #         coordinate_away += 70
        #         index_away += 1

        # #Ищем лучшего игрока в team_home
        # list_for_goals_home = []
        # list_for_goals_home_name_player = []
        # list_for_assists_home = []

        # goals_team_home = 0
        # assists_team_home = 0
        # best_player_goals_home = ''
        # index_mvp_home = 0

        # #Создаю списки с параметрами по голам и ассистам, потому что апи вытаскивает значение none вместо 0
        # for find_mvp_player_home in range(len(data['response'][0]['players'][0]['players'])):
        #     list_for_goals_home.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['statistics'][0]['goals']['total'])
        #     list_for_goals_home_name_player.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['player']['name'])
        #     if list_for_goals_home[find_mvp_player_home] == None:
        #         del list_for_goals_home[find_mvp_player_home]
        #         list_for_goals_home.insert(find_mvp_player_home, 0)
        #     list_for_assists_home.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['statistics'][0]['goals']['assists'])
        #     if list_for_assists_home[find_mvp_player_home] == None:
        #         del list_for_assists_home[find_mvp_player_home]
        #         list_for_assists_home.insert(find_mvp_player_home, 0)

        # #Прохожусь по спискам и ищу лучшего игрока
        # while index_mvp_home != len(list_for_goals_home):
        #     if list_for_goals_home[index_mvp_home] >= goals_team_home:
        #         best_player_goals_home = list_for_goals_home_name_player[index_mvp_home]
        #         goals_team_home = list_for_goals_home[index_mvp_home]
        #     if list_for_assists_home[index_mvp_home] >= assists_team_home:
        #         assists_team_home = list_for_assists_home[index_mvp_home]
        #     index_mvp_home += 1

        # #Ищем лучшего игрока в team_away
        # list_for_goals_away = []
        # list_for_goals_away_name_player = []
        # list_for_assists_away = []

        # goals_team_away = 0
        # assists_team_away = 0
        # best_player_goals_away = ''
        # index_mvp_away = 0

        # #Создаю списки с параметрами по голам и ассистам, потому что апи вытаскивает значение none вместо 0
        # for find_mvp_player_away in range(len(data['response'][0]['players'][1]['players'])):
        #     list_for_goals_away.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['statistics'][0]['goals']['total'])
        #     list_for_goals_away_name_player.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['player']['name'])
        #     if list_for_goals_away[find_mvp_player_away] == None:
        #         del list_for_goals_away[find_mvp_player_away]
        #         list_for_goals_away.insert(find_mvp_player_away, 0)
        #     list_for_assists_away.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['statistics'][0]['goals']['assists'])
        #     if list_for_assists_away[find_mvp_player_away] == None:
        #         del list_for_assists_away[find_mvp_player_away]
        #         list_for_assists_away.insert(find_mvp_player_away, 0)

        # #Прохожусь по спискам и ищу лучшего игрока
        # while index_mvp_away != len(list_for_goals_away):
        #     if list_for_goals_away[index_mvp_away] >= goals_team_away:
        #         best_player_goals_away = list_for_goals_away_name_player[index_mvp_away]
        #         goals_team_away = list_for_goals_away[index_mvp_away]
        #     if list_for_assists_away[index_mvp_away] >= assists_team_away:
        #         assists_team_away = list_for_assists_away[index_mvp_away]
        #     index_mvp_away += 1

        if list_l[i] == 'eng':
            # with open(f'/opt/footballBot/parameters/football/users/dicts/wc_teams.json') as file:
            #     teams_for_cup = json.load(file)
            # name_home_review = teams_for_cup[list_l[i]][name_home_review]
            # name_away_review = teams_for_cup[list_l[i]][name_away_review]
            # # Лига и названия команд
            # name_team = ImageDraw.Draw(background)
            # # name_team.line(((630, 600), (630, 200)), "red") #якорь, метка откуда начинается текст
            # # name_team.line(((500, 470), (900, 470)), "red")
            # if len(name_home_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
            #     mylist_home = []
            #     mylist_home_2 = []
            #     for i in name_home_review.split():
            #         if i == name_home_review.split()[0] or i == name_home_review.split()[1]:
            #             mylist_home.append(i)
            #         elif i == name_home_review.split()[2] or i == name_home_review.split()[3]:
            #             mylist_home_2.append(i)
            #     name_team.text((680, 470), ' '.join(mylist_home), anchor="ls", font=font_for_name, fill='white')
            #     name_team.text((680, 550), ' '.join(mylist_home_2), anchor="ls", font=font_for_name, fill='white')
            # else:
            #     name_team.text((680, 470), name_home_review, anchor="ls", font=font_for_name, fill='white')

            # print(league_name)
            # name_team.line(((2870, 600), (2870, 200)), "red") #якорь, метка откуда начинается текст
            # name_team.line(((2600, 470), (3100, 470)), "red")
            # if len(name_away_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
            #     mylist_away = []
            #     mylist_away_2 = []
            #     for i in name_away_review.split():
            #         if i == name_away_review.split()[0] or i == name_away_review.split()[1]:
            #             mylist_away.append(i)
            #         elif i == name_away_review.split()[2] or i == name_away_review.split()[3]:
            #             mylist_away_2.append(i)
            #     name_team.text((2900, 470), ' '.join(mylist_away), anchor="rs", font=font_for_name, fill='white')
            #     name_team.text((2900, 550), ' '.join(mylist_away_2), anchor="rs", font=font_for_name, fill='white')
            # else:
            #     name_team.text((2900, 470), name_away_review, anchor="rs", font=font_for_name)

            # league0 = ImageDraw.Draw(background)
            # # league0.line(((1750, 1400), (1750, 800)), "red") #якорь, метка откуда начинается текст
            # # league0.line(((1500, 1170), (2000, 1170)), "red")
            # league0.text((1800, 1170), league_name, anchor="ms", font=font_for_league, fill='#cbf705')

            # font_for_mvp = ImageFont.truetype('/opt/footballBot/tools/fonts/BebasNeue-Regular.ttf', size=85)

            # mvp_player = ''

            # if goals_team_home > goals_team_away and assists_team_home > assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away and assists_team_home < assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif goals_team_home > goals_team_away and assists_team_home >= assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away and assists_team_home <= assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif goals_team_home > goals_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif assists_team_home > assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif assists_team_home < assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif assists_team_home >= assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'

            # # elif goals_team_home >= goals_team_away and assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home <= goals_team_away and assists_team_home <= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home > goals_team_away and assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home < goals_team_away and assists_team_home <= assists_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif goals_team_home >= goals_team_away and assists_team_home > assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home <= goals_team_away and assists_team_home < assists_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif goals_team_home > goals_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home < goals_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif assists_team_home > assists_team_away or assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif assists_team_home < assists_team_away:
            # #     mvp_player = best_player_goals_away

            # mvp_player1 = ImageDraw.Draw(background)
            # # mvp_player.line(((1750, 2100), (1750, 1500)), "red") #якорь, метка откуда начинается текст
            # # mvp_player.line(((1500, 1800), (2000, 1800)), "red")
            # mvp_player1.text((1800, 1800), f'MVP: {mvp_player}', anchor="ms", font=font_for_mvp, fill='#cbf705')

            date = ImageDraw.Draw(background)
            # date.line(((1780, 400), (1780, 100)), "red") #якорь
            # date.line(((1500, 750), (2000, 750)), "red")
            x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
            # date.text((1750, 300), x.strftime('%A %B %d %Y'), anchor='ms', font=font_for_date, fill='black') # Полностью
            date.text((2200, 750), x.strftime('%B %d %Y'), anchor='ms', font=font_for_date, fill='white')  # Сокращенно

        elif list_l[i] == 'ru':
            with open(root_folder / 'parameters/football/users/dicts/wc_teams.json') as file:
                teams_for_cup = json.load(file)

            font_for_name = ImageFont.truetype(str(root_folder / 'tools/fonts/days2.ttf'), size=70)
            font_for_league = ImageFont.truetype(str(root_folder / 'tools/fonts/days2.ttf'), size=120)
            # font_for_date = ImageFont.truetype(str(root_folder / 'tools/fonts/days2.ttf'), size=85)
            font_for_mvp = ImageFont.truetype(str(root_folder / 'tools/fonts/days2.ttf'), size=85)

            if league_name == 'World Cup':
                name_home_review = teams_for_cup[list_l[i]][name_home_review]
                name_away_review = teams_for_cup[list_l[i]][name_away_review]

            if league_name == "English Premier League":
                league_name = "Английская премьер-лига"
            elif league_name == "Bundesliga":
                league_name = "Бундеслига"
            elif league_name == "Ligue 1":
                league_name = "Французкая Лига-1"
            elif league_name == "La Liga":
                league_name = "Ла Лига"
            elif league_name == "Serie A":
                league_name = "Сериа-А"
            elif league_name == "Primeira Liga":
                league_name = "Португальская премьер-лига"
            elif league_name == "World Cup":
                league_name = "Чемпионат мира"


            # Лига и названия команд
            # name_team = ImageDraw.Draw(background)
            # # name_team.line(((630, 600), (630, 200)), "red") #якорь, метка откуда начинается текст
            # # name_team.line(((500, 470), (900, 470)), "red")
            # if len(name_home_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
            #     mylist_home = []
            #     mylist_home_2 = []
            #     for i in name_home_review.split():
            #         if i == name_home_review.split()[0] or i == name_home_review.split()[1]:
            #             mylist_home.append(i)
            #         elif i == name_home_review.split()[2] or i == name_home_review.split()[3]:
            #             mylist_home_2.append(i)
            #     name_team.text((680, 470), ' '.join(mylist_home), anchor="ls", font=font_for_name, fill='white')
            #     name_team.text((680, 550), ' '.join(mylist_home_2), anchor="ls", font=font_for_name, fill='white')
            # else:
            #     name_team.text((680, 470), name_home_review, anchor="ls", font=font_for_name, fill='white')

            # #print(league_name)
            # # name_team.line(((2870, 600), (2870, 200)), "red") #якорь, метка откуда начинается текст
            # # name_team.line(((2600, 470), (3100, 470)), "red")
            # if len(name_away_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
            #     mylist_away = []
            #     mylist_away_2 = []
            #     for i in name_away_review.split():
            #         if i == name_away_review.split()[0] or i == name_away_review.split()[1]:
            #             mylist_away.append(i)
            #         elif i == name_away_review.split()[2] or i == name_away_review.split()[3]:
            #             mylist_away_2.append(i)
            #     name_team.text((2900, 470), ' '.join(mylist_away), anchor="rs", font=font_for_name, fill='white')
            #     name_team.text((2900, 550), ' '.join(mylist_away_2), anchor="rs", font=font_for_name, fill='white')
            # else:
            #     name_team.text((2900, 470), name_away_review, anchor="rs", font=font_for_name)

            # league0 = ImageDraw.Draw(background)
            # # league0.line(((1750, 1400), (1750, 800)), "red") #якорь, метка откуда начинается текст
            # # league0.line(((1500, 1170), (2000, 1170)), "red")
            # league0.text((1800, 1170), league_name, anchor="ms", font=font_for_league, fill='#cbf705')

            # mvp_player = ''

            # if goals_team_home > goals_team_away and assists_team_home > assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away and assists_team_home < assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif goals_team_home > goals_team_away and assists_team_home >= assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away and assists_team_home <= assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif goals_team_home > goals_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif goals_team_home < goals_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif assists_team_home > assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'
            # elif assists_team_home < assists_team_away:
            #     mvp_player = best_player_goals_away + ' (' + name_away_review + ')'
            # elif assists_team_home >= assists_team_away:
            #     mvp_player = best_player_goals_home + ' (' + name_home_review + ')'

            # # elif goals_team_home >= goals_team_away and assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home <= goals_team_away and assists_team_home <= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home > goals_team_away and assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home < goals_team_away and assists_team_home <= assists_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif goals_team_home >= goals_team_away and assists_team_home > assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home <= goals_team_away and assists_team_home < assists_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif goals_team_home > goals_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif goals_team_home < goals_team_away:
            # #     mvp_player = best_player_goals_away
            # # elif assists_team_home > assists_team_away or assists_team_home >= assists_team_away:
            # #     mvp_player = best_player_goals_home
            # # elif assists_team_home < assists_team_away:
            # #     mvp_player = best_player_goals_away

            # mvp_player1 = ImageDraw.Draw(background)
            # # mvp_player.line(((1750, 2100), (1750, 1500)), "red") #якорь, метка откуда начинается текст
            # # mvp_player.line(((1500, 1800), (2000, 1800)), "red")
            # mvp_player1.text((1800, 1800), f'MVP: {mvp_player}', anchor="ms", font=font_for_mvp, fill='#cbf705')

            # #x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))

            with open(root_folder / 'parameters/football/users/dicts/months_for_users.json') as file:
                month_json = json.load(file)

            month = month_json[list_l[i]][date_match[5:7]]
            day = date_match[8:10]
            year = date_match[0:4]
            date_ru = day + ' ' + month + ' ' + year
            # print(date_ru)
            date = ImageDraw.Draw(background)
            # date.line(((1780, 400), (1780, 100)), "red") #якорь
            # date.line(((1500, 750), (2000, 750)), "red")
            # date.text((1750, 300), x.strftime('%A %B %d %Y'), anchor='ms', font=font_for_date, fill='black') # Полностью
            date.text((1780, 750), date_ru, anchor='ms', font=font_for_date, fill='white')  # Сокращенно

        # if league_name == "Ligue 1" or league_name == "English Premier League" or league_name == "La Liga":
        #     venue0 = ImageDraw.Draw(background) #arena
        #     # league0.line(((1750, 2000), (1750, 1400)), "red") #якорь, метка откуда начинается текст
        #     # league0.line(((1500, 1700), (2000, 1700)), "red")
        #     venue0.text((1800, 1700), f'Arena: {venue}', anchor="ms", font=font_for_arena, fill='white')
        # else:
        #     venue0 = ImageDraw.Draw(background) #arena
        #     # league0.line(((1750, 2000), (1750, 1400)), "red") #якорь, метка откуда начинается текст
        #     # league0.line(((1500, 1700), (2000, 1700)), "red")
        #     venue0.text((1800, 1700), f'Arena: {venue}', anchor="ms", font=font_for_arena, fill='black')

        # # #Вывожу конкретную дату
        # date = ImageDraw.Draw(background)
        # # date.line(((1750, 400), (1750, 100)), "red") #якорь
        # # date.line(((1500, 300), (2000, 300)), "red")
        # x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
        # # date.text((1750, 300), x.strftime('%A %B %d %Y'), anchor='ms', font=font_for_date, fill='black') # Полностью
        # date.text((1750, 300), x.strftime('%b %d %Y'), anchor='ms', font=font_for_date, fill='black') # Сокращенно

        # Меняю размер logo
        new_size_logo1 = logo_team1.resize((400, 400))
        new_size_logo2 = logo_team2.resize((400, 400))
        new_size_logo_league = league_logo.resize((500, 500))
        # # league0.line(((1750, 1400), (1750, 800)), "red") #якорь, метка откуда начинается текст
        # # league0.line(((1500, 1170), (2000, 1170)), "red")

        background.paste(new_size_logo1, (1500, 900), mask=new_size_logo1.convert('RGBA'))
        background.paste(new_size_logo2, (2600, 900), mask=new_size_logo2.convert('RGBA'))
        background.paste(new_size_logo_league, (1950, 150), mask=new_size_logo_league.convert('RGBA'))
        # Вывод
        # width, height = background.size
        # print(width, height)
        new_image = background.resize((1778, 1000))
        output_path = root_folder / f'result/img_match/{list_l[i]}_{fixture_match}_review.png'
        # print("output_path")
        # print(output_path)
        # print("output_path")
        new_image.save(output_path)
        # background.save(f'/opt/footballBot/result/img_match/{fixture_match}_review.png')
        sleep(2)

# start_review_image('1208745')
def start_gemini_review_image(fixture_match, website=None):
    import requests
    from review.db import get_data
    import datetime
    import json
    from publication.utils import generate_gemini_image, replace_vars

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_logo = requests.get(url, headers=headers, params={
        'id': f'{fixture_match}'
    })
    data = req_logo.json()

    league_name = data['response'][0]['league']['name']
    venue = data['response'][0]['fixture']['venue']['name']
    date_match = data['response'][0]['fixture']['date']

    # Запрос в бд
    insert_query = (
        f"SELECT fixture_match, name_home_review, name_away_review, goals_home, goals_away,time_home_goal, player_home_goal, time_away_goal, player_away_goal FROM match_review WHERE fixture_match_for_check={fixture_match}"
    )

    index = get_data(insert_query)[0]

    fixture_match, name_home_review, name_away_review, goals_home, goals_away,time_home_goal, player_home_goal, time_away_goal, player_away_goal = index


    time_home_goal = time_home_goal.split()
    time_away_goal = time_away_goal.split()
    player_home_goal = str(player_home_goal).replace("+", " ")
    player_home_goal = player_home_goal.replace("_", "")
    player_away_goal = str(player_away_goal).replace("+", " ")
    player_away_goal = player_away_goal.replace("_", "")
    player_away_goal = player_away_goal.split()
    player_home_goal = player_home_goal.split()

    # Format date for prompt
    x = datetime.datetime(int(date_match[:4]), int(date_match[5:7]), int(date_match[8:10]))
    x = x.strftime('%B %d %Y')

    # Gemini API setup

    for lang in ['eng']:
        if lang == 'ru':
            with open(root_folder / 'parameters/football/users/dicts/wc_teams.json') as file:
                teams_for_cup = json.load(file)

            if league_name == 'World Cup':
                name_home_review = teams_for_cup[lang][name_home_review]
                name_away_review = teams_for_cup[lang][name_away_review]

            if league_name == "English Premier League":
                league_name = "Английская премьер-лига"
            elif league_name == "Bundesliga":
                league_name = "Бундеслига"
            elif league_name == "Ligue 1":
                league_name = "Французкая Лига-1"
            elif league_name == "La Liga":
                league_name = "Ла Лига"
            elif league_name == "Serie A":
                league_name = "Сериа-А"
            elif league_name == "Primeira Liga":
                league_name = "Португальская премьер-лига"
            elif league_name == "World Cup":
                league_name = "Чемпионат мира"

            with open(root_folder / 'parameters/football/users/dicts/months_for_users.json') as file:
                month_json = json.load(file)

            month = month_json[lang][date_match[5:7]]
            day = date_match[8:10]
            year = date_match[0:4]
            x = day + ' ' + month + ' ' + year

        # Check for custom prompt
        custom_prompt = website.get('data', {}).get('review_news_image_prompt') if website else None
        
        if custom_prompt:
            prompt_vars = {
                "team1": name_home_review,
                "team2": name_away_review,
                "goals_a": goals_home,
                "goals_b": goals_away,
                "league_name1": league_name,
                "review_match_date": x,
                "venue": venue or "Stadium",
                "league_name": league_name, # alias
                "home_team": name_home_review,
                "away_team": name_away_review,
                "goals_home": goals_home,
                "goals_away": goals_away,
                "match_date": x
            }
            prompt_text = replace_vars(custom_prompt, prompt_vars)
            prompt = f"Generate a football match review image with the following details:\n{prompt_text}"
        else:
            # Compose structured prompt
            prompt = {
                "league_name": league_name,
                "home_team": {
                    "name": name_home_review,
                    "goals": goals_home
                },
                "away_team": {
                    "name": name_away_review,
                    "goals": goals_away
                },
                "venue": venue,
                "match_date": x,
                "design": "modern, clean, professional sports news review graphic, bold typography, authentic sports media style, automatically fetch and display the official league logo in the top-left corner, and fetch team small logos to display beside team names and scores in small without extra labels. Logo's Positioned tastefully anywhere on the graphic without blocking players. Make sure the real action photo of players from this match remains clearly visible and not covered by overlays. Do not use abstract, gradient, digital art, or poster-style backgrounds",
                "size": "1024x1024"
            }

            prompt = f"Generate a football match review image with the following details:\n{prompt}"

        generate_gemini_image(prompt, fixture_match, lang, 'review')