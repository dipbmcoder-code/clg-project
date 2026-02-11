#!/root/football_bot/venv/bin/python3


# ФУНКЦИЯ ДЛЯ РУССКОЙ ВЕРСИИ ПРЕВЬЮ МАТЧА

# Импорт
import requests

import sys
import os

from datetime import datetime, timedelta

from distutils.core import setup


# ИМПОРТ ФУНКЦИЙ
# from insert_preview_api import insert_preview_match_api  #Сохранение в БД
from db import check_fixture_match, insert_db, check_fixture_match_preview_post_ru  #Импорт функций которые работают с БД

# Скрипт для иморта с другого каталога
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from publication.app_ru import main_publication_ru #Создание поста на WORDPRESS



# Сохранение результаты в переменные
# api = check_match() 
# fixture_m = api[0]
# date_m = api[1]


#TODO JSON файлы будут сохраняются так: {fixture_match}_{types}_ru.json
#TODO Картинки будут сохраняются так: {fixture_match}_{types}_ru.png



# Ближайшие матчи-
def check_match():  # Функция будет принимать:  !!! league, season !!!  Данные будут взяты с подписки юзера
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"        # V3 - Next {x} Fixtures to come
    headers = {
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    req_gen = requests.get(url, headers=headers, params={
        "league": "39", 
        "season": "2022",
        "next": "7"
    })
    req_gen2 = requests.get(url, headers=headers, params={
        "league": "78", 
        "season": "2022",
        "next": "7"
    })
    req_gen3 = requests.get(url, headers=headers, params={
        "league": "61", 
        "season": "2022",
        "next": "7"
    })
    req_gen4 = requests.get(url, headers=headers, params={
        "league": "135", 
        "season": "2022",
        "next": "7"
    })
    req_gen5 = requests.get(url, headers=headers, params={
        "league": "140", 
        "season": "2022",
        "next": "7"
    })
    req_gen6 = requests.get(url, headers=headers, params={
        "league": "94", 
        "season": "2022",
        "next": "7"
    })
    
    data_gen = req_gen.json()
    data_gen2 = req_gen2.json()
    data_gen3 = req_gen3.json()
    data_gen4 = req_gen4.json()
    data_gen5 = req_gen5.json()
    data_gen6 = req_gen6.json()
    
    fixture_m = []
    date_m = []

    #Цикл добавления списков даты и айди матча в списки  
    for num in range(len(data_gen['response'])):
        fixture_match = data_gen['response'][num]['fixture']['id']
        date_match = data_gen['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match)
        date_m.append(date_match)
    
    for num in range(len(data_gen2['response'])):
        fixture_match2 = data_gen2['response'][num]['fixture']['id']
        date_match2 = data_gen2['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match2)
        date_m.append(date_match2)
    
    for num in range(len(data_gen3['response'])):
        fixture_match3 = data_gen3['response'][num]['fixture']['id']
        date_match3 = data_gen3['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match3)
        date_m.append(date_match3)

    for num in range(len(data_gen4['response'])):
        fixture_match4 = data_gen4['response'][num]['fixture']['id']
        date_match4 = data_gen4['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match4)
        date_m.append(date_match4)

    for num in range(len(data_gen5['response'])):
        fixture_match5 = data_gen5['response'][num]['fixture']['id']
        date_match5 = data_gen5['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match5)
        date_m.append(date_match5)
    
    for num in range(len(data_gen6['response'])):
        fixture_match6 = data_gen6['response'][num]['fixture']['id']
        date_match6 = data_gen6['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match6)
        date_m.append(date_match6)

    return fixture_m, date_m



# Сохранение результаты в переменные
api = check_match() 
fixture_m = api[0]
date_m = api[1] 
# fixture_m = ['867961']
# date_m = ['2022-08-15T19:00']



# Цикл по ближайшим матчам + проверка + запуск генерации запросов в АПИ
for check_time in range(len(date_m)):
    if check_fixture_match_preview_post_ru(f'{fixture_m[check_time]}00000') == False:

        # Дата ближайших матчей
        time_match = datetime.strptime(date_m[check_time], "%Y-%m-%dT%H:%M")  

        # Проверка по дате
        if datetime.now() >= time_match - timedelta(hours=7, minutes=30):
                        
            # 1  Проверка есть ли в БД данный fixture_match 
            if check_fixture_match(fixture_m[check_time]) == True:

                main_publication_ru(fixture_m[check_time], 'preview')
                
                insert_query = (
                            f"INSERT INTO post_preview (fixture_match, type)"
                            f"VALUES ('{fixture_m[check_time]}00000', 'ru')"
                        )
                insert_db(insert_query, 'post_preview')




