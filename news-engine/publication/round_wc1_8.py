import psycopg2
import requests
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import json
import base64
import boto3
import os
from time import sleep
from urllib.request import urlopen
from dotenv import load_dotenv
load_dotenv()

host = '3.70.209.102'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
def check_stat_round_wc(insert_query):
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

insert_query = (
    f"SELECT fixture_match FROM match_review WHERE league = '1';"
    )
amount_games = len(check_stat_round_wc(insert_query))

insert_query = (
    f"SELECT league_name FROM match_review WHERE league = '1';"
    )
league_name1 = check_stat_round_wc(insert_query)
league_name = league_name1[0][0]
league_name = f"FIFA {league_name} 2022"


url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"

headers = {
	"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
	"X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
}

req = requests.get(url, headers=headers, params={
    "league":"1",
    "season":"2022",
    "next":"8"
})

data_next_games = req.json()

team_home = []
team_away = []

for takes_games in range(len(data_next_games['response'])):
    team_home.append(data_next_games['response'][takes_games]['teams']['home']['name'])
    team_away.append(data_next_games['response'][takes_games]['teams']['away']['name'])



insert_query = (
    f"SELECT name, max(goals) AS S FROM teams_cup GROUP BY name ORDER BY S DESC LIMIT 1;"
    )
max_goals = check_stat_round_wc(insert_query)
max_amount_goals = max_goals[0][1]
max_goals_team = max_goals[0][0] 



insert_query = (
    f"SELECT name, min(goals) AS Q FROM teams_cup GROUP BY name ORDER BY Q ASC LIMIT 1;"
    )
min_goals = check_stat_round_wc(insert_query)
min_amount_goals = min_goals[0][1]
min_goals_team = min_goals[0][0] 


# insert_query = (
#     f"SELECT max(precent_accuracy) AS K, team_id_api FROM teams_cup_round GROUP BY team_id_api ORDER BY K DESC LIMIT 1;"
# )
# index_max_accuracy = check_stat_round_wc(insert_query)
# max_accuracy = index_max_accuracy[0][0]
# team_id_max_accuracy = index_max_accuracy[0][1]
# print(max_accuracy, team_id_max_accuracy)

# list_team_id = check_stat_round_wc(f'SELECT team_id_api FROM teams_cup')
# print(list_team_id)
# list_teams = []
# list_precent_teams = []

# for i_team in range(len(list_team_id)):
#     querry_get_precent = check_stat_round_wc(f'SELECT precent_accuracy FROM teams_cup_round WHERE team_id_api={list_team_id[0][i_team]}')
#     print(querry_get_precent)
#     total_precent = 0
#     count = len(querry_get_precent)
#     if querry_get_precent != []:
#         for i_precent in range(len(querry_get_precent)):
#             total_precent = total_precent + querry_get_precent[i_precent]
#     if total_precent != 0 and len(querry_get_precent) != 0:
#         precent_accuracy = int(total_precent) // len(querry_get_precent)
#         list_precent_teams.append(precent_accuracy)
#     else:     list_precent_teams.append(0)
#     list_teams.append(list_team_id[i_team])


# index = list_precent_teams.index(max(list_precent_teams))
# print(list_precent_teams, list_teams)
# top_precent_acc = max(list_precent_teams)
# top_teams_acc = list_teams[index]
# print(top_teams_acc, top_precent_acc)


insert_query = (
    f"SELECT sum(goals) FROM teams_cup;"
    )
all_goals = check_stat_round_wc(insert_query)
all_amount_goals = all_goals[0][0]

insert_query = (
    f"SELECT sum(penalty) FROM players_cup;"
    )
all_goals_penalty = check_stat_round_wc(insert_query)
all_amount_goals_penalty = all_goals_penalty[0][0]

average_goals_in_game = int(all_amount_goals) // int(amount_games)

#graph
fig = go.Figure()
fig.add_trace(go.Bar(x=['2002', '2006', '2010', '2014', '2018', '2022'] ,y=[130, 117, 101, 136, 122, all_amount_goals],
                     base=0,
                     text=[130, 117, 101, 136, 122, all_amount_goals],
                     marker_color='magenta',
                     name='expenses'))
fig.update_traces(textposition='outside')
fig.update_layout(font_size=30, uniformtext_minsize=40, uniformtext_mode='hide')

fig.write_image(f'/opt/footballBot/result/img_match/graph_wc.png', width=1900, height=1100) #Меняю размер таблицы

access_key = 'AKIA6MTJZAMUJMX2K77J'
secret_access_key = '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'

client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)


client.upload_file(f"/opt/footballBot/result/img_match/graph_wc.png","buckets-botbot-football", f"match/graph_wc.png", ExtraArgs={'ACL':'public-read'})

sleep(5) #5 Секунд паузы, для того чтобы отправилось
os.remove(f'/opt/footballBot/result/img_match/graph_wc.png')
    
img_all_wc = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/graph_wc.png\" alt=\"\">"



insert_query = (
        f'SELECT name, min(fast_goal), team_id AS S, fixture_match_for_fast_goal FROM players_cup WHERE fast_goal != 0 GROUP BY name, team_id, fixture_match_for_fast_goal ORDER BY S DESC LIMIT 1;'
    )

