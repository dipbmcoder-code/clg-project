# import json
# s = 333333333333333333333333
# if int(predictions_percent_home[:2]) >= int(predictions_percent_away[:2]):
#     win_or_lose = 'победит (победа или ничья)'
# elif int(predictions_percent_home[:2]) <= int(predictions_percent_away[:2]):
#     win_or_lose = 'проиграет (проиграет или ничья)'


# data_review = [{
#         "img_review":"path",
#         "title":f"{name_home_review} - {name_away_review}. {goals_home} : {goals_away}",
#         "subtitle_lineups":{
#             "title":f"Составы игравших команд",
#             "lineups":f"{name_home_review} : {' '.join(lineups_home)} и {name_away_review} : {' '.join(lineups_away)}",
#             "lineups_in_game":f"Замены у {name_home_review}: {subs_home} и замены у {name_away_review}: {subs_away}"
#         },
#         "goals_scorers":{
#             "goals":{
#                 "title":f"Авторы голов:",
#                 "scorers":f"{goal_all_time}",
#                 "total_shots":f"На двоих команды нанесли {total_shots_off} ударов в створ и {total_shots_on} по воротам:",
#                 "shots_team1":f"Команда {name_home_review}:{shots_off_goal_home} ударов в створ, {shots_on_goal_home} по воротам. Самый активный по количеству ударов — {name_home_top_shots}.",
#                 "shots_team2":f"Команда {name_away_review}: {shots_off_goal_away} ударов в створ, {shots_on_goal_away}  по воротам. Больше всего нанёс ударов — {name_away_top_shots}.",
#                 "total_assists":f"В общей сложности у {name_home_review} было {total_assists_home} голевых моментов, у {name_away_review} — {total_assists_away}."
#                 },
#             "defensive":{
#                 "title":f"Оборонительные действия:",
#                 "amount_interseptions":f"Количество перехватов у {name_home_review} — {total_interceptions_home} (лидер — {name_home_top_interceptions}, {amount_home_interceptions} перехватов). У {name_away_review} - {total_interceptions_away}  (больше всего у {name_away_top_interceptions}, {amount_away_interceptions} перехватов).",
#                 "amount_blocks":f"Отборы. {name_home_review} — {total_blocks_home} (больше всех у {name_home_top_block}, {amount_home_block} отборов). {name_away_review} — {total_blocks_away}  (у {name_away_top_block} — {amount_away_block} отборов)."
#                 },
#             "duels":{
#                 "title":f"Единоборства: ",
#                 "subtitle_duels":f"По количеству выигранных единоборств лидерами в командах стали: ",
#                 "amount_duels_team1":f"{name_home_top_duels}, {name_home_review} (количество единоборств - {amount_home_duels})",
#                 "amount_duels_team2":f"{name_away_top_duels}, {name_away_review} (количество единоборств - {amount_away_duels})"
#                 },
#             "ball_pos":{
#                 "title":f"Процент владения мячом: ",
#                 "possession_team1":f"{name_home_review} — {ball_possession_home} процентов",
#                 "possession_team2":f"{name_away_review} — {ball_possession_away} процентов",
#                 "subtitle_for_spent":f"Больше всего игрового времени команды провели на половине Команды 1 / 2 / в центре поля."  #Пока нет параметра
#                 },
#             "fouls":{
#                 "title":f"Наказания: ",
#                 "fouls_yel_team1":f"{name_home_review} *жёлтую* карточку получил(и): {yellow_card_home}",
#                 "fouls_yel_team2":f"{name_away_review} *жёлтую* карточку получил(и): {yellow_card_away}",
#                 "fouls_red_team1":f"{name_home_review} *красную* карточку получил(и): {red_card_home}",
#                 "fouls_red_team2":f"{name_away_review} *красную* карточку получил(и): {red_card_away}"
#                 }
            
