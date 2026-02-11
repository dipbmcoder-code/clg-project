from dataclasses import replace
from datetime import datetime
import requests
from preview.db_preview import insert_db
import os
from dotenv import load_dotenv
#TODO МЫ СМОТРИМ БУДУЩИЕ МАТЧИ И МОЖЕТ БЫТЬ ОШИБКА, ЕСЛИ АПИ БУДЕТ ПУСТЫМ


load_dotenv()

# Function to escape single quotes in strings
def escape_quotes(text):
    if text is None:
        return ''
    return str(text).replace("'", "''")

def insert_preview_match_api(fixture_match):
    # print(fixture_match)

    #Ищу будущие встречи команды №
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"        # V3 - Next {x} Fixtures to come
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_gen = requests.get(url, headers=headers, params={
        'id':f'{fixture_match}'
    })
    data_gen = req_gen.json()
    # print(data_gen)
    # exit()

    name_home_preview = data_gen['response'][0]['teams']['home']['name']
    name_away_preview = data_gen['response'][0]['teams']['away']['name']
    date_match = data_gen['response'][0]['fixture']['date'][:16]
    d = f"{date_match[:10]}"
    date_match2 = d.replace("-",'')
    #fix_id_match = data_gen['response'][0]['fixture']['id']
    venue = data_gen['response'][0]['fixture']['venue']['name']
    id_team_home_preview = data_gen['response'][0]['teams']['home']['id']
    id_team_away_preview = data_gen['response'][0]['teams']['away']['id']
    league = data_gen['response'][0]['league']['id']
    season = data_gen['response'][0]['league']['season']
    name_league = data_gen['response'][0]['league']['name']
    country = data_gen['response'][0]['league']['country']
    standings = data_gen['response'][0]['league']['standings']
    if name_league == "Premier League":
        name_league = country + " " + name_league
    



    #standings----------------------------------------------------------------------------------------
    #TODO добавил в параметры ид команды, в другом файле есть код через цикл
    #Места идут по группам
    #HOME
    url = os.getenv('RAPID_API_BASE_URL')+"/standings"   #V3 - Standings by league id
    req_rank_home = requests.get(url=url, headers=headers, params={
        'season':season,
        'league':league,
        'team':id_team_home_preview
    })
    data_rank_home = req_rank_home.json()

    #AWAY
    req_rank_away = requests.get(url=url, headers=headers, params={
        'season':season,
        'league':league,
        'team':id_team_away_preview
    })
    data_rank_away = req_rank_away.json()

    # Check if standings exist
    rank_team_home = ''
    rank_team_away = ''
    if standings:
        # Место team home
        if data_rank_home['response']:
            rank_team_home = data_rank_home['response'][0]['league']['standings'][0][0]['rank'] if data_rank_home['response'][0]['league']['standings'][0][0].get('rank') else ''
        # Место team away
        if data_rank_away['response']:
            rank_team_away = data_rank_away['response'][0]['league']['standings'][0][0]['rank'] if data_rank_away['response'][0]['league']['standings'][0][0].get('rank') else ''

    

    #TODO МЫ БЕРЕМ СТАТУ ЗА 1 ПОСЛЕДНЮЮ ИГРУ, СОХРАНЯЕМ В БД И В САМОЙ БД СУММИРУЕМ
    #Ищу id ласт игры команды HOME
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    req_fixture_last_game_home = requests.get(url, headers=headers, params={
        "league":league,
        "season":season,
        "team":id_team_home_preview,
        # "last":"50"
    })
    data_fixture_last_game_home = req_fixture_last_game_home.json()
    # print(data_fixture_last_game_home)
    # print(league)
    # print(season)
    # print(id_team_home_preview)
    #Ищу id ласт игры команды HOME
    req_fixture_last_game_away = requests.get(url, headers=headers, params={
        "league":league,
        "season":season,
        "team":id_team_away_preview,
        # "last":"50"
    })
    data_fixture_last_game_away = req_fixture_last_game_away.json()

    fixture_last_game_home = data_fixture_last_game_home['response'][0]['fixture']['id']
    fixture_last_game_away = data_fixture_last_game_away['response'][0]['fixture']['id']




    #Результативныe игроки в лиге 2ух играющих команд (Goals)
    # print(fixture_last_game_home)
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    req_topplayer_home = requests.get(url, headers=headers, params={
        "id":fixture_last_game_home
    })
    data_topplayer_home = req_topplayer_home.json()
    #---------------------------------------------------------------------
    req_topplayer_away = requests.get(url, headers=headers, params={
        "id":fixture_last_game_away
    })
    data_topplayer_away = req_topplayer_away.json()

    if data_topplayer_home['response'][0]['fixture']['status']['long'] != "Match Postponed":
        #HOME
        #Ищу лучшего по голам HOME
        players_a_name = ''
        players_a_goals_total = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_goal_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
                    if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] is not None and \
                    data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] > players_a_goals_total:
                        players_a_goals_total = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total']
                        players_a_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['player']['name']
            else:
                players_a_name = ''
                players_a_goals_total = 0

        elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_goal_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])): 
                    if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] is not None and \
                    data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] > players_a_goals_total:
                        players_a_goals_total = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total']
                        players_a_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['player']['name']
            else:
                players_a_name = ''
                players_a_goals_total = 0

        #AWAY
        #Ищу лучшего по голам AWAY
        players_b_name = ''
        players_b_goals_total = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_goal_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
                    if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] is not None and \
                    data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] > players_b_goals_total:
                        players_b_goals_total = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total']
                        players_b_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['player']['name']
            else:
                players_b_name = ''
                players_b_goals_total = 0

        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_goal_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
                    if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] is not None and \
                    data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] > players_b_goals_total:
                        players_b_goals_total = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total']
                        players_b_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['player']['name']
            else:
                players_b_name = ''
                players_b_goals_total = 0


        #Top 3 scorer in league ----------------------------------------------------------------------------------------
        url = os.getenv('RAPID_API_BASE_URL')+"/players/topscorers"    #V3 - Top Scorers
        req_goal = requests.get(url=url, headers=headers, params={
            'league':league,
            'season':season
        })
        data_topscorers = req_goal.json()
        # print(data_topscorers)

        #Top 3 scorer in league ----------------------------------------------------------------------------------------
        if data_topscorers['response']:
            topscorer_name_in_league_1 = data_topscorers['response'][0]['player']['name']
            topscorer_name_in_league_2 = data_topscorers['response'][1]['player']['name'] if len(data_topscorers['response']) > 1 else ''
            topscorer_name_in_league_3 = data_topscorers['response'][2]['player']['name'] if len(data_topscorers['response']) > 2 else ''
            topscorer_name_in_league_4 = data_topscorers['response'][3]['player']['name'] if len(data_topscorers['response']) > 3 else ''
            topscorer_name_in_league_5 = data_topscorers['response'][4]['player']['name'] if len(data_topscorers['response']) > 4 else ''

            topscorer_amount_in_league_1 = data_topscorers['response'][0]['statistics'][0]['goals']['total']
            topscorer_amount_in_league_2 = data_topscorers['response'][1]['statistics'][0]['goals']['total'] if len(data_topscorers['response']) > 1 else ''
            topscorer_amount_in_league_3 = data_topscorers['response'][2]['statistics'][0]['goals']['total'] if len(data_topscorers['response']) > 2 else ''
            topscorer_amount_in_league_4 = data_topscorers['response'][3]['statistics'][0]['goals']['total'] if len(data_topscorers['response']) > 3 else ''
            topscorer_amount_in_league_5 = data_topscorers['response'][4]['statistics'][0]['goals']['total'] if len(data_topscorers['response']) > 4 else ''

            topscorer_team_in_league_1 = data_topscorers['response'][0]['statistics'][0]['team']['name']
            topscorer_team_in_league_2 = data_topscorers['response'][1]['statistics'][0]['team']['name'] if len(data_topscorers['response']) > 1 else ''
            topscorer_team_in_league_3 = data_topscorers['response'][2]['statistics'][0]['team']['name'] if len(data_topscorers['response']) > 2 else ''
            topscorer_team_in_league_4 = data_topscorers['response'][3]['statistics'][0]['team']['name'] if len(data_topscorers['response']) > 3 else ''
            topscorer_team_in_league_5 = data_topscorers['response'][4]['statistics'][0]['team']['name'] if len(data_topscorers['response']) > 4 else ''
        else:
            topscorer_name_in_league_1 = ''
            topscorer_name_in_league_2 = ''
            topscorer_name_in_league_3 = ''
            topscorer_name_in_league_4 = ''
            topscorer_name_in_league_5 = ''

            topscorer_amount_in_league_1 = 0
            topscorer_amount_in_league_2 = 0
            topscorer_amount_in_league_3 = 0
            topscorer_amount_in_league_4 = 0
            topscorer_amount_in_league_5 = 0

            topscorer_team_in_league_1 = ''
            topscorer_team_in_league_2 = ''
            topscorer_team_in_league_3 = ''
            topscorer_team_in_league_4 = ''
            topscorer_team_in_league_5 = ''



        #Top assists
        #HOME
        #Ищу лучшего по ассистам HOME
        topscorers_assists_home_name = ''
        topscorers_assists_home_amount = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_assists_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
                    if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] != None and \
                    data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_home_amount:
                        topscorers_assists_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists']
                        topscorers_assists_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['player']['name']
            else:
                topscorers_assists_home_name = ''
                topscorers_assists_home_amount = 0

        elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_assists_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
                    if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] is not None and \
                    data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_home_amount:
                        topscorers_assists_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists']
                        topscorers_assists_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['player']['name']
            else:
                topscorers_assists_home_name = ''
                topscorers_assists_home_amount = 0



        #AWAY
        #Ищу лучшего по ассистам AWAY
        topscorers_assists_away_name = ''
        topscorers_assists_away_amount = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_assists_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
                    if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] is not None and \
                    data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_away_amount:
                        topscorers_assists_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists']
                        topscorers_assists_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['player']['name']
            else:
                topscorers_assists_away_name = ''
                topscorers_assists_away_amount = 0

        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_assists_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
                    if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] is not None and \
                    data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_away_amount:
                        topscorers_assists_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists']
                        topscorers_assists_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['player']['name']
            else:
                topscorers_assists_away_name = ''
                topscorers_assists_away_amount = 0





        #Find tackles (blocks)
        #HOME
        #Ищу лучшего по отборам HOME
        topscorers_blocks_home_name = ''
        topscorers_blocks_home_amount = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_blocks_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
                    if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] is not None and \
                    data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_home_amount:
                        topscorers_blocks_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks']
                        topscorers_blocks_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['player']['name']
            else:
                topscorers_blocks_home_name = ''
                topscorers_blocks_home_amount = 0

        if name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_blocks_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
                    if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] is not None and \
                    data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_home_amount:
                        topscorers_blocks_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks']
                        topscorers_blocks_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['player']['name']
            else:
                topscorers_blocks_home_name = ''
                topscorers_blocks_home_amount = 0



        #AWAY
        #Ищу лучшего по отборам AWAY
        topscorers_blocks_away_name = ''
        topscorers_blocks_away_amount = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:   
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_blocks_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
                    if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] is not None and \
                    data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_away_amount:
                        topscorers_blocks_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks']
                        topscorers_blocks_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['player']['name']
            else:
                topscorers_blocks_away_name = ''
                topscorers_blocks_away_amount = 0

        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_blocks_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
                    if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] is not None and \
                    data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_away_amount:
                        topscorers_blocks_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks']
                        topscorers_blocks_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['player']['name']
            else:
                topscorers_blocks_away_name = ''
                topscorers_blocks_away_amount = 0



        #Find duels
        #HOME
        #Ищу лучшего по duels HOME
        topscorers_duels_home_name = ''
        topscorers_duels_home_amount = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_duels_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
                    if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] is not None and \
                    data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_home_amount:
                        topscorers_duels_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won']
                        topscorers_duels_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['player']['name']
            else:
                topscorers_duels_home_name = ''
                topscorers_duels_home_amount = 0

        elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_duels_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
                    if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] is not None and \
                    data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_home_amount:
                        topscorers_duels_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won']
                        topscorers_duels_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['player']['name']
            else:
                topscorers_duels_home_name = ''
                topscorers_duels_home_amount = 0

        #AWAY
        #Ищу лучшего по duels AWAY
        topscorers_duels_away_name = ''
        topscorers_duels_away_amount = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_duels_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
                    if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] is not None and \
                    data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_away_amount:
                        topscorers_duels_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won']
                        topscorers_duels_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['player']['name']
            else:
                topscorers_duels_away_name = ''
                topscorers_duels_away_amount = 0


        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_duels_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
                    if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] is not None and \
                    data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_away_amount:
                        topscorers_duels_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won']
                        topscorers_duels_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['player']['name']
            else:
                topscorers_duels_away_name = ''
                topscorers_duels_away_amount = 0




        #Find fouls
        #HOME
        #Ищу лучшего по fouls HOME
        topscorers_fouls_home_name = ''
        topscorers_fouls_home_amount = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_fouls_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
                    if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] is not None and \
                    data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_home_amount:
                        topscorers_fouls_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed']
                        topscorers_fouls_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['name']
            else:
                topscorers_fouls_home_name = ''
                topscorers_fouls_home_amount = 0

        elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                for find_home_top_fouls_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
                    if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] is not None and \
                    data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_home_amount:
                        topscorers_fouls_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed']
                        topscorers_fouls_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['player']['name']
            else:
                topscorers_fouls_home_name = ''
                topscorers_fouls_home_amount = 0


        #AWAY
        #Ищу лучшего по fouls AWAY
        topscorers_fouls_away_name = ''
        topscorers_fouls_away_amount = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_fouls_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
                    if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] is not None and \
                    data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_away_amount:
                        topscorers_fouls_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed']
                        topscorers_fouls_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['player']['name']
            else:
                topscorers_fouls_away_name = ''
                topscorers_fouls_away_amount = 0

        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                for find_away_top_fouls_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
                    if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] is not None and \
                    data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_away_amount:
                        topscorers_fouls_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed']
                        topscorers_fouls_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['name']
            else:
                topscorers_fouls_away_name = ''
                topscorers_fouls_away_amount = 0




        #Top goals saves
        #HOME
        #Ищу лучшего по сейвам HOME
        # print("name_league")
        topscorers_saves_home_name = ''
        topscorers_saves_home_amount = 0
        if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
            if data_topplayer_home['response'][0]['players']:
                topscorers_saves_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][0]['statistics'][0]['goals']['saves']
                topscorers_saves_home_name = data_topplayer_home['response'][0]['players'][0]['players'][0]['player']['name']
                if topscorers_saves_home_amount is None:
                    topscorers_saves_home_amount = 0
            else:
                topscorers_saves_home_amount = 0
                topscorers_saves_home_name = ''


        elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
            if data_topplayer_home['response'][0]['players']:
                topscorers_saves_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][0]['statistics'][0]['goals']['saves']
                topscorers_saves_home_name = data_topplayer_home['response'][0]['players'][1]['players'][0]['player']['name']
                if topscorers_saves_home_amount is None:
                    topscorers_saves_home_amount = 0
            else:
                topscorers_saves_home_amount = 0
                topscorers_saves_home_name = ''


        #AWAY
        #Ищу лучшего по сейвам AWAY
        topscorers_saves_away_name = ''
        topscorers_saves_away_amount = 0
        if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
            if data_topplayer_away['response'][0]['players']:
                topscorers_saves_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][0]['statistics'][0]['goals']['saves']
                topscorers_saves_away_name = data_topplayer_away['response'][0]['players'][0]['players'][0]['player']['name']
                if topscorers_saves_away_amount is None:
                    topscorers_saves_away_amount = 0
            else:
                topscorers_saves_away_amount = 0
                topscorers_saves_away_name = ''

        elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
            if data_topplayer_away['response'][0]['players']:
                topscorers_saves_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][0]['statistics'][0]['goals']['saves']
                topscorers_saves_away_name = data_topplayer_away['response'][0]['players'][1]['players'][0]['player']['name']
                if topscorers_saves_away_amount is None:
                    topscorers_saves_away_amount = 0
            else:
                topscorers_saves_away_amount = 0
                topscorers_saves_away_name = ''


        # #TODO Убрать этот запрос (не нужен)
        # #Last 5 game
        # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"         #V3 - Last {x} Fixtures that were played
        # req_last_game_home = requests.get(url=url, headers=headers, params={
        #     'league':league,
        #     'season':season,
        #     'team':id_team_home_preview,   #Вставляю ид команды, выше есть переменные по обеим командам
        #     'last':'5'
        # })
        # data_last_game_home = req_last_game_home.json()
        # req_last_game_away = requests.get(url=url, headers=headers, params={
        #     'league':league,
        #     'season':season,
        #     'team':id_team_away_preview,   #Вставляю ид команды, выше есть переменные по обеим командам
        #     'last':'5'
        # })
        # data_last_game_away = req_last_game_away.json()


        # #TODO Важно счет последних игр будет в формате словаря
        # #Статистика за последние № игр команды HOME
        # home_last_games_who = []
        # home_last_games_rival = []
        # home_last_games_scores = []
        # for find_last_games_home in range(len(data_last_game_home['response'])):
        #     if data_last_game_home['response'][find_last_games_home]['teams']['home']['name'] == name_home_preview:
        #         home_last_games_who.append(data_last_game_home['response'][find_last_games_home]['teams']['home']['name'])
        #     else:
        #         home_last_games_who.append(data_last_game_home['response'][find_last_games_home]['teams']['away']['name'])

        #     if data_last_game_home['response'][find_last_games_home]['teams']['home']['name'] != name_home_preview:
        #         home_last_games_rival.append(data_last_game_home['response'][find_last_games_home]['teams']['home']['name'])
        #     else:
        #         home_last_games_rival.append(data_last_game_home['response'][find_last_games_home]['teams']['away']['name'])

        #     home_last_games_scores.append(data_last_game_home['response'][find_last_games_home]['goals'])


        # #Статистика за последние № игр команды AWAY
        # away_last_games_who = []
        # away_last_games_rival = []
        # away_last_games_scores = []
        # for find_last_games_away in range(len(data_last_game_away['response'])):
        #     if data_last_game_away['response'][find_last_games_away]['teams']['home']['name'] == name_away_preview:
        #         away_last_games_who.append(data_last_game_away['response'][find_last_games_away]['teams']['home']['name'])
        #     else:
        #         away_last_games_who.append(data_last_game_away['response'][find_last_games_away]['teams']['away']['name'])

        #     if data_last_game_away['response'][find_last_games_away]['teams']['home']['name'] != name_away_preview:
        #         away_last_games_rival.append(data_last_game_away['response'][find_last_games_away]['teams']['home']['name'])
        #     else:
        #         away_last_games_rival.append(data_last_game_away['response'][find_last_games_away]['teams']['away']['name'])

        #     away_last_games_scores.append(data_last_game_away['response'][find_last_games_away]['goals'])



        #TODO cчитаем игры в ноль, крупные победы, поражения только 1 команды, запрос идет к айди команды
        #Cчитаю сколько раз команда home играла в ничью, крупные поражения и победы
        url = os.getenv('RAPID_API_BASE_URL')+"/teams/statistics"            #V3 - Teams Statistics
        req_game_stat_home = requests.get(url, headers=headers, params={
            'league':league,
            'season':season,
            'team':id_team_home_preview
        })
        data_home_stat = req_game_stat_home.json()
        req_game_stat_away = requests.get(url, headers=headers, params={
            'league':league,
            'season':season,
            'team':id_team_away_preview
        })
        data_away_stat = req_game_stat_away.json()

        #HOME
        home_play_clean_sheet = data_home_stat['response']['clean_sheet']['total']       #на ноль сыграла
        home_biggest_win_in_home = data_home_stat['response']['biggest']['wins']['home']
        home_biggest_win_in_away = data_home_stat['response']['biggest']['wins']['away']
        home_biggest_lose_in_home = data_home_stat['response']['biggest']['loses']['home']
        home_biggest_lose_in_away = data_home_stat['response']['biggest']['loses']['away']

        

        #Если параметр равен null, то приравниваем к 0
        if home_biggest_win_in_home == None:
            home_biggest_win_in_home = 0
        if home_biggest_win_in_away == None:
            home_biggest_win_in_away = 0
        if home_biggest_lose_in_home == None:
            home_biggest_lose_in_home = 0
        if home_biggest_lose_in_away == None:
            home_biggest_lose_in_away = 0


        #Form game
        # print(data_home_stat['response'])
        form_home = data_home_stat['response']['form'][:5] if data_home_stat['response']['form'] is not None else ''
        form_away = data_away_stat['response']['form'][:5] if data_away_stat['response']['form'] is not None else ''


        #AWAY
        away_play_clean_sheet = data_away_stat['response']['clean_sheet']['total']        #на ноль сыграла
        away_biggest_win_in_home = data_away_stat['response']['biggest']['wins']['home']
        away_biggest_win_in_away = data_away_stat['response']['biggest']['wins']['away']
        away_biggest_lose_in_home = data_away_stat['response']['biggest']['loses']['home']
        away_biggest_lose_in_away = data_away_stat['response']['biggest']['loses']['away']


        #Если параметр равен null, то приравниваем к 0
        if away_biggest_win_in_home == None:
            away_biggest_win_in_home = 0
        if away_biggest_win_in_away == None:
            away_biggest_win_in_away = 0
        if away_biggest_lose_in_home == None:
            away_biggest_lose_in_home = 0
        if away_biggest_lose_in_away == None:
            away_biggest_lose_in_away = 0


        #В текущем сезоне HOME выигрывала дома, проигрывала и сыграла в ничью
        home_win_once_in_home = data_home_stat['response']['fixtures']['wins']['total']
        home_lose_once_in_home = data_home_stat['response']['fixtures']['loses']['total']
        home_draws_once_in_home = data_home_stat['response']['fixtures']['draws']['total']


        #В текущем сезоне AWAY выигрывала на выезде, проигрывала и сыграла в ничью
        away_win_once_in_away = data_away_stat['response']['fixtures']['wins']['total']
        away_lose_once_in_away = data_away_stat['response']['fixtures']['loses']['total']
        away_draws_once_in_away = data_away_stat['response']['fixtures']['draws']['total']



        #Создаю список когда HOME забивали и на какой минуте, если значение None, список не пополняется
        list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
        list_minute_for_goals_home = []
        list_for_goal_home = []
        for minute_for_goal_home in range(8):
            if data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'] != None:
                list_minute_for_goals_home.append(list_minute[minute_for_goal_home])
                list_for_goal_home.append(data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'])



        #Создаю список когда HOME пропускали голы и на какой минуте, если значение None, список не пополняется
        list_minute_missed_goals_home = []
        list_missed_goal_home = []
        for minute_for_missed_home in range(8):
            if data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'] != None:
                list_minute_missed_goals_home.append(list_minute[minute_for_missed_home])
                list_missed_goal_home.append(data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'])



        # #TODO Списки не имеют 0% значения, поэтому вызываем по индексу
        #Создаю список когда AWAY забивали и на какой минуте, если значение None, список не пополняется
        list_minute_for_goals_away = []
        list_for_goal_away = []
        for minute_for_goal_away in range(8):
            if data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'] != None:
                list_minute_for_goals_away.append(list_minute[minute_for_goal_away])
                list_for_goal_away.append(data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'])



        #Создаю список когда AWAY пропускали голы и на какой минуте, если значение None, список не пополняется
        list_minute_missed_goals_away = []
        list_missed_goal_away = []
        for minute_for_missed_away in range(8):
            if data_away_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_away]]['percentage'] != None:
                list_minute_missed_goals_away.append(list_minute[minute_for_missed_away])
                list_missed_goal_away.append(data_away_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_away]]['percentage'])



        # #TODO Списки не имеют 0% значения, поэтому вызываем по индексу

        #Predictions
        url = os.getenv('RAPID_API_BASE_URL')+"/predictions"            #V3 - Predictions
        req_predictions = requests.get(url, headers=headers, params={
            "fixture":f'{fixture_match}'
        })
        data_predictions = req_predictions.json()


        predictions_percent_home = data_predictions['response'][0]['predictions']['percent']['home']
        predictions_percent_away = data_predictions['response'][0]['predictions']['percent']['away']
        predictions_percent_draw = data_predictions['response'][0]['predictions']['percent']['draw']


        predictions_goals_home = data_predictions['response'][0]['predictions']['goals']['home']
        predictions_goals_away = data_predictions['response'][0]['predictions']['goals']['away']
        

        #Статистика личных встреч за последние 3 сезона
        #HOME
        h2h_home_total_games = 0
        h2h_home_total_wins_in_home = 0
        h2h_home_total_wins_in_away = 0
        h2h_home_total_draws_in_home = 0
        h2h_home_total_draws_in_away = 0
        h2h_home_total_loses_in_home = 0
        h2h_home_total_loses_in_away = 0
        for h2h_home in range(len(data_predictions['response'][0]['h2h'])):
            if data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['name'] == name_home_preview:
                if data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2021 or \
                data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2020 or \
                data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2019:
                    h2h_home_total_games += 1
                    if data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == True:
                        h2h_home_total_wins_in_home += 1
                    elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == False:
                        h2h_home_total_loses_in_home += 1
                    elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == None:
                        h2h_home_total_draws_in_home += 1


            elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['name'] == name_home_preview:
                if data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2021 or \
                data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2020 or \
                data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2019:
                    h2h_home_total_games += 1
                    if data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == True:
                        h2h_home_total_wins_in_away += 1
                    elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == False:
                        h2h_home_total_loses_in_away += 1
                    elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == None:
                        h2h_home_total_draws_in_away += 1


        #AWAY

        h2h_away_total_games = 0
        h2h_away_total_wins_home = 0
        h2h_away_total_wins_away = 0
        h2h_away_total_draws_in_home = 0
        h2h_away_total_draws_in_away = 0
        h2h_away_total_loses_in_home = 0
        h2h_away_total_loses_in_away = 0
        for h2h_away in range(len(data_predictions['response'][0]['h2h'])):
            if data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['name'] == name_away_preview:
                if data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2021 or \
                data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2020 or \
                data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2019:
                    h2h_away_total_games += 1
                    if data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == True:
                        h2h_away_total_wins_home += 1
                    elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == False:
                        h2h_away_total_loses_in_home += 1
                    elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == None:
                        h2h_away_total_draws_in_home += 1

            elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['name'] == name_away_preview:
                if data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2021 or \
                data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2020 or \
                data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2019:
                    h2h_away_total_games += 1
                    if data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == True:
                        h2h_away_total_wins_away += 1
                    elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == False:
                        h2h_away_total_loses_in_away += 1
                    elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == None:
                        h2h_away_total_draws_in_away += 1

        #Вероятностные характеристики команд перед матчем:
        comparison_total_home = ''
        comparison_att_home = ''
        comparison_def_home = ''
        comparison_h2h_home = ''
        comparison_goals_home = ''

        if data_predictions['response'][0]['teams']['home']['name'] == name_home_preview:
            comparison_total_home = data_predictions['response'][0]['comparison']['total']['home']
            comparison_att_home = data_predictions['response'][0]['comparison']['att']['home']
            comparison_def_home = data_predictions['response'][0]['comparison']['def']['home']
            comparison_h2h_home = data_predictions['response'][0]['comparison']['h2h']['home']
            comparison_goals_home = data_predictions['response'][0]['comparison']['goals']['home']
        elif data_predictions['response'][0]['teams']['away']['name'] == name_home_preview:
            comparison_total_home = data_predictions['response'][0]['comparison']['total']['home']
            comparison_att_home = data_predictions['response'][0]['comparison']['att']['home']
            comparison_def_home = data_predictions['response'][0]['comparison']['def']['home']
            comparison_h2h_home = data_predictions['response'][0]['comparison']['h2h']['home']
            comparison_goals_home = data_predictions['response'][0]['comparison']['goals']['home']


        comparison_total_away = ''
        comparison_att_away = ''
        comparison_def_away = ''
        comparison_h2h_away = ''
        comparison_goals_away = ''

        if data_predictions['response'][0]['teams']['home']['name'] == name_away_preview:
            comparison_total_away = data_predictions['response'][0]['comparison']['total']['home']
            comparison_att_away = data_predictions['response'][0]['comparison']['att']['home']
            comparison_def_away = data_predictions['response'][0]['comparison']['def']['home']
            comparison_h2h_away = data_predictions['response'][0]['comparison']['h2h']['home']
            comparison_goals_away = data_predictions['response'][0]['comparison']['goals']['home']
        elif data_predictions['response'][0]['teams']['away']['name'] == name_away_preview:
            comparison_total_away = data_predictions['response'][0]['comparison']['total']['home']
            comparison_att_away = data_predictions['response'][0]['comparison']['att']['home']
            comparison_def_away = data_predictions['response'][0]['comparison']['def']['home']
            comparison_h2h_away = data_predictions['response'][0]['comparison']['h2h']['home']
            comparison_goals_away = data_predictions['response'][0]['comparison']['goals']['home']




        #BK
        url = os.getenv('RAPID_API_BASE_URL')+"/odds"
        req_bk = requests.request("GET", url, headers=headers, params={
            'fixture':f'{fixture_match}'
        })
        data_bk = req_bk.json()
        # print('test data_bk:', data_bk)

        bk_coef_name = []
        bk_coef_home = []
        bk_coef_draw = []
        bk_coef_away = []
        if data_bk['response'] != []:
            for find_bk in range(len(data_bk['response'][0]['bookmakers'])):
                try:
                    bk_coef_name.append(data_bk['response'][0]['bookmakers'][find_bk]['name']) 
                    bk_coef_home.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][0]['odd'])
                    bk_coef_draw.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][1]['odd'])
                    bk_coef_away.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][2]['odd'])
                except Exception as IndexError:
                    try:
                        del bk_coef_name[find_bk], bk_coef_home[find_bk], bk_coef_draw[find_bk], bk_coef_away[find_bk]
                    except Exception as IndexError:
                        continue

        elif data_bk['response']:
            bk_coef_name = ['None']
            bk_coef_home = ['0']
            bk_coef_draw = ['0']
            bk_coef_away = ['0']
        # for find_bk in range(len(data_bk['response'][0]['bookmakers'])):           
        #     bk_coef_name.append(data_bk['response'][0]['bookmakers'][find_bk]['name']) 
        #     bk_coef_home.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][0]['odd'])
        #     bk_coef_draw.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][1]['odd'])
        #     bk_coef_away.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][2]['odd'])
        
        
        # result_home_last_games_who = ' '.join(home_last_games_who)
        # result_home_last_games_rival = ' '.join(home_last_games_rival)
        # list_home_last_games_scores = []
        # for dict1 in home_last_games_scores:
        #     if type(dict1) == type(str()):
        #         list_home_last_games_scores.append(dict1)
        #     elif type(dict1) == type(dict()):
        #         for key in dict1:
        #             list_home_last_games_scores += [key, str(dict1[key])]
        # result_home_last_games_scores = ' '.join(list_home_last_games_scores)

        # result_away_last_games_who = ' '.join(away_last_games_who)
        # result_away_last_games_rival = ' '.join(away_last_games_rival)
        # list_awa  y_last_games_scores = []
        # for dict2 in away_last_games_scores:
        #     if type(dict2) == type(str()):
        #         list_away_last_games_scores.append(dict2)
        #     elif type(dict2) == type(dict()):
        #         for key in dict2:
        #             list_away_last_games_scores += [key, str(dict2[key])]
        #result_away_last_games_scores = ' '.join(list_away_last_games_scores)

        result_list_minute = ' '.join(list_minute)
        result_list_minute_for_goals_home = ' '.join(list_minute_for_goals_home)
        result_list_for_goal_home = ' '.join(list_for_goal_home)
        result_list_minute_missed_goals_home = ' '.join(list_minute_missed_goals_home)
        result_list_missed_goal_home = ' '.join(list_missed_goal_home)
        result_list_minute_for_goals_away = ' '.join(list_minute_for_goals_away)
        result_list_for_goal_away = ' '.join(list_for_goal_away)
        result_list_minute_missed_goals_away = ' '.join(list_minute_missed_goals_away)
        result_list_missed_goal_away = ' '.join(list_missed_goal_away)
        result_bk_coef_name = ' '.join(bk_coef_name)
        result_bk_coef_home = ' '.join(bk_coef_home)
        result_bk_coef_draw = ' '.join(bk_coef_draw)
        result_bk_coef_away = ' '.join(bk_coef_away)

        #f" INSERT INTO match_preview (fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_home_name, topscorers_fouls_home_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_last_games_who, home_last_games_rival, home_last_games_scores, away_last_games_who, away_last_games_rival, away_last_games_scores, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away)"
        name_home_preview = escape_quotes(name_home_preview)
        name_away_preview = escape_quotes(name_away_preview) 
        venue = escape_quotes(venue)
        name_league = escape_quotes(name_league)
        players_a_name = escape_quotes(players_a_name)
        players_b_name = escape_quotes(players_b_name)
        topscorer_team_in_league_1 = escape_quotes(topscorer_team_in_league_1)
        topscorer_team_in_league_2 = escape_quotes(topscorer_team_in_league_2) 
        topscorer_team_in_league_3 = escape_quotes(topscorer_team_in_league_3)
        topscorer_team_in_league_4 = escape_quotes(topscorer_team_in_league_4)
        topscorer_team_in_league_5 = escape_quotes(topscorer_team_in_league_5)
        topscorer_name_in_league_1 = escape_quotes(topscorer_name_in_league_1)
        topscorer_name_in_league_2 = escape_quotes(topscorer_name_in_league_2)
        topscorer_name_in_league_3 = escape_quotes(topscorer_name_in_league_3) 
        topscorer_name_in_league_4 = escape_quotes(topscorer_name_in_league_4)
        topscorer_name_in_league_5 = escape_quotes(topscorer_name_in_league_5)
        topscorers_blocks_away_name = escape_quotes(topscorers_blocks_away_name)
        topscorers_duels_away_name = escape_quotes(topscorers_duels_away_name)
        topscorers_fouls_away_name = escape_quotes(topscorers_fouls_away_name)
        topscorers_saves_away_name = escape_quotes(topscorers_saves_away_name)
        topscorers_saves_home_name = escape_quotes(topscorers_saves_home_name)
        topscorers_blocks_home_name = escape_quotes(topscorers_blocks_home_name)
        topscorers_assists_home_name = escape_quotes(topscorers_assists_home_name)
        topscorers_duels_home_name = escape_quotes(topscorers_duels_home_name)
        topscorers_fouls_home_name = escape_quotes(topscorers_fouls_home_name)
        topscorers_assists_away_name = escape_quotes(topscorers_assists_away_name)

        # Составление запроса
        # print(name_home_preview)
        insert_query = (
                        
                        f" INSERT INTO match_preview (fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_home_name, topscorers_fouls_home_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3,topscorer_name_in_league_4,topscorer_name_in_league_5, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3,topscorer_amount_in_league_4,topscorer_amount_in_league_5, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3,topscorer_team_in_league_4,topscorer_team_in_league_5,home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league)"
                        f"VALUES ('{fixture_match}', '{name_home_preview}', '{name_away_preview}', '{date_match}', '{venue}', '{id_team_home_preview}',"
                        f"'{id_team_away_preview}', '{league}', '{season}', '{rank_team_home}', '{rank_team_away}', '{fixture_last_game_home}',"
                        f"'{fixture_last_game_away}', '{players_a_name}', '{players_a_goals_total}', '{players_b_name}', '{players_b_goals_total}',"
                        f"'{topscorers_assists_home_name}', '{topscorers_assists_home_amount}', '{topscorers_assists_away_name}', '{topscorers_assists_away_amount}',"
                        f"'{topscorers_blocks_home_name}', '{topscorers_blocks_home_amount}', '{topscorers_blocks_away_name}', '{topscorers_blocks_away_amount}',"
                        f"'{topscorers_duels_home_name}', '{topscorers_duels_home_amount}', '{topscorers_duels_away_name}', '{topscorers_duels_away_amount}',"
                        f"'{topscorers_fouls_home_name}', '{topscorers_fouls_home_amount}', '{topscorers_fouls_away_name}', '{topscorers_fouls_away_amount}',"
                        f"'{topscorers_saves_home_name}', '{topscorers_saves_home_amount}', '{topscorers_saves_away_name}', '{topscorers_saves_away_amount}', '{fixture_match}', '{date_match2}',"
                        
                        f"'{topscorer_name_in_league_1}', '{topscorer_name_in_league_2}', '{topscorer_name_in_league_3}','{topscorer_name_in_league_4}','{topscorer_name_in_league_5}', '{topscorer_amount_in_league_1}',"
                        f"'{topscorer_amount_in_league_2}', '{topscorer_amount_in_league_3}', '{topscorer_amount_in_league_4}', '{topscorer_amount_in_league_5}', '{topscorer_team_in_league_1}', '{topscorer_team_in_league_2}',"
                        f"'{topscorer_team_in_league_3}','{topscorer_team_in_league_4}','{topscorer_team_in_league_5}', '{home_play_clean_sheet}',"
                        
                        f"'{home_biggest_win_in_home}', '{home_biggest_win_in_away}', '{home_biggest_lose_in_home}', '{home_biggest_lose_in_away}',"
                        f"'{away_play_clean_sheet}', '{away_biggest_win_in_home}', '{away_biggest_win_in_away}', '{away_biggest_lose_in_home}',"
                        f"'{away_biggest_lose_in_away}', '{home_win_once_in_home}', '{home_lose_once_in_home}', '{home_draws_once_in_home}',"
                        
                        f"'{away_win_once_in_away}', '{away_lose_once_in_away}', '{away_draws_once_in_away}', '{result_list_minute}',"
                        f"'{result_list_minute_for_goals_home}', '{result_list_for_goal_home}', '{result_list_minute_missed_goals_home}', '{result_list_missed_goal_home}',"
                        f"'{result_list_minute_for_goals_away}', '{result_list_for_goal_away}', '{result_list_minute_missed_goals_away}', '{result_list_missed_goal_away}',"
                        f"'{predictions_percent_home}', '{predictions_percent_away}', '{predictions_percent_draw}', '{predictions_goals_home}', '{predictions_goals_away}', '{form_home}', '{form_away}', '{result_bk_coef_name}', '{result_bk_coef_home}', '{result_bk_coef_draw}', '{result_bk_coef_away}',"
                        f"'{h2h_home_total_games}', '{h2h_home_total_wins_in_home}', '{h2h_home_total_wins_in_away}', '{h2h_home_total_draws_in_home}', '{h2h_home_total_draws_in_away}',"
                        f"'{h2h_home_total_loses_in_home}', '{h2h_home_total_loses_in_away}', '{h2h_away_total_games}', '{h2h_away_total_wins_home}', '{h2h_away_total_wins_away}',"
                        f"'{h2h_away_total_draws_in_home}', '{h2h_away_total_draws_in_away}', '{h2h_away_total_loses_in_home}', '{h2h_away_total_loses_in_away}', '{comparison_total_home}', '{comparison_att_home}', '{comparison_def_home}',"
                        f"'{comparison_h2h_home}', '{comparison_goals_home}', '{comparison_total_away}', '{comparison_att_away}', '{comparison_def_away}', '{comparison_h2h_away}', '{comparison_goals_away}', '{name_league}')"
                        )
                    
        # Запуск функции сохранения 
        # print("name_league")

        insert_db(insert_query, 'match')

