import requests
# from copy_text1_future_match import id_team_away_preview, id_team_home_preview, league, season
from review.db import insert_db, chec_in_db, check_form_review, get_one_data
from review.db import check_player, get_old_data, check_fixture_match_in_db, check_form, check_fixture_match_in_db_with_round
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

def update_form_teams(team_id, view, league_id, season):
    league_id = f"{league_id}"
    if league_id == "1":
        teams = 'teams_cup'
    else:
        teams = 'teams_test'

    old_form = get_old_data(team_id, 'form', teams, '1', 'team_id_api', season)

    if old_form != '0':
        new_form = view + old_form
    else:
        new_form = view

    if len(new_form) > 5:
        new_form = new_form[:5]

    insert_query = f" UPDATE {teams} SET form = '{new_form}' WHERE team_id_api = {team_id};"
    insert_db(insert_query, 'add team')

import requests
import json

def request_name_to_api(season, league_id, player_id, name):
    """
    Функция для изменения имени

    Получение с API or Database
    return имя
    """

    """ Проверка есть ли он в БД """
    search_user = get_one_data(f"SELECT name FROM players_test WHERE player_id_api = {player_id} AND season = {season} AND league_id = {league_id}") # -> ['name']
    if search_user == []:
        """
        Если нет: 
        
        1. Делаем запрос в АПИ 
        2. Получаем firstname + lastname
        3. Сохраняем в переменную "name"
        """
        url = os.getenv('RAPID_API_BASE_URL')+"/players"
        querystring = {"id":str(player_id),"season":season}
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
            "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
        }
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        """ Поиск по ответу """
        try:
            full_name = response['response'][0]['player']['firstname'] + " " + response['response'][0]['player']['lastname']
            if "'" in full_name: full_name = full_name.replace("'", "")

            insert_db(f"INSERT INTO players_test(player_id_api, name, season, league_id) "
                      f"VALUES ('{player_id}','{full_name}', '{season}', '{league_id}')", "add name")

            return full_name # -> firstname + lastname
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
        return search_user[0][0] # [('Leo Messi')] -> 'Leo Messi'

def player_update(list_id, list_name, list_amount, data_types, season, league_id, team_id, round, fixture_match):
    league_id = f"{league_id}"
    add_query = f" AND season = {season} AND league_id = {league_id}"

    if list_id != []:
        if league_id == '1':
            players = 'players_cup'
        else:
            players = 'players_test'

        for i in range(len(list_id)):
            name = list_name[i]
            name_old = list_name[i]
            if str(name).find("'"):
                name = str(name).replace("'", "")

            """ Проверка есть ли проблема с именем (Есть ли точка в full_name Пример: L. Messi) """
            if "." in name: # L. Messi
                """ Проверяем есть ли в БД """
                db_name = get_one_data(
                    f"SELECT name FROM players_test "
                    f"WHERE player_id_api = {list_id[i]} "
                    f"AND season = {season} AND league_id = {league_id} "
                   )
                if db_name == []:
                    """ Если в БД нет """
                    try:
                        """ Пробуем взять с АПИ fitsname + lastname """
                        name = request_name_to_api(
                            season, league_id,
                            list_id[i], list_name[i]) # id (L. Messi) -> Leo Messi
                    except:
                        """ Если нет данных оставляем старое имя с "." """
                        name = name_old # id (L. Messi)
                elif db_name != []:
                    """ Если в БД есть """
                    name = db_name[0][0] # [('Leo Messi')] -> Leo Messi

            # update
            if check_player(list_id[i], players, '1', season, league_id, team_id) == True:
                old_data = get_old_data(list_id[i], data_types, players, '1', 'player_id_api', season)
                data = list_amount[i]
                insert_query = ''
                if old_data == None:
                    if data_types == 'fast_goal':
                        if int(data) != 0:
                            insert_query = (
                                f" UPDATE {players} SET {data_types} = {data}, fixture_match_for_fast_goal = {fixture_match} WHERE player_id_api = {list_id[i]}{add_query}"
                            )
                    else:
                        insert_query = (
                            f" UPDATE {players} SET {data_types} = {data} WHERE player_id_api = {list_id[i]}{add_query}"
                        )
                else:
                    if data_types == 'fast_goal':
                        if int(data) != 0:
                            if int(old_data) != 0:
                                if int(old_data) > int(data):
                                    insert_query = (
                                        f" UPDATE {players} SET {data_types} = {data}, fixture_match_for_fast_goal = {fixture_match} WHERE player_id_api = {list_id[i]}{add_query}"
                                    )
                            else:
                                insert_query = (
                                    f" UPDATE {players} SET {data_types} = {data}, fixture_match_for_fast_goal = {fixture_match} WHERE player_id_api = {list_id[i]}{add_query}"
                                )
                    else:
                        data = int(old_data) + int(data) if int(old_data) != 0 else data
                        insert_query = (
                            f" UPDATE {players} SET {data_types} = {data} WHERE player_id_api = {list_id[i]}{add_query}"
                        )
                if insert_query != '':
                    insert_db(insert_query, f'UPDATE {players}')
            # create
            elif check_player(list_id[i], players, '1', season, league_id, team_id) == False:
                if data_types == 'fast_goal':
                    insert_query = (
                        f" INSERT INTO {players}(player_id_api, name, {data_types}, fixture_match_for_fast_goal , season, league_id, team_id)"
                        f" VALUES ('{list_id[i]}', '{name}', '{list_amount[i]}', '{fixture_match}','{season}', '{league_id}', '{team_id}')"
                    )
                else:
                    insert_query = (
                        f" INSERT INTO {players}(player_id_api, name, {data_types}, season, league_id, team_id)"
                        f" VALUES ('{list_id[i]}', '{name}', '{list_amount[i]}', '{season}', '{league_id}', '{team_id}')"
                    )
                insert_db(insert_query, 'add_player')

        if league_id != '1':
            for i in range(len(list_id)):
                name = list_name[i]
                
                name_old = list_name[i]
                if str(name).find("'"):
                    name = str(name).replace("'", "")

                """ Проверка есть ли проблема с именем (Есть ли точка в full_name Пример: L. Messi) """
                if "." in name:  # L. Messi
                    """ Проверяем есть ли в БД """
                    db_name = get_one_data(f"SELECT name FROM players_test WHERE player_id_api = {list_id[i]}{add_query}")
                    if db_name == []:
                        """ Если в БД нет """
                        try:
                            """ Пробуем взять с АПИ fitsname + lastname """
                            name = request_name_to_api(season, league_id, list_id[i], name_old)  # id (L. Messi) -> Leo Messi
                        except:
                            """ Если нет данных оставляем старое имя с "." """
                            name = name_old  # id (L. Messi)
                    elif db_name != []:
                        """ Если в БД есть """
                        name = db_name[0][0]  # [('Leo Messi')] -> Leo Messi

                # update
                if check_player(list_id[i], 'players_round', round, season, league_id, team_id) == True:
                    old_data = get_old_data(list_id[i], data_types, 'players_round', round, 'player_id_api', season)
                    data = list_amount[i]
                    insert_query = ''
                    if old_data == None:
                        insert_query = (
                            f" UPDATE players_round SET {data_types} = {data} WHERE player_id_api = {list_id[i]} AND round = {round}{add_query}"
                        )
                    else:
                        if data_types == 'fast_goal':
                            if int(data) != 0:
                                if int(old_data) != 0:
                                    if int(old_data) > int(data):
                                        insert_query = (
                                            f" UPDATE players_round SET {data_types} = {data}, fixture_match = {fixture_match} WHERE player_id_api = {list_id[0]} AND round = {round}{add_query}"
                                        )
                                else:
                                    insert_query = (
                                        f" UPDATE players_round SET {data_types} = {data}, fixture_match = {fixture_match} WHERE player_id_api = {list_id[0]} AND round = {round}{add_query}"
                                    )
                        elif data_types == 'penalty':
                            data = 1 if int(old_data) == 0 else int(data) + int(old_data)
                            insert_query = (
                                f" UPDATE players_round SET {data_types} = {data}, fixture_match = {fixture_match} WHERE player_id_api = {list_id[0]} AND round = {round}{add_query}"
                            )
                        else:
                            insert_query = (
                                f" UPDATE players_round SET {data_types} = {old_data} + {data} WHERE player_id_api = {list_id[i]} AND round = {round}{add_query}"
                            )
                    if insert_query != '':
                        insert_db(insert_query, f'UPDATE {players}')

                # create
                elif check_player(list_id[i], 'players_round', round, season, league_id, team_id) == False: 
                    if data_types == 'fast_goal':
                        insert_query = (
                            f" INSERT INTO players_round(player_id_api, name, {data_types}, fixture_match, season, league_id, team_id, round)"
                            f" VALUES ('{list_id[i]}', '{name}', '{list_amount[i]}', '{fixture_match}','{season}', '{league_id}', '{team_id}', '{round}')"
                        )
                    else:

                        insert_query = (
                            f" INSERT INTO players_round(player_id_api, name, {data_types}, season, league_id, team_id, round, fixture_match)"
                            f" VALUES ('{list_id[i]}', '{name}', '{list_amount[i]}', '{season}', '{league_id}', '{team_id}', '{round}', '{fixture_match}')"
                        )
                    insert_db(insert_query, 'add_player')
""""""
def update_teams(dict_list):
    team_id = dict_list["team_id"]
    name = dict_list["name"]

    season = dict_list["season"]
    league_id = dict_list["league_id"]
    rounds = dict_list['round']

    list_data = ['wins', 'loses', 'draws', 'clean_sheet_count', 'goals', 'without_scored_count', 'conceded_goals',
                 'conceded_goals_count', 'injuries_count']
    league_id = f"{league_id}"

    if league_id == '1':
        teams = 'teams_cup'
    elif league_id != '1':
        teams = 'teams_test'

    add_query = f" AND season = {season}"
    insert_query_for_check = f"SELECT team_id_api FROM {teams} WHERE team_id_api = {team_id}{add_query}"

    # update

    if chec_in_db(insert_query_for_check) == True:
        for i in range(len(list_data)):
            data = dict_list['list_data'][list_data[i]]  # 1
            data_name = list_data[i]  # wins

            # data_name = data_name[0]
            old_data = get_old_data(team_id, data_name, teams, '1', 'team_id_api', season)  # 22

            if data != '0':
                if old_data == '0':
                    insert_query = f" UPDATE {teams} SET {data_name} = {data} WHERE team_id_api = {team_id}{add_query}"

                elif old_data != '0':
                    insert_query = f" UPDATE {teams} SET {data_name} = {old_data} + {data} WHERE team_id_api = {team_id}{add_query}"

                insert_db(insert_query, 'update team')
        # create
    elif chec_in_db(insert_query_for_check) == False:
        d = dict_list['list_data']
        wins, loses, draws, clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count = \
        d['wins'], d['loses'], d['draws'], d['clean_sheet_count'], d['goals'], d['without_scored_count'], d[
            'conceded_goals'], d['conceded_goals_count'], d['injuries_count']

        insert_query = (
            f" INSERT INTO {teams}(team_id_api,wins, loses,draws,clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count,name, season, league_id)"
            f" VALUES ('{team_id}', '{wins}', '{loses}','{draws}','{clean_sheet_count}', '{goals}', '{without_scored_count}', '{conceded_goals}', '{conceded_goals_count}', '{injuries_count}','{name}', '{season}', '{league_id}')"
        )

        insert_db(insert_query, f'add {teams}')

    # FOR Rounds
    # update
    if league_id != '1':
        insert_query_for_check_round = f"SELECT team_id_api FROM teams_round WHERE team_id_api = {team_id} AND round = {rounds}{add_query}"
        if chec_in_db(insert_query_for_check_round) == True:
            for i in range(len(list_data)):
                data = dict_list['list_data'][list_data[i]]  # 1
                data_name = [list_data[i]]  # wins

                data_name = data_name[0]
                old_data = get_old_data(team_id, data_name, 'teams_round', rounds, 'team_id_api', season)  # 22

                if data != '0':
                    if old_data == '0':
                        insert_query = f" UPDATE teams_round SET {data_name} = {data} WHERE team_id_api = {team_id} AND round = {rounds}{add_query}"

                    elif old_data != '0':
                        insert_query = f" UPDATE teams_round SET {data_name} = {old_data} + {data} WHERE team_id_api = {team_id} AND round = {rounds}{add_query}"

                    insert_db(insert_query, 'update team round')
        # create
        elif chec_in_db(insert_query_for_check_round) == False:
            d = dict_list['list_data']
            wins, loses, draws, clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count = \
            d['wins'], d['loses'], d['draws'], d['clean_sheet_count'], d['goals'], d['without_scored_count'], d[
                'conceded_goals'], d['conceded_goals_count'], d['injuries_count']

            insert_query = (
                f" INSERT INTO teams_round(team_id_api,wins, loses,draws,clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count,name, season, league_id, round)"
                f" VALUES ('{team_id}', '{wins}', '{loses}','{draws}','{clean_sheet_count}', '{goals}', '{without_scored_count}', '{conceded_goals}', '{conceded_goals_count}', '{injuries_count}','{name}', '{season}', '{league_id}', '{rounds}')"
            )

            insert_db(insert_query, 'add team round')


