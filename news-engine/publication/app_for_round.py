import os
from time import sleep
import requests
import json
import base64
from datetime import datetime, timedelta
# import datetime
# from db_for_app import get_user_id_main
import psycopg2
from publication.change_text import main_change_text
from publication.db_for_app import bot_send_message_tg, upload_image_to_wordpress


def check_stat_preview(insert_query):
    try:
        connection = psycopg2.connect(
            host='localhost',
            user = 'db_user',
            password = 'PASS',
            database = 'db_match'
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()
            connection.commit()
            return result


    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def replace_new_list(list_old):
    new_list = []
    for i in range(len(list_old)):
        if " " in list_old[i]:
            new_list.append(list_old[i].replace("_", " "))
        else:
            new_list.append(list_old[i])
    return new_list


def get_data_fix(fixture_match, team_name_home):
    insert_query = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE fixture_match_for_check = {fixture_match}"
    )
    index = check_stat_preview(insert_query)
    index = index[0]
    name_home_review = index[0]
    name_away_review = index[1]
    goals_home = index[2]
    goals_away = index[3]

    if name_home_review == team_name_home:
        team_away = name_away_review
        goals_home_new = goals_home
        goals_away_new = goals_away
    else:
        team_away = name_home_review
        goals_away_new = goals_home
        goals_home_new = goals_away

    return team_away, goals_home_new, goals_away_new

def upload_photo():
    """
    Функция для загрузки фото на сервак
    """
    pass
def replace_new_list(list_old):
    new_list = []
    for i in range(len(list_old)):
        if " " in list_old[i]:
            new_list.append(list_old[i].replace("_", " "))
        else:
            new_list.append(list_old[i])
    return new_list


def get_user_id_main(type_subscribe):
    try:
        # Подключаемся
        connection = psycopg2.connect(
            host='localhost',
            user='db_user',
            password='PASS',
            database='main'
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT id_user FROM subscribe WHERE type_subscribe LIKE '{type_subscribe}';"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            l = []
            for i in range(len(result)):
                l.append(result[i][0])
            return l

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()


def publish(id, league_name, featured_image, title, text_all, types, round, language, league_id):  # list_id[global_for]

    # TODO подумать по поводу отдельного файла (JSON)

    """
    Получаем информацию по клиенту и делаем публикацию
    """
    with open(
            # f'/Applications/BotBot/work_rep/new/footballBot/parameters/football/users/parameters/{id}.json'
            f'/opt/footballBot/parameters/football/users/parameters/{id}.json'
    ) as file:
        data_j = json.load(file)

    platform_name = data_j['platform_name']
    l_version = data_j['l_version']
    """
    Будут разные типы платформ
    Нужно будте делат через if, elif, else    
    """

    if platform_name == 'wordpress':
        url = data_j['platform_url']
        user = data_j['platform_user']
        password = data_j['platform_password']
        type_status = data_j['type_status']


        credentials = user + ':' + password
        """
        Получение категории (Как правило Лиги)
        """

        category = ''

        if league_name in data_j['list_id']: category = data_j['list_id'][league_name]['id']

        if category != "" \
                and data_j['category_id'] != "": category = [category, data_j['category_id']]
        elif category == "" \
                and data_j['category_id'] != "": category = data_j['category_id']
        types_for_publish = data_j['subscribe']['football'][league_name]['types']


        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}

        if data_j['featured_image'] == 'upload':

            """ upload image to wordpress """
            img_id = upload_image_to_wordpress(
                f'/opt/footballBot/result/img_match/{language}_{league_id}_{round}_{types}.png',
                url.replace('posts', 'media'),
                header
            )

            post = {
                'title': title,
                'status': f'{type_status}',  # тип
                'content': text_all,
                'categories': category, # category ID
                'featured_media': img_id
            }
        else: post = {
            'title': title,
            'status': f'{type_status}',  # тип
            'content': text_all,
            'categories': category, # category ID
            # 'date'   : f'{date}',   # время публикации --  {время матча - один день}
            'meta': {'_knawatfibu_url': featured_image}
        }

        if types_for_publish != 'nothing':
            if types + "_round" in types_for_publish \
                    or types_for_publish == 'all':
                    responce = requests.post(url, headers=header, json=post).json()
                    print(f"[INFO]  posted")
                    return responce
        return False




def change_date(list_date, l_version):

    returned_date = []

    """ Открытие JSON """
    with open(
            # f'/Applications/BotBot/work_rep/new/footballBot/parameters/football/users/dicts/months_for_users.json'
              f'/opt/footballBot/parameters/football/users/dicts/months_for_users.json'
              ) as file:
        month_json = json.load(file)

    for i in range(len(list_date)):
        date = list_date[i]
        if ' ' in str(list_date[i]):
            date = str(list_date[i]).replace(" ", "T")

        month = month_json[l_version][date[5:7]]
        day = date[8:10]
        time = date[11:16]
        year = date[0:4]

        if l_version == 'ru':
            returned_date.append(f'{day} {month} в {time} (UTC)')
        else:
            returned_date.append(f'{month} {day} at {time} (UTC)')

    return returned_date