#         },
#         "top_players_league":{
#             "title":f"Тройка лидеров в гонке бомбардиров чемпионата:",
#             "top3":{
#                 "first_top":f"1. {topscorer_name_in_league_1}, команда {topscorer_team_in_league_1}(количество {topscorer_amount_in_league_1})",
#                 "second_top":f"2. {topscorer_name_in_league_2}, команда {topscorer_team_in_league_2}(количество {topscorer_amount_in_league_2})",
#                 "third_top":f"3. {topscorer_name_in_league_3}, команда {topscorer_team_in_league_3}(количество {topscorer_amount_in_league_3})"
#             }
#         },
#         "next_matches":{
#             "title":f"Следующие матчи: ",
#             "show_next_matches":{
#                 "next_match_team1":f"Команда {name_home_review} играет с {home_next_match_rival}. {home_date_match_vs_rival}, {home_next_venue_vs_rival}.",
#                 "next_match_team2":f"Команда {name_away_review} играет с {away_next_match_rival}. {away_date_match_vs_rival}, {away_venue_vs_rival}."

#             }
#         }  
#     }]
    



# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file)










# f"SELECT player_a_name, players_a_goals_total FROM match_preview WHERE id_team_home_preview = "


# import boto3
# access_key = 'KEY'
# secret_access_key = 'KEY'



# client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

# # client.upload_file('/root/result/img_preview/878003_preview.png', 'botbot-buckets-football', 'preview/878003_preview.png')
# s = client.put_object(ACL='public-read', Bucket='botbot-buckets-football', Key='preview/881859_preview.png', Body='/root/result/img_preview/881859_preview.png')
    
# import base64
# import requests
# l = {3:'EPL', 4:'La Liga', 5:'Serie A', 6:'Bundesliga', 7:'Ligue 1'}
# def test():   
#     url = 'https://botbot.news/wp-json/wp/v2/posts'
#     user = 'botbot'
#     password = 'cGvj MT0x lqRl cEuY tddX huHk'

#     credentials = user + ':' + password

#     token = base64.b64encode(credentials.encode())
#     header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#     post = {
#     'title'    : 'test1',
#     'status'   : 'publish', #тип
#     'content'  : 'text',
#     'categories': [1, 7], # category ID
#     # 'tags'       : [1,5],
#     'date'   : f'2022-10-02T19:13:00'   # время публикации --  {время матча - один день} 
#     }
#     # '2022-09-30T8:00:00'
#     # '2022-10-02T19:13'
#     #f'{date - timedelta(days=1)}'
#     responce = requests.post(url , headers=header, json=post)
#     print(responce.text)
# # test()
# import json


# league_name1 = 'La Liga'
# team1 = 'Barcelona'
# team2 = 'Real Madrid'
# data_tags = {
#     "English Premier League": {
#         "Manchester City":"8",
#         "Liverpool":"11"
#         },
#     "La Liga" : {
#         "Barcelona":"12", 
#         "Real Madrid":"13"
#         },
#     "Ligue 1" : {
#         "PSG":"14", 
#         "Marseille":"15"
#         },
#     "Serie A" :{
#         "Napoli":"16", 
#         "Atalanta":"17"
#         },
#     "Bundesliga" : {
#         "Union Berlin":"18", 
#         "Freiburg":"19"
#         }
# }
# # data_tags = json.dumps(data_tags, skipkeys = True)
# # data_tags = json.loads(data_tags)
# tags1 = data_tags[league_name1][team1]
# tags2 = data_tags[f'{league_name1}'][team2]
# tags2 = data_tags['La Liga']['Barcelona2']
# print(tags2)


# import os
# import requests


