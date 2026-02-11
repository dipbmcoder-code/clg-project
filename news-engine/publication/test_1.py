import psycopg2

def search_value(insert_query):
    l = []
    try:
        connection = psycopg2.connect(
            host='localhost',
            user = 'db_user',
            password = 'baaI$SkBvZ~P',
            database = 'db_match'
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()

            for i in range(len(result)): l.append(result[i][0])
            return l

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    finally:
        if connection:
            connection.close()


""" Получаем все айди команд """
list_team_id = search_value(f'SELECT team_id_api FROM teams_cup')
list_teams = []
list_precent_teams = []

for i_team in range(len(list_team_id)):
    querry_get_precent = search_value(f'SELECT precent_accuracy FROM teams_cup_round WHERE team_id_api={list_team_id[i_team]}')
    total_precent,count = 0, len(querry_get_precent)
    if querry_get_precent != []:
        for i_precent in range(len(querry_get_precent)):
            total_precent = total_precent + querry_get_precent[i_precent]
    if total_precent != 0 and len(querry_get_precent) != 0:
        precent_accuracy = int(total_precent) // len(querry_get_precent)
        list_precent_teams.append(precent_accuracy)
    else:     list_precent_teams.append(0)
    list_teams.append(list_team_id[i_team])



# MAX
index_max = list_precent_teams.index(max(list_precent_teams))
top_precent_acc = max(list_precent_teams)
top_teams_acc = list_teams[index_max]
# MIN
index_min = list_precent_teams.index(min(list_precent_teams))
top_teams_acc = list_teams[index_min]
min_precent_acc = min(list_precent_teams)