index_fast_goal = check_stat_round_wc(insert_query)
index_fast_goal = index_fast_goal[0]
player_fast_goal = index_fast_goal[0]
minute_fast_goal = index_fast_goal[1]
id_team_fast_goal = index_fast_goal[2]
id_game_fast_goal = index_fast_goal[3]


insert_query = (
    f"SELECT name FROM teams_cup WHERE team_id_api = {id_team_fast_goal}"
)
index_team_fast_goal = check_stat_round_wc(insert_query)
team_fast_goal = index_team_fast_goal[0][0]

insert_query = (
    f"SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE fixture_match_for_check = {id_game_fast_goal}"
)
index_stat_game_fast_goal = check_stat_round_wc(insert_query)
index_stat_game_fast_goal = index_stat_game_fast_goal[0]
name_home_fast_goal = index_stat_game_fast_goal[0]
name_away_fast_goal = index_stat_game_fast_goal[1]
count_home_fast_goal = index_stat_game_fast_goal[2]
count_away_fast_goal = index_stat_game_fast_goal[3]

#Подумать над выводом забитых и пропущенных голов
list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']

insert_query = (
    f"SELECT list_for_goal_home FROM match_preview \
            WHERE league = '1' "
)
index_list_for_home = check_stat_round_wc(insert_query)

insert_query = (
    f"SELECT list_missed_goal_home \
         FROM match_preview \
            WHERE league = '1' "
)
index_list_missed_home = check_stat_round_wc(insert_query)

insert_query = (
    f"SELECT list_for_goal_away FROM match_preview \
            WHERE league = '1' "
)
index_list_for_away = check_stat_round_wc(insert_query)

insert_query = (
    f"SELECT list_missed_goal_away \
         FROM match_preview \
            WHERE league = '1' "
)
index_list_missed_away = check_stat_round_wc(insert_query)

for_goals = []


for all_for_goals in range(len(index_list_for_home)):
    list1 = for_goals
    for_goals = []
    for sum_for_goals in range(len(index_list_for_home[0][0].split())):
        if index_list_for_home[all_for_goals][0].replace('%', '').split()[sum_for_goals] == '0' and index_list_for_away[all_for_goals][0].replace('%', '').split()[sum_for_goals] == '0':
            sum_amount = int(index_list_for_home[all_for_goals][0].replace('%', '').split()[sum_for_goals]) + int(index_list_for_away[all_for_goals][0].replace('%', '').split()[sum_for_goals])
        else:
            sum_amount = float(index_list_for_home[all_for_goals][0].replace('%', '').split()[sum_for_goals]) + float(index_list_for_away[all_for_goals][0].replace('%', '').split()[sum_for_goals])
        for_goals.append(sum_amount)
    for count_for_goals in range(8):
        if list1 == []:
            continue
        else:
            for_goals[count_for_goals] = list1[count_for_goals] + for_goals[count_for_goals]

for find_average in range(len(for_goals)):
    for_goals[find_average] = for_goals[find_average] % int(amount_games)
    for_goals[find_average] = str(for_goals[find_average])[:5] + '%'



missed_goals = []

for all_missed_goals in range(len(index_list_missed_home)):
    list2 = missed_goals
    missed_goals = []
    for sum_missed_goals in range(len(index_list_for_home[0][0].split())):
        if index_list_missed_home[all_missed_goals][0].replace('%', '').split()[sum_missed_goals] == '0' and index_list_missed_away[all_missed_goals][0].replace('%', '').split()[sum_missed_goals] == '0':
            sum_amount2 = int(index_list_missed_home[all_missed_goals][0].replace('%', '').split()[sum_missed_goals]) + int(index_list_missed_away[all_missed_goals][0].replace('%', '').split()[sum_missed_goals])       
        else:
            sum_amount2 = float(index_list_missed_home[all_missed_goals][0].replace('%', '').split()[sum_missed_goals]) + float(index_list_missed_away[all_missed_goals][0].replace('%', '').split()[sum_missed_goals])
        missed_goals.append(sum_amount2)
    for count_missed_goals in range(8):
        if list2 == []:
            continue
        else:
            missed_goals[count_missed_goals] = list1[count_missed_goals] + missed_goals[count_missed_goals]

for find_average2 in range(len(missed_goals)):
    missed_goals[find_average2] = missed_goals[find_average2] % int(amount_games)
    missed_goals[find_average2] = str(missed_goals[find_average2])[:5] + '%'

insert_query =(
    f"SELECT team_id_api, name, max(destroyer_total) AS K FROM teams_cup WHERE destroyer_total != 0 GROUP BY team_id_api, name ORDER BY K DESC LIMIT 1;"
)
index_top_destroyer = check_stat_round_wc(insert_query)
index_top_destroyer = index_top_destroyer[0]
top_detroyer_id_team = index_top_destroyer[0]
top_detroyer_name_team = index_top_destroyer[1]
top_detroyer_total_amount = index_top_destroyer[2]

insert_query = (
    f"SELECT interceptions, blocks, tackles, saves FROM teams_cup WHERE team_id_api = {top_detroyer_id_team}"
)
index_stat_top_destroyer = check_stat_round_wc(insert_query)
index_stat_top_destroyer = index_stat_top_destroyer[0]
top_destroyer_interseptions = index_stat_top_destroyer[0]
top_destroyer_blocks = index_stat_top_destroyer[1]
top_destroyer_tackles = index_stat_top_destroyer[2]
top_destroyer_saves = index_stat_top_destroyer[3]

