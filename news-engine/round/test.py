host = '127.0.0.1'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
import psycopg2
import requests
def check_stat_preview(insert_query):
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

host = '127.0.0.1'
user = 'db_user'
password = 'baaI$SkBvZ~P'
db_name = 'db_match'
import psycopg2
def check_stat_preview(insert_query):
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

insert_query = f"SELECT fixture_match FROM match_review WHERE league = '1';"
# insert_query = f"DELETE FROM post_review WHERE league = '1';"
fast_goal_game = check_stat_preview(insert_query)
print(len(fast_goal_game))

# def check_stat_preview2(insert_query):
#     '''Вытаскиваем всю статистику'''
#     try:
#         connection = psycopg2.connect ( 
#             host= host,
#             user = user,
#             password = password,
#             database = db_name
#         )
#         with connection.cursor() as cursor:
#             cursor.execute(insert_query)
            
#             connection.commit()
            
            
            

#     except Exception as _ex:
#         print('[INFO] ERROR', _ex)

#     finally:
#         if connection:
#             connection.close()
# for i in range(len(fast_goal_game)):
#     insert_query = f"DELETE FROM match_review WHERE fixture_match = '{fast_goal_game[i][0]}';"
#     fast_goal_game1 = check_stat_preview2(insert_query)


# team_name = ''
# team_away = ''
# insert_query = (
#     f"SELECT goals_home, goals_away, name_home_review, name_away_review FROM match_review WHERE fixture_match_for_check = 867947;"
# )
# fast_goal_game = check_stat_preview(insert_query)
# if team_name != fast_goal_game[0][2]:
#     team_away = fast_goal_game[0][2]
# if team_name != fast_goal_game[0][3]:
#     team_away = fast_goal_game[0][3]




# insert_query_destroyer = (
#     f"SELECT max(destroyer_total) AS S, team_id_api FROM teams_round WHERE league_id = {39} AND season = {2022} AND destroyer_total != 0 AND round = {13} GROUP BY team_id_api ORDER BY S DESC LIMIT 1;"
#     )
# max_destroyer= check_stat_preview(insert_query_destroyer) 
# team_id_max_destroyer = max_destroyer[0][1]
# amount_max_destroyer = max_destroyer[0][0]

# insert_query_destroyer = (
#     f"SELECT interceptions, blocks, tackles, saves FROM teams_round WHERE league_id = {39} AND season = {2022} AND team_id_api = {team_id_max_destroyer} AND round = {13};"
#     )
# data_for_max_destroyer= check_stat_preview(insert_query_destroyer) 
# data_for_max_destroyer = data_for_max_destroyer[0] #(8, 9, 23, 5)
# print(data_for_max_destroyer)



# insert_query_creator = (
#     f"SELECT max(creator_total) AS S, team_id_api FROM teams_round WHERE league_id = {39} AND season = {2022} AND creator_total != 0 AND round = {13} GROUP BY team_id_api ORDER BY S DESC LIMIT 1;"
#     )
# max_creator= check_stat_preview(insert_query_creator) 
# team_id_max_creator = max_creator[0][1]
# amount_max_creator = max_creator[0][0]

# insert_query_creator = (
#     f"SELECT duels, shots_on_target, shots_of_target FROM teams_round WHERE league_id = {39} AND season = {2022} AND team_id_api = {team_id_max_creator} AND round = {13};"
#     )
# data_for_max_creator= check_stat_preview(insert_query_creator) 
# data_for_max_creator = data_for_max_creator[0] #(110, 4, 8)



# print(data_for_max_creator)
# insert_query = (
#         f"SELECT * FROM round_preview WHERE rounds=14 AND league_id=39"
#     )

# index_for_review = check_stat_preview(insert_query)

