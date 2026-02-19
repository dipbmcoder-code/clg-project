import os
from time import sleep
import requests
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
# import datetime
# from db_for_app import get_user_id_main
import psycopg2
# from db_for_app import get_data
from publication.change_text import main_change_text
from publication.db_for_app import bot_send_message_tg, upload_image_to_wordpress
from publication.cms_db import decrypt_password
from publication.utils import generate_openai_content, replace_vars
from publication.cms_logs import insert_news_log
import openai
import ast
from dotenv import load_dotenv
load_dotenv()
# publication


#         media = {'file': open(f'/opt/footballBot/result/img_match/{fixture_match}_{types}.png', 'rb'),'caption': f'{fixture_match}_{types}'}
#         responce = requests.post(url + "wp-json/wp/v2/media", headers = header_json, files = media)
#         r = responce.json()
#         return r['id']


def change_date(list_date, l_version):
    returned_date = []

    """ Открытие JSON """
    with open(
            root_folder / 'parameters/football/users/dicts/months_for_users.json'
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
                returned_date.append(f'{day} {month} в {time} (GMT)')
            else:
                returned_date.append(f'{month} {day} at {time} (GMT)')
        else:
            returned_date.append('')
    return returned_date


def get_data(insert_query):
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
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
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
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

def ensure_full_keys(data):
    # Create a dictionary to ensure all indices from 0 to 6 exist
    return data + [''] * (7 - len(data))

def publish(data_j, league_name, team_name_home, team_name_away, featured_image, title, text_all, types, fixture_match,
            l_version, league_id):  # list_id[global_for]
    """
    Получаем информацию по клиенту и делаем публикацию
    """
    # exit()
    # print(league_name)
    # print(l_version)
    img_id = 0
    try:
        platform_name = 'wordpress'
        if platform_name.strip() == 'wordpress':
            url = data_j['platform_url'].strip()
            user = data_j['platform_user'].strip()
            password = data_j['platform_password'].strip()
            type_status = data_j.get('type_status', 'publish')
            #data_tags = data_j['list_id']
            auth_type = data_j.get('auth_type','json')
            application_password = data_j.get('application_password','')
            author = data_j.get('website_author') or []
            decryptPassword = decrypt_password(password)
            if not decryptPassword:
                print(f" Password decryption failed.")
                None
            if auth_type == 'json':
                credentials = user + ':' + decryptPassword
            else:
                credentials = user + ':' + application_password

            category = "1"
            tags = ''
            if data_j['categories']:
                category_ids = [str(category['id']) for category in data_j['categories']]
                category = ','.join(category_ids)
            token = base64.b64encode(credentials.encode())
            header = {'Authorization': 'Basic ' + token.decode('utf-8')}
            feature_img = data_j.get('featured_image') if data_j.get('featured_image') else 'upload'
            print("feature image", feature_img)
            if feature_img == 'upload':
                img_path = root_folder / f'result/img_match/{l_version}_{fixture_match}_{types}.png'
                print(f"img_path: {img_path}")
                img_id = upload_image_to_wordpress(
                    img_path,
                    url + '/wp-json/wp/v2/media',
                    header, fixture_match, types
                )
                print(f"image id: {img_id}")
                post = {
                    'title': title,
                    'status': f'{type_status}',
                    'content': text_all,
                    'categories': category,
                    'tags': tags,
                    'featured_media': img_id
                }

            elif data_j['featured_image'] == 'url':
                post = {
                    'title': title,
                    'status': f'{type_status}',
                    'content': text_all,
                    'categories': category,
                    'tags': tags,
                    # 'meta': {'fifu_image_url': featured_image}
                }

            else:
                post = {
                    'title': title,
                    'status': f'{type_status}',
                    'content': text_all,
                    'categories': category,
                    'tags': tags,
                    # 'meta': {'fifu_image_url': featured_image}
                }
            if author:
                post['author'] = author[0]["id"]
            responce = requests.post(url + '/wp-json/wp/v2/posts', headers=header, json=post).json()

            if feature_img != 'upload':
                data = {
                    "meta": {
                        "fifu_image_url": featured_image
                    }
                }
                post_id = responce.get("id")
                # Force FIFU to refresh image
                if post_id:
                    requests.put(url + f'/wp-json/wp/v2/posts/{post_id}', headers=header, json=data)

            site_posted_data = {
                "website": data_j['platform_url'],
                "Post Id": responce['id'],
                "time": responce['date'],
                "website_name": data_j['platform_name'],
                "website_id": data_j['documentId'],
                "title": title,
            }
            print(f"[INFO]  {site_posted_data}")
            # insert_news_log(types, title, data_j["platform_name"], bool(img_id), 'Published', None, responce['date'])

            # Auto-post to social media via Node.js backend
            try:
                from auth.session_manager import session_manager
                sm_session = session_manager.get_authenticated_session()
                if sm_session:
                    post_url = responce.get('link', '')
                    social_payload = {
                        "websiteId": data_j.get('id'),
                        "title": title,
                        "url": post_url,
                        "imageUrl": featured_image if featured_image else None,
                        "platforms": ["twitter", "reddit"]
                    }
                    sm_api = f"{os.getenv('CMS_BASE_URL')}/api/social-media/post"
                    sm_resp = sm_session.post(sm_api, json=social_payload, timeout=30)
                    if sm_resp.status_code == 200:
                        print(f"[INFO] Social media auto-post triggered for: {title[:50]}")
                    else:
                        print(f"[WARN] Social media auto-post returned {sm_resp.status_code}")
            except Exception as sm_err:
                print(f"[WARN] Social media auto-post failed (non-blocking): {sm_err}")

            return site_posted_data

    except Exception as e:
        # insert_news_log(types, title, data_j["platform_name"], bool(img_id), 'Failed')
        print(f"[INFO] Not posted for site {data_j['platform_url']} error: {e}")

        # Track publication error
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.PUBLICATION,
                MessageStatus.ERROR,
                f"Publication failed for {data_j.get('platform_name', 'unknown site')}",
                error_details=str(e)
            )

        return None
                    # if 'twitter' in data_j['auto-posting']:
                    #     bot_send_twitter(title, responce_json['content']['raw'][:100], league_name, responce_json['link'], featured_image, team_name_home, team_name_away, [data_j['twitter']['api_key'], data_j['twitter']['api_secrets'], data_j['twitter']['access_token'], data_j['twitter']['access_secrets']])


def check_pub(league_name, team_names, ID, types):
    status = False
    
    with open(root_folder / f'parameters/football/users/parameters/{ID}.json') as file:
        data_j = json.load(file)
    var = league_name in data_j['subscribe']['football'] \
            and data_j['subscribe']['football'][league_name]["teams"] == "all" \
            or True in [index in data_j['subscribe']['football'][league_name]['teams'] for index in team_names]\
                and types + '_match' in data_j['subscribe']['football'][league_name]['types'] \
                or data_j['subscribe']['football'][league_name]['types'] == "all"
    
    return var