insert_query = (
    f"SELECT name FROM players_cup WHERE team_id = {top_detroyer_id_team} AND saves != 0"
)
index_name_goalkeeper_top_destroyer = check_stat_round_wc(insert_query)
index_name_goalkeeper_top_destroyer = index_name_goalkeeper_top_destroyer[0]
name_goalkeeper_top_destroyer = index_name_goalkeeper_top_destroyer[0]

insert_query = (
    f"SELECT team_id_api, name, max(creator_total) AS G FROM teams_cup WHERE creator_total != 0 GROUP BY team_id_api, name ORDER BY G DESC LIMIT 1;"
)
index_top_creator = check_stat_round_wc(insert_query)
index_top_creator = index_top_creator[0]
id_team_top_creator = index_top_creator[0]
name_team_top_creator = index_top_creator[1]
amount_top_creator = index_top_creator[2]

insert_query = (
    f"SELECT duels, shots_on_target, shots_of_target FROM teams_cup WHERE team_id_api = {id_team_top_creator}"
)
index_stat_top_creator = check_stat_round_wc(insert_query)
index_stat_top_creator = index_stat_top_creator[0]
duels_top_creator = index_stat_top_creator[0]
shots_on_top_creator = index_stat_top_creator[1]
shots_off_top_creator = index_stat_top_creator[2]


#Статистика по игрокам:


insert_query = (
    f"SELECT name, max(goals), team_id AS L FROM players_cup WHERE goals != 0 GROUP BY name, team_id ORDER BY L DESC LIMIT 1;"
)
index_max_goals = check_stat_round_wc(insert_query)
name_max_goals_player = index_max_goals[0][0]
amount_max_goals_player = index_max_goals[0][1]
id_team_max_goals_player = index_max_goals[0][2]

insert_query = (
    f"SELECT name FROM teams_cup WHERE team_id_api = {id_team_max_goals_player}"
)
index_max_goals_player_his_team = check_stat_round_wc(insert_query)
max_goals_player_his_team = index_max_goals_player_his_team[0][0]


#############

insert_query = (
    f"SELECT name, max(goals) AS H, team_id FROM players_cup WHERE goals != 0 GROUP BY name, team_id ORDER BY H DESC LIMIT 5;"
)
index_top_players_league = check_stat_round_wc(insert_query)

top_player_in_league_1 = index_top_players_league[0][0]
top_player_in_league_2 = index_top_players_league[1][0]
top_player_in_league_3 = index_top_players_league[2][0]
top_player_in_league_4 = index_top_players_league[3][0]
top_player_in_league_5 = index_top_players_league[4][0]

top_amount_in_league_1 = index_top_players_league[0][1]
top_amount_in_league_2 = index_top_players_league[1][1]
top_amount_in_league_3 = index_top_players_league[2][1]
top_amount_in_league_4 = index_top_players_league[3][1]
top_amount_in_league_5 = index_top_players_league[4][1]

top_teams_goals = []
for g in range(5):
    insert_query = (
        f"SELECT name FROM teams_cup WHERE team_id_api = {index_top_players_league[g][2]}"
    )
    index_teams_goals = check_stat_round_wc(insert_query)
    top_teams_goals.append(index_teams_goals[0][0])


# insert_query = (
#     f"SELECT topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_name_in_league_4, \
#     topscorer_name_in_league_5, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, \
#     topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_1, topscorer_team_in_league_2, \
#     topscorer_team_in_league_3, topscorer_team_in_league_4, topscorer_team_in_league_5 FROM match_review WHERE fixture_match = '855769'"
# )
# index_top_players_league = check_stat_round_wc(insert_query)
# print(index_top_players_league)
# top_player_in_league_1 = index_top_players_league[0][0]
# top_player_in_league_2 = index_top_players_league[0][1]
# top_player_in_league_3 = index_top_players_league[0][2]
# top_player_in_league_4 = index_top_players_league[0][3]
# top_player_in_league_5 = index_top_players_league[0][4]

# top_amount_in_league_1 = index_top_players_league[0][5]
# top_amount_in_league_2 = index_top_players_league[0][6]
# top_amount_in_league_3 = index_top_players_league[0][7]
# top_amount_in_league_4 = index_top_players_league[0][8]
# top_amount_in_league_5 = index_top_players_league[0][9]

# top_team_in_league_1 = index_top_players_league[0][10]
# top_team_in_league_2 = index_top_players_league[0][11]
# top_team_in_league_3 = index_top_players_league[0][12]
# top_team_in_league_4 = index_top_players_league[0][13]
# top_team_in_league_5 = index_top_players_league[0][14]

insert_query = (
    f"SELECT name, max(assists) AS H, team_id FROM players_cup WHERE assists != 0 GROUP BY name, team_id ORDER BY H DESC LIMIT 5;"
)
index_top_assists = check_stat_round_wc(insert_query)

top_assists_player_in_league_1 = index_top_assists[0][0]
top_assists_player_in_league_2 = index_top_assists[1][0]
top_assists_player_in_league_3 = index_top_assists[2][0]
top_assists_player_in_league_4 = index_top_assists[3][0]
top_assists_player_in_league_5 = index_top_assists[4][0]

