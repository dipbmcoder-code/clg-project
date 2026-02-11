import os
from dotenv import load_dotenv
load_dotenv()

def start_review_graph(fixture_match):
    '''Создаем график'''
    from db import get_data
    from PIL import Image, ImageDraw, ImageFont
    import plotly.graph_objects as go
    from urllib.request import urlopen
    import requests
    import os
    from time import sleep
    #from Football_API import team_away, team_home, logo_away, logo_home, fixture
    #from football_table import data

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_graph = requests.get(url, headers=headers, params={
        'id':f'{fixture_match}'
    })
    data = req_graph.json()

    logo_home = data['response'][0]['teams']['home']['logo']
    logo_away = data['response'][0]['teams']['away']['logo']

    insert_query = (
        f"SELECT fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time FROM match_review WHERE fixture_match_for_check={fixture_match}"
    )

    index = get_data(insert_query)
    index = index[0]
    fixture_match, name_home_review, name_away_review, lineups_home, lineups_away, gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round_main, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time = index

    #Делаю таблицу
    #Home

    total_shots1 = data['response'][0]['statistics'][0]['statistics'][2]['value']
    ball_possession1 = data['response'][0]['statistics'][0]['statistics'][9]['value']
    passes_percent1 = data['response'][0]['statistics'][0]['statistics'][15]['value']
    yellow_card1 = data['response'][0]['statistics'][0]['statistics'][10]['value']
    if yellow_card1 is None:
        yellow_card1 = 0
    red_card1 = data['response'][0]['statistics'][0]['statistics'][11]['value']
    if red_card1 is None:
        red_card1 = 0

    headerColor = '#bdbdbd'
    rowEvenColor = 'black'
    rowOddColor = 'white'
    fig = go.Figure(data=[go.Table(
        columnwidth=[(len(name_home_review) + 10), 13, 15, 13, 15, 13],
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
                [name_home_review],
                [total_shots1],
                [ball_possession1],
                [passes_percent1],
                [yellow_card1],
                [red_card1]
            ],
            line_color='darkslategray',
            # 2-D list of colors for alternating rows
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor] * 5],
            align=['left', 'left'],
            font=dict(color='darkslategray', size=12)
        ))
    ])
    fig.write_image(f'/opt/footballBot/result/img_match/table_{fixture_match}_home.png', width=1100, height=1300) #Меняю размер таблицы




    #Away
    total_shots2 = data['response'][0]['statistics'][1]['statistics'][2]['value']
    ball_possession2 = data['response'][0]['statistics'][1]['statistics'][9]['value']
    passes_percent2 = data['response'][0]['statistics'][1]['statistics'][15]['value']
    yellow_card2 = data['response'][0]['statistics'][1]['statistics'][10]['value']
    if yellow_card2 is None:
        yellow_card2 = 0
    red_card2 = data['response'][0]['statistics'][1]['statistics'][11]['value']
    if red_card2 is None:
        red_card2 = 0

    headerColor = '#bdbdbd'
    rowEvenColor = 'black'
    rowOddColor = 'white'
    fig = go.Figure(data=[go.Table(
        columnwidth=[13, 15, 13, 15, 13, (len(name_away_review) + 10)],
        header=dict(
            values=['<b>Red Cards</b>','<b>Yellow Cards</b>','<b>Passes %</b>','<b>Ball Possession</b>','<b>Total Shots</b>','<b>Team</b>'],
            line_color='darkslategray',
            fill_color=headerColor,

            align=['right','right'],
            font=dict(color='black', size=12)
        ),
        cells=dict(
            values=[
                [red_card2],[yellow_card2],[passes_percent2],[ball_possession2],[total_shots2],[name_away_review]],
            line_color='darkslategray',
            # 2-D list of colors for alternating rows
            fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
            align = ['right', 'right'],
            font = dict(color = 'darkslategray', size = 12)
        ))
    ])
    fig.write_image(f'/opt/footballBot/result/img_match/table_{fixture_match}_away.png', width=1100, height=1300) #Меняю размер таблицы


    #Обрезаю таблицы

    table_home = Image.open(f'/opt/footballBot/result/img_match/table_{fixture_match}_home.png')
    crop_home = table_home.crop((80, 100, 1021, 152))
    crop_home.save(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_home.png')

    table_away = Image.open(f'/opt/footballBot/result/img_match/table_{fixture_match}_away.png')
    crop_away = table_away.crop((80, 100, 1021, 152))
    crop_away.save(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_away.png')

    #GRAPH
    #Ищу в команде №1 значения показателей
    shots_on_goal1 = data['response'][0]['statistics'][0]['statistics'][0]['value']
    if shots_on_goal1 is None:
        shots_on_goal1 = 0
    blocked_shot1 = data['response'][0]['statistics'][0]['statistics'][3]['value']
    if blocked_shot1 is None:
        blocked_shot1 = 0
    insidebox1 = data['response'][0]['statistics'][0]['statistics'][4]['value']
    if insidebox1 is None:
        insidebox1 = 0
    gol_saves1 = data['response'][0]['statistics'][0]['statistics'][12]['value']
    if gol_saves1 is None:
        gol_saves1 = 0
    outsidebox1 = data['response'][0]['statistics'][0]['statistics'][5]['value']
    if outsidebox1 is None:
        outsidebox1 = 0
    # print(shots_on_goal1, blocked_shot1, fouls1, offsides1, corner_kicks1)


    #Ищу в команде №2значения показателей
    shots_on_goal2 = data['response'][0]['statistics'][1]['statistics'][0]['value']
    if shots_on_goal2 is None:
        shots_on_goal2 = 0
    blocked_shot2 = data['response'][0]['statistics'][1]['statistics'][3]['value']
    if blocked_shot2 is None:
        blocked_shot2 = 0
    insidebox2 = data['response'][0]['statistics'][1]['statistics'][4]['value']
    if insidebox2 is None:
        insidebox2 = 0
    gol_saves2 = data['response'][0]['statistics'][1]['statistics'][12]['value']
    if gol_saves2 is None:
        gol_saves2 = 0
    outsidebox2 = data['response'][0]['statistics'][1]['statistics'][5]['value']
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
        dict(source=Image.open('/opt/footballBot/tools/img/small_gradient2.png'),
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

    fig.write_image(f'/opt/footballBot/result/img_match/plotly_scores_{fixture_match}.png', width=2100, height=1300) #Меняю размер паутины
    image_plotly = Image.open(f'/opt/footballBot/result/img_match/plotly_scores_{fixture_match}.png')
    # image_plotly.resize((3000, 3000))
    back = Image.open('/opt/footballBot/tools/img/gradient2.png')
    back.paste(image_plotly, (700, 300))

    #Вставляю лого и названия команд
    logo_team1 = Image.open(urlopen(logo_home))
    logo_team2 = Image.open(urlopen(logo_away))
    font_for_name = ImageFont.truetype('/opt/footballBot/tools/fonts/Roboto-Black.ttf', size=85)
    new_size_logo1 = logo_team1.resize((500, 500))
    new_size_logo2 = logo_team2.resize((500, 500))

    back.paste(new_size_logo1, (300, 600), mask=new_size_logo1.convert('RGBA'))
    back.paste(new_size_logo2, (2750, 600), mask=new_size_logo2.convert('RGBA'))

    name_team = ImageDraw.Draw(back)
    # name_team.line(((550, 500), (550, 100)), "red") #якорь, метка откуда начинается текст
    # name_team.line(((150, 200), (650, 200)), "red")
    if len(name_home_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
        mylist_home = []
        mylist_home_2 = []
        for i in name_home_review.split():
            if i == name_home_review.split()[0] or i == name_home_review.split()[1]:
                mylist_home.append(i)
            elif i == name_home_review.split()[2] or i == name_home_review.split()[3]:
                mylist_home_2.append(i)
        name_team.text((550, 200), ' '.join(mylist_home), anchor="ms", font=font_for_name, fill='white')
        name_team.text((550, 270), ' '.join(mylist_home_2), anchor="ms", font=font_for_name, fill='white')
    else:
        name_team.text((550, 200), name_home_review, anchor="ms", font=font_for_name, fill='white')


    # name_team.line(((3000, 500), (3000, 100)), "red") #якорь, метка откуда начинается текст
    # name_team.line(((2900, 200), (3400, 200)), "red")
    if len(name_away_review) >= 18: #Если название команды больше 2 слов, то переношу последний элемент на новую строчку
        mylist_away = []
        mylist_away_2 = []
        for i in name_away_review.split():
            if i == name_away_review.split()[0] or i == name_away_review.split()[1]:
                mylist_away.append(i)
            elif i == name_away_review.split()[2] or i == name_away_review.split()[3]:
                mylist_away_2.append(i)
        name_team.text((3000, 200), ' '.join(mylist_away), anchor="ms", font=font_for_name, fill='white')
        name_team.text((3000, 270), ' '.join(mylist_away_2), anchor="ms", font=font_for_name, fill='white')
    else:
        name_team.text((3000, 200), name_away_review, anchor="ms", font=font_for_name, fill='white')
    #Добавляю таблицу


    table_home = Image.open(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_home.png')
    new_table1 = table_home.resize((1750, 120))
    back.paste(new_table1, (10, 1800))

    table_away = Image.open(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_away.png')
    new_table2 = table_away.resize((1750, 120))
    back.paste(new_table2, (1800, 1800))
    # width, height = back.size
    # print(width, height)
    new_image = back.resize((1200, 750))
    new_image.save(f'/opt/footballBot/result/img_match/{fixture_match}_graph_review.png')



    sleep(10) #10 Секунды паузы, для того чтобы сохранилось и нанеслось на картинку с диаграммой
    os.remove(f'/opt/footballBot/result/img_match/table_{fixture_match}_home.png')
    os.remove(f'/opt/footballBot/result/img_match/table_{fixture_match}_away.png')
    os.remove(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_home.png')
    os.remove(f'/opt/footballBot/result/img_match/table_ready_{fixture_match}_away.png')
    os.remove(f'/opt/footballBot/result/img_match/plotly_scores_{fixture_match}.png')

    #print('test')
#start_review_graph('868033')