def main_publication(fixture_match, types, league_id, website):
    # list_id = get_user_id_main('football')
    website['categories'] = []
    for lg in website.get('website_leagues') or []:
        if lg.get('id') == int(league_id):
            website['categories'] = lg['categories']
            break

    print("league categories", website['categories'])
    with open(root_folder / f'result/json/{fixture_match}_{types}.json') as file:
        text = json.load(file)
        # print(root_folder / f'result/json/{fixture_match}_{types}.json')
    if types == "review":
            img_graph = f"<img src=\"{os.getenv('AWS_URL')}/match/{fixture_match}_graph_{types}.png\" alt=\"\">"
            img_lineups = f"<img src=\"{os.getenv('AWS_URL')}/match/{fixture_match}_lineups_{types}.png\" alt=\"\">"
            for game in text:
                team1 = game['title']['team_a']
                team2 = game['title']['team_b']
                goals_a = game['title']['goal_a']
                goals_b = game['title']['goal_b']
                league_name1 = game['title']['league_name']
                lineups_a = game['subtitle_lineups']['lineups_a']
                lineups_b = game['subtitle_lineups']['lineups_b']
                lineups_in_game_a = game['subtitle_lineups']['lineups_in_game_a']
                lineups_in_game_b = game['subtitle_lineups']['lineups_in_game_b']
                total_shots_off = game['goals_scorers']['goals']['total_shots_off']
                total_shots_on = game['goals_scorers']['goals']['total_shots_on']
                shots_team1_off = game['goals_scorers']['goals']['shots_team1_off']
                shots_team1_on = game['goals_scorers']['goals']['shots_team1_on']
                active_shots_player_home = game['goals_scorers']['goals']['active_shots_player_home']
                shots_team2_off = game['goals_scorers']['goals']['shots_team2_off']
                shots_team2_on = game['goals_scorers']['goals']['shots_team2_on']
                active_shots_player_away = game['goals_scorers']['goals']['active_shots_player_away']
                total_assists_home = game['goals_scorers']['goals']['total_assists_home']
                total_assists_away = game['goals_scorers']['goals']['total_assists_away']
                total_interceptions_home = game['goals_scorers']['defensive']['total_interceptions_home']
                name_top_inceptions_home = game['goals_scorers']['defensive']['name_top_inceptions_home']
                amount_interceptions_home = game['goals_scorers']['defensive']['amount_interceptions_home']
                total_inteceptions_away = game['goals_scorers']['defensive']['total_inteceptions_away']
                name_top_inceptions_away = game['goals_scorers']['defensive']['name_top_inceptions_away']
                amount_interseptions_away = game['goals_scorers']['defensive']['amount_interseptions_away']
                total_blocks_home = game['goals_scorers']['defensive']['total_blocks_home']
                name_top_blocks_home = game['goals_scorers']['defensive']['name_top_blocks_home']
                amount_blocks_home = game['goals_scorers']['defensive']['amount_blocks_home']
                total_blocks_away = game['goals_scorers']['defensive']['total_blocks_away']
                name_top_blocks_away = game['goals_scorers']['defensive']['name_top_blocks_away']
                amount_blocks_away = game['goals_scorers']['defensive']['amount_blocks_away']
                name_duels_team1 = game['goals_scorers']['duels']['name_duels_team1']
                amount_duels_team1 = game['goals_scorers']['duels']['amount_duels_team1']
                name_duels_team2 = game['goals_scorers']['duels']['name_duels_team2']
                amount_duels_team2 = game['goals_scorers']['duels']['amount_duels_team2']
                possession_team1 = game['goals_scorers']['ball_pos']['possession_team1']
                possession_team2 = game['goals_scorers']['ball_pos']['possession_team2']
                first_top_name = game['top_players_league']['top3']['first_top_name']
                first_top_team = game['top_players_league']['top3']['first_top_team']
                first_top_amount = game['top_players_league']['top3']['first_top_amount']
                second_top_name = game['top_players_league']['top3']['second_top_name']
                second_top_team = game['top_players_league']['top3']['second_top_team']
                second_top_amount = game['top_players_league']['top3']['second_top_amount']

                third_top_name = game['top_players_league']['top3']['third_top_name']
                third_top_team = game['top_players_league']['top3']['third_top_team']
                third_top_amount = game['top_players_league']['top3']['third_top_amount']
                next_match_team1_with = game['next_matches']['show_next_matches']['next_match_team1_with']
                next_match_team1_date = game['next_matches']['show_next_matches']['next_match_team1_date']
                next_match_team1_venue = game['next_matches']['show_next_matches']['next_match_team1_venue']
                next_match_team2_with = game['next_matches']['show_next_matches']['next_match_team2_with']
                next_match_team2_date = game['next_matches']['show_next_matches']['next_match_team2_date']
                next_match_team2_venue = game['next_matches']['show_next_matches']['next_match_team2_venue']
                arena = game['title']['venue']
                date = game['title']['date_match3']
                form_home = game['title']['form_home']
                form_away = game['title']['form_away']
                fourth_top_name = game['top_players_league']['top3']['fourth_top_name']
                fourth_top_team = game['top_players_league']['top3']['fourth_top_team']
                fourth_top_amount = game['top_players_league']['top3']['fourth_top_amount']
                fifth_top_name = game['top_players_league']['top3']['fifth_top_name']
                fifth_top_team = game['top_players_league']['top3']['fifth_top_team']
                fifth_top_amount = game['top_players_league']['top3']['fifth_top_amount']
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
                logo_table = ''

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

                # logo_table = str(logo_table).replace("+", " ")
                # print(logo_table[0].replace("+", " "))


            # проверка нужна ли публикация по данному матчу
            # if check_pub(league_name1, [team1, team2], global_for, 'review'):

            # with open(root_folder / f'parameters/football/users/parameters/{global_for}.json') as file:
            #     user = json.load(file)
            # print(root_folder / f'parameters/football/users/text/{global_for}_review_match.json')
            # with open(root_folder / f'parameters/football/users/text/{global_for}_review_match.json') as file:
            #     main_text = json.load(file)

            with open(root_folder / f'parameters/football/users/dicts/wc_teams.json') as file:
                teams_for_cup = json.load(file)

            # y_cards_title = main_text['y_cards']
            # r_cards_title = main_text['r_cards']
            # fouls_title = main_text['fouls_title']
            # penalties_title = main_text['penalties_title']
            # goalscorers = main_text['goalscorers']

            l_version = website.get('l_version') if website.get('l_version') else 'eng'

            if l_version == 'ru':
                y_cards_title = "<p><b>Желтые карточки: </b></p>"
                r_cards_title = "<p><b>Красные карточки: </b></p>"
                fouls_title = "<h4><b>Фолы:</b></h4>"
                penalties_title = "<h4><b>Пенальти в матче:</b></h4>"
                goalscorers = "<h4><b>Голы:</b></h4>"
            else:
                y_cards_title = "<p><b>Yellow cards: </b></p>"
                r_cards_title = "<p><b>Red cards: </b></p>"
                fouls_title = "<h4><b>Fouls:</b></h4>"
                penalties_title = "<h4><b>Penalties in a match:</b></h4>"
                goalscorers = "<h4><b>Goalscorers:</b></h4>"

            insert_query = (
                f"SELECT fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time FROM match_review WHERE fixture_match_for_check={fixture_match}"
            )
            # print(insert_query)
            index = get_data(insert_query)
            index = index[0]

            fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time = index

            time_home_goal = time_home_goal.split()
            time_away_goal = time_away_goal.split()
            time_home_penalti = time_home_penalti.split()
            time_away_penalti = time_away_penalti.split()
            player_home_goal = str(player_home_goal).replace("+", " ")
            player_away_goal = str(player_away_goal).replace("+", " ")
            player_away_goal = [player.replace("_", " ") for player in player_away_goal.split()]
            player_home_goal = [player.replace("_", " ") for player in player_home_goal.split()]
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
            # with open(
            #         root_folder / f'parameters/football/users/parameters/{global_for}.json',
            #         encoding='utf-8'
            # ) as file:
            #     data_j = json.load(file)

            client_language = website.get('l_version') if website.get('l_version') else 'eng'
            featured_image_url = f"{os.getenv('AWS_URL')}/match/{client_language}_{fixture_match}_{types}.png"
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
                goals_for_openai = ""
                if time_home_goal != [] and time_away_goal != []:
                    if int(time_home_goal[index]) < int(time_away_goal[index]):
                        first_goal = f'{player_home_goal[0]} drop first goal at {time_home_goal[0]} minute of the match.'
                        goals_for_openai += f"{player_home_goal[0]} from {team1} scored at {time_home_goal[0]} minute (1:0), "
                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        first_goal = f'{player_away_goal[0]} drop first goal at {time_away_goal[0]} minute of the match.'
                        goals_for_openai += f"{player_away_goal[0]} from {team2} scored at {time_away_goal[0]} minute (0:1), "
                elif time_home_goal != [] and time_away_goal == []:
                    first_goal = f'{player_home_goal[0]} drop first goal at {time_home_goal[0]} minute of the match.'
                    goals_for_openai += f"{player_home_goal[0]} from {team1} scored at {time_home_goal[0]} minute (1:0), "
                elif time_home_goal == [] and time_away_goal != []:
                    first_goal = f'{player_away_goal[0]} drop first goal at {time_away_goal[0]} minute of the match.'
                    goals_for_openai += f"{player_away_goal[0]} from {team2} scored at {time_away_goal[0]} minute (0:1), "
                else:
                    goal_all_time = ''
                    first_goal = ''

                while len(player_home_goal) + len(player_away_goal) != 0:

                    if time_home_goal == []:
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> at {time_away_goal[index]} minute ({index_home} : {index_away}) (<b>{team2}</b>)</li>'
                        goals_for_openai += f"{player_away_goal[index]} from {team2} scored at {time_away_goal[index]} minute ({index_home} : {index_away}), "

                        del time_away_goal[index], player_away_goal[index]

                    elif time_away_goal == []:
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) < int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> at {time_away_goal[index]} minute ({index_home} : {index_away}) ({team2})</li>'
                        goals_for_openai += f"{player_away_goal[index]} from {team2} scored at {time_away_goal[index]} minute ({index_home} : {index_away}), "
                        del time_away_goal[index], player_away_goal[index]

                    elif int(time_home_goal[index]) == int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> at {time_home_goal[index]} minute ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                yellow_card_home = ''
                for yel_cards_home in range(len(time_home_yellow)):
                    yellow_card_home += '<li>' + ' ' + '<b>' + player_home_yellow[yel_cards_home].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team1 + ') at ' + \
                                        time_home_yellow[yel_cards_home] + ' minute </li> '

                yellow_card_away = ''
                for yel_cards_away in range(len(time_away_yellow)):
                    yellow_card_away += '<li>' + ' ' + '<b>' + player_away_yellow[yel_cards_away].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team2 + ') at ' + \
                                        time_away_yellow[yel_cards_away] + ' minute </li> '

                red_card_home = ''
                for red_cards_home in range(len(time_home_red)):
                    red_card_home += '<li>' + ' ' + '<b>' + player_home_red[red_cards_home].replace("_",
                                                                                                    " ") + '</b>' + ' (' + team1 + ') at ' + \
                                        time_home_red[red_cards_home] + ' minute </li> '

                red_card_away = ''
                for red_cards_away in range(len(time_away_red)):
                    red_card_away += '<li>' + ' ' + '<b>' + player_away_red[red_cards_away].replace("_",
                                                                                                    " ") + '</b>' + ' (' + team2 + ') at ' + \
                                        time_away_red[red_cards_away] + ' minute </li> '

                penalti_home = ''
                if time_home_penalti != [] and player_home_penalti != []:
                    for penalti_home_cycle in range(len(time_home_penalti)):
                        penalti_home += '<li>' + ' ' + '<b>' + player_home_penalti[penalti_home_cycle].replace("_",
                                                                                                                " ") + '</b>' + ' (' + team1 + ') at ' + \
                                        time_home_penalti[penalti_home_cycle] + ' minute </li> '

                penalti_away = ''
                if time_away_penalti != [] and player_away_penalti != []:
                    for penalti_away_cycle in range(len(time_away_penalti)):
                        penalti_away += '<li>' + ' ' + '<b>' + player_away_penalti[penalti_away_cycle].replace("_",
                                                                                                                " ") + '</b>' + ' (' + team2 + ') at ' + \
                                        time_away_penalti[penalti_away_cycle] + ' minute </li> '

            list_teams = [fifth_top_team, fourth_top_team, third_top_team, second_top_team, first_top_team]
            list_teams_new = []
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
                    team1, team2 = teams_for_cup[l_version][team1], teams_for_cup[l_version][team2]
                    if next_match_team1_with != '': next_match_team1_with = teams_for_cup[l_version][
                        next_match_team1_with]
                    if next_match_team2_with != '': next_match_team2_with = teams_for_cup[l_version][
                        next_match_team2_with]

                goal_all_time = ''
                first_goal = ''
                index = 0
                index_home = 0
                index_away = 0
                goals_for_openai = ''

                if time_home_goal != [] and time_away_goal != []:
                    if int(time_home_goal[index]) < int(time_away_goal[index]):
                        first_goal = f'{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча.'
                        # goals_for_openai += f"{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча."
                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        first_goal = f'{player_away_goal[0]} забил первый гол на {time_away_goal[0]} минуте матча.'
                        # goals_for_openai += f"{player_home_goal[0]} from  {time_home_goal[0]} минуте матча."

                elif time_home_goal != [] and time_away_goal == []:
                    first_goal = f'{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча.'
                    # goals_for_openai += f"{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча."

                elif time_home_goal == [] and time_away_goal != []:
                    first_goal = f'{player_away_goal[0]} забил первый гол на {time_away_goal[0]} минуте матча.'
                    # goals_for_openai += f"{player_home_goal[0]} забил первый гол на {time_home_goal[0]} минуте матча."

                else:
                    goal_all_time = ''
                    first_goal = ''
                while len(player_home_goal) + len(player_away_goal) != 0:
                    if time_home_goal == []:
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> на {time_away_goal[index]} минуте ({index_home} : {index_away}) ({team2})</li>'
                        goals_for_openai += f"{player_away_goal[index]} from {team2} scored at {time_away_goal[index]} minute ({index_home} : {index_away}), "
                        del time_away_goal[index], player_away_goal[index]

                    elif time_away_goal == []:
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) < int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                    elif int(time_home_goal[index]) > int(time_away_goal[index]):
                        index_away += 1

                        goal_all_time += f'<li> <b>{player_away_goal[index]}</b> на {time_away_goal[index]} минуте ({index_home} : {index_away}) ({team2})</li>'
                        goals_for_openai = f"{player_away_goal[index]} from {team2} scored at {time_away_goal[index]} minute ({index_home} : {index_away}), "
                        del time_away_goal[index], player_away_goal[index]

                    elif int(time_home_goal[index]) == int(time_away_goal[index]):
                        index_home += 1

                        goal_all_time += f'<li> <b>{player_home_goal[index]}</b> на {time_home_goal[index]} минуте ({index_home} : {index_away}) ({team1})</li>'
                        goals_for_openai += f"{player_home_goal[index]} from {team1} scored at {time_home_goal[index]} minute ({index_home} : {index_away}), "
                        del time_home_goal[index], player_home_goal[index]

                yellow_card_home = ''
                for yel_cards_home in range(len(time_home_yellow)):
                    yellow_card_home += '<li>' + ' ' + '<b>' + player_home_yellow[yel_cards_home].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team1 + ') на ' + \
                                        time_home_yellow[yel_cards_home] + ' минуте </li> '

                yellow_card_away = ''
                for yel_cards_away in range(len(time_away_yellow)):
                    yellow_card_away += '<li>' + ' ' + '<b>' + player_away_yellow[yel_cards_away].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team2 + ') на ' + \
                                        time_away_yellow[yel_cards_away] + ' минуте </li> '

                red_card_home = ''
                for red_cards_home in range(len(time_home_red)):
                    red_card_home += '<li>' + ' ' + '<b>' + player_home_red[red_cards_home].replace("_",
                                                                                                    " ") + '</b>' + ' (' + team1 + ') на ' + \
                                        time_home_red[red_cards_home] + ' минуте </li> '

                red_card_away = ''
                for red_cards_away in range(len(time_away_red)):
                    red_card_away += '<li>' + ' ' + '<b>' + player_away_red[red_cards_away].replace("_",
                                                                                                    " ") + '</b>' + ' (' + team2 + ') на ' + \
                                        time_away_red[red_cards_away] + ' минуте </li> '

                penalti_home = ''
                for penalti_home_cycle in range(len(time_home_penalti)):
                    penalti_home += '<li>' + ' ' + '<b>' + player_home_penalti[penalti_home_cycle].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team1 + ') на ' + \
                                    time_home_penalti[penalti_home_cycle] + ' минуте </li> '

                penalti_away = ''
                for penalti_away_cycle in range(len(time_away_penalti)):
                    penalti_away += '<li>' + ' ' + '<b>' + player_away_penalti[penalti_away_cycle].replace("_",
                                                                                                            " ") + '</b>' + ' (' + team2 + ') на ' + \
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

            review_match_date = date
            list_date = [next_match_team1_date, next_match_team2_date]
            date = change_date(list_date, l_version)
            next_match_team1_date, next_match_team2_date = date[0], date[1]

            if website.get("custom","") == "":
                title, text_all = main_change_text(l_version, 'match', 'review', False)
            elif website.get("custom","") != "":
                title, text_all = main_change_text(l_version, 'match', 'review', True)

            openai.api_key = os.getenv('OPENAI_API_KEY')
            """ review """
            # print(date)
            prompt_vars = {
                "team1": team1,
                "team2": team2,
                "goals_a": goals_a,
                "goals_b": goals_b,
                "review_match_date": review_match_date,
                "league_name1": league_name1,
                "round": round,
                # Aliases for dashboard consistency
                "home_team": team1,
                "away_team": team2,
                "goals_home": goals_a,
                "goals_away": goals_b,
                "match_date": review_match_date,
                "league_name": league_name1,
                # ... existing variables
                "goals_for_openai": goals_for_openai[:-2] if goals_for_openai else "",
                "possession_team1": possession_team1,
                "possession_team2": possession_team2,
                "shots_team1_off": shots_team1_off,
                "shots_team1_on": shots_team1_on,
                "active_shots_player_home": active_shots_player_home,
                "shots_team2_off": shots_team2_off,
                "shots_team2_on": shots_team2_on,
                "active_shots_player_away": active_shots_player_away,
                "name_home_top_pass_accuracy": name_home_top_pass_accuracy,
                "top__home_precent_accuracy": top__home_precent_accuracy,
                "top__home_total_passes": top__home_total_passes,
                "name_away_top_pass_accuracy": name_away_top_pass_accuracy,
                "top__away_precent_accuracy": top__away_precent_accuracy,
                "top__away_total_passes": top__away_total_passes,
                "name_home_top_pass_key": name_home_top_pass_key,
                "top__home_amount_key": top__home_amount_key,
                "name_away_top_pass_key": name_away_top_pass_key,
                "top__away_amount_key": top__away_amount_key,
                "total_interceptions_home": total_interceptions_home,
                "name_top_inceptions_home": name_top_inceptions_home,
                "amount_interceptions_home": amount_interceptions_home,
                "total_inteceptions_away": total_inteceptions_away,
                "name_top_inceptions_away": name_top_inceptions_away,
                "amount_interseptions_away": amount_interseptions_away,
                "total_blocks_home": total_blocks_home,
                "name_top_blocks_home": name_top_blocks_home,
                "amount_blocks_home": amount_blocks_home,
                "total_blocks_away": total_blocks_away,
                "name_top_blocks_away": name_top_blocks_away,
                "amount_blocks_away": amount_blocks_away,
                "name_duels_team1": name_duels_team1,
                "amount_duels_team1": amount_duels_team1,
                "name_duels_team2": name_duels_team2,
                "amount_duels_team2": amount_duels_team2
            }

            custom_title = website.get('data', {}).get('review_news_title_prompt')
            custom_news = website.get('data', {}).get('review_news_content_prompt')

            if custom_news and custom_title:
                news_prompt = replace_vars(custom_news, prompt_vars)
                title_prompt = replace_vars(custom_title, prompt_vars)
                # For custom prompts, we treat them as a 2-step process (title then content) 
                # or pass them appropriately to the generation function.
                # However, the original loop iterates through a list of prompts to build paragraphs.
                # If using custom prompts, we likely want a single cohesive article or specific structure.
                # If custom prompts are enabled, we might override the list_text approach.
                
                # Assuming custom prompts replace the entire default list flow for title and content.
                # But the code below expects a list of responses to build paragraphs.
                # Let's adapt: If custom, we generate content in one go or split if needed.
                # For now, let's assume custom prompts return full article body in one prompt or we put them in list.
                
                # If custom prompts are simple strings, we can put them in a list.
                # BUT the original code handles multiple paragraphs. 
                # Let's try to map custom prompt to a single content generation if possible, 
                # or just use the custom prompts as the list.
                
                # Actually, the user wants "use it for the generate news".
                # If custom prompts are provided, we should probably use them.
                # Let's use the custom title prompt for title and custom news prompt for body.
                
                # If we have only 2 prompts (title + body), the loop below expects 
                # index 1 = title, others = paragraphs.
                
                list_text = [title_prompt, news_prompt] # Title first, then body
                
            else:
                list_text = [
                    f"Write a headline for a football match report. The headline must be structured for SEO and AI search discovery: '{team1} vs {team2} {goals_a}:{goals_b}, {review_match_date}, {league_name1}'.",

                    f"Using the information and data from the just-ended match, write a comprehensive football match report suitable for publication on a football news website {team1} vs {team2} {goals_a}:{goals_b} in Match Round {round} of {league_name1}. {goals_for_openai[:-2] if goals_for_openai else ''}. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking. Write the content in a natural, human-like style, ensuring it passes AI content detection tools.",

                    f"Write a match report that includes ball possession and shooting statistics: Ball possession: {team1} — {possession_team1}, {team2} — {possession_team2}. {team1} made {shots_team1_off} shots on target, {shots_team1_on} on goal. The most active in terms of the number of shots was — {active_shots_player_home}. {team2} made {shots_team2_off} shots on target, {shots_team2_on} on goal. Best in hits on goal – {active_shots_player_away}. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",

                    f"Write a match report using the provided data about passing accuracy: {name_home_top_pass_accuracy} ({team1}) — pass accuracy {top__home_precent_accuracy}%, total passes {top__home_total_passes}. {name_away_top_pass_accuracy} ({team2}) — pass accuracy {top__away_precent_accuracy}%, total passes {top__away_total_passes}. {name_home_top_pass_key} ({team1}) — {top__home_amount_key} key passes. {name_away_top_pass_key} ({team2}) — {top__away_amount_key}. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",

                    f"Write a match report with a focus on defensive actions, including interceptions and blocks. Number of interceptions for {team1} — {total_interceptions_home} (leader — {name_top_inceptions_home}, {amount_interceptions_home}). {team2} — {total_inteceptions_away} ({name_top_inceptions_away} has the most, {amount_interseptions_away}). {team1} — {total_blocks_home} ({name_top_blocks_home}, {amount_blocks_home}). {team2} — {total_blocks_away} ({name_top_blocks_away} — {amount_blocks_away}). The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",

                    f"Write a match report using the data about face-to-face duels for the ball: By the number of face-to-face fights for the ball, the leaders in the teams are: {name_duels_team1} ({amount_duels_team1}) {team1} and {name_duels_team2} ({amount_duels_team2}) {team2}. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking."
                ]
                
            index_openai = 0
            main_text_list = []
            
            # Use generate_openai_content for reviews
            for text in list_text:
                index_openai += 1
                result = generate_openai_content(text, "review")
                
                if not result:
                    print("Error generating content for review")
                    continue

                if index_openai != 1:
                     main_text_list.append("<p>" + result + "</p>\n")
                else:
                    title_openAI = result

            # Ensure we have enough paragraphs to unpack
            # If dynamic prompts used, we might have fewer paragraphs than the original code expects (5).
            # The original code unpacks into 5 variables: first...fiveth_paragraph
            # We must handle this gracefully.
            
            # Pad the list if needed to avoid unpacking errors, although dynamic prompts logic 
            # might not use these specific variable names if we were fully refactoring.
            # But the existing code below line 906 EXPECTS these 5 variables.
            # Let's fill missing spots with empty strings to prevent crashes.
            while len(main_text_list) < 5:
                main_text_list.append("")
                
            first_paragraph, second_paragraph, threeth_paragraph, fourth_paragraph, fiveth_paragraph = main_text_list[:5]
            
            for i in ['"', "'"]:
                title_openAI = title_openAI.replace(i, "") if i in title_openAI else title_openAI

            l2 = [first_paragraph, second_paragraph, threeth_paragraph, fourth_paragraph, fiveth_paragraph, var_for_title_1, var_for_title_2, var_for_title_3, summ_shorts_target, team1, team2, goals_a, goals_b,
                    league_name1, lineups_a, lineups_b, lineups_in_game_a, lineups_in_game_b, first_goal, all_scorers,
                    total_shots_off, total_shots_on, shots_team1_off, shots_team1_on, active_shots_player_home,
                    shots_team2_off, shots_team2_on, active_shots_player_away, total_assists_home, total_assists_away,
                    total_interceptions_home, name_top_inceptions_home, amount_interceptions_home,
                    total_inteceptions_away, name_top_inceptions_away, amount_interseptions_away, total_blocks_home,
                    name_top_blocks_home, amount_blocks_home, total_blocks_away, name_top_blocks_away, amount_blocks_away,
                    name_duels_team1, amount_duels_team1, name_duels_team2, amount_duels_team2, possession_team1,
                    possession_team1, possession_team2, first_top_name, first_top_team, first_top_amount, second_top_name,
                    second_top_name, second_top_team, second_top_amount, third_top_name, fourth_top_team,
                    fourth_top_amount, fifth_top_name, fifth_top_team, fifth_top_amount, rank, all_games, third_top_team,
                    third_top_amount, next_match_team1_with, next_match_team1_date, next_match_team1_venue,
                    next_match_team2_with, next_match_team2_date, next_match_team2_venue, arena, date, form_home,
                    form_away, penalti_home, fourth_top_name, form_all, logo_table, name_home_top_pass_accuracy,
                    top__home_precent_accuracy, top__home_total_passes, win_games, draw_games, lose_games, goals_for,
                    goals_missed, goals_diff, points, name_teams, form_all, logo_table, name_home_top_pass_accuracy,
                    top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy,
                    top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key,
                    name_away_top_pass_key, top__away_amount_key, next_match_team1_date, next_match_team2_date, img_graph,
                     yellow_card, red_card, title3, fouls_y_card, fouls_r_card, fouls, title2, penalti_home,
                    penalti, title1, goals,img_lineups, round]
            l = ['{first_paragraph}', '{second_paragraph}', '{threeth_paragraph}', '{fourth_paragraph}', '{fiveth_paragraph}',
                    '{var_for_title_1}', '{var_for_title_2}', '{var_for_title_3}', '{summ_shorts_target}', '{team1}',
                    '{team2}', '{goals_a}', '{goals_b}', '{league_name1}', '{lineups_a}', '{lineups_b}',
                    '{lineups_in_game_a}', '{lineups_in_game_b}', '{first_goal}', '{all_scorers}', '{total_shots_off}',
                    '{total_shots_on}', '{shots_team1_off}', '{shots_team1_on}', '{active_shots_player_home}',
                    '{shots_team2_off}', '{shots_team2_on}', '{active_shots_player_away}', '{total_assists_home}',
                    '{total_assists_away}', '{total_interceptions_home}', '{name_top_inceptions_home}',
                    '{amount_interceptions_home}', '{total_inteceptions_away}', '{name_top_inceptions_away}',
                    '{amount_interseptions_away}', '{total_blocks_home}', '{name_top_blocks_home}', '{amount_blocks_home}',
                    '{total_blocks_away}', '{name_top_blocks_away}', '{amount_blocks_away}', '{name_duels_team1}',
                    '{amount_duels_team1}', '{name_duels_team2}', '{amount_duels_team2}', '{possession_team1}',
                    '{possession_team1}', '{possession_team2}', '{first_top_name}', '{first_top_team}',
                    '{first_top_amount}', '{second_top_name}', '{second_top_name}', '{second_top_team}',
                    '{second_top_amount}', '{third_top_name}', '{fourth_top_team}', '{fourth_top_amount}',
                    '{fifth_top_name}', '{fifth_top_team}', '{fifth_top_amount}', '{rank}', '{all_games}',
                    '{third_top_team}', '{third_top_amount}', '{next_match_team1_with}', '{next_match_team1_date}',
                    '{next_match_team1_venue}', '{next_match_team2_with}', '{next_match_team2_date}',
                    '{next_match_team2_venue}', '{arena}', '{date}', '{form_home}', '{form_away}', '{penalti_home}',
                    '{fourth_top_name}', '{form_all}', '{logo_table}', '{name_home_top_pass_accuracy}',
                    '{top__home_precent_accuracy}', '{top__home_total_passes}', '{win_games}', '{draw_games}',
                    '{lose_games}', '{goals_for}', '{goals_missed}', '{goals_diff}', '{points}', '{name_teams}',
                    '{form_all}', '{logo_table}', '{name_home_top_pass_accuracy}', '{top__home_precent_accuracy}',
                    '{top__home_total_passes}', '{name_away_top_pass_accuracy}', '{top__away_precent_accuracy}',
                    '{top__away_total_passes}', '{name_home_top_pass_key}', '{top__home_amount_key}',
                    '{name_away_top_pass_key}', '{top__away_amount_key}', '{next_match_team1_date}',
                    '{next_match_team2_date}', '{img_graph}', '{yellow_card}', '{red_card}', '{title3}',
                    '{fouls_y_card}', '{fouls_r_card}', '{fouls}', '{title2}', '{penalti_home}', '{penalti}', '{title1}',
                    '{goals}', '{img_lineups}', '{round_for_text}']

            for i in range(len(l)):
                if l[i] in text_all:
                    text_all = text_all.replace(l[i], str(l2[i]))
                if l[i] in title:
                    title = title.replace(l[i], str(l2[i]))
            if "<b>" in title and "</b>" in title:
                title = title.replace("<b>", "").replace("</b>", "")


            """ Публикация статьи """
            # exit()
            result_publish = publish(website, league_name1, team1, team2,
                                        featured_image_url, title_openAI,
                                        text_all, types, fixture_match, l_version, league_id)
            # result_publish - responcce_json

            """ Запуск публикации в телеграм если она есть """
            # if 'telegram' in data_j['auto-posting'] and result_publish != False:

            #     """ Получение текста """
            #     with open(root_folder / f'parameters/football/users/text/{l_version}_{types}_match_tg.json') as file:
            #         tg_json = json.load(file)
            #     with open(root_folder / f'parameters/football/users/dicts/flag_for_tg.json',
            #                 encoding='utf-8') as flag_json:
            #         flag_json = json.load(flag_json)

            #     text_for_tg = tg_json['main_text']

            #     """ Получение смайлика флаг по обоим командам """
            #     if league_name in flag_json:
            #         if team1 in flag_json[league_name]: flag_team1 = flag_json[league_name][team1]
            #         if team2 in flag_json[league_name]: flag_team2 = flag_json[league_name][team2]
            #     else:
            #         flag_team1, flag_team2 = '', ''
            #     league_name_tg = ''
            #     if ' ' in league_name:
            #         league_name_tg = league_name.replace(" ", "")
            #     else:
            #         league_name_tg = league_name
            #     """ Добавление переменных """
            #     l_new = ['{league_name_tg}', '{team1_tg}', '{team2_tg}', '{url_publ}', '{flag_team1}', '{flag_team2}',
            #                 '{title}']
            #     l2_new = [f"{league_name_tg}2022", team1.replace(' ', ''), team2.replace(' ', ''),
            #                 result_publish['link'], flag_team1, flag_team2, title]
            #     l_tags = ['<b>', '<p>', '<li>', '</b>', '</p>', '</li>', '<ul>', '</ul>']

            #     for i in range(len(l_new)):
            #         l2.append(l2_new[i])
            #         l.append(l_new[i])

            #     """ Замена переменных на данных в тексте """
            #     for i in range(len(l)):
            #         if l[i] in text_for_tg:
            #             text_for_tg = text_for_tg.replace(l[i], str(l2[i]))

            #     """ Замена тега </li> на 'пропуск строки' """
            #     for i_t in range(len(l_tags)):
            #         if l_tags[i_t] in text_for_tg:
            #             if l_tags[i_t] == '</li>':
            #                 tag = '\n'
            #             else:
            #                 tag = ''
            #             text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

            #     """ Отправка в телегам """
            #     bot_send_message_tg(featured_image_url,
            #                         data_j['auto-posting']['telegram']['token'],
            #                         data_j['auto-posting']['telegram']['channel'],
            #                         text_for_tg
            #                         )

    elif types == 'preview':

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
                for_goals_home = ensure_full_keys(game['goals']['home']['g'].split())
                missed_goals_home = ensure_full_keys(game['goals']['home']['m'].split())
                for_goals_away = ensure_full_keys(game['goals']['away']['g'].split())
                missed_goals_away = ensure_full_keys(game['goals']['away']['m'].split())
                # Define a function to ensure all lists have the keys from 0 to 6

                # print(for_goals_home)
                # print(missed_goals_home)
                # print(for_goals_away)
                # print(missed_goals_away)
                # exit()

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
        
            # if check_pub(league_name1, [team1, team2], global_for, 'preview'):

                # with open(
                #     f'/opt/footballBot/parameters/football/users/parameters/{global_for}.json', encoding='utf-8'
                # ) as file:
                #     data_j = json.load(file)

            # with open(root_folder / f'parameters/football/users/parameters/{global_for}.json') as file:
            #     user = json.load(file)
            with open(root_folder / f'parameters/football/users/dicts/wc_teams.json') as file:
                teams_for_cup = json.load(file)

            l_version = website.get('l_version') if website.get('l_version') else 'eng'

            new_date = change_date([full_date], l_version)
            new_date = new_date[0]

            # with open(
            #         root_folder / f'parameters/football/users/text/{global_for}_preview_match.json') as file:
            #     main_text = json.load(file)

            if l_version == 'ru':
                # home_win_or_lose = home_win_or_lose_ru
                # title_big_home_in_home1 = "in the home game"  # f"in the home game, — {title_big_home_in_home1}"             #main_text['title_big_home_in_home']
                # title_big_home_in_away1 = main_text['title_big_home_in_away']
                # title_big_away_in_home1 = main_text['title_big_away_in_home']
                # title_big_home_in_away_AWAY = main_text['title_big_home_in_away_AWAY']

                if league_name1 == 'World Cup':
                    if team1 in teams_for_cup[l_version]:
                        team1 = teams_for_cup[l_version][team1]
                    if team2 in teams_for_cup[l_version]:
                        team2 = teams_for_cup[l_version][team2]

            elif l_version == 'eng':
                home_win_or_lose = home_win_or_lose

            title_big_home_in_home1 = "в домашней игре" if l_version == 'ru' else "in the home game"  # f"in the home game, — {title_big_home_in_home1}"             #main_text['title_big_home_in_home']
            title_big_home_in_away1 = "на гостевой арене" if l_version == 'ru' else "on the guest arena"
            title_big_away_in_home1 = "выиграл дома с самым большим счетом" if l_version == 'ru' else "with a biggest score"
            title_big_home_in_away_AWAY = "а на выезде" if l_version == 'ru' else "and away with a score"

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

            if website.get('custom',"") == "": title, text_all = main_change_text(l_version, 'match', 'preview', False)
            if website.get('custom',"") != "": title, text_all = main_change_text(l_version, 'match', 'preview', True)

            featured_image_url = f"{os.getenv('AWS_URL')}/match/eng_{fixture_match}_{types}.png"
            openai.api_key = os.getenv('OPENAI_API_KEY')
            """ Preview """
            # print(new_date)
            prompt_vars = {
                "team1": team1,
                "team2": team2,
                "new_date": new_date,
                "rank1": rank1,
                "rank2": rank2,
                "league_name1": league_name1,
                # Aliases for dashboard consistency
                "home_team": team1,
                "away_team": team2,
                "match_date": new_date,
                "league_name": league_name1,
                "venue": venue1,
                # ... existing variables
                "top_player_a": top_player_a,
                "top_home_total": top_home_total,
                "top_player_b": top_player_b,
                "top_away_total": top_away_total,
                "home_forms": home_forms,
                "away_forms": away_forms,
                "home_biggest_win_in_home": home_biggest_win_in_home,
                "home_biggest_win_in_away": home_biggest_win_in_away,
                "home_biggest_lose_in_home": home_biggest_lose_in_home,
                "home_biggest_lose_in_away": home_biggest_lose_in_away,
                "home_win_once_in_home": home_win_once_in_home,
                "home_draws_once_in_home": home_draws_once_in_home,
                "home_lose_once_in_home": home_lose_once_in_home,
                "away_win_once_in_away": away_win_once_in_away,
                "away_draws_once_in_away": away_draws_once_in_away,
                "away_lose_once_in_away": away_lose_once_in_away,
                "clean_home": clean_home,
                "clean_away": clean_away,
                "away_biggest_win_in_home": away_biggest_win_in_home,
                "away_biggest_win_in_away": away_biggest_win_in_away,
                "away_biggest_lose_in_home": away_biggest_lose_in_home,
                "away_biggest_lose_in_away": away_biggest_lose_in_away
            }

            custom_title = website.get('data', {}).get('preview_news_title_prompt') or ""
            custom_news = website.get('data', {}).get('preview_news_content_prompt') or ""

            if custom_news and custom_title:
                news_prompt = replace_vars(custom_news, prompt_vars)
                title_prompt = replace_vars(custom_title, prompt_vars)
                list_text = [title_prompt, news_prompt]
            else:
                article_template = f"The article must be written in the BBC style of writing articles which is the pyramid style of writing. Do not use fluff at the start of the paragraph or article or sentence. Go straight to the point like the BBC does in its articles. \nExample: {team1} vs {team2}, {new_date}. please do not generate any dummy text in []"

                if rank1 and rank2:
                    article_template += f"{team1} — on the {rank1}nd place in {league_name1}, {team2} — {rank2}th in {league_name1}. please do not generate any dummy text in []"

                article_template += f"{top_player_a} scored {top_home_total} goals this season for {team1}, {top_player_b} scored {top_away_total} for {team2}. article Must be long, SEO-friendly, with natural language to pass AI content detection. Last five {team1} games: {home_forms}. {team2} last five games: {away_forms}. please do not generate any dummy text in []"

                list_text = [
                    f"Write a Headline using this example: \n{team1} vs {team2}, {new_date}The format of the headline must be structured for SEO and AI search discovery and must be this: [Team A] vs [Team B]: Preview -  Team News, Line-ups, Prediction and Tips | [Date] [Kickoff time in GMT]",

                    # f"Write a Preview Description of the Example.\nExample: {team1} vs {team2}, {new_date}.",
                    article_template,

                    f"Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. \nExample:{team1} won at home with a biggest score — {home_biggest_win_in_home}, and away with a score —{home_biggest_win_in_away}. Biggest loss of the season at home —{home_biggest_lose_in_home}, away game —{home_biggest_lose_in_away}. This season {team1} at home: wins –{home_win_once_in_home}, draws —{home_draws_once_in_home}, losses —{home_lose_once_in_home}. {team2} away: wins —{away_win_once_in_away}, draws —{away_draws_once_in_away}, losses —{away_lose_once_in_away}. Must be  words long, SEO-friendly, with natural language to pass AI content detection.",

                    f"Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. \nExample: This season {team1} has played without scoring a goal {clean_home} times. {team2} did not conceded in {clean_away} match of the season. {team2} has the biggest winning score gap in the home game — {away_biggest_win_in_home}, and away with a score of —{away_biggest_win_in_away}. The biggest loss at home —{away_biggest_lose_in_home}, away game —{away_biggest_lose_in_away}. Must be  words long, SEO-friendly, with natural language to pass AI content detection.",
                    
                    f"Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. \nExample: Last five {team1} games: {home_forms}. {team2} last five games: {away_forms}. Must be  words long, SEO-friendly, with natural language to pass AI content detection. please do not generate any dummy text in []"
                ]
            main_text = ""
            index_openai = 0
            list_results_openai = []
            
            # Use generate_openai_content for previews
            for text in list_text:
                index_openai += 1
                result = generate_openai_content(text, "preview")
                
                if not result:
                     print("Error generating content for preview")
                     continue

                if index_openai != 1:
                    list_results_openai.append("<p>" + result + "</p>\n")
                else:
                    title_openAI = result

            for i in ['"', "'"]:
                title_openAI = title_openAI.replace(i, "") if i in title_openAI else title_openAI

            # Ensure we have enough paragraphs to unpack
            # Similar to reviews, the original code expects 4 paragraphs
            while len(list_results_openai) < 4:
                list_results_openai.append("")

            first_paragraph, second_paragraph, thr3_paragraph, fourth_paragraph = list_results_openai[0], list_results_openai[1], list_results_openai[2], list_results_openai[3]

            l2 = [first_paragraph, second_paragraph, thr3_paragraph, fourth_paragraph ,new_date, team1, team2, date1, full_date, full_date[11:], venue1, league_name1, rank1, rank2,
                top_player_a, top_home_total, top_player_b, top_away_total, first_in_league_name,
                first_in_league_team, first_in_league_amount, second_in_league_name, second_in_league_team,
                second_in_league_amount, thrid_in_league_name, thrid_in_league_team, thrid_in_league_amount,
                fourth_in_league_name, fourth_in_league_team, fourth_in_league_amount, fifth_in_league_name,
                fifth_in_league_team, fifth_in_league_amount, top_home_assist_name, top_home_assist_amount,
                top_away_assist_name, top_away_assist_amount, top_home_saves_name, top_home_saves_amount,
                top_away_saves_name, top_away_saves_amount, top_home_blocks_name, top_home_blocks_amount,
                top_away_blocks_name, top_away_blocks_amount, top_home_duels_name, top_home_duels_amount,
                top_away_duels_name, top_away_duels_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card,
                name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card,
                amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, home_forms,
                away_forms, clean_home, clean_away, home_biggest_win_in_home, home_biggest_win_in_away,
                home_biggest_lose_in_home, home_biggest_lose_in_away, away_biggest_win_in_home,
                away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home,
                home_draws_once_in_home, home_lose_once_in_home, away_win_once_in_away, away_draws_once_in_away,
                away_lose_once_in_away, for_goals_home, for_goals_home[0], for_goals_home[1], for_goals_home[2],
                for_goals_home[3], for_goals_home[4], for_goals_home[5], for_goals_home[6], missed_goals_home[0],
                missed_goals_home[1], missed_goals_home[2], missed_goals_home[3], missed_goals_home[4],
                missed_goals_home[5], missed_goals_home[6], for_goals_away[0],
                for_goals_away[1], for_goals_away[2], for_goals_away[3], for_goals_away[4], for_goals_away[5],
                for_goals_away[6], missed_goals_away[0], missed_goals_away[1], missed_goals_away[2],
                missed_goals_away[3], missed_goals_away[4], missed_goals_away[5], missed_goals_away[6],
                table_h2h_total_game, home_table_h2h_win_in_home, home_table_h2h_win_in_away,
                home_table_h2h_draws_in_home, home_table_h2h_draws_in_away, home_table_h2h_lose_in_home,
                home_table_h2h_lose_in_away, away_table_h2h_win_in_home, away_table_h2h_win_in_away,
                away_table_h2h_draws_in_home, away_table_h2h_draws_in_away, away_table_h2h_lose_in_home,
                away_table_h2h_lose_in_away, home_comparison_win, home_comparison_att, home_comparison_def,
                home_comparison_t2t, home_comparison_goals, away_comparison_win, away_comparison_att,
                away_comparison_def, away_comparison_t2t, away_comparison_goals, predictions_win_home,
                predictions_draws, predictions_lose_home, home_win_or_lose, home_predictions_goals,
                away_predictions_goals, bk1_name, bk1_win_home, bk1_draw, bk1_win_away, bk2_name, bk2_win_home,
                bk2_draw, bk2_win_away, bk3_name, bk3_win_home, bk3_draw, bk3_win_away, list_minute[0],
                list_minute[1], list_minute[2], list_minute[3], list_minute[4], list_minute[5], list_minute[6],
                title_big_home_in_home, title_big_home_in_away,
                title_big_away_in_home]  # ,title_big_home_in_home, title_big_home_in_away, title_big_away_in_home
            l = ['{first_paragraph}', '{second_paragraph}', '{thr3_paragraph}', '{fourth_paragraph}', '{new_date}', '{team1}', '{team2}', '{date1}', '{full_date}', '{full_date[11:]}', '{venue1}',
                '{league_name1}', '{rank1}', '{rank2}', '{top_player_a}', '{top_home_total}', '{top_player_b}',
                '{top_away_total}', '{first_in_league_name}', '{first_in_league_team}', '{first_in_league_amount}',
                '{second_in_league_name}', '{second_in_league_team}', '{second_in_league_amount}',
                '{thrid_in_league_name}', '{thrid_in_league_team}', '{thrid_in_league_amount}',
                '{fourth_in_league_name}', '{fourth_in_league_team}', '{fourth_in_league_amount}',
                '{fifth_in_league_name}', '{fifth_in_league_team}', '{fifth_in_league_amount}',
                '{top_home_assist_name}', '{top_home_assist_amount}', '{top_away_assist_name}',
                '{top_away_assist_amount}', '{top_home_saves_name}', '{top_home_saves_amount}',
                '{top_away_saves_name}', '{top_away_saves_amount}', '{top_home_blocks_name}',
                '{top_home_blocks_amount}', '{top_away_blocks_name}', '{top_away_blocks_amount}',
                '{top_home_duels_name}', '{top_home_duels_amount}', '{top_away_duels_name}', '{top_away_duels_amount}',
                '{name_home_top_fouls_yel_card}', '{amount_home_fouls_yel_card}', '{name_away_top_fouls_yel_card}',
                '{amount_away_fouls_yel_card}', '{name_home_top_fouls_red_card}', '{amount_home_fouls_red_card}',
                '{name_away_top_fouls_red_card}', '{amount_away_fouls_red_card}', '{home_forms}', '{away_forms}',
                '{clean_home}', '{clean_away}', '{home_biggest_win_in_home}', '{home_biggest_win_in_away}',
                '{home_biggest_lose_in_home}', '{home_biggest_lose_in_away}', '{away_biggest_win_in_home}',
                '{away_biggest_win_in_away}', '{away_biggest_lose_in_home}', '{away_biggest_lose_in_away}',
                '{home_win_once_in_home}', '{home_draws_once_in_home}', '{home_lose_once_in_home}',
                '{away_win_once_in_away}', '{away_draws_once_in_away}', '{away_lose_once_in_away}', '{for_goals_home}',
                '{for_goals_home[0]}', '{for_goals_home[1]}', '{for_goals_home[2]}', '{for_goals_home[3]}',
                '{for_goals_home[4]}', '{for_goals_home[5]}', '{for_goals_home[6]}', '{missed_goals_home[0]}',
                '{missed_goals_home[1]}', '{missed_goals_home[2]}', '{missed_goals_home[3]}', '{missed_goals_home[4]}',
                '{missed_goals_home[5]}', '{missed_goals_home[6]}', '{for_goals_away[0]}',
                '{for_goals_away[1]}', '{for_goals_away[2]}', '{for_goals_away[3]}', '{for_goals_away[4]}',
                '{for_goals_away[5]}', '{for_goals_away[6]}', '{missed_goals_away[0]}', '{missed_goals_away[1]}',
                '{missed_goals_away[2]}', '{missed_goals_away[3]}', '{missed_goals_away[4]}', '{missed_goals_away[5]}', '{missed_goals_away[6]}',
                '{table_h2h_total_game}', '{home_table_h2h_win_in_home}',
                '{home_table_h2h_win_in_away}', '{home_table_h2h_draws_in_home}', '{home_table_h2h_draws_in_away}',
                '{home_table_h2h_lose_in_home}', '{home_table_h2h_lose_in_away}', '{away_table_h2h_win_in_home}',
                '{away_table_h2h_win_in_away}', '{away_table_h2h_draws_in_home}', '{away_table_h2h_draws_in_away}',
                '{away_table_h2h_lose_in_home}', '{away_table_h2h_lose_in_away}', '{home_comparison_win}',
                '{home_comparison_att}', '{home_comparison_def}', '{home_comparison_t2t}', '{home_comparison_goals}',
                '{away_comparison_win}', '{away_comparison_att}', '{away_comparison_def}', '{away_comparison_t2t}',
                '{away_comparison_goals}', '{predictions_win_home}', '{predictions_draws}', '{predictions_lose_home}',
                '{home_win_or_lose}', '{home_predictions_goals}', '{away_predictions_goals}', '{bk1_name}',
                '{bk1_win_home}', '{bk1_draw}', '{bk1_win_away}', '{bk2_name}', '{bk2_win_home}', '{bk2_draw}',
                '{bk2_win_away}', '{bk3_name}', '{bk3_win_home}', '{bk3_draw}', '{bk3_win_away}', '{list_minute[0]}',
                '{list_minute[1]}', '{list_minute[2]}', '{list_minute[3]}', '{list_minute[4]}', '{list_minute[5]}',
                '{list_minute[6]}', '{title_big_home_in_home}', '{title_big_home_in_away}',
                '{title_big_away_in_home}']  # , '{title_big_home_in_home}', '{title_big_home_in_away}', '{title_big_away_in_home}'


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
            # print(text_all)
            result_publish = publish(website, league_name1, team1, team2, featured_image_url, title_openAI,
                                    text_all, types, fixture_match, l_version, league_id)

            # if 'telegram' in user['auto-posting'] and result_publish != False:

            #     """ Получение текста """
            #     with open(root_folder / f'parameters/football/users/text/{l_version}_preview_match_tg.json') as file:
            #         tg_json = json.load(file)
            #     with open(root_folder / f'parameters/football/users/dicts/flag_for_tg.json',
            #               encoding='utf-8') as flag_json:
            #         flag_json = json.load(flag_json)

            #     text_for_tg = tg_json['main_text']

            #     """ Получение смайлика флаг по обоим командам """
            #     if league_name1 in flag_json:
            #         if team1 in flag_json[league_name1]: flag_team1 = flag_json[league_name1][team1]
            #         if team2 in flag_json[league_name1]: flag_team2 = flag_json[league_name1][team2]
            #     else:
            #         flag_team1, flag_team2 = '', ''
            #     league_name_tg = ''
            #     if ' ' in league_name1:
            #         league_name_tg = league_name1.replace(" ", "")
            #     else:
            #         league_name_tg = league_name1
            #     """ Добавление переменных """
            #     l_new = ['{league_name_tg}', '{team1_tg}', '{team2_tg}', '{url_publ}', '{flag_team1}', '{flag_team2}',
            #              '{title}']
            #     l2_new = [f"{league_name_tg}2022", team1.replace(' ', ''), team2.replace(' ', ''),
            #               result_publish['link'], flag_team1, flag_team2, title]
            #     l_tags = ['<b>', '<p>', '<li>', '</b>', '</p>', '</li>', '<ul>', '</ul>']

            #     for i in range(len(l_new)):
            #         l2.append(l2_new[i])
            #         l.append(l_new[i])

            #     """ Замена переменных на данных в тексте """
            #     for i in range(len(l)):
            #         if l[i] in text_for_tg:
            #             text_for_tg = text_for_tg.replace(l[i], str(l2[i]))

            #     """ Замена тега </li> на 'пропуск строки' """
            #     for i_t in range(len(l_tags)):
            #         if l_tags[i_t] in text_for_tg:
            #             if l_tags[i_t] == '</li>':
            #                 tag = '\n'
            #             else:
            #                 tag = ''
            #             text_for_tg = text_for_tg.replace(f"{l_tags[i_t]}", tag)

            #     """ Отправка в телегам """
            #     bot_send_message_tg(featured_image_url,
            #                         user['auto-posting']['telegram']['token'],
            #                         user['auto-posting']['telegram']['channel'],
            #                         text_for_tg
            #                         )

    return result_publish

