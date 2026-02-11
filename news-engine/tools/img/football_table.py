import requests
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
from Football_API import fixture, team_home, team_away
#API для таблицы

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

headers = {
        "X-RapidAPI-Key": "8058e21169msh996327e1648c9fep1065d1jsn25f60b5e3028",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params={
    "fixture":"828360"
})

data = response.json()


#Делаю таблицу
#Home

total_shots1 = data['response'][0]['statistics'][2]['value']
ball_possession1 = data['response'][0]['statistics'][9]['value']
passes_percent1 = data['response'][0]['statistics'][15]['value']
yellow_card1 = data['response'][0]['statistics'][10]['value']
if yellow_card1 is None:
    yellow_card1 = 0
red_card1 = data['response'][0]['statistics'][11]['value']
if red_card1 is None:
    red_card1 = 0
headerColor = '#bdbdbd'
rowEvenColor = 'black'
rowOddColor = 'white'
fig = go.Figure(data=[go.Table(
       columnwidth=[(len(team_home) + 10), 13, 15, 13, 15, 13],
    header=dict(
        values=['<b>Team</b>', '<b>Total Shots</b>', '<b>Ball Possession</b>', '<b>Passes %</b>', '<b>Yellow Cards</b>',
                '<b>Red Cards</b>'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'left'],
        font=dict(color='black', size=12)
    ),
    cells=dict(
        values=[
            [team_home],
            [total_shots1],
            [ball_possession1],
            [passes_percent1],
            [yellow_card1],
            [red_card1]],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor] * 5],
        align=['left', 'left'],
        font=dict(color='darkslategray', size=12)
    ))
])
fig.write_image('table1.png', width=1100, height=1300) #Меняю размер таблицы




#Away

total_shots2 = data['response'][1]['statistics'][2]['value']
ball_possession2 = data['response'][1]['statistics'][9]['value']
passes_percent2 = data['response'][1]['statistics'][15]['value']
yellow_card2 = data['response'][1]['statistics'][10]['value']
if yellow_card2 is None:
    yellow_card2 = 0
red_card2 = data['response'][1]['statistics'][11]['value']
if red_card2 is None:
    red_card2 = 0

headerColor = '#bdbdbd'
rowEvenColor = 'black'
rowOddColor = 'white'
fig = go.Figure(data=[go.Table(
    columnwidth=[13, 15, 13, 15, 13, (len(team_home) + 10)],
    header=dict(
        values=['<b>Red Cards</b>','<b>Yellow Cards</b>','<b>Passes %</b>','<b>Ball Possession</b>','<b>Total Shots</b>','<b>Team</b>'],
        line_color='darkslategray',
        fill_color=headerColor,

        align=['right','right'],
        font=dict(color='black', size=12)
    ),
    cells=dict(
        values=[
            [red_card2],[yellow_card2],[passes_percent2],[ball_possession2],[total_shots2],[team_home]],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
        align = ['right', 'right'],
        font = dict(color = 'darkslategray', size = 12)
    ))
])
fig.write_image('table2.png', width=1100, height=1300) #Меняю размер таблицы


#Обрезаю таблицы

table_home = Image.open('table1.png')
crop_home = table_home.crop((80, 100, 1021, 152))
crop_home.save('table_home.png')

table_away = Image.open('table2.png')
crop_away = table_away.crop((80, 100, 1021, 152))
crop_away.save('table_away.png')
