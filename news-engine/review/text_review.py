import json
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]


def start_review_text(fixture_match):

    '''Берем с бд данные и засовываем в текст для тг бота'''

    from review.db import get_data
    #Запрос в бд
    insert_query = (
        f"SELECT fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves,  id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time FROM match_review WHERE fixture_match_for_check={fixture_match}"
    )

    index = get_data(insert_query)
    # print(index[0])
    index = index[0]
    #fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name = index[0],index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],index[14],index[15],index[16],index[17],index[18],index[19],index[20],index[21],index[22],index[23],index[24],index[25],index[26],index[27],index[28],index[29],index[30],index[31],index[32],index[33],index[34],index[35],index[36],index[37],index[38],index[39],index[40],index[41],index[42],index[43],index[44],index[45],index[46],index[47],index[48],index[49],index[50],index[51],index[52],index[53],index[54],index[55],index[56],index[57],index[58],index[59],index[60],index[61],index[62],index[63],index[64],index[65],index[66],index[67],index[68],index[69],index[70],index[71],index[72],     index[92],index[93],index[94],index[95],index[96],index[97],index[98],index[99],index[100],index[101],index[102],index[103],index[104],index[105],index[106],index[107],index[108],index[109],index[110],index[111],index[112],index[113],index[114]
    fixture_match, name_home_review, name_away_review, lineups_home, lineups_away, gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, id_team_home_review, id_team_away_review, league, venue, date_match3, player_home_penalti, time_home_penalti, player_away_penalti, time_away_penalti, form_home, form_away, topscorer_name_in_league_4, topscorer_amount_in_league_4, topscorer_team_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_5, topscorer_team_in_league_5, rank_for_table, name_table_team, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, logo_for_table, league_name, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, name_home_top_pass_accuracy, top__home_precent_accuracy, top__home_total_passes, name_away_top_pass_accuracy, top__away_precent_accuracy, top__away_total_passes, name_home_top_pass_key, top__home_amount_key, name_away_top_pass_key, top__away_amount_key, round_main, team_home_passes_accurate, team_away_passes_accurate, team_home_percent_passes_accurate, team_away_percent_passes_accurate, team_home_total_passes, team_away_total_passes, injuries_count, total_cards_in_game, count_yel_card, count_red_card, match_lasted, referee_time = index

    time_home_goal = time_home_goal.split()
    time_away_goal = time_away_goal.split()
    lineups_home = str(lineups_home).replace("+", "</li><li>").split()
    lineups_away = str(lineups_away).replace("+", "</li><li>").split()
    lineups_home="<ul><li>" + ''.join(lineups_home) + "</li></ul>"
    lineups_away="<ul><li>" + ''.join(lineups_away) + "</li></ul>"
    time_home_penalti = time_home_penalti.split()
    time_away_penalti = time_away_penalti.split()

    player_home_goal = str(player_home_goal).replace("+", " ")
    
    player_away_goal = str(player_away_goal).replace("+", " ")
    #player_away_goal = player_away_goal.replace("_", "")
    player_away_goal = player_away_goal.split()
    player_home_goal = player_home_goal.split()
    gone_player_home = str(gone_player_home).replace("+", " ").split()
    gone_player_away = str(gone_player_away).replace("+", " ").split()
    came_player_home = str(came_player_home).replace("+", " ").split()
    came_player_away = str(came_player_away).replace("+", " ").split()
    time_home_yellow = time_home_yellow.split()
    time_away_yellow = time_away_yellow.split()
    time_home_red = time_home_red.split()
    time_away_red = time_away_red.split()
    player_home_yellow = str(player_home_yellow).replace("+", " ").split()
    player_away_yellow = str(player_away_yellow).replace("+", " ").split()  #TODO заменить
    player_home_red = str(player_home_red).replace("+", " ").split()
    player_away_red = str(player_away_red).replace("+", " ").split()
    time_subst_home = time_subst_home.split()
    time_subst_away = time_subst_away.split()
    player_home_penalti = str(player_home_penalti).replace("+", " ")
    # player_home_penalti = player_home_penalti.replace("_", "").split()
    player_home_penalti = player_home_penalti.split()
    player_away_penalti = str(player_away_penalti).replace("+", " ")
    player_away_penalti = player_away_penalti.split()
    # player_away_penalti = player_away_penalti.replace("_", "").split()
    



    subs_home = '<ul>'
    subs_away = '<ul>'
    for sub_home in range(len(gone_player_home)):
        subs_home += f'<li>{gone_player_home[sub_home]} '
        if sub_home+1 <= len(came_player_home): subs_home += f"({came_player_home[sub_home]}, {time_subst_home[sub_home]})"
        subs_home += " </li>"

    for sub_away in range(len(gone_player_away)):
        subs_away += f'<li>{gone_player_away[sub_away]} '
        if sub_away+1 <= len(came_player_away): subs_away += f"({came_player_away[sub_away]}, {time_subst_away[sub_away]})"
        subs_away += " </li>"

    subs_home += "</ul>"
    subs_away += "</ul>"
    # print(rank_for_table)
    # print(points_for_table)

    total_shots_2_teams_on_target = int(total_shots_home) + int(total_shots_away) 
    total_shots_2_teams_on_goal = int(shots_on_goal_home) + int(shots_on_goal_away)
    # print(goals_for)

    data_review = [{
        "img_review":"path",
        "title":{
            "team_a":f"{name_home_review}",
            "team_b":f"{name_away_review}",
            "goal_a":f"{goals_home}",
            "goal_b":f"{goals_away}",
            "venue":f"{venue}",
            "date_match3":f"{date_match3}",
            "form_home":f"<b>{form_home}</b>",
            "form_away":f"<b>{form_away}</b>",
            "league_name":f"{league_name}"
        },
        "subtitle_lineups":{
            "title":f"Составы игравших команд",
            "lineups_a":f"{lineups_home.replace('_', ' ')}",
            "lineups_b":f"{lineups_away.replace('_', ' ')}",
            "lineups_in_game_a":f"{subs_home.replace('_', ' ')}",
            "lineups_in_game_b":f"{subs_away.replace('_', ' ')}"
        },
        "goals_scorers":{
            "goals":{
                "title":f"Авторы голов:",
                "total_shots_off":f"{total_shots_2_teams_on_target}",
                "total_shots_on":f"{total_shots_2_teams_on_goal}",
                "shots_team1_off":f"{total_shots_home}",
                "shots_team1_on":f"{shots_on_goal_home}",
                "active_shots_player_home":f"{name_home_top_shots}",
                "shots_team2_off":f"{total_shots_away}",
                "shots_team2_on":f"{shots_on_goal_away}",
                "active_shots_player_away":f"{name_away_top_shots}",
                "total_assists_home":f"{total_assists_home}",
                "total_assists_away":f"{total_assists_away}"
                },
            "defensive":{
                "title":f"Оборонительные действия:",
                "total_interceptions_home":f"{total_interceptions_home}",
                "name_top_inceptions_home":f"{name_home_top_interceptions}",
                "amount_interceptions_home":f"{amount_home_interceptions}",
                "total_inteceptions_away":f"{total_interceptions_away}",
                "name_top_inceptions_away":f"{name_away_top_interceptions}",
                "amount_interseptions_away":f"{amount_away_interceptions}",
                "total_blocks_home":f"{total_blocks_home}",
                "name_top_blocks_home":f"{name_home_top_block}",
                "amount_blocks_home":f"{amount_home_block}",
                "total_blocks_away":f"{total_blocks_away}",
                "name_top_blocks_away":f"{name_away_top_block}",
                "amount_blocks_away":f"{amount_away_block}"
                },
            "passes":{
                
                "name_home_top_pass_accuracy":f"{name_home_top_pass_accuracy}",
                "top__home_precent_accuracy":f"{top__home_precent_accuracy}",
                "top__home_total_passes":f"{top__home_total_passes}",
                "name_away_top_pass_accuracy":f"{name_away_top_pass_accuracy}",
                "top__away_precent_accuracy":f"{top__away_precent_accuracy}",
                "top__away_total_passes":f"{top__away_total_passes}", 
                "name_home_top_pass_key":f"{name_home_top_pass_key}",
                "top__home_amount_key":f"{top__home_amount_key}",
                "name_away_top_pass_key":f"{name_away_top_pass_key}",
                "top__away_amount_key":f"{top__away_amount_key}"
                
            },
            "duels":{
                "title":f"Единоборства:",
                "name_duels_team1":f"<b>{name_home_top_duels}</b>",
                "amount_duels_team1":f"{amount_home_duels}",
                "name_duels_team2":f"<b>{name_away_top_duels}</b>",
                "amount_duels_team2":f"{amount_away_duels}"
                },
            "ball_pos":{
                "title":f"Процент владения мячом: ",
                "possession_team1":f"<b>{ball_possession_home}</b>",
                "possession_team2":f"<b>{ball_possession_away}</b>"
                },
            "fouls":{
                "title":f"Наказания: ",
                }
            
        },
        "top_players_league":{
            "title":f"Пятерка лидеров в гонке бомбардиров чемпионата:",
            "top3":{
                "first_top_name":f"<b>{topscorer_name_in_league_1}</b>",
                "first_top_team":f"{topscorer_team_in_league_1}",
                "first_top_amount":f"<b>{topscorer_amount_in_league_1}</b>",
                "second_top_name":f"<b>{topscorer_name_in_league_2}</b>",
                "second_top_team":f"{topscorer_team_in_league_2}",
                "second_top_amount":f"<b>{topscorer_amount_in_league_2}</b>",
                "third_top_name":f"<b>{topscorer_name_in_league_3}</b>",
                "third_top_team":f"{topscorer_team_in_league_3}",
                "third_top_amount":f"<b>{topscorer_amount_in_league_3}</b>",
                "fourth_top_name":f"<b>{topscorer_name_in_league_4}</b>",
                "fourth_top_team":f"{topscorer_team_in_league_4}",
                "fourth_top_amount":f"<b>{topscorer_amount_in_league_4}</b>",
                "fifth_top_name":f"<b>{topscorer_name_in_league_5}</b>",
                "fifth_top_team":f"{topscorer_team_in_league_5}",
                "fifth_top_amount":f"<b>{topscorer_amount_in_league_5}</b>"
            }
        },
        "next_matches":{
            "title":f"Следующие матчи: ",
            "show_next_matches":{
                "next_match_team1_with":f"{home_next_match_rival}",
                "next_match_team1_date":f"{home_date_match_vs_rival}",
                "next_match_team1_venue":f"{home_next_venue_vs_rival}",
                "next_match_team2_with":f"{away_next_match_rival}",
                "next_match_team2_date":f"{away_date_match_vs_rival}",
                "next_match_team2_venue":f"{away_venue_vs_rival}"

            }
        }  
    }]

    result_folder = root_folder / "result" / "json"
    result_folder.mkdir(parents=True, exist_ok=True)
    with open(result_folder / f"{fixture_match}_review.json", "w", encoding="utf-8") as write_file:
        json.dump(data_review, write_file, indent=4, ensure_ascii=False)



    # text = (
    #     f"{name_home_review} — {name_away_review} {goals_home} : {goals_away} \n",
    #     f"Составы игравших команд: \n",
    #     f"{name_home_review}: {' '.join(lineups_home)} \n",
    #     f"{name_away_review}: {' '.join(lineups_away)} \n",
    #     f"Замены у {name_home_review}: {subs_home} \n",
    #     f"Замены у {name_away_review}: {subs_away} \n",
    #     f"Авторы голов: \n",
    #     f"{goal_all_time}  \n", 
    #     f"На двоих команды нанесли {total_shots_off} ударов в створ и {total_shots_on} по воротам: \n",
    #     f"Команда {name_home_review}: {shots_off_goal_home} ударов в створ, {shots_on_goal_home} по воротам. Самый \n",
    #     f"активный по количеству ударов — {name_home_top_shots} .\n",
    #     f"Команда {name_away_review}: {shots_off_goal_away} ударов в створ, {shots_on_goal_away}  по воротам. Больше \n",
    #     f"всего нанёс ударов — {name_away_top_shots} . \n",
    #     f"В общей сложности у {name_home_review} было {total_assists_home} голевых моментов, у {name_away_review} — \n",
    #     f"{total_assists_away} .\n",
    #     f"Оборонительные действия:\n",
    #     f"Количество перехватов у {name_home_review} — {total_interceptions_home} (лидер —  \n",
    #     f"{name_home_top_interceptions}, {amount_home_interceptions} перехватов). У {name_away_review} — \n",
    #     f"{total_interceptions_away}  (больше всего у {name_away_top_interceptions}, \n",
    #     f"{amount_away_interceptions} перехватов). \n",
    #     f"Отборы. {name_home_review} — {total_blocks_home} (больше всех у {name_home_top_block}, \n",
    #     f"{amount_home_block} отборов). {name_away_review} — {total_blocks_away}  (у {name_away_top_block} —  \n",
    #     f"{amount_away_block} отборов). \n",
    #     f"Единоборства: \n",
    #     f"По количеству выигранных единоборств лидерами в командах стали: \n",
    #     f"{name_home_top_duels}, {name_home_review} (количество единоборств - {amount_home_duels}) \n",
    #     f"{name_away_top_duels}, {name_away_review} (количество единоборств - {amount_away_duels}) \n",
    #     f"Процент владения мячом: \n",
    #     f"{name_home_review} — {ball_possession_home} процентов \n",
    #     f"{name_away_review} — {ball_possession_away} процентов \n",
    #     f"Больше всего игрового времени команды провели на половине Команды 1 / 2 / в центре  \n",
    #     f"поля. (Этого параметра нет) \n",   #TODO пока нет параметра
    #     f"Наказания: \n",
    #     f"{name_home_review} *жёлтую* карточку получил(и): {yellow_card_home} \n",
    #     f"{name_away_review} *жёлтую* карточку получил(и): {yellow_card_away} \n",
    #     f"{name_home_review} *красную* карточку получил(и): {red_card_home} \n",    
    #     f"{name_away_review} *красную* карточку получил(и): {red_card_away} \n",
    #     f"Тройка лидеров в гонке бомбардиров чемпионата: \n",
    #     f"1. {topscorer_name_in_league_1}, команда {topscorer_team_in_league_1}(количество \n",
    #     f"   {topscorer_amount_in_league_1}) \n",
    #     f"2. {topscorer_name_in_league_2}, команда {topscorer_team_in_league_2}(количество \n",
    #     f"   {topscorer_amount_in_league_2}) \n",
    #     f"3. {topscorer_name_in_league_3}, команда {topscorer_team_in_league_3}(количество \n",
    #     f"   {topscorer_amount_in_league_3}) \n",
    #     f"Следующие матчи: \n",
    #     f"Команда {name_home_review} играет с {home_next_match_rival}. {home_date_match_vs_rival}, \n",
    #     f"{home_next_venue_vs_rival}. \n",
    #     f"Команда {name_away_review} играет с {away_next_match_rival}. {away_date_match_vs_rival}, \n",
    #     f"{away_venue_vs_rival}.\n") 


    # return ''.join(text)


# start_review_text('868112')