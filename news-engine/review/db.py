# Импорт для работы с postgresql
import psycopg2
	
# Импорт данных БД
from review.config import host, db_name, password, user
from datetime import datetime, timedelta

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

def insert_top_db_home(insert_query_home, types):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query_home)

            connection.commit()
            print(f'[INFO] new insert in top__home_db {types}')

        

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def insert_top_db_away(insert_query_away, types):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query_away)

            connection.commit()
            print(f'[INFO] new insert in top_away_db {types}')

        

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def chec_in_db(insert_query):
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


def get_one_data(insert_query):
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

            # Создаем запрос в БД. Сам запрос в 'insert_query'
            cursor.execute(insert_query)
            # Записываем результат
            result = cursor.fetchall()
            return result

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()

def get_league(fixture_match):
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

            # Создаем запрос в БД. Сам запрос в 'insert_query'
            insert_query = (
                f"SELECT league FROM match_preview WHERE fixture_match={fixture_match};"
            )
            cursor.execute(insert_query)
            # Записываем результат
            result = cursor.fetchone()
            return result

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
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
def check_fixture_match_review_post(fixture_match, websiteId):
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
                f"""SELECT fixture_match FROM match_review WHERE fixture_match = '{str(fixture_match)}' AND is_posted AND website_ids @> '["{websiteId}"]'::jsonb;"""
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
def get_fixture_match(types, list_date):
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
            # print(types)
            list_fixture_MAIN = []
            if types == 'list':
                for date in list_date:
                    d = f'{date}'
                    # d = '2023-01-15'

                    # print(f"SELECT fixture_match,league FROM match_preview WHERE date_match2={d.replace('-','')}")
                    insert_query = (
                        #f"SELECT fixture_match FROM match_preview WHERE fixture_match3={fixture_match};",
                        f"SELECT fixture_match,league FROM match_preview WHERE date_match2={d.replace('-','')};"
                    )
                    # Создаем запрос в БД. Сам запрос в 'insert_query'
                    cursor.execute(insert_query)
                    # Записываем результат
                    result1 = cursor.fetchall()
                    # if result1 == []:
                    #     return False
                    # else:
                    for i in range(len(result1)):
                        list_fixture_MAIN.append(result1[i][0])
                        # print(list_id)

                return list_fixture_MAIN
            else:
                date = datetime.now().date()
                yesterday = date - timedelta(days=1)
                d = f'{date}'
                y = f'{yesterday}'
                # d = '20230115'
                # print(f"SELECT fixture_match FROM match_preview WHERE date_match2={d.replace('-','')} or date_match2={y.replace('-','')}")
                insert_query = (
                    # f"SELECT fixture_match FROM match_preview WHERE fixture_match3={fixture_match};",
                    f"SELECT fixture_match FROM match_preview WHERE date_match2={d.replace('-', '')} or date_match2={y.replace('-','')};"
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



def get_test_fixture_match(insert_query_test):
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
                       
            cursor.execute(insert_query_test)
            # Записываем результат
            result_find_fixture = cursor.fetchall()
            list_id = []
            for i in range(len(result_find_fixture)):
                list_id.append(result_find_fixture[i][0])
            
            if len(list_id) > 2: 
                return False
            elif len(list_id) == 0:
                return True
        
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()

def check_form(insert_query_form):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
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



# Для суммирования


def check_player(player_id, db, round, season, league_id, team_id):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            add_query = f" AND season = {season} AND league_id = {league_id}"

            if "round" in db:
                insert_query = (
                    f"SELECT * FROM {db} WHERE player_id_api = {player_id} AND round ={round}{add_query}"
                )
            else:
                insert_query = (
                    f"SELECT team_id FROM {db} WHERE player_id_api = {player_id}{add_query}"
                )

            cursor.execute(insert_query)
            result = cursor.fetchall()
            
            if result == []: 
                return False
            else:
                # print(result)
                if result[0][0] in ['None', None]:
                    insert_db(
                        f"UPDATE {db} SET team_id={team_id} "
                        f"WHERE player_id_api = {player_id}{add_query}", "test update team_id"
                    )
                return True
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def get_old_data(id, data_type, db, round, view_type, season):
    try:
        connection = psycopg2.connect ( 
            host= host,
            user = user,
            password = password,
            database = db_name
        )
        with connection.cursor() as cursor:
            r = ''
            if db == 'players_round':
                r = f' AND round={round}'
            insert_query = (
                f"SELECT {data_type} FROM {db} WHERE {view_type} = {id}{r} AND season = {season}"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            if result != []:
                # print(result)
                if result[0][0] == None:
                    return '0'
                return result[0][0]
            return '0'
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def check_fixture_match_in_db(fixture_match, db, data):
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
                # data - отвечает за столбец в БД
                # db - отвечает за название БД
                f"SELECT fixture_match FROM {db} WHERE {data}={fixture_match};"
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


def check_fixture_match_in_db_with_round(id, db, data, round):
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
                # data - отвечает за столбец в БД
                # db - отвечает за название БД
                f"SELECT id FROM {db} WHERE {data}={id} AND round = {round};"
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



def check_form_review(insert_query_form):
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
#