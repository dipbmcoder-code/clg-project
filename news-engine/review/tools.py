import os
import sys
import requests
from dotenv import load_dotenv
import psycopg2
load_dotenv()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from review.insert_review_api import insert_review_match_api

host = '127.0.0.1'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'


def check_in_db(insert_query, types):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            if types == 'get':
                result = cursor.fetchall()
                connection.commit()

                return result
            elif types == 'del':
                connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    finally:
        if connection:
            connection.close()

def clear_all_match():


    """ Get fixtures """
    query_for_get = f"SELECT fixture_match FROM match_preview"
    result_fixture = check_in_db(query_for_get, 'get')
    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # querystring = {
    #     "league": league_id,
    #     "season": "2022"
    # }
    # headers = {
    #     "X-RapidAPI-Key": "ed9df9b66dmsh3488c78a45168b3p1f47e6jsn129a6c17d435",
    #     "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    # }
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # json_dict = response.json()
    # list_id = []
    # for i in range(len(json_dict['response'])):
    #     list_id.append(json_dict['response'][i]['fixture']['id'])

    """ Del review and update_fixture DB (fixture) """
    # db = ['match_review', 'update_fixture']
    # for i_db in range(len(db)):
    #     for i in range(len(result_fixture)):
    #         if db == "match_review": data = 'fixture_match_for_check'
    #         else: data = 'fixture_match'
    #         query_for_del = f"DELETE FROM {db[i_db]} WHERE {data}='{result_fixture[i][0]}'"
    #         result = check_in_db(query_for_del, 'del')

    """ Del dbs (fixture) """
    # if league_id == '1': db_list_for_del = ['players_cup', 'teams_cup']
    # if league_id != '1': db_list_for_del = ['players', 'players_round', 'teams', 'teams_round']
    # for i_del_db in range(len(db_list_for_del)):
    #     query_for_del = f"DELETE FROM {db_list_for_del[i_del_db]}"
    #     result = check_in_db(query_for_del, 'del')

    """ ADD review DB (fixture) """
    for i_fixture_add in range(len(result_fixture)):
        insert_review_match_api(result_fixture[i_fixture_add][0])

    """ DEL preview DB (fixture) """
    # for i_del in range(len(result_fixture)):
    #     query_for_del = f"DELETE FROM match_preview WHERE fixture_match ='{result_fixture[i_del][0]}'"
    #     result = check_in_db(query_for_del, 'del')
    #
    # """ Add preview """
    # for i_fixture_add in range(len(result_fixture)):
    #     insert_preview_match_api(result_fixture[i_fixture_add][0])

clear_all_match()
def add_preview():

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    querystring = {
        "league": "1",
        "season": "2022"
    }
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_dict = response.json()
    list_id = []
    for i in range(len(json_dict['response'])):
        list_id.append(json_dict['response'][i]['fixture']['id'])
    # result_fixture = check_in_db(query_for_get, 'get')



# add_preview()