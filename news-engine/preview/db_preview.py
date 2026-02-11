# Импорт для работы с postgresql
import psycopg2

# Импорт данных БД
from preview.config import host, db_name, password, user


def check_form(insert_query_form):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query_form)
            result = cursor.fetchall()
            connection.commit()
            return result


    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def check_team(team_id, league, season):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            if league == '1' or league == 1: players = 'players_cup'
            else: players = 'players_test'
            insert_query = (
                f"SELECT * FROM {players} WHERE team_id = {team_id} AND season = {season};"
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

def get_top_player(data_types, team_id, limit, league, season):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            if league == 1 or league == '1': players = 'players_cup'
            else: players = 'players_test'
            insert_query =(
                f"SELECT name, max({data_types}) AS S FROM {players} WHERE team_id = {team_id} AND {data_types} != 0 AND season = {season} GROUP BY name ORDER BY S DESC LIMIT {limit}"
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

def check_fixture_match_preview_post(fixture_match, websiteId):
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
                f"""SELECT fixture_match FROM match_preview WHERE fixture_match={fixture_match} AND is_posted AND website_ids @> '["{websiteId}"]'::jsonb;"""
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

def get_data(insert_query):

    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
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

def get_request_db(output_query_home):
    '''Вытаскиваем данные из ревью бд, суммируем между играми, выбираем максимальное количество по событиям и добавляем в бд превью '''
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        
        #Создаем курсор
        with connection.cursor() as cursor:

            cursor.execute(output_query_home)
            result1 = cursor.fetchall()
            connection.commit()
            return result1


           
    except Exception as _ex:
            print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()


def check_match_for_insert(id_team, id_team_in_db):
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
                f"SELECT fixture_match FROM review_top_players WHERE {id_team_in_db}={id_team};"  #f"SELECT fixture_match FROM match_review WHERE {id_team_in_db}={id_team};"
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

def check_form_preview(insert_query_form):
     #Вытаскиваем Forms из ревью бд

    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query_form)
            result1 = cursor.fetchall()
            connection.commit()
            return result1
            

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()