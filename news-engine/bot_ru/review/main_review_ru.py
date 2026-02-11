#!/root/football_bot/venv_new/bin/python3



# #Сделать запрос к db - fixture match
# #Условие 1, если дата матча = дата сейчас - 105 минут
# #Условие 2, Делаем запрос к апи и смотрим статус 

# from review_text import check_review_match
from datetime import datetime, timedelta
import os
import sys
from time import sleep
import requests
from db import check_fixture_match_review_post_ru, get_fixture_match, check_fixture_match, insert_db, get_date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from publication.app_ru import main_publication_ru #Создание поста на WORDPRESS


def check_status(fixture_match):

    #Запрос в апи, чтобы проверить статус матча
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"        
    headers = {
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    req_check = requests.get(url, headers=headers, params={
        'id':f'{fixture_match}'
    })

    data_check = req_check.json()
    data_review_match = data_check['response'][0]['fixture']['status']['long']

    return data_review_match

# Получение fixture_match. Все матчи которые будут проводиться сегодня
list_fixture_match = get_fixture_match()

list_fixture_match = ['867961']
# date_m = ['2022-10-10T19:00']

if list_fixture_match != False:
    
    for check_time_for_review in range(len(list_fixture_match)):
        
        if check_fixture_match_review_post_ru(f'{list_fixture_match[check_time_for_review]}00000') == True:
            print(12)

            # Получение даты и времени матча по fixture_match
            time_match = datetime.strptime(get_date(list_fixture_match[check_time_for_review]), "%Y-%m-%dT%H:%M")  
                # print(check_status(fixture_match=list_fixture_match[check_time_for_review]))

                # Проверка по дате
            if datetime.now() >= time_match + timedelta(minutes=90):
                    
                #Проверяю статус матча
                if check_status(fixture_match=list_fixture_match[check_time_for_review]) == 'Match Finished':
                    print(12)
                    if check_fixture_match(list_fixture_match[check_time_for_review]) == True :
                        

                        main_publication_ru(list_fixture_match[check_time_for_review], 'review')

                        # Сохранение поста в БД
                        insert_query = (
                            f"INSERT INTO post_review (fixture_match, type)"
                            f"VALUES ('{list_fixture_match[check_time_for_review]}00000', 'ru')"
                        )
                        insert_db(insert_query, 'post_review')
                        # print(list_fixture_match[check_time_for_review])
                    # print(check_status(fixture_match=list_fixture_match[check_time_for_review]))

