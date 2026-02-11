import os
from time import sleep
import requests
import json
import base64
from datetime import datetime, timedelta
#import datetime
# from db_for_app import get_user_id_main
import psycopg2
# from db_for_app import get_data
from publication.change_text import main_change_text
from publication.db_for_app import bot_send_message_tg, upload_image_to_wordpress, writesonic
# publication


#         media = {'file': open(f'/opt/footballBot/result/img_match/{fixture_match}_{types}.png', 'rb'),'caption': f'{fixture_match}_{types}'}
#         responce = requests.post(url + "wp-json/wp/v2/media", headers = header_json, files = media)
#         r = responce.json()
#         return r['id']


def change_date(list_date, l_version):

    returned_date = []

    """ Открытие JSON """
    with open(
              f'/opt/footballBot/parameters/football/users/dicts/months_for_users.json'
              ) as file:
        month_json = json.load(file)

    for i in range(len(list_date)):
        date = list_date[i]
        if ' ' in str(list_date[i]):
            date = str(list_date[i]).replace(" ", "T")
        if date != '':
            month = month_json[l_version][date[5:7]]
            day = date[8:10]
            time = date[11:16]
            year = date[0:4]

            if l_version == 'ru':
                returned_date.append(f'{day} {month} в {time} (UTC)')
            else:
                returned_date.append(f'{month} {day} at {time} (UTC)')
        else: returned_date.append('')
    return returned_date

def get_data(insert_query):
    try:
        connection = psycopg2.connect (
            host='localhost',
            user = 'db_user',
            password = 'pass',
            database = 'db_match'
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def get_user_id_main(type_subscribe):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host='localhost',
            user='db_user',
            password='pass',
            database='main'
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT id_user FROM subscribe WHERE type_subscribe LIKE '{type_subscribe}';"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            l=[]
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

def publish(id, league_name, team_name_home, team_name_away, featured_image, title, text_all, types, fixture_match, l_version):  # list_id[global_for]
    """
    Получаем информацию по клиенту и делаем публикацию
    """
    with open(
            f'/opt/footballBot/parameters/football/users/parameters/{id}.json'
    ) as file:
        data_j = json.load(file)

    platform_name = data_j['platform_name']

    if platform_name == 'wordpress':

        url = data_j['platform_url']
        user = data_j['platform_user']
        password = data_j['platform_password']
        type_status = data_j['type_status']
        data_tags = data_j['list_id']

        credentials = user + ':' + password
        """
        Получение категории (Как правило Лиги)
        """
        category, tags = '', ''
        if league_name in data_j['list_id']:

            category = data_j['list_id'][league_name]['id']
            # получение id команд тега

            team1_tags, team2_tags = '', ''

            if team_name_home in data_j['list_id'][league_name]: team1_tags = data_j['list_id'][league_name][team_name_home]
            if team_name_away in data_j['list_id'][league_name]: team2_tags = data_j['list_id'][league_name][team_name_away]

            # Создания тега
            if team1_tags != "": tags = team1_tags
            if team2_tags != "": tags = team2_tags
            if team1_tags != "" and team2_tags != "": tags = [team1_tags, team2_tags]

        if data_j['category_id'] != "" \
                and category != "": category = [category, data_j['category_id']]
        elif category == "" \
                and data_j['category_id'] != "": category = data_j['category_id']

        types_for_publish = data_j['subscribe']['football'][league_name]['types']
        list_teams_for_publish = data_j['subscribe']['football'][league_name]['teams']

        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}


        if types + "_match" in types_for_publish \
                or types_for_publish == 'all':
            if team_name_home in list_teams_for_publish \
                    or team_name_away in list_teams_for_publish \
                    or list_teams_for_publish == 'all':
                if data_j['featured_image'] == 'upload':

                    """ upload image to wordpress """
                    img_id = upload_image_to_wordpress(
                        f'/opt/footballBot/result/img_match/{l_version}_{fixture_match}_{types}.png',
                        url.replace('posts', 'media'),
                        header, fixture_match
                    )

                    post = {
                        'title': title,
                        'status': f'{type_status}',  # тип
                        'content': text_all,
                        'categories': category,  # category ID
                        'tags': tags,
                        'featured_media': img_id
                    }

                elif data_j['featured_image'] == 'url':
                    post = {
                        'title': title,
                        'status': f'{type_status}',  # тип
                        'content': text_all,
                        'categories': category,  # category ID
                        'tags': tags,
                        # 'date'   : f'{date}',   # время публикации --  {время матча - один день}
                        'meta': {'_knawatfibu_url': featured_image}
                    }

                else:
                    post = {
                        'title': title,
                        'status': f'{type_status}',  # тип
                        'content': text_all,
                        'categories': category,  # category ID
                        'tags': tags,
                        # 'date'   : f'{date}',   # время публикации --  {время матча - один день}
                        'meta': {'_knawatfibu_url': featured_image}
                    }

                responce = requests.post(url, headers=header, json=post).json()

                print(f"[INFO]  posted")
                return responce
                # if 'twitter' in data_j['auto-posting']:
                #     bot_send_twitter(title, responce_json['content']['raw'][:100], league_name, responce_json['link'], featured_image, team_name_home, team_name_away, [data_j['twitter']['api_key'], data_j['twitter']['api_secrets'], data_j['twitter']['access_token'], data_j['twitter']['access_secrets']])
        return False


