from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import requests
from urllib.request import urlopen
from Football_API import team_away, team_home, logo_away, logo_home, fixture
from football_table import data


#Ищу в команде №1 значения показателей
shots_on_goal1 = data['response'][0]['statistics'][0]['value']
if shots_on_goal1 is None:
    shots_on_goal1 = 0
blocked_shot1 = data['response'][0]['statistics'][3]['value']
if blocked_shot1 is None:
    blocked_shot1 = 0
insidebox1 = data['response'][0]['statistics'][4]['value']
if insidebox1 is None:
    insidebox1 = 0
gol_saves1 = data['response'][0]['statistics'][12]['value']
if gol_saves1 is None:
    gol_saves1 = 0
outsidebox1 = data['response'][0]['statistics'][5]['value']
if outsidebox1 is None:
    outsidebox1 = 0
# print(shots_on_goal1, blocked_shot1, fouls1, offsides1, corner_kicks1)


#Ищу в команде №2значения показателей
shots_on_goal2 = data['response'][1]['statistics'][0]['value']
if shots_on_goal2 is None:
    shots_on_goal2 = 0
blocked_shot2 = data['response'][1]['statistics'][3]['value']
if blocked_shot2 is None:
    blocked_shot2 = 0
insidebox2 = data['response'][1]['statistics'][4]['value']
if insidebox2 is None:
    insidebox2 = 0
gol_saves2 = data['response'][1]['statistics'][12]['value']
if gol_saves2 is None:
    gol_saves2 = 0
outsidebox2 = data['response'][1]['statistics'][5]['value']
if outsidebox2 is None:
    outsidebox2 = 0
# print(shots_on_goal2, blocked_shot2, fouls2, offsides2, corner_kicks2)


# Включаю библиотеку PIL и plotly для графика

categories = ['Shots on Goal', 'Blocked Shots', 'Goalkeeper Saves', 'Shots insidebox', 'Shots outsidebox']
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[shots_on_goal1, blocked_shot1, gol_saves1, insidebox1, outsidebox1],
    theta=categories,
    fillcolor='rgba(26,150,65,0.4)',                          #Меняет цвет и прозрачность линии
    line=dict(color='green', width=2),                        #Меняет цвет линий и shape='spline'
    fill='toself',                                            #закрашивает внутри диаграммы
    name='team_home'
))
fig.add_trace(go.Scatterpolar(
    r=[shots_on_goal2, blocked_shot2, gol_saves2, insidebox2, outsidebox1],
    theta=categories,
    fillcolor='rgba(255, 0, 1, 0.4)',                         #Меняет цвет и прозрачность линии
    line=dict(color='red', width=2),                          #Меняет цвет линий
    fill='toself',
    name='team_away'
))

fig.update_layout(                                            #Параметры снаружи круга
    # title='Тест1',                                          #В правом углу добавляю текст
    polar=dict(
        angularaxis=dict(
            color='white',
            gridcolor='black',                                #Цвет цифр
            # linecolor='black',                              #Меняет цвет радиуса
            tickfont=dict(size=40))))                         #Меняю размер списка categories

fig.update_layout(                                            #Параметры внутри круга
    polar=dict(
        radialaxis=dict(
            visible=True,                                     #Убирает цифры в паутине
            color='black',                                    #Цвет категорий
            gridcolor='black', #linecolor='black',
            tickfont=dict(size=20))),                         #Изменяет размер цифр в паутине
            #range=[0, 20])),                                 #Шаги внутренних кругов
    showlegend=False                                          #В углу команды и цвет на графике
)

fig.add_layout_image(                                         #Вставляю свою картинку в фон диаграммы
    dict(source=Image.open('small gradient2.png'),
         xref="paper",
         yref="paper",
         x=0.5,
         y=0.5,
         sizex=1.180,
         sizey=1.180,
         sizing="contain",
         xanchor="center",
         yanchor="middle",
         layer="below"))

fig.write_image('plotly_scores.png', width=2100, height=1300) #Меняю размер паутины
image_plotly = Image.open('plotly_scores.png')
# image_plotly.resize((3000, 3000))
back = Image.open('gradient2.png')
back.paste(image_plotly, (700, 300))

#Вставляю лого и названия команд
logo_team1 = Image.open(urlopen(logo_home))
logo_team2 = Image.open(urlopen(logo_away))
font_for_name = ImageFont.truetype('Roboto-Black.ttf', size=85)
new_size_logo1 = logo_team1.resize((500, 500))
new_size_logo2 = logo_team2.resize((500, 500))

back.paste(new_size_logo1, (300, 600), mask=new_size_logo1.convert('RGBA'))
back.paste(new_size_logo2, (2750, 600), mask=new_size_logo2.convert('RGBA'))

name_team = ImageDraw.Draw(back)
# name_team.line(((550, 500), (550, 100)), "red") #якорь, метка откуда начинается текст
# name_team.line(((150, 200), (650, 200)), "red")
if len(team_home) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
    mylist_home = []
    mylist_home_2 = []
    for i in team_home.split():
        if i == team_home.split()[0] or i == team_home.split()[1]:
            mylist_home.append(i)
        elif i == team_home.split()[2] or i == team_home.split()[3]:
            mylist_home_2.append(i)
    name_team.text((550, 200), ' '.join(mylist_home), anchor="ms", font=font_for_name, fill='white')
    name_team.text((550, 270), ' '.join(mylist_home_2), anchor="ms", font=font_for_name, fill='white')
else:
    name_team.text((550, 200), team_home, anchor="ms", font=font_for_name, fill='white')


# name_team.line(((3000, 500), (3000, 100)), "red") #якорь, метка откуда начинается текст
# name_team.line(((2900, 200), (3400, 200)), "red")
if len(team_away) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
    mylist_away = []
    mylist_away_2 = []
    for i in team_away.split():
        if i == team_away.split()[0] or i == team_away.split()[1]:
            mylist_away.append(i)
        elif i == team_away.split()[2] or i == team_away.split()[3]:
            mylist_away_2.append(i)
    name_team.text((3000, 200), ' '.join(mylist_away), anchor="ms", font=font_for_name, fill='white')
    name_team.text((3000, 270), ' '.join(mylist_away_2), anchor="ms", font=font_for_name, fill='white')
else:
    name_team.text((3000, 200), team_away, anchor="ms", font=font_for_name, fill='white')
#Добавляю таблицу


table_home = Image.open('table_home.png')
new_table1 = table_home.resize((1750, 120))
back.paste(new_table1, (10, 1800))

table_away = Image.open('table_away.png')
new_table2 = table_away.resize((1750, 120))
back.paste(new_table2, (1800, 1800))


back.save('graph_football_scores.png')
back.show()