def check_none(view):
    if view == None: view = 0
    return view


def team_update_destroyer(
        team_id, rounds, interceptions, blocks,
            saves, duels, shots_on_target, shots_of_target,
                tackles, precent_accuracy, league_id, season):

    league_id = f"{league_id}"
    if league_id != '1':
        teams = 'teams'
    else:
        teams = 'teams_cup'

    if team_id != '':

        destroyer_total = int(interceptions) + int(blocks) + int(saves) + int(tackles)

        creator_total = int(duels) + int(shots_on_target) + int(shots_of_target)

        old_destroyer_total = get_old_data(team_id, 'destroyer_total', teams, rounds, 'team_id_api', season)
        old_destroyer_total = check_none(old_destroyer_total)
        old_creator_total = get_old_data(team_id, 'creator_total', teams, rounds, 'team_id_api', season)
        old_creator_total = check_none(old_creator_total)
        old_interceptions = get_old_data(team_id, 'interceptions', teams, rounds, 'team_id_api', season)  # 22
        old_interceptions = check_none(old_interceptions)
        old_blocks = get_old_data(team_id, 'blocks', teams, rounds, 'team_id_api', season)  # 22
        old_blocks = check_none(old_blocks)
        old_saves = get_old_data(team_id, 'saves', teams, rounds, 'team_id_api', season)  # 22
        old_saves = check_none(old_saves)
        old_tackles = get_old_data(team_id, 'tackles', teams, rounds, 'team_id_api', season)  # 22
        old_tackles = check_none(old_tackles)
        old_duels = get_old_data(team_id, 'duels', teams, rounds, 'team_id_api', season)  # 22
        old_duels = check_none(old_duels)
        old_shots_on_target = get_old_data(team_id, 'shots_on_target', teams, rounds, 'team_id_api', season)  # 22
        old_shots_on_target = check_none(old_shots_on_target)
        old_shots_of_target = get_old_data(team_id, 'shots_of_target', teams, rounds, 'team_id_api', season)  # 22
        old_shots_of_target = check_none(old_shots_of_target)

        insert_query = f" UPDATE {teams} SET interceptions = {old_interceptions} + {interceptions}, blocks = {old_blocks} + {blocks}, saves = {old_saves} + {saves} , duels = {old_duels} + {duels}, shots_on_target = {old_shots_on_target} + {shots_on_target}, shots_of_target = {old_shots_of_target} + {shots_of_target}, tackles = {old_tackles} + {tackles}, destroyer_total = {old_destroyer_total} + {destroyer_total}, creator_total = {old_creator_total} + {creator_total} WHERE team_id_api = {team_id} AND season = {season}"
        insert_db(insert_query, 'update team')

        if league_id != '1':
            insert_query_round = f" UPDATE teams_round SET interceptions = {interceptions}, blocks = {blocks}, saves = {saves}, duels =  {duels}, shots_on_target = {shots_on_target}, shots_of_target = {shots_of_target}, tackles = {tackles}, destroyer_total = {destroyer_total}, creator_total = {creator_total} WHERE team_id_api = {team_id} AND round = {rounds} AND season = {season}"
            insert_db(insert_query_round, 'update team round')

            insert_query = f" UPDATE teams_round SET precent_accuracy = {precent_accuracy} WHERE team_id_api = {team_id} AND round = {rounds} AND season = {season}"
            insert_db(insert_query, 'add team')
        elif league_id == '1':
            insert_q = f"INSERT INTO teams_cup_round(precent_accuracy, team_id_api)" \
                       f"VALUES ('{precent_accuracy}', '{team_id}')"
            insert_db(insert_q, "teams_cup")


