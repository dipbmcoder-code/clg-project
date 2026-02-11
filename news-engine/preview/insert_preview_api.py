import os
import sys
from dataclasses import replace
from datetime import datetime
import math
import requests
from dotenv import load_dotenv
load_dotenv()
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from preview.db_preview import insert_db, get_request_db, check_match_for_insert, get_top_player, check_team, check_form_preview, check_form

#TODO МЫ СМОТРИМ БУДУЩИЕ МАТЧИ И МОЖЕТ БЫТЬ ОШИБКА, ЕСЛИ АПИ БУДЕТ ПУСТЫМ
def insert_preview_match_api(fixture_match):
    
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

    
    name_home_preview = data_gen['response'][0]['teams']['home']['name']
    name_away_preview = data_gen['response'][0]['teams']['away']['name']
    date_match = data_gen['response'][0]['fixture']['date'][:16]
    d = f"{date_match[:10]}"
    date_match2 = d.replace("-",'')
    venue = data_gen['response'][0]['fixture']['venue']['name']
    id_team_home_preview = data_gen['response'][0]['teams']['home']['id']
    id_team_away_preview = data_gen['response'][0]['teams']['away']['id']
    round = data_gen['response'][0]['league']['round']
    
    # if str(round).find("Regular Season - "):
    #     round = str(round).replace("Regular Season - ", "")
    # if str(round).find("Group Stage - "):
    #     round = str(round).replace("Group Stage - ", "")

    if "Regular Season - " in round: round = str(round).replace("Regular Season - ", "")
    elif "Group Stage - " in round: round = str(round).replace("Group Stage - ", "")
    elif 'Round of ' in round: round = str(round).replace("Round of ", "")
    elif '3rd Place Final' in round: round = str(round).replace("3rd Place Final", '1')

    round = int(round)
    # round = 1
    league = data_gen['response'][0]['league']['id']
    season = data_gen['response'][0]['league']['season']
    name_league = data_gen['response'][0]['league']['name']
    
    if name_league == "Premier League":
        name_league = "English" + " " + name_league

    if league == '1' or league == 1: teams = 'teams_cup'
    else: teams = 'teams'


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
    #Место team home
    rank_team_home = data_rank_home['response'][0]['league']['standings'][0][0]['rank']
    #Место team away
    rank_team_away = data_rank_away['response'][0]['league']['standings'][0][0]['rank']

    
   
    #SUM = суммирует, GROUP BY группирует строки, объединяет их, если нашло совпадение в значениях, ORDER BY сортирует строки по заданным настройкам (DESC по убыванию, ASK по возрастанию), AS (AliaS) S временно заменяет имена таблиц (только во время запроса)
    # Вывод максимального значения
    players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, topscorers_saves_home_name, topscorers_saves_home_amount = '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0
    if check_team(id_team_home_preview, league, season) == True:
        
        g = get_top_player('goals', id_team_home_preview, '1', league, season)
        if g != []:
            players_a_name = g[0]
            players_a_goals_total = g[1]
        else:
            players_a_name = ''
            players_a_goals_total = '0'

            
        assists = get_top_player('assists', id_team_home_preview, '1', league, season)
        if assists != []:
            topscorers_assists_home_name = assists[0]
            topscorers_assists_home_amount = assists[1]
        else:
            topscorers_assists_home_name = ''
            topscorers_assists_home_amount = '0'

        interceptions = get_top_player('interceptions', id_team_home_preview, '1', league, season)
        if interceptions != []:
            topscorers_interceptions_home_name = interceptions[0]
            topscorers_interceptions_home_amount = interceptions[1]
        else:
            topscorers_interceptions_home_name = ''
            topscorers_interceptions_home_amount = '0'

        duels = get_top_player('duels', id_team_home_preview, '1', league, season)
        if duels != []:
            topscorers_duels_home_name= duels[0]
            topscorers_duels_home_amount= duels[1]
        else:
            topscorers_duels_home_name= ''
            topscorers_duels_home_amount= '0'
        
        y_cards = get_top_player('y_cards', id_team_home_preview, '1', league, season)
        if y_cards != []:
            name_home_top_fouls_yel_card= y_cards[0]
            amount_home_fouls_yel_card = y_cards[1]
        else:
            name_home_top_fouls_yel_card= ''
            amount_home_fouls_yel_card = '0'

        r_cards = get_top_player('r_cards', id_team_home_preview, '1', league, season)
        if r_cards != []:
            name_home_top_fouls_red_card= r_cards[0]
            amount_home_fouls_red_card = r_cards[1]
        else:
            name_home_top_fouls_red_card= ''
            amount_home_fouls_red_card = '0'

        saves = get_top_player('saves', id_team_home_preview, '1', league, season)
        if saves != []:
            topscorers_saves_home_name = saves[0]
            topscorers_saves_home_amount = saves[1]
        else:
            topscorers_saves_home_name = ''
            topscorers_saves_home_amount = '0'

    elif check_team(id_team_away_preview, league, season) == False:
        players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, topscorers_saves_home_name, topscorers_saves_home_amount = '',0,'',0,'',0,'',0,'',0,'',0,'',0
    
    if check_team(id_team_away_preview, league, season) == True:
        goals = get_top_player('goals', id_team_away_preview, '1', league, season)
        if goals != []:
            players_b_name = goals[0]
            players_b_goals_total= goals[1]
        else:
            players_b_name = ''
            players_b_goals_total= '0'

        assists = get_top_player('assists', id_team_away_preview, '1',league, season)
        if assists != []:
            topscorers_assists_away_name = assists[0]
            topscorers_assists_away_amount = assists[1]
        else:
            topscorers_assists_away_name = ''
            topscorers_assists_away_amount = '0'

        interceptions = get_top_player('interceptions', id_team_away_preview, '1',league, season)
        if interceptions != []:
            topscorers_interceptions_away_name = interceptions[0]
            topscorers_interceptions_away_amount = interceptions[1]
        else:
            topscorers_interceptions_away_name = ''
            topscorers_interceptions_away_amount = '0'
        
        duels = get_top_player('duels', id_team_away_preview, '1',league, season)
        if duels != []:
            topscorers_duels_away_name = duels[0]
            topscorers_duels_away_amount = duels[1]
        else:
            topscorers_duels_away_name = ''
            topscorers_duels_away_amount = '0'
        
        fouls_y = get_top_player('y_cards', id_team_away_preview, '1',league, season)
        if fouls_y != []:
            name_away_top_fouls_yel_card = fouls_y[0]
            amount_away_fouls_yel_card = fouls_y[1]
        else:
            name_away_top_fouls_yel_card = ''
            amount_away_fouls_yel_card = '0'

        fouls_r = get_top_player('r_cards', id_team_away_preview, '1',league, season)
        if fouls_r != []:
            name_away_top_fouls_red_card = fouls_r[0]
            amount_away_fouls_red_card = fouls_r[1]
        else:
            name_away_top_fouls_red_card = ''
            amount_away_fouls_red_card = '0'
            
        saves = get_top_player('saves', id_team_away_preview, '1',league, season)
        if saves != []:
            topscorers_saves_away_name= saves[0]
            topscorers_saves_away_amount = saves[1]
        else:
            topscorers_saves_away_name= ''
            topscorers_saves_away_amount = '0'

    elif check_team(id_team_away_preview, league, season) == False:
        players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, topscorers_saves_away_name, topscorers_saves_away_amount = '',0,'',0,'',0,'',0,'',0,'',0,'',0

    
    # print(players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, topscorers_saves_home_name, topscorers_saves_home_amount)



    # #Top 3 scorer in league ----------------------------------------------------------------------------------------
    url = os.getenv('RAPID_API_BASE_URL')+"/players/topscorers"    #V3 - Top Scorers
    req_goal = requests.get(url=url, headers=headers, params={
        'league':league,
        'season':season
    })
    data_topscorers = req_goal.json()

    #Top 3 scorer in league ----------------------------------------------------------------------------------------
    topscorer_name_in_league_1 = data_topscorers['response'][0]['player']['name']
    topscorer_name_in_league_2 = data_topscorers['response'][1]['player']['name']
    topscorer_name_in_league_3 = data_topscorers['response'][2]['player']['name']
    topscorer_name_in_league_4 = data_topscorers['response'][3]['player']['name']
    topscorer_name_in_league_5 = data_topscorers['response'][4]['player']['name']
    

    topscorer_amount_in_league_1 = data_topscorers['response'][0]['statistics'][0]['goals']['total']
    topscorer_amount_in_league_2 = data_topscorers['response'][1]['statistics'][0]['goals']['total']
    topscorer_amount_in_league_3 = data_topscorers['response'][2]['statistics'][0]['goals']['total']
    topscorer_amount_in_league_4 = data_topscorers['response'][3]['statistics'][0]['goals']['total']
    topscorer_amount_in_league_5 = data_topscorers['response'][4]['statistics'][0]['goals']['total']

    topscorer_team_in_league_1 = data_topscorers['response'][0]['statistics'][0]['team']['name']
    topscorer_team_in_league_2 = data_topscorers['response'][1]['statistics'][0]['team']['name']
    topscorer_team_in_league_3 = data_topscorers['response'][2]['statistics'][0]['team']['name']
    topscorer_team_in_league_4 = data_topscorers['response'][3]['statistics'][0]['team']['name']
    topscorer_team_in_league_5 = data_topscorers['response'][4]['statistics'][0]['team']['name']

    if league != '1':
        insert_query = (
            f"SELECT max(goals) AS S , name, team_id FROM players_test WHERE league_id={league} AND goals != 0 AND season = {season} GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
        )
        teams = 'teams_test'
    elif league == '1':
        insert_query = (
            f"SELECT max(goals) AS S , name, team_id FROM players_cup WHERE league_id={league} AND goals != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
        )
        teams = 'teams_cup'
    # index_top_player_goals = check_form(insert_query)

    # topscorer_amount_in_league_1, topscorer_name_in_league_1, topscorer_amount_in_league_2, topscorer_name_in_league_2, topscorer_amount_in_league_3, topscorer_name_in_league_3, topscorer_amount_in_league_4, topscorer_name_in_league_4, topscorer_amount_in_league_5, topscorer_name_in_league_5 = 0, '', 0, '', 0, '', 0, '', 0, ''
    # topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, topscorer_team_in_league_4, topscorer_team_in_league_5 = '', '', '', '', ''

    # index = 0
    # for i in range(len(index_top_player_goals)):
    #     insert_query_for_teams = f"SELECT name FROM {teams} WHERE team_id_api=1111 AND season = {season};"

    #     index += 1
    #     goals = index_top_player_goals[i]
    #     goals_new = []
    #     for i in range(len(goals)):
    #         if "'" in str(goals[i]):
    #             goals_new.append(str(goals[i]).replace("'", ""))
    #         else:
    #             goals_new.append(goals[i])

    #     if goals_new != []: goals = goals_new
    #     if index == 1:
    #         topscorer_amount_in_league_1, topscorer_name_in_league_1, team_id_top_goals_league1 = goals[0], goals[1], \
    #                                                                                               goals[2]
    #         index_top_goals_team1 = check_form(insert_query_for_teams.replace("1111", f"{team_id_top_goals_league1}"))
    #         topscorer_team_in_league_1 = index_top_goals_team1[0][0]
    #         if "'" in topscorer_team_in_league_1: topscorer_team_in_league_1 = topscorer_team_in_league_1.replace("'",
    #                                                                                                               "")

    #     elif index == 2:
    #         topscorer_amount_in_league_2, topscorer_name_in_league_2, team_id_top_goals_league2 = goals[0], goals[1], \
    #                                                                                                   goals[2]
    #         index_top_goals_team2 = check_form(insert_query_for_teams.replace("1111", f"{team_id_top_goals_league2}"))
    #         print(index_top_goals_team2)
    #         if index_top_goals_team2 != []: topscorer_team_in_league_2 = index_top_goals_team2[0][0]
    #         if "'" in topscorer_team_in_league_2: topscorer_team_in_league_2 = topscorer_team_in_league_2.replace("'",
    #                                                                                                               "")

    #     elif index == 3:
    #         topscorer_amount_in_league_3, topscorer_name_in_league_3, team_id_top_goals_league3 = goals[0], goals[1], \
    #                                                                                               goals[2]
    #         index_top_goals_team3 = check_form(insert_query_for_teams.replace("1111", f"{team_id_top_goals_league3}"))
    #         topscorer_team_in_league_3 = index_top_goals_team3[0][0]
    #         if "'" in topscorer_team_in_league_3: topscorer_team_in_league_3 = topscorer_team_in_league_3.replace("'",
    #                                                                                                               "")

    #     elif index == 4:
    #         topscorer_amount_in_league_4, topscorer_name_in_league_4, team_id_top_goals_league4 = goals[0], goals[1], \
    #                                                                                               goals[2]
    #         index_top_goals_team4 = check_form(insert_query_for_teams.replace("1111", f"{team_id_top_goals_league4}"))
    #         topscorer_team_in_league_4 = index_top_goals_team4[0][0]
    #         if "'" in topscorer_team_in_league_4: topscorer_team_in_league_4 = topscorer_team_in_league_4.replace("'",
    #                                                                                                               "")

    #     elif index == 5:
    #         topscorer_amount_in_league_5, topscorer_name_in_league_5, team_id_top_goals_league5 = goals[0], goals[1], \
    #                                                                                               goals[2]
    #         index_top_goals_team5 = check_form(insert_query_for_teams.replace("1111", f"{team_id_top_goals_league5}"))
    #         topscorer_team_in_league_5 = index_top_goals_team5[0][0]
    #         if "'" in topscorer_team_in_league_5: topscorer_team_in_league_5 = topscorer_team_in_league_5.replace("'",
    #                                                                                                               "")

    # insert_query = (
    #     f"SELECT max(goals) AS S , name, team_id FROM players WHERE league_id={league} AND goals != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
    # )
    # index_top_player_goals = get_request_db(insert_query)
    
    # if index_top_player_goals != []:
    #     goals1 = index_top_player_goals[0]
    #     goals2 = index_top_player_goals[1]
    #     goals3 = index_top_player_goals[2]
    #     goals4 = index_top_player_goals[3]
    #     goals5 = index_top_player_goals[4]
    
    #     topscorer_amount_in_league_1, topscorer_name_in_league_1, team_id_top_goals_league1  = goals1[0], goals1[1], goals1[2]
    #     topscorer_amount_in_league_2, topscorer_name_in_league_2, team_id_top_goals_league2  = goals2[0], goals2[1], goals2[2]
    #     topscorer_amount_in_league_3, topscorer_name_in_league_3, team_id_top_goals_league3 = goals3[0], goals3[1], goals3[2]
    #     topscorer_amount_in_league_4, topscorer_name_in_league_4, team_id_top_goals_league4 = goals4[0], goals4[1], goals4[2]
    #     topscorer_amount_in_league_5, topscorer_name_in_league_5, team_id_top_goals_league5 = goals5[0], goals5[1], goals5[2]
    
    #     insert_query = (
    #     f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league1};"
    #     )
    #     index_top_goals_team1 = get_request_db(insert_query)
    #     index_top_goals_team1 = index_top_goals_team1[0]
    #     topscorer_team_in_league_1 = index_top_goals_team1[0]
    
    #     insert_query = (
    #         f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league2};"
    #     )
    #     index_top_goals_team2 = get_request_db(insert_query)
    #     index_top_goals_team2 = index_top_goals_team2[0]
    #     topscorer_team_in_league_2 = index_top_goals_team2[0]
    
    #     insert_query = (
    #         f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league3};"
    #     )
    #     index_top_goals_team3 = get_request_db(insert_query)
    #     index_top_goals_team3 = index_top_goals_team3[0]
    #     topscorer_team_in_league_3 = index_top_goals_team3[0]
    
    #     insert_query = (
    #         f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league4};"
    #     )
    #     index_top_goals_team4 = get_request_db(insert_query)
    #     index_top_goals_team4 = index_top_goals_team4[0]
    #     topscorer_team_in_league_4 = index_top_goals_team4[0]
    
    #     insert_query = (
    #         f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league5};"
    #     )
    #     index_top_goals_team5 = get_request_db(insert_query)
    #     index_top_goals_team5 = index_top_goals_team5[0]
    #     topscorer_team_in_league_5 = index_top_goals_team5[0]
    
    # else:
    #     topscorer_name_in_league_1 = topscorer_name_in_league_1
    #     topscorer_name_in_league_2 = topscorer_name_in_league_2
    #     topscorer_name_in_league_3 = topscorer_name_in_league_3
    #     topscorer_name_in_league_4 = topscorer_name_in_league_4
    #     topscorer_name_in_league_5 = topscorer_name_in_league_5
    
    #     topscorer_amount_in_league_1 = topscorer_amount_in_league_1
    #     topscorer_amount_in_league_2 = topscorer_amount_in_league_2
    #     topscorer_amount_in_league_3 = topscorer_amount_in_league_3
    #     topscorer_amount_in_league_4 = topscorer_amount_in_league_4
    #     topscorer_amount_in_league_5 = topscorer_amount_in_league_5
    
    #     topscorer_team_in_league_1 = topscorer_team_in_league_1
    #     topscorer_team_in_league_2 = topscorer_team_in_league_2
    #     topscorer_team_in_league_3 = topscorer_team_in_league_3
    #     topscorer_team_in_league_4 = topscorer_team_in_league_4
    #     topscorer_team_in_league_5 = topscorer_team_in_league_5

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
    insert_query_form = (
                f"SELECT form FROM {teams} WHERE team_id_api={id_team_home_preview} AND season = {season};"
            )
    g = check_form_preview(insert_query_form)
    if g != []:
        g = g[0]
        form_home = g[0]
    else:
        form_home = ''

    insert_query_form = (
                f"SELECT form FROM {teams} WHERE team_id_api={id_team_away_preview} AND season = {season};"
            )
    k = check_form_preview(insert_query_form)
    if k != []:
        k = k[0]
        form_away = k[0]
    else:
        form_away = ''
    
    
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
    home_win_once_in_home = data_home_stat['response']['fixtures']['wins']['home']
    home_lose_once_in_home = data_home_stat['response']['fixtures']['loses']['home']
    home_draws_once_in_home = data_home_stat['response']['fixtures']['draws']['home']


    #В текущем сезоне AWAY выигрывала на выезде, проигрывала и сыграла в ничью
    away_win_once_in_away = data_away_stat['response']['fixtures']['wins']['away']
    away_lose_once_in_away = data_away_stat['response']['fixtures']['loses']['away']
    away_draws_once_in_away = data_away_stat['response']['fixtures']['draws']['away']



    #Создаю список когда HOME забивали и на какой минуте, если значение None, список не пополняется
    list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
    list_minute_for_goals_home = []
    list_for_goal_home = []
    for minute_for_goal_home in range(8):
        if data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'] == None:
            list_minute_for_goals_home.append(list_minute[minute_for_goal_home])
            list_for_goal_home.append('0%')
        if data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'] != None:
            list_minute_for_goals_home.append(list_minute[minute_for_goal_home])
            list_for_goal_home.append(data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'])



    #Создаю список когда HOME пропускали голы и на какой минуте, если значение None, список не пополняется
    list_minute_missed_goals_home = []
    list_missed_goal_home = []
    for minute_for_missed_home in range(8):
        if data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'] == None:
            list_minute_missed_goals_home.append(list_minute[minute_for_missed_home])
            list_missed_goal_home.append('0%')
        if data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'] != None:
            list_minute_missed_goals_home.append(list_minute[minute_for_missed_home])
            list_missed_goal_home.append(data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'])



    # #TODO Списки не имеют 0% значения, поэтому вызываем по индексу
    #Создаю список когда AWAY забивали и на какой минуте, если значение None, список не пополняется
    list_minute_for_goals_away = []
    list_for_goal_away = []
    for minute_for_goal_away in range(8):
        if data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'] == None:
            list_minute_for_goals_away.append(list_minute[minute_for_goal_away])
            list_for_goal_away.append('0%')
        if data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'] != None:
            list_minute_for_goals_away.append(list_minute[minute_for_goal_away])
            list_for_goal_away.append(data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'])



    #Создаю список когда AWAY пропускали голы и на какой минуте, если значение None, список не пополняется
    list_minute_missed_goals_away = []
    list_missed_goal_away = []
    for minute_for_missed_away in range(8):
        if data_away_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_away]]['percentage'] == None:
            list_minute_missed_goals_away.append(list_minute[minute_for_missed_away])
            list_missed_goal_away.append('0%')
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
    if predictions_goals_home != None:
        predictions_goals_home = str(predictions_goals_home).replace("-", "")
        #predictions_goals_home = int(float(predictions_goals_home))
        predictions_goals_home = math.ceil(float(predictions_goals_home))
        #predictions_goals_home = round(float(predictions_goals_home)+ 0.1)
    elif predictions_goals_home == None:
        predictions_goals_home = 0

    if predictions_goals_away != None:
        predictions_goals_away = str(predictions_goals_away).replace("-", "")
        predictions_goals_away = math.ceil(float(predictions_goals_away))
        #predictions_goals_away = round(float(predictions_goals_away)+ 0.1)
    elif predictions_goals_away == None:
        predictions_goals_away = 0


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
        comparison_total_home = data_predictions['response'][0]['comparison']['total']['away']
        comparison_att_home = data_predictions['response'][0]['comparison']['att']['away']
        comparison_def_home = data_predictions['response'][0]['comparison']['def']['away']
        comparison_h2h_home = data_predictions['response'][0]['comparison']['h2h']['away']
        comparison_goals_home = data_predictions['response'][0]['comparison']['goals']['away']


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
        comparison_total_away = data_predictions['response'][0]['comparison']['total']['away']
        comparison_att_away = data_predictions['response'][0]['comparison']['att']['away']
        comparison_def_away = data_predictions['response'][0]['comparison']['def']['away']
        comparison_h2h_away = data_predictions['response'][0]['comparison']['h2h']['away']
        comparison_goals_away = data_predictions['response'][0]['comparison']['goals']['away']


    #BK
    url = os.getenv('RAPID_API_BASE_URL')+"/odds"            #V3 - Odds by fixture id
    req_bk = requests.request("GET", url, headers=headers, params={
        'fixture':f'{fixture_match}'
    })
    data_bk = req_bk.json()

    
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

    # print(bk_coef_name)
    # print(bk_coef_home)
    # print(bk_coef_draw)
    # print(bk_coef_away)
    


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

    if venue.find("'"):
        venue = venue.replace("'", " ")
    # if name_home_preview.find("'"):
    #     name_home_preview = name_home_preview.replace("'", " ")
    # if name_away_preview.find("'"):
    #     name_away_preview = name_away_preview.replace("'", " ")
    if name_league.find("'"):
        name_league = name_league.replace("'", " ")
    if players_a_name.find("'"):
        players_a_name = players_a_name.replace("'", " ")
    if players_b_name.find("'"):
        players_b_name = players_b_name.replace("'", " ")
    if topscorer_name_in_league_4.find("'"):
        topscorer_name_in_league_4 = topscorer_name_in_league_4.replace("'", "")
    if topscorer_name_in_league_5.find("'"):
        topscorer_name_in_league_5 = topscorer_name_in_league_5.replace("'", "")
    if topscorer_team_in_league_4.find("'"):
        topscorer_team_in_league_4 = topscorer_team_in_league_4.replace("'", "")
    if topscorer_team_in_league_5.find("'"):
        topscorer_team_in_league_5 = topscorer_team_in_league_5.replace("'", "")
    
    if topscorer_team_in_league_3.find("'"):
        topscorer_team_in_league_3 = topscorer_team_in_league_3.replace("'", " ")
    if topscorer_team_in_league_2.find("'"):
        topscorer_team_in_league_2 = topscorer_team_in_league_2.replace("'", " ")
    if topscorer_team_in_league_1.find("'"):
        topscorer_team_in_league_1 = topscorer_team_in_league_1.replace("'", " ")
    if topscorer_name_in_league_3.find("'"):
        topscorer_name_in_league_3 = topscorer_name_in_league_3.replace("'", " ")
    if topscorer_name_in_league_2.find("'"):
        topscorer_name_in_league_2 = topscorer_name_in_league_2.replace("'", " ")
    if topscorer_name_in_league_1.find("'"):
        topscorer_name_in_league_1 = topscorer_name_in_league_1.replace("'", " ")
    if topscorers_interceptions_away_name.find("'"):
        topscorers_interceptions_away_name = topscorers_interceptions_away_name.replace("'", " ")
    if topscorers_duels_away_name.find("'"):
        topscorers_duels_away_name = topscorers_duels_away_name.replace("'", " ")
    
    if topscorers_saves_away_name.find("'"):
        topscorers_saves_away_name = topscorers_saves_away_name.replace("'", " ")
    if topscorers_saves_home_name.find("'"):
        topscorers_saves_home_name = topscorers_saves_home_name.replace("'", " ")
    if topscorers_interceptions_home_name.find("'"):
        topscorers_interceptions_home_name = topscorers_interceptions_home_name.replace("'", " ")
    if topscorers_assists_home_name.find("'"):
        topscorers_assists_home_name = topscorers_assists_home_name.replace("'", " ")
    if topscorers_duels_home_name.find("'"):
        topscorers_duels_home_name = topscorers_duels_home_name.replace("'", " ")
    if name_home_top_fouls_yel_card.find("'"):
        name_home_top_fouls_yel_card = name_home_top_fouls_yel_card.replace("'", " ")
    if name_home_top_fouls_red_card.find("'"):
        name_home_top_fouls_red_card = name_home_top_fouls_red_card.replace("'", " ")
    if name_away_top_fouls_yel_card.find("'"):
        name_away_top_fouls_yel_card = name_away_top_fouls_yel_card.replace("'", " ")
    if name_away_top_fouls_red_card.find("'"):
        name_away_top_fouls_red_card = name_away_top_fouls_red_card.replace("'", " ")

    list_v = [fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview, league, season, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, result_list_minute,  result_list_minute_for_goals_home, result_list_for_goal_home, result_list_minute_missed_goals_home, result_list_missed_goal_home, result_list_minute_for_goals_away, result_list_for_goal_away, result_list_minute_missed_goals_away, result_list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, result_bk_coef_name, result_bk_coef_home, result_bk_coef_draw, result_bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, round]

    for index_replace in range(len(list_v)):
        if type(list_v[index_replace]) == str:
            if "'" in list_v[index_replace]:
                list_v[index_replace] = list_v[index_replace].replace("'", "")

    fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview, league, season, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, result_list_minute,  result_list_minute_for_goals_home, result_list_for_goal_home, result_list_minute_missed_goals_home, result_list_missed_goal_home, result_list_minute_for_goals_away, result_list_for_goal_away, result_list_minute_missed_goals_away, result_list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, result_bk_coef_name, result_bk_coef_home, result_bk_coef_draw, result_bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, round = list_v

    # Составление запроса
    insert_query = ( 
                    f" INSERT INTO match_preview (fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, round)"
                    f"VALUES ('{fixture_match}', '{name_home_preview}', '{name_away_preview}', '{date_match}', '{venue}', '{id_team_home_preview}',"
                    f"'{id_team_away_preview}', '{league}', '{season}', '{rank_team_home}', '{rank_team_away}',"
                    f"'{players_a_name}', '{players_a_goals_total}', '{players_b_name}', '{players_b_goals_total}',"
                    f"'{topscorers_assists_home_name}', '{topscorers_assists_home_amount}', '{topscorers_assists_away_name}', '{topscorers_assists_away_amount}',"
                    f"'{topscorers_interceptions_home_name}', '{topscorers_interceptions_home_amount}', '{topscorers_interceptions_away_name}', '{topscorers_interceptions_away_amount}',"
                    f"'{topscorers_duels_home_name}', '{topscorers_duels_home_amount}', '{topscorers_duels_away_name}', '{topscorers_duels_away_amount}',"
                    
                    f"'{topscorers_saves_home_name}', '{topscorers_saves_home_amount}', '{topscorers_saves_away_name}', '{topscorers_saves_away_amount}', '{fixture_match}', '{date_match2}',"
                    
                    f"'{topscorer_name_in_league_1}', '{topscorer_name_in_league_2}', '{topscorer_name_in_league_3}', '{topscorer_amount_in_league_1}',"
                    f"'{topscorer_amount_in_league_2}', '{topscorer_amount_in_league_3}', '{topscorer_team_in_league_1}', '{topscorer_team_in_league_2}',"
                    f"'{topscorer_team_in_league_3}', '{home_play_clean_sheet}',"
                    
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
                    f"'{comparison_h2h_home}', '{comparison_goals_home}', '{comparison_total_away}', '{comparison_att_away}', '{comparison_def_away}', '{comparison_h2h_away}', '{comparison_goals_away}', '{name_league}',"
                    f"'{topscorer_name_in_league_4}', '{topscorer_name_in_league_5}', '{topscorer_amount_in_league_4}', '{topscorer_amount_in_league_5}', '{topscorer_team_in_league_4}', '{topscorer_team_in_league_5}',"
                    f"'{name_home_top_fouls_yel_card}', '{amount_home_fouls_yel_card}', '{name_away_top_fouls_yel_card}', '{amount_away_fouls_yel_card}', '{name_home_top_fouls_red_card}', '{amount_home_fouls_red_card}', '{name_away_top_fouls_red_card}', '{amount_away_fouls_red_card}', '{round}')"
                    )
                
    # Запуск функции сохранения 
    insert_db(insert_query, 'match_preview')


# fixture_m = ['898687', '898689', '898693', '898685', '898691', '898686', '898688', '898690', '898692', '898684', '898683', '898679', '898682', '898678', '898681', '898677', '898680', '898676', '898667', '898674', '898672', '898670', '898673', '898675', '898669', '898671', '898668', '898665', '898663', '898661', '898666', '898664', '898658', '898662', '898659', '898660', '898649', '898655', '898657', '898650', '898653', '898652', '898651', '898654', '898656', '898644', '898645', '898642', '898647', '898641', '898640', '898646', '898643', '898648', '898630', '898632', '898635', '898633', '898639', '898638', '898634', '898637', '898636', '898631', '898623', '898624', '898627', '898622', '898626', '898628', '898625', '898629', '898619', '898621', '898616', '898613', '898614', '898618', '898615', '898620', '898617', '898607', '898611', '898606', '898609', '898610', '898612', '898608', '898604', '898605', '868074', '868073', '868066', '868075', '868072', '868069', '868067', '868070', '868068', '868071', '868061', '868060', '868065', '868064', '868057', '868063', '868058', '868056', '868062', '868059', '868051', '868046', '868049', '868052', '868053', '868054', '868055', '868048', '868050', '868047', '868044', '871271', '868041', '868037', '868045', '868040', '868038', '868039', '868043', '868042', '868036', '868031', '868030', '868033', '868035', '868028', '868026', '868029', '868032', '868034', '868027', '868019', '868020', '868021', '868017', '868024', '868022', '868018', '868025', '868023', '868016', '868010', '868008', '868015', '868007', '868013', '868011', '868012', '868014', '868006', '868009', '868001', '867998', '867996', '867999', '867997', '868003', '868004', '868005', '868002', '868000', '867990', '867994', '867991', '867986', '867995', '867987', '867989', '867993', '867992', '867988', '867983', '867985', '867977', '867976', '867979', '867978', '867980', '867982', '867981', '871262', '871596', '871260', '871259', '871261', '871258', '871256', '871255', '871254', '871257', '871245', '871247', '871248', '871246', '871251', '871249', '871250', '871253', '871252', '871243', '871244', '871240', '871236', '871238', '871237', '871241', '871242', '871239', '871234', '871233', '871235', '871232', '871231', '871230', '871229', '871228', '871227', '871224', '871223', '871221', '871219', '871226', '871225', '871220', '871218', '871222', '871211', '871212', '871216', '871215', '871213', '871214', '871210', '871209', '871217', '871203', '871207', '871204', '871206', '871205', '871208', '871202', '871201', '871200', '871199', '871194', '871191', '871192', '871195', '871197', '871198', '871196', '871193', '871188', '871186', '871184', '871183', '871182', '871187', '871189', '871190', '871185', '871173', '871177', '871180', '871181', '871179', '871178', '871175', '871174', '871176', '871167', '871172', '871165', '871170', '871169', '871168', '871171', '871166', '871164', '871583', '871585', '871589', '871582', '871587', '871588', '871581', '871586', '871584', '871580', '871574', '871571', '871577', '871579', '871570', '871573', '871578', '871575', '871572', '871576', '871562', '871568', '871567', '871564', '871561', '871560', '871563', '871569', '871566', '871565', '871556', '871552', '871559', '871558', '871551', '871550', '871554', '871555', '871557', '871553', '871546', '871542', '871548', '871547', '871545', '871541', '871549', '871543', '871544', '871540', '871531', '871538', '871530', '871532', '871533', '871539', '871537', '871534', '871535', '871536', '871483', '871525', '871529', '871528', '871527', '871522', '871520', '871524', '871523', '871526', '871521', '871519', '871518', '871516', '871515', '871512', '871510', '871511', '871514', '871517', '871513', '871505', '871508', '871509', '871507', '871504', '871502', '871503', '871506', '871501', '871500', '871493', '871498', '871494', '871492', '871499', '871491', '871497', '871496', '881888', '881882', '881886', '881880', '881881', '881889', '881883', '881885', '878059', '881887', '881884', '881875', '881877', '881872', '881876', '881878', '881874', '881873', '881870', '881879', '881871', '881862', '881865', '881861', '881869', '881866', '881864', '881868', '881860', '881863', '881867', '881852', '881854', '881850', '881859', '881858', '881856', '881855', '881851', '881853', '881857', '881843', '881845', '881844', '881842', '881841', '881849', '881848', '881847', '881840', '881846', '881832', '881834', '881835', '881831', '881836', '881839', '881830', '881838', '881833', '881837', '881829', '881828', '881827', '881826', '881825', '881824', '881823', '881822', '881821', '881820', '881819', '881818', '881817', '881816', '881814', '881813', '881815', '881812', '881811', '881810', '881808', '881809', '881807', '881806', '881804', '881805', '881803', '881802', '881801', '881800', '881799', '881798', '881797', '881796', '881795', '881794', '881793', '881792', '881791', '878042', '878045', '878051', '878044', '878046', '878047', '878043', '878048', '878050', '878049', '878033', '878041', '878036', '878034', '878040', '878038', '878039', '878032', '878037', '878035', '878030', '878031', '878025', '878026', '878023', '878022', '878024', '878027', '878029', '878028', '878014', '878013', '878018', '878016', '878021', '878015', '878020', '878012', '878019', '878017', '878009', '878010', '878005', '878008', '878004', '878007', '878006', '878002', '878003', '878011', '877993', '877995', '877999', '878000', '877997', '877992', '877996', '877994', '878001', '877998', '877987', '877983', '877984', '877989', '877991', '877982', '877990', '877985', '877986', '877988', '877980', '877978', '877977', '877972', '877973', '877975', '877974', '877976', '877981', '877979', '877969', '877968', '877966', '877962', '877965', '877967', '877971', '877964', '877963', '877970', '877959', '877961', '877957', '877953', '877952', '877954', '877958', '877960', '877956']
# l = ['867946', '867947',  '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '867963', '867964', '867965', '867966','867967','867968','867969','867970','867971','867972','867973','867974','867975','867976','867977','867978','867979','867980','867981','867982','867983','867984','867985', '877942','877943','877944','877945','877946','877947','877948','877949','877950','877951']
# l1 = ['881780', '881781', '881782', '881783', '881784','881785', '881786','881787','881788', '881789', '871470', '871471', '871472', '871473','871474','871475','871476','871477','871478','871479','871480','871481','871482','871484','871485','871486','871487','871488','871489','877942','877943','877944','877945','877946','877947','877948','877949','877950','877950','877951', '867947', '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '867963', '867964', '867965', '867966', '867967', '867968', '867969', '867970', '867971', '867972', '867973', '867974', '867975', '867984']
# l = l + l1

# for i in range(len(l)):
#     if l[i] not in fixture_m:
#         fixture_m.append(l[i])
# print(len(fixture_m))
# fixture_m.sort()

# l78 = ['871263', '871264', '871265', '871266', '871267', '871268', '871269', '871270', '871271']
# l140 = ['878052' , '878053', '878054', '878055', '878056', '878057', '878058', '878059', '878060', '878061']
# l61 = ['871590', '871591', '871592', '871593', '871594', '871595', '871596', '871597', '871598', '871599']
# l135 = ['881890', '881891', '881892', '881893', '881894','881895', '881896', '881897', '881898', '881899']
# fixture_m = ['868126', '868127', '868128', '868130', '868131', '868132', '868133', '868134', '868135']
# for i in range(len(fixture_m)):
# #
# host = 'localhost'
# user = 'db_user'
# password = 'baaI$SkBvZ~P'
# db_name = 'db_match'
# import psycopg2
# #     insert_preview_match_api(fixture_m[i])
# def get_data():
#     try:
#         connection = psycopg2.connect (
#             host= host,
#             user = user,
#             password = password,
#             database = db_name
#         )
#         with connection.cursor() as cursor:
#             insert_query = (
#                 f"SELECT fixture_match FROM match_review "
#             )
#             cursor.execute(insert_query)
#             result = cursor.fetchall()
#             list_f = []
#             if result != []:
#                 for i in range(len(result)):
#                     insert_preview_match_api(result[i][0])
#             return list_f
#
#             connection.commit()
#     except Exception as _ex:
#         print('[INFO] ERROR', _ex)
#     finally:
#         if connection:
#             connection.close()
# get_data()


def custom_insert():
    list_league = [772]
    season = "2023"

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }

    for league in list_league:

        url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"

        querystring = {"league": str(league), "season": str(season)}

        response = requests.get(url, headers=headers, params=querystring).json()

        for fixture in [response['response'][fixture_match]['fixture']['id'] for fixture_match in range(len(response['response'])) if response['response'][fixture_match]['fixture']['status']['long'] == "Match Finished"]:
            insert_preview_match_api(fixture)


# custom_insert()
