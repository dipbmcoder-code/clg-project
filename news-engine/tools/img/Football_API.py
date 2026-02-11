import requests

#Запрос к апи лайв игры
url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'
headers = {
    "X-RapidAPI-Key": "8058e21169msh996327e1648c9fep1065d1jsn25f60b5e3028",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params={
    'live':'all'

})
data = response.json()

#Вывод данных

num = 0
date_match = data['response'][num]['fixture']['date'][0:10]
fixture = data['response'][num]['fixture']['id']
league = data['response'][num]['league']['name']
venue = data['response'][num]['fixture']['venue']['name']
city = data['response'][num]['fixture']['venue']['city']

team_home = data['response'][num]['teams']['home']['name']
team_away = data['response'][num]['teams']['away']['name']
logo_home = data['response'][num]['teams']['home']['logo']
logo_away = data['response'][num]['teams']['away']['logo']


goals_home = str(data['response'][num]['goals']['home'])
goals_away = str(data['response'][num]['goals']['away'])

#Имена тех, кто забил и на какой минуте

events_index = len(data['response'][num]['events'])
#Ищу голы

time_home_goal = []
player_home_goal = []
time_away_goal = []
player_away_goal = []

#Ищу карточки за нарушения
time_home_yellow = []
player_home_yellow = []
time_away_yellow = []
player_away_yellow = []

time_home_red = []
player_home_red = []
time_away_red = []
player_away_red = []
index = 0
if events_index >= 1:
    while index != events_index:
        events = data['response'][num]['events'][index]['type']
        if events == 'Goal' and data['response'][num]['events'][index]['team']['name'] == team_home:
            time_home_goal.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_home_goal.append(str(data['response'][num]['events'][index]['player']['name']))
        elif events == 'Goal' and data['response'][num]['events'][index]['team']['name'] == team_away:
            time_away_goal.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_away_goal.append(str(data['response'][num]['events'][index]['player']['name']))
        elif events == 'Card' and data['response'][num]['events'][index]['team']['name'] == team_home \
            and data['response'][num]['events'][index]['detail'] == 'Yellow Card':
            time_home_yellow.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_home_yellow.append(str(data['response'][num]['events'][index]['player']['name']))
        elif events == 'Card' and data['response'][num]['events'][index]['team']['name'] == team_away \
                and data['response'][num]['events'][index]['detail'] == 'Yellow Card':
            time_away_yellow.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_away_yellow.append(str(data['response'][num]['events'][index]['player']['name']))
        elif events == 'Card' and data['response'][num]['events'][index]['team']['name'] == team_home \
                and data['response'][num]['events'][index]['detail'] == 'Red Card':
            time_home_red.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_home_red.append(str(data['response'][num]['events'][index]['player']['name']))
        elif events == 'Card' and data['response'][num]['events'][index]['team']['name'] == team_away \
                and data['response'][num]['events'][index]['detail'] == 'Red Card':
            time_away_red.append(str(data['response'][num]['events'][index]['time']['elapsed']))
            player_away_red.append(str(data['response'][num]['events'][index]['player']['name']))
        index += 1




