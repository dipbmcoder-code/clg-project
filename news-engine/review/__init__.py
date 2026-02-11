# from dataclasses import replace
# from datetime import datetime
# import math
# import requests
# from db_preview import insert_db
#
# #TODO МЫ СМОТРИМ БУДУЩИЕ МАТЧИ И МОЖЕТ БЫТЬ ОШИБКА, ЕСЛИ АПИ БУДЕТ ПУСТЫМ
#
#
#
# def insert_preview_match_api(fixture_match):
#
#
#     #Ищу будущие встречи команды №
#     url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"        # V3 - Next {x} Fixtures to come
#     headers = {
#         "X-RapidAPI-Key": "ed9df9b66dmsh3488c78a45168b3p1f47e6jsn129a6c17d435",
#         "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
#     }
#     req_gen = requests.get(url, headers=headers, params={
#         'id':f'{fixture_match}'
#     })
#     data_gen = req_gen.json()
#
#
#     name_home_preview = data_gen['response'][0]['teams']['home']['name']
#     name_away_preview = data_gen['response'][0]['teams']['away']['name']
#     date_match = data_gen['response'][0]['fixture']['date'][:16]
#     d = f"{date_match[:10]}"
#     date_match2 = d.replace("-",'')
#     #fix_id_match = data_gen['response'][0]['fixture']['id']
#     venue = data_gen['response'][0]['fixture']['venue']['name']
#     id_team_home_preview = data_gen['response'][0]['teams']['home']['id']
#     id_team_away_preview = data_gen['response'][0]['teams']['away']['id']
#     league = data_gen['response'][0]['league']['id']
#     season = data_gen['response'][0]['league']['season']
#
#
#
#
#
#     #standings----------------------------------------------------------------------------------------
#     #TODO добавил в параметры ид команды, в другом файле есть код через цикл
#     #Места идут по группам
#     #HOME
#     url = "https://api-football-v1.p.rapidapi.com/v3/standings"   #V3 - Standings by league id
#
#     req_rank_home = requests.get(url=url, headers=headers, params={
#         'season':season,
#         'league':league,
#         'team':id_team_home_preview
#     })
#     data_rank_home = req_rank_home.json()
#
#     #AWAY
#     req_rank_away = requests.get(url=url, headers=headers, params={
#         'season':season,
#         'league':league,
#         'team':id_team_away_preview
#     })
#     data_rank_away = req_rank_away.json()
#
#     #Место team home
#     rank_team_home = data_rank_home['response'][0]['league']['standings'][0][0]['rank']
#     #Место team away
#     rank_team_away = data_rank_away['response'][0]['league']['standings'][0][0]['rank']
#
#
#
#     #TODO МЫ БЕРЕМ СТАТУ ЗА 1 ПОСЛЕДНЮЮ ИГРУ, СОХРАНЯЕМ В БД И В САМОЙ БД СУММИРУЕМ
#     #Ищу id ласт игры команды HOME
#     url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
#     req_fixture_last_game_home = requests.get(url, headers=headers, params={
#         "league":league,
#         "season":season,
#         "team":id_team_home_preview,
#         "last":"50"
#     })
#     data_fixture_last_game_home = req_fixture_last_game_home.json()
#     #Ищу id ласт игры команды HOME
#     req_fixture_last_game_away = requests.get(url, headers=headers, params={
#         "league":league,
#         "season":season,
#         "team":id_team_away_preview,
#         "last":"50"
#     })
#     data_fixture_last_game_away = req_fixture_last_game_away.json()
#
#     fixture_last_game_home = data_fixture_last_game_home['response'][0]['fixture']['id']
#     fixture_last_game_away = data_fixture_last_game_away['response'][0]['fixture']['id']
#
#     # insert_query_home = (
#     #             f"SELECT name_home_top_goals, sum(amount_home_goals), name_away_top_goals, sum(amount_away_goals), name_home_top_assists, sum(amount_home_assists), \
#     #                 name_away_top_assists, sum(amount_away_assists), name_home_top_saves, sum(amount_home_saves), name_away_top_saves, sum(amount_away_saves), \
#     #                 name_home_top_interceptions, sum(amount_home_interceptions), name_away_top_interceptions, sum(amount_away_interceptions), \
#     #                 name_home_top_duels, sum(amount_home_duels), name_away_top_duels, sum(amount_away_duels), name_home_top_fouls, sum(amount_home_fouls), \
#     #                 name_away_top_fouls, sum(amount_away_fouls)  AS name_home_review FROM match_review GROUP BY name_home_top_goals, name_away_top_goals, \
#     #                 name_home_top_assists, name_away_top_assists, name_home_top_saves, name_away_top_saves, name_home_top_interceptions, name_away_top_interceptions, \
#     #                 name_home_top_duels, name_away_top_duels, name_home_top_fouls, name_away_top_fouls"
#
#     # )
#
#
#     # insert_query_home = (
#     #     f"SELECT name_home_top_goals, sum(amount_home_goals), name_home_top_assists, sum(amount_home_assists), \
#     #         name_home_top_saves, sum(amount_home_saves),  \
#     #         name_home_top_interceptions, sum(amount_home_interceptions), \
#     #         name_home_top_duels, sum(amount_home_duels),  name_home_top_fouls, sum(amount_home_fouls), \
#     #         FROM match_review WHERE name_home_review={id_team_home_preview};"
#     # )
#     # g = insert_query_home
#     # g = g[0]
#     # print(g)
#
#     # players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_fouls_home_name,  topscorers_fouls_home_amount, topscorers_saves_home_name, topscorers_saves_home_amount = g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8],g[9],g[10],g[11]
#
#
#     # insert_query_away = (
#     #     f"SELECT name_away_top_goals, sum(amount_away_goals), \
#     #         name_away_top_assists, sum(amount_away_assists), name_away_top_saves, sum(amount_away_saves), \
#     #         name_away_top_interceptions, sum(amount_away_interceptions), \
#     #         name_away_top_duels, sum(amount_away_duels), \
#     #         name_away_top_fouls, sum(amount_away_fouls) FROM match_review WHERE name_home_review={id_team_away_preview};"
#     # )
#     # k = insert_query_away
#     # k = k[0]
#     # print(k)
#
#     # players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_away_name, topscorers_saves_away_amount = k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11]
#
#
#     insert_query_home = (
#         f"SELECT name_home_top_goals, sum(amount_home_goals), name_home_top_assists, sum(amount_home_assists), \
#             name_home_top_saves, sum(amount_home_saves),  \
#             name_home_top_interceptions, sum(amount_home_interceptions), \
#             name_home_top_duels, sum(amount_home_duels),  name_home_top_fouls, sum(amount_home_fouls), \
#             FROM match_review GROUP BY name_home_top_goals, name_home_top_assists, name_home_top_saves, name_home_top_interceptions, name_home_top_duels, name_home_top_fouls;"
#     )
#     g = insert_query_home
#     g = g[0]
#     print(g)
#
#     players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_fouls_home_name,  topscorers_fouls_home_amount, topscorers_saves_home_name, topscorers_saves_home_amount = g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8],g[9],g[10],g[11]
#
#     insert_query_away = (
#         f"SELECT name_away_top_goals, sum(amount_away_goals), \
#             name_away_top_assists, sum(amount_away_assists), name_away_top_saves, sum(amount_away_saves), \
#             name_away_top_interceptions, sum(amount_away_interceptions), \
#             name_away_top_duels, sum(amount_away_duels), \
#             name_away_top_fouls, sum(amount_away_fouls) FROM match_review GROUP BY name_away_top_goals, name_away_top_assists, name_away_top_saves, name_away_top_interceptions, name_away_top_duels, name_away_top_fouls;"
#     )
#     k = insert_query_away
#     k = k[0]
#     print(k)
#
#     players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_away_name, topscorers_saves_away_amount = k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11]
#
#
#
#
#
#     #Результативныe игроки в лиге 2ух играющих команд (Goals)
#     url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
#     req_topplayer_home = requests.get(url, headers=headers, params={
#         "id":fixture_last_game_home
#     })
#     data_topplayer_home = req_topplayer_home.json()
#     #---------------------------------------------------------------------
#     req_topplayer_away = requests.get(url, headers=headers, params={
#         "id":fixture_last_game_away
#     })
#     data_topplayer_away = req_topplayer_away.json()
#
#     if data_topplayer_home['response'][0]['fixture']['status']['long'] != "Match Postponed":
#     #     #HOME
#     #     #Ищу лучшего по голам HOME
#     #     players_a_name = ''
#     #     players_a_goals_total = 0
#     #     if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#     #         for find_home_top_goal_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
#     #             if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] != None and \
#     #             data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] > players_a_goals_total:
#     #                 players_a_goals_total = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total']
#     #                 players_a_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_goal_player]['player']['name']
#
#     #     elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#     #         for find_home_top_goal_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
#     #             if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] != None and \
#     #             data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total'] > players_a_goals_total:
#     #                 players_a_goals_total = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['statistics'][0]['goals']['total']
#     #                 players_a_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_goal_player]['player']['name']
#
#     #     #AWAY
#     #     #Ищу лучшего по голам AWAY
#     #     players_b_name = ''
#     #     players_b_goals_total = 0
#     #     if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#     #         for find_away_top_goal_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
#     #             if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] != None and \
#     #             data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] > players_b_goals_total:
#     #                 players_b_goals_total = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total']
#     #                 players_b_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_goal_player]['player']['name']
#
#     #     elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#     #         for find_away_top_goal_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
#     #             if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] != None and \
#     #             data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total'] > players_b_goals_total:
#     #                 players_b_goals_total = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['statistics'][0]['goals']['total']
#     #                 players_b_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_goal_player]['player']['name']
#
#     #     print('TEST')
#
#         #Top 3 scorer in league ----------------------------------------------------------------------------------------
#         url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"    #V3 - Top Scorers
#         req_goal = requests.get(url=url, headers=headers, params={
#             'league':league,
#             'season':'2022'
#         })
#         data_topscorers = req_goal.json()
#
#         #Top 3 scorer in league ----------------------------------------------------------------------------------------
#         topscorer_name_in_league_1 = data_topscorers['response'][0]['player']['name']
#         topscorer_name_in_league_2 = data_topscorers['response'][1]['player']['name']
#         topscorer_name_in_league_3 = data_topscorers['response'][2]['player']['name']
#
#         topscorer_amount_in_league_1 = data_topscorers['response'][0]['statistics'][0]['goals']['total']
#         topscorer_amount_in_league_2 = data_topscorers['response'][1]['statistics'][0]['goals']['total']
#         topscorer_amount_in_league_3 = data_topscorers['response'][2]['statistics'][0]['goals']['total']
#
#         topscorer_team_in_league_1 = data_topscorers['response'][0]['statistics'][0]['team']['name']
#         topscorer_team_in_league_2 = data_topscorers['response'][1]['statistics'][0]['team']['name']
#         topscorer_team_in_league_3 = data_topscorers['response'][2]['statistics'][0]['team']['name']
#
#
#
#         # #Top assists
#         # #HOME
#         # #Ищу лучшего по ассистам HOME
#         # topscorers_assists_home_name = ''
#         # topscorers_assists_home_amount = 0
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#         #     for find_home_top_assists_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] != None and \
#         #         data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_home_amount:
#         #             topscorers_assists_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists']
#         #             topscorers_assists_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_assists_player]['player']['name']
#
#         # elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#         #     for find_home_top_assists_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] != None and \
#         #         data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_home_amount:
#         #             topscorers_assists_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['statistics'][0]['goals']['assists']
#         #             topscorers_assists_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_assists_player]['player']['name']
#
#
#
#         # #AWAY
#         # #Ищу лучшего по ассистам AWAY
#         # topscorers_assists_away_name = ''
#         # topscorers_assists_away_amount = 0
#         # if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#         #     for find_away_top_assists_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] != None and \
#         #         data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_away_amount:
#         #             topscorers_assists_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists']
#         #             topscorers_assists_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_assists_player]['player']['name']
#
#         # elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#         #     for find_away_top_assists_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] != None and \
#         #         data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists'] > topscorers_assists_away_amount:
#         #             topscorers_assists_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals']['assists']
#         #             topscorers_assists_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_assists_player]['player']['name']
#
#
#
#
#
#         # #Find tackles (blocks)
#         # #HOME
#         # #Ищу лучшего по отборам HOME
#         # topscorers_blocks_home_name = ''
#         # topscorers_blocks_home_amount = 0
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#         #     for find_home_top_blocks_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] != None and \
#         #         data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_home_amount:
#         #             topscorers_blocks_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks']
#         #             topscorers_blocks_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_blocks_player]['player']['name']
#
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#         #     for find_home_top_blocks_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] != None and \
#         #         data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_home_amount:
#         #             topscorers_blocks_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['statistics'][0]['tackles']['blocks']
#         #             topscorers_blocks_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_blocks_player]['player']['name']
#
#
#
#         # #AWAY
#         # #Ищу лучшего по отборам AWAY
#         # topscorers_blocks_away_name = ''
#         # topscorers_blocks_away_amount = 0
#         # if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#         #     for find_away_top_blocks_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] != None and \
#         #         data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_away_amount:
#         #             topscorers_blocks_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks']
#         #             topscorers_blocks_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_blocks_player]['player']['name']
#
#         # elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#         #     for find_away_top_blocks_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] != None and \
#         #         data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks'] > topscorers_blocks_away_amount:
#         #             topscorers_blocks_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['statistics'][0]['tackles']['blocks']
#         #             topscorers_blocks_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_blocks_player]['player']['name']
#
#
#
#         # #Find duels
#         # #HOME
#         # #Ищу лучшего по duels HOME
#         # topscorers_duels_home_name = ''
#         # topscorers_duels_home_amount = 0
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#         #     for find_home_top_duels_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] != None and \
#         #         data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_home_amount:
#         #             topscorers_duels_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won']
#         #             topscorers_duels_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_duels_player]['player']['name']
#
#         # elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#         #     for find_home_top_duels_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] != None and \
#         #         data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_home_amount:
#         #             topscorers_duels_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['statistics'][0]['duels']['won']
#         #             topscorers_duels_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_duels_player]['player']['name']
#
#         # #AWAY
#         # #Ищу лучшего по duels AWAY
#         # topscorers_duels_away_name = ''
#         # topscorers_duels_away_amount = 0
#         # if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#         #     for find_away_top_duels_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] != None and \
#         #         data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_away_amount:
#         #             topscorers_duels_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won']
#         #             topscorers_duels_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_duels_player]['player']['name']
#
#
#         # elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#         #     for find_away_top_duels_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] != None and \
#         #         data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won'] > topscorers_duels_away_amount:
#         #             topscorers_duels_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['statistics'][0]['duels']['won']
#         #             topscorers_duels_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_duels_player]['player']['name']
#
#
#
#
#         # #Find fouls
#         # #HOME
#         # #Ищу лучшего по fouls HOME
#         # topscorers_fouls_home_name = ''
#         # topscorers_fouls_home_amount = 0
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#         #     for find_home_top_fouls_player in range(len(data_topplayer_home['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
#         #         data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_home_amount:
#         #             topscorers_fouls_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed']
#         #             topscorers_fouls_home_name = data_topplayer_home['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['name']
#
#         # elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#         #     for find_home_top_fouls_player in range(len(data_topplayer_home['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
#         #         data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_home_amount:
#         #             topscorers_fouls_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed']
#         #             topscorers_fouls_home_name = data_topplayer_home['response'][0]['players'][1]['players'][find_home_top_fouls_player]['player']['name']
#
#
#         # #AWAY
#         # #Ищу лучшего по fouls AWAY
#         # topscorers_fouls_away_name = ''
#         # topscorers_fouls_away_amount = 0
#         # if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#         #     for find_away_top_fouls_player in range(len(data_topplayer_away['response'][0]['players'][0]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
#         #         data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_away_amount:
#         #             topscorers_fouls_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed']
#         #             topscorers_fouls_away_name = data_topplayer_away['response'][0]['players'][0]['players'][find_away_top_fouls_player]['player']['name']
#
#         # elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#         #     for find_away_top_fouls_player in range(len(data_topplayer_away['response'][0]['players'][1]['players'])):
#         #         if data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
#         #         data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] > topscorers_fouls_away_amount:
#         #             topscorers_fouls_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed']
#         #             topscorers_fouls_away_name = data_topplayer_away['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['name']
#
#
#
#
#         # #Top goals saves
#         # #HOME
#         # #Ищу лучшего по сейвам HOME
#         # topscorers_saves_home_name = ''
#         # topscorers_saves_home_amount = 0
#         # if name_home_preview == data_topplayer_home['response'][0]['teams']['home']['name']:
#         #     topscorers_saves_home_amount = data_topplayer_home['response'][0]['players'][0]['players'][0]['statistics'][0]['goals']['saves']
#         #     topscorers_saves_home_name = data_topplayer_home['response'][0]['players'][0]['players'][0]['player']['name']
#         #     if topscorers_saves_home_amount == None:
#         #         topscorers_saves_home_amount = 0
#
#
#         # elif name_home_preview == data_topplayer_home['response'][0]['teams']['away']['name']:
#         #     topscorers_saves_home_amount = data_topplayer_home['response'][0]['players'][1]['players'][0]['statistics'][0]['goals']['saves']
#         #     topscorers_saves_home_name = data_topplayer_home['response'][0]['players'][1]['players'][0]['player']['name']
#         #     if topscorers_saves_home_amount == None:
#         #         topscorers_saves_home_amount = 0
#
#
#         # #AWAY
#         # #Ищу лучшего по сейвам AWAY
#         # topscorers_saves_away_name = ''
#         # topscorers_saves_away_amount = 0
#         # if name_away_preview == data_topplayer_away['response'][0]['teams']['home']['name']:
#         #     topscorers_saves_away_amount = data_topplayer_away['response'][0]['players'][0]['players'][0]['statistics'][0]['goals']['saves']
#         #     topscorers_saves_away_name = data_topplayer_away['response'][0]['players'][0]['players'][0]['player']['name']
#         #     if topscorers_saves_away_amount == None:
#         #         topscorers_saves_away_amount = 0
#
#         # elif name_away_preview == data_topplayer_away['response'][0]['teams']['away']['name']:
#         #     topscorers_saves_away_amount = data_topplayer_away['response'][0]['players'][1]['players'][0]['statistics'][0]['goals']['saves']
#         #     topscorers_saves_away_name = data_topplayer_away['response'][0]['players'][1]['players'][0]['player']['name']
#         #     if topscorers_saves_away_amount == None:
#         #         topscorers_saves_away_amount = 0
#
#
#         # #TODO Убрать этот запрос (не нужен)
#         # #Last 5 game
#         # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"         #V3 - Last {x} Fixtures that were played
#         # req_last_game_home = requests.get(url=url, headers=headers, params={
#         #     'league':league,
#         #     'season':season,
#         #     'team':id_team_home_preview,   #Вставляю ид команды, выше есть переменные по обеим командам
#         #     'last':'5'
#         # })
#         # data_last_game_home = req_last_game_home.json()
#         # req_last_game_away = requests.get(url=url, headers=headers, params={
#         #     'league':league,
#         #     'season':season,
#         #     'team':id_team_away_preview,   #Вставляю ид команды, выше есть переменные по обеим командам
#         #     'last':'5'
#         # })
#         # data_last_game_away = req_last_game_away.json()
#
#
#         # #TODO Важно счет последних игр будет в формате словаря
#         # #Статистика за последние № игр команды HOME
#         # home_last_games_who = []
#         # home_last_games_rival = []
#         # home_last_games_scores = []
#         # for find_last_games_home in range(len(data_last_game_home['response'])):
#         #     if data_last_game_home['response'][find_last_games_home]['teams']['home']['name'] == name_home_preview:
#         #         home_last_games_who.append(data_last_game_home['response'][find_last_games_home]['teams']['home']['name'])
#         #     else:
#         #         home_last_games_who.append(data_last_game_home['response'][find_last_games_home]['teams']['away']['name'])
#
#         #     if data_last_game_home['response'][find_last_games_home]['teams']['home']['name'] != name_home_preview:
#         #         home_last_games_rival.append(data_last_game_home['response'][find_last_games_home]['teams']['home']['name'])
#         #     else:
#         #         home_last_games_rival.append(data_last_game_home['response'][find_last_games_home]['teams']['away']['name'])
#
#         #     home_last_games_scores.append(data_last_game_home['response'][find_last_games_home]['goals'])
#
#
#         # #Статистика за последние № игр команды AWAY
#         # away_last_games_who = []
#         # away_last_games_rival = []
#         # away_last_games_scores = []
#         # for find_last_games_away in range(len(data_last_game_away['response'])):
#         #     if data_last_game_away['response'][find_last_games_away]['teams']['home']['name'] == name_away_preview:
#         #         away_last_games_who.append(data_last_game_away['response'][find_last_games_away]['teams']['home']['name'])
#         #     else:
#         #         away_last_games_who.append(data_last_game_away['response'][find_last_games_away]['teams']['away']['name'])
#
#         #     if data_last_game_away['response'][find_last_games_away]['teams']['home']['name'] != name_away_preview:
#         #         away_last_games_rival.append(data_last_game_away['response'][find_last_games_away]['teams']['home']['name'])
#         #     else:
#         #         away_last_games_rival.append(data_last_game_away['response'][find_last_games_away]['teams']['away']['name'])
#
#         #     away_last_games_scores.append(data_last_game_away['response'][find_last_games_away]['goals'])
#
#
#
#         #TODO cчитаем игры в ноль, крупные победы, поражения только 1 команды, запрос идет к айди команды
#         #Cчитаю сколько раз команда home играла в ничью, крупные поражения и победы
#         url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"            #V3 - Teams Statistics
#         req_game_stat_home = requests.get(url, headers=headers, params={
#             'league':league,
#             'season':season,
#             'team':id_team_home_preview
#         })
#         data_home_stat = req_game_stat_home.json()
#         req_game_stat_away = requests.get(url, headers=headers, params={
#             'league':league,
#             'season':season,
#             'team':id_team_away_preview
#         })
#         data_away_stat = req_game_stat_away.json()
#
#         #HOME
#         home_play_clean_sheet = data_home_stat['response']['clean_sheet']['total']       #на ноль сыграла
#         home_biggest_win_in_home = data_home_stat['response']['biggest']['wins']['home']
#         home_biggest_win_in_away = data_home_stat['response']['biggest']['wins']['away']
#         home_biggest_lose_in_home = data_home_stat['response']['biggest']['loses']['home']
#         home_biggest_lose_in_away = data_home_stat['response']['biggest']['loses']['away']
#
#
#
#         #Если параметр равен null, то приравниваем к 0
#         if home_biggest_win_in_home == None:
#             home_biggest_win_in_home = 0
#         if home_biggest_win_in_away == None:
#             home_biggest_win_in_away = 0
#         if home_biggest_lose_in_home == None:
#             home_biggest_lose_in_home = 0
#         if home_biggest_lose_in_away == None:
#             home_biggest_lose_in_away = 0
#
#
#         #Form game
#         form_home = data_home_stat['response']['form'][:5]
#         form_away = data_away_stat['response']['form'][:5]
#
#
#         #AWAY
#         away_play_clean_sheet = data_away_stat['response']['clean_sheet']['total']        #на ноль сыграла
#         away_biggest_win_in_home = data_away_stat['response']['biggest']['wins']['home']
#         away_biggest_win_in_away = data_away_stat['response']['biggest']['wins']['away']
#         away_biggest_lose_in_home = data_away_stat['response']['biggest']['loses']['home']
#         away_biggest_lose_in_away = data_away_stat['response']['biggest']['loses']['away']
#
#
#         #Если параметр равен null, то приравниваем к 0
#         if away_biggest_win_in_home == None:
#             away_biggest_win_in_home = 0
#         if away_biggest_win_in_away == None:
#             away_biggest_win_in_away = 0
#         if away_biggest_lose_in_home == None:
#             away_biggest_lose_in_home = 0
#         if away_biggest_lose_in_away == None:
#             away_biggest_lose_in_away = 0
#
#
#         #В текущем сезоне HOME выигрывала дома, проигрывала и сыграла в ничью
#         home_win_once_in_home = data_home_stat['response']['fixtures']['wins']['total']
#         home_lose_once_in_home = data_home_stat['response']['fixtures']['loses']['total']
#         home_draws_once_in_home = data_home_stat['response']['fixtures']['draws']['total']
#
#
#         #В текущем сезоне AWAY выигрывала на выезде, проигрывала и сыграла в ничью
#         away_win_once_in_away = data_away_stat['response']['fixtures']['wins']['total']
#         away_lose_once_in_away = data_away_stat['response']['fixtures']['loses']['total']
#         away_draws_once_in_away = data_away_stat['response']['fixtures']['draws']['total']
#
#
#
#         #Создаю список когда HOME забивали и на какой минуте, если значение None, список не пополняется
#         list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
#         list_minute_for_goals_home = []
#         list_for_goal_home = []
#         for minute_for_goal_home in range(8):
#             if data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'] != None:
#                 list_minute_for_goals_home.append(list_minute[minute_for_goal_home])
#                 list_for_goal_home.append(data_home_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_home]]['percentage'])
#
#
#
#         #Создаю список когда HOME пропускали голы и на какой минуте, если значение None, список не пополняется
#         list_minute_missed_goals_home = []
#         list_missed_goal_home = []
#         for minute_for_missed_home in range(8):
#             if data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'] != None:
#                 list_minute_missed_goals_home.append(list_minute[minute_for_missed_home])
#                 list_missed_goal_home.append(data_home_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_home]]['percentage'])
#
#
#
#         # #TODO Списки не имеют 0% значения, поэтому вызываем по индексу
#         #Создаю список когда AWAY забивали и на какой минуте, если значение None, список не пополняется
#         list_minute_for_goals_away = []
#         list_for_goal_away = []
#         for minute_for_goal_away in range(8):
#             if data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'] != None:
#                 list_minute_for_goals_away.append(list_minute[minute_for_goal_away])
#                 list_for_goal_away.append(data_away_stat['response']['goals']['for']['minute'][list_minute[minute_for_goal_away]]['percentage'])
#
#
#
#         #Создаю список когда AWAY пропускали голы и на какой минуте, если значение None, список не пополняется
#         list_minute_missed_goals_away = []
#         list_missed_goal_away = []
#         for minute_for_missed_away in range(8):
#             if data_away_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_away]]['percentage'] != None:
#                 list_minute_missed_goals_away.append(list_minute[minute_for_missed_away])
#                 list_missed_goal_away.append(data_away_stat['response']['goals']['against']['minute'][list_minute[minute_for_missed_away]]['percentage'])
#
#
#
#         # #TODO Списки не имеют 0% значения, поэтому вызываем по индексу
#
#         #Predictions
#         url = "https://api-football-v1.p.rapidapi.com/v3/predictions"            #V3 - Predictions
#         req_predictions = requests.get(url, headers=headers, params={
#             "fixture":f'{fixture_match}'
#         })
#         data_predictions = req_predictions.json()
#
#
#         predictions_percent_home = data_predictions['response'][0]['predictions']['percent']['home']
#         predictions_percent_away = data_predictions['response'][0]['predictions']['percent']['away']
#         predictions_percent_draw = data_predictions['response'][0]['predictions']['percent']['draw']
#
#
#         predictions_goals_home = data_predictions['response'][0]['predictions']['goals']['home']
#         predictions_goals_away = data_predictions['response'][0]['predictions']['goals']['away']
#
#         predictions_goals_home = str(predictions_goals_home).replace("-", "")
#         predictions_goals_home = math.ceil(float(predictions_goals_home))
#         predictions_goals_home = round(float(predictions_goals_home)+ 0.1)
#
#         predictions_goals_away = str(predictions_goals_away).replace("-", "")
#         predictions_goals_away = math.ceil(float(predictions_goals_away))
#         predictions_goals_away = round(float(predictions_goals_away)+ 0.1)
#
#         print(predictions_goals_home)
#         #Статистика личных встреч за последние 3 сезона
#         #HOME
#         print('test Статистика личных встреч за последние 3 сезона')
#         h2h_home_total_games = 0
#         h2h_home_total_wins_in_home = 0
#         h2h_home_total_wins_in_away = 0
#         h2h_home_total_draws_in_home = 0
#         h2h_home_total_draws_in_away = 0
#         h2h_home_total_loses_in_home = 0
#         h2h_home_total_loses_in_away = 0
#         for h2h_home in range(len(data_predictions['response'][0]['h2h'])):
#             if data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['name'] == name_home_preview:
#                 if data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2021 or \
#                 data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2020 or \
#                 data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2019:
#                     h2h_home_total_games += 1
#                     if data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == True:
#                         h2h_home_total_wins_in_home += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == False:
#                         h2h_home_total_loses_in_home += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['home']['winner'] == None:
#                         h2h_home_total_draws_in_home += 1
#
#
#             elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['name'] == name_home_preview:
#                 if data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2021 or \
#                 data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2020 or \
#                 data_predictions['response'][0]['h2h'][h2h_home]['league']['season'] == 2019:
#                     h2h_home_total_games += 1
#                     if data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == True:
#                         h2h_home_total_wins_in_away += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == False:
#                         h2h_home_total_loses_in_away += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_home]['teams']['away']['winner'] == None:
#                         h2h_home_total_draws_in_away += 1
#
#
#         #AWAY
#
#         h2h_away_total_games = 0
#         h2h_away_total_wins_home = 0
#         h2h_away_total_wins_away = 0
#         h2h_away_total_draws_in_home = 0
#         h2h_away_total_draws_in_away = 0
#         h2h_away_total_loses_in_home = 0
#         h2h_away_total_loses_in_away = 0
#         for h2h_away in range(len(data_predictions['response'][0]['h2h'])):
#             if data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['name'] == name_away_preview:
#                 if data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2021 or \
#                 data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2020 or \
#                 data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2019:
#                     h2h_away_total_games += 1
#                     if data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == True:
#                         h2h_away_total_wins_home += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == False:
#                         h2h_away_total_loses_in_home += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['home']['winner'] == None:
#                         h2h_away_total_draws_in_home += 1
#
#             elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['name'] == name_away_preview:
#                 if data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2021 or \
#                 data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2020 or \
#                 data_predictions['response'][0]['h2h'][h2h_away]['league']['season'] == 2019:
#                     h2h_away_total_games += 1
#                     if data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == True:
#                         h2h_away_total_wins_away += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == False:
#                         h2h_away_total_loses_in_away += 1
#                     elif data_predictions['response'][0]['h2h'][h2h_away]['teams']['away']['winner'] == None:
#                         h2h_away_total_draws_in_away += 1
#
#         print('test Вероятностные характеристики команд перед матчем:')
#         #Вероятностные характеристики команд перед матчем:
#         comparison_total_home = ''
#         comparison_att_home = ''
#         comparison_def_home = ''
#         comparison_h2h_home = ''
#         comparison_goals_home = ''
#
#         if data_predictions['response'][0]['teams']['home']['name'] == name_home_preview:
#             comparison_total_home = data_predictions['response'][0]['comparison']['total']['home']
#             comparison_att_home = data_predictions['response'][0]['comparison']['att']['home']
#             comparison_def_home = data_predictions['response'][0]['comparison']['def']['home']
#             comparison_h2h_home = data_predictions['response'][0]['comparison']['h2h']['home']
#             comparison_goals_home = data_predictions['response'][0]['comparison']['goals']['home']
#         elif data_predictions['response'][0]['teams']['away']['name'] == name_home_preview:
#             comparison_total_home = data_predictions['response'][0]['comparison']['total']['home']
#             comparison_att_home = data_predictions['response'][0]['comparison']['att']['home']
#             comparison_def_home = data_predictions['response'][0]['comparison']['def']['home']
#             comparison_h2h_home = data_predictions['response'][0]['comparison']['h2h']['home']
#             comparison_goals_home = data_predictions['response'][0]['comparison']['goals']['home']
#
#
#         comparison_total_away = ''
#         comparison_att_away = ''
#         comparison_def_away = ''
#         comparison_h2h_away = ''
#         comparison_goals_away = ''
#
#         if data_predictions['response'][0]['teams']['home']['name'] == name_away_preview:
#             comparison_total_away = data_predictions['response'][0]['comparison']['total']['home']
#             comparison_att_away = data_predictions['response'][0]['comparison']['att']['home']
#             comparison_def_away = data_predictions['response'][0]['comparison']['def']['home']
#             comparison_h2h_away = data_predictions['response'][0]['comparison']['h2h']['home']
#             comparison_goals_away = data_predictions['response'][0]['comparison']['goals']['home']
#         elif data_predictions['response'][0]['teams']['away']['name'] == name_away_preview:
#             comparison_total_away = data_predictions['response'][0]['comparison']['total']['home']
#             comparison_att_away = data_predictions['response'][0]['comparison']['att']['home']
#             comparison_def_away = data_predictions['response'][0]['comparison']['def']['home']
#             comparison_h2h_away = data_predictions['response'][0]['comparison']['h2h']['home']
#             comparison_goals_away = data_predictions['response'][0]['comparison']['goals']['home']
#
#
#
#
#         #BK
#         url = "https://api-football-v1.p.rapidapi.com/v3/odds"
#         req_bk = requests.request("GET", url, headers=headers, params={
#             'fixture':f'{fixture_match}'
#         })
#         data_bk = req_bk.json()
#
#
#         bk_coef_name = []
#         bk_coef_home = []
#         bk_coef_draw = []
#         bk_coef_away = []
#         for find_bk in range(len(data_bk['response'][0]['bookmakers'])):
#             bk_coef_name.append(data_bk['response'][0]['bookmakers'][find_bk]['name'])
#             bk_coef_home.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][0]['odd'])
#             bk_coef_draw.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][1]['odd'])
#             bk_coef_away.append(data_bk['response'][0]['bookmakers'][find_bk]['bets'][0]['values'][2]['odd'])
#
#
#         # result_home_last_games_who = ' '.join(home_last_games_who)
#         # result_home_last_games_rival = ' '.join(home_last_games_rival)
#         # list_home_last_games_scores = []
#         # for dict1 in home_last_games_scores:
#         #     if type(dict1) == type(str()):
#         #         list_home_last_games_scores.append(dict1)
#         #     elif type(dict1) == type(dict()):
#         #         for key in dict1:
#         #             list_home_last_games_scores += [key, str(dict1[key])]
#         # result_home_last_games_scores = ' '.join(list_home_last_games_scores)
#
#         # result_away_last_games_who = ' '.join(away_last_games_who)
#         # result_away_last_games_rival = ' '.join(away_last_games_rival)
#         # list_awa  y_last_games_scores = []
#         # for dict2 in away_last_games_scores:
#         #     if type(dict2) == type(str()):
#         #         list_away_last_games_scores.append(dict2)
#         #     elif type(dict2) == type(dict()):
#         #         for key in dict2:
#         #             list_away_last_games_scores += [key, str(dict2[key])]
#         #result_away_last_games_scores = ' '.join(list_away_last_games_scores)
#
#         result_list_minute = ' '.join(list_minute)
#         result_list_minute_for_goals_home = ' '.join(list_minute_for_goals_home)
#         result_list_for_goal_home = ' '.join(list_for_goal_home)
#         result_list_minute_missed_goals_home = ' '.join(list_minute_missed_goals_home)
#         result_list_missed_goal_home = ' '.join(list_missed_goal_home)
#         result_list_minute_for_goals_away = ' '.join(list_minute_for_goals_away)
#         result_list_for_goal_away = ' '.join(list_for_goal_away)
#         result_list_minute_missed_goals_away = ' '.join(list_minute_missed_goals_away)
#         result_list_missed_goal_away = ' '.join(list_missed_goal_away)
#         result_bk_coef_name = ' '.join(bk_coef_name)
#         result_bk_coef_home = ' '.join(bk_coef_home)
#         result_bk_coef_draw = ' '.join(bk_coef_draw)
#         result_bk_coef_away = ' '.join(bk_coef_away)
#
#         #f" INSERT INTO match_preview (fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_home_name, topscorers_fouls_home_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_last_games_who, home_last_games_rival, home_last_games_scores, away_last_games_who, away_last_games_rival, away_last_games_scores, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away)"
#         if venue.find("'"):
#             venue = venue.replace("'", " ")
#         # if name_home_preview.find("'"):
#         #     name_home_preview = name_home_preview.replace("'", " ")
#         # if name_away_preview.find("'"):
#         #     name_away_preview = name_away_preview.replace("'", " ")
#         if players_a_name.find("'"):
#             players_a_name = players_a_name.replace("'", " ")
#         if players_b_name.find("'"):
#             players_b_name = players_b_name.replace("'", " ")
#         if topscorer_team_in_league_3.find("'"):
#             topscorer_team_in_league_3 = topscorer_team_in_league_3.replace("'", " ")
#         if topscorer_team_in_league_2.find("'"):
#             topscorer_team_in_league_2 = topscorer_team_in_league_2.replace("'", " ")
#         if topscorer_team_in_league_1.find("'"):
#             topscorer_team_in_league_1 = topscorer_team_in_league_1.replace("'", " ")
#         if topscorer_name_in_league_3.find("'"):
#             topscorer_name_in_league_3 = topscorer_name_in_league_3.replace("'", " ")
#         if topscorer_name_in_league_2.find("'"):
#             topscorer_name_in_league_2 = topscorer_name_in_league_2.replace("'", " ")
#         if topscorer_name_in_league_1.find("'"):
#             topscorer_name_in_league_1 = topscorer_name_in_league_1.replace("'", " ")
#         if topscorers_blocks_away_name.find("'"):
#             topscorers_blocks_away_name = topscorers_blocks_away_name.replace("'", " ")
#         if topscorers_duels_away_name.find("'"):
#             topscorers_duels_away_name = topscorers_duels_away_name.replace("'", " ")
#         if topscorers_fouls_away_name.find("'"):
#             topscorers_fouls_away_name = topscorers_fouls_away_name.replace("'", " ")
#         if topscorers_saves_away_name.find("'"):
#             topscorers_saves_away_name = topscorers_saves_away_name.replace("'", " ")
#         if topscorers_saves_home_name.find("'"):
#             topscorers_saves_home_name = topscorers_saves_home_name.replace("'", " ")
#         if topscorers_blocks_home_name.find("'"):
#             topscorers_blocks_home_name = topscorers_blocks_home_name.replace("'", " ")
#         if topscorers_assists_home_name.find("'"):
#             topscorers_assists_home_name = topscorers_assists_home_name.replace("'", " ")
#         if topscorers_duels_home_name.find("'"):
#             topscorers_duels_home_name = topscorers_duels_home_name.replace("'", " ")
#         if topscorers_fouls_home_name.find("'"):
#             topscorers_fouls_home_name = topscorers_fouls_home_name.replace("'", " ")
#
#
#
#         # Составление запроса
#         insert_query = (
#
#                         f" INSERT INTO match_preview (fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, fixture_last_game_home, fixture_last_game_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_blocks_home_name, topscorers_blocks_home_amount, topscorers_blocks_away_name, topscorers_blocks_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_home_name, topscorers_fouls_home_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away)"
#                         f"VALUES ('{fixture_match}', '{name_home_preview}', '{name_away_preview}', '{date_match}', '{venue}', '{id_team_home_preview}',"
#                         f"'{id_team_away_preview}', '{league}', '{season}', '{rank_team_home}', '{rank_team_away}', '{fixture_last_game_home}',"
#                         f"'{fixture_last_game_away}', '{players_a_name}', '{players_a_goals_total}', '{players_b_name}', '{players_b_goals_total}',"
#                         f"'{topscorers_assists_home_name}', '{topscorers_assists_home_amount}', '{topscorers_assists_away_name}', '{topscorers_assists_away_amount}',"
#                         f"'{topscorers_blocks_home_name}', '{topscorers_blocks_home_amount}', '{topscorers_blocks_away_name}', '{topscorers_blocks_away_amount}',"
#                         f"'{topscorers_duels_home_name}', '{topscorers_duels_home_amount}', '{topscorers_duels_away_name}', '{topscorers_duels_away_amount}',"
#                         f"'{topscorers_fouls_home_name}', '{topscorers_fouls_home_amount}', '{topscorers_fouls_away_name}', '{topscorers_fouls_away_amount}',"
#                         f"'{topscorers_saves_home_name}', '{topscorers_saves_home_amount}', '{topscorers_saves_away_name}', '{topscorers_saves_away_amount}', '{fixture_match}', '{date_match2}',"
#
#                         f"'{topscorer_name_in_league_1}', '{topscorer_name_in_league_2}', '{topscorer_name_in_league_3}', '{topscorer_amount_in_league_1}',"
#                         f"'{topscorer_amount_in_league_2}', '{topscorer_amount_in_league_3}', '{topscorer_team_in_league_1}', '{topscorer_team_in_league_2}',"
#                         f"'{topscorer_team_in_league_3}', '{home_play_clean_sheet}',"
#
#                         f"'{home_biggest_win_in_home}', '{home_biggest_win_in_away}', '{home_biggest_lose_in_home}', '{home_biggest_lose_in_away}',"
#                         f"'{away_play_clean_sheet}', '{away_biggest_win_in_home}', '{away_biggest_win_in_away}', '{away_biggest_lose_in_home}',"
#                         f"'{away_biggest_lose_in_away}', '{home_win_once_in_home}', '{home_lose_once_in_home}', '{home_draws_once_in_home}',"
#
#                         f"'{away_win_once_in_away}', '{away_lose_once_in_away}', '{away_draws_once_in_away}', '{result_list_minute}',"
#                         f"'{result_list_minute_for_goals_home}', '{result_list_for_goal_home}', '{result_list_minute_missed_goals_home}', '{result_list_missed_goal_home}',"
#                         f"'{result_list_minute_for_goals_away}', '{result_list_for_goal_away}', '{result_list_minute_missed_goals_away}', '{result_list_missed_goal_away}',"
#                         f"'{predictions_percent_home}', '{predictions_percent_away}', '{predictions_percent_draw}', '{predictions_goals_home}', '{predictions_goals_away}', '{form_home}', '{form_away}', '{result_bk_coef_name}', '{result_bk_coef_home}', '{result_bk_coef_draw}', '{result_bk_coef_away}',"
#                         f"'{h2h_home_total_games}', '{h2h_home_total_wins_in_home}', '{h2h_home_total_wins_in_away}', '{h2h_home_total_draws_in_home}', '{h2h_home_total_draws_in_away}',"
#                         f"'{h2h_home_total_loses_in_home}', '{h2h_home_total_loses_in_away}', '{h2h_away_total_games}', '{h2h_away_total_wins_home}', '{h2h_away_total_wins_away}',"
#                         f"'{h2h_away_total_draws_in_home}', '{h2h_away_total_draws_in_away}', '{h2h_away_total_loses_in_home}', '{h2h_away_total_loses_in_away}', '{comparison_total_home}', '{comparison_att_home}', '{comparison_def_home}',"
#                         f"'{comparison_h2h_home}', '{comparison_goals_home}', '{comparison_total_away}', '{comparison_att_away}', '{comparison_def_away}', '{comparison_h2h_away}', '{comparison_goals_away}')"
#                         )
#
#         # Запуск функции сохранения
#         insert_db(insert_query)
#
# #'{h2h_away_total_wins}', '{h2h_away_total_draws}', '{h2h_away_total_loses}',
# #h2h_home_total_games, h2h_home_total_wins, h2h_home_total_draws, h2h_home_total_loses, h2h_away_total_games, h2h_away_total_wins, h2h_away_total_draws, h2h_away_total_loses,     #f"'{h2h_home_total_games}', '{h2h_home_total_wins}', '{h2h_home_total_draws}', '{h2h_home_total_loses}', '{h2h_away_total_games}',"