def insert_review_match_api(fixture_match):
    """ Делаем запрос в апи и записываем данные в бд """
    # Составы игравших команд
    # Общее количество blocks, duels, shots, possession
    # Blocked, duels, shots, possession

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"  # V3 - Fixtures
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_all = requests.get(url, headers=headers, params={
        "id": fixture_match
    })
    data_all = req_all.json()
    data_gen = req_all.json()
    
    if data_all['response'][0]['fixture']['status']['long'] != 'Match Postponed' and \
            data_all['response'][0]['fixture']['status']['long'] != 'Not Started' and \
            data_all['response'][0]['fixture']['status']['long'] != 'Time to be defined':

        date_match3 = data_gen['response'][0]['fixture']['date'][:10]
        date_match = data_gen['response'][0]['fixture']['date'][:16]
        d = f"{date_match[:10]}"
        date_match2 = d.replace("-", '')
        venue = data_gen['response'][0]['fixture']['venue']['name']
        id_team_home_review = data_all['response'][0]['teams']['home']['id']
        id_team_away_review = data_all['response'][0]['teams']['away']['id']
        season = data_gen['response'][0]['league']['season']
        league = data_gen['response'][0]['league']['id']
        league_id = data_gen['response'][0]['league']['id']
        league_name = data_gen['response'][0]['league']['name']
        country = data_gen['response'][0]['league']['country']

        # Сколько длился матч и сколько добавил рефери
        time_match = datetime.strptime(date_match, "%Y-%m-%dT%H:%M")
        date_now = datetime.now()
        match_lasted = date_now - time_match
        test_referee_time = match_lasted - timedelta(minutes=105)
        referee_time = str(test_referee_time)[2:]
        match_lasted = str(match_lasted)
        match_lasted = match_lasted.replace(':', '').replace('.', '').replace(' ', '').replace(',', '')

        if 'day' in match_lasted:
            match_lasted = int(match_lasted[8:])
        else:
            match_lasted = int(match_lasted)

        if league_name == "Premier League":
            league_name = country + " " + league_name

        round = data_gen['response'][0]['league']['round']
        if 'Regular Season - ' in round: round_main = str(round).replace("Regular Season - ", "")
        if 'Group Stage - ' in round: round_main = str(round).replace("Group Stage - ", "")
        if 'Round of ' in round: round_main = str(round).replace("Round of ", "")
        if 'Quarter-finals' in round or 'Semi-finals' in round: round_main = 1
        if '3rd Place Final' in round: round_main = 1
        if 'Final' in round: round_main = '1'
        if "Group" in round: round_main = round.split(" - ")[-1]
        else: round_main = str(round.split(" ")[-1])

        # Следующие матчи
        url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"  # V3 - Fixtures by team id
        req_next_match_home = requests.get(url, headers=headers, params={
            'league': league,
            "season": season,
            "team": id_team_home_review,
            "next": "30"
        })
        req_next_match_away = requests.get(url, headers=headers, params={
            'league': league,
            "season": season,
            "team": id_team_away_review,
            "next": "30"
        })
        data_next_match_home = req_next_match_home.json()
        data_next_match_away = req_next_match_away.json()

        # Ищу основную инфу прошлого матча

        insert_query_form = (
            f"SELECT form_home FROM match_review WHERE id_team_home_review={id_team_home_review}"
        )
        g = check_form(insert_query_form)

        insert_query_form = (
            f"SELECT form_away FROM match_review WHERE id_team_away_review={id_team_away_review}"
        )
        k = check_form(insert_query_form)

        name_home_review = data_all['response'][0]['teams']['home']['name']
        name_away_review = data_all['response'][0]['teams']['away']['name']
        goals_home = data_all['response'][0]['goals']['home']
        goals_away = data_all['response'][0]['goals']['away']

        # TODO МЫ СМОТРИМ БУДУЩИЕ МАТЧИ И МОЖЕТ БЫТЬ ОШИБКА, ЕСЛИ АПИ БУДЕТ ПУСТЫМ
        # Состав команд
        lineups_home = []
        lineups_away = []
        # range_lineups = len(data_all['response'][0]['lineups'][0]['startXI']) if len(data_all['response'][0]['lineups'][0]['startXI']) >= len(data_all['response'][0]['lineups'][1]['startXI']) else len(data_all['response'][0]['lineups'][1]['startXI'])
        # print(data_all['response'][0]['lineups'])
        if data_all['response'][0]['lineups']:
            if data_all['response'][0]['lineups'][0]['team']['name'] == name_home_review:
                if 'startXI' in data_all['response'][0]['lineups'][0]:
                    for line in range(len(data_all['response'][0]['lineups'][0]['startXI'])):
                        # TODO сделать проверку на нацинальность
                        dict_path = data_all['response'][0]['lineups'][0]['startXI'][line]['player']
                        if dict_path['id'] != None:
                            name = request_name_to_api(season, league_id, dict_path['id'], dict_path['name'])
                            lineups_home.append(name)
            else:
                if 'startXI' in data_all['response'][0]['lineups'][1]:
                    for line_2 in range(len(data_all['response'][0]['lineups'][1]['startXI'])):
                        dict_path = data_all['response'][0]['lineups'][1]['startXI'][line_2]['player']
                        if dict_path['id'] != None:
                            name = request_name_to_api(season, league_id, dict_path['id'], dict_path['name'])
                            lineups_home.append(name)

            if data_all['response'][0]['lineups'][0]['team']['name'] == name_away_review:
                if 'startXI' in data_all['response'][0]['lineups'][0]:
                    for line_3 in range(len(data_all['response'][0]['lineups'][0]['startXI'])):
                        dict_path = data_all['response'][0]['lineups'][0]['startXI'][line_3]['player']
                        if dict_path['id'] != None:
                            name = request_name_to_api(season, league_id, dict_path['id'], dict_path['name'])
                            lineups_away.append(name)
            else:
                if data_all['response'][0]['lineups'] and 1 in data_all['response'][0]['lineups']:
                    if 'startXI' in data_all['response'][0]['lineups'][1]:
                        for line_4 in range(len(data_all['response'][0]['lineups'][1]['startXI'])):
                            dict_path = data_all['response'][0]['lineups'][1]['startXI'][line_4]['player']
                            if dict_path['id'] != None:
                                name = request_name_to_api(season, league_id, dict_path['id'], dict_path['name'])
                                lineups_away.append(name)

        # Добавляем рейтинг
        if data_all['response'][0]['players'] != []:
            for rating_home in range(len(data_all['response'][0]['players'][0]['players'])):
                for rating_home2 in range(len(lineups_home)):
                    if lineups_home[rating_home2][3:] in \
                            request_name_to_api(season, league_id,
                                data_all['response'][0]['players'][0]['players'][rating_home]['player']['id'],
                                data_all['response'][0]['players'][0]['players'][rating_home]['player']['name']
                            ) and \
                            data_all['response'][0]['players'][0]['players'][rating_home]['statistics'][0]['games']['rating'] != None:

                        lineups_home[rating_home2] += ' (' + \
                                                      data_all['response'][0]['players'][0]['players'][rating_home]['statistics'][0]['games']['rating'] \
                                                      + ')'

                    elif lineups_home[rating_home2][3:] in \
                            request_name_to_api(season, league_id,
                                data_all['response'][0]['players'][0]['players'][rating_home]['player']['id'],
                                data_all['response'][0]['players'][0]['players'][rating_home]['player']['name']
                            ) \
                            and data_all['response'][0]['players'][0]['players'][rating_home]['statistics'][0]['games']['rating'] == None:

                        lineups_home[rating_home2] += ' (0)'

            for rating_away in range(len(data_all['response'][0]['players'][1]['players'])):
                for rating_away2 in range(len(lineups_away)):
                    if lineups_away[rating_away2][3:] in \
                            request_name_to_api(season, league_id,
                                data_all['response'][0]['players'][1]['players'][rating_away]['player']['id'],
                                data_all['response'][0]['players'][1]['players'][rating_away]['player']['name']
                            ) and \
                            data_all['response'][0]['players'][1]['players'][rating_away]['statistics'][0]['games'][
                                'rating'] != None:
                        lineups_away[rating_away2] += ' (' + \
                                                      data_all['response'][0]['players'][1]['players'][rating_away][
                                                          'statistics'][0]['games']['rating'] + ')'
                    elif lineups_away[rating_away2][3:] in \
                            request_name_to_api(season, league_id,
                                data_all['response'][0]['players'][1]['players'][rating_away]['player']['id'],
                                data_all['response'][0]['players'][1]['players'][rating_away]['player']['name']
                            ) \
                            and data_all['response'][0]['players'][1]['players'][rating_away]['statistics'][0]['games']['rating'] == None:

                        lineups_away[rating_away2] += ' (0)'

        # Заменили кого и на какой минуте
        gone_player_home = []
        gone_player_away = []
        came_player_home = []
        came_player_away = []
        time_subst_home = []
        time_subst_away = []
        for substitutes in range(len(data_all['response'][0]['events'])):
            if data_all['response'][0]['events'][substitutes]['type'] == 'subst' and \
                    data_all['response'][0]['events'][substitutes]['team']['name'] == name_home_review and \
                    data_all['response'][0]['events'][substitutes]['player']['id'] != None:

                gone_player_home.append(request_name_to_api(
                    season, league_id, data_all['response'][0]['events'][substitutes]['player']['id'], data_all['response'][0]['events'][substitutes]['player']['name']))

                if data_all['response'][0]['events'][substitutes]['assist']["id"] != None:
                    came_player_home.append(request_name_to_api(
                        season, league_id, data_all['response'][0]['events'][substitutes]['assist']['id'], data_all['response'][0]['events'][substitutes]['assist']['name']))
                    time_subst_home.append(str(data_all['response'][0]['events'][substitutes]['time']['elapsed']))
            elif data_all['response'][0]['events'][substitutes]['type'] == 'subst' and \
                    data_all['response'][0]['events'][substitutes]['team']['name'] == name_away_review and \
                    data_all['response'][0]['events'][substitutes]['player']['id'] != None:

                gone_player_away.append(
                    request_name_to_api(season, league_id, data_all['response'][0]['events'][substitutes]['player']['id'], data_all['response'][0]['events'][substitutes]['player']['name']))

                if data_all['response'][0]['events'][substitutes]['assist']["id"] != None:
                    came_player_away.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['events'][substitutes]['assist']['id'], data_all['response'][0]['events'][substitutes]['assist']['name']))
                    time_subst_away.append(str(data_all['response'][0]['events'][substitutes]['time']['elapsed']))

        # Имена тех, кто забил и на какой минуте
        events_index = len(data_all['response'][0]['events'])

        # Ищу голы
        time_home_goal = []
        player_home_goal = []
        player_home_id_goal = []
        time_away_goal = []
        player_away_goal = []
        player_away_id_goal = []

        # Ищу карточки за нарушения
        time_home_yellow = []
        player_home_yellow = []
        time_away_yellow = []
        player_away_yellow = []

        time_home_red = []
        player_home_red = []
        time_away_red = []
        player_away_red = []

        player_home_penalti = []
        time_home_penalti = []
        player_home_id_penalti = []

        player_away_penalti = []
        time_away_penalti = []
        player_away_id_penalti = []

        count_yel_card = 0
        count_red_card = 0


        check_ghana =  False
        index = 0
        if events_index >= 1:
            while index != events_index:
                if data_all['response'][0]['events'][index]['player']['id'] != None:

                    events = data_all['response'][0]['events'][index]['type']


                    """ goals: """
                    if events == 'Goal' and data_all['response'][0]['events'][index]['team']['name'] == name_home_review \
                            and data_all['response'][0]['events'][index]['detail'] != "Missed Penalty":

                        time_home_goal.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_home_goal.append(request_name_to_api(season, league_id, str(data_all['response'][0]['events'][index]['player']['id']), str(data_all['response'][0]['events'][index]['player']['name'])))
                        player_home_id_goal.append(str(data_all['response'][0]['events'][index]['player']['id']))

                    elif events == 'Goal' and data_all['response'][0]['events'][index]['team']['name'] == name_away_review \
                            and data_all['response'][0]['events'][index]['detail'] != "Missed Penalty":

                        time_away_goal.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_away_goal.append(request_name_to_api(season, league_id, str(data_all['response'][0]['events'][index]['player']['id']), str(data_all['response'][0]['events'][index]['player']['name'])))
                        player_away_id_goal.append(str(data_all['response'][0]['events'][index]['player']['id']))


                    """ cards: """
                    if events == 'Card' and data_all['response'][0]['events'][index]['team']['name'] == name_home_review \
                            and data_all['response'][0]['events'][index]['detail'] == 'Yellow Card':
                        time_home_yellow.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_home_yellow.append(
                            request_name_to_api(season, league_id,
                                          data_all['response'][0]['events'][index]['player']['id'],
                                          data_all['response'][0]['events'][index]['player']['name']
                            )
                        )
                        count_yel_card += 1
                    elif events == 'Card' and data_all['response'][0]['events'][index]['team']['name'] == name_away_review \
                            and data_all['response'][0]['events'][index]['detail'] == 'Yellow Card':
                        time_away_yellow.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_away_yellow.append(request_name_to_api(season, league_id, str(data_all['response'][0]['events'][index]['player']['id']), str(data_all['response'][0]['events'][index]['player']['name'])))
                        count_yel_card += 1
                    elif events == 'Card' and data_all['response'][0]['events'][index]['team']['name'] == name_home_review \
                            and data_all['response'][0]['events'][index]['detail'] == 'Red Card':
                        time_home_red.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_home_red.append(request_name_to_api(season, league_id, str(data_all['response'][0]['events'][index]['player']['id']), str(data_all['response'][0]['events'][index]['player']['name'])))
                        count_red_card += 1
                    elif events == 'Card' and data_all['response'][0]['events'][index]['team']['name'] == name_away_review \
                            and data_all['response'][0]['events'][index]['detail'] == 'Red Card':
                        time_away_red.append(str(data_all['response'][0]['events'][index]['time']['elapsed']))
                        player_away_red.append(request_name_to_api(season, league_id, str(data_all['response'][0]['events'][index]['player']['id']), str(data_all['response'][0]['events'][index]['player']['name'])))
                        count_red_card += 1

                index += 1
        total_cards_in_game = count_yel_card + count_red_card
        index22 = 0
        total_count_penalty = 0
        if events_index >= 1:
            while index22 != events_index:
                events = data_all['response'][0]['events'][index22]['type']
                
                # Initialize default values
                player_id = "None"
                player_name = ""
                time_elapsed = "0"
                
                # Get player data if available
                if ('player' in data_all['response'][0]['events'][index22] and 
                    data_all['response'][0]['events'][index22]['player'] and 
                    'id' in data_all['response'][0]['events'][index22]['player']):
                    player_id = data_all['response'][0]['events'][index22]['player']['id']
                    player_name = data_all['response'][0]['events'][index22]['player']['name']
                
                # Get time if available
                if ('time' in data_all['response'][0]['events'][index22] and 
                    data_all['response'][0]['events'][index22]['time'] and 
                    'elapsed' in data_all['response'][0]['events'][index22]['time']):
                    time_elapsed = str(data_all['response'][0]['events'][index22]['time']['elapsed'])

                if events == 'Goal' and data_all['response'][0]['events'][index22]['team']['name'] == name_home_review \
                        and data_all['response'][0]['events'][index22]['detail'] == 'Penalty':
                    time_home_penalti.append(time_elapsed)
                    player_home_id_penalti.append(str(player_id) if player_id else "0")
                    if player_id:
                        player_name = request_name_to_api(season, league_id, player_id, player_name)
                    player_home_penalti.append(player_name)
                    total_count_penalty += 1
                elif events == 'Goal' and data_all['response'][0]['events'][index22]['team']['name'] == name_away_review \
                        and data_all['response'][0]['events'][index22]['detail'] == 'Penalty':
                    time_away_penalti.append(time_elapsed)
                    player_away_id_penalti.append(str(player_id) if player_id else "0")
                    if player_id:
                        player_name = request_name_to_api(season, league_id, player_id, player_name)
                    player_away_penalti.append(player_name)
                    total_count_penalty += 1

                index22 += 1

        total_count_penalty_list = ['1' for i in range(total_count_penalty)]
        fаst_name_goal = []
        time_fast_goal = []
        fast_id_player = []
        type_team_fast_goal = ''
        index = 0

        if time_home_goal != [] and time_away_goal != []:
            if int(time_home_goal[0]) < int(time_away_goal[0]):
                fаst_name_goal.append(player_home_goal[0])
                time_fast_goal.append(int(time_home_goal[0]))
                fast_id_player.append(player_home_id_goal[0])
                type_team_fast_goal = 'home'

            elif int(time_home_goal[0]) > int(time_away_goal[0]):
                fаst_name_goal.append(player_away_goal[0])
                time_fast_goal.append(int(time_away_goal[0]))
                fast_id_player.append(player_away_id_goal[0])
                type_team_fast_goal = 'away'

        elif time_home_goal != [] and time_away_goal == []:
            fаst_name_goal.append(player_home_goal[0])
            time_fast_goal.append(int(time_home_goal[0]))
            fast_id_player.append(player_home_id_goal[0])
            type_team_fast_goal = 'home'

        elif time_home_goal == [] and time_away_goal != []:
            fаst_name_goal.append(player_away_goal[0])
            time_fast_goal.append(int(time_away_goal[0]))
            fast_id_player.append(player_away_id_goal[0])
            type_team_fast_goal = 'away'
        else:
            pass

        # Голы для суммирования в превью
        name_home_top_goals = ''
        amount_home_goals = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_goals_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_goals_player]['statistics'][0]['goals'][
                    'total'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_goals_player]['statistics'][0][
                            'goals']['total'] > amount_home_goals:
                    amount_home_goals = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_goals_player]['statistics'][0]['goals'][
                        'total']
                    name_home_top_goals = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_goals_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_goals_player]['player']['name'])

        name_away_top_goals = ''
        amount_away_goals = 0
        if data_all['response'][0]['players'] != []:
            for find_away_top_goals_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_goals_player]['statistics'][0]['goals'][
                    'total'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_goals_player]['statistics'][0][
                            'goals']['total'] > amount_away_goals:
                    amount_away_goals = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_goals_player]['statistics'][0]['goals'][
                        'total']
                    name_away_top_goals = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_goals_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_goals_player]['player']['name'])

        # Ассисты для суммирования в превью
        name_home_top_assists = ''
        amount_home_assists = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_assists_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0]['goals'][
                    'assists'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0][
                            'goals']['assists'] > amount_home_assists:
                    amount_home_assists = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_assists_player]['statistics'][0][
                        'goals']['assists']
                    name_home_top_assists = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_assists_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_assists_player]['player']['name'])

        name_away_top_assists = ''
        amount_away_assists = 0
        if data_all['response'][0]['players'] != []:
            for find_away_top_assists_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0]['goals'][
                    'assists'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0][
                            'goals']['assists'] > amount_away_assists:
                    amount_away_assists = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_assists_player]['statistics'][0][
                        'goals']['assists']
                    name_away_top_assists = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_assists_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_assists_player]['player']['name'])

        # Сейвы для суммирования в превью
        name_home_top_saves = ''
        amount_home_saves = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_saves_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_saves_player]['statistics'][0]['goals'][
                    'saves'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_saves_player]['statistics'][0][
                            'goals']['saves'] > amount_home_saves:
                    amount_home_saves = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_saves_player]['statistics'][0]['goals'][
                        'saves']
                    name_home_top_saves = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_saves_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_saves_player]['player']['name'])

        name_away_top_saves = ''
        amount_away_saves = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_saves_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_saves_player]['statistics'][0]['goals'][
                    'saves'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_saves_player]['statistics'][0][
                            'goals']['saves'] > amount_away_saves:
                    amount_away_saves = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_saves_player]['statistics'][0]['goals'][
                        'saves']
                    name_away_top_saves = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_saves_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_saves_player]['player']['name'])

        amount_home_saves3 = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_saves_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0]['goals'][
                    'saves'] != None:
                    amount_home_saves3 += \
                    data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0]['goals'][
                        'saves']

        amount_away_saves3 = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_saves_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0]['goals'][
                    'saves']:
                    amount_away_saves3 += \
                    data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0]['goals'][
                        'saves']

        # #Фолы для суммирования в превью
        # name_home_top_fouls = ''
        # amount_home_fouls = 0
        # for find_home_top_fouls_player in range(len(data_all['response'][0]['players'][0]['players'])):
        #     if data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
        #     data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed'] > amount_home_fouls:
        #         amount_home_fouls = data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['fouls']['committed']
        #         name_home_top_fouls = data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['name']

        # name_away_top_fouls = ''
        # amount_away_fouls = 0
        # for find_away_top_fouls_player in range(len(data_all['response'][0]['players'][1]['players'])):
        #     if data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] != None and \
        #     data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed'] > amount_away_fouls:
        #         amount_away_fouls = data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['fouls']['committed']
        #         name_away_top_fouls = data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['name']

        # Фолы для суммирования в превью
        name_home_top_fouls_yel_card = ''
        amount_home_fouls_yel_card = 0
        name_home_top_fouls_red_card = ''
        amount_home_fouls_red_card = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_fouls_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['cards'][
                    'yellow'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0][
                            'cards']['yellow'] > amount_home_fouls_yel_card:
                    amount_home_fouls_yel_card = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['cards'][
                        'yellow']
                    name_home_top_fouls_yel_card = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['name'])
                if data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['cards'][
                    'red'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0][
                            'cards']['red'] > amount_home_fouls_red_card:
                    amount_home_fouls_red_card = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['statistics'][0]['cards'][
                        'red']
                    name_home_top_fouls_red_card = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player]['player']['name'])

        name_away_top_fouls_yel_card = ''
        amount_away_fouls_yel_card = 0
        name_away_top_fouls_red_card = ''
        amount_away_fouls_red_card = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_fouls_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['cards'][
                    'yellow'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0][
                            'cards']['yellow'] > amount_away_fouls_yel_card:
                    amount_away_fouls_yel_card = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['cards'][
                        'yellow']
                    name_away_top_fouls_yel_card = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['name'])
                if data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['cards'][
                    'red'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0][
                            'cards']['red'] > amount_away_fouls_red_card:
                    amount_away_fouls_red_card = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['statistics'][0]['cards'][
                        'red']
                    name_away_top_fouls_red_card = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player]['player']['name'])

        # Сколько нанесли ударов в створ и по воротам
        # HOME
        # Команда HOME нанесла ударов по воротам
        shots_on_goal_home = 0
        shots_off_goal_home = 0

        if data_all['response'][0]['statistics'] != []:
            shots_on_goal_home = data_all['response'][0]['statistics'][0]['statistics'][0]['value']
            if shots_on_goal_home == None:
                shots_on_goal_home = 0

            # Команда HOME нанесла ударов в створ (удары в сторону)
            shots_off_goal_home = data_all['response'][0]['statistics'][0]['statistics'][2]['value']
            if shots_off_goal_home == None:
                shots_off_goal_home = 0

        # Ищу лучшего по ударам HOME
        name_home_top_shots = ''
        amount_home_shots = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_shots_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_shots_player]['statistics'][0]['shots'][
                    'total'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_shots_player]['statistics'][0][
                            'shots']['total'] > amount_home_shots:
                    amount_home_shots = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_shots_player]['statistics'][0]['shots'][
                        'total']
                    name_home_top_shots = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_shots_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_shots_player]['player']['name'])

        # AWAY
        # Команда AWAY нанесла ударов по воротам
        shots_on_goal_away = 0
        shots_off_goal_away = 0
        if data_all['response'][0]['statistics'] != []:

            shots_on_goal_away = data_all['response'][0]['statistics'][1]['statistics'][0]['value']
            if shots_on_goal_away == None:
                shots_on_goal_away = 0

            # Команда AWAY нанесла ударов в створ (удары в сторону)
            shots_off_goal_away = data_all['response'][0]['statistics'][1]['statistics'][2]['value']
            if shots_off_goal_away == None:
                shots_off_goal_away = 0

        # Ищу лучшего по ударам AWAY
        name_away_top_shots = ''
        amount_away_shots = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_shots_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_home_top_shots_player]['statistics'][0]['shots'][
                    'total'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_home_top_shots_player]['statistics'][0][
                            'shots']['total'] > amount_away_shots:
                    amount_away_shots = \
                    data_all['response'][0]['players'][1]['players'][find_home_top_shots_player]['statistics'][0]['shots'][
                        'total']
                    name_away_top_shots = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_home_top_shots_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_home_top_shots_player]['player']['name'])

        # Считаю общее количество голевых моментов (ассистов)
        # HOME
        total_assists_home = 0
        if data_all['response'][0]['players'] != []:
            for find_home_amount_assists in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_amount_assists]['statistics'][0]['goals'][
                    'assists'] != None:
                    total_assists_home = \
                    data_all['response'][0]['players'][0]['players'][find_home_amount_assists]['statistics'][0]['goals'][
                        'assists'] + total_assists_home

        # AWAY
        total_assists_away = 0
        if data_all['response'][0]['players'] != []:
            for find_away_amount_assists in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_amount_assists]['statistics'][0]['goals'][
                    'assists'] != None:
                    total_assists_away = \
                    data_all['response'][0]['players'][1]['players'][find_away_amount_assists]['statistics'][0]['goals'][
                        'assists'] + total_assists_away

        # Общее количество ударов у команды №
        total_shots_home, total_shots_away = 0, 0
        if data_all['response'][0]['statistics'] != []:

            total_shots_home = data_all['response'][0]['statistics'][0]['statistics'][2]['value']
            total_shots_away = data_all['response'][0]['statistics'][1]['statistics'][2]['value']
            if total_shots_home == None:
                total_shots_home = 0
            if total_shots_away == None:
                total_shots_away = 0
        # Общее количество ударов в игре
        total_shots_on = shots_on_goal_home + shots_on_goal_away
        total_shots_off = shots_off_goal_home + shots_off_goal_away

        # Количество отборов и перехватов (blocks and interceptions)
        # BLOCKS
        # HOME
        # Общее количество блоков HOME
        total_blocks_home = 0
        if data_all['response'][0]['players'] != []:
            for find_home_amount_blocks in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_amount_blocks]['statistics'][0]['tackles'][
                    'blocks'] != None:
                    total_blocks_home = \
                    data_all['response'][0]['players'][0]['players'][find_home_amount_blocks]['statistics'][0]['tackles'][
                        'blocks'] + total_blocks_home
        # if data_all['response'][0]['statistics'][0]['statistics'][3]['value'] == None:
        #     total_blocks_home = 0
        # else:
        #     total_blocks_home = data_all['response'][0]['statistics'][0]['statistics'][3]['value']

        name_home_top_block = ''
        amount_home_block = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_block_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_block_player]['statistics'][0]['tackles'][
                    'blocks'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_block_player]['statistics'][0][
                            'tackles']['blocks'] > amount_home_block:
                    amount_home_block = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_block_player]['statistics'][0][
                        'tackles']['blocks']
                    name_home_top_block = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_block_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_block_player]['player']['name'])

        # AWAY
        # Общее количество блоков AWAY
        total_blocks_away = 0
        if data_all['response'][0]['players'] != []:

            for find_away_amount_blocks in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_amount_blocks]['statistics'][0]['tackles'][
                    'blocks'] != None:
                    total_blocks_away = \
                    data_all['response'][0]['players'][1]['players'][find_away_amount_blocks]['statistics'][0]['tackles'][
                        'blocks'] + total_blocks_away

        # if data_all['response'][0]['statistics'][1]['statistics'][3]['value'] == None:
        #     total_blocks_away = 0
        # else:
        #     total_blocks_away = data_all['response'][0]['statistics'][1]['statistics'][3]['value']

        name_away_top_block = ''
        amount_away_block = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_block_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_block_player]['statistics'][0]['tackles'][
                    'blocks'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_block_player]['statistics'][0][
                            'tackles']['blocks'] > amount_away_block:
                    amount_away_block = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_block_player]['statistics'][0][
                        'tackles']['blocks']
                    name_away_top_block = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_block_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_block_player]['player']['name'])
        # print(name_away_top_block, amount_away_block)

        # INTERCEPTIONS
        # HOME
        # Общее количество перехватов HOME
        total_interceptions_home = 0
        if data_all['response'][0]['players'] != []:

            for find_home_amount_interceptions in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_amount_interceptions]['statistics'][0][
                    'tackles']['interceptions'] != None:
                    total_interceptions_home = \
                    data_all['response'][0]['players'][0]['players'][find_home_amount_interceptions]['statistics'][0][
                        'tackles']['interceptions'] + total_interceptions_home

        # Ищу лучшего игрока по перехватам HOME
        name_home_top_interceptions = ''
        amount_home_interceptions = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_interceptions_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player]['statistics'][0][
                    'tackles']['interceptions'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player]['statistics'][
                            0]['tackles']['interceptions'] > amount_home_interceptions:
                    amount_home_interceptions = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player]['statistics'][0][
                        'tackles']['interceptions']
                    name_home_top_interceptions = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player]['player']['name'])

        # AWAY
        # Общее количество перехватов AWAY
        total_interceptions_away = 0
        if data_all['response'][0]['players'] != []:

            for find_away_amount_interceptions in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_amount_interceptions]['statistics'][0][
                    'tackles']['interceptions'] != None:
                    total_interceptions_away = \
                    data_all['response'][0]['players'][1]['players'][find_away_amount_interceptions]['statistics'][0][
                        'tackles']['interceptions'] + total_interceptions_away

        # Ищу лучшего игрока по перехватам AWAY
        name_away_top_interceptions = ''
        amount_away_interceptions = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_interceptions_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player]['statistics'][0][
                    'tackles']['interceptions'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player]['statistics'][
                            0]['tackles']['interceptions'] > amount_away_interceptions:
                    amount_away_interceptions = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player]['statistics'][0][
                        'tackles']['interceptions']
                    name_away_top_interceptions = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player]['player']['name'])

        # Процент ведения мячом
        ball_possession_home = 0
        ball_possession_away = 0
        if data_all['response'][0]['statistics'] != []:

            ball_possession_home = data_all['response'][0]['statistics'][0]['statistics'][9]['value']
            ball_possession_away = data_all['response'][0]['statistics'][1]['statistics'][9]['value']

        # Единоборства
        # HOME
        name_home_top_duels = ''
        amount_home_duels = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_duel_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_duel_player]['statistics'][0]['duels'][
                    'won'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_duel_player]['statistics'][0][
                            'duels']['won'] > amount_home_duels:
                    amount_home_duels = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_duel_player]['statistics'][0]['duels'][
                        'won']
                    name_home_top_duels = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_duel_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_duel_player]['player']['name'])

        # AWAY
        name_away_top_duels = ''
        amount_away_duels = 0
        if data_all['response'][0]['players'] != []:
            for find_away_top_duel_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_duel_player]['statistics'][0]['duels'][
                    'won'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_duel_player]['statistics'][0][
                            'duels']['won'] > amount_away_duels:
                    amount_away_duels = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_duel_player]['statistics'][0]['duels'][
                        'won']
                    name_away_top_duels = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_duel_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_duel_player]['player']['name'])
        # print(fixture_match)
        # print(data_all['response'][0]['players'][0]['players'][12]['statistics'][0]['passes']['accuracy'])
        # Passes
        # HOME
        name_home_top_pass_accuracy = ''
        top__home_total_accuracy = 0
        top__home_total_passes = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_pass_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['statistics'][0]['passes'][
                    'accuracy'] != None and \
                        int(data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['statistics'][0][
                                'passes']['accuracy']) > top__home_total_accuracy:
                    top__home_total_accuracy = int(
                        data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['statistics'][0][
                            'passes']['accuracy'])
                    top__home_total_passes = \
                    data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['statistics'][0]['passes'][
                        'total']
                    name_home_top_pass_accuracy = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_pass_player]['player']['name'])

        # total_num_home = int(top__home_total_passes - top__home_total_accuracy)
        top__home_precent_accuracy = 0
        try:
            top__home_precent_accuracy = int(100 * top__home_total_accuracy // top__home_total_passes)
        except: ...
        # AWAY
        name_away_top_pass_accuracy = ''
        top__away_total_accuracy = 0
        top__away_total_passes = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_pass_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['statistics'][0]['passes'][
                    'accuracy'] != None and \
                        int(data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['statistics'][0][
                                'passes']['accuracy']) > top__away_total_accuracy:
                    top__away_total_accuracy = int(
                        data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['statistics'][0][
                            'passes']['accuracy'])
                    top__away_total_passes = \
                    data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['statistics'][0]['passes'][
                        'total']
                    name_away_top_pass_accuracy = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_pass_player]['player']['name'])
        # total_num_away = int(top__away_total_passes - top__away_total_accuracy)
        top__away_precent_accuracy = 0
        try:
            top__away_precent_accuracy = int(100 * top__away_total_accuracy // top__away_total_passes)
        except: ...

        top__home_precent_accuracy = str(top__home_precent_accuracy)
        top__away_precent_accuracy = str(top__away_precent_accuracy)

        # Passes KEY
        # HOME
        name_home_top_pass_key = ''
        top__home_amount_key = 0
        if data_all['response'][0]['players'] != []:

            for find_home_top_key_player in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_key_player]['statistics'][0]['passes'][
                    'key'] != None and \
                        int(data_all['response'][0]['players'][0]['players'][find_home_top_key_player]['statistics'][0][
                                'passes']['key']) > top__home_amount_key:
                    top__home_amount_key = int(
                        data_all['response'][0]['players'][0]['players'][find_home_top_key_player]['statistics'][0][
                            'passes']['key'])
                    name_home_top_pass_key = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_key_player]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_key_player]['player']['name'])

        # AWAY
        name_away_top_pass_key = ''
        top__away_amount_key = 0
        if data_all['response'][0]['players'] != []:

            for find_away_top_key_player in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_key_player]['statistics'][0]['passes'][
                    'key'] != None and \
                        int(data_all['response'][0]['players'][1]['players'][find_away_top_key_player]['statistics'][0][
                                'passes']['key']) > top__away_amount_key:
                    top__away_amount_key = int(
                        data_all['response'][0]['players'][1]['players'][find_away_top_key_player]['statistics'][0][
                            'passes']['key'])
                    name_away_top_pass_key = \
                    request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_key_player]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_key_player]['player']['name'])

        team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes = 0, 0, 0, 0, 0, 0

        if data_all['response'][0]['statistics'] != []:

            team_home_passes_accurate = int(data_all['response'][0]['statistics'][0]['statistics'][14]['value'] or 0)
            team_away_passes_accurate = int(data_all['response'][0]['statistics'][1]['statistics'][14]['value'] or 0)
        # print(data_all['response'][0]['statistics'][0]['statistics'][15])
            team_home_percent_passes_accurate = int((data_all['response'][0]['statistics'][0]['statistics'][15]['value'] or "0").replace("%", ""))
            team_away_percent_passes_accurate = int((data_all['response'][0]['statistics'][1]['statistics'][15]['value'] or "0").replace("%", ""))
            team_home_total_passes = int(data_all['response'][0]['statistics'][0]['statistics'][13]['value'] or 0)
            team_away_total_passes = int(data_all['response'][0]['statistics'][1]['statistics'][13]['value'] or 0)

        # FOR TEAMS

        without_score_home = 0
        without_score_away = 0
        if goals_home == 0:
            without_score_home = 1
        elif goals_away == 0:
            without_score_away = 1

        win_team_home = 0
        win_team_away = 0
        lose_team_home = 0
        lose_team_away = 0
        draw_team_home = 0
        draw_team_away = 0
        if goals_home > goals_away:
            win_team_home = 1
            lose_team_away = 1
        elif goals_home < goals_away:
            win_team_away = 1
            lose_team_home = 1
        elif goals_home == goals_away:
            draw_team_home = 1
            draw_team_away = 1

        clean_sheet_home = 0
        clean_sheet_away = 0
        if goals_home == 0 and goals_away == 0:
            clean_sheet_home = 1
            clean_sheet_away = 1

        conceded_score_home = 0
        conceded_score_away = 0
        if goals_home != 0:
            conceded_score_away = 1
        if goals_away != 0:
            conceded_score_home = 1

        # TODO МЫ СМОТРИМ БУДУЩИЕ МАТЧИ И МОЖЕТ БЫТЬ ОШИБКА, ЕСЛИ АПИ БУДЕТ ПУСТЫМ
        # Следующий матч
        # HOME
        home_next_match_rival = ''
        home_date_match_vs_rival = ''
        home_next_venue_vs_rival = ""
        #Если команда принимает дома, то путь такой, иначе...
        if data_next_match_home['results'] != 0:
            if data_next_match_home['response'][0]['teams']['away']['name'] != name_home_review:
                home_next_match_rival = data_next_match_home['response'][0]['teams']['away']['name']
            else:
                home_next_match_rival = data_next_match_home['response'][0]['teams']['home']['name']

            home_date_match_vs_rival = data_next_match_home['response'][0]['fixture']['date'][:16]
            home_next_venue_vs_rival = data_next_match_home['response'][0]['fixture']['venue']['name']  # TODO API в первых матчах арену может не видеть и выводить None, косяк API

        # AWAY
        away_next_match_rival = ''
        away_date_match_vs_rival = ''
        away_venue_vs_rival = ''
        #Если команда принимает дома, то путь такой, иначе...
        if data_next_match_away['results'] != 0:
            if data_next_match_away['response'][0]['teams']['away']['name'] != name_away_review:
                away_next_match_rival = data_next_match_away['response'][0]['teams']['away']['name']
            else:
                away_next_match_rival = data_next_match_away['response'][0]['teams']['home']['name']

            away_date_match_vs_rival = data_next_match_away['response'][0]['fixture']['date'][:16]
            away_venue_vs_rival = data_next_match_away['response'][0]['fixture']['venue'][
                'name']  # TODO API в первых матчах арену может не видеть и выводить None, косяк API

        # Травмы
        url = os.getenv('RAPID_API_BASE_URL')+"/injuries"

        req_injuries = requests.request("GET", url, headers=headers, params={
            "fixture": fixture_match
        })

        data_injuries = req_injuries.json()

        player_id_injuries = []
        player_name_injuries = []
        amount_injuries = []
        count_home_injuries = 0
        count_away_injuries = 0
        for injuries in range(len(data_injuries['response'])):
            player_id_injuries.append(data_injuries['response'][injuries]['player']['id'])
            player_name_injuries.append(request_name_to_api(season, league_id, data_injuries['response'][injuries]['player']['id'], data_injuries['response'][injuries]['player']['name']))
            amount_injuries.append('1')

        for injuries_team in range(len(data_injuries['response'])):
            if data_injuries['response'][injuries_team]['team']['name'] == name_home_review:
                count_home_injuries += 1
            elif data_injuries['response'][injuries_team]['team']['name'] == name_away_review:
                count_away_injuries += 1

        injuries_count = len(data_injuries['response'])

        # Подумать в какое бд засунуть этот параметр

        url = os.getenv('RAPID_API_BASE_URL')+"/standings"  # V3 - Standings by league id

        req_rank = requests.request("GET", url, headers=headers, params={
            "season": season,
            "league": league
        })

        data_rank = req_rank.json()

        rank_for_table = []
        name_table_team = []
        form_table = []
        all_matches_table = []
        win_matches_table = []
        draw_matches_table = []
        lose_matches_table = []
        goals_scored_for_table = []
        goals_missed_for_table = []
        goals_diff_table = []
        points_for_table = []
        logo_for_table = []

        if data_rank['response']:
            for find_rank in range(len(data_rank['response'][0]['league']['standings'][0])):
                rank_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['rank']))
                name_table_team.append(data_rank['response'][0]['league']['standings'][0][find_rank]['team']['name'])
                form_table.append(data_rank['response'][0]['league']['standings'][0][find_rank]['form'])
                all_matches_table.append(
                    str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['played']))
                win_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['win']))
                draw_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['draw']))
                lose_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['lose']))
                goals_scored_for_table.append(
                    str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['goals']['for']))
                goals_missed_for_table.append(
                    str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['goals']['against']))
                goals_diff_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['goalsDiff']))
                points_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['points']))
                logo_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['team']['logo']))

        name_home_top_goals2 = []
        amount_home_goals2 = []
        id_goals_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_goals_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['statistics'][0]['goals'][
                    'total'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['statistics'][0][
                            'goals']['total'] > 0:
                    amount_home_goals2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['statistics'][0][
                            'goals']['total']))
                    name_home_top_goals2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['player']['name']))
                    id_goals_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_goals_player2]['player']['id'])

        name_away_top_goals2 = []
        amount_away_goals2 = []
        id_goals_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_goals_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['statistics'][0]['goals'][
                    'total'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['statistics'][0][
                            'goals']['total'] > 0:
                    amount_away_goals2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['statistics'][0][
                            'goals']['total']))
                    id_goals_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['player']['id'])
                    name_away_top_goals2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_goals_player2]['player']['name']))

        name_home_top_assists2 = []
        amount_home_assists2 = []
        id_assists_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_assists_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if \
                data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['statistics'][0]['goals'][
                    'assists'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['statistics'][0][
                            'goals']['assists'] > 0:
                    amount_home_assists2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['statistics'][0][
                            'goals']['assists']))
                    name_home_top_assists2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['player']['name']))
                    id_assists_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_assists_player2]['player']['id'])

        name_away_top_assists2 = []
        amount_away_assists2 = []
        id_assists_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_assists_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if \
                data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['statistics'][0]['goals'][
                    'assists'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['statistics'][0][
                            'goals']['assists'] > 0:
                    amount_away_assists2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['statistics'][0][
                            'goals']['assists']))
                    name_away_top_assists2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['player']['name']))
                    id_assists_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_assists_player2]['player']['id'])

        name_home_top_saves2 = []
        amount_home_saves2 = []
        id_saves_home_players2 = []
        count_home_conceded = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_saves_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0]['goals'][
                    'conceded'] != None:
                    count_home_conceded += \
                    data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0]['goals'][
                        'conceded']
                if data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0]['goals'][
                    'saves'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0][
                            'goals']['saves'] > 0:
                    amount_home_saves2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['statistics'][0][
                            'goals']['saves']))
                    name_home_top_saves2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['player']['name']))
                    id_saves_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_saves_player2]['player']['id'])

        name_away_top_saves2 = []
        amount_away_saves2 = []
        id_saves_away_players2 = []
        count_away_conceded = 0
        if data_all['response'][0]['players'] != []:
            for find_away_top_saves_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0]['goals'][
                    'conceded'] != None:
                    count_away_conceded += \
                    data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0]['goals'][
                        'conceded']
                if data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0]['goals'][
                    'saves'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0][
                            'goals']['saves'] > 0:
                    amount_away_saves2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['statistics'][0][
                            'goals']['saves']))
                    name_away_top_saves2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['player']['name']))
                    id_saves_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_saves_player2]['player']['id'])

        name_goalkeeper_home_top_conceded2 = []
        amount_home_conceded2 = []
        id_conceded_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_conceded_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if \
                data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['statistics'][0]['goals'][
                    'conceded'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['statistics'][0][
                            'goals']['conceded'] > 0:
                    amount_home_conceded2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['statistics'][0][
                            'goals']['conceded']))
                    name_goalkeeper_home_top_conceded2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['player']['name']))
                    id_conceded_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_conceded_player2]['player']['id'])

        name_goalkeeper_away_top_conceded2 = []
        amount_away_conceded2 = []
        id_conceded_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_conceded_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if \
                data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['statistics'][0]['goals'][
                    'conceded'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['statistics'][0][
                            'goals']['conceded'] > 0:
                    amount_away_conceded2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['statistics'][0][
                            'goals']['conceded']))
                    name_goalkeeper_away_top_conceded2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['player']['name']))
                    id_conceded_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_conceded_player2]['player']['id'])

        name_home_top_fouls_yel_card2 = []
        amount_home_fouls_yel_card2 = []
        id_yel_card_home_players2 = []
        name_home_top_fouls_red_card2 = []
        amount_home_fouls_red_card2 = []
        id_red_card_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_fouls_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0]['cards'][
                    'yellow'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0][
                            'cards']['yellow'] > 0:
                    amount_home_fouls_yel_card2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0][
                            'cards']['yellow']))
                    name_home_top_fouls_yel_card2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['name']))
                    id_yel_card_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['id'])
                if data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0]['cards'][
                    'red'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0][
                            'cards']['red'] > 0:
                    amount_home_fouls_red_card2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['statistics'][0][
                            'cards']['red']))
                    name_home_top_fouls_red_card2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['name']))
                    id_red_card_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_fouls_player2]['player']['id'])

        name_away_top_fouls_yel_card2 = []
        amount_away_fouls_yel_card2 = []
        id_yel_card_away_players2 = []
        name_away_top_fouls_red_card2 = []
        amount_away_fouls_red_card2 = []
        id_red_card_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_fouls_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0]['cards'][
                    'yellow'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0][
                            'cards']['yellow'] > 0:
                    amount_away_fouls_yel_card2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0][
                            'cards']['yellow']))
                    name_away_top_fouls_yel_card2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['name']))
                    id_yel_card_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['id'])
                if data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0]['cards'][
                    'red'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0][
                            'cards']['red'] > 0:
                    amount_away_fouls_red_card2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['statistics'][0][
                            'cards']['red']))
                    name_away_top_fouls_red_card2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['name']))
                    id_red_card_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_fouls_player2]['player']['id'])

        name_home_top_block2 = []
        amount_home_block2 = []
        id_block_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_block_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if \
                data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['statistics'][0]['tackles'][
                    'blocks'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['statistics'][0][
                            'tackles']['blocks'] > 0:
                    amount_home_block2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['statistics'][0][
                            'tackles']['blocks']))
                    name_home_top_block2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['player']['name']))
                    id_block_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_block_player2]['player']['id'])

        name_away_top_block2 = []
        amount_away_block2 = []
        id_block_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_block_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if \
                data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['statistics'][0]['tackles'][
                    'blocks'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['statistics'][0][
                            'tackles']['blocks'] > 0:
                    amount_away_block2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['statistics'][0][
                            'tackles']['blocks']))
                    name_away_top_block2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['player']['name']))
                    id_block_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_block_player2]['player']['id'])

        name_home_top_interceptions2 = []
        amount_home_interceptions2 = []
        id_interceptions_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_interceptions_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['statistics'][0][
                    'tackles']['interceptions'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['statistics'][
                            0]['tackles']['interceptions'] > 0:
                    amount_home_interceptions2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['statistics'][
                            0]['tackles']['interceptions']))
                    name_home_top_interceptions2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['player'][
                            'id'], data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['player'][
                            'name']))
                    id_interceptions_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_interceptions_player2]['player'][
                            'id'])

        name_away_top_interceptions2 = []
        amount_away_interceptions2 = []
        id_interceptions_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_interceptions_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['statistics'][0][
                    'tackles']['interceptions'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['statistics'][
                            0]['tackles']['interceptions'] > 0:
                    amount_away_interceptions2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['statistics'][
                            0]['tackles']['interceptions']))
                    name_away_top_interceptions2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['player'][
                            'id'], data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['player'][
                            'name']))
                    id_interceptions_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_interceptions_player2]['player'][
                            'id'])

        amount_home_tackles2 = 0
        if data_all['response'][0]['players'] != []:
            for find_home_top_tackles_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if \
                data_all['response'][0]['players'][0]['players'][find_home_top_tackles_player2]['statistics'][0]['tackles'][
                    'total'] != None:
                    amount_home_tackles2 += \
                    data_all['response'][0]['players'][0]['players'][find_home_top_tackles_player2]['statistics'][0][
                        'tackles']['total']

        amount_away_tackles2 = 0
        if data_all['response'][0]['players'] != []:
            for find_away_top_tackles_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if \
                data_all['response'][0]['players'][1]['players'][find_away_top_tackles_player2]['statistics'][0]['tackles'][
                    'total'] != None:
                    amount_away_tackles2 += \
                    data_all['response'][0]['players'][1]['players'][find_away_top_tackles_player2]['statistics'][0][
                        'tackles']['total']

        name_home_top_duels2 = []
        amount_home_duels2 = []
        id_duels_home_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_home_top_duel_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                if data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['statistics'][0]['duels'][
                    'won'] != None and \
                        data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['statistics'][0][
                            'duels']['won'] > 0:
                    amount_home_duels2.append(str(
                        data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['statistics'][0][
                            'duels']['won']))
                    name_home_top_duels2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['player']['id'], data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['player']['name']))
                    id_duels_home_players2.append(
                        data_all['response'][0]['players'][0]['players'][find_home_top_duel_player2]['player']['id'])

        # AWAY
        name_away_top_duels2 = []
        amount_away_duels2 = []
        id_duels_away_players2 = []
        if data_all['response'][0]['players'] != []:
            for find_away_top_duel_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['statistics'][0]['duels'][
                    'won'] != None and \
                        data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['statistics'][0][
                            'duels']['won'] > 0:
                    amount_away_duels2.append(str(
                        data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['statistics'][0][
                            'duels']['won']))
                    name_away_top_duels2.append(
                        request_name_to_api(season, league_id, data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['player']['id'], data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['player']['name']))
                    id_duels_away_players2.append(
                        data_all['response'][0]['players'][1]['players'][find_away_top_duel_player2]['player']['id'])

        # HOME
        total_amount_home_duels2 = 0
        if data_all['response'][0]['players'] != []:
            for find_home_total_duel_player2 in range(len(data_all['response'][0]['players'][0]['players'])):
                    if data_all['response'][0]['players'][0]['players'][find_home_total_duel_player2]['statistics'][0]['duels'][
                        'total'] != None:
                        total_amount_home_duels2 += \
                        data_all['response'][0]['players'][0]['players'][find_home_total_duel_player2]['statistics'][0][
                            'duels']['total']

        # AWAY
        total_amount_away_duels2 = 0
        if data_all['response'][0]['players'] != []:
            for find_away_total_duel_player2 in range(len(data_all['response'][0]['players'][1]['players'])):
                if data_all['response'][0]['players'][1]['players'][find_away_total_duel_player2]['statistics'][0]['duels'][
                    'total'] != None:
                    total_amount_away_duels2 += \
                    data_all['response'][0]['players'][1]['players'][find_away_total_duel_player2]['statistics'][0][
                        'duels']['total']

        form_home = ''
        form_away = ''

        # Проверка заполнялся ли по этому матчу данные
        if check_fixture_match_in_db(fixture_match, 'update_fixture', 'fixture_match') == False:

            # goals
            player_update(id_goals_home_players2, name_home_top_goals2, amount_home_goals2, 'goals', season, league_id,
                          id_team_home_review, round_main, fixture_match)
            player_update(id_goals_away_players2, name_away_top_goals2, amount_away_goals2, 'goals', season, league_id,
                          id_team_away_review, round_main, fixture_match)
            # assists

            player_update(id_assists_home_players2, name_home_top_assists2, amount_home_assists2, 'assists', season,
                          league_id, id_team_home_review, round_main, fixture_match)
            player_update(id_assists_away_players2, name_away_top_assists2, amount_away_assists2, 'assists', season,
                          league_id, id_team_away_review, round_main, fixture_match)
            # fouls
            # y_cards
            player_update(id_yel_card_home_players2, name_home_top_fouls_yel_card2, amount_home_fouls_yel_card2,
                          'y_cards', season, league_id, id_team_home_review, round_main, fixture_match)
            player_update(id_yel_card_away_players2, name_away_top_fouls_yel_card2, amount_away_fouls_yel_card2,
                          'y_cards', season, league_id, id_team_away_review, round_main, fixture_match)
            # r_cards
            player_update(id_red_card_home_players2, name_home_top_fouls_red_card2, amount_home_fouls_red_card2,
                          'r_cards', season, league_id, id_team_home_review, round_main, fixture_match)
            player_update(id_red_card_away_players2, name_away_top_fouls_red_card2, amount_away_fouls_red_card2,
                          'r_cards', season, league_id, id_team_away_review, round_main, fixture_match)
            # blocks name_home_top_block2
            player_update(id_block_home_players2, name_home_top_block2, amount_home_block2, 'blocks', season, league_id,
                          id_team_home_review, round_main, fixture_match)
            player_update(id_block_away_players2, name_away_top_block2, amount_away_block2, 'blocks', season, league_id,
                          id_team_away_review, round_main, fixture_match)
            # name_home_top_interceptions2
            player_update(id_interceptions_home_players2, name_home_top_interceptions2, amount_home_interceptions2,
                          'interceptions', season, league_id, id_team_home_review, round_main, fixture_match)
            player_update(id_interceptions_away_players2, name_away_top_interceptions2, amount_away_interceptions2,
                          'interceptions', season, league_id, id_team_away_review, round_main, fixture_match)
            # saves
            player_update(id_saves_home_players2, name_home_top_saves2, amount_home_saves2, 'saves', season, league_id,
                          id_team_home_review, round_main, fixture_match)
            player_update(id_saves_away_players2, name_away_top_saves2, amount_away_saves2, 'saves', season, league_id,
                          id_team_away_review, round_main, fixture_match)
            # duels
            player_update(id_duels_home_players2, name_home_top_duels2, amount_home_duels2, 'duels', season, league_id,
                          id_team_home_review, round_main, fixture_match)
            player_update(id_duels_away_players2, name_away_top_duels2, amount_away_duels2, 'duels', season, league_id,
                          id_team_away_review, round_main, fixture_match)
            # goalkeepers
            player_update(id_conceded_home_players2, name_goalkeeper_home_top_conceded2, amount_home_conceded2,
                          'conceded', season, league_id, id_team_home_review, round_main, fixture_match)
            player_update(id_conceded_away_players2, name_goalkeeper_away_top_conceded2, amount_away_conceded2,
                          'conceded', season, league_id, id_team_away_review, round_main, fixture_match)

            player_update(player_id_injuries, player_name_injuries, amount_injuries, 'injuries', season, league_id,
                          id_team_away_review, round_main, fixture_match)
            if fast_id_player != []:
                if type_team_fast_goal == 'home':
                    player_update(fast_id_player, fаst_name_goal, time_fast_goal, 'fast_goal', season, league_id,
                                  id_team_home_review, round_main, fixture_match)
                elif type_team_fast_goal == 'away':
                    player_update(fast_id_player, fаst_name_goal, time_fast_goal, 'fast_goal', season, league_id,
                                  id_team_away_review, round_main, fixture_match)

            player_update(player_home_id_penalti, player_home_penalti,
                          total_count_penalty_list, 'penalty', season,
                          league_id, id_team_home_review, round_main, fixture_match)
            player_update(player_away_id_penalti, time_away_penalti,
                          total_count_penalty_list, 'penalty', season,
                          league_id, id_team_away_review, round_main, fixture_match)

            data_home = {
                "team_id": f"{id_team_home_review}",
                "league_id": f"{league_id}",
                "season": f"{season}",
                "name": f"{name_home_review}",
                "round": f"{round_main}",
                "list_data": {
                    "wins": f"{win_team_home}",
                    "loses": f"{lose_team_home}",
                    "draws": f"{draw_team_home}",
                    "clean_sheet_count": f"{clean_sheet_home}",
                    "goals": f"{goals_home}",
                    "without_scored_count": f"{without_score_home}",
                    "conceded_goals": f"{goals_away}",
                    "conceded_goals_count": f"{conceded_score_home}",
                    "injuries_count": f"{count_home_injuries}"
                }
            }
            update_teams(data_home)
            data_away = {
                "team_id": f"{id_team_away_review}",
                "league_id": f"{league_id}",
                "season": f"{season}",
                "name": f"{name_away_review}",
                "round": f"{round_main}",
                "list_data": {
                    "wins": f"{win_team_away}",
                    "loses": f"{lose_team_away}",
                    "draws": f"{draw_team_away}",
                    "clean_sheet_count": f"{clean_sheet_away}",
                    "goals": f"{goals_away}",
                    "without_scored_count": f"{without_score_away}",
                    "conceded_goals": f"{goals_home}",
                    "conceded_goals_count": f"{conceded_score_away}",
                    "injuries_count": f"{count_away_injuries}"
                }
            }
            update_teams(data_away)

            team_update_destroyer(id_team_home_review, round_main, total_interceptions_home, total_blocks_home,
                                  amount_home_saves3, total_amount_home_duels2, shots_on_goal_home, shots_off_goal_home,
                                  amount_home_tackles2, top__home_precent_accuracy, league_id, season)
            team_update_destroyer(id_team_away_review, round_main, total_interceptions_away, total_blocks_away,
                                  amount_away_saves3, total_amount_away_duels2, shots_on_goal_away, shots_off_goal_away,
                                  amount_away_tackles2, top__away_precent_accuracy, league_id, season)

            if goals_home > goals_away:
                view_home = 'W'
                view_away = 'L'
            elif goals_home < goals_away:
                view_home = 'L'
                view_away = 'W'
            elif goals_home == goals_away:
                view_home = 'D'
                view_away = 'D'

            update_form_teams(id_team_home_review, view_home, league_id, season)
            update_form_teams(id_team_away_review, view_away, league_id, season)

            if league_name == "World Cup":
                insert_query_form = f"SELECT form FROM teams_cup WHERE team_id_api={id_team_home_review};"
            else:
                insert_query_form = f"SELECT form FROM teams_test WHERE team_id_api={id_team_home_review} AND season = {season}"
            g = check_form_review(insert_query_form)
            if g != []:
                form_home = g[0][0]
            else:
                form_home = ''

            if league_name == "World Cup":
                insert_query_form = f"SELECT form FROM teams_cup WHERE team_id_api={id_team_away_review};"
            else:
                insert_query_form = f"SELECT form FROM teams_test WHERE team_id_api={id_team_away_review} AND season = {season}"
            k = check_form_review(insert_query_form)
            if k != []:
                form_away = k[0][0]
            else:
                form_away = ''

            insert_query_for_update = (
                f"INSERT INTO update_fixture (fixture_match)"
                f"VALUES ('{fixture_match}');"
            )
            insert_db(insert_query_for_update, f'update all players and teams for {fixture_match}')

        league_id = f"{league_id}"

        """ Топ 5 сезона """

        if league_id != '1':
            insert_query = (
                f"SELECT max(goals) AS S , name, team_id FROM players_test WHERE league_id={league_id} AND goals != 0 AND season = {season} GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
            )
            teams = 'teams_test'
        elif league_id == '1':
            insert_query = (
                f"SELECT max(goals) AS S , name, team_id FROM players_cup WHERE league_id={league_id} AND goals != 0 AND season = {season} GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
            )
            teams = 'teams_cup'
        index_top_player_goals = check_form(insert_query)

        topscorer_amount_in_league_1, topscorer_name_in_league_1, topscorer_amount_in_league_2, topscorer_name_in_league_2, topscorer_amount_in_league_3, topscorer_name_in_league_3, topscorer_amount_in_league_4, topscorer_name_in_league_4, topscorer_amount_in_league_5, topscorer_name_in_league_5 = 0, '', 0, '', 0, '', 0, '', 0, ''
        topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, topscorer_team_in_league_4, topscorer_team_in_league_5 = '', '', '', '', ''

        index = 0
        for i in range(len(index_top_player_goals)):
            insert_query_for_teams = f"SELECT name FROM {teams} WHERE team_id_api=1111 AND season = {season}"
            
            index += 1
            goals = index_top_player_goals[i]
            goals_new = []
            for i in range(len(goals)):
                if "'" in str(goals[i]):
                    goals_new.append(str(goals[i]).replace("'", ""))
                else:
                    goals_new.append(goals[i])

            if goals_new != []: goals = goals_new
            if index == 1:
                topscorer_amount_in_league_1, topscorer_name_in_league_1, team_id_top_goals_league1 = goals[0], goals[
                    1], goals[2]
                index_top_goals_team1 = check_form(
                    insert_query_for_teams.replace("1111", f"{team_id_top_goals_league1}"))
                topscorer_team_in_league_1 = ''
                if topscorer_team_in_league_1 != []: topscorer_team_in_league_1 = index_top_goals_team1[0][0]
                if "'" in topscorer_team_in_league_1: topscorer_team_in_league_1 = topscorer_team_in_league_1.replace(
                    "'", "")

            elif index == 2:
                topscorer_amount_in_league_2, topscorer_name_in_league_2, team_id_top_goals_league2 = goals[0], goals[
                    1], goals[2]
                index_top_goals_team2 = check_form(
                    insert_query_for_teams.replace("1111", f"{team_id_top_goals_league2}"))
                topscorer_team_in_league_2 = ''
                if index_top_goals_team2 != []: topscorer_team_in_league_2 = index_top_goals_team2[0][0]
                if "'" in topscorer_team_in_league_2: topscorer_team_in_league_2 = topscorer_team_in_league_2.replace(
                    "'", "")

            elif index == 3:
                topscorer_amount_in_league_3, topscorer_name_in_league_3, team_id_top_goals_league3 = goals[0], goals[
                    1], goals[2]
                index_top_goals_team3 = check_form(
                    insert_query_for_teams.replace("1111", f"{team_id_top_goals_league3}"))
                topscorer_team_in_league_3 = ''
                if index_top_goals_team3 != []: topscorer_team_in_league_3 = index_top_goals_team3[0][0]
                if "'" in topscorer_team_in_league_3: topscorer_team_in_league_3 = topscorer_team_in_league_3.replace(
                    "'", "")

            elif index == 4:
                topscorer_amount_in_league_4, topscorer_name_in_league_4, team_id_top_goals_league4 = goals[0], goals[
                    1], goals[2]
                index_top_goals_team4 = check_form(
                    insert_query_for_teams.replace("1111", f"{team_id_top_goals_league4}"))
                topscorer_team_in_league_4 = ''
                if index_top_goals_team4 != []: topscorer_team_in_league_4 = index_top_goals_team4[0][0]
                if "'" in topscorer_team_in_league_4: topscorer_team_in_league_4 = topscorer_team_in_league_4.replace(
                    "'", "")

            elif index == 5:
                topscorer_amount_in_league_5, topscorer_name_in_league_5, team_id_top_goals_league5 = goals[0], goals[
                    1], goals[2]
                index_top_goals_team5 = check_form(
                    insert_query_for_teams.replace("1111", f"{team_id_top_goals_league5}"))
                topscorer_team_in_league_5 = ''
                if index_top_goals_team5 != []: topscorer_team_in_league_5 = index_top_goals_team5[0][0]
                if "'" in topscorer_team_in_league_5: topscorer_team_in_league_5 = topscorer_team_in_league_5.replace(
                    "'", "")

        lineups_home = '+'.join(lineups_home)
        lineups_away = '+'.join(lineups_away)
        lineups_home = lineups_home.replace(" ", "_")
        lineups_away = lineups_away.replace(" ", "_")
        for i in range(len(gone_player_home)):
            if None == gone_player_home[i]: gone_player_home[i] = ""
        if len(gone_player_home) > 1: gone_player_home = '+'.join(gone_player_home)
        else: gone_player_home = ''.join(gone_player_home)
        gone_player_home = gone_player_home.replace(" ", "_")
        for i in range(len(gone_player_away)):
            if None == gone_player_away[i]: gone_player_away[i] = ""
        if len(gone_player_away) > 1:gone_player_away = '+'.join(gone_player_away)
        else: gone_player_away = ''.join(gone_player_away)
        gone_player_away = gone_player_away.replace(" ", "_")
        came_player_home = '+'.join(came_player_home)
        came_player_home = came_player_home.replace(" ", "_")
        came_player_away = '+'.join(came_player_away)
        came_player_away = came_player_away.replace(" ", "_")

        time_subst_home = ' '.join(time_subst_home)
        time_subst_away = ' '.join(time_subst_away)

        time_home_goal = ' '.join(time_home_goal)
        player_home_goal = '+'.join(player_home_goal)
        player_home_goal = player_home_goal.replace(" ", "_")
        time_away_goal = ' '.join(time_away_goal)
        player_away_goal = '+'.join(player_away_goal)
        player_away_goal = player_away_goal.replace(" ", "_")
        time_home_yellow = ' '.join(time_home_yellow)
        player_home_yellow = '+'.join(player_home_yellow)
        player_home_yellow = player_home_yellow.replace(" ", "_")
        time_away_yellow = ' '.join(time_away_yellow)
        player_away_yellow = '+'.join(player_away_yellow)
        player_away_yellow = player_away_yellow.replace(" ", "_")
        time_home_red = ' '.join(time_home_red)
        player_home_red = '+'.join(player_home_red)
        player_home_red = player_home_red.replace(" ", "_")
        time_away_red = ' '.join(time_away_red)
        player_away_red = '+'.join(player_away_red)
        player_away_red = player_away_red.replace(" ", "_")
        player_home_penalti = '+'.join(player_home_penalti)
        player_home_penalti = player_home_penalti.replace(" ", "_")
        time_home_penalti = ' '.join(time_home_penalti)
        player_away_penalti = '+'.join(player_away_penalti)
        player_away_penalti = player_away_penalti.replace(" ", "_")
        time_away_penalti = ' '.join(time_away_penalti)

        rank_for_table = ' '.join(rank_for_table)
        name_table_team = '+'.join(name_table_team)
        name_table_team = name_table_team.replace(" ", "_")
        logo_for_table = '+'.join(logo_for_table)
        logo_for_table = logo_for_table.replace(" ", "_")

        form_table = ''

        all_matches_table = ' '.join(all_matches_table)
        win_matches_table = ' '.join(win_matches_table)
        draw_matches_table = ' '.join(draw_matches_table)
        lose_matches_table = ' '.join(lose_matches_table)
        goals_scored_for_table = ' '.join(goals_scored_for_table)
        goals_missed_for_table = ' '.join(goals_missed_for_table)
        goals_diff_table = ' '.join(goals_diff_table)
        points_for_table = ' '.join(points_for_table)

        if name_table_team:
            name_table_team = name_table_team.replace("'", "")
        if venue:
            venue = venue.replace("'", "")
        if player_away_red:
            player_away_red = player_away_red.replace("'", "")
        if player_home_red:
            player_home_red = player_home_red.replace("'", "")
        if player_home_penalti:
            player_home_penalti = player_home_penalti.replace("'", "")
        if player_away_penalti:
            player_away_penalti = player_away_penalti.replace("'", "")
        if lineups_home:
            lineups_home = lineups_home.replace("'", "")
        if lineups_away:
            lineups_away = lineups_away.replace("'", "")
        if gone_player_home:
            gone_player_home = gone_player_home.replace("'", "")
        if gone_player_away:
            gone_player_away = gone_player_away.replace("'", "")
        if came_player_home:
            came_player_home = came_player_home.replace("'", "")
        if came_player_away:
            came_player_away = came_player_away.replace("'", "")
        if player_home_goal:
            player_home_goal = player_home_goal.replace("'", "")
        if player_away_goal:
            player_away_goal = player_away_goal.replace("'", "")

        if player_home_yellow:
            player_home_yellow = player_home_yellow.replace("'", "")
        if player_away_yellow:
            player_away_yellow = player_away_yellow.replace("'", "")
        if player_home_red:
            player_home_red = player_home_red.replace("'", "")
        if player_away_red:
            player_away_red = player_away_red.replace("'", "")

        if name_away_top_interceptions:
            name_away_top_interceptions = name_away_top_interceptions.replace("'", "")
        if name_home_top_interceptions:
            name_home_top_interceptions = name_home_top_interceptions.replace("'", "")
        if name_home_top_duels:
            name_home_top_duels = name_home_top_duels.replace("'", "")
        if name_away_top_duels:
            name_away_top_duels = name_away_top_duels.replace("'", "")
        if name_home_top_shots:
            name_home_top_shots = name_home_top_shots.replace("'", "")
        if name_away_top_shots:
            name_away_top_shots = name_away_top_shots.replace("'", "")
        if name_home_top_block:
            name_home_top_block = name_home_top_block.replace("'", "")
        if name_away_top_block:
            name_away_top_block = name_away_top_block.replace("'", "")
        if away_venue_vs_rival:
            away_venue_vs_rival = away_venue_vs_rival.replace("'", "")
        if home_next_venue_vs_rival:
            home_next_venue_vs_rival = home_next_venue_vs_rival.replace("'", "")
        if name_home_top_goals:
            name_home_top_goals = name_home_top_goals.replace("'", "")
        if name_away_top_goals:
            name_away_top_goals = name_away_top_goals.replace("'", "")
        if name_home_top_assists:
            name_home_top_assists = name_home_top_assists.replace("'", "")
        if name_away_top_assists:
            name_away_top_assists = name_away_top_assists.replace("'", "")
        if name_home_top_saves:
            name_home_top_saves = name_home_top_saves.replace("'", "")
        if name_away_top_saves:
            name_away_top_saves = name_away_top_saves.replace("'", "")
        if name_home_top_fouls_yel_card:
            name_home_top_fouls_yel_card = name_home_top_fouls_yel_card.replace("'", "")
        if name_away_top_fouls_yel_card:
            name_away_top_fouls_yel_card = name_away_top_fouls_yel_card.replace("'", "")
        if name_home_top_pass_accuracy:
            name_home_top_pass_accuracy = name_home_top_pass_accuracy.replace("'", "")
        if name_away_top_pass_accuracy:
            name_away_top_pass_accuracy = name_away_top_pass_accuracy.replace("'", "")
        if name_home_top_pass_key:
            name_home_top_pass_key = name_home_top_pass_key.replace("'", "")
        if name_away_top_pass_key:
            name_away_top_pass_key = name_away_top_pass_key.replace("'", "")
        if name_home_top_fouls_red_card:
            name_home_top_fouls_red_card = name_home_top_fouls_red_card.replace("'", "")
        if str(name_home_top_fouls_yel_card):
            name_home_top_fouls_yel_card = str(name_home_top_fouls_yel_card).replace("'", "")
        if str(name_home_top_fouls_red_card2):
            name_home_top_fouls_red_card2 = str(name_home_top_fouls_red_card2).replace("'", "")
        if str(name_home_top_fouls_yel_card2):
            name_home_top_fouls_yel_card2 = str(name_home_top_fouls_yel_card2).replace("'", "")

        list_v = [fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table,league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card,amount_home_fouls_red_card, name_away_top_fouls_red_card,amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes,name_away_top_pass_accuracy, top__away_precent_accuracy,top__away_total_passes, name_home_top_pass_key,top__home_amount_key, name_away_top_pass_key,top__away_amount_key, round_main, team_home_passes_accurate,team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate,team_home_total_passes, team_away_total_passes, injuries_count ,total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time]

        for index_replace in range(len(list_v)):
            if type(list_v[index_replace]) == str:
                if "'" in list_v[index_replace]:
                    list_v[index_replace] = list_v[index_replace].replace("'", "")

        fixture_match, name_home_review, name_away_review, lineups_home, lineups_away, gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round_main, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time = list_v

        # Составление запроса
        insert_query = (
            f" INSERT INTO match_review (fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time) "  # name_home_top_fouls_yel_card  amount_home_fouls_yel_card
            f"VALUES ('{fixture_match}', '{name_home_review}', '{name_away_review}', '{lineups_home}', '{lineups_away}',  '{gone_player_home}', '{gone_player_away}', '{came_player_home}', '{came_player_away}', '{time_subst_home}', '{time_subst_away}', '{time_home_goal}', '{player_home_goal}', '{time_away_goal}', '{player_away_goal}', '{time_home_yellow}', '{player_home_yellow}', '{time_away_yellow}', '{player_away_yellow}', '{time_home_red}', '{player_home_red}', '{time_away_red}', '{player_away_red}', '{name_home_top_shots}', '{name_away_top_shots}', '{name_home_top_block}', '{name_away_top_block}', '{name_home_top_interceptions}', '{name_away_top_interceptions}', '{ball_possession_home}', '{ball_possession_away}', '{name_home_top_duels}', '{name_away_top_duels}', '{home_next_match_rival}', '{home_date_match_vs_rival}', '{home_next_venue_vs_rival}', '{away_next_match_rival}', '{away_date_match_vs_rival}', '{away_venue_vs_rival}', '{topscorer_name_in_league_1}', '{topscorer_name_in_league_2}', '{topscorer_name_in_league_3}', '{topscorer_amount_in_league_1}', '{topscorer_amount_in_league_2}', '{topscorer_amount_in_league_3}', '{topscorer_team_in_league_1}', '{topscorer_team_in_league_2}', '{topscorer_team_in_league_3}', '{fixture_match}', '{goals_home}', '{goals_away}', '{shots_on_goal_home}', '{shots_off_goal_home}', '{amount_home_shots}', '{amount_away_shots}', '{total_assists_home}', '{total_assists_away}', '{total_shots_home}', '{total_shots_away}', '{total_shots_on}', '{total_shots_off}', '{total_blocks_home}', '{amount_home_block}', '{total_blocks_away}', '{amount_away_block}', '{total_interceptions_home}', '{amount_home_interceptions}', '{total_interceptions_away}', '{amount_away_interceptions}', '{amount_home_duels}', '{amount_away_duels}', '{shots_on_goal_away}', '{shots_off_goal_away}', '{name_home_top_goals}', '{amount_home_goals}', '{name_away_top_goals}', '{amount_away_goals}', '{name_home_top_assists}', '{amount_home_assists}', '{name_away_top_assists}', '{amount_away_assists}', '{name_home_top_saves}', '{amount_home_saves}', '{name_away_top_saves}', '{amount_away_saves}', '{id_team_home_review}', '{id_team_away_review}', '{league}', '{venue}', '{date_match3}', '{player_home_penalti}', '{time_home_penalti}', '{player_away_penalti}', '{time_away_penalti}', '{form_home}', '{form_away}', '{topscorer_name_in_league_4}', '{topscorer_amount_in_league_4}', '{topscorer_team_in_league_4}', '{topscorer_name_in_league_5}', '{topscorer_amount_in_league_5}', '{topscorer_team_in_league_5}', '{rank_for_table}', '{name_table_team}', '{form_table}', '{all_matches_table}', '{win_matches_table}', '{draw_matches_table}', '{lose_matches_table}', '{goals_scored_for_table}', '{goals_missed_for_table}', '{goals_diff_table}', '{points_for_table}', '{logo_for_table}','{league_name}', '{name_home_top_fouls_yel_card}', '{amount_home_fouls_yel_card}', '{name_away_top_fouls_yel_card}', '{amount_away_fouls_yel_card}', '{name_home_top_fouls_red_card}','{amount_home_fouls_red_card}', '{name_away_top_fouls_red_card}','{amount_away_fouls_red_card}', '{name_home_top_pass_accuracy}', '{top__home_precent_accuracy}', '{top__home_total_passes}','{name_away_top_pass_accuracy}', '{top__away_precent_accuracy}','{top__away_total_passes}', '{name_home_top_pass_key}','{top__home_amount_key}', '{name_away_top_pass_key}','{top__away_amount_key}', '{round_main}', '{team_home_passes_accurate}','{team_away_passes_accurate}', '{team_home_percent_passes_accurate}', '{team_away_percent_passes_accurate}','{team_home_total_passes}', '{team_away_total_passes}', '{injuries_count}' ,'{total_cards_in_game}', '{count_yel_card}', '{count_red_card}', '{match_lasted}', '{referee_time}');"
        )
        # Запуск функции сохранения 
        insert_db(insert_query, 'match_review')

