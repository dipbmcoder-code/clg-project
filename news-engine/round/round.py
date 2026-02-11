#!/opt/envs/venv_310/bin/python3

import psycopg2
from db import insert_db, get_all_match_for_round, check_round_in_db, find_belated_round
from API import check_match_round_api, check_all_rounds, get_date_next_round, check_match_list_rounds_api, get_round, get_date_last_fixture_round_now
from insert_tour_preview import main_insert_preview_round
from img_preview_round import start_create_img_preview_round, delete
from img_review_round import start_create_img_review_round
from insert_tour_review import main_start_review_round
from text_preview_tour import preview_round_text
from text_review_tour import review_round_text
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from datetime import datetime, timedelta
from publication.app_for_round_test import main_publication

"""
Документация

Делаем цикл по списку всех лиг


    Превью тура
        Получаем номер тура
        Получаем список игр с АПИ, получаем их с БД и делаем проверку
        Проверям есть ли этот тур в БД, если нет делаем проверку по дате и времени (должно быть 9 часов до начала первого матча)
            Запускаем поулчение данных + запись в БД     insert_tour_preview
            Создание текста    text_preview_round.py
            Картинка    img_preview_round.py
            Публикация    publication/app_for_round.py
            Запись в БД превью тур пост, что манипуляция (алгоритм) произошела


    Ревью тура
        Получаем номер тура
        Проходим цикл по двум туром (обьяснение строка 168)
            Получаем список игр с АПИ, получаем их с БД и делаем проверку на то что все матчи завершены
            Далее
            Запускаем поулчение данных + запись в БД  insert_tour_review.py
            Создание текста  text_review_round.py
            Картинка   img_review_round.py
            Публикация  publication/app_for_round.py
            Запись в БД ревью тур пост, что манипуляция (алгоритм) произошела


"""

"""  Список всех лиг  """
list_league_id = ['39', '61', '78', '140', '135', '94']
if list_league_id != []:

    for league in range(len(list_league_id)):
        round_now = get_round(list_league_id[league], 2022)
        # preview
        for i in range(2):
            round_now = int(round_now) + 1 if i == 2 else int(round_now)

            if find_belated_round(list_league_id[league], round_now, 'preview') == True:
                all_round_api = check_match_list_rounds_api(list_league_id[league], '2022', round_now)
                list_all_fixture_match = get_all_match_for_round(round_now, list_league_id[league], 'preview')
                list_all_fixture_match_api = all_round_api[0]

                # if list_all_fixture_match_api != [] or list_all_fixture_match != []:
                date = get_date_next_round(list_league_id[league], '2022', round_now)

                if date != '':

                    if datetime.now() >= date - timedelta(hours=9):

                        if check_round_in_db(list_league_id[league], round_now, 'round', 'id', 'preview') == False:

                            """ Создание данных + запись в БД  """
                            main_insert_preview_round(round_now, list_league_id[league], '2022')
                            """ Создание текста  """
                            preview_round_text(round_now, list_league_id[league])
                            """ Создание картинки  """
                            start_create_img_preview_round(round_now, list_league_id[league])
                            """ Публикация  """
                            main_publication(round_now, 'preview', list_league_id[league])
                            """ Удаление картинок с сервера """
                            delete(list_league_id[league], round_now, 'preview')

                            """ Запись в БД что алгоритм прошел  """
                            insert_query = (
                                f"INSERT INTO round(round, league_id, season, type)"
                                f"VALUES ('{round_now}','{list_league_id[league]}','2022','preview');"
                            )
                            insert_db(insert_query, 'round_preview_POST')

        # review
        for i in range(3):

            """
            АПИ не всегда обновлчяет номер раунда
            Из-за этого проходимся сразу по двум
            """
            c = 1
            if i == 0:
                round_for_review = int(round_now)
            elif i == 1:
                round_for_review = int(round_now) - 1
            elif i == 2:
                round_for_review = int(round_now) + 1

            if find_belated_round(list_league_id[league], int(round_for_review), 'review') == True:

                """
                Убрать все эти проверки
                
                Добавить новую:
                Если последний матч тура (делаем спислок по дате и выбираем самую большу (последнию)) закончился == True
                
                """
                date_last_match = get_date_last_fixture_round_now(list_league_id[league], '2022', round_for_review)
#                date_last_match = datetime.strptime(date_last_match, "%Y-%m-%dT%H:%M")

                if date_last_match != '':

                    if datetime.now() >= date_last_match + timedelta(hours=2):


                        if check_round_in_db(list_league_id[league], round_for_review, 'round', 'id',
                                             'review') == False:

                            if check_round_in_db(list_league_id[league], round_for_review, 'round', 'id',
                                                 'preview') == True:
                                """ Создание данных + запись в БД  """
                                main_start_review_round(round_for_review, list_league_id[league], '2022')
                                """ Создание текста  """
                                review_round_text(round_for_review, list_league_id[league])
                                """ Создание картинки  """
                                start_create_img_review_round(round_for_review, list_league_id[league])
                                """ Публикация  """
                                main_publication(round_for_review, 'review', list_league_id[league])
                                """ Удаление картинок с сервера """
                                delete(list_league_id[league], round_for_review, 'review')

                                """ Запись в БД что алгоритм прошел  """
                                insert_query = (
                                    f"INSERT INTO round(round, league_id, season, type)"
                                    f"VALUES ('{round_for_review}','{list_league_id[league]}','2022', 'review');"
                                )
                                insert_db(insert_query, 'round_review_POST')