def main_publication(rounds, types, league_id):
    """
    Документация. Этапы фунkции

    Функция принимает значение номера тура, тип публикации тура (ревью, превью) и также айди лиги
    Открывает JSON с параметрами/значениеми эданного тура
    Включаем цикл по все клиентам
    Проверяем тип публикации тура
    Вытягиваем фьючер картинку
    Заполняем перемнные с json
    Проводим манипуляцию в тексте (заменение слов по значениям)
    Вытягиваем текст юзера
    Заменяем переменные в тексте на значение с JSON
    Проводим публикацию с помощью функции publish
    """

    list_id = get_user_id_main('football')
    season = '2022'

    with open(
            f'/opt/footballBot/result/json/{league_id}_{rounds}_{types}_round.json'
    ) as file:
        variables_json = json.load(file)
        # print(type(variables_json)) # переменные

    for global_for in range(len(list_id)):

        # для большой скорости поместить после вывода перемен (перед текстом)

        if types == 'review':

            # переменые

            rounds = variables_json["title"]["rounds"]
            all_matches_round_tg = variables_json["title"]['all_matches_round_tg']
            league_name = variables_json["title"]["league_name"]
            all_rounds = variables_json["title"]["all_rounds"]
            team_home_leader = variables_json["matches"]["team_home_leader"]
            team_away_rival = variables_json["matches"]["team_away_rival"]
            goal_leader = variables_json["matches"]["goal_leader"]
            goal_rival = variables_json["matches"]["goal_rival"]
            all_matches_round = variables_json["matches"]["all_matches_round"]
            count_home = variables_json["matches"]["count_home"]
            count_away = variables_json["matches"]["count_away"]
            count_draw = variables_json["matches"]["count_draw"]
            h3_leader = variables_json["matches"]["h3_leader"]
            h3_another = variables_json["matches"]["h3_another"]
            all_goals_round = variables_json["stats"]["all_goals_round"]
            all_penalty_round = variables_json["stats"]["all_penalty_round"]
            total_percent_round = variables_json["stats"]["total_percent_round"]
            average_goals_in_season = variables_json["stats"]["average_goals_in_season"]
            average_penalty_in_season = variables_json["stats"]["average_penalty_in_season"]
            time_fast_goal = variables_json["stats"]["time_fast_goal"]
            name_fast_goal = variables_json["stats"]["name_fast_goal"]
            team_name_fast_goal = variables_json["stats"]["team_name_fast_goal"]
            team_away_fast_goal = variables_json["stats"]["team_away_fast_goal"]
            scrore_fast_goal = variables_json["stats"]["scrore_fast_goal"]
            team_top_destroyer = variables_json["team_efficiency"]["team_top_destroyer"]
            destroyer_interceptions = variables_json["team_efficiency"]["destroyer_interceptions"]
            destroyer_blocks = variables_json["team_efficiency"]["destroyer_blocks"]
            destroyer_tackles = variables_json["team_efficiency"]["destroyer_tackles"]
            destroyer_saves = variables_json["team_efficiency"]["destroyer_saves"]
            amount_max_destroyer = variables_json["team_efficiency"]["amount_max_destroyer"]
            team_main_destroyer = variables_json["team_efficiency"]["team_main_destroyer"]
            team_rival_destroyer = variables_json["team_efficiency"]["team_rival_destroyer"]
            goals_main_destroyer = variables_json["team_efficiency"]["goals_main_destroyer"]
            goals_rival_destroyer = variables_json["team_efficiency"]["goals_rival_destroyer"]
            max_destroyer_of_season_name = variables_json["team_efficiency"]["max_destroyer_of_season_name"]
            max_destroyer_of_season_amount = variables_json["team_efficiency"]["max_destroyer_of_season_amount"]
            team_top_creator = variables_json["team_efficiency"]["team_top_creator"]
            creator_duels = variables_json["team_efficiency"]["creator_duels"]
            creator_shots_on_target = variables_json["team_efficiency"]["creator_shots_on_target"]
            creator_shots_off_target = variables_json["team_efficiency"]["creator_shots_off_target"]
            amount_max_creator = variables_json["team_efficiency"]["amount_max_creator"]
            team_main_creator = variables_json["team_efficiency"]["team_main_creator"]
            team_rival_creator = variables_json["team_efficiency"]["team_rival_creator"]
            goals_main_creator = variables_json["team_efficiency"]["goals_main_creator"]
            goals_rival_creator = variables_json["team_efficiency"]["goals_rival_creator"]
            max_creator_of_season_name = variables_json["team_efficiency"]["max_creator_of_season_name"]
            max_creator_of_season_amount = variables_json["team_efficiency"]["max_creator_of_season_amount"]
            name_max_accurate_in_round = variables_json["team_efficiency"]["name_max_accurate_in_round"]
            max_accurate_in_round = variables_json["team_efficiency"]["max_accurate_in_round"]
            max_total_passes_with_accurate_in_round = variables_json["team_efficiency"]["max_total_passes_with_accurate_in_round"]
            name_max_accuracy_in_season = variables_json["team_efficiency"]["name_max_accuracy_in_season"]
            percent_max_accuracy_in_season = variables_json["team_efficiency"]["percent_max_accuracy_in_season"]
            name_min_accurate_in_round = variables_json["team_efficiency"]["name_min_accurate_in_round"]
            min_accurate_in_round = variables_json["team_efficiency"]["min_accurate_in_round"]
            name_min_accuracy_in_season = variables_json["team_efficiency"]["name_min_accuracy_in_season"]
            min_total_passes_with_accurate_in_round = variables_json["team_efficiency"]["min_total_passes_with_accurate_in_round"]
            percent_min_accuracy_in_season = variables_json["team_efficiency"]["percent_min_accuracy_in_season"]
            name_max_saves_of_round = variables_json["players_stats"]["name_max_saves_of_round"]
            main_team_max_saves = variables_json["players_stats"]["main_team_max_saves"]
            round_max_saves_of_round = variables_json["players_stats"]["round_max_saves_of_round"]
            amount_max_saves_of_round = variables_json["players_stats"]["amount_max_saves_of_round"]
            rival_team_max_saves = variables_json["players_stats"]["rival_team_max_saves"]
            goals_and_info_max_saves = variables_json["players_stats"]["goals_and_info_max_saves"]
            date_game_max_saves = variables_json["players_stats"]["date_game_max_saves"]
            top_fouls_total_yel_card = variables_json["players_stats"]["top_fouls_total_yel_card"]
            top_fouls_total_red_card = variables_json["players_stats"]["top_fouls_total_red_card"]
            top_fouls_team_name_home = variables_json["players_stats"]["top_fouls_team_name_home"]
            top_fouls_team_name_away = variables_json["players_stats"]["top_fouls_team_name_away"]
            top_fouls_goals_home = variables_json["players_stats"]["top_fouls_goals_home"]
            top_fouls_goals_away = variables_json["players_stats"]["top_fouls_goals_away"]
            name_top3_fouls_of_season = variables_json["players_stats"]["name_top3_fouls_of_season"]
            ycards_top3_fouls_of_season = variables_json["players_stats"]["ycards_top3_fouls_of_season"]
            rcards_top3_fouls_of_season = variables_json["players_stats"]["rcards_top3_fouls_of_season"]
            name_teams_cards_top3_fouls_of_season = variables_json["players_stats"]["name_teams_cards_top3_fouls_of_season"]
            round_injuries = variables_json["players_stats"]["round_injuries"]
            average_injuries_in_round = variables_json["players_stats"]["average_injuries_in_round"]
            top_round_injuries_name_team = variables_json["players_stats"]["top_round_injuries_name_team"]
            top_round_injuries_amount = variables_json["players_stats"]["top_round_injuries_amount"]
            name_top_goals_league_1 = variables_json["tops"]["name_top_goals_league_1"]
            name_top_goals_league_2 = variables_json["tops"]["name_top_goals_league_2"]
            name_top_goals_league_3 = variables_json["tops"]["name_top_goals_league_3"]
            name_top_goals_league_4 = variables_json["tops"]["name_top_goals_league_4"]
            name_top_goals_league_5 = variables_json["tops"]["name_top_goals_league_5"]
            goals_top_league_1 = variables_json["tops"]["goals_top_league_1"]
            goals_top_league_2 = variables_json["tops"]["goals_top_league_2"]
            goals_top_league_3 = variables_json["tops"]["goals_top_league_3"]
            goals_top_league_4 = variables_json["tops"]["goals_top_league_4"]
            goals_top_league_5 = variables_json["tops"]["goals_top_league_5"]
            team_top_goals_league1_1 = variables_json["tops"]["team_top_goals_league1_1"]
            team_top_goals_league2_1 = variables_json["tops"]["team_top_goals_league2_1"]
            team_top_goals_league3_1 = variables_json["tops"]["team_top_goals_league3_1"]
            team_top_goals_league4_1 = variables_json["tops"]["team_top_goals_league4_1"]
            team_top_goals_league5_1 = variables_json["tops"]["team_top_goals_league5_1"]
            name_top_assists_league_1 = variables_json["tops"]["name_top_assists_league_1"]
            assists_top_league_1 = variables_json["tops"]["assists_top_league_1"]
            team_top_assists_league1 = variables_json["tops"]["team_top_assists_league1"]
            name_top_assists_league_2 = variables_json["tops"]["name_top_assists_league_2"]
            assists_top_league_2 = variables_json["tops"]["assists_top_league_2"]
            team_top_assists_league2 = variables_json["tops"]["team_top_assists_league2"]
            name_top_assists_league_3 = variables_json["tops"]["name_top_assists_league_3"]
            assists_top_league_3 = variables_json["tops"]["assists_top_league_3"]
            team_top_assists_league3 = variables_json["tops"]["team_top_assists_league3"]
            name_top_assists_league_4 = variables_json["tops"]["name_top_assists_league_4"]
            assists_top_league_4 = variables_json["tops"]["assists_top_league_4"]
            team_top_assists_league4 = variables_json["tops"]["team_top_assists_league4"]
            name_top_assists_league_5 = variables_json["tops"]["name_top_assists_league_5"]
            assists_top_league_5 = variables_json["tops"]["assists_top_league_5"]
            team_top_assists_league5 = variables_json["tops"]["team_top_assists_league5"]
            name_top_saves_league_1 = variables_json["tops"]["name_top_saves_league_1"]
            saves_top_league_1 = variables_json["tops"]["saves_top_league_1"]
            team_top_saves_league1 = variables_json["tops"]["team_top_saves_league1"]
            name_top_saves_league_2 = variables_json["tops"]["name_top_saves_league_2"]
            saves_top_league_2 = variables_json["tops"]["saves_top_league_2"]
            team_top_saves_league2 = variables_json["tops"]["team_top_saves_league2"]
            name_top_saves_league_3 = variables_json["tops"]["name_top_saves_league_3"]
            saves_top_league_3 = variables_json["tops"]["saves_top_league_3"]
            team_top_saves_league3 = variables_json["tops"]["team_top_saves_league3"]
            name_top_saves_league_4 = variables_json["tops"]["name_top_saves_league_4"]
            saves_top_league_4 = variables_json["tops"]["saves_top_league_4"]
            team_top_saves_league4 = variables_json["tops"]["team_top_saves_league4"]
            name_top_saves_league_5 = variables_json["tops"]["name_top_saves_league_5"]
            saves_top_league_5 = variables_json["tops"]["saves_top_league_5"]
            team_top_saves_league5 = variables_json["tops"]["team_top_saves_league5"]
            total_name_top_goals_league_1_round = variables_json["tops"]["total_name_top_goals_league_1_round"]
            total_name_top_goals_league_2_round = variables_json["tops"]["total_name_top_goals_league_2_round"]
            total_name_top_goals_league_3_round = variables_json["tops"]["total_name_top_goals_league_3_round"]
            total_name_top_goals_league_4_round = variables_json["tops"]["total_name_top_goals_league_4_round"]
            total_name_top_goals_league_5_round = variables_json["tops"]["total_name_top_goals_league_5_round"]
            total_of_round_top_assists_league_1 = variables_json["tops"]["total_of_round_top_assists_league_1"]
            total_of_round_top_assists_league_2 = variables_json["tops"]["total_of_round_top_assists_league_2"]
            total_of_round_top_assists_league_3 = variables_json["tops"]["total_of_round_top_assists_league_3"]
            total_of_round_top_assists_league_4 = variables_json["tops"]["total_of_round_top_assists_league_4"]
            total_of_round_top_assists_league_5 = variables_json["tops"]["total_of_round_top_assists_league_5"]
            total_of_round_top_saves_league_1 = variables_json["tops"]["total_of_round_top_saves_league_1"]
            total_of_round_top_saves_league_2 = variables_json["tops"]["total_of_round_top_saves_league_2"]
            total_of_round_top_saves_league_3 = variables_json["tops"]["total_of_round_top_saves_league_3"]
            total_of_round_top_saves_league_4 = variables_json["tops"]["total_of_round_top_saves_league_4"]
            total_of_round_top_saves_league_5 = variables_json["tops"]["total_of_round_top_saves_league_5"]
            city_next_round = variables_json["tops"]["city_next_round"]
            h3_team_names_list =variables_json["tops"]["h3_team_names_list"]
            h3_names_list =variables_json["tops"]["h3_names_list"]
            h3_fixture_match_list = variables_json["tops"]["h3_fixture_match_list"].replace("[", "").replace("]", "").replace("'", "").replace(",", "")
            h3_amounts_list = variables_json["tops"]["h3_amounts_list"].replace("[", "").replace("]", "").replace("'", "").replace(",", "").split()

            h3_fixture_match_list = h3_fixture_match_list.split()
            h3_names_list = h3_names_list.replace("+", " ").split()
            h3_team_names_list = h3_team_names_list.replace("+", " ").split()
            h3_names_list = replace_new_list(h3_names_list)
            h3_team_names_list = replace_new_list(h3_team_names_list)

            f = variables_json["tops"]["f_table"]
            date_next_round = variables_json["next_round"]["date_next_round"]
            date_next_round = datetime.strptime(date_next_round, "%Y-%m-%dT%H:%M")

            arena_next_round = variables_json["next_round"]["arena_next_round"]
            first_team_home_next_round = variables_json["next_round"]["first_team_home_next_round"]
            first_team_away_next_round = variables_json["next_round"]["first_team_away_next_round"]
            
            list_date = [date_next_round]
            ycard_for_top3_1 = ''
            ycard_for_top3_2 = ''
            ycard_for_top3_3 = ''
            if len(ycards_top3_fouls_of_season) == 4:
                ycard_for_top3_1 = ycards_top3_fouls_of_season[:2]
                ycard_for_top3_2 = ycards_top3_fouls_of_season[2:3]
                ycard_for_top3_3 = ycards_top3_fouls_of_season[3:]
            elif len(ycards_top3_fouls_of_season) == 5:
                ycard_for_top3_1 = ycards_top3_fouls_of_season[:2]
                ycard_for_top3_2 = ycards_top3_fouls_of_season[2:4]
                ycard_for_top3_3 = ycards_top3_fouls_of_season[4:]
            elif len(ycards_top3_fouls_of_season) == 3:
                ycard_for_top3_1 = ycards_top3_fouls_of_season[:1]
                ycard_for_top3_2 = ycards_top3_fouls_of_season[1:2]
                ycard_for_top3_3 = ycards_top3_fouls_of_season[2:]


            # with open(
            #         f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_review_round.json'
            # ) as file:
            #     user_text = json.load(file)

            

            """ Получение данных клиента """
            with open(
                    f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json', encoding='utf-8'
            ) as file:
                data_j = json.load(file)



            client_language = data_j['l_version']

            featured_image = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{client_language}_{league_id}_{rounds}_{types}.png"
       
            date_next_round = change_date(list_date, client_language)
            date_next_round = date_next_round[0]
            

            if client_language == 'eng':

                """ H3 """
                for i in range(len(h3_team_names_list)):
                    team_names = h3_team_names_list[i]
                    name_players_for_h3 = h3_names_list[i]
                    if i == 0:
                        h3_fixture = get_data_fix(h3_fixture_match_list[i], team_names.replace("_", " "))
                        team_away = h3_fixture[0]
                        goals_home_h3 = h3_fixture[1]
                        goals_away_h3 = h3_fixture[2]
                        if goals_home_h3 > goals_away_h3:
                            result = 'won'
                        if goals_home_h3 < goals_away_h3:
                            result = 'lost'
                        if goals_home_h3 == goals_away_h3:
                            result = 'make it a draw'

                        h3_leader = f'{name_players_for_h3.replace("_", " ")} (<b>{team_names.replace("_", " ")}</b>) scored {h3_amounts_list[i]} in the match with <b>{team_away.replace("_", " ")}</b>. His team {result} with the final score {goals_home_h3} - {goals_away_h3}.'
                    if i != 0:
                        h3_another = h3_another + f'{name_players_for_h3.replace("_", " ")} ({team_names.replace("_", " ")}) scored {h3_amounts_list[i]}, '
                h3_another = h3_another[:-2] 
                """ TABLE_league """
                tr_1 = (
                        f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Team</b></td>'
                        f'<td><b>Form</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">W</td>'
                        f'<td>D</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">L</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>'
                )
                table = f"<table><tbody>{tr_1}{f}</tbody></table>"

                """ table_round_result """
                tr_1_games = (
                            f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                            f'<td><b>Teams</b></td>'
                            f'<td><b>Result</b></td>'
                            f'</tr>'
                            )
                table_all_matches_round = f"<table><tbody>{tr_1_games}{all_matches_round}</tbody></table>"

                goals = 'goals'
                destroyer_results = ''
                if goals_main_destroyer > goals_rival_destroyer:
                    destroyer_results = 'won'
                elif goals_main_destroyer < goals_rival_destroyer:
                    destroyer_results = 'lost'
                elif goals_main_destroyer == goals_rival_destroyer:
                    destroyer_results = 'make it a draw'

                percent_for_round = ''
                if total_percent_round.find('-'):
                    total_percent_round.replace('-', '')
                    percent_for_round = 'less'
                elif total_percent_round.find('+'):
                    total_percent_round.replace('+', '')
                    percent_for_round = 'more'

                result_game_leader = ''
                if goal_leader > goal_rival:
                    result_game_leader = 'won'
                elif goal_leader < goal_rival:
                    result_game_leader = 'lost'
                elif goal_leader == goal_rival:
                    result_game_leader = 'make it a draw'


            elif client_language == 'ru':

                for i in range(len(h3_team_names_list)):
                    team_names = h3_team_names_list[i]
                    name_players_for_h3 = h3_names_list[i]
                    if i == 0:

                        h3_fixture = get_data_fix(h3_fixture_match_list[i], team_names.replace("_", " "))
                        team_away = h3_fixture[0]
                        goals_home_h3 = h3_fixture[1]
                        goals_away_h3 = h3_fixture[2]
                        if goals_home_h3 > goals_away_h3:
                            result = 'выиграла'
                        if goals_home_h3 < goals_away_h3:
                            result = 'проиграла'
                        if goals_home_h3 == goals_away_h3:
                            result = 'сыграла в ничью'

                        h3_leader = f'{name_players_for_h3.replace("_", " ")} (<b>{team_names.replace("_", " ")}</b>) забил {h3_amounts_list[i]} в матче против <b>{team_away.replace("_", " ")}</b>. Его команда {result} с финальным счетом {goals_home_h3} - {goals_away_h3}.'
                    if i != 0:
                        h3_another = h3_another + f'{name_players_for_h3.replace("_", " ")} ({team_names.replace("_", " ")}) забил {h3_amounts_list[i]}, '
                h3_another = h3_another[:-2] 

                goals = 'голов'
                if '-' in total_percent_round:
                    total_percent_round = total_percent_round.replace('-', '')
                    total_percent_round = total_percent_round + 'меньше'
                elif '+' in total_percent_round:
                    total_percent_round = total_percent_round.replace('+', '')
                    total_percent_round = total_percent_round + 'больше'
                tr_1 = (
                        f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Команда</b></td>'
                        f'<td><b>Форма</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">В</td>'
                        f'<td>Н</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">П</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>'
                )
                table = f"<table><tbody>{tr_1}{f}</tbody></table>"


                tr_1_games = (
                            f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                            f'<td><b>Команды</b></td>'
                            f'<td><b>Результат</b></td>'
                            f'</tr>'
                            )
                table_all_matches_round = f"<table><tbody>{tr_1_games}{all_matches_round}</tbody></table>"

                destroyer_results = ''
                if goals_main_destroyer > goals_rival_destroyer:
                    destroyer_results = 'выиграл'
                elif goals_main_destroyer < goals_rival_destroyer:
                    destroyer_results = 'проиграл'
                elif goals_main_destroyer == goals_rival_destroyer:
                    destroyer_results = 'сыграл в ничью'

                percent_for_round = ''
                if total_percent_round.find('-'):
                    total_percent_round.replace('-', '')
                    percent_for_round = 'меньше'
                elif total_percent_round.find('+'):
                    total_percent_round.replace('+', '')
                    percent_for_round = 'больше'

                result_game_leader = ''
                if goal_leader > goal_rival:
                    result_game_leader = 'выиграл'
                elif goal_leader < goal_rival:
                    result_game_leader = 'проиграл'
                elif goal_leader == goal_rival:
                    result_game_leader = 'сыграл в ничью'

            else:


                tr_1 = (
                        f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Команда</b></td>'
                        f'<td><b>Форма</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">В</td>'
                        f'<td>Н</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">П</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>'
                )
                table = f"<table><tbody>{tr_1}{f}</tbody></table>"


                tr_1_games = (
                            f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                            f'<td><b>Команды</b></td>'
                            f'<td><b>Результат</b></td>'
                            f'</tr>'
                            )
                table_all_matches_round = f"<table><tbody>{tr_1_games}{all_matches_round}</tbody></table>"

                for i in range(len(h3_team_names_list)):
                    team_names = h3_team_names_list[i]
                    name_players_for_h3 = h3_names_list[i]
                    if i == 0:

                        h3_fixture = get_data_fix(h3_fixture_match_list[i], team_names.replace("_", " "))
                        team_away = h3_fixture[0]
                        goals_home_h3 = h3_fixture[1]
                        goals_away_h3 = h3_fixture[2]
                        if goals_home_h3 > goals_away_h3:
                            result = 'won'
                        if goals_home_h3 < goals_away_h3:
                            result = 'lost'
                        if goals_home_h3 == goals_away_h3:
                            result = 'make it a draw'

                        h3_leader = f'{name_players_for_h3.replace("_", " ")} ({team_names.replace("_", " ")}) scored {h3_amounts_list[i]} in the match with {team_away.replace("_", " ")}. His team {result} with the final score {goals_home_h3} - {goals_away_h3}.'
                    if i != 0:
                        h3_another = h3_another + f'{name_players_for_h3.replace("_", " ")} ({team_names.replace("_", " ")}) scored {h3_amounts_list[i]}, '
                h3_another = h3_another[:-2] + "."

                goals = 'goals'


                destroyer_results = ''
                if goals_main_destroyer > goals_rival_destroyer:
                    destroyer_results = 'won'
                elif goals_main_destroyer < goals_rival_destroyer:
                    destroyer_results = 'lost'
                elif goals_main_destroyer == goals_rival_destroyer:
                    destroyer_results = 'make it a draw'

                percent_for_round = ''
                if total_percent_round.find('-'):
                    total_percent_round.replace('-', '')
                    percent_for_round = 'less'
                elif total_percent_round.find('+'):
                    total_percent_round.replace('+', '')
                    percent_for_round = 'more'

                result_game_leader = ''
                if goal_leader > goal_rival:
                    result_game_leader = 'won'
                elif goal_leader < goal_rival:
                    result_game_leader = 'lost'
                elif goal_leader == goal_rival:
                    result_game_leader = 'make it a draw'

            list_who_scored_of_round_name = []
            list_who_scored_of_round_amount = []

            total_of_round = [total_name_top_goals_league_1_round, total_name_top_goals_league_2_round,
                              total_name_top_goals_league_3_round, total_name_top_goals_league_4_round,
                              total_name_top_goals_league_5_round]
            top5_name = [name_top_goals_league_1, name_top_goals_league_2, name_top_goals_league_3,
                         name_top_goals_league_4, name_top_goals_league_5]

            for i in range(len(top5_name)):
                if int(total_of_round[i]) > 0:
                    list_who_scored_of_round_name.append(top5_name[i])
                    list_who_scored_of_round_amount.append(total_of_round[i])

            list_who_scored_of_round_result = ''
            for i in range(len(list_who_scored_of_round_name)):
                list_who_scored_of_round_result = list_who_scored_of_round_result + f' {list_who_scored_of_round_name[i]} ({list_who_scored_of_round_amount[i]} {goals}), '
            list_who_scored_of_round_result = list_who_scored_of_round_result[:-2] + '.'

            name_top3_fouls_of_season = name_top3_fouls_of_season.replace("+", " ").split()
            name_top3_fouls_of_season = replace_new_list(name_top3_fouls_of_season)

            name_teams_cards_top3_fouls_of_season = name_teams_cards_top3_fouls_of_season.replace("+", " ").split()
            name_teams_cards_top3_fouls_of_season = replace_new_list(name_teams_cards_top3_fouls_of_season)

            """
            l1 - переменные в тексте
            l2 - статические перемнные с значением
            """

            l1 = ['{rounds}', '{league_name}', '{all_rounds}', '{team_home_leader}', '{team_away_rival}',
                  '{goal_leader}', '{goal_rival}', '{table_all_matches_round}', '{count_home}', '{count_away}',
                  '{count_draw}', '{h3_leader}', '{h3_another}', '{all_goals_round}', '{all_penalty_round}',
                  '{total_percent_round}', '{average_goals_in_season}', '{average_penalty_in_season}',
                  '{time_fast_goal}', '{name_fast_goal}', '{team_name_fast_goal}', '{team_away_fast_goal}',
                  '{scrore_fast_goal}', '{team_top_destroyer}', '{destroyer_interceptions}', '{destroyer_blocks}',
                  '{destroyer_tackles}', '{destroyer_saves}', '{amount_max_destroyer}', '{team_main_destroyer}',
                  '{team_rival_destroyer}', '{goals_main_destroyer}', '{goals_rival_destroyer}',
                  '{max_destroyer_of_season_name}', '{max_destroyer_of_season_amount}', '{team_top_creator}',
                  '{creator_duels}', '{creator_shots_on_target}', '{creator_shots_off_target}', '{amount_max_creator}',
                  '{team_main_creator}', '{team_rival_creator}', '{goals_main_creator}', '{goals_rival_creator}',
                  '{max_creator_of_season_name}', '{max_creator_of_season_amount}', '{name_max_accurate_in_round}',
                  '{max_accurate_in_round}', '{max_total_passes_with_accurate_in_round}',
                  '{name_max_accuracy_in_season}', '{percent_max_accuracy_in_season}', '{name_min_accurate_in_round}',
                  '{min_accurate_in_round}', '{name_min_accuracy_in_season}',
                  '{min_total_passes_with_accurate_in_round}', '{percent_min_accuracy_in_season}',
                  '{name_max_saves_of_round}', '{main_team_max_saves}', '{round_max_saves_of_round}',
                  '{amount_max_saves_of_round}', '{rival_team_max_saves}', '{goals_and_info_max_saves}',
                  '{top_fouls_total_yel_card}', '{top_fouls_total_red_card}', '{top_fouls_team_name_home}',
                  '{top_fouls_team_name_away}', '{top_fouls_goals_home}', '{top_fouls_goals_away}',
                  '{name_top3_fouls_of_season}', '{ycards_top3_fouls_of_season}', '{rcards_top3_fouls_of_season}',
                  '{name_teams_cards_top3_fouls_of_season}', '{round_injuries}', '{average_injuries_in_round}',
                  '{top_round_injuries_name_team}', '{top_round_injuries_amount}', '{name_top_goals_league_1}',
                  '{name_top_goals_league_2}', '{name_top_goals_league_3}', '{name_top_goals_league_4}',
                  '{name_top_goals_league_5}', '{goals_top_league_1}', '{goals_top_league_2}', '{goals_top_league_3}',
                  '{goals_top_league_4}', '{goals_top_league_5}', '{team_top_goals_league1_1}',
                  '{team_top_goals_league2_1}', '{team_top_goals_league3_1}', '{team_top_goals_league4_1}',
                  '{team_top_goals_league5_1}', '{name_top_assists_league_1}', '{assists_top_league_1}',
                  '{team_top_assists_league1}', '{name_top_assists_league_2}', '{assists_top_league_2}',
                  '{team_top_assists_league2}', '{name_top_assists_league_3}', '{assists_top_league_3}',
                  '{team_top_assists_league3}', '{name_top_assists_league_4}', '{assists_top_league_4}',
                  '{team_top_assists_league4}', '{name_top_assists_league_5}', '{assists_top_league_5}',
                  '{team_top_assists_league5}', '{name_top_saves_league_1}', '{saves_top_league_1}',
                  '{team_top_saves_league1}', '{name_top_saves_league_2}', '{saves_top_league_2}',
                  '{team_top_saves_league2}', '{name_top_saves_league_3}', '{saves_top_league_3}',
                  '{team_top_saves_league3}', '{name_top_saves_league_4}', '{saves_top_league_4}',
                  '{team_top_saves_league4}', '{name_top_saves_league_5}', '{saves_top_league_5}',
                  '{team_top_saves_league5}', '{total_name_top_goals_league_1_round}',
                  '{total_name_top_goals_league_2_round}', '{total_name_top_goals_league_3_round}',
                  '{total_name_top_goals_league_4_round}', '{total_name_top_goals_league_5_round}',
                  '{total_of_round_top_assists_league_1}', '{total_of_round_top_assists_league_2}',
                  '{total_of_round_top_assists_league_3}', '{total_of_round_top_assists_league_4}',
                  '{total_of_round_top_assists_league_5}', '{total_of_round_top_saves_league_1}',
                  '{total_of_round_top_saves_league_2}', '{total_of_round_top_saves_league_3}',
                  '{total_of_round_top_saves_league_4}', '{total_of_round_top_saves_league_5}', '{date_next_round}',
                  '{arena_next_round}', '{first_team_home_next_round}', '{first_team_away_next_round}',
                  '{list_who_scored_of_round_result}', '{result_game_leader}', '{table}',
                  '{name_top3_fouls_of_season[0]}', '{name_top3_fouls_of_season[1]}', '{name_top3_fouls_of_season[2]}',
                  '{ycard_for_top3_1}', '{ycard_for_top3_2}',
                  '{ycard_for_top3_3}', '{rcards_top3_fouls_of_season[0]}',
                  '{rcards_top3_fouls_of_season[1]}', '{rcards_top3_fouls_of_season[2]}',
                  '{name_teams_cards_top3_fouls_of_season[0]}', '{name_teams_cards_top3_fouls_of_season[1]}',
                  '{name_teams_cards_top3_fouls_of_season[2]}', '{destroyer_results}', '{date_game_max_saves}', '{city_next_round}']
            l2 = [rounds, league_name, all_rounds, team_home_leader, team_away_rival, goal_leader, goal_rival,
                  table_all_matches_round, count_home, count_away, count_draw, h3_leader, h3_another, all_goals_round,
                  all_penalty_round, total_percent_round, average_goals_in_season, average_penalty_in_season,
                  time_fast_goal, name_fast_goal, team_name_fast_goal, team_away_fast_goal, scrore_fast_goal,
                  team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves,
                  amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer,
                  goals_rival_destroyer, max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator,
                  creator_duels, creator_shots_on_target, creator_shots_off_target, amount_max_creator,
                  team_main_creator, team_rival_creator, goals_main_creator, goals_rival_creator,
                  max_creator_of_season_name, max_creator_of_season_amount, name_max_accurate_in_round,
                  max_accurate_in_round, max_total_passes_with_accurate_in_round, name_max_accuracy_in_season,
                  percent_max_accuracy_in_season, name_min_accurate_in_round, min_accurate_in_round,
                  name_min_accuracy_in_season, min_total_passes_with_accurate_in_round, percent_min_accuracy_in_season,
                  name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, amount_max_saves_of_round,
                  rival_team_max_saves, goals_and_info_max_saves, top_fouls_total_yel_card, top_fouls_total_red_card,
                  top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away,
                  name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season,
                  name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,
                  top_round_injuries_name_team, top_round_injuries_amount, name_top_goals_league_1,
                  name_top_goals_league_2, name_top_goals_league_3, name_top_goals_league_4, name_top_goals_league_5,
                  goals_top_league_1, goals_top_league_2, goals_top_league_3, goals_top_league_4, goals_top_league_5,
                  team_top_goals_league1_1, team_top_goals_league2_1, team_top_goals_league3_1,
                  team_top_goals_league4_1, team_top_goals_league5_1, name_top_assists_league_1, assists_top_league_1,
                  team_top_assists_league1, name_top_assists_league_2, assists_top_league_2, team_top_assists_league2,
                  name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4,
                  assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5,
                  team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1,
                  name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3,
                  saves_top_league_3, team_top_saves_league3, name_top_saves_league_4, saves_top_league_4,
                  team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5,
                  total_name_top_goals_league_1_round, total_name_top_goals_league_2_round,
                  total_name_top_goals_league_3_round, total_name_top_goals_league_4_round,
                  total_name_top_goals_league_5_round, total_of_round_top_assists_league_1,
                  total_of_round_top_assists_league_2, total_of_round_top_assists_league_3,
                  total_of_round_top_assists_league_4, total_of_round_top_assists_league_5,
                  total_of_round_top_saves_league_1, total_of_round_top_saves_league_2,
                  total_of_round_top_saves_league_3, total_of_round_top_saves_league_4,
                  total_of_round_top_saves_league_5, date_next_round, arena_next_round, first_team_home_next_round,
                  first_team_away_next_round, list_who_scored_of_round_result, result_game_leader, table,
                  name_top3_fouls_of_season[0], name_top3_fouls_of_season[1], name_top3_fouls_of_season[2],
                  ycard_for_top3_1, ycard_for_top3_2, ycard_for_top3_3,
                  rcards_top3_fouls_of_season[0], rcards_top3_fouls_of_season[1], rcards_top3_fouls_of_season[2],
                  name_teams_cards_top3_fouls_of_season[0], name_teams_cards_top3_fouls_of_season[1],
                  name_teams_cards_top3_fouls_of_season[2], destroyer_results, date_game_max_saves, city_next_round]

            title, text_all = main_change_text(client_language, 'round', 'review', False, list_id[global_for])
            for i in range(len(l1)):
                """_____
                Замена переменых в тексте на значение
                _____"""

                if l1[i] in text_all:
                    text_all = text_all.replace(l1[i], str(l2[i]))
                if l1[i] in title:
                    title = title.replace(l1[i], str(l2[i]))

            if "<b>" in title and "</b>" in title:
                title = title.replace("<b>", "").replace("</b>", "")

            """_____
            Делаем публикацию
            _____"""
            result_publish = publish(list_id[global_for], league_name, featured_image, title, text_all, types, rounds, client_language, league_id)
            try:
                if 'telegram' in data_j['auto-posting'] and result_publish != False:

                    """ Получение текста """
                    with open(
                            f'/opt/footballBot/parameters/football/users/text/{client_language}_review_round_tg.json') as file:
                        tg_json = json.load(file)

                    text_for_tg = tg_json['main_text']

                    league_name_tg = league_name.replace(" ", "") if ' ' in league_name else league_name

                    """ Добавление переменных """
                    l_new = ['{league_name_tg}', '{url_publ}',
                             '{title}', '{all_matches_round_tg}']
                    l2_new = [f"{league_name_tg}2022",
                              result_publish['link'], title, all_matches_round_tg]
                    l_tags = ['<b>', '<p>', '<li>', '</b>', '</p>', '</li>', '<ul>', '</ul>', '<tr>', '<td>', '</td>']

                    for i in range(len(l_new)):
                        l2.append(l2_new[i])
                        l1.append(l_new[i])

                    """ Замена переменных на данных в тексте """
                    for i in range(len(l1)):
                        if l1[i] in text_for_tg:
                            text_for_tg = text_for_tg.replace(l1[i], str(l2[i]))

                    """ Замена тега </li> на 'пропуск строки' """
                    for i_t in range(len(l_tags)):
                        if l_tags[i_t] in text_for_tg:
                            if l_tags[i_t] == '</li>' or l_tags[i_t] == '</td>':tag = '\n' 
                            else: tag = ''
                            text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

                    """ Отправка в телегам """
                    bot_send_message_tg(featured_image,
                                        data_j['auto-posting']['telegram']['token'],
                                        data_j['auto-posting']['telegram']['channel'],
                                        text_for_tg)
            except Exception:
                continue



        elif types == 'preview':

            # for game in variables_json:
            rounds_for_text = variables_json['title']['rounds']
            # print(rounds_for_text)
            league_id = variables_json['title']['league_id']
            all_rounds = variables_json['title']['all_rounds']
            city_first_match = variables_json['subtitle']['city']
            venue_first_match = variables_json['subtitle']['venue']
            first_date_round = variables_json['subtitle']['first_date']
            home_first_match = variables_json['subtitle']['home_first_match']
            away_first_match = variables_json['subtitle']['away_first_match']
            all_home_teams = variables_json['subtitle']['all_home_teams']
            all_away_teams = variables_json['subtitle']['all_away_teams']

            team_name_max_injuries = variables_json['team_stat']['team_name_injuries']
            max_injuries = variables_json['team_stat']['max_injuries']
            team_max_goals_league = variables_json['team_stat']['team_max_goals_league']
            max_goals_league = variables_json['team_stat']['max_goals_league']
            team_min_conceded_league = variables_json['team_stat']['team_min_conceded_league']
            min_conceded_top_saves = variables_json['team_stat']['min_conceded_top_saves'],
            best_team_of_the_season = variables_json['team_stat']['best_team_of_the_season']
            team_max_clean_sheet_league = variables_json['team_stat']['team_max_clean_sheet_league']
            max_cleen_sheet_league = variables_json['team_stat']['max_cleen_sheet_league']
            team_max_conceded_league = variables_json['team_stat']['team_max_conceded_league']
            max_conceded_saves_league = variables_json['team_stat']['max_conceded_saves_league']
            team_min_goals_attack_league = variables_json['team_stat']['team_min_goals_attack_league']
            min_goals_attack_league = variables_json['team_stat']['min_goals_attack_league']
            team_max_without_scored_league = variables_json['team_stat']['team_max_without_scored_league']
            max_without_scored_league = variables_json['team_stat']['max_without_scored_league']
            wins_without_scored = variables_json['team_stat']['wins_without_scored']
            loses_without_scored = variables_json['team_stat']['loses_without_scored']
            draws_without_scored = variables_json['team_stat']['draws_without_scored']
            team_max_conceded_goals_league = variables_json['team_stat']['team_max_conceded_goals_league']
            max_conceded_goals_league = variables_json['team_stat']['max_conceded_goals_league']
            wins_conceded_goals = variables_json['team_stat']['wins_conceded_goals']
            loses_conceded_goals = variables_json['team_stat']['loses_conceded_goals']
            draws_conceded_goals = variables_json['team_stat']['draws_conceded_goals']
            goals_top_league_1 = variables_json['players_stat']['goals_top_league_1']
            name_top_goals_league_1 = variables_json['players_stat']['name_top_goals_league_1']
            goals_top_league_2 = variables_json['players_stat']['goals_top_league_2']
            name_top_goals_league_2 = variables_json['players_stat']['name_top_goals_league_2']
            goals_top_league_3 = variables_json['players_stat']['goals_top_league_3']
            name_top_goals_league_3 = variables_json['players_stat']['name_top_goals_league_3']
            goals_top_league_4 = variables_json['players_stat']['goals_top_league_4']
            name_top_goals_league_4 = variables_json['players_stat']['name_top_goals_league_4']
            goals_top_league_5 = variables_json['players_stat']['goals_top_league_5']
            name_top_goals_league_5 = variables_json['players_stat']['name_top_goals_league_5']
            assists_top_league_1 = variables_json['players_stat']['assists_top_league_1']
            name_top_assists_league_1 = variables_json['players_stat']['name_top_assists_league_1']
            assists_top_league_2 = variables_json['players_stat']['assists_top_league_2']
            name_top_assists_league_2 = variables_json['players_stat']['name_top_assists_league_2']
            assists_top_league_3 = variables_json['players_stat']['assists_top_league_3']
            name_top_assists_league_3 = variables_json['players_stat']['name_top_assists_league_3']
            assists_top_league_4 = variables_json['players_stat']['assists_top_league_4']
            name_top_assists_league_4 = variables_json['players_stat']['name_top_assists_league_4']
            assists_top_league_5 = variables_json['players_stat']['assists_top_league_5']
            name_top_assists_league_5 = variables_json['players_stat']['name_top_assists_league_5']
            saves_top_league_1 = variables_json['players_stat']['saves_top_league_1']
            name_top_saves_league_1 = variables_json['players_stat']['name_top_saves_league_1']
            saves_top_league_2 = variables_json['players_stat']['saves_top_league_2']
            name_top_saves_league_2 = variables_json['players_stat']['name_top_saves_league_2']
            saves_top_league_3 = variables_json['players_stat']['saves_top_league_3']
            name_top_saves_league_3 = variables_json['players_stat']['name_top_saves_league_3']
            saves_top_league_4 = variables_json['players_stat']['saves_top_league_4']
            name_top_saves_league_4 = variables_json['players_stat']['name_top_saves_league_4']
            saves_top_league_5 = variables_json['players_stat']['saves_top_league_5']
            name_top_saves_league_5 = variables_json['players_stat']['name_top_saves_league_5']

            league_name = variables_json['title']['league_name']
            odds_win_home = variables_json['BK']['odds_win_home']
            odds_win_away = variables_json['BK']['odds_win_away']
            odds_draw = variables_json['BK']['odds_draw']
            top_win_home = variables_json['BK']['top_win_home']
            top_lose_home = variables_json['BK']['top_lose_home']
            top_draw = variables_json['BK']['top_draw']
            count_matchs = variables_json['subtitle']['count_matchs']

            main_match_for_bk_team_home = variables_json['BK']['main_match_for_bk_team_home']
            main_match_for_bk_team_away = variables_json['BK']['main_match_for_bk_team_away']
            rank_for_team_home = variables_json['BK']['rank_for_team_home']
            rank_for_team_away = variables_json['BK']['rank_for_team_away']
            points_for_team_home = variables_json['BK']['points_for_team_home']
            points_for_team_away = variables_json['BK']['points_for_team_away']
            date_previous_match = variables_json['BK']['date_previous_match']
            away_previous_match = variables_json['BK']['away_previous_match']  # ПОка не нужен
            goals_home_previous_match = variables_json['BK']['goals_home_previous_match']
            goals_away_previous_match = variables_json['BK']['goals_away_previous_match']

            team_top_goals_league1 = variables_json['players_stat']['team_top_goals_league1']
            team_top_goals_league2 = variables_json['players_stat']['team_top_goals_league2']
            team_top_goals_league3 = variables_json['players_stat']['team_top_goals_league3']
            team_top_goals_league4 = variables_json['players_stat']['team_top_goals_league4']
            team_top_goals_league5 = variables_json['players_stat']['team_top_goals_league5']
            team_top_assists_league1 = variables_json['players_stat']['team_top_assists_league1']
            team_top_assists_league2 = variables_json['players_stat']['team_top_assists_league2']
            team_top_assists_league3 = variables_json['players_stat']['team_top_assists_league3']
            team_top_assists_league4 = variables_json['players_stat']['team_top_assists_league4']
            team_top_assists_league5 = variables_json['players_stat']['team_top_assists_league5']
            team_top_saves_league1 = variables_json['players_stat']['team_top_saves_league1']
            team_top_saves_league2 = variables_json['players_stat']['team_top_saves_league2']
            team_top_saves_league3 = variables_json['players_stat']['team_top_saves_league3']
            team_top_saves_league4 = variables_json['players_stat']['team_top_saves_league4']
            team_top_saves_league5 = variables_json['players_stat']['team_top_saves_league5']
            preview_home_teams = variables_json['subtitle']['all_home_teams']
            preview_away_teams = variables_json['subtitle']['all_away_teams']
            date_matches = variables_json['subtitle']['date_matches']
            t = variables_json['f']
            preview_home_teams = preview_home_teams.replace("+", " ").replace("'", "").replace(",", "").replace("[","").replace("]", "").split()
            preview_away_teams = preview_away_teams.replace("+", " ").replace("'", "").replace(",", "").replace("[","").replace("]", "").split()
            first_date_round = first_date_round.replace(" ", "T")
            date_previous_match = date_previous_match.replace(" ", "T")
            first_date_round = datetime.strptime(first_date_round[:16], "%Y-%m-%dT%H:%M")  # .strftime('%B %d %Y')
            date_previous_match = datetime.strptime(date_previous_match[:16], "%Y-%m-%dT%H:%M")  # .strftime('%B %d %Y')
            date_matches = date_matches.replace("+", " ").replace("_", "T").split()

            list_date = [first_date_round, date_previous_match]

            preview_home_teams_new = []
            preview_away_teams_new = []

            for i in range(len(preview_home_teams)):

                if '_' in preview_home_teams[i]:
                    new1 = preview_home_teams[i].replace("_", " ")
                    preview_home_teams_new.append(new1)
                else:
                    preview_home_teams_new.append(preview_home_teams[i])

            for i in range(len(preview_away_teams)):

                if '_' in preview_away_teams[i]:
                    new2 = preview_away_teams[i].replace("_", " ")
                    preview_away_teams_new.append(new2)

                else:
                    preview_away_teams_new.append(preview_away_teams[i])

            odds_win_home = odds_win_home.replace(",", "").split()
            odds_win_away = odds_win_away.replace(",", "").split()
            odds_draw = odds_draw.replace(",", "").split()

            """ Получение данных клиента """
            with open(
                    f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json'
                    # f'/Applications/BotBot/work_rep/new/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json'
            ) as file:
                data_j = json.load(file)

            """ Получение текста юзера """
            with open(
                    f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_preview_round.json', encoding='utf-8'
            ) as file:
                user_text = json.load(file)


            client_language = data_j['l_version']

            featured_image = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{client_language}_{league_id}_{rounds}_{types}.png"

            result_list_date = change_date(list_date, client_language)
            date_matches = change_date(date_matches, client_language)


            first_date_round, date_previous_match = result_list_date[0], result_list_date[1]

            # TABLE
            data_for_title_matches = ''

            for matches in range(len(preview_home_teams_new)):
                date_for_table = date_matches[matches]
                # data_for_title_matches = data_for_title_matches + f"<li>{preview_home_teams_new[matches]} - {preview_away_teams_new[matches]} ({date_matches[matches]}), general odds: home win <b>{odds_win_home[matches]}</b>, draw <b>{odds_draw[matches]}</b>, away win <b>{odds_win_away[matches]}</b></li><br>"
                data_for_title_matches = data_for_title_matches + f"<tr><td>{preview_home_teams_new[matches]} - {preview_away_teams_new[matches]}</td><td>{date_for_table}</td><td><b>{odds_win_home[matches]}</b></td><td><b>{odds_draw[matches]}</b></td><td><b>{odds_win_away[matches]}</b></td></tr>"

            data_for_title_matches_tg = ''
            for matches in range(len(preview_home_teams_new)):
                date_for_table = date_matches[matches]
                # data_for_title_matches = data_for_title_matches + f"<li>{preview_home_teams_new[matches]} - {preview_away_teams_new[matches]} ({date_matches[matches]}), general odds: home win <b>{odds_win_home[matches]}</b>, draw <b>{odds_draw[matches]}</b>, away win <b>{odds_win_away[matches]}</b></li><br>"
                data_for_title_matches_tg = data_for_title_matches_tg + f"{matches+1}. *{preview_home_teams_new[matches]}* - *{preview_away_teams_new[matches]}*\n{date_for_table}\n{odds_win_home[matches]} (HW) - {odds_draw[matches]} (D) - {odds_win_away[matches]} (AW)\n\n"

            # ENG
            if client_language == 'eng':
                tr_1 = (f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Team</b></td>'
                        f'<td><b>Form</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">W</td>'
                        f'<td>D</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">L</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>')

                table = f"<table><tbody>{tr_1}{t}</tbody></table>"

                data_for_title_matches = '<table  valign="top"><tbody><tr style= "background-color: #aedbea;"><th rowspan="2">Teams</th><th rowspan="2">Date</th><th colspan="3" rowspan="1">odds</th></tr><tr style= "background-color: #aedbea;"><th>HW</th><th>D</th><th>AW</th></tr>' + data_for_title_matches + '<tr><b><i>HW - home win, AW - away win, D - draw.</i></b></tr></tbody></table>'
                if goals_home_previous_match > goals_away_previous_match:
                    replace_text = main_match_for_bk_team_home + ' won the previous match between this team'
                elif goals_home_previous_match == goals_away_previous_match:
                    replace_text = 'Both teams played draw last time'
                elif goals_home_previous_match < goals_away_previous_match:
                    replace_text = ''
            # RU
            elif client_language == 'ru':
                tr_1 = (f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Команда</b></td>'
                        f'<td><b>Форма</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">В</td>'
                        f'<td>Н</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">П</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>')

                table = f"<table><tbody>{tr_1}{t}</tbody></table>"

                data_for_title_matches = '<table  valign="top"><tbody><tr style= "background-color: #aedbea;"><th rowspan="2">Команды</th><th rowspan="2">Дата</th><th colspan="3" rowspan="1">Коэффициенты</th></tr><tr style= "background-color: #aedbea;"><th>HW</th><th>D</th><th>AW</th></tr>' + data_for_title_matches + '<tr><b><i>HW - победа хоязев, AW - победа гостей, D - ничья.</i></b></tr></tbody></table>'
                if goals_home_previous_match > goals_away_previous_match:
                    replace_text = main_match_for_bk_team_home + ' выиграл предыдущий матч между этой командой'
                elif goals_home_previous_match == goals_away_previous_match:
                    replace_text = 'Обе команды в прошлый раз сыграли вничью'
                elif goals_home_previous_match < goals_away_previous_match:
                    replace_text = ''

            # ENG standart
            else:
                tr_1 = (f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
                        f'<td>#</td>'
                        f'<td></td>'
                        f'<td><b>Team</b></td>'
                        f'<td><b>Form</b></td>'
                        f'<td>PL</td>'
                        f'<td style= "background-color: #4a9460;">W</td>'
                        f'<td>D</td>'  # style= "background-color: #9f9c98;"
                        f'<td style= "background-color: #a13c3c;">L</td>'
                        f'<td>GF</td>'
                        f'<td>GA</td>'
                        f'<td>GD</td>'
                        f'<td>Pts</td>'
                        f'</tr>')

                table = f"<table><tbody>{tr_1}{t}</tbody></table>"

                data_for_title_matches = '<table  valign="top"><tbody><tr style= "background-color: #aedbea;"><th rowspan="2">Teams</th><th rowspan="2">Date</th><th colspan="3" rowspan="1">odds</th></tr><tr style= "background-color: #aedbea;"><th>HW</th><th>D</th><th>AW</th></tr>' + data_for_title_matches + '<tr><b><i>HW - home win, AW - away win, D - draw.</i></b></tr></tbody></table>'
                if goals_home_previous_match > goals_away_previous_match:
                    replace_text = main_match_for_bk_team_home + ' won the previous match between this team'
                elif goals_home_previous_match == goals_away_previous_match:
                    replace_text = 'Both teams played draw last time'
                elif goals_home_previous_match < goals_away_previous_match:
                    replace_text = ''

            count_matchs2 = ''
            if count_matchs == '0':
                count_matchs2 = ''
            elif count_matchs != '0':
                count_matchs2 = f'<p>Some matches will be rescheduled to a later date. Amount rescheduled games {count_matchs}.</p>\n'
            #добавить доп инфу
            match_postned = ''
            if count_matchs != '':
                match_postned = ''

            l1 = ['{best_team_of_the_season}','{count_matchs}', '{rounds_for_text}', '{league_id}', '{city_first_match}', '{venue_first_match}',
                  '{first_date_round}', '{home_first_match}', '{away_first_match}', '{all_home_teams}',
                  '{all_away_teams}', '{team_name_max_injuries}', '{max_injuries}', '{team_max_goals_league}',
                  '{max_goals_league}', '{team_min_conceded_league}', '{min_conceded_top_saves}',
                  '{team_max_clean_sheet_league}', '{max_cleen_sheet_league}', '{team_max_conceded_league}',
                  '{max_conceded_saves_league}', '{team_min_goals_attack_league}', '{min_goals_attack_league}',
                  '{team_max_without_scored_league}', '{max_without_scored_league}', '{wins_without_scored}',
                  '{loses_without_scored}', '{draws_without_scored}', '{team_max_conceded_goals_league}',
                  '{max_conceded_goals_league}', '{wins_conceded_goals}', '{loses_conceded_goals}',
                  '{draws_conceded_goals}', '{goals_top_league_1}', '{name_top_goals_league_1}', '{goals_top_league_2}',
                  '{name_top_goals_league_2}', '{goals_top_league_3}', '{name_top_goals_league_3}',
                  '{goals_top_league_4}', '{name_top_goals_league_4}', '{goals_top_league_5}',
                  '{name_top_goals_league_5}', '{assists_top_league_1}', '{name_top_assists_league_1}',
                  '{assists_top_league_2}', '{name_top_assists_league_2}', '{assists_top_league_3}',
                  '{name_top_assists_league_3}', '{assists_top_league_4}', '{name_top_assists_league_4}',
                  '{assists_top_league_5}', '{name_top_assists_league_5}', '{saves_top_league_1}',
                  '{name_top_saves_league_1}', '{saves_top_league_2}', '{name_top_saves_league_2}',
                  '{saves_top_league_3}', '{name_top_saves_league_3}', '{saves_top_league_4}',
                  '{name_top_saves_league_4}', '{saves_top_league_5}', '{name_top_saves_league_5}', '{league_name}',
                  '{odds_win_home}', '{odds_win_away}', '{odds_draw}', '{top_win_home}', '{top_lose_home}',
                  '{top_draw}', '{team_top_goals_league1}', '{team_top_goals_league2}', '{team_top_goals_league3}',
                  '{team_top_goals_league4}', '{team_top_goals_league5}', '{team_top_assists_league1}',
                  '{team_top_assists_league2}', '{team_top_assists_league3}', '{team_top_assists_league4}',
                  '{team_top_assists_league5}', '{team_top_saves_league1}', '{team_top_saves_league2}',
                  '{team_top_saves_league3}', '{team_top_saves_league4}', '{team_top_saves_league5}',
                  '{preview_home_teams}', '{preview_away_teams}', '{date_matches}', '{table}',
                  '{main_match_for_bk_team_home}', '{main_match_for_bk_team_away}', '{rank_for_team_home}',
                  '{rank_for_team_away}', '{points_for_team_home}', '{points_for_team_away}', '{date_previous_match}',
                  '{away_previous_match}', '{goals_home_previous_match}', '{goals_away_previous_match}',
                  '{replace_text}', '{data_for_title_matches}']
            l2 = [best_team_of_the_season, count_matchs2, rounds_for_text, league_id, city_first_match, venue_first_match, first_date_round,
                  home_first_match, away_first_match, all_home_teams, all_away_teams, team_name_max_injuries,
                  max_injuries, team_max_goals_league, max_goals_league, team_min_conceded_league,
                  min_conceded_top_saves, team_max_clean_sheet_league, max_cleen_sheet_league, team_max_conceded_league,
                  max_conceded_saves_league, team_min_goals_attack_league, min_goals_attack_league,
                  team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored,
                  draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals,
                  loses_conceded_goals, draws_conceded_goals, goals_top_league_1, name_top_goals_league_1,
                  goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3,
                  goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5,
                  assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2,
                  assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4,
                  assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1,
                  saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3,
                  saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, league_name,
                  odds_win_home, odds_win_away, odds_draw, top_win_home, top_lose_home, top_draw,
                  team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4,
                  team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3,
                  team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2,
                  team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, preview_home_teams,
                  preview_away_teams, date_matches, table, main_match_for_bk_team_home, main_match_for_bk_team_away,
                  rank_for_team_home, rank_for_team_away, points_for_team_home, points_for_team_away,
                  date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match,
                  replace_text, data_for_title_matches]

            if data_j["custom"] == "": title, text_all = main_change_text(client_language, 'round', 'preview', False, list_id[global_for])
            elif data_j["custom"] != "": title, text_all = main_change_text(client_language, 'round', 'preview', True, list_id[global_for])

            for i in range(len(l1)):
                if l1[i] in text_all:
                    text_all = text_all.replace(l1[i], str(l2[i]))
                if l1[i] in title:
                    title = title.replace(l1[i], l2[i])
            if "<b>" in title and "</b>" in title:
                title = title.replace("<b>", "").replace("</b>", "")
            """_____
            Делаем публикацию
            _____"""
            result_publish = publish(list_id[global_for], league_name, featured_image, title, text_all, types, rounds, client_language, league_id)
            # print(result_publish)

            if 'telegram' in data_j['auto-posting'] and result_publish != False:

                """ Получение текста """
                with open(
                        f'/opt/footballBot/parameters/football/users/text/{client_language}_preview_round_tg.json') as file:
                    tg_json = json.load(file)

                text_for_tg = tg_json['main_text']

                league_name_tg = league_name.replace(" ", "") if ' ' in league_name else league_name

                """ Добавление переменных """
                l_new = ['{league_name_tg}', '{url_publ}',
                         '{title}', '{data_for_title_matches_tg}']
                l2_new = [f"{league_name_tg}2022",
                          result_publish['link'], title, data_for_title_matches_tg]
                l_tags = ['<i>HW - home win, AW - away win, D - draw.</i></tbody></table>','<table  valign="top"><tbody><tr style= "background-color: #aedbea;"><th rowspan="2">Teams</th><th rowspan="2">Date</th><th colspan="3" rowspan="1">odds</th></tr><tr style= "background-color: #aedbea;"><th>HW</th><th>D</th><th>AW</th></tr>','<b>', '<p>', '<li>', '</b>', '</p>', '</li>', '<ul>', '</ul>', '<tr>', '<td>', '</td>', '</tr>' ]

                for i in range(len(l_new)):
                    l2.append(l2_new[i])
                    l1.append(l_new[i])

                """ Замена переменных на данных в тексте """
                for i in range(len(l1)):
                    if l1[i] in text_for_tg:
                        text_for_tg = text_for_tg.replace(l1[i], str(l2[i]))

                """ Замена тега </li> на 'пропуск строки' """
                for i_t in range(len(l_tags)):
                    if l_tags[i_t] in text_for_tg:
                        # tag = '\n' if l_tags[i_t] == '</li>' or l_tags[i_t] == '</td>' else tag = ''
                        # or l_tags[i_t] == '</td>'
                        if l_tags[i_t] == '</li>':tag = '\n'
                        else: tag = ''
                        text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

                """ Отправка в телегам """
                bot_send_message_tg(featured_image,
                                    data_j['auto-posting']['telegram']['token'],
                                    data_j['auto-posting']['telegram']['channel'],
                                    text_for_tg)
# main_publication('19', 'review', '39')