top_assists_amount_in_league_1 = index_top_assists[0][1]
top_assists_amount_in_league_2 = index_top_assists[1][1]
top_assists_amount_in_league_3 = index_top_assists[2][1]
top_assists_amount_in_league_4 = index_top_assists[3][1]
top_assists_amount_in_league_5 = index_top_assists[4][1]

top_teams_assists = []
for g in range(5):
    insert_query = (
        f"SELECT name FROM teams_cup WHERE team_id_api = {index_top_assists[g][2]}"
    )
    index_teams_assists = check_stat_round_wc(insert_query)
    top_teams_assists.append(index_teams_assists[0][0])


insert_query = (
    f"SELECT name, max(saves) AS H, team_id FROM players_cup WHERE saves != 0 GROUP BY name, team_id ORDER BY H DESC LIMIT 5;"
)
index_top_saves = check_stat_round_wc(insert_query)

top_saves_player_in_league_1 = index_top_saves[0][0]
top_saves_player_in_league_2 = index_top_saves[1][0]
top_saves_player_in_league_3 = index_top_saves[2][0]
top_saves_player_in_league_4 = index_top_saves[3][0]
top_saves_player_in_league_5 = index_top_saves[4][0]

top_saves_amount_in_league_1 = index_top_saves[0][1]
top_saves_amount_in_league_2 = index_top_saves[1][1]
top_saves_amount_in_league_3 = index_top_saves[2][1]
top_saves_amount_in_league_4 = index_top_saves[3][1]
top_saves_amount_in_league_5 = index_top_saves[4][1]

top_teams_saves = []
for t in range(5):
    insert_query = (
        f"SELECT name FROM teams_cup WHERE team_id_api = {index_top_saves[t][2]}"
    )
    index_teams_saves = check_stat_round_wc(insert_query)
    top_teams_saves.append(index_teams_saves[0][0])


#Карточки

insert_query = (
        f"SELECT fixture_match, max(total_cards_in_game) AS B FROM match_review WHERE league='1' GROUP BY fixture_match ORDER BY B DESC LIMIT 1;"
    )
index_find_top_fouls_season = check_stat_round_wc(insert_query)


index_find_top_fouls_season = index_find_top_fouls_season[0]

fix_match_top_fouls_of_round, count_top_fouls_of_round = index_find_top_fouls_season[0], index_find_top_fouls_season[1]

insert_query = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away, count_yel_card, count_red_card FROM match_review WHERE fixture_match_for_check={fix_match_top_fouls_of_round} ;"
    )

index_find_top_fouls_season1 = check_stat_round_wc(insert_query)

index_find_top_fouls_season1 = index_find_top_fouls_season1[0]
top_fouls_team_name_home , top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, top_fouls_total_yel_card, top_fouls_total_red_card = index_find_top_fouls_season1[0], index_find_top_fouls_season1[1], index_find_top_fouls_season1[2], index_find_top_fouls_season1[3], index_find_top_fouls_season1[4], index_find_top_fouls_season1[5]




insert_query = (
    f"SELECT name, max(y_cards) AS F, team_id, r_cards FROM players_cup WHERE y_cards != 0 GROUP BY name, team_id, r_cards ORDER BY F DESC LIMIT 3;"
)

index_top3_players_with_cards = check_stat_round_wc(insert_query)

name_top3_fouls_of_world_cup = []
ycards_top3_fouls_of_world_cup = []
rcards_top3_fouls_of_world_cup = []
id_team_cards_top3_fouls_of_world_cup = []

for i in range(len(index_top3_players_with_cards)):
    r_card = index_top3_players_with_cards[i][3]
    name_top3_fouls = index_top3_players_with_cards[i][0]
    id_team_cards_top3_fouls_of_world_cup1 = index_top3_players_with_cards[i][2]
    if r_card == None:
        r_card = 0
    name_top3_fouls_of_world_cup.append(name_top3_fouls.replace(" ", "_"))
    ycards_top3_fouls_of_world_cup.append(index_top3_players_with_cards[i][1])
    rcards_top3_fouls_of_world_cup.append(r_card)
    id_team_cards_top3_fouls_of_world_cup.append(id_team_cards_top3_fouls_of_world_cup1)

name_teams_cards_top3_fouls_of_world_cup = []
for find_team_for_top3_cards in range(len(id_team_cards_top3_fouls_of_world_cup)):
    insert_query = (
        f"SELECT name FROM teams_cup WHERE team_id_api={id_team_cards_top3_fouls_of_world_cup[find_team_for_top3_cards]}"
    )
    index_find_teams_for_top3_cards= check_stat_round_wc(insert_query)
  
    index_find_teams_for_top3_cards = index_find_teams_for_top3_cards[0][0]
    name_teams_cards_top3_fouls_of_world_cup.append(index_find_teams_for_top3_cards.replace(" ", "_"))


for f in range(len(name_top3_fouls_of_world_cup)):
    name_top3_fouls_of_world_cup[f] = name_top3_fouls_of_world_cup[f].replace("_", " ")
    name_teams_cards_top3_fouls_of_world_cup[f] = name_teams_cards_top3_fouls_of_world_cup[f].replace("_", " ")



