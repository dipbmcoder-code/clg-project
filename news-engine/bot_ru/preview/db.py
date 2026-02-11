# Импорт для работы с postgresql
import os
import sys
import psycopg2

# Импорт данных БД
from config import host, db_name, password, user
def check_team(team_id):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT * FROM players WHERE team_id = {team_id}"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            if result == []: 
                return False
            else:
                return True
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def get_top_player(data_types, team_id, limit):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            insert_query =(
                f"SELECT name, max({data_types}) AS S FROM players WHERE team_id = {team_id} AND {data_types} != 0 GROUP BY name ORDER BY S DESC LIMIT {limit}"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            if limit == '1': 
                if result != []:

                    result0 = result[0][0]
                    result1 = result[0][1]

                    if result[0][0] == None:
                        result0 = ''
                    if result[0][1] == None:
                        result1 = '0'

                    return result0, result1
                elif result == []:
                    return result
            else:
                if result != []:
                    return result
                elif result == []:
                    return result
            print(result)
            connection.commit()
            # print(f'[INFO] new insert in db {types}')

        

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

# Инсерт (сохранение) в Бд
def insert_db(insert_query, types):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query)

            connection.commit()
            # print(f'[INFO] new insert in db {types}')

        

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


# Проверка есть ли fixture_match в БД
def check_fixture_match(fixture_match):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT fixture_match FROM match_preview WHERE fixture_match3={fixture_match};"
            )
            # Создаем запрос в БД. Сам запрос в 'insert_query' 
            cursor.execute(insert_query)
            # Записываем результат
            result = cursor.fetchall()
            if result == []: 
                return False
            else:
                return True
   
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()

def check_fixture_match_preview_post_ru(fixture_match):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT fixture_match FROM post_preview WHERE fixture_match={fixture_match} AND type LIKE 'ru';"
            )
            # Создаем запрос в БД. Сам запрос в 'insert_query' 
            cursor.execute(insert_query)
            # Записываем результат
            result = cursor.fetchall()
            if result == []: 
                return False
            elif result != []:
                return True
   
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()
#Запрос к бд превью, чтобы вытащить для ревью дату матча и добавить ид матча
def check_fixture_match_date(date_match):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT date_match FROM match_preview WHERE date_match={date_match};"
            )
            # Создаем запрос в БД. Сам запрос в 'insert_query' 
            cursor.execute(insert_query)
            # Записываем результат
            result1 = cursor.fetchall()
            if result1 == []: 
                return False
            else:
                return True
    
        
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()

    return result1