#'{h2h_away_total_wins}', '{h2h_away_total_draws}', '{h2h_away_total_loses}',
#h2h_home_total_games, h2h_home_total_wins, h2h_home_total_draws, h2h_home_total_loses, h2h_away_total_games, h2h_away_total_wins, h2h_away_total_draws, h2h_away_total_loses,     #f"'{h2h_home_total_games}', '{h2h_home_total_wins}', '{h2h_home_total_draws}', '{h2h_home_total_loses}', '{h2h_away_total_games}',"




def start_preview_graph(fixture_match):
    from PIL import Image
    from plotly import graph_objects as go
    from plotly.subplots import make_subplots
    from db_preview import get_data
    
    insert_query = (
        f"SELECT * FROM match_preview WHERE fixture_match3={fixture_match}"
    )

    r = get_data(insert_query)

    r = r[0]

    
    # Создание переменных по индексам результата    
    fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, fixture_match3, date_match2, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card = r[0], r[1], r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[21],r[22],r[23],r[24],r[25],r[26],r[27],r[28],r[29],r[30],r[31],r[32],r[33],r[34],r[35],r[36],r[37],r[38],r[39],r[40],r[41],r[42],r[43],r[44],r[45],r[46],r[47],r[48],r[49],r[50],r[51],r[52],r[53],r[54],r[55],r[56],r[57],r[58],r[59],r[60],r[61],r[62],r[63],r[64],r[65],r[66],r[67],r[68],r[69],r[70],r[71],r[72],r[73],r[74],r[75],r[76],r[77],r[78],r[79],r[80],r[81],r[82],r[83],r[84],r[85],r[86],r[87],r[88],r[89],r[90],r[91],r[92],r[93],r[94],r[95],r[96],r[97],r[98],r[99],r[100],r[101],r[102],r[103],r[104],r[105],r[106],r[107],r[108],r[109],r[110],r[111],r[112],r[113],r[114],r[115],r[116],r[117],r[118]
    # Восстановление списков
    list_for_goal_away=list_for_goal_away.split()
    list_for_goal_home=list_for_goal_home.split()
    list_minute_for_goals_home=list_minute_for_goals_home.split()
    list_minute_for_goals_away=list_minute_for_goals_away.split()
    list_minute_missed_goals_away=list_minute_missed_goals_away.split()
    list_minute_missed_goals_home=list_minute_missed_goals_home.split()
    list_missed_goal_away=list_missed_goal_away.split()
    list_missed_goal_home=list_missed_goal_home.split()


    percent_for_home = []
    minute_home_for = []
    percent_missed_home = []
    minute_home_missed = []

    for home_for in range(len(list_minute_for_goals_home)):
        percent_for_home.append(float(list_for_goal_home[home_for].replace("%", "")))
        minute_home_for.append(list_minute_for_goals_home[home_for] + ' ' + 'mins,' + ' ' + 'goals scored')


    for home_against in range(len(list_minute_missed_goals_home)):
        percent_missed_home.append(float(list_missed_goal_home[home_against].replace("%", "")))
        minute_home_missed.append(list_minute_missed_goals_home[home_against] + ' ' + 'mins,' + ' ' + 'goals conceded')


    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    fig.add_trace(go.Pie(labels=minute_home_for, values=percent_for_home, textinfo='label+percent'), 1, 1)
    fig.add_trace(go.Pie(labels=minute_home_missed, values=percent_missed_home, textinfo='label+percent'), 1, 2)
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(showlegend=False, font_size=21)

    fig.add_layout_image(                                         #Вставляю свою картинку в фон диаграммы
        dict(source=Image.open('/root/tools/img/gradient.png'),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            sizex=2,
            sizey=2,
            sizing="contain",
            xanchor="center",
            yanchor="middle",
            layer="below"))

    fig.write_image(f'/root/result/img_match/graph_home_{fixture_match}_preview.png', width=2100, height=1300)
    # image_plotly = Image.open('/root/result/img_match/graph_home.png')
    # image_plotly.save(f'/root/result/img_match/graph_home_{fixture_match}_preview.png')

    percent_for_away = []
    minute_away_for = []
    percent_missed_away = []
    minute_away_missed = []

    for away_for in range(len(list_minute_for_goals_away)):
        percent_for_away.append(float(list_for_goal_away[away_for].replace("%", "")))
        minute_away_for.append(list_minute_for_goals_away[away_for] + ' ' + 'mins,' + ' ' + 'goals scored')


    for away_against in range(len(list_minute_missed_goals_away)):
        percent_missed_away.append(float(list_missed_goal_away[away_against].replace("%", "")))
        minute_away_missed.append(list_minute_missed_goals_away[away_against] + ' ' + 'mins,' + ' ' + 'goals conceded')


    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    fig.add_trace(go.Pie(labels=minute_away_for, values=percent_for_away, textinfo='label+percent'), 1, 1)
    fig.add_trace(go.Pie(labels=minute_away_missed, values=percent_missed_away, textinfo='label+percent'), 1, 2)
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(showlegend=False, font_size=21)

    fig.add_layout_image(                                         #Вставляю свою картинку в фон диаграммы
        dict(source=Image.open('/root/tools/img/gradient.png'),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            sizex=2,
            sizey=2,
            sizing="contain",
            xanchor="center",
            yanchor="middle",
            layer="below"))

    fig.write_image(f'/root/result/img_match/graph_away_{fixture_match}_preview.png', width=2100, height=1300)
    # print('graph')

# start_preview_graph('868046')

