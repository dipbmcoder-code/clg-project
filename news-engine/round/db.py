import psycopg2

host = 'localhost'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
import psycopg2

def insert_db(insert_query, types):
    try:
        connection = psycopg2.connect ( 
            host = 'localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
            database = 'db_match'
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query)

            connection.commit()
            print(f'[INFO] new round insert in db {types}')

        

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def find_belated_round(league_id, round, type1):
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
            database = 'db_match'
        )
        with connection.cursor() as cursor:
            insert_query = (
                        f"SELECT id FROM round_{type1} WHERE rounds={round} AND league_id = {league_id};"
                    )

            cursor.execute(insert_query)
            result = cursor.fetchall()
            if result == []:
                return True
            else:
                return False
    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()



def check_round_in_db(league_id, round, db_name, data, types):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host = 'localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
            database = 'db_match'
        )
        
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                # data - отвечает за столбец в БД
                # db - отвечает за название БД
                f"SELECT {data} FROM {db_name} WHERE league_id={league_id} AND round = {round} AND type LIKE '{types}';"
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
def get_all_match_for_round(round, league_id, type1):
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
            database = 'db_match'
        )
        with connection.cursor() as cursor:
            insert_query = (
                        f"SELECT fixture_match FROM match_{type1} WHERE round={round} AND league = {league_id};"
                    )

            cursor.execute(insert_query)
            result = cursor.fetchall()
            list_f = []
            if result != []:
                for i in range(len(result)):
                    list_f.append(result[i][0])
            # print(list_id)
            return list_f
    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def take_date_in_review(insert_query):
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
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

def check_stat(insert_query):
    '''Вытаскиваем всю статистику'''
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
            connection.commit()
            return result
            

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def check_stat_preview(insert_query):
    '''Вытаскиваем всю статистику'''
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
            connection.commit()
            return result
            

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()


def get_data_round(insert_query):

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

def total_of_round_name(name, view, rounds):
    insert_query = (
        "SELECT {} FROM players_round WHERE round = {} AND name LIKE '{}'".format(view, rounds, name)
    )
    result = check_stat_preview(insert_query)
    if result != []:
        return result[0][0]
    else:
        return 0

def total_of_round_name(name, view, rounds):
    insert_query = (
        "SELECT {} FROM players_round WHERE round = {} AND name LIKE '{}'".format(view, rounds, name)
    )
    result = check_stat_preview(insert_query)
    if result != []:
        return result[0][0]
    else:
        return 0
def total_summ(types, league_id, rounds):
    insert_query = (
        f"SELECT {types} FROM teams_round WHERE round = {rounds} AND league_id = {league_id} AND {types} != 0"
    )
    result = check_stat_preview(insert_query)
    result2 = 0
    for i in range(len(result)):
        if result[i][0] != None:
            result2 = int(result[i][0]) + result2
    return result2
# print(total_of_round_name('Erling Haaland','goals', '10'))
def get_user_id_main(types, rounds, league_id, season, view):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host='localhost',
            user='db_user',
            password='baaI$SkBvZ~P',
            database='db_match'
        )
        # Создаем курсор
        with connection.cursor() as cursor:

            if view == 'summ':
                insert_query = (
                        f"SELECT {types} FROM players_round WHERE round = {rounds} AND league_id = {league_id} AND season = {season} AND {types} != 0;"
                )
                cursor.execute(insert_query)
                result = cursor.fetchall()
                l=[]
                

                result2 = 0
                for i in range(len(result)):
                    if result[i][0] != None:
                        result2 = int(result[i][0]) + result2

                return result2
            elif view == 'h3':
                insert_query = (
                        f"SELECT name, max(goals) AS Test, team_id, fixture_match FROM players_round WHERE round = {rounds} AND league_id = {league_id} AND season = {season} AND {types} != 0 AND {types} >= 2 GROUP BY name ,team_id, fixture_match ORDER BY Test DESC;"
                )
                cursor.execute(insert_query)
                result = cursor.fetchall()
                l1= []  #leader

                names = []
                amouts = []
                team_id = []
                fixtures = []
                # l2 =[]  # another
                for i in range(len(result)):
                    name = result[i][0]
                    names.append(name.replace(" ", "_"))
                    amouts.append(f'{result[i][1]}')
                    insert_query = (
                        f"SELECT name FROM teams WHERE team_id_api={result[i][2]};"
                    )
                    team_name = check_stat_preview(insert_query)
                    team_name = team_name[0][0]
                    team_id.append(team_name.replace(" ", "_"))
                    fixtures.append(f'{result[i][3]}')

                return names, amouts, team_id, fixtures
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()


# print(get_user_id_main('goals', '9', '39', '2022', 'h3'))

