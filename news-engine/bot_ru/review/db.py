from datetime import datetime, timedelta
import psycopg2

from config import host, db_name, password, user

def check_fixture_match_review_post_ru(fixture_match):
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
                f"SELECT fixture_match FROM match_review WHERE fixture_match_for_check={fixture_match};"
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
def get_fixture_match():
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
            date = datetime.now().date()
            d = f'{date}'
            # d = '20221016'

            
            insert_query = (
                #f"SELECT fixture_match FROM match_preview WHERE fixture_match3={fixture_match};",
                f"SELECT fixture_match FROM match_preview WHERE date_match2={d.replace('-','')};"
            )
            # Создаем запрос в БД. Сам запрос в 'insert_query' 
            cursor.execute(insert_query)
            # Записываем результат
            result1 = cursor.fetchall()
            if result1 == []: 
                return False
            else:
                list_fixture_match = []
                for i in range(len(result1)):
                    list_fixture_match.append(result1[i][0])
                # print(list_id)
                return list_fixture_match
        
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()
def get_date(fixture_match):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT date_match FROM match_preview WHERE fixture_match3 = {fixture_match}"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result[0][0]
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()