from PIL import Image, ImageDraw, ImageFont
from Football_API import league, team_home, team_away, logo_away, logo_home, goals_away, goals_home, \
    index, events_index, time_away_goal, time_home_goal, player_away_goal, player_home_goal, date_match, venue
from urllib.request import urlopen # Сохраняет лого по ссылке и вставляет в код #Добавил эту библиотеку, дольше выводить стало

# Добавляю объекты
font_for_name = ImageFont.truetype('Kanit-Medium.ttf', size=70)
#font_for_league = ImageFont.truetype('BebasNeue-Regular.ttf', size=120)
font_for_league2 = ImageFont.truetype('Kanit-Medium.ttf', size=110)
font_for_points = ImageFont.truetype('Kanit-Medium.ttf', size=240)
font_for_arena = ImageFont.truetype('Kanit-Medium.ttf', size=55)
font_for_goal = ImageFont.truetype('Kanit-Medium.ttf', size=50)
font_for_date = ImageFont.truetype('Kanit-Medium.ttf', size=70)
background = Image.open('back_black.png')
logo_team1 = Image.open(urlopen(logo_home))
logo_team2 = Image.open(urlopen(logo_away))

# Статистика голов
goals_home1 = ImageDraw.Draw(background)
goals_home1.text((2150, 270), goals_home, font=font_for_points, fill='white')
dash = ImageDraw.Draw(background)
dash.text((2350, 270), '-', font=font_for_points, fill='white')
goals_away1 = ImageDraw.Draw(background)
goals_away1.text((2510, 270), goals_away, font=font_for_points, fill='white')

# Кто забил и на какой минуте
#HomeTeam
index_home = 0
coordinate_home = 820
if len(player_home_goal) >= 1:
    while index_home != len(player_home_goal):
        player_goal_home3 = ImageDraw.Draw(background)
        # player_goal_home3.line(((1720, 1100), (1720, 600)), "red") #якорь
        # player_goal_home3.line(((1500, 820), (2000, 820)), "red")
        player_goal_home3.text((1720, coordinate_home), f"({time_home_goal[index_home]}')  {player_home_goal[index_home]}", anchor='ms', font=font_for_goal, fill='white')
        coordinate_home += 70
        index_home += 1
#AwayTeam
index_away = 0
coordinate_away = 820
if len(player_away_goal) >= 1:
    while index_away != len(player_away_goal):
        player_goal_away3 = ImageDraw.Draw(background)
        # player_goal_away3.line(((3085, 1100), (3085, 600)), "red") #якорь
        # player_goal_away3.line(((2850, 820), (3350, 820)), "red")
        player_goal_away3.text((3085, coordinate_away), f"({time_away_goal[index_away]}')  {player_away_goal[index_away]}", anchor='ms',  font=font_for_goal, fill='white')
        coordinate_away += 70
        index_away += 1


# Лига и названия команд
name_team = ImageDraw.Draw(background)
if len(team_home) >= 18: #Если название команды больше 18 букв, то переношу последний элемент на новую строчку
    mylist_home = []
    mylist_home_2 = []
    for i in team_home.split():  #bar foo bars
        if i == team_home.split()[0] or i == team_home.split()[1]:
            mylist_home.append(i)
        elif i == team_home.split()[2] or i == team_home.split()[3]:
            mylist_home_2.append(i)
    # name_team.line(((1720, 900), (1720, 600)), "red") #якорь
    # name_team.line(((1500, 650), (2000, 650)), "red")
    name_team.text((1720, 650), ' '.join(mylist_home), anchor='ms', font=font_for_name, fill='white')
    name_team.text((1720, 720), ' '.join(mylist_home_2), anchor='ms', font=font_for_name, fill='white')
else:
    name_team.text((1720, 650), team_home, anchor='ms', font=font_for_name, fill='white')


if len(team_away) >= 18: #Если название команды больше 18 букв, то переношу последний элемент на новую строчку
    mylist_away = []
    mylist_away_2 = []
    for i in team_away.split():
        if i == team_away.split()[0] or i == team_away.split()[1]:
            mylist_away.append(i)
        elif i == team_away.split()[2] or i == team_away.split()[3]:
            mylist_away_2.append(i)
    # name_team.line(((3085, 900), (3085, 600)), "red") #якорь
    # name_team.line(((2850, 650), (3350, 650)), "red")
    name_team.text((3085, 650), ' '.join(mylist_away), anchor='ms', font=font_for_name, fill='white')
    name_team.text((3085, 720), ' '.join(mylist_away_2), anchor='ms', font=font_for_name, fill='white')
else:
    name_team.text((3085, 650), team_away, anchor='ms', font=font_for_name, fill='white')


date = ImageDraw.Draw(background)
# date.line(((2400, 400), (2400, 100)), "red") #якорь
# date.line(((2200, 250), (2700, 250)), "red")
date.text((2400, 250), date_match, anchor='ms', font=font_for_date, fill='white')

league0 = ImageDraw.Draw(background)
# league0.line(((2400, 1500), (2400, 1100)), "red") #якорь
# league0.line(((2150, 1300), (2650, 1300)), "red")
league0.text((2400, 1300), league, anchor='ms', font=font_for_league2, fill='#cbf705')

arena = ImageDraw.Draw(background)
# arena.line(((2400, 1630), (2400, 1230)), "red") #якорь
# arena.line(((2150, 1430), (2650, 1430)), "red")
arena.text((2400, 1430), f'Arena: {venue}', anchor="ms", font=font_for_arena, fill='white')


# Меняю размер logo
new_size_logo1 = logo_team1.resize((350, 350))
new_size_logo2 = logo_team2.resize((350, 350))

# Делаю из лого эллипсисы (обрезаю черный фон)
# mask_logo1 = Image.new('L', new_size_logo1.size, 0)
# draw = ImageDraw.Draw(mask_logo1)
# draw.ellipse((1, 1, 350, 350), fill=255)
#
# mask_logo2 = Image.new('L', new_size_logo2.size, 0)
# draw = ImageDraw.Draw(mask_logo2)
# draw.ellipse((1, 1, 350, 350), fill=255)



#Вывод
background.paste(new_size_logo1, (1550, 175),  mask=new_size_logo1.convert('RGBA'))
background.paste(new_size_logo2, (2900, 175),  mask=new_size_logo2.convert('RGBA'))
background.save('black_done.png')
background.show()