# def restImgUL(fixture_match):
#     url='https://botbot.news/wp-json/wp/v2/posts'
#     data = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_review.png"
#     res = requests.post(url='https://botbot.news/wp-json/wp/v2/posts',
#                         data=data,
#                         headers={ f'Content-Type': 'image/jpg','Content-Disposition' : f'attachment; filename={fixture_match}'},
#                         auth=('authname', 'authpass'))
#     # pp = pprint.PrettyPrinter(indent=4) ## print it pretty. 
#     # pp.pprint(res.json()) #this is nice when you need it
#     newDict=res.json()
#     # newID= newDict.get('id')
#     # link = newDict.get('guid').get("rendered")
#     # print(newID) 
#     # print(link)
#     # return (newID, link)
# # restImgUL("868033")


# import base64, requests, json

# def header():
#     user = 'botbot'
#     password = 'cGvj MT0x lqRl cEuY tddX huHk'

#     credentials = user + ':' + password
#     token = base64.b64encode(credentials.encode())
#     header_json = {'Authorization': 'Basic ' + token.decode('utf-8')}
#     return header_json

# def upload_image_to_wordpress(fixture_match, types, url, header_json):
#     media = {'file': open(f'/root/result/img_match/{fixture_match}_{types}.png', 'rb'),'caption': f'{fixture_match}_{types}'}
#     responce = requests.post(url + "wp-json/wp/v2/media", headers = header_json, files = media)
#     r = responce.json()
#     print(r['id'])

# hed = header() #username, application password                       
# upload_image_to_wordpress('868027', 'review', 'https://botbot.news/',hed)
# l = ['s', 'ss2', 's5']
# team1 = 'ss'
# team2 = 's5'
# if team1 in l or team2 in l:
#     print('ss')

# class N:
#     name = 'name'
#     age = 'age'
#     def __init__(self, name, age):
#         name = self.name
#         age = self.age

#  - getAll() Должен возвращать изначальный массив элементов.
#  - getItem(id) Принимает id элемента и возвращает сам объект элемента;
#  - getChildren(id) Принимает id элемента и возвращает массив элементов, являющихся дочерними для того элемента,
# чей id получен в аргументе. Если у элемента нет дочерних, то должен возвращаться пустой массив;
#  - getAllParents(id) Принимает id элемента и возвращает массив из цепочки родительских элементов,
# начиная от самого элемента, чей id был передан в аргументе и до корневого элемента,
# т.е. должен получиться путь элемента наверх дерева через цепочку родителей к корню дерева. Порядок элементов важен!
# class TreeStore:
#     def get_all():
#         id = items['id']
#         parent = items['parent']
        


# items = [
#     {"id": 1, "parent": "root"},
#     {"id": 2, "parent": 1, "type": "test"},
#     {"id": 3, "parent": 1, "type": "test"},
#     {"id": 4, "parent": 2, "type": "test"},
#     {"id": 5, "parent": 2, "type": "test"},
#     {"id": 6, "parent": 2, "type": "test"},
#     {"id": 7, "parent": 4, "type": None},
#     {"id": 8, "parent": 4, "type": None}
# ]
# ts = TreeStore(items)



# l_id = ['1123', '2233', '1123']
# l_name = ['name1', 'name2', 'name3']
# l_amount = ['2', '4', '1']

# player_update(l_id, l_name, l_amount, 'goals')

# import requests


# url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"          #V3 - Fixtures
# headers = {
#         "X-RapidAPI-Key": "ed9df9b66dmsh3488c78a45168b3p1f47e6jsn129a6c17d435",
#         "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
#     }
# req_all = requests.get(url, headers=headers, params={
#         "id":'868025'
#     })


# data_all = req_all.json()

# if data_all['response'][0]['lineups']:
#     print(123)
from db import chec_in_db, get_old_data, insert_db