def main_publication(fixture_match, types):

    list_id = get_user_id_main('football')

    for global_for in range(len(list_id)):
        
        with open(f'/opt/footballBot/result/json/{fixture_match}_{types}.json') as file:
            text = json.load(file)
        # featured_image_url = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_{types}.png"

        if types == "review":
            img_graph = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_graph_{types}.png\" alt=\"\">"
            img_lineups = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_lineups_{types}.png\" alt=\"\">"
            for game in text:
                team1= game['title']['team_a']
                team2= game['title']['team_b']
                goals_a= game['title']['goal_a']
                goals_b= game['title']['goal_b']
                league_name1 = game['title']['league_name']
                lineups_a=game['subtitle_lineups']['lineups_a']
                lineups_b=game['subtitle_lineups']['lineups_b']
                lineups_in_game_a=game['subtitle_lineups']['lineups_in_game_a']
                lineups_in_game_b=game['subtitle_lineups']['lineups_in_game_b']
                total_shots_off=game['goals_scorers']['goals']['total_shots_off']
                total_shots_on=game['goals_scorers']['goals']['total_shots_on']
                shots_team1_off=game['goals_scorers']['goals']['shots_team1_off']
                shots_team1_on=game['goals_scorers']['goals']['shots_team1_on']
                active_shots_player_home=game['goals_scorers']['goals']['active_shots_player_home']
                shots_team2_off=game['goals_scorers']['goals']['shots_team2_off']
                shots_team2_on=game['goals_scorers']['goals']['shots_team2_on']
                active_shots_player_away=game['goals_scorers']['goals']['active_shots_player_away']
                total_assists_home=game['goals_scorers']['goals']['total_assists_home']
                total_assists_away=game['goals_scorers']['goals']['total_assists_away']
                total_interceptions_home=game['goals_scorers']['defensive']['total_interceptions_home']
                name_top_inceptions_home=game['goals_scorers']['defensive']['name_top_inceptions_home']
                amount_interceptions_home=game['goals_scorers']['defensive']['amount_interceptions_home']
                total_inteceptions_away=game['goals_scorers']['defensive']['total_inteceptions_away']
                name_top_inceptions_away=game['goals_scorers']['defensive']['name_top_inceptions_away']
                amount_interseptions_away=game['goals_scorers']['defensive']['amount_interseptions_away']
                total_blocks_home=game['goals_scorers']['defensive']['total_blocks_home']
                name_top_blocks_home=game['goals_scorers']['defensive']['name_top_blocks_home']
                amount_blocks_home=game['goals_scorers']['defensive']['amount_blocks_home']
                total_blocks_away=game['goals_scorers']['defensive']['total_blocks_away']
                name_top_blocks_away=game['goals_scorers']['defensive']['name_top_blocks_away']
                amount_blocks_away=game['goals_scorers']['defensive']['amount_blocks_away']
                name_duels_team1=game['goals_scorers']['duels']['name_duels_team1']
                amount_duels_team1=game['goals_scorers']['duels']['amount_duels_team1']
                name_duels_team2=game['goals_scorers']['duels']['name_duels_team2']
                amount_duels_team2=game['goals_scorers']['duels']['amount_duels_team2']
                possession_team1=game['goals_scorers']['ball_pos']['possession_team1']
                possession_team2=game['goals_scorers']['ball_pos']['possession_team2']
                first_top_name=game['top_players_league']['top3']['first_top_name']
                first_top_team=game['top_players_league']['top3']['first_top_team']
                first_top_amount=game['top_players_league']['top3']['first_top_amount']
                second_top_name=game['top_players_league']['top3']['second_top_name']
                second_top_team=game['top_players_league']['top3']['second_top_team']
                second_top_amount=game['top_players_league']['top3']['second_top_amount']
                
                third_top_name=game['top_players_league']['top3']['third_top_name']
                third_top_team=game['top_players_league']['top3']['third_top_team']
                third_top_amount=game['top_players_league']['top3']['third_top_amount']
                next_match_team1_with=game['next_matches']['show_next_matches']['next_match_team1_with']
                next_match_team1_date=game['next_matches']['show_next_matches']['next_match_team1_date']
                next_match_team1_venue=game['next_matches']['show_next_matches']['next_match_team1_venue']
                next_match_team2_with=game['next_matches']['show_next_matches']['next_match_team2_with']
                next_match_team2_date=game['next_matches']['show_next_matches']['next_match_team2_date']
                next_match_team2_venue=game['next_matches']['show_next_matches']['next_match_team2_venue']
                arena= game['title']['venue']
                date= game['title']['date_match3']
                form_home= game['title']['form_home']
                form_away= game['title']['form_away']
                fourth_top_name=game['top_players_league']['top3']['fourth_top_name']
                fourth_top_team=game['top_players_league']['top3']['fourth_top_team']
                fourth_top_amount=game['top_players_league']['top3']['fourth_top_amount']
                fifth_top_name=game['top_players_league']['top3']['fifth_top_name']
                fifth_top_team=game['top_players_league']['top3']['fifth_top_team']
                fifth_top_amount=game['top_players_league']['top3']['fifth_top_amount']
                rank = ''
                all_games = ''
                l = []
                win_games = ''
                draw_games = ''
                lose_games = ''
                goals_for = ''
                goals_missed = ''
                goals_diff = ''
                points = ''
                name_teams = ''
                form_all = ''
                logo_table= ''

                name_home_top_pass_accuracy = game['goals_scorers']['passes']['name_home_top_pass_accuracy']
                top__home_precent_accuracy = game['goals_scorers']['passes']['top__home_precent_accuracy']
                top__home_total_passes = game['goals_scorers']['passes']['top__home_total_passes']
                name_away_top_pass_accuracy = game['goals_scorers']['passes']['name_away_top_pass_accuracy']
                top__away_precent_accuracy = game['goals_scorers']['passes']['top__away_precent_accuracy']
                top__away_total_passes = game['goals_scorers']['passes']['top__away_total_passes']
                name_home_top_pass_key = game['goals_scorers']['passes']['name_home_top_pass_key']
                top__home_amount_key = game['goals_scorers']['passes']['top__home_amount_key']
                name_away_top_pass_key = game['goals_scorers']['passes']['name_away_top_pass_key']
                top__away_amount_key = game['goals_scorers']['passes']['top__away_amount_key']


                

                #logo_table = str(logo_table).replace("+", " ")
                # print(logo_table[0].replace("+", " "))

            # import json
            
            with open(f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json') as file:
                user = json.load(file)

            with open(f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_review_match.json') as file:
                main_text = json.load(file)

            with open(f'/opt/footballBot/parameters/football/users/dicts/wc_teams.json') as file:
                teams_for_cup = json.load(file)

            y_cards_title = main_text['y_cards']
            r_cards_title = main_text['r_cards']
            fouls_title = main_text['fouls_title']
            penalties_title = main_text['penalties_title']
            goalscorers = main_text['goalscorers']

            l_version = user['l_version']
            print(l_version)

            
            insert_query = (
                f"SELECT * FROM match_review WHERE fixture_match_for_check={fixture_match}"
            )

            index = get_data(insert_query)
            index = index[0]

            fixture_match, name_home_review, name_away_review, lineups_home, lineups_away, gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key = \
            index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14], index[15], index[16], index[17], index[18], index[19],index[20], index[21], index[22], index[23], index[24], index[25], index[26], index[27], index[28], index[29], index[30], index[31], index[32], index[33], index[34], index[35], index[36], index[37], index[38],index[39], index[40], index[41], index[42], index[43], index[44], index[45], index[46], index[47], index[48], index[49], index[50], index[51], index[52], index[53], index[54], index[55], index[56], index[57],index[58], index[59], index[60], index[61], index[62], index[63], index[64], index[65], index[66], index[67], index[68], index[69], index[70], index[71], index[72], index[73], index[74], index[75], index[76],index[77], index[78], index[79], index[80], index[81], index[82], index[83], index[84], index[85], index[86], index[87], index[88], index[89], index[90], index[91], index[92], index[93], index[94], index[95],index[96], index[97], index[98], index[99], index[100], index[101], index[102], index[103], index[104],index[105], index[106], index[107], index[108], index[109], index[110], index[111], index[112], index[113],index[114], index[115], index[116], index[117], index[118], index[119], index[120], index[121], index[122],index[123], index[124], index[125], index[126], index[127], index[128], index[129], index[130], index[131],index[132]

            time_home_goal = time_home_goal.split()
            time_away_goal = time_away_goal.split()
            time_home_penalti = time_home_penalti.split()
            time_away_penalti = time_away_penalti.split()
            player_home_goal = str(player_home_goal).replace("+", " ")
            player_away_goal = str(player_away_goal).replace("+", " ")
            player_away_goal = player_away_goal.split()
            player_home_goal = player_home_goal.split()
            time_home_yellow = time_home_yellow.split()
            time_away_yellow = time_away_yellow.split()
            time_home_red = time_home_red.split()
            time_away_red = time_away_red.split()
            player_home_yellow = str(player_home_yellow).replace("+", " ").split()
            player_away_yellow = str(player_away_yellow).replace("+", " ").split()
            player_home_red = str(player_home_red).replace("+", " ").split()
            player_away_red = str(player_away_red).replace("+", " ").split()
            player_home_penalti = str(player_home_penalti).replace("+", " ")
            player_home_penalti = player_home_penalti.split()
            player_away_penalti = str(player_away_penalti).replace("+", " ")
            player_away_penalti = player_away_penalti.split()

            """ Получение данных клиента """
            with open(
                    f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json', encoding='utf-8'
            ) as file:
                data_j = json.load(file)
            
            client_language = data_j['l_version']
            featured_image_url = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{client_language}_{fixture_match}_{types}.png"
            summ_shorts_target = int(shots_team1_off) + int(shots_team2_off)
            if l_version == 'eng':
                if goals_a > goals_b:

                    """ home win """
                    var_for_title_1 = f'{team1} vs {team2} {goals_a}:{goals_b}. The winner made {shots_team1_off} shots on target'
                    var_for_title_2 = f'{team1} won the game with {team2}. Final score — {goals_a}:{goals_b}'
                    var_for_title_3 = f'{team2} lost the game with {team1}. The score — {goals_a}:{goals_b}'


                elif goals_a < goals_b:
                    """ away win """
                    var_for_title_1 = f'{team1} vs {team2} {goals_a}:{goals_b}. The winner made {shots_team2_off} shots on target'
                    var_for_title_2 = f'{team2} won the game with {team1}. Final score — {goals_a}:{goals_b}'
                    var_for_title_3 = f'{team1} lost the game with {team2}. The score — {goals_a}:{goals_b}'


                elif goals_a == goals_b:
                    """ draw """
                    var_for_title_1 = f'{team1} and {team2} made it draw today. Final score — {goals_a}:{goals_b}'
                    var_for_title_2 = f'{team1} and {team2} made it draw today. Final score — {goals_a}:{goals_b}'
                    var_for_title_3 = f'{team1} and {team2} made it draw today. Final score — {goals_a}:{goals_b}'
#
                goal_all_time = ''
                first_goal = ''
                index = 0
                index_home = 0
                index_away = 0
                if time_home_goal != [] and time_away_goal != []:
                    if int(time_home_goal[index]) < int(time_away_goal[index]):
                        first_goal = f'{player_home_goal[0]} drop first goal at {time_home_goal[0]} minute of the match.'
                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        first_goal = f'{player_away_goal[0]} drop first goal at {time_away_goal[0]} minute of the match.'
                elif time_home_goal != [] and time_away_goal == []:
                    first_goal = f'{player_home_goal[0]} drop first goal at {time_home_goal[0]} minute of the match.'
                elif time_home_goal == [] and time_away_goal != []:
                    first_goal = f'{player_away_goal[0]} drop first goal at {time_away_goal[0]} minute of the match.'
                else:
                    goal_all_time = ''
                    first_goal = ''
                

                while len(player_home_goal) + len(player_away_goal) != 0:
                    
                    if time_home_goal == []:
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> at {time_away_goal[index]} minute ({index_home} : {index_away}) (<b>{team2}</b>)</li>'
                        del time_away_goal[index], player_away_goal[index]

                    elif time_away_goal == []:
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) < int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> at {time_away_goal[index]} minute ({index_home} : {index_away}) ({team2})</li>'
                        del time_away_goal[index], player_away_goal[index]

                    elif int(time_home_goal[index]) == int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                
                yellow_card_home = ''
                for yel_cards_home in range(len(time_home_yellow)):
                    yellow_card_home += '<li>' + ' ' + '<b>' + player_home_yellow[yel_cards_home].replace("_"," ") + '</b>' + ' (' + team1 + ') at ' + \
                                        time_home_yellow[yel_cards_home] + ' minute </li> '

                yellow_card_away = ''
                for yel_cards_away in range(len(time_away_yellow)):
                    yellow_card_away += '<li>' + ' ' + '<b>' + player_away_yellow[yel_cards_away].replace("_"," ") + '</b>' + ' (' + team2 + ') at ' + \
                                        time_away_yellow[yel_cards_away] + ' minute </li> '

                red_card_home = ''
                for red_cards_home in range(len(time_home_red)):
                    red_card_home += '<li>' + ' ' + '<b>' + player_home_red[red_cards_home].replace("_"," ") + '</b>' + ' (' + team1 + ') at ' + \
                                     time_home_red[red_cards_home] + ' minute </li> '

                red_card_away = ''
                for red_cards_away in range(len(time_away_red)):
                    red_card_away += '<li>' + ' ' + '<b>' + player_away_red[red_cards_away].replace("_"," ") + '</b>' + ' (' + team2 + ') at ' + \
                                     time_away_red[red_cards_away] + ' minute </li> '

                penalti_home = ''
                for penalti_home_cycle in range(len(time_home_penalti)):
                    penalti_home += '<li>' + ' ' + '<b>' + player_home_penalti[penalti_home_cycle].replace("_"," ") + '</b>' + ' (' + team1 + ') at ' + \
                                    time_home_penalti[penalti_home_cycle] + ' minute </li> '

                penalti_away = ''
                for penalti_away_cycle in range(len(time_away_penalti)):
                    penalti_away += '<li>' + ' ' + '<b>' + player_away_penalti[penalti_away_cycle].replace("_"," ") + '</b>' + ' (' + team2 + ') at ' + \
                                    time_away_penalti[penalti_away_cycle] + ' minute </li> '


            list_teams =[fifth_top_team, fourth_top_team, third_top_team, second_top_team, first_top_team]
            list_teams_new =[]
            if l_version == 'ru':

                if goals_a > goals_b:
                    """ home win """
                    var_for_title_1 = f'{team1} нанёс {shots_team1_off} ударов по воротам соперника'
                    var_for_title_2 = f'{team1} выиграл матч с {team2}. Счёт — {goals_a}:{goals_b}'
                    var_for_title_3 = f'{team2} проиграла свой матч с {team1} — {goals_a}:{goals_b}'


                elif goals_a < goals_b:
                    """ away win """
                    var_for_title_1 = f'{team2} нанёс {shots_team2_off} ударов по воротам соперника'
                    var_for_title_2 = f'{team2} выиграл матч с {team1}. Счёт — {goals_b}:{goals_a}'
                    var_for_title_3 = f'{team1} проиграла свой матч с {team2} — {goals_b}:{goals_a}'


                elif goals_a == goals_b:
                    """ draw """
                    var_for_title_1 = f'{team1} и {team2} сыграли сегодня вничью со счётом {goals_a}:{goals_b}'
                    var_for_title_2 = f'{team1} и {team2} сыграли сегодня вничью со счётом {goals_a}:{goals_b}'
                    var_for_title_3 = f'{team1} и {team2} сыграли сегодня вничью со счётом {goals_a}:{goals_b}'

                lineups_a = lineups_a.replace('rating', 'рейтинг')
                lineups_b = lineups_b.replace('rating', 'рейтинг')
                if league_name1 == 'World Cup':
                    for i in range(len(list_teams)):
                        if list_teams[i] != '':
                            list_teams_new.append(teams_for_cup[l_version][list_teams[i]])
                        else:
                            list_teams_new.append(list_teams[i])
                    fifth_top_team, fourth_top_team, third_top_team, second_top_team, first_top_team = list_teams_new
                    team1,team2 = teams_for_cup[l_version][team1], teams_for_cup[l_version][team2]
                    if next_match_team1_with != '': next_match_team1_with = teams_for_cup[l_version][next_match_team1_with]
                    if next_match_team2_with != '': next_match_team2_with = teams_for_cup[l_version][next_match_team2_with]

                goal_all_time = ''
                first_goal = ''
                index = 0
                index_home = 0
                index_away = 0
                if time_home_goal != [] and time_away_goal != []:
                    if int(time_home_goal[index]) < int(time_away_goal[index]):
                        first_goal = f'{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча.'
                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        first_goal = f'{player_away_goal[0]} забил первый гол на {time_away_goal[0]} минуте матча.'
                elif time_home_goal != [] and time_away_goal == []:
                    first_goal = f'{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча.'
                elif time_home_goal == [] and time_away_goal != []:
                    first_goal = f'{player_away_goal[0]} забил первый гол на {time_away_goal[0]} минуте матча.'
                else:
                    goal_all_time = ''
                    first_goal = ''

                while len(player_home_goal) + len(player_away_goal) != 0:
                    if time_home_goal == []:
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> на {time_away_goal[index]} минуте ({index_home} : {index_away}) ({team2})</li>'
                        del time_away_goal[index], player_away_goal[index]

                    elif time_away_goal == []:
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) < int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> на {time_away_goal[index]} минуте ({index_home} : {index_away}) ({team2})</li>'
                        del time_away_goal[index], player_away_goal[index]

                    elif int(time_home_goal[index]) == int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        del time_home_goal[index], player_home_goal[index]

                yellow_card_home = ''
                for yel_cards_home in range(len(time_home_yellow)):
                    yellow_card_home += '<li>' + ' ' + '<b>' + player_home_yellow[yel_cards_home].replace("_"," ") + '</b>' + ' (' + team1 + ') на ' + \
                                        time_home_yellow[yel_cards_home] + ' минуте </li> '

                yellow_card_away = ''
                for yel_cards_away in range(len(time_away_yellow)):
                    yellow_card_away += '<li>' + ' ' + '<b>' + player_away_yellow[yel_cards_away].replace("_"," ") + '</b>' + ' (' + team2 + ') на ' + \
                                        time_away_yellow[yel_cards_away] + ' минуте </li> '

                red_card_home = ''
                for red_cards_home in range(len(time_home_red)):
                    red_card_home += '<li>' + ' ' + '<b>' + player_home_red[red_cards_home].replace("_"," ") + '</b>' + ' (' + team1 + ') на ' + \
                                     time_home_red[red_cards_home] + ' минуте </li> '

                red_card_away = ''
                for red_cards_away in range(len(time_away_red)):
                    red_card_away += '<li>' + ' ' + '<b>' + player_away_red[red_cards_away].replace("_"," ") + '</b>' + ' (' + team2 + ') на ' + \
                                     time_away_red[red_cards_away] + ' минуте </li> '

                penalti_home = ''
                for penalti_home_cycle in range(len(time_home_penalti)):
                    penalti_home += '<li>' + ' ' + '<b>' + player_home_penalti[penalti_home_cycle].replace("_"," ") + '</b>' + ' (' + team1 + ') на ' + \
                                    time_home_penalti[penalti_home_cycle] + ' минуте </li> '

                penalti_away = ''
                for penalti_away_cycle in range(len(time_away_penalti)):
                    penalti_away += '<li>' + ' ' + '<b>' + player_away_penalti[penalti_away_cycle].replace("_", " ") + '</b>' + ' (' + team2 + ') на ' + \
                                    time_away_penalti[penalti_away_cycle] + ' минуте </li> '

                
            first_goal = first_goal.replace('_', ' ')
            all_scorers = goal_all_time.replace("_", "")

            fouls_yel_team1 = yellow_card_home
            fouls_yel_team2 = yellow_card_away
            fouls_red_team1 = red_card_home
            fouls_red_team2 = red_card_away
            penalti_home = penalti_home
            penalti_away = penalti_away


            yellow_card = f"{y_cards_title}<p>{fouls_yel_team1} {fouls_yel_team2}</p>"
            red_card = f"{r_cards_title}<p>{fouls_red_team1} {fouls_red_team2}</p>"

            fouls_y_card = ''
            fouls_r_card = ''

            if fouls_yel_team1 != '' or fouls_yel_team2 != '' or fouls_red_team1 != '' or fouls_red_team2 != '':
                title3 = f"{fouls_title}"

                if fouls_yel_team1 != '' or fouls_yel_team2 != '':
                    fouls_y_card = f'{yellow_card}'
                elif fouls_yel_team1 == '' and fouls_yel_team2 == '':
                    fouls_y_card = ''

                if fouls_red_team1 != '' or fouls_red_team2 != '':
                    fouls_r_card = f"{red_card}"
                elif fouls_red_team1 == '' and fouls_red_team2 == '':
                    fouls_r_card = ''
                fouls = f"{fouls_y_card}{fouls_r_card}"
            else:
                fouls = f""
                title3 = ''
            if penalti_home != '' or penalti_away != '':
                title2 = f"{penalties_title}"

                if penalti_home != '':
                    penalti_home = f'{penalti_home}'
                elif penalti_home == '':
                    penalti_home = ''

                if penalti_away != '':
                    penalti_away = f"{penalti_away}"
                elif penalti_away == '':
                    penalti_away = ''

                penalti = f"{penalti_home}{penalti_away}"
            else:
                penalti = ''
                title2 = ''
            if all_scorers != '':
                title1 = f'{goalscorers}'
                goals = f"<p>{all_scorers}</p>"
            else:
                title1 = ''
                goals = ''

            list_date = [next_match_team1_date, next_match_team2_date]
            date = change_date(list_date, l_version)
            next_match_team1_date, next_match_team2_date = date[0], date[1]

            if data_j["custom"] == "": title, text_all = main_change_text(l_version, 'match', 'review', False, list_id[global_for])
            elif data_j["custom"] != "": title, text_all = main_change_text(l_version, 'match', 'review', True, list_id[global_for])

            l2 = [var_for_title_1, var_for_title_2, var_for_title_3, summ_shorts_target, team1, team2, goals_a, goals_b, league_name1,lineups_a, lineups_b, lineups_in_game_a, lineups_in_game_b, first_goal,all_scorers,total_shots_off ,total_shots_on, shots_team1_off, shots_team1_on,active_shots_player_home,shots_team2_off,shots_team2_on, active_shots_player_away, total_assists_home, total_assists_away, total_interceptions_home,name_top_inceptions_home , amount_interceptions_home,total_inteceptions_away, name_top_inceptions_away, amount_interseptions_away, total_blocks_home, name_top_blocks_home, amount_blocks_home, total_blocks_away, name_top_blocks_away, amount_blocks_away, name_duels_team1, amount_duels_team1, name_duels_team2, amount_duels_team2,possession_team1,possession_team1 , possession_team2, first_top_name, first_top_team,first_top_amount, second_top_name, second_top_name, second_top_team, second_top_amount, third_top_name,fourth_top_team, fourth_top_amount, fifth_top_name, fifth_top_team, fifth_top_amount, rank, all_games,third_top_team, third_top_amount, next_match_team1_with,next_match_team1_date, next_match_team1_venue,next_match_team2_with,next_match_team2_date,next_match_team2_venue, arena, date, form_home, form_away, penalti_home, fourth_top_name, form_all, logo_table, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, win_games, draw_games, lose_games, goals_for, goals_missed, goals_diff,points,name_teams, form_all, logo_table, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes,name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, next_match_team1_date, next_match_team2_date, img_graph, img_lineups, yellow_card,red_card, title3, fouls_y_card, fouls_r_card, fouls, title2, penalti_home, penalti, title1, goals]
            l = ['{var_for_title_1}', '{var_for_title_2}', '{var_for_title_3}','{summ_shorts_target}', '{team1}', '{team2}', '{goals_a}', '{goals_b}', '{league_name1}','{lineups_a}', '{lineups_b}', '{lineups_in_game_a}', '{lineups_in_game_b}', '{first_goal}','{all_scorers}','{total_shots_off}' ,'{total_shots_on}', '{shots_team1_off}', '{shots_team1_on}','{active_shots_player_home}','{shots_team2_off}','{shots_team2_on}', '{active_shots_player_away}', '{total_assists_home}', '{total_assists_away}', '{total_interceptions_home}','{name_top_inceptions_home}' , '{amount_interceptions_home}','{total_inteceptions_away}', '{name_top_inceptions_away}', '{amount_interseptions_away}', '{total_blocks_home}', '{name_top_blocks_home}', '{amount_blocks_home}', '{total_blocks_away}', '{name_top_blocks_away}', '{amount_blocks_away}', '{name_duels_team1}', '{amount_duels_team1}', '{name_duels_team2}', '{amount_duels_team2}','{possession_team1}','{possession_team1}' , '{possession_team2}', '{first_top_name}', '{first_top_team}','{first_top_amount}', '{second_top_name}', '{second_top_name}', '{second_top_team}', '{second_top_amount}', '{third_top_name}','{fourth_top_team}', '{fourth_top_amount}', '{fifth_top_name}', '{fifth_top_team}', '{fifth_top_amount}', '{rank}', '{all_games}','{third_top_team}', '{third_top_amount}', '{next_match_team1_with}','{next_match_team1_date}', '{next_match_team1_venue}','{next_match_team2_with}','{next_match_team2_date}','{next_match_team2_venue}', '{arena}', '{date}', '{form_home}', '{form_away}', '{penalti_home}', '{fourth_top_name}', '{form_all}', '{logo_table}', '{name_home_top_pass_accuracy}', '{top__home_precent_accuracy}', '{top__home_total_passes}', '{win_games}', '{draw_games}', '{lose_games}', '{goals_for}', '{goals_missed}', '{goals_diff}','{points}','{name_teams}', '{form_all}', '{logo_table}', '{name_home_top_pass_accuracy}', '{top__home_precent_accuracy}', '{top__home_total_passes}','{name_away_top_pass_accuracy}', '{top__away_precent_accuracy}', '{top__away_total_passes}', '{name_home_top_pass_key}', '{top__home_amount_key}', '{name_away_top_pass_key}', '{top__away_amount_key}', '{next_match_team1_date}', '{next_match_team2_date}', '{img_graph}', '{img_lineups}', '{yellow_card}','{red_card}', '{title3}', '{fouls_y_card}', '{fouls_r_card}', '{fouls}', '{title2}', '{penalti_home}', '{penalti}', '{title1}', '{goals}']

            for i in range(len(l)):
                if l[i] in text_all:
                    text_all = text_all.replace(l[i], str(l2[i]))
                if l[i] in title:
                    title = title.replace(l[i], str(l2[i]))
            if "<b>" in title and "</b>" in title:
                title = title.replace("<b>", "").replace("</b>", "")
            
            # if l_version == 'eng':
            #     text_from_writesonic = writesonic(title)

            #     if '{text_from_writesonic}' in text_all:
            #         text_all = text_all.replace('{text_from_writesonic}', text_from_writesonic)


            """ Публикация статьи """
            result_publish = publish(list_id[global_for], league_name1, team1, team2, featured_image_url, title, text_all, types, fixture_match, l_version)
            #result_publish - responcce_json

            """ Запуск публикации в телеграм если она есть """
            if 'telegram' in data_j['auto-posting'] and result_publish != False:

                """ Получение текста """
                with open(f'/opt/footballBot/parameters/football/users/text/{l_version}_{types}_match_tg.json') as file: tg_json = json.load(file)
                with open(f'/opt/footballBot/parameters/football/users/dicts/flag_for_tg.json', encoding='utf-8') as flag_json: flag_json = json.load(flag_json)

                text_for_tg = tg_json['main_text']

                """ Получение смайлика флаг по обоим командам """
                if league_name in flag_json:
                    if team1 in flag_json[league_name]: flag_team1 = flag_json[league_name][team1]
                    if team2 in flag_json[league_name]: flag_team2 = flag_json[league_name][team2]
                else:
                    flag_team1, flag_team2 = '', ''
                league_name_tg = ''
                if ' ' in league_name:
                    league_name_tg = league_name.replace(" ", "")
                else:
                    league_name_tg = league_name
                """ Добавление переменных """
                l_new = ['{league_name_tg}', '{team1_tg}', '{team2_tg}', '{url_publ}', '{flag_team1}', '{flag_team2}', '{title}']
                l2_new = [f"{league_name_tg}2022", team1.replace(' ', ''), team2.replace(' ', ''), result_publish['link'], flag_team1, flag_team2, title]
                l_tags = ['<b>', '<p>', '<li>','</b>', '</p>', '</li>', '<ul>', '</ul>']

                for i in range(len(l_new)):
                    l2.append(l2_new[i])
                    l.append(l_new[i])

                """ Замена переменных на данных в тексте """
                for i in range(len(l)):
                    if l[i] in text_for_tg:
                        text_for_tg = text_for_tg.replace(l[i], str(l2[i]))

                """ Замена тега </li> на 'пропуск строки' """
                for i_t in range(len(l_tags)):
                    if l_tags[i_t] in text_for_tg:
                        if l_tags[i_t] == '</li>': tag = '\n'
                        else: tag = ''
                        text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

                """ Отправка в телегам """
                bot_send_message_tg(featured_image_url,
                             data_j['auto-posting']['telegram']['token'], data_j['auto-posting']['telegram']['channel'],
                             text_for_tg
                             )


        
        elif types == 'preview':

                    # preview
                # img_graph_preview_home = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/graph_home_{fixture_match}_{types}.png\" alt=\"\">"
                # img_graph_preview_away = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/graph_away_{fixture_match}_{types}.png\" alt=\"\">"

                # Type == Preview
                for game in text:

                    team1 = game['title1']['team_name_home']
                    team2 = game['title1']['team_name_away']
                    date1 = game['subtitle_start']['date']
                    full_date = game['subtitle_start']['full_date']
                    venue1 = game['subtitle_start']['venue']
                    league_name1 = game['standings']['league_name']
                    rank1 = game['standings']['rank_team_home']
                    rank2 = game['standings']['rank_team_away']
                    top_player_a = game['scorers_a_b']['home_top_name']
                    top_home_total = game['scorers_a_b']['home_top_total']
                    top_player_b = game['scorers_a_b']['away_top_name']
                    top_away_total = game['scorers_a_b']['away_top_total']
                    first_in_league_name = game['table_scorers']['first_top_name']
                    first_in_league_team = game['table_scorers']['first_top_team']
                    first_in_league_amount = game['table_scorers']['first_top_amount']
                    second_in_league_name = game['table_scorers']['second_top_name']
                    second_in_league_team = game['table_scorers']['second_top_team']
                    second_in_league_amount = game['table_scorers']['second_top_amount']
                    thrid_in_league_name = game['table_scorers']['third_top_name']
                    thrid_in_league_team = game['table_scorers']['third_top_team']
                    thrid_in_league_amount = game['table_scorers']['third_top_amount']
                    fourth_in_league_name = game['table_scorers']['fourth_top_name']
                    fourth_in_league_team = game['table_scorers']['fourth_top_team']
                    fourth_in_league_amount = game['table_scorers']['fourth_top_amount']
                    fifth_in_league_name = game['table_scorers']['fifth_top_name']
                    fifth_in_league_team = game['table_scorers']['fifth_top_team']
                    fifth_in_league_amount = game['table_scorers']['fifth_top_amount']
                    top_home_assist_name = game['assists']['topscorers_assists_home_name']
                    top_home_assist_amount = game['assists']['topscorers_assists_home_amount']
                    top_away_assist_name = game['assists']['topscorers_assists_away_name']
                    top_away_assist_amount = game['assists']['topscorers_assists_away_amount']
                    top_home_saves_name = game['saves']['topscorers_saves_home_name']
                    top_home_saves_amount = game['saves']['topscorers_saves_home_amount']
                    top_away_saves_name = game['saves']['topscorers_saves_away_name']
                    top_away_saves_amount = game['saves']['topscorers_saves_away_amount']
                    top_home_blocks_name = game['blocks']['topscorers_interceptions_home_name']
                    top_home_blocks_amount = game['blocks']['topscorers_interceptions_home_amount']
                    top_away_blocks_name = game['blocks']['topscorers_interceptions_away_name']
                    top_away_blocks_amount = game['blocks']['topscorers_interceptions_away_amount']
                    top_home_duels_name = game['duels']['topscorers_duels_home_name']
                    top_home_duels_amount = game['duels']['topscorers_duels_home_amount']
                    top_away_duels_name = game['duels']['topscorers_duels_away_name']
                    top_away_duels_amount = game['duels']['topscorers_duels_away_amount']

                    name_home_top_fouls_yel_card = game['fouls']['name_home_top_fouls_yel_card']
                    amount_home_fouls_yel_card = game['fouls']['amount_home_fouls_yel_card']
                    name_away_top_fouls_yel_card = game['fouls']['name_away_top_fouls_yel_card']
                    amount_away_fouls_yel_card = game['fouls']['amount_away_fouls_yel_card']
                    name_home_top_fouls_red_card = game['fouls']['name_home_top_fouls_red_card']
                    amount_home_fouls_red_card = game['fouls']['amount_home_fouls_red_card']
                    name_away_top_fouls_red_card = game['fouls']['name_away_top_fouls_red_card']
                    amount_away_fouls_red_card = game['fouls']['amount_away_fouls_red_card']

                    home_forms = game['team_statistics']['forms']['home']
                    away_forms = game['team_statistics']['forms']['away']
                    clean_home = game['clean_sheet']['home_play_clean_sheet']
                    clean_away = game['clean_sheet']['away_play_clean_sheet']
                    home_biggest_win_in_home = game['biggest']['home']['win']['home']
                    home_biggest_win_in_away = game['biggest']['home']['win']['away']
                    home_biggest_lose_in_home = game['biggest']['lose']['home']
                    home_biggest_lose_in_away = game['biggest']['lose']['away']
                    away_biggest_win_in_home = game['away']['win']['home']
                    away_biggest_win_in_away = game['away']['win']['away']
                    away_biggest_lose_in_home = game['away']['lose']['home']
                    away_biggest_lose_in_away = game['away']['lose']['away']
                    home_win_once_in_home = game['win_once']['home']['win']
                    home_draws_once_in_home = game['win_once']['home']['draws']
                    home_lose_once_in_home = game['win_once']['home']['lose']
                    away_win_once_in_away = game['win_once']['away']['win']
                    away_draws_once_in_away = game['win_once']['away']['draws']
                    away_lose_once_in_away = game['win_once']['away']['lose']
                    for_goals_home = game['goals']['home']['g'].split()
                    missed_goals_home = game['goals']['home']['m'].split()
                    for_goals_away = game['goals']['away']['g'].split()
                    missed_goals_away = game['goals']['away']['m'].split()
                    
                    table_h2h_total_game = game['Table_h2h']['games']
                    home_table_h2h_win_in_home = game['Table_h2h']['team_home']['win_home']
                    home_table_h2h_win_in_away = game['Table_h2h']['team_home']['win_away']
                    home_table_h2h_draws_in_home = game['Table_h2h']['team_home']['draws_home']
                    home_table_h2h_draws_in_away = game['Table_h2h']['team_home']['draws_away']
                    home_table_h2h_lose_in_home = game['Table_h2h']['team_home']['loses_home']
                    home_table_h2h_lose_in_away = game['Table_h2h']['team_home']['loses_away']
                    away_table_h2h_win_in_home = game['Table_h2h']['team_away']['win_home']
                    away_table_h2h_win_in_away = game['Table_h2h']['team_away']['win_away']
                    away_table_h2h_draws_in_home = game['Table_h2h']['team_away']['draws_home']
                    away_table_h2h_draws_in_away = game['Table_h2h']['team_away']['draws_away']
                    away_table_h2h_lose_in_home = game['Table_h2h']['team_away']['loses_home']
                    away_table_h2h_lose_in_away = game['Table_h2h']['team_away']['loses_away']
                    home_comparison_win = game['Сomparison']['table']['team_home']['win']
                    home_comparison_att = game['Сomparison']['table']['team_home']['attack']
                    home_comparison_def = game['Сomparison']['table']['team_home']['def']
                    home_comparison_t2t = game['Сomparison']['table']['team_home']['t2t']
                    home_comparison_goals = game['Сomparison']['table']['team_home']['goals']
                    away_comparison_win = game['Сomparison']['table']['team_away']['win']
                    away_comparison_att = game['Сomparison']['table']['team_away']['attack']
                    away_comparison_def = game['Сomparison']['table']['team_away']['def']
                    away_comparison_t2t = game['Сomparison']['table']['team_away']['t2t']
                    away_comparison_goals = game['Сomparison']['table']['team_away']['goals']
                    predictions_win_home = game['subtitle']['predictions_win_home']
                    predictions_draws = game['subtitle']['predictions_draws']
                    predictions_lose_home = game['subtitle']['predictions_win_away']
                    home_win_or_lose = game['subtitle']['predictions_home_win_or_lose']
                    home_predictions_goals = game['subtitle']['predictions_home_goals']
                    away_predictions_goals = game['subtitle']['predictions_away_goals']
                    bk1_name = game['bk']['table']['bk1']
                    bk1_win_home = game['bk']['table']['bk1_win_home']
                    bk1_draw = game['bk']['table']['bk1_draw']
                    bk1_win_away = game['bk']['table']['bk1_win_away']
                    bk2_name = game['bk']['table']['bk2']
                    bk2_win_home = game['bk']['table']['bk2_win_home']
                    bk2_draw = game['bk']['table']['bk2_draw']
                    bk2_win_away = game['bk']['table']['bk2_win_away']
                    bk3_name = game['bk']['table']['bk3']
                    bk3_win_home = game['bk']['table']['bk3_win_home']
                    bk3_draw = game['bk']['table']['bk3_draw']
                    bk3_win_away = game['bk']['table']['bk3_win_away']
                    list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']

                    home_win_or_lose_ru = game['subtitle']['home_win_or_lose_ru']

                # with open(
                #     f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json', encoding='utf-8'
                # ) as file:
                #     data_j = json.load(file)
                
                with open(f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json') as file:
                    user = json.load(file)
                with open(f'/opt/footballBot/parameters/football/users/dicts/wc_teams.json') as file:
                    teams_for_cup = json.load(file)

                l_version = user['l_version']

                new_date = change_date([full_date], l_version)
                new_date = new_date[0]

                with open(f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_preview_match.json') as file:
                    main_text = json.load(file)

                if l_version == 'ru':
                    home_win_or_lose = home_win_or_lose_ru
                    title_big_home_in_home1 = main_text['title_big_home_in_home'] #f"in the home game, — {title_big_home_in_home1}"             #main_text['title_big_home_in_home']
                    title_big_home_in_away1 = main_text['title_big_home_in_away']
                    title_big_away_in_home1 = main_text['title_big_away_in_home']
                    title_big_home_in_away_AWAY = main_text['title_big_home_in_away_AWAY']

                    if league_name1 == 'World Cup':
                        if team1 in teams_for_cup[l_version]:
                            team1 = teams_for_cup[l_version][team1]
                        if team2 in teams_for_cup[l_version]:
                            team2 = teams_for_cup[l_version][team2]

                elif l_version == 'eng':
                    home_win_or_lose = home_win_or_lose

                title_big_home_in_home1 = main_text['title_big_home_in_home'] #f"in the home game, — {title_big_home_in_home1}"             #main_text['title_big_home_in_home']
                title_big_home_in_away1 = main_text['title_big_home_in_away']
                title_big_away_in_home1 = main_text['title_big_away_in_home']
                title_big_home_in_away_AWAY = main_text['title_big_home_in_away_AWAY']
                    
                if str(home_biggest_win_in_home) == '0':
                    title_big_home_in_home = ''
                else:
                    title_big_home_in_home = f'{title_big_home_in_home1}'

                if str(home_biggest_win_in_home) == '0':
                    title_big_home_in_away = ''
                else:
                    title_big_home_in_away = f'{title_big_home_in_away1}'
                
                if str(away_biggest_win_in_home) == '0':
                    title_big_away_in_home = ''
                else:
                    title_big_away_in_home = f'{title_big_away_in_home1}'
                
                if str(away_biggest_win_in_away) == '0':
                    title_big_home_in_away = ''
                else:
                    title_big_home_in_away = f'{title_big_home_in_away_AWAY}'

                if user['custom'] == "": title, text_all = main_change_text(l_version, 'match', 'preview', False,
                                                                                list_id[global_for])
                if user['custom'] != "": title, text_all = main_change_text(l_version, 'match', 'preview', True,
                                                                                list_id[global_for])

                featured_image_url = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/eng_{fixture_match}_{types}.png"


                l2 = [new_date,team1,team2,date1,full_date,full_date[11:],venue1,league_name1,rank1,rank2,top_player_a,top_home_total,top_player_b,top_away_total,first_in_league_name,first_in_league_team,first_in_league_amount,second_in_league_name,second_in_league_team,second_in_league_amount,thrid_in_league_name,thrid_in_league_team,thrid_in_league_amount,fourth_in_league_name,fourth_in_league_team,fourth_in_league_amount,fifth_in_league_name,fifth_in_league_team,fifth_in_league_amount,top_home_assist_name,top_home_assist_amount,top_away_assist_name,top_away_assist_amount,top_home_saves_name,top_home_saves_amount,top_away_saves_name,top_away_saves_amount,top_home_blocks_name,top_home_blocks_amount,top_away_blocks_name,top_away_blocks_amount,top_home_duels_name,top_home_duels_amount,top_away_duels_name,top_away_duels_amount,name_home_top_fouls_yel_card,amount_home_fouls_yel_card,name_away_top_fouls_yel_card,amount_away_fouls_yel_card,name_home_top_fouls_red_card,amount_home_fouls_red_card,name_away_top_fouls_red_card,amount_away_fouls_red_card,home_forms,away_forms,clean_home,clean_away,home_biggest_win_in_home,home_biggest_win_in_away,home_biggest_lose_in_home,home_biggest_lose_in_away,away_biggest_win_in_home,away_biggest_win_in_away,away_biggest_lose_in_home,away_biggest_lose_in_away,home_win_once_in_home,home_draws_once_in_home,home_lose_once_in_home,away_win_once_in_away,away_draws_once_in_away,away_lose_once_in_away,for_goals_home,for_goals_home[0],for_goals_home[1],for_goals_home[2],for_goals_home[3],for_goals_home[4],for_goals_home[5],for_goals_home[6],missed_goals_home[1],missed_goals_home[0],missed_goals_home[2],missed_goals_home[3],missed_goals_home[4],missed_goals_home[5],missed_goals_home[6],missed_goals_home[7],for_goals_away[0],for_goals_away[1],for_goals_away[2],for_goals_away[3],for_goals_away[4],for_goals_away[5],for_goals_away[6],missed_goals_away[0],missed_goals_away[1],missed_goals_away[2],missed_goals_away[3],missed_goals_away[4],missed_goals_away[5],missed_goals_away[6],table_h2h_total_game,home_table_h2h_win_in_home,home_table_h2h_win_in_away,home_table_h2h_draws_in_home,home_table_h2h_draws_in_away,home_table_h2h_lose_in_home,home_table_h2h_lose_in_away,away_table_h2h_win_in_home,away_table_h2h_win_in_away,away_table_h2h_draws_in_home,away_table_h2h_draws_in_away,away_table_h2h_lose_in_home,away_table_h2h_lose_in_away,home_comparison_win,home_comparison_att,home_comparison_def,home_comparison_t2t,home_comparison_goals,away_comparison_win,away_comparison_att,away_comparison_def,away_comparison_t2t,away_comparison_goals,predictions_win_home,predictions_draws,predictions_lose_home,home_win_or_lose,home_predictions_goals,away_predictions_goals,bk1_name,bk1_win_home,bk1_draw,bk1_win_away,bk2_name,bk2_win_home,bk2_draw,bk2_win_away,bk3_name,bk3_win_home,bk3_draw,bk3_win_away,list_minute[0],list_minute[1],list_minute[2],list_minute[3],list_minute[4],list_minute[5],list_minute[6], title_big_home_in_home, title_big_home_in_away, title_big_away_in_home] #,title_big_home_in_home, title_big_home_in_away, title_big_away_in_home
                l = ['{new_date}','{team1}','{team2}','{date1}','{full_date}','{full_date[11:]}','{venue1}','{league_name1}','{rank1}','{rank2}','{top_player_a}','{top_home_total}','{top_player_b}','{top_away_total}','{first_in_league_name}','{first_in_league_team}','{first_in_league_amount}','{second_in_league_name}','{second_in_league_team}','{second_in_league_amount}','{thrid_in_league_name}','{thrid_in_league_team}','{thrid_in_league_amount}','{fourth_in_league_name}','{fourth_in_league_team}','{fourth_in_league_amount}','{fifth_in_league_name}','{fifth_in_league_team}','{fifth_in_league_amount}','{top_home_assist_name}','{top_home_assist_amount}','{top_away_assist_name}','{top_away_assist_amount}','{top_home_saves_name}','{top_home_saves_amount}','{top_away_saves_name}','{top_away_saves_amount}','{top_home_blocks_name}','{top_home_blocks_amount}','{top_away_blocks_name}','{top_away_blocks_amount}','{top_home_duels_name}','{top_home_duels_amount}','{top_away_duels_name}','{top_away_duels_amount}','{name_home_top_fouls_yel_card}','{amount_home_fouls_yel_card}','{name_away_top_fouls_yel_card}','{amount_away_fouls_yel_card}','{name_home_top_fouls_red_card}','{amount_home_fouls_red_card}','{name_away_top_fouls_red_card}','{amount_away_fouls_red_card}','{home_forms}','{away_forms}','{clean_home}','{clean_away}','{home_biggest_win_in_home}','{home_biggest_win_in_away}','{home_biggest_lose_in_home}','{home_biggest_lose_in_away}','{away_biggest_win_in_home}','{away_biggest_win_in_away}','{away_biggest_lose_in_home}','{away_biggest_lose_in_away}','{home_win_once_in_home}','{home_draws_once_in_home}','{home_lose_once_in_home}','{away_win_once_in_away}','{away_draws_once_in_away}','{away_lose_once_in_away}','{for_goals_home}','{for_goals_home[0]}','{for_goals_home[1]}','{for_goals_home[2]}','{for_goals_home[3]}','{for_goals_home[4]}','{for_goals_home[5]}','{for_goals_home[6]}','{missed_goals_home[1]}','{missed_goals_home[0]}','{missed_goals_home[2]}','{missed_goals_home[3]}','{missed_goals_home[4]}','{missed_goals_home[5]}','{missed_goals_home[6]}','{missed_goals_home[7]}','{for_goals_away[0]}','{for_goals_away[1]}','{for_goals_away[2]}','{for_goals_away[3]}','{for_goals_away[4]}','{for_goals_away[5]}','{for_goals_away[6]}','{missed_goals_away[0]}','{missed_goals_away[1]}','{missed_goals_away[2]}','{missed_goals_away[3]}','{missed_goals_away[4]}','{missed_goals_away[5]}','{missed_goals_away[6]}','{table_h2h_total_game}','{home_table_h2h_win_in_home}','{home_table_h2h_win_in_away}','{home_table_h2h_draws_in_home}','{home_table_h2h_draws_in_away}','{home_table_h2h_lose_in_home}','{home_table_h2h_lose_in_away}','{away_table_h2h_win_in_home}','{away_table_h2h_win_in_away}','{away_table_h2h_draws_in_home}','{away_table_h2h_draws_in_away}','{away_table_h2h_lose_in_home}','{away_table_h2h_lose_in_away}','{home_comparison_win}','{home_comparison_att}','{home_comparison_def}','{home_comparison_t2t}','{home_comparison_goals}','{away_comparison_win}','{away_comparison_att}','{away_comparison_def}','{away_comparison_t2t}','{away_comparison_goals}','{predictions_win_home}','{predictions_draws}','{predictions_lose_home}','{home_win_or_lose}','{home_predictions_goals}','{away_predictions_goals}','{bk1_name}','{bk1_win_home}','{bk1_draw}','{bk1_win_away}','{bk2_name}','{bk2_win_home}','{bk2_draw}','{bk2_win_away}','{bk3_name}','{bk3_win_home}','{bk3_draw}','{bk3_win_away}','{list_minute[0]}','{list_minute[1]}','{list_minute[2]}','{list_minute[3]}','{list_minute[4]}','{list_minute[5]}','{list_minute[6]}' , '{title_big_home_in_home}', '{title_big_home_in_away}', '{title_big_away_in_home}'] #, '{title_big_home_in_home}', '{title_big_home_in_away}', '{title_big_away_in_home}'
                for i in range(len(l)):
                    if l[i] in text_all:
                        text_all = str(text_all).replace(str(l[i]), str(l2[i]))
                    if l[i] in title:
                        title = str(title).replace(l[i], l2[i])
                if "<b>" in title and "</b>" in title:
                    title = title.replace("<b>", "").replace("</b>", "")
                
                # if l_version == 'eng':
                #     text_from_writesonic = writesonic(title)
                    
                #     if '{text_from_writesonic}' in text_all:
                #         text_all = text_all.replace('{text_from_writesonic}', text_from_writesonic)


                result_publish = publish(list_id[global_for], league_name1, team1, team2, featured_image_url, title, text_all, types, fixture_match, l_version)

                if 'telegram' in user['auto-posting'] and result_publish != False:

                    """ Получение текста """
                    with open(f'/opt/footballBot/parameters/football/users/text/{l_version}_preview_match_tg.json') as file: tg_json = json.load(file)
                    with open(f'/opt/footballBot/parameters/football/users/dicts/flag_for_tg.json', encoding='utf-8') as flag_json: flag_json = json.load(flag_json)

                    text_for_tg = tg_json['main_text']

                    """ Получение смайлика флаг по обоим командам """
                    if league_name1 in flag_json:
                        if team1 in flag_json[league_name1]: flag_team1 = flag_json[league_name1][team1]
                        if team2 in flag_json[league_name1]: flag_team2 = flag_json[league_name1][team2]
                    else:
                        flag_team1, flag_team2 = '', ''
                    league_name_tg = ''
                    if ' ' in league_name1:
                        league_name_tg = league_name1.replace(" ", "")
                    else:
                        league_name_tg = league_name1
                    """ Добавление переменных """
                    l_new = ['{league_name_tg}', '{team1_tg}', '{team2_tg}', '{url_publ}', '{flag_team1}', '{flag_team2}', '{title}']
                    l2_new = [f"{league_name_tg}2022", team1.replace(' ', ''), team2.replace(' ', ''), result_publish['link'], flag_team1, flag_team2, title]
                    l_tags = ['<b>', '<p>', '<li>','</b>', '</p>', '</li>', '<ul>', '</ul>']

                    for i in range(len(l_new)):
                        l2.append(l2_new[i])
                        l.append(l_new[i])

                    """ Замена переменных на данных в тексте """
                    for i in range(len(l)):
                        if l[i] in text_for_tg:
                            text_for_tg = text_for_tg.replace(l[i], str(l2[i]))

                    """ Замена тега </li> на 'пропуск строки' """
                    for i_t in range(len(l_tags)):
                        if l_tags[i_t] in text_for_tg:
                            if l_tags[i_t] == '</li>': tag = '\n'
                            else: tag = ''
                            text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

                    """ Отправка в телегам """
                    bot_send_message_tg(featured_image_url,
                                 user['auto-posting']['telegram']['token'], user['auto-posting']['telegram']['channel'],
                                 text_for_tg
                                 )


# main_publication('878093', 'review')
