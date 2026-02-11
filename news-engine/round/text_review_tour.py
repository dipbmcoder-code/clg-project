import json
from db import check_stat_preview
import datetime
def replace_new_list(list_old):
    new_list = []
    for i in range(len(list_old)):
        if " " in list_old[i]:
            new_list.append(list_old[i].replace("_", " "))
        else:
            new_list.append(list_old[i])
    return new_list



def review_round_text(rounds, league_id):
    from db import get_data_round

    # Запрос в БД
    insert_query = (
        f"SELECT rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home, goals_away, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves FROM round_review WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_review_round = get_data_round(insert_query)
    print(index_text_review_round)
    index_text_review_round = index_text_review_round[0]


    rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home, goals_away, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves = index_text_review_round
    
    rank_for_table = rank_for_table.split()
    all_matches_table = all_matches_table.split()
    win_matches_table = win_matches_table.split()
    draw_matches_table = draw_matches_table.split()
    lose_matches_table = lose_matches_table.split()
    goals_scored_for_table = goals_scored_for_table.split()
    goals_missed_for_table = goals_missed_for_table.split()
    goals_diff_table = goals_diff_table.split()
    points_for_table = points_for_table.split()
    name_table_team = str(name_table_team).replace("+", " ").split()
    form_table = str(form_table).replace("+", " ").split()
    logo_for_table = str(logo_for_table).replace("+", " ").split()

    name_home_review = str(name_home_review).replace("+", " ").split()
    name_away_review = str(name_away_review).replace("+", " ").split()
    # who_scored_home = str(who_scored_home).replace("+", " ").split()
    # who_scored_away = str(who_scored_away).replace("+", " ").split()
    # name_top3_fouls_of_season = str(name_top3_fouls_of_season).replace("+", " ").split()
    # ycards_top3_fouls_of_season = str(ycards_top3_fouls_of_season).split()
    # rcards_top3_fouls_of_season = str(rcards_top3_fouls_of_season).split()
    rcards_top3_fouls_of_season = rcards_top3_fouls_of_season.replace(" ", "")
    ycards_top3_fouls_of_season = ycards_top3_fouls_of_season.replace(" ", "")
    # sum_accuracy = str(sum_accuracy).split()
    # name_teams_cards_top3_fouls_of_season = str(name_teams_cards_top3_fouls_of_season).replace("+", " ").split()
    # sum_accuracy_name = str(sum_accuracy_name).replace("+", " ").split()
    goals_home = goals_home.split()
    goals_away = goals_away.split()
    h3_amounts_list = str(h3_amounts_list).split()

    x = datetime.datetime(int(date_game_max_saves[:4]), int(date_game_max_saves[5:7]), int(date_game_max_saves[8:10]))
    date_game_max_saves = x.strftime('%B %d %Y')
    
    
    name_home_review = replace_new_list(name_home_review)
    name_away_review = replace_new_list(name_away_review)
    # who_scored_home = replace_new_list(who_scored_home)
    # who_scored_away = replace_new_list(who_scored_away)
    # name_top3_fouls_of_season = replace_new_list(name_top3_fouls_of_season)
    # name_teams_cards_top3_fouls_of_season = replace_new_list(name_teams_cards_top3_fouls_of_season)
    name_table_team = replace_new_list(name_table_team)
    name_max_accuracy_in_season = name_max_accuracy_in_season.replace("_", " ")
    
    # goals_home = goals_home.split()
    

    h3_leader = ''
    h3_another = ''
    best_team_of_the_season = name_table_team[0]
    f = ''
    for table in range(len(rank_for_table)):
        f = f + f"<tr align='centre' valign='top'><td>{rank_for_table[table]}</td><td><img src='{logo_for_table[table]}' alt=''></td><td>{name_table_team[table]}</td><td>{form_table[table]}</td><td>{all_matches_table[table]}</td><td>{win_matches_table[table]}</td><td>{draw_matches_table[table]}</td><td>{lose_matches_table[table]}</td><td>{goals_scored_for_table[table]}</td><td>{goals_missed_for_table[table]}</td><td>{goals_diff_table[table]}</td><td>{points_for_table[table]}</td></tr>"
    



    

    all_matches_round = ''
    all_matches_round_tg = ''
    name_home_review_for_all_matches = team_home_leader
    name_away_review_for_all_matches = team_away_rival
    goals_home_new = goal_leader
    goals_away_new = goal_rival
    for all_matches in range(len(name_home_review)):
        # print(name_home_review[all_matches])
        # print(type(goals_home))
        # goals_home_new  =  goals_home[all_matches]
        # goals_away_new  =  goals_away[all_matches]
        # name_home_review_for_all_matches = name_home_review[all_matches]
        # name_away_review_for_all_matches = name_away_review[all_matches]
        # print(name_home_review_for_all_matches)
        # print(name_away_review_for_all_matches)
        all_matches_round = all_matches_round + f"<tr align='centre' valign='top'><td>{str(name_home_review_for_all_matches).replace('_',' ')} - {str(name_away_review_for_all_matches).replace('_', ' ')}</td><td>{goals_home_new} - {goals_away_new}</td></tr>"
        all_matches_round_tg = all_matches_round_tg + f"{all_matches+1}. {str(name_home_review_for_all_matches).replace('_',' ')} - {str(name_away_review_for_all_matches).replace('_', ' ')} ({goals_home_new} - {goals_away_new})\n"
        goals_home_new  =  goals_home[all_matches]
        goals_away_new  =  goals_away[all_matches]
        name_home_review_for_all_matches = name_home_review[all_matches]
        name_away_review_for_all_matches = name_away_review[all_matches]
    
    
    data = {
        "title":{
            "rounds":f"{rounds}",
            "league_name":f"{league_name}", 
            "all_rounds":f"{all_rounds}",
            "all_matches_round_tg":f"{all_matches_round_tg}"
        },
        "matches":{
            "team_home_leader":f"{team_home_leader}",
            "team_away_rival":f"{team_away_rival}",
            "goal_leader":f"{goal_leader}",
            "goal_rival":f"{goal_rival}",
            "all_matches_round":f"{all_matches_round}",
            "count_home":f"{count_home}",
            "count_away":f"{count_away}",
            "count_draw":f"{count_draw}",
            "h3_leader":f"{h3_leader}",
            "h3_another":f"{h3_another}"
        },
        "stats":{
                      
            "all_goals_round":f"{all_goals_round}",
            "all_penalty_round":f"{all_penalty_round}",
            "total_percent_round":f"{total_percent_round}",
            "average_goals_in_season":f"{average_goals_in_season}",
            "all_penalty_round":f"{all_penalty_round}",
            "average_penalty_in_season":f"{average_penalty_in_season}",
            "time_fast_goal":f"{time_fast_goal}",
            "name_fast_goal":f"{name_fast_goal}",
            "team_name_fast_goal":f"{team_name_fast_goal}",
            "team_away_fast_goal":f"{team_away_fast_goal}",
            "scrore_fast_goal":f"{scrore_fast_goal}"
        },
        "team_efficiency":{
            "team_top_destroyer":f"{team_top_destroyer}",
            "destroyer_interceptions":f"{destroyer_interceptions}",
            "destroyer_blocks":f"{destroyer_blocks}",
            "destroyer_tackles":f"{destroyer_tackles}",
            "destroyer_saves":f"{destroyer_saves}",
            "amount_max_destroyer":f"{amount_max_destroyer}",
            "team_main_destroyer":f"{team_main_destroyer}",
            "team_rival_destroyer":f"{team_rival_destroyer}",
            "goals_main_destroyer":f"{goals_main_destroyer}",
            "goals_rival_destroyer":f"{goals_rival_destroyer}",
            "max_destroyer_of_season_name":f"{max_destroyer_of_season_name}",
            "max_destroyer_of_season_amount":f"{max_destroyer_of_season_amount}",
            

            "team_top_creator":f"{team_top_creator}",
            "creator_duels":f"{creator_duels}",
            "creator_shots_on_target":f"{creator_shots_on_target}",
            "creator_shots_off_target":f"{creator_shots_off_target}",
            "amount_max_creator":f"{amount_max_creator}",
            "team_main_creator":f"{team_main_creator}",
            "team_rival_creator":f"{team_rival_creator}",
            "goals_main_creator":f"{goals_main_creator}",
            "goals_rival_creator":f"{goals_rival_creator}",
            "max_creator_of_season_name":f"{max_creator_of_season_name}",
            "max_creator_of_season_amount":f"{max_creator_of_season_amount}",

            "name_max_accurate_in_round":f"{name_max_accurate_in_round}",
            "max_accurate_in_round":f"{max_accurate_in_round}",
            "max_total_passes_with_accurate_in_round":f"{max_total_passes_with_accurate_in_round}",
            "name_max_accuracy_in_season":f"{name_max_accuracy_in_season}",
            "percent_max_accuracy_in_season":f"{percent_max_accuracy_in_season}",
            "name_min_accurate_in_round":f"{name_min_accurate_in_round}",
            "min_accurate_in_round":f"{min_accurate_in_round}",
            "name_min_accuracy_in_season":f"{name_min_accuracy_in_season}",
            "min_total_passes_with_accurate_in_round":f"{min_total_passes_with_accurate_in_round}",
            "percent_min_accuracy_in_season":f"{percent_min_accuracy_in_season}",

        },
        "players_stats":{
            "name_max_saves_of_round":f"{name_max_saves_of_round}",
            "main_team_max_saves":f"{main_team_max_saves}",
            "round_max_saves_of_round":f"{round_max_saves_of_round}",
            "amount_max_saves_of_round":f"{amount_max_saves_of_round}",
            "rival_team_max_saves":f"{rival_team_max_saves}",
            "goals_and_info_max_saves":f"{goals_and_info_max_saves}",
            "date_game_max_saves":f"{date_game_max_saves}",
            "top_fouls_total_yel_card":f"{top_fouls_total_yel_card}",
            "top_fouls_total_red_card":f"{top_fouls_total_red_card}",
            "top_fouls_team_name_home":f"{top_fouls_team_name_home}",
            "top_fouls_team_name_away":f"{top_fouls_team_name_away}",
            "top_fouls_goals_home":f"{top_fouls_goals_home}",
            "top_fouls_goals_away":f"{top_fouls_goals_away}",
            "name_top3_fouls_of_season":f"{name_top3_fouls_of_season}",
            "ycards_top3_fouls_of_season":f"{ycards_top3_fouls_of_season}",
            "rcards_top3_fouls_of_season":f"{rcards_top3_fouls_of_season}",
            "name_teams_cards_top3_fouls_of_season":f"{name_teams_cards_top3_fouls_of_season}",
            "round_injuries":f"{round_injuries}",
            "average_injuries_in_round":f"{average_injuries_in_round}",
            "top_round_injuries_name_team":f"{top_round_injuries_name_team}",
            "top_round_injuries_amount":f"{top_round_injuries_amount}"
            
        },
        "tops":{
            "name_top_goals_league_1":f"{name_top_goals_league_1}",
            "name_top_goals_league_2":f"{name_top_goals_league_2}",
            "name_top_goals_league_3":f"{name_top_goals_league_3}",
            "name_top_goals_league_4":f"{name_top_goals_league_4}",
            "name_top_goals_league_5":f"{name_top_goals_league_5}",
            "goals_top_league_1":f"{goals_top_league_1}",
            "goals_top_league_2":f"{goals_top_league_2}",
            "goals_top_league_3":f"{goals_top_league_3}",
            "goals_top_league_4":f"{goals_top_league_4}",
            "goals_top_league_5":f"{goals_top_league_5}",
            "team_top_goals_league1_1":f"{team_top_goals_league1_1}",
            "team_top_goals_league2_1":f"{team_top_goals_league2_1}",
            "team_top_goals_league3_1":f"{team_top_goals_league3_1}",
            "team_top_goals_league4_1":f"{team_top_goals_league4_1}",
            "team_top_goals_league5_1":f"{team_top_goals_league5_1}",
            "name_top_assists_league_1":f"{name_top_assists_league_1}",
            "assists_top_league_1":f"{assists_top_league_1}",
            "team_top_assists_league1":f"{team_top_assists_league1}",
            "name_top_assists_league_2":f"{name_top_assists_league_2}",
            "assists_top_league_2":f"{assists_top_league_2}",
            "team_top_assists_league2":f"{team_top_assists_league2}",
            "name_top_assists_league_3":f"{name_top_assists_league_3}",
            "assists_top_league_3":f"{assists_top_league_3}",
            "team_top_assists_league3":f"{team_top_assists_league3}",
            "name_top_assists_league_4":f"{name_top_assists_league_4}",
            "assists_top_league_4":f"{assists_top_league_4}",
            "team_top_assists_league4":f"{team_top_assists_league4}",
            "name_top_assists_league_5":f"{name_top_assists_league_5}",
            "assists_top_league_5":f"{assists_top_league_5}",
            "team_top_assists_league5":f"{team_top_assists_league5}",
            "name_top_saves_league_1":f"{name_top_saves_league_1}",
            "saves_top_league_1":f"{saves_top_league_1}",
            "team_top_saves_league1":f"{team_top_saves_league1}",
            "name_top_saves_league_2":f"{name_top_saves_league_2}",
            "saves_top_league_2":f"{saves_top_league_2}",
            "team_top_saves_league2":f"{team_top_saves_league2}",
            "name_top_saves_league_3":f"{name_top_saves_league_3}",
            "saves_top_league_3":f"{saves_top_league_3}",
            "team_top_saves_league3":f"{team_top_saves_league3}",
            "name_top_saves_league_4":f"{name_top_saves_league_4}",
            "saves_top_league_4":f"{saves_top_league_4}",
            "team_top_saves_league4":f"{team_top_saves_league4}",
            "name_top_saves_league_5":f"{name_top_saves_league_5}",
            "saves_top_league_5":f"{saves_top_league_5}",
            "team_top_saves_league5":f"{team_top_saves_league5}",
            "total_name_top_goals_league_1_round":f"{total_name_top_goals_league_1_round}",
            "total_name_top_goals_league_2_round":f"{total_name_top_goals_league_2_round}",
            "total_name_top_goals_league_3_round":f"{total_name_top_goals_league_3_round}",
            "total_name_top_goals_league_4_round":f"{total_name_top_goals_league_4_round}",
            "total_name_top_goals_league_5_round":f"{total_name_top_goals_league_5_round}",
            "total_of_round_top_assists_league_1":f"{total_of_round_top_assists_league_1}",
            "total_of_round_top_assists_league_2":f"{total_of_round_top_assists_league_2}",
            "total_of_round_top_assists_league_3":f"{total_of_round_top_assists_league_3}",
            "total_of_round_top_assists_league_4":f"{total_of_round_top_assists_league_4}",
            "total_of_round_top_assists_league_5":f"{total_of_round_top_assists_league_5}",
            "total_of_round_top_saves_league_1":f"{total_of_round_top_saves_league_1}",
            "total_of_round_top_saves_league_2":f"{total_of_round_top_saves_league_2}",
            "total_of_round_top_saves_league_3":f"{total_of_round_top_saves_league_3}",
            "total_of_round_top_saves_league_4":f"{total_of_round_top_saves_league_4}",
            "total_of_round_top_saves_league_5":f"{total_of_round_top_saves_league_5}",
            "f_table":f"{f}",
            "h3_team_names_list":f"{h3_team_names_list}",
            "h3_names_list":f"{h3_names_list}",
            "h3_fixture_match_list":f"{h3_fixture_match_list}",
            "h3_amounts_list":f"{h3_amounts_list}", 
            'city_next_round':f"{city_next_round}",
            "best_team_of_the_season":f"{best_team_of_the_season}"



        },
        "next_round":{
            "date_next_round":f"{date_next_round}",
            "arena_next_round":f"{arena_next_round}",
            "first_team_home_next_round":f"{first_team_home_next_round}",
            "first_team_away_next_round":f"{first_team_away_next_round}",
        }  
    }

    with open(f"/opt/footballBot/result/json/{league_id}_{rounds}_review_round.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)



# review_round_text(19, 39)