def update_teams(dict_list):
    team_id= dict_list["team_id"]
    name = dict_list["name"]
    season = dict_list["season"]
    league_id = dict_list["league_id"]

    list_data = ['wins', 'loses','draws','clean_sheet_count', 'goals', 'without_scored_count', 'conceded_goals', 'conceded_goals_count', 'injuries_count']

    if team_id != '':
        insert_query_for_check = f"SELECT team_id_api FROM teams WHERE team_id_api = {team_id}"
        
        # update
        if chec_in_db(insert_query_for_check) == True:
            for i in range(len(list_data)):
                data = dict_list['list_data'][list_data[i]]  #1
                data_name = [list_data[i]]  #wins
                data_name = data_name[0]
                old_data = get_old_data(team_id , data_name, 'teams', '1', 'team_id_api')   #22
                print(type(data))
                if data != '0':
                    if old_data == 0:
                        insert_query = f" UPDATE teams SET {data_name} = {data} WHERE team_id_api = {team_id};"

                    elif old_data != 0:
                        insert_query = f" UPDATE teams SET {data_name} = {data_name} + {data} WHERE team_id_api = {team_id};"
                    
                    insert_db(insert_query, 'update team')
        # create
        elif chec_in_db(insert_query_for_check) == False:
            d = dict_list['list_data']
            wins, loses,draws,clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count = d['wins'],d['loses'],d['draws'],d['clean_sheet_count'],d['goals'],d['without_scored_count'],d['conceded_goals'],d['conceded_goals_count'],d['injuries_count']
            print(loses)

            insert_query = (
                f" INSERT INTO teams(team_id_api,wins, loses,draws,clean_sheet_count, goals, without_scored_count, conceded_goals, conceded_goals_count, injuries_count,name, season, league_id)" 
                f" VALUES ('{team_id}', '{wins}','{loses}','{draws}','{clean_sheet_count}', '{goals}', '{without_scored_count}', '{conceded_goals}', '{conceded_goals_count}', '{injuries_count}','{name}', '{season}', '{league_id}')"
                    )
                    
            insert_db(insert_query, 'add team')

team_id = '11'
data_home = {
    "team_id":f"{team_id}",
    "league_id":"0",
    "season":"1",
    "name":"name",
    "list_data":{
        "wins":"1",
        "loses":"0",
        "draws":"0",
        "clean_sheet_count":"0",
        "goals":f"1",
        "without_scored_count":"0",
        "conceded_goals":"0",
        "conceded_goals_count":"0",
        "injuries_count":"1"
    }
}
# update_teams(data_home)

import psycopg2
host = '127.0.0.1'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
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
            #print(result)
            return result
            

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

# insert_query = (
#         f"SELECT max(goals), name AS FA FROM players WHERE league_id=39 AND goals != 0 GROUP BY name ORDER BY FA DESC;"
#     )
insert_query = (
        f"SELECT precent_accuracy AS S , name FROM teams_round WHERE league_id=39 AND precent_accuracy != 0 GROUP BY name ORDER BY S DESC;"
    )
precent_accuracy = check_stat_preview(insert_query)

for i in range(len(precent_accuracy)):
    for i2 in range(len(precent_accuracy[i])):
        pass

# index_top_player_goals = check_stat_preview(insert_query)
# n_1 = index_top_player_goals[0]
# n_2 = index_top_player_goals[1]
# n_3 = index_top_player_goals[2]
# n_4 = index_top_player_goals[3]
# n_5 = index_top_player_goals[4]

# goals_top_league_1, name_top_goals_league_1,  = n_1[0], n_1[1]
# goals_top_league_2, name_top_goals_league_2,  = n_2[0], n_2[1]
# goals_top_league_3, name_top_goals_league_3,  = n_3[0], n_3[1]
# goals_top_league_4, name_top_goals_league_4,  = n_4[0], n_4[1]
# goals_top_league_5, name_top_goals_league_5,  = n_5[0], n_5[1]


# print(goals_top_league_5, name_top_goals_league_5)

# print(name_top_goals_league)
# print(goals_top_league)

team1 = []
team2 = []
date = []
r = ''
for i in range(len(date)):
    r = r + f'<ul>{team1[i]} - {team2[i]}'