def main_publication2(data, types, key, website):
    # --- Spread into variables ---
    additional_text = ""
    l_version = website.get('l_version') if website.get('l_version') else 'eng'
    featured_image_url = f"{os.getenv('AWS_URL')}/match/{l_version}_{key}_{types}.png"

    # Import message tracker components
    from publication.message_tracker import MessageStage, MessageStatus

    if types == 'transfer':
        website['categories'] = website['transfer_categories']
        player = data["player"]
        transfer = data["transfer"]

        # Player info
        player_id = int(player.get("id")) if player.get("id") else None
        player_name = player.get("name")
        position = player.get("position")
        nationality = player.get("nationality")

        # Transfer info
        from_club = transfer.get("from_club", {}).get("name")
        to_club = transfer.get("to_club", {}).get("name")
        from_country = transfer.get("from_club", {}).get("flag")
        to_country = transfer.get("to_club", {}).get("flag")
        from_league = transfer.get("from_league", {}).get("name")
        to_league = transfer.get("to_league", {}).get("name")
        market_value = transfer.get("market_value")
        fee = transfer.get("fee")
        transfer_date = transfer.get("date")
        transfer_fee = transfer.get("fee")
        transfer_history = player.get("transfer_history")
        market_value_history = player.get("market_value_history")
        player_age = player.get("age")
        date_of_birth = player.get("date_of_birth")
        date_of_joined = transfer.get("date_of_joined")
        contract_expires = transfer.get("contract_expires")
        height = player.get("height")
        
        # --- Dynamic Prompt Logic ---
        prompt_vars = {
            "player_name": player_name,
            "position": position,
            "from_club": from_club,
            "from_country": from_country,
            "to_club": to_club,
            "to_country": to_country,
            "from_league": from_league,
            "to_league": to_league,
            "market_value": market_value,
            "fee": fee,
            "transfer_date": transfer_date,
            "transfer_fee": transfer_fee,
            "transfer_history": json.dumps(transfer_history),
            "market_value_history": json.dumps(market_value_history),
            "player_age": player_age,
            "date_of_birth": date_of_birth,
            "date_of_joined": date_of_joined,
            "contract_expires": contract_expires,
            "height": height,
            "nationality": nationality,
            "all_data": json.dumps(data)
        }
        custom_title = website.get('data', {}).get('transfer_news_title_prompt')
        custom_news = website.get('data', {}).get('transfer_news_content_prompt')

        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            list_text = [
                f" Write a Headline for a transfer news. The headline must be written in the same format as the BBC writes its catchy headlines. The headline must be structured for SEO and AI search discovery: 'player - {player_name}, player position -{position} , linked with club name - {to_club}, country - {to_country}. Examples of the BBC writes its headlines with necessary places for caps are below:\n\nThomas Partey: Ghanaian midfielder leaves Arsenal to join Atletico Madrid.\nMohammed Kudus: Tottenham star on the verge of joining Barcelona.\nIsak in but no Gyokeres in Potter's Sweden squad.\nPalace ask for Leeds game to be moved in fixture pile-up.\n\nHow Athletic Club's unique player policy drives success. You must follow the BBC style for writing headlines as not all words in the headline are capped. The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. Avoid clichés and make it engaging.",

            (
                f"Using information from from the data provided, write a transfer news. The article must be written in the inverted pyramid style of writing articles. Go straight to the article and avoid using redundant words to start the article.Note that these are confirmed transfers so it must be written as such. And you can find the dates for the start of the contract and the end of the contract. So do not write it like a rumour but a confirmed and completed transfer. Do not put dates in the article. Only put dates for the start of the transfer and end of the contract.\n\nPlayer data: {json.dumps(data)}"

                f"Report the article as fact and not reportedly or a speculation. Also note that it is transfer news therefore it must there is a possiblity of someone becoming a free agent based on the information you receive from the data. Use the rest of the player's data like his makret value, date of birth, previous clubs, leagues he has played in nationality or players nationalities (if the players has dual nationality), positions he can play in, previous clubs to enhance the lower parts of aritcle.\n\nDo not invent facts for the article. Do not add quotes. Report only on facts from the data. If the data is not sufficient to write up to the word limit, ignore the word limit. "

                f"Write a detailed football news article (300–500 words) about { player_name } , a { nationality } { position }, who is currently transfer to be linked with a move from { from_club } to { to_club }. Follow these rules:"
                "- Make the article sound natural and human, not formulaic."
                "- Vary writing style, vocabulary, and sentence structure, as if written by different journalists each time."
                "- Use different tones (analytical, emotional, historical, tactical) across different articles."
                f"- Emphasize that { player_name } could be playing abroad, potentially competing in the { to_league } in { to_country } instead of his home country { nationality }."
                f"- Mention the reported transfer date ({ transfer_date }), estimated transfer fee ({ fee }), and the player's market value ({ market_value }) in the context of speculation."
                f"- Include specific recent match details: opponent, date, scoreline, and {player_name}’s performance"
                "- Add season context: appearances, stats, and contributions so far."
                # f"- Show his previews transfers and market values in seperate headings."
                "- Provide both local and international perspectives: how home-country fans, local supporters, and media are reacting to the rumors and potential move."
                "- End with a forward-looking statement about how this possible transfer could shape his career, reputation, or potential if it happens."
                "The article must be written in continuous prose, no bullet points, and should feel like authentic sports journalism."
            ),
        ]

    elif types == 'rumour':
        website['categories'] = website['rumors_categories']
        player = data["player"]
        rumour = data["rumour"]
        metadata = data["metadata"]

        # Player info
        player_id = int(player.get("id")) if player.get("id") else None
        player_name = player.get("name")
        position = player.get("position")
        nationality = player.get("nationality")

        # Transfer info
        from_club = rumour.get("from_club", {}).get("name")
        to_club = rumour.get("to_club", {}).get("name")
        to_country = rumour.get("to_club", {}).get("flag")
        to_league = rumour.get("to_league", {}).get("name")
        market_value = rumour.get("market_value")
        probability = rumour.get("probability")
        rumor_date = rumour.get("date")
        from_country = rumour.get("from_club", {}).get("flag")
        from_league = rumour.get("from_league", {}).get("name")
        transfer_history = player.get("transfer_history")
        market_value_history = player.get("market_value_history")
        player_age = player.get("age")
        date_of_birth = player.get("date_of_birth")
        date_of_joined = rumour.get("date_of_joined")
        contract_expires = rumour.get("contract_expires")
        height = player.get("height")

        """ rumour """

        # --- Dynamic Prompt Logic ---
        prompt_vars = {
            "player_name": player_name,
            "position": position,
            "from_club": from_club,
            "from_country": from_country,
            "to_club": to_club,
            "to_country": to_country,
            "from_league": from_league,
            "to_league": to_league,
            "market_value": market_value,
            "probability": probability,
            "rumor_date": rumor_date,
            "transfer_history": json.dumps(transfer_history),
            "market_value_history": json.dumps(market_value_history),
            "player_age": player_age,
            "date_of_birth": date_of_birth,
            "date_of_joined": date_of_joined,
            "contract_expires": contract_expires,
            "height": height,
            "nationality": nationality,
            "all_data": json.dumps(data)
        }
        custom_title = website.get('data', {}).get('rumor_news_title_prompt')
        custom_news = website.get('data', {}).get('rumor_news_content_prompt')

        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            list_text = [
            f"Write a bold and attention-grabbing headline for the article in the BBC style of writing headlines. The headline must be structured for SEO and AI search discovery: 'player - {player_name}, player position - {position}, linked with club name - {to_club}, country - {to_country}'. You must follow the BBC style for writing headlines as not all words in the headline are capped. Examples of the BBC writes its headlines with necessary places for caps are below: \n\nThomas Partey: Ghanaian midfielder leaves Arsenal to join Atletico Madrid.\nMohammed Kudus: Tottenham star on the verge of joining Barcelona.\nIsak in but no Gyokeres in Potter's Sweden squad.\nPalace ask for Leeds game to be moved in fixture pile-up.\n\nHow Athletic Club's unique player policy drives success" ,

            (
                f"Using information from the data provided, write a BBC-written transfer rumour news article. The article must be written in the inverted pyramid style of writing articles. Go straight to the article. Avoid using redundant words at the start of the opening sentence that makes it took robotic. Note that these are transfers rumours so it must be written as such. Since this is not a confirmed transfer yet, do not state dates for the start of the contract and the end of the contract. So do not write it like a confirmed or completed transfer but a transfer rumour. You must write the article in UK English and not American English.\n\n player data: {json.dumps(data)} "

                f"Report the article as a rumour. Also note that it is transfer news therefore it must there is a possibility of someone becoming a free agent based on the information you receive from the data. Use the rest of the player's data like his market value, date of birth, previous clubs, leagues he has played in nationality or players nationalities (if the players has dual nationality), positions he can play in, previous clubs to enhance the lower parts of article. Bold the first sentence of the article. "

                "Do not invent facts for the article. Do not add quotes. Report only on facts from the data.\n\nWrite the detailed football news article (maximum 300 words) about [Execute previous nodes for preview] , a [Execute previous nodes for preview] [Execute previous nodes for preview], who is currently transfer to be linked with a move from [Execute previous nodes for preview] to [Execute previous nodes for preview]."

                f"Write a detailed football transfer rumours news article (maximum words) about {player_name}, "
                f"a {nationality} {position}, who is currently rumored to be linked with a move from {from_club} to {to_club}. "
                "Follow these rules:\n\n"
                "- Make the article sound natural and human, not formulaic.\n"
                "- Vary writing style, vocabulary, and sentence structure, as if written by different journalists each time.\n"
                "- Use different tones (analytical, emotional, historical, tactical) across different articles.\n"
                f"- Mention the player's market value ({market_value}) in the context of speculation.\n"
                f"- Include specific recent match details: opponent, date, scoreline, and {player_name}’s performance "
                f"- If available, include the reported probability of the move happening (e.g., {probability}).\n"
                # f"- Show his previews transfers and market values in seperate headings."
                "- End with a forward-looking statement about how this possible transfer could shape his career, reputation, or potential if it happens.\n\n"
                "The article must be written in continuous prose, not bullet points, and should feel like authentic sports journalism."
            ),
        ]
        
    elif types == 'player_abroad':
        website['categories'] = website['player_abroad_categories']
        pd = data['playerDetails']
        league_name= data["league"]
        league_country= data["leagueCountry"]
        home_team= data["homeTeam"]
        away_team= data["awayTeam"]
        player_id= data["playerId"]
        player_name= data["playerName"]
        event_type= data["eventType"]
        event_detail= data["eventDetail"]
        team_name= data["team"]
        nationality= pd.get("nationality")

        # --- Dynamic Prompt Logic ---
        prompt_vars = {
            "player_name": player_name,
            "team_name": team_name,
            "event_type": event_type,
            "event_detail": event_detail,
            "league_country": league_country,
            "league_name": league_name,
            "nationality": nationality,
            "all_data": json.dumps(data),
            "home_team": home_team,
            "away_team": away_team,
        }

        custom_title = website.get('data', {}).get('player_abroad_news_title_prompt')
        custom_news = website.get('data', {}).get('player_abroad_news_content_prompt')

        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            headline_prompt = f"Write a bold and attention-grabbing sports news headline for a abroad player. The headline must be structured for SEO and AI search discovery: 'player - {player_name}, team name - {team_name}, event type - {event_type}, event detail - {event_detail}', country - {league_country}. The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. Avoid clichés and make it engaging."
            news_prompt = (
                f" You are a professional sports journalist.  \nWrite a detailed news article between 500 and 700 words about the following football match and the performance of an abroad player (a player competing outside his home country).  \n\nMatch Data (JSON):\n{json.dumps(data)}\n\nGuidelines:\n- Generate a natural, human-like article — not formulaic.  \n- Vary writing style, sentence structure, and vocabulary in every article.  \n- Each time you generate, the article should feel like it comes from a different journalist.  \n- Use different tones: sometimes analytical, sometimes emotional, sometimes focused on history, sometimes focused on tactics.  \n- Emphasize that the player is an abroad player (playing in { league_name } in { league_country } instead of his home country { nationality }.  \n- Include match details: teams, date, score, and player performance (goals, assists, cards, minutes).  \n- Add season context: appearances, stats, contributions so far.  \n- Provide local vs international perspective: how foreign fans, local supporters, or media might see this performance.  \n- End with a forward-looking statement about the player’s career, reputation, or potential.  \n\nRequirements:\n- Length: 500–700 words.  \n- Do not repeat the same sentence structures in multiple articles.  \n- Avoid robotic transitions like “First,” “Secondly,” or “In conclusion.”  \n- Make sure the output is continuous prose, not bullet points.  \n\nOutput:\nWrite only the full news article. No extra explanation."
            )
            list_text = [headline_prompt, news_prompt]

    elif types == 'player_profile':
        website['categories'] = website['player_profiles_categories']
        position= data["position"]
        nationality= data["nationality"]
        player_id= data["id"]
        player_name= data["name"]

        """ player profile """
        
        prompt_vars = {
            "player_name": player_name,
            "position": position,
            "nationality": nationality,
            "all_data": json.dumps(data)
        }
        
        custom_title = website.get('data', {}).get('player_profile_news_title_prompt')
        custom_news = website.get('data', {}).get('player_profile_news_content_prompt')
        
        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            list_text = [
                f"Write a bold and attention-grabbing sports news headline for a player profile. The headline must be structured for SEO and AI search discovery: 'player - {player_name}, position - {position}, nationality - {nationality}. The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. Avoid clichés and make it engaging.",

                (
                    f" You are a professional sports journalist.  \nWrite a detailed news article between 500 and 700 words about the following player profile, nationality, birth, their current year statistics, transfers, and achievements .  \n\nMatch Data (JSON):\n{json.dumps(data)}\n\nGuidelines:\n- Generate a natural, human-like article — not formulaic.  \n- Vary writing style, sentence structure, and vocabulary in every article.  \n- Each time you generate, the article should feel like it comes from a different journalist.  \n- Use different tones: sometimes analytical, sometimes emotional, sometimes focused on history, sometimes focused on tactics. \n- Include player info details: name, position, age, jersy number, birth and player statistics in current year (leaage, team).  \n- Add transfer history: team in, team out, date, \n thier achivements: league, season, country, place.  \n- End with a forward-looking statement about the player’s career, reputation, or potential.  \n\nRequirements:\n- Length: 500–700 words.  \n- Do not repeat the same sentence structures in multiple articles.  \n- Avoid robotic transitions like “Firstly,” “Secondly,” or “In conclusion.”  \n- Make sure the output is continuous prose, not bullet points.  \n\nOutput:\nWrite only the full news article. No extra explanation."
                ),
            ]
        
    elif types == 'social_media':
        website['categories'] = website['social_media_categories']
        handler = data.get('handler', 'Unknown')
        tweet_text = data["tweet_text"]
        tweeted_time = data["timestamp"]
        likes = data["likes"]
        retweets = data["retweets"]
        replies = data["replies"]
        url = data["embedded_url"]

        """ social media """
        
        prompt_vars = {
            "tweet_text": tweet_text,
            "handler": handler,
            "timestamp": tweeted_time,
            "all_data": json.dumps(data)
        }
        
        custom_title = website.get('data', {}).get('social_media_news_title_prompt')
        custom_news = website.get('data', {}).get('social_media_news_content_prompt')
        
        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            list_text = [
                f"Write a professional, SEO-optimized headline for a football news story based on this content: '{tweet_text[:100]}'. "
                "The headline should be compelling and journalistic, suitable for a major sports website. Do NOT mention social media, Twitter, X, or any platform.",

                (
                    f"You are an experienced BBC Sport journalist. Turn the following content into a professional, publication-ready news article for a major sports website.\n\n"
                    f"STRICT RULES (never break these):\n"
                    f"- Do NOT mention X, Twitter, social media, posts, screenshots, platforms, or any source whatsoever.\n"
                    f"- Tone: completely neutral, objective, balanced BBC journalism.\n"
                    f"- Length: 250–400 words by default. Automatically expand to 600–800 words with deeper background, history, expert-style analysis, and implications if the story is major.\n"
                    f"- Use breaking-news style when appropriate: short paragraphs, urgent tone, strong immediate lead.\n"
                    f"- Rephrase informal or first-person quotes into clean indirect/reported speech unless they are formal direct statements from a player, manager, or official club announcement.\n"
                    f"- Naturally incorporate relevant keywords for SEO without stuffing.\n"
                    f"- Structure exactly:\n"
                    f"  • Strong headline\n"
                    f"  • Sub-headline\n"
                    f"  • Lead paragraph (2–3 sentences summarising the news)\n"
                    f"  • Details of the announcement\n"
                    f"  • Background and context\n"
                    f"  • Implications / what it means\n"
                    f"  • Closing paragraph\n\n"
                    f"Tweet content to convert:\n"
                    f"[{tweet_text}]\n\n"
                    f"Now write the full article."
                ),
            ]

        # additional_text = f'<blockquote class="twitter-tweet"><p lang="en" dir="ltr">{tweet_text}</p>&mdash; {handler} (@{handler}) <a href="{url}">{tweeted_time[:10]}</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        
        player_id = 0
        featured_image_url = ""

    elif types == 'where_to_watch':
        website['categories'] = website['where_to_watch_categories']
        season = data["seasons"][0]
        league = data["league"]
        country = data["country"]

        # League info
        player_id = league.get('id')
        league_name = league.get("name")
        country_name = country.get("name")
        start_date = season.get("start")
        tv_channels = data.get("tv_channels")
        season_year = season.get("year")
        end_date = season.get("end")
        logo = league.get("logo")

        """ Where to Watch """
        # print(date)
        
        prompt_vars = {
            "league_name": league_name,
            "country_name": country_name,
            "start_date": start_date,
            "end_date": end_date,
            "season_year": season_year,
            "tv_channels": json.dumps(tv_channels),
            "all_data": json.dumps(data)
        }
        
        custom_title = website.get('data', {}).get('where_to_watch_news_title_prompt')
        custom_news = website.get('data', {}).get('where_to_watch_news_content_prompt')
        
        if custom_news and custom_title:
            news_prompt = replace_vars(custom_news, prompt_vars)
            title_prompt = replace_vars(custom_title, prompt_vars)
            list_text = [title_prompt, news_prompt]
        else:
            list_text = [
                f"Write a bold and attention-grabbing sports news headline for a where to watch league. The headline must be structured for SEO and AI search discovery: 'league name - {league_name}, league country - {country_name}, start date - {start_date}'. The headline should feel natural, like a professional journalist wrote it for a sports newspaper or online publication. Avoid cliches and make it engaging.",

                (
                    f"You are a professional sports journalist.\n"
                    "Write a detailed, natural-sounding news article (500–700 words) about where fans around the world can watch a football league.\n"
                    f"Use the following JSON data as your factual source:\n{json.dumps(data, indent=2)}\n\n"
                    "Guidelines:\n"
                    "- Write the article as if published by a reputable sports outlet — rich in storytelling, tone, and journalistic flow.\n"
                    "Include the following naturally within the text: League name, Country of origin, Start date and end date, Broadcast details for each country, smoothly integrated into the narrative.\n"
                    "Avoid bullet points — use continuous, engaging prose.\n"
                    "- Vary tone and style: sometimes analytical, sometimes emotional, sometimes focused on broadcast innovation or fan culture.\n"
                    "- Avoid repetitive sentence structures and robotic phrasing (no 'Firstly,' or 'In conclusion').\n"
                    "- Make the reader feel the excitement of the new season and the ease of global accessibility through TV and streaming."
                ),
            ]

    index_openai = 0
    main_text_list = []
    for text in list_text:
        index_openai += 1
        result = generate_openai_content(text, types)

        if not result:
            return None
        
        if len(list_text) == 1:
            # Single prompt case: First paragraph is title, rest is body
            paragraphs = result.split("\n\n")
            title_openAI = paragraphs[0]
            if len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    paragraph = paragraph.replace('*',"").strip()
                    if paragraph:
                        main_text_list.append(f"<p>{paragraph}</p>\n")
        else:
            # Original case with multiple prompts
            if index_openai != 1:
                for paragraph in result.split("\n\n"):
                    paragraph = paragraph.replace('*',"").strip()
                    if paragraph:
                        main_text_list.append(f"<p>{paragraph}</p>\n")
            else:
                title_openAI = result

    article_html = f"""
        <article>
        {''.join(main_text_list)}
        {additional_text}
        </article>
        """
    for i in ['"', "'",'*']:
        title_openAI = title_openAI.replace(i, "") if i in title_openAI else title_openAI

    
    return publish(website, "", "", "", featured_image_url, title_openAI, article_html, types, key, l_version, player_id)
        

# main_publication('1286523', 'review', "567")