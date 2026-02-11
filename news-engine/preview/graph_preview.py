from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]

def start_preview_graph(fixture_match):
    from PIL import Image
    from plotly import graph_objects as go
    from plotly.subplots import make_subplots
    from db_preview import get_data
    
    insert_query = (
        f"SELECT * FROM match_preview WHERE fixture_match3={fixture_match}"
    )

    r = get_data(insert_query)

    r = r[0]
    
    # Создание переменных по индексам результата    
    fixture_match, name_home_preview, name_away_preview, date_match, venue, id_team_home_preview, id_team_away_preview,  league, season, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, fixture_match3, date_match2, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_games, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, league_name, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, round = r # r[0], r[1], r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[21],r[22],r[23],r[24],r[25],r[26],r[27],r[28],r[29],r[30],r[31],r[32],r[33],r[34],r[35],r[36],r[37],r[38],r[39],r[40],r[41],r[42],r[43],r[44],r[45],r[46],r[47],r[48],r[49],r[50],r[51],r[52],r[53],r[54],r[55],r[56],r[57],r[58],r[59],r[60],r[61],r[62],r[63],r[64],r[65],r[66],r[67],r[68],r[69],r[70],r[71],r[72],r[73],r[74],r[75],r[76],r[77],r[78],r[79],r[80],r[81],r[82],r[83],r[84],r[85],r[86],r[87],r[88],r[89],r[90],r[91],r[92],r[93],r[94],r[95],r[96],r[97],r[98],r[99],r[100],r[101],r[102],r[103],r[104],r[105],r[106],r[107],r[108],r[109],r[110],r[111],r[112],r[113],r[114],r[115],r[116],r[117],r[118]
    # Восстановление списков
    list_for_goal_away=list_for_goal_away.split()
    list_for_goal_home=list_for_goal_home.split()
    list_minute_for_goals_home=list_minute_for_goals_home.split()
    list_minute_for_goals_away=list_minute_for_goals_away.split()
    list_minute_missed_goals_away=list_minute_missed_goals_away.split()
    list_minute_missed_goals_home=list_minute_missed_goals_home.split()
    list_missed_goal_away=list_missed_goal_away.split()
    list_missed_goal_home=list_missed_goal_home.split()


    percent_for_home = []
    minute_home_for = []
    percent_missed_home = []
    minute_home_missed = []

    for home_for in range(len(list_minute_for_goals_home)):
        percent_for_home.append(float(list_for_goal_home[home_for].replace("%", "")))
        minute_home_for.append(list_minute_for_goals_home[home_for])


    for home_against in range(len(list_minute_missed_goals_home)):
        percent_missed_home.append(float(list_missed_goal_home[home_against].replace("%", "")))
        minute_home_missed.append(list_minute_missed_goals_home[home_against])



    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=minute_home_for, values=percent_for_home, name="HOME", textinfo='label+percent'),
                1, 1)
    fig.add_trace(go.Pie(labels=minute_home_missed, values=percent_missed_home, name="AWAY", textinfo='label+percent'),
                1, 2)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(font_size=33,

    annotations=[dict(text='Goals scored', x=0.17, y=0.5, font_size=35, showarrow=False),
                 dict(text='Goals conceded', x=0.84, y=0.5, font_size=35, showarrow=False)], showlegend=False)

    

    output_path = root_folder / 'result' / 'img_match' / f'graph_home_{fixture_match}_preview.png'
    fig.write_image(str(output_path), width=2100, height=1300)

    percent_for_away = []
    minute_away_for = []
    percent_missed_away = []
    minute_away_missed = []

    for away_for in range(len(list_minute_for_goals_away)):
        percent_for_away.append(float(list_for_goal_away[away_for].replace("%", "")))
        minute_away_for.append(list_minute_for_goals_away[away_for])


    for away_against in range(len(list_minute_missed_goals_away)):
        percent_missed_away.append(float(list_missed_goal_away[away_against].replace("%", "")))
        minute_away_missed.append(list_minute_missed_goals_away[away_against])


    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=minute_away_for, values=percent_for_away, name="HOME", textinfo='label+percent'),
                1, 1)
    fig.add_trace(go.Pie(labels=minute_away_missed, values=percent_missed_away, name="AWAY", textinfo='label+percent'),
                1, 2)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(font_size=33,

    annotations=[dict(text='Goals scored', x=0.17, y=0.5, font_size=35, showarrow=False),
                 dict(text='Goals conceded', x=0.84, y=0.5, font_size=35, showarrow=False)], showlegend=False)

    

    output_path = root_folder / 'result' / 'img_match' / f'graph_away_{fixture_match}_preview.png'
    fig.write_image(str(output_path), width=2100, height=1300)

    

# start_preview_graph('867947')