text_1_8 = ''
for knockouts in range(len(team_home)):
    text_1_8 = text_1_8 + f"<li>{team_home[knockouts]} - {team_away[knockouts]}</li>" 

all_table_goals = ''

for goals in range(len(list_minute)):
    all_table_goals = all_table_goals + f"<tr> \
        <td style= 'background-color: #e0d3d3;'>{list_minute[goals]}</td> \
        <td style= 'background-color: #b1e0b8;'>{for_goals[goals]}</td> \
        <td style= 'background-color: #ebc996;'>{missed_goals[goals]}</td> \
        </tr>"

top3_fouls_text_ru = ''
for fouls_text in range(3):
    top3_fouls_text_ru = top3_fouls_text_ru + f"<li>{name_top3_fouls_of_world_cup[fouls_text]}, <b>{ycards_top3_fouls_of_world_cup[fouls_text]}</b> желтых + <b>{rcards_top3_fouls_of_world_cup[fouls_text]}</b> красных ({name_teams_cards_top3_fouls_of_world_cup[fouls_text]})</li>"

top3_fouls_text_eng = ''
for fouls_text in range(3):
    top3_fouls_text_eng = top3_fouls_text_eng + f"<li>{name_top3_fouls_of_world_cup[fouls_text]}, <b>{ycards_top3_fouls_of_world_cup[fouls_text]}</b> yellow + <b>{rcards_top3_fouls_of_world_cup[fouls_text]}</b> red ({name_teams_cards_top3_fouls_of_world_cup[fouls_text]})</li>"