host = '127.0.0.1'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
import psycopg2
def get_top_player():
    try:
        connection = psycopg2.connect (
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT fixture_match FROM match_preview WHERE league = 772 AND season = 2023;"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            list_f = []
            if result != []:
                for i in range(len(result)):
                    list_f.append(result[i][0])
            return list_f

            connection.commit()
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    finally:
        if connection:
            connection.close()

def custom_insert():
    list_fixture = get_top_player()
    list_fixture.sort()
    for fixture in list_fixture:
        insert_review_match_api(fixture)

# custom_insert()
# # def delete(insert_query):
# #     try:
# #         connection = psycopg2.connect (
# #             host= host,
# #             user = user,
# #             password = password,
# #             database = db_name
# #         )
# #         with connection.cursor() as cursor:
# #             cursor.execute(insert_query)
# #             connection.commit()
# #     except Exception as _ex:
# #         print('[INFO] ERROR', _ex)
# #     finally:
# #         if connection:
# #             connection.close()
# # # print(get_top_player())
# # #
# # #
# # #
# # # # fixture_m = ['898687', '898689', '898693', '898685', '898691', '898686', '898688', '898690', '898692', '898684', '898683', '898679', '898682', '898678', '898681', '898677', '898680', '898676', '898667', '898674', '898672', '898670', '898673', '898675', '898669', '898671', '898668', '898665', '898663', '898661', '898666', '898664', '898658', '898662', '898659', '898660', '898649', '898655', '898657', '898650', '898653', '898652', '898651', '898654', '898656', '898644', '898645', '898642', '898647', '898641', '898640', '898646', '898643', '898648', '898630', '898632', '898635', '898633', '898639', '898638', '898634', '898637', '898636', '898631', '898623', '898624', '898627', '898622', '898626', '898628', '898625', '898629', '898619', '898621', '898616', '898613', '898614', '898618', '898615', '898620', '898617', '898607', '898611', '898606', '898609', '898610', '898612', '898608', '898604', '898605', '868074', '868073', '868066', '868075', '868072', '868069', '868067', '868070', '868068', '868071', '868061', '868060', '868065', '868064', '868057', '868063', '868058', '868056', '868062', '868059', '868051', '868046', '868049', '868052', '868053', '868054', '868055', '868048', '868050', '868047', '868044', '871271', '868041', '868037', '868045', '868040', '868038', '868039', '868043', '868042', '868036', '868031', '868030', '868033', '868035', '868028', '868026', '868029', '868032', '868034', '868027', '868019', '868020', '868021', '868017', '868024', '868022', '868018', '868025', '868023', '868016', '868010', '868008', '868015', '868007', '868013', '868011', '868012', '868014', '868006', '868009', '868001', '867998', '867996', '867999', '867997', '868003', '868004', '868005', '868002', '868000', '867990', '867994', '867991', '867986', '867995', '867987', '867989', '867993', '867992', '867988', '867983', '867985', '867977', '867976', '867979', '867978', '867980', '867982', '867981', '871262', '871596', '871260', '871259', '871261', '871258', '871256', '871255', '871254', '871257', '871245', '871247', '871248', '871246', '871251', '871249', '871250', '871253', '871252', '871243', '871244', '871240', '871236', '871238', '871237', '871241', '871242', '871239', '871234', '871233', '871235', '871232', '871231', '871230', '871229', '871228', '871227', '871224', '871223', '871221', '871219', '871226', '871225', '871220', '871218', '871222', '871211', '871212', '871216', '871215', '871213', '871214', '871210', '871209', '871217', '871203', '871207', '871204', '871206', '871205', '871208', '871202', '871201', '871200', '871199', '871194', '871191', '871192', '871195', '871197', '871198', '871196', '871193', '871188', '871186', '871184', '871183', '871182', '871187', '871189', '871190', '871185', '871173', '871177', '871180', '871181', '871179', '871178', '871175', '871174', '871176', '871167', '871172', '871165', '871170', '871169', '871168', '871171', '871166', '871164', '871583', '871585', '871589', '871582', '871587', '871588', '871581', '871586', '871584', '871580', '871574', '871571', '871577', '871579', '871570', '871573', '871578', '871575', '871572', '871576', '871562', '871568', '871567', '871564', '871561', '871560', '871563', '871569', '871566', '871565', '871556', '871552', '871559', '871558', '871551', '871550', '871554', '871555', '871557', '871553', '871546', '871542', '871548', '871547', '871545', '871541', '871549', '871543', '871544', '871540', '871531', '871538', '871530', '871532', '871533', '871539', '871537', '871534', '871535', '871536', '871483', '871525', '871529', '871528', '871527', '871522', '871520', '871524', '871523', '871526', '871521', '871519', '871518', '871516', '871515', '871512', '871510', '871511', '871514', '871517', '871513', '871505', '871508', '871509', '871507', '871504', '871502', '871503', '871506', '871501', '871500', '871493', '871498', '871494', '871492', '871499', '871491', '871497', '871496', '881888', '881882', '881886', '881880', '881881', '881889', '881883', '881885', '878059', '881887', '881884', '881875', '881877', '881872', '881876', '881878', '881874', '881873', '881870', '881879', '881871', '881862', '881865', '881861', '881869', '881866', '881864', '881868', '881860', '881863', '881867', '881852', '881854', '881850', '881859', '881858', '881856', '881855', '881851', '881853', '881857', '881843', '881845', '881844', '881842', '881841', '881849', '881848', '881847', '881840', '881846', '881832', '881834', '881835', '881831', '881836', '881839', '881830', '881838', '881833', '881837', '881829', '881828', '881827', '881826', '881825', '881824', '881823', '881822', '881821', '881820', '881819', '881818', '881817', '881816', '881814', '881813', '881815', '881812', '881811', '881810', '881808', '881809', '881807', '881806', '881804', '881805', '881803', '881802', '881801', '881800', '881799', '881798', '881797', '881796', '881795', '881794', '881793', '881792', '881791', '878042', '878045', '878051', '878044', '878046', '878047', '878043', '878048', '878050', '878049', '878033', '878041', '878036', '878034', '878040', '878038', '878039', '878032', '878037', '878035', '878030', '878031', '878025', '878026', '878023', '878022', '878024', '878027', '878029', '878028', '878014', '878013', '878018', '878016', '878021', '878015', '878020', '878012', '878019', '878017', '878009', '878010', '878005', '878008', '878004', '878007', '878006', '878002', '878003', '878011', '877993', '877995', '877999', '878000', '877997', '877992', '877996', '877994', '878001', '877998', '877987', '877983', '877984', '877989', '877991', '877982', '877990', '877985', '877986', '877988', '877980', '877978', '877977', '877972', '877973', '877975', '877974', '877976', '877981', '877979', '877969', '877968', '877966', '877962', '877965', '877967', '877971', '877964', '877963', '877970', '877959', '877961', '877957', '877953', '877952', '877954', '877958', '877960', '877956']
# # # # l = ['867946', '867947',  '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '867963', '867964', '867965', '867966','867967','867968','867969','867970','867971','867972','867973','867974','867975','867976','867977','867978','867979','867980','867981','867982','867983','867984','867985', '877942','877943','877944','877945','877946','877947','877948','877949','877950','877951']
# # # l1 = ['881780', '881781', '881782', '881783', '881784','881785', '881786','881787','881788', '881789', '871470', '871471', '871472', '871473','871474','871475','871476','871477','871478','871479','871480','871481','871482','871484','871485','871486','871487','871488','877942','877943','877944','877945','877946','877947','877948','877949','877950','877950','877951', '867947', '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '867963', '867964', '867965', '867966', '867967', '867968', '867969', '867970', '867971', '867972', '867973', '867974', '867975', '867984', '871263', '871264', '871265', '871266', '871267', '871268', '871269', '871270', '871271', '868076', '868077','868078','868079','868080','868081','868082','868083','868084','868085', '878052' , '878053', '878054', '878055', '878056', '878057', '878058', '878059', '878060', '878061', '871590', '871591', '871592', '871593', '871594', '871595', '871596', '871597', '871598', '871599', '881890', '881891', '881892', '881893', '881894','881895', '881896', '881897', '881898', '881899']
# # # l = l + l1
# # l = ['868126', '868127', '868128', '868130', '868131', '868132', '868133', '868134', '868135']
# # for i in l:
# #     insert_review_match_api(i)
# # fixture_m.sort()
# #
# # # fixture_m = ['866681','866682','866683','871850','871851','855735','855736']
# # insert_query = (
# #     f"DELETE FROM match_review WHERE league = '1'"
# # )
# # d = delete(insert_query)
# # fixture_m = get_top_player()
# # for i in range(len(fixture_m)):
# #     insert_query = (
# #         f"DELETE FROM update_fixture WHERE fixture_match = '{fixture_m[i]}'"
# #     )
# #     d2 = delete(insert_query)
# #
# #     insert_review_match_api(fixture_m[i])
# #
# #
# # insert_review_match_api('898737')