# index_for_review = index_for_review[0]
# idd, rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3,  goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_name_max_injuries, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, new_date, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4,  team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round = index_for_review[0], index_for_review[1], index_for_review[2], index_for_review[3], index_for_review[4], index_for_review[5], index_for_review[6], index_for_review[7], index_for_review[8], index_for_review[9], index_for_review[10], index_for_review[11], index_for_review[12], index_for_review[13], index_for_review[14], index_for_review[15], index_for_review[16], index_for_review[17], index_for_review[18], index_for_review[19], index_for_review[20], index_for_review[21], index_for_review[22], index_for_review[23], index_for_review[24], index_for_review[25], index_for_review[26], index_for_review[27], index_for_review[28], index_for_review[29], index_for_review[30], index_for_review[31], index_for_review[32], index_for_review[33], index_for_review[34], index_for_review[35], index_for_review[36], index_for_review[37], index_for_review[38], index_for_review[39], index_for_review[40], index_for_review[41], index_for_review[42], index_for_review[43], index_for_review[44], index_for_review[45], index_for_review[46], index_for_review[47], index_for_review[48], index_for_review[49], index_for_review[50], index_for_review[51], index_for_review[52], index_for_review[53], index_for_review[54], index_for_review[55], index_for_review[56], index_for_review[57], index_for_review[58], index_for_review[59], index_for_review[60], index_for_review[61], index_for_review[62], index_for_review[63], index_for_review[64], index_for_review[65], index_for_review[66], index_for_review[67], index_for_review[68], index_for_review[69], index_for_review[70], index_for_review[71], index_for_review[72], index_for_review[73], index_for_review[74], index_for_review[75], index_for_review[76], index_for_review[77], index_for_review[78], index_for_review[79], index_for_review[80], index_for_review[81], index_for_review[82], index_for_review[83], index_for_review[84], index_for_review[85], index_for_review[86], index_for_review[87], index_for_review[88], index_for_review[89], index_for_review[90], index_for_review[91], index_for_review[92], index_for_review[93], index_for_review[94], index_for_review[95], index_for_review[96], index_for_review[97], index_for_review[98], index_for_review[99], index_for_review[100], index_for_review[101], index_for_review[102], index_for_review[103], index_for_review[104],  index_for_review[105], index_for_review[106], index_for_review[107], index_for_review[108], index_for_review[109], index_for_review[110], index_for_review[111], index_for_review[112]
# rank_for_table = rank_for_table.split()
# all_matches_table = all_matches_table.split()
# win_matches_table = win_matches_table.split()
# draw_matches_table = draw_matches_table.split()
# lose_matches_table = lose_matches_table.split()
# goals_scored_for_table = goals_scored_for_table.split()
# goals_missed_for_table = goals_missed_for_table.split()
# goals_diff_table = goals_diff_table.split()
# points_for_table = points_for_table.split()
# name_table_team = str(name_table_team).replace("+", " ").split()
# form_table = str(form_table).replace("+", " ").split()
# logo_for_table = str(logo_for_table).replace("+", " ").split()
# preview_home_teams = preview_home_teams.replace("+", " ").split()
# preview_away_teams = preview_away_teams.replace("+", " ").split()










# rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review,goals_home, goals_away, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season                    
# s = f"'{rounds}', '{season}', '{league_id}', '{league_name}', '{team_home_leader}', '{team_away_rival}', '{goal_leader}','{goal_rival}', '{name_home_review}',  '{name_away_review}','{goals_home}', '{goals_away}', '{count_home}','{count_away}','{count_draw}', '{h3_amounts_list}', '{h3_names_list}', '{h3_team_names_list}','{h3_fixture_match_list}', '{name_top_goals_league_1}', '{goals_top_league_1}', '{team_top_goals_league1_1}', '{name_top_goals_league_2}', '{goals_top_league_2}', '{team_top_goals_league2_1}', '{name_top_goals_league_3}', '{goals_top_league_3}', '{team_top_goals_league3_1}', '{name_top_goals_league_4}', '{goals_top_league_4}' , '{team_top_goals_league4_1}', '{name_top_goals_league_5}', '{goals_top_league_5}', '{team_top_goals_league5_1}','{all_goals_round}','{all_penalty_round}','{all_goals_previous_round}', '{total_percent_round}','{average_goals_in_season}','{average_penalty_in_season}','{time_fast_goal}','{team_name_fast_goal}', '{name_fast_goal}', '{team_away_fast_goal}', '{scrore_fast_goal}', '{team_top_destroyer}', '{destroyer_interceptions}', '{destroyer_blocks}', '{destroyer_tackles}', '{destroyer_saves}', '{amount_max_destroyer}', '{team_main_destroyer}', '{team_rival_destroyer}', '{goals_main_destroyer}', '{goals_rival_destroyer}' , '{max_destroyer_of_season_name}', '{max_destroyer_of_season_amount}', '{team_top_creator}', '{creator_duels}', '{creator_shots_on_target}', '{creator_shots_off_target}', '{team_main_creator}', '{team_rival_creator}' , '{goals_main_creator}', '{goals_rival_creator}', '{amount_max_creator}', '{max_creator_of_season_name}', '{max_creator_of_season_amount}' , '{name_max_accurate_in_round}', '{max_accurate_in_round}', '{max_total_passes_with_accurate_in_round}' , '{name_min_accurate_in_round}', '{min_accurate_in_round}', '{min_total_passes_with_accurate_in_round}', '{name_max_accuracy_in_season}', '{percent_max_accuracy_in_season}', '{name_min_accuracy_in_season}', '{percent_min_accuracy_in_season}'"               











# future_fixture_round = future_fixture_round.replace("+", " ").split()

# # #Эффективность команд:
# #     #Команда с самой высокой точностью пасов
# # team_id_home = []
# # for find_team_id in range(len(preview_home_teams)):
# #     insert_query = (
# #         f"SELECT team_id_api FROM teams_round WHERE name LIKE '{preview_home_teams[find_team_id]}'"
# #     )

# #     index_find_team_id = check_stat_preview(insert_query)
    
# #     team_id_home.append(index_find_team_id[0][0])
# # print(team_id_home)
# # sum_accuracy = []

# # for find_sum_accuracy in range(len(team_id_home)):
# #     insert_query1 = (
# #         f"SELECT COUNT(team_id_api) FROM teams_round WHERE team_id_api={team_id_home[find_sum_accuracy]}"
# #     )
# #     index_count_games = check_stat_preview(insert_query1)
    
# #     print(index_count_games[0])

# #     insert_query = (
# #         f"SELECT sum(precent_accuracy) AS W, name FROM teams_round WHERE team_id_api={team_id_home[find_sum_accuracy]} GROUP BY name ORDER BY W DESC LIMIT 1;"
# #     )
# #     index_sum_accuracy = check_stat_preview(insert_query)
    
# #     sum_accuracy.append([int(index_sum_accuracy[0][0]) // int(index_count_games[0][0]), index_sum_accuracy[0][1]])

# # name_max_accuracy = ''
# # percent_max_accuracy = 0

# # for i in range(len(sum_accuracy)):
# #     if sum_accuracy[i][0] > percent_max_accuracy:
# #         name_max_accuracy = sum_accuracy[i][1]
# #         percent_max_accuracy = sum_accuracy[i][0]

# # print(name_max_accuracy)
# headers = {
#         "X-RapidAPI-Key": "ed9df9b66dmsh3488c78a45168b3p1f47e6jsn129a6c17d435",
#         "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
#     }
# # print(percent_max_accuracy)
# url = "https://api-football-v1.p.rapidapi.com/v3/standings"

# req_leader = requests.request("GET", url, headers=headers, params={
#     "season":season,
#     "league":league_id
#     })
# data_leader = req_leader.json()
# name_leader_in_table = data_leader['response'][0]['league']['standings'][0][0]['team']['name']

# url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
# req_tour_review = requests.request("GET", url, headers=headers, params={
#     "league":league_id,
#     "season":season,
#     "round":rounds
# })

# data_tour_review = req_tour_review.json()



# id_fixture_leader_game = ''
# for find_rival_team_leader in range(len(data_tour_review['response'])):
#     if name_leader_in_table == data_tour_review['response'][find_rival_team_leader]['teams']['home']['name'] or \
#     name_leader_in_table == data_tour_review['response'][find_rival_team_leader]['teams']['away']['name']:
#         id_fixture_leader_game = data_tour_review['response'][find_rival_team_leader]['fixture']['id']
# name_home_review = []
# name_away_review = []
# goals_home = []
# goals_away = []
# who_scored_home = []
# who_scored_away = []
# for find_tour_matches in range(len(future_fixture_round)):
#     insert_query = (
#         f"SELECT name_home_review, name_away_review, goals_home, goals_away, player_home_goal, player_away_goal FROM match_review WHERE fixture_match_for_check={future_fixture_round[find_tour_matches]} AND fixture_match_for_check != {id_fixture_leader_game};"
#     )
#     index1 = check_stat_preview(insert_query)
#     index1 = index1[0]
#     print(index1[0])
#     name_home_review.append(index1[0])
#     name_away_review.append(index1[1])
#     goals_home.append(index1[2])
#     goals_away.append(index1[3])
#     who_scored_home.append(index1[4])
#     who_scored_away.append(index1[5])

# print(who_scored_home)
# print(who_scored_away)