title_ru = f"{league_name}: Самая интересная статистика чемпионата мира"
text_ru = (
    f"<p>Чемпионат мира в Катаре закончился. Команды сыграли <b>{amount_games}</b> матчей, по результатам которых сформировались следующие пары ⅛ финала.</p>"

    f'<ul>'
        f"{text_1_8}"
    f'</ul>'

    f'<p>И вот самые интересные цифры чемпионата мира.'

    f'<p><h3>Голы</h3>'

        f'<p>Больше всего голов на этом этапе забила команда <b>{max_goals_team}</b> — <b>{max_amount_goals}</b> голов. Меньше всего — <b>{min_goals_team}</b> (<b>{min_amount_goals}</b> голов).'

        f'<p>Все сборные вместе забили <b>{all_amount_goals}</b> голов. Из них — <b>{all_amount_goals_penalty}</b> с пенальти. В среднем команды забивали по <b>{average_goals_in_game}</b> голов за игру.'

        f'{img_all_wc}'

        f'<p>Самый быстрый гол в чемпионате был забит в матче <b>{name_home_fast_goal}</b> и <b>{name_away_fast_goal}</b>. {player_fast_goal} (<b>{team_fast_goal}</b>) забил на {minute_fast_goal} минуте. Финальный счёт того матча <b>{count_home_fast_goal}</b> — <b>{count_away_fast_goal}</b>.'

        f'<p>Если игру разбить на временные отрезки, то вот так выглядит процент забитых и пропущенных мячей в эти периоды.'

        f"<table align='center' border='1'>"
            f'<tbody>'
            f"<tr align='center' valign='center'>"
                f"<td style= 'background-color: #e0d3d3;'><b>Интервал</b></td>"
                f"<td style= 'background-color: #b1e0b8;'><b>Забитые голы, %</b></td>"
                f"<td style= 'background-color: #ebc996;'><b>Пропущенные голы, %</b></td>"
            f"</tr>"
                f"{all_table_goals}"
            f'</tbody>'
        f"</table>"

    f'<p><h3>Эффективность команд:</h3>'
        f'<p><b>Главный разрушитель чемпионата</b> — <b>{top_detroyer_name_team}</b>. Игроки этой команды вместе сделали <b>{top_destroyer_interseptions}</b> перехватов, <b>{top_destroyer_blocks}</b> блокировок ударов, <b>{top_destroyer_tackles}</b> подкатов, а вратарь команды — {name_goalkeeper_top_destroyer} сделал <b>{top_destroyer_saves}</b> сейвов. В общей сложности — <b>{top_detroyer_total_amount}</b> разрушающих действий.'

        f'<p><b>Главный созидатель чемпионата</b> — <b>{name_team_top_creator}</b>. Игроки суммарно выиграли <b>{duels_top_creator}</b> дуэлей, нанесли <b>{shots_on_top_creator}</b> ударов по воротам и <b>{shots_off_top_creator}</b> ударов в сторону ворот. Всего — <b>{amount_top_creator}</b> созидательных действий.'

        f'<p><b>Команда с лучшим качеством пасов</b> — Бельгия (95% удачных пасов из 981). Хуже всего дела обстояли у Саудовской Аравии (только 72% из 722 пасов дошли до адресатов).'
        
    f'<p><h3>Статистика по игрокам:</h3>'

        f'<p>Больше всего голов на чемпионате мира забил {name_max_goals_player} из <b>{max_goals_player_his_team}</b> (<b>{amount_max_goals_player}</b>).'

        f'<b><p>Вот так выглядит пятёрка лучших нападающих турнира по итогам чемпионата:</b>'
        f'<ul>'
            f'<li> {top_player_in_league_1}, (<b>{top_amount_in_league_1}, {top_teams_goals[0]}</b>).</li>'
            f'<li> {top_player_in_league_2}, (<b>{top_amount_in_league_2}, {top_teams_goals[1]}</b>).</li>'
            f'<li> {top_player_in_league_3}, (<b>{top_amount_in_league_3}, {top_teams_goals[2]}</b>).</li>'
            f'<li> {top_player_in_league_4}, (<b>{top_amount_in_league_4}, {top_teams_goals[3]}</b>).</li>'
            f'<li> {top_player_in_league_5}, (<b>{top_amount_in_league_5}, {top_teams_goals[4]}</b>).</li>'
        f'</ul>'

        f'<p>Как мы видим, лидер среди бомбардиров забил пока что <b>{top_amount_in_league_1}</b> голов. Ниже можно увидеть, кто и сколько забивал на предыдущих чемпионатах мира (до 2002 года включительно):'


    f"<table align='center' border='1'>"
        f"<tbody>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>Год</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>Голы</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Игрок</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Команда</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2018</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>5</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Harry Kane</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Англия</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2014</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>6</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>James Rodriguez</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Колумбия</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2010</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>6</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Thomas Muller</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Германия</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2006</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>5</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Miroslav Klose</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Германия</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2002</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>8</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Ronaldo</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Бразилия</b></td>"
        f"</tr>"
        f"</tbody>"
    f"</table>"
    f'<b><p>По голевым передачам на этом чемпионате мира пятёрка лучших пока выглядит так:</b>'
    f'<ul>'
       
        f'<li> {top_assists_player_in_league_1}, (<b>{top_assists_amount_in_league_1}, {top_teams_assists[0]}</b>).</li>'
        f'<li> {top_assists_player_in_league_2}, (<b>{top_assists_amount_in_league_2}, {top_teams_assists[1]}</b>).</li>'
        f'<li> {top_assists_player_in_league_3}, (<b>{top_assists_amount_in_league_3}, {top_teams_assists[2]}</b>).</li>'
        f'<li> {top_assists_player_in_league_4}, (<b>{top_assists_amount_in_league_4}, {top_teams_assists[3]}</b>).</li>'
        f'<li> {top_assists_player_in_league_5}, (<b>{top_assists_amount_in_league_5}, {top_teams_assists[4]}</b>).</li>'
    f'</ul>'
    f'<b><p>Ну и лучшие голкиперы по общему количеству сейвов за весь чемпионат мира:</b>'
    f'<ul>'
        f'<li> {top_saves_player_in_league_1}, (<b>{top_saves_amount_in_league_1}, {top_teams_saves[0]}</b>).</li>'
        f'<li> {top_saves_player_in_league_2}, (<b>{top_saves_amount_in_league_2}, {top_teams_saves[1]}</b>).</li>'
        f'<li> {top_saves_player_in_league_3}, (<b>{top_saves_amount_in_league_3}, {top_teams_saves[2]}</b>).</li>'
        f'<li> {top_saves_player_in_league_4}, (<b>{top_saves_amount_in_league_4}, {top_teams_saves[3]}</b>).</li>'
        f'<li> {top_saves_player_in_league_5}, (<b>{top_saves_amount_in_league_5}, {top_teams_saves[4]}</b>).</li>'
    f'</ul>'
    f'<p>Что касается жёлтых и красных карточек, то самый грязный матч по этому параметру — игра между <b>{top_fouls_team_name_home}</b> и <b>{top_fouls_team_name_away}</b> (<b>{top_fouls_total_yel_card}</b> жёлтых и <b>{top_fouls_total_red_card}</b> красных). Итоговый счёт этого матча <b>{top_fouls_goals_home}</b> — <b>{top_fouls_goals_away}</b>.'

    f'<b><p>И вот топ 3 игроков с наибольшим количеством карточек за групповой этап:</p></b>'
    f'<ul>'
        f"{top3_fouls_text_ru}"
    f'</ul>'
        )

title_eng = f"{league_name}: The most interesting stats of the world cup"

text_eng = (

    f"<p>The world cup of the FIFA World Cup is over. The teams played <b>{amount_games}</b> matches. This is the list of teams for knockouts:</p>"

    f'<ul>'
        f"{text_1_8}"
    f'</ul>'

    f"<h3><p>Let’s see the most interesting stats so far.</p></h3>"

    f"<p><h3>Goals:</h3></p>"

    f"<p>Most goals during the world cup were scored by <b>{max_goals_team}</b> (<b>{max_amount_goals}</b>). Fewest goals scored by <b>{min_goals_team}</b> (<b>{min_amount_goals}</b>).</p>"

    f"<p>All the teams scored <b>{all_amount_goals}</b> goals (<b>{all_amount_goals_penalty}</b> from penalties) on the world cup. This is in general <b>{average_goals_in_game}</b> goals per match.</p>"

    f'{img_all_wc}'

    f"<p>The fastest goal of the world cup was scored at {minute_fast_goal} minute by {player_fast_goal} (<b>{team_fast_goal}</b>) during the game with <b>{name_home_fast_goal}</b>. The final score of the match <b>{count_home_fast_goal}</b> — <b>{count_away_fast_goal}</b>.</p>"

    f"<p>All teams scores more goals and concedes more in the following intervals</p>"

    f"<table align='center' border='1'>"
            f'<tbody>'
            f"<tr align='center' valign='center'>"
                f"<td style= 'background-color: #e0d3d3;'><b>Minutes</b></td>"
                f"<td style= 'background-color: #b1e0b8;'><b>Scored, %</b></td>"
                f"<td style= 'background-color: #ebc996;'><b>Conceded, %</b></td>"
            f"</tr>"
                f"{all_table_goals}"
            f'</tbody>'
        f"</table>"

    f"<p><h3>Team efficiency:</h3></p>"

    f"<p><b>Destroyer of the world cup</b> — {top_detroyer_name_team}. The players of this team did <b>{top_destroyer_interseptions}</b> interceptions, <b>{top_destroyer_blocks}</b> blocks, <b>{top_destroyer_tackles}</b> tackles, and the goalkeeper made <b>{top_destroyer_saves}</b> saves. In total — <b>{top_detroyer_total_amount}</b> destroying actions.</p>"

    f"<p><b>Creator of the world cup</b> — {name_team_top_creator}. The players of this team won <b>{duels_top_creator}</b> duels, made <b>{shots_on_top_creator}</b> shots on target and <b>{shots_off_top_creator}</b> shots off target. In total — <b>{amount_top_creator}</b> actions.</p>"

    f"<p><b>The team with the best pass accuracy</b> — Belgium (95% of the total 981 passes). The worst team in terms of pass accuracy — Saudi Arabia (only 72% of the passes that are successful).</p>"
    
    f"<p><h3>Players’ stats:</h3></p>"

    f"<p>{top_saves_player_in_league_1} ({top_teams_saves[0]}) made more saves during the world cup — <b>{top_saves_amount_in_league_1}</b>.</p>"

    f"<p>As to fouls — the match with the most cards shown (<b>{top_fouls_total_yel_card}</b> yellow and <b>{top_fouls_total_red_card}</b> red) is the game between <b>{top_fouls_team_name_home}</b> and <b>{top_fouls_team_name_away}</b> (final score <b>{top_fouls_goals_home}</b> — <b>{top_fouls_goals_away}</b>).</p>"

    f"<h3><p>There is a top 3 of players with yellow and red cards this world cup:</p></h3>"
    
    f'<ul>'
        f"{top3_fouls_text_eng}"
    f'</ul>'

    f"<p>The best goalscorer for now is {name_max_goals_player} from {max_goals_player_his_team} (<b>{amount_max_goals_player}</b> goals).</p>"

    f"<h3><p>See the current topscorers list in the World Cup:</p></h3>"

    f'<ul>'
            f'<li> {top_player_in_league_1}, (<b>{top_amount_in_league_1}, {top_teams_goals[0]}</b>).</li>'
            f'<li> {top_player_in_league_2}, (<b>{top_amount_in_league_2}, {top_teams_goals[1]}</b>).</li>'
            f'<li> {top_player_in_league_3}, (<b>{top_amount_in_league_3}, {top_teams_goals[2]}</b>).</li>'
            f'<li> {top_player_in_league_4}, (<b>{top_amount_in_league_4}, {top_teams_goals[3]}</b>).</li>'
            f'<li> {top_player_in_league_5}, (<b>{top_amount_in_league_5}, {top_teams_goals[4]}</b>).</li>'
    f'</ul>'

    f"<p>Now the leader has <b>{top_amount_in_league_1}</b> goals. And let’s look how much did players score during in the previous World Cups:</p>"

        f"<table align='center' border='1'>"
        f"<tbody>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>Year</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>Goals</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Player</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Team</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2018</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>5</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Harry Kane</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>England</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2014</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>6</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>James Rodriguez</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Colombia</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2010</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>6</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Thomas Muller</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Germany</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2006</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>5</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Miroslav Klose</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Germany</b></td>"
        f"</tr>"
        f"<tr align='center' valign='center'>"
            f"<td style= 'background-color: #e0d3d3;'><b>2002</b></td>"
            f"<td style= 'background-color: #b1e0b8;'><b>8</b></td>"
            f"<td style= 'background-color: #ebc996;'><b>Ronaldo</b></td>"
            f"<td style= 'background-color: #e8eb96;'><b>Brazil</b></td>"
        f"</tr>"
        f"</tbody>"
    f"</table>"

   

    f"<h3><p>In terms of assists — here is top 5 players:</p></h3>"

     f'<ul>'
        f'<li> {top_assists_player_in_league_1}, (<b>{top_assists_amount_in_league_1}, {top_teams_assists[0]}</b>).</li>'
        f'<li> {top_assists_player_in_league_2}, (<b>{top_assists_amount_in_league_2}, {top_teams_assists[1]}</b>).</li>'
        f'<li> {top_assists_player_in_league_3}, (<b>{top_assists_amount_in_league_3}, {top_teams_assists[2]}</b>).</li>'
        f'<li> {top_assists_player_in_league_4}, (<b>{top_assists_amount_in_league_4}, {top_teams_assists[3]}</b>).</li>'
        f'<li> {top_assists_player_in_league_5}, (<b>{top_assists_amount_in_league_5}, {top_teams_assists[4]}</b>).</li>'
    f'</ul>'

    f"<h3><p>The best goalkeepers:</p></h3>"
    f'<ul>'
        f'<li> {top_saves_player_in_league_1}, (<b>{top_saves_amount_in_league_1}, {top_teams_saves[0]}</b>).</li>'
        f'<li> {top_saves_player_in_league_2}, (<b>{top_saves_amount_in_league_2}, {top_teams_saves[1]}</b>).</li>'
        f'<li> {top_saves_player_in_league_3}, (<b>{top_saves_amount_in_league_3}, {top_teams_saves[2]}</b>).</li>'
        f'<li> {top_saves_player_in_league_4}, (<b>{top_saves_amount_in_league_4}, {top_teams_saves[3]}</b>).</li>'
        f'<li> {top_saves_player_in_league_5}, (<b>{top_saves_amount_in_league_5}, {top_teams_saves[4]}</b>).</li>'
    f'</ul>'

    )


language_version = ['eng', 'ru']
for language in range(len(language_version)):
    with open(
            f'/opt/footballBot/parameters/football/users/parameters/{language + 1}.json'
    ) as file:
        data_j = json.load(file)
    font_for_date = ImageFont.truetype('/opt/footballBot/tools/fonts/days2.ttf', size=175)
    league_logo = Image.open('/opt/footballBot/tools/img/logo_WC.png')
    background = Image.open('/opt/footballBot/tools/img/world_cup1.png')
    group_eng = 'The most interesting statistics'
    group_eng2 = 'of the World Cup'
    group_ru = 'Самая интересная статистика'
    group_ru2 = 'Чемпионата мира'

    if language == 0:
        group1 = ImageDraw.Draw(background)
        # group1.line(((1780, 600), (1780, 300)), "red") #якорь
        # group1.line(((1500, 950), (2000, 950)), "red")
        # group1.text((1750, 300), x.strftime('%A %B %d %Y'), anchor='ms', font=font_for_date, fill='black') # Полностью
        group1.text((1780, 950), group_eng, anchor='ms', font=font_for_date, fill='white')
        group1.text((1780, 1150), group_eng2, anchor='ms', font=font_for_date, fill='white')
    elif language == 1:
        group1 = ImageDraw.Draw(background)
        # group1.line(((1780, 600), (1780, 300)), "red") #якорь
        # group1.line(((1500, 950), (2000, 950)), "red")
        # group1.text((1750, 300), x.strftime('%A %B %d %Y'), anchor='ms', font=font_for_date, fill='black') # Полностью
        group1.text((1780, 950), group_ru, anchor='ms', font=font_for_date, fill='white')
        group1.text((1780, 1150), group_ru2, anchor='ms', font=font_for_date, fill='white')

    new_size_logo_league = league_logo.resize((600, 600))
    background.paste(new_size_logo_league, (1480, 10), mask=new_size_logo_league.convert('RGBA'))
    new_image = background.resize((1778, 1000))
    new_image.save(f'/opt/footballBot/result/img_match/main_img_wc_{language_version[language]}.png')

    access_key = 'AKIA6MTJZAMUJMX2K77J'
    secret_access_key = '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'

    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)


    client.upload_file(f"/opt/footballBot/result/img_match/main_img_wc_{language_version[language]}.png","buckets-botbot-football", f"match/main_img_wc_{language_version[language]}.png", ExtraArgs={'ACL':'public-read'})

    sleep(5) #5 Секунд паузы, для того чтобы отправилось
    os.remove(f'/opt/footballBot/result/img_match/main_img_wc_{language_version[language]}.png')

    main_img = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/main_img_wc_{language_version[language]}.png"



    platform_name = data_j['platform_name']
    text_all = ''
    title = ''
    if language == 0:
        title = title_eng
        text_all = text_eng
    elif language == 1:
        title = title_ru
        text_all = text_ru
    if platform_name == 'wordpress':

        url = data_j['platform_url']
        user = data_j['platform_user']
        password = data_j['platform_password']
        type_status = data_j['type_status']
        data_tags = data_j['list_id']

        credentials = user + ':' + password
        """
        Получение категории (Как правило Лиги)
        """
        category, tags = '', ''
        if league_name in data_j['list_id']:

            category = data_j['list_id'][league_name]['id']
            # получение id команд тега

            team1_tags, team2_tags = '', ''

            if team_name_home in data_j['list_id'][league_name]: team1_tags = data_j['list_id'][league_name][team_name_home]
            if team_name_away in data_j['list_id'][league_name]: team2_tags = data_j['list_id'][league_name][team_name_away]

            # Создания тега
            if team1_tags != "": tags = team1_tags
            if team2_tags != "": tags = team2_tags
            if team1_tags != "" and team2_tags != "": tags = [team1_tags, team2_tags]

        if data_j['category_id'] != "" \
                and category != "": category = [category, data_j['category_id']]
        elif category == "" \
                and data_j['category_id'] != "": category = data_j['category_id']


        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        post = {
            'title': title,
            'status': f'{type_status}',  # тип
            'content': text_all,
            'categories': category, # category ID
            'tags': tags,
            # 'date'   : f'{date}',   # время публикации --  {время матча - один день}
            'meta': {'_knawatfibu_url': main_img}
        }

        
        responce = requests.post(url, headers=header, json=post)
        #responce_json = responce.json()

        print(f"[INFO]  posted")