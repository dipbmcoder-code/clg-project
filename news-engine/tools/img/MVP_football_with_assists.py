#Подсчитываем мвп игрока и выписываем его
#Создаем API под мвп игрока
import requests
from Football_API import fixture

#Example

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"  #V3 - Fixtures

headers = {
    "X-RapidAPI-Key": "8058e21169msh996327e1648c9fep1065d1jsn25f60b5e3028",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params={
        'id':'854578'
})
data = response.json()


# Ищем команды #Example
team_home = 'Spain'
team_away = 'Portugal'

#Ищем лучшего игрока в team_home
list_for_goals_home = []
list_for_goals_home_name_player = []
list_for_assists_home = []

goals_team_home = 0
assists_team_home = 0
best_player_goals_home = ''
index_mvp_home = 0

#Создаю списки с параметрами по голам и ассистам, потому что апи вытаскивает значение none вместо 0
for find_mvp_player_home in range(len(data['response'][0]['players'][0]['players'])):
    list_for_goals_home.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['statistics'][0]['goals']['total'])
    list_for_goals_home_name_player.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['player']['name'])
    if list_for_goals_home[find_mvp_player_home] == None:
        del list_for_goals_home[find_mvp_player_home]
        list_for_goals_home.insert(find_mvp_player_home, 0)
    list_for_assists_home.append(data['response'][0]['players'][0]['players'][find_mvp_player_home]['statistics'][0]['goals']['assists'])
    if list_for_assists_home[find_mvp_player_home] == None:
        del list_for_assists_home[find_mvp_player_home]
        list_for_assists_home.insert(find_mvp_player_home, 0)

#Прохожусь по спискам и ищу лучшего игрока
while index_mvp_home != len(list_for_goals_home):
    if list_for_goals_home[index_mvp_home] >= goals_team_home and list_for_assists_home[index_mvp_home] >= assists_team_home:
        best_player_goals_home = list_for_goals_home_name_player[index_mvp_home]
        goals_team_home = list_for_goals_home[index_mvp_home]
        assists_team_home = list_for_assists_home[index_mvp_home]
    index_mvp_home += 1



#Ищем лучшего игрока в team_away
list_for_goals_away = []
list_for_goals_away_name_player = []
list_for_assists_away = []

goals_team_away = 0
assists_team_away = 0
best_player_goals_away = ''
index_mvp_away = 0

#Создаю списки с параметрами по голам и ассистам, потому что апи вытаскивает значение none вместо 0
for find_mvp_player_away in range(len(data['response'][0]['players'][1]['players'])):
    list_for_goals_away.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['statistics'][0]['goals']['total'])
    list_for_goals_away_name_player.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['player']['name'])
    if list_for_goals_away[find_mvp_player_away] == None:
        del list_for_goals_away[find_mvp_player_away]
        list_for_goals_away.insert(find_mvp_player_away, 0)
    list_for_assists_away.append(data['response'][0]['players'][1]['players'][find_mvp_player_away]['statistics'][0]['goals']['assists'])
    if list_for_assists_away[find_mvp_player_away] == None:
        del list_for_assists_away[find_mvp_player_away]
        list_for_assists_away.insert(find_mvp_player_away, 0)

#Прохожусь по спискам и ищу лучшего игрока
while index_mvp_away != len(list_for_goals_away):
    if list_for_goals_away[index_mvp_away] >= goals_team_away and list_for_assists_away[index_mvp_away] >= assists_team_away:
        best_player_goals_away = list_for_goals_away_name_player[index_mvp_away]
        goals_team_away = list_for_goals_away[index_mvp_away]
        assists_team_away = list_for_assists_away[index_mvp_away]
    index_mvp_away += 1


mvp_player = ''

if goals_team_home >= goals_team_away and assists_team_home >= assists_team_away:
    mvp_player = best_player_goals_home
elif goals_team_home > goals_team_away and assists_team_home >= assists_team_away:
    mvp_player = best_player_goals_home
elif goals_team_home < goals_team_away and assists_team_home <= assists_team_away:
    mvp_player = best_player_goals_away
elif goals_team_home >= goals_team_away and assists_team_home > assists_team_away:
    mvp_player = best_player_goals_home
elif goals_team_home <= goals_team_away and assists_team_home < assists_team_away:
    mvp_player = best_player_goals_away
elif goals_team_home > goals_team_away:
    mvp_player = best_player_goals_home
elif goals_team_home < goals_team_away:
    mvp_player = best_player_goals_away
elif assists_team_home > assists_team_away or assists_team_home >= assists_team_away:
    mvp_player = best_player_goals_home
elif assists_team_home < assists_team_away:
    mvp_player = best_player_goals_away



