
import os
from time import sleep
import requests
import json
import base64
from datetime import datetime, timedelta
#import datetime
# from db_for_app import get_user_id_main
import psycopg2

def replace_new_list(list_old):
    new_list = []
    for i in range(len(list_old)):
        if " " in list_old[i]:
            new_list.append(list_old[i].replace("_", " "))
        else:
            new_list.append(list_old[i])
    return new_list

def get_user_id_main(type_subscribe):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host='localhost',
            user='db_user',
            password='baaI$SkBvZ~P',
            database='main'
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT id_user FROM subscribe WHERE type_subscribe LIKE '{type_subscribe}';"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            l=[]
            for i in range(len(result)):
                l.append(result[i][0])
            return l
   
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()



def main_publication(rounds , types, league_id):
    list_id = get_user_id_main('football')
    season = '2022'
    
    with open(f'/opt/footballBot/result/json/{league_id}_{rounds}_{types}_round.json') as file:
        variables_json = json.load(file)
        # print(type(variables_json)) # переменные 
    
    for global_for in range(len(list_id)):
    
    # для большой скорости поместить после вывода перемен (перед текстом)
        featured_image = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/league_id_{league_id}_{rounds}_round_{types}.png"   
            
        if types == 'review':
            
            # переменые
            
            rounds = variables_json["title"]["rounds"]
            
            league_name = variables_json["title"]["league_name"]
            all_rounds = variables_json["title"]["all_rounds"]
            team_home_leader = variables_json["matches"]["team_home_leader"]
            team_away_rival = variables_json["matches"]["team_away_rival"]
            goal_leader = variables_json["matches"]["goal_leader"]
            goal_rival = variables_json["matches"]["goal_rival"]
            table_all_matches_round = variables_json["matches"]["table_all_matches_round"]
            count_home = variables_json["matches"]["count_home"]
            count_away = variables_json["matches"]["count_away"]
            count_draw = variables_json["matches"]["count_draw"]
            h3_leader = variables_json["matches"]["h3_leader"]
            h3_another = variables_json["matches"]["h3_another"]
            all_goals_round = variables_json["stats"]["all_goals_round"]
            all_penalty_round = variables_json["stats"]["all_penalty_round"]
            total_percent_round = variables_json["stats"]["total_percent_round"]
            average_goals_in_season = variables_json["stats"]["average_goals_in_season"]
            average_penalty_in_season = variables_json["stats"]["average_penalty_in_season"]
            time_fast_goal = variables_json["stats"]["time_fast_goal"]
            name_fast_goal = variables_json["stats"]["name_fast_goal"]
            team_name_fast_goal = variables_json["stats"]["team_name_fast_goal"]
            team_away_fast_goal = variables_json["stats"]["team_away_fast_goal"]
            scrore_fast_goal = variables_json["stats"]["scrore_fast_goal"]
            team_top_destroyer = variables_json["team_efficiency"]["team_top_destroyer"]
            destroyer_interceptions = variables_json["team_efficiency"]["destroyer_interceptions"]
            destroyer_blocks = variables_json["team_efficiency"]["destroyer_blocks"]
            destroyer_tackles = variables_json["team_efficiency"]["destroyer_tackles"]
            destroyer_saves = variables_json["team_efficiency"]["destroyer_saves"]
            amount_max_destroyer = variables_json["team_efficiency"]["amount_max_destroyer"]
            team_main_destroyer = variables_json["team_efficiency"]["team_main_destroyer"]
            team_rival_destroyer = variables_json["team_efficiency"]["team_rival_destroyer"]
            goals_main_destroyer = variables_json["team_efficiency"]["goals_main_destroyer"]
            goals_rival_destroyer = variables_json["team_efficiency"]["goals_rival_destroyer"]
            max_destroyer_of_season_name = variables_json["team_efficiency"]["max_destroyer_of_season_name"]
            max_destroyer_of_season_amount = variables_json["team_efficiency"]["max_destroyer_of_season_amount"]
            team_top_creator = variables_json["team_efficiency"]["team_top_creator"]
            creator_duels = variables_json["team_efficiency"]["creator_duels"]
            creator_shots_on_target = variables_json["team_efficiency"]["creator_shots_on_target"]
            creator_shots_off_target = variables_json["team_efficiency"]["creator_shots_off_target"]
            amount_max_creator = variables_json["team_efficiency"]["amount_max_creator"]
            team_main_creator = variables_json["team_efficiency"]["team_main_creator"]
            team_rival_creator = variables_json["team_efficiency"]["team_rival_creator"]
            goals_main_creator = variables_json["team_efficiency"]["goals_main_creator"]
            goals_rival_creator = variables_json["team_efficiency"]["goals_rival_creator"]
            max_creator_of_season_name = variables_json["team_efficiency"]["max_creator_of_season_name"]
            max_creator_of_season_amount = variables_json["team_efficiency"]["max_creator_of_season_amount"]
            name_max_accurate_in_round = variables_json["team_efficiency"]["name_max_accurate_in_round"]
            max_accurate_in_round = variables_json["team_efficiency"]["max_accurate_in_round"]
            max_total_passes_with_accurate_in_round = variables_json["team_efficiency"]["max_total_passes_with_accurate_in_round"]
            name_max_accuracy_in_season = variables_json["team_efficiency"]["name_max_accuracy_in_season"]
            percent_max_accuracy_in_season = variables_json["team_efficiency"]["percent_max_accuracy_in_season"]
            name_min_accurate_in_round = variables_json["team_efficiency"]["name_min_accurate_in_round"]
            min_accurate_in_round = variables_json["team_efficiency"]["min_accurate_in_round"]
            name_min_accuracy_in_season = variables_json["team_efficiency"]["name_min_accuracy_in_season"]
            min_total_passes_with_accurate_in_round = variables_json["team_efficiency"]["min_total_passes_with_accurate_in_round"]
            percent_min_accuracy_in_season = variables_json["team_efficiency"]["percent_min_accuracy_in_season"]
            name_max_saves_of_round = variables_json["players_stats"]["name_max_saves_of_round"]
            main_team_max_saves = variables_json["players_stats"]["main_team_max_saves"]
            round_max_saves_of_round = variables_json["players_stats"]["round_max_saves_of_round"]
            amount_max_saves_of_round = variables_json["players_stats"]["amount_max_saves_of_round"]
            rival_team_max_saves = variables_json["players_stats"]["rival_team_max_saves"]
            goals_and_info_max_saves = variables_json["players_stats"]["goals_and_info_max_saves"]
            top_fouls_total_yel_card = variables_json["players_stats"]["top_fouls_total_yel_card"]
            top_fouls_total_red_card = variables_json["players_stats"]["top_fouls_total_red_card"]
            top_fouls_team_name_home = variables_json["players_stats"]["top_fouls_team_name_home"]
            top_fouls_team_name_away = variables_json["players_stats"]["top_fouls_team_name_away"]
            top_fouls_goals_home = variables_json["players_stats"]["top_fouls_goals_home"]
            top_fouls_goals_away = variables_json["players_stats"]["top_fouls_goals_away"]
            name_top3_fouls_of_season = variables_json["players_stats"]["name_top3_fouls_of_season"]
            ycards_top3_fouls_of_season = variables_json["players_stats"]["ycards_top3_fouls_of_season"]
            rcards_top3_fouls_of_season = variables_json["players_stats"]["rcards_top3_fouls_of_season"]
            name_teams_cards_top3_fouls_of_season = variables_json["players_stats"]["name_teams_cards_top3_fouls_of_season"]
            round_injuries = variables_json["players_stats"]["round_injuries"]
            average_injuries_in_round = variables_json["players_stats"]["average_injuries_in_round"]
            top_round_injuries_name_team = variables_json["players_stats"]["top_round_injuries_name_team"]
            top_round_injuries_amount = variables_json["players_stats"]["top_round_injuries_amount"]
            name_top_goals_league_1 = variables_json["tops"]["name_top_goals_league_1"] 
            name_top_goals_league_2 = variables_json["tops"]["name_top_goals_league_2"]
            name_top_goals_league_3 = variables_json["tops"]["name_top_goals_league_3"]
            name_top_goals_league_4 = variables_json["tops"]["name_top_goals_league_4"]
            name_top_goals_league_5 = variables_json["tops"]["name_top_goals_league_5"]
            goals_top_league_1 = variables_json["tops"]["goals_top_league_1"] 
            goals_top_league_2 = variables_json["tops"]["goals_top_league_2"] 
            goals_top_league_3 = variables_json["tops"]["goals_top_league_3"]
            goals_top_league_4 = variables_json["tops"]["goals_top_league_4"]
            goals_top_league_5 = variables_json["tops"]["goals_top_league_5"]
            team_top_goals_league1_1 = variables_json["tops"]["team_top_goals_league1_1"] 
            team_top_goals_league2_1 = variables_json["tops"]["team_top_goals_league2_1"] 
            team_top_goals_league3_1 = variables_json["tops"]["team_top_goals_league3_1"] 
            team_top_goals_league4_1 = variables_json["tops"]["team_top_goals_league4_1"]
            team_top_goals_league5_1 = variables_json["tops"]["team_top_goals_league5_1"] 
            name_top_assists_league_1 = variables_json["tops"]["name_top_assists_league_1"] 
            assists_top_league_1 = variables_json["tops"]["assists_top_league_1"] 
            team_top_assists_league1 = variables_json["tops"]["team_top_assists_league1"]
            name_top_assists_league_2 = variables_json["tops"]["name_top_assists_league_2"] 
            assists_top_league_2 = variables_json["tops"]["assists_top_league_2"] 
            team_top_assists_league2 = variables_json["tops"]["team_top_assists_league2"]
            name_top_assists_league_3 = variables_json["tops"]["name_top_assists_league_3"]
            assists_top_league_3 = variables_json["tops"]["assists_top_league_3"]
            team_top_assists_league3 = variables_json["tops"]["team_top_assists_league3"]
            name_top_assists_league_4 = variables_json["tops"]["name_top_assists_league_4"]
            assists_top_league_4 = variables_json["tops"]["assists_top_league_4"]
            team_top_assists_league4 = variables_json["tops"]["team_top_assists_league4"]
            name_top_assists_league_5 = variables_json["tops"]["name_top_assists_league_5"]
            assists_top_league_5 = variables_json["tops"]["assists_top_league_5"]
            team_top_assists_league5 = variables_json["tops"]["team_top_assists_league5"]
            name_top_saves_league_1 = variables_json["tops"]["name_top_saves_league_1"]
            saves_top_league_1 = variables_json["tops"]["saves_top_league_1"]
            team_top_saves_league1 = variables_json["tops"]["team_top_saves_league1"]
            name_top_saves_league_2 = variables_json["tops"]["name_top_saves_league_2"]
            saves_top_league_2 = variables_json["tops"]["saves_top_league_2"]
            team_top_saves_league2 = variables_json["tops"]["team_top_saves_league2"]
            name_top_saves_league_3 = variables_json["tops"]["name_top_saves_league_3"]
            saves_top_league_3 = variables_json["tops"]["saves_top_league_3"]
            team_top_saves_league3 = variables_json["tops"]["team_top_saves_league3"]
            name_top_saves_league_4 = variables_json["tops"]["name_top_saves_league_4"]
            saves_top_league_4 = variables_json["tops"]["saves_top_league_4"]
            team_top_saves_league4 = variables_json["tops"]["team_top_saves_league4"]
            name_top_saves_league_5 = variables_json["tops"]["name_top_saves_league_5"]
            saves_top_league_5 = variables_json["tops"]["saves_top_league_5"]
            team_top_saves_league5 = variables_json["tops"]["team_top_saves_league5"]
            total_name_top_goals_league_1_round = variables_json["tops"]["total_name_top_goals_league_1_round"]
            total_name_top_goals_league_2_round = variables_json["tops"]["total_name_top_goals_league_2_round"]
            total_name_top_goals_league_3_round = variables_json["tops"]["total_name_top_goals_league_3_round"]
            total_name_top_goals_league_4_round = variables_json["tops"]["total_name_top_goals_league_4_round"]
            total_name_top_goals_league_5_round = variables_json["tops"]["total_name_top_goals_league_5_round"]
            total_of_round_top_assists_league_1 = variables_json["tops"]["total_of_round_top_assists_league_1"]
            total_of_round_top_assists_league_2 = variables_json["tops"]["total_of_round_top_assists_league_2"]
            total_of_round_top_assists_league_3 = variables_json["tops"]["total_of_round_top_assists_league_3"]
            total_of_round_top_assists_league_4 = variables_json["tops"]["total_of_round_top_assists_league_4"]
            total_of_round_top_assists_league_5 = variables_json["tops"]["total_of_round_top_assists_league_5"]
            total_of_round_top_saves_league_1 = variables_json["tops"]["total_of_round_top_saves_league_1"]
            total_of_round_top_saves_league_2 = variables_json["tops"]["total_of_round_top_saves_league_2"]
            total_of_round_top_saves_league_3 = variables_json["tops"]["total_of_round_top_saves_league_3"]
            total_of_round_top_saves_league_4 = variables_json["tops"]["total_of_round_top_saves_league_4"]
            total_of_round_top_saves_league_5 = variables_json["tops"]["total_of_round_top_saves_league_5"]
            table = variables_json["tops"]["table"]
            date_next_round = variables_json["next_round"]["date_next_round"]
            arena_next_round = variables_json["next_round"]["arena_next_round"]
            first_team_home_next_round = variables_json["next_round"]["first_team_home_next_round"]
            first_team_away_next_round = variables_json["next_round"]["first_team_away_next_round"]
                
            # '{rounds}','{league_name}','{all_rounds}','{team_home_leader}','{team_away_rival}','{goal_leader}','{goal_rival}','{table_all_matches_round}','{count_home}','{count_away}','{count_draw}','{h3_leader}','{h3_another}','{all_goals_round}','{all_penalty_round}','{total_percent_round}','{average_goals_in_season}','{average_penalty_in_season}','{time_fast_goal}','{name_fast_goal}','{team_name_fast_goal}','{team_away_fast_goal}','{scrore_fast_goal}','{team_top_destroyer}','{destroyer_interceptions}','{destroyer_blocks}','{destroyer_tackles}','{destroyer_saves}','{amount_max_destroyer}','{team_main_destroyer}','{team_rival_destroyer}','{goals_main_destroyer}','{goals_rival_destroyer}','{max_destroyer_of_season_name}','{max_destroyer_of_season_amount}','{team_top_creator}','{creator_duels}','{creator_shots_on_target}','{creator_shots_off_target}','{amount_max_creator}','{team_main_creator}','{team_rival_creator}','{goals_main_creator}','{goals_rival_creator}','{max_creator_of_season_name}','{max_creator_of_season_amount}','{name_max_accurate_in_round}','{max_accurate_in_round}','{max_total_passes_with_accurate_in_round}','{name_max_accuracy_in_season}','{percent_max_accuracy_in_season}','{name_min_accurate_in_round}','{min_accurate_in_round}','{name_min_accuracy_in_season}','{min_total_passes_with_accurate_in_round}','{percent_min_accuracy_in_season}','{name_max_saves_of_round}','{main_team_max_saves}','{round_max_saves_of_round}','{amount_max_saves_of_round}','{rival_team_max_saves}','{goals_and_info_max_saves}','{top_fouls_total_yel_card}','{top_fouls_total_red_card}','{top_fouls_team_name_home}','{top_fouls_team_name_away}','{top_fouls_goals_home}','{top_fouls_goals_away}','{name_top3_fouls_of_season}','{ycards_top3_fouls_of_season}','{rcards_top3_fouls_of_season}','{name_teams_cards_top3_fouls_of_season}','{round_injuries}','{average_injuries_in_round}','{top_round_injuries_name_team}','{top_round_injuries_amount}','{name_top_goals_league_1}','{name_top_goals_league_2}','{name_top_goals_league_3}','{name_top_goals_league_4}','{name_top_goals_league_5}','{goals_top_league_1}','{goals_top_league_2}','{goals_top_league_3}','{goals_top_league_4}','{goals_top_league_5}','{team_top_goals_league1_1}','{team_top_goals_league2_1}','{team_top_goals_league3_1}','{team_top_goals_league4_1}','{team_top_goals_league5_1}','{name_top_assists_league_1}','{assists_top_league_1}','{team_top_assists_league1}','{name_top_assists_league_2}','{assists_top_league_2}','{team_top_assists_league2}','{name_top_assists_league_3}','{assists_top_league_3}','{team_top_assists_league3}','{name_top_assists_league_4}','{assists_top_league_4}','{team_top_assists_league4}','{name_top_assists_league_5}','{assists_top_league_5}','{team_top_assists_league5}','{name_top_saves_league_1}','{saves_top_league_1}','{team_top_saves_league1}','{name_top_saves_league_2}','{saves_top_league_2}','{team_top_saves_league2}','{name_top_saves_league_3}','{saves_top_league_3}','{team_top_saves_league3}','{name_top_saves_league_4}','{saves_top_league_4}','{team_top_saves_league4}','{name_top_saves_league_5}','{saves_top_league_5}','{team_top_saves_league5}','{total_name_top_goals_league_1_round}','{total_name_top_goals_league_2_round}','{total_name_top_goals_league_3_round}','{total_name_top_goals_league_4_round}','{total_name_top_goals_league_5_round}','{total_of_round_top_assists_league_1}','{total_of_round_top_assists_league_2}','{total_of_round_top_assists_league_3}','{total_of_round_top_assists_league_4}','{total_of_round_top_assists_league_5}','{total_of_round_top_saves_league_1}','{total_of_round_top_saves_league_2}','{total_of_round_top_saves_league_3}','{total_of_round_top_saves_league_4}','{total_of_round_top_saves_league_5}','{date_next_round}','{arena_next_round}','{first_team_home_next_round}','{first_team_away_next_round}','{            #}' Получение текста
            # rounds,league_name,all_rounds,team_home_leader,team_away_rival,goal_leader,goal_rival,table_all_matches_round,count_home,count_away,count_draw,h3_leader,h3_another,all_goals_round,all_penalty_round,total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,name_fast_goal,team_name_fast_goal,team_away_fast_goal,scrore_fast_goal,team_top_destroyer,destroyer_interceptions,destroyer_blocks,destroyer_tackles,destroyer_saves,amount_max_destroyer,team_main_destroyer,team_rival_destroyer,goals_main_destroyer,goals_rival_destroyer,max_destroyer_of_season_name,max_destroyer_of_season_amount,team_top_creator,creator_duels,creator_shots_on_target,creator_shots_off_target,amount_max_creator,team_main_creator,team_rival_creator,goals_main_creator,goals_rival_creator,max_creator_of_season_name,max_creator_of_season_amount,name_max_accurate_in_round,max_accurate_in_round,max_total_passes_with_accurate_in_round,name_max_accuracy_in_season,percent_max_accuracy_in_season,name_min_accurate_in_round,min_accurate_in_round,name_min_accuracy_in_season,min_total_passes_with_accurate_in_round,percent_min_accuracy_in_season,name_max_saves_of_round,main_team_max_saves,round_max_saves_of_round,amount_max_saves_of_round,rival_team_max_saves,goals_and_info_max_saves,top_fouls_total_yel_card,top_fouls_total_red_card,top_fouls_team_name_home,top_fouls_team_name_away,top_fouls_goals_home,top_fouls_goals_away,name_top3_fouls_of_season,ycards_top3_fouls_of_season,rcards_top3_fouls_of_season,name_teams_cards_top3_fouls_of_season,round_injuries,average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_goals_league_1,name_top_goals_league_2,name_top_goals_league_3,name_top_goals_league_4,name_top_goals_league_5,goals_top_league_1,goals_top_league_2,goals_top_league_3,goals_top_league_4,goals_top_league_5,team_top_goals_league1_1,team_top_goals_league2_1,team_top_goals_league3_1,team_top_goals_league4_1,team_top_goals_league5_1,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1,name_top_assists_league_2,assists_top_league_2,team_top_assists_league2,name_top_assists_league_3,assists_top_league_3,team_top_assists_league3,name_top_assists_league_4,assists_top_league_4,team_top_assists_league4,name_top_assists_league_5,assists_top_league_5,team_top_assists_league5,name_top_saves_league_1,saves_top_league_1,team_top_saves_league1,name_top_saves_league_2,saves_top_league_2,team_top_saves_league2,name_top_saves_league_3,saves_top_league_3,team_top_saves_league3,name_top_saves_league_4,saves_top_league_4,team_top_saves_league4,name_top_saves_league_5,saves_top_league_5,team_top_saves_league5,total_name_top_goals_league_1_round,total_name_top_goals_league_2_round,total_name_top_goals_league_3_round,total_name_top_goals_league_4_round,total_name_top_goals_league_5_round,total_of_round_top_assists_league_1,total_of_round_top_assists_league_2,total_of_round_top_assists_league_3,total_of_round_top_assists_league_4,total_of_round_top_assists_league_5,total_of_round_top_saves_league_1,total_of_round_top_saves_league_2,total_of_round_top_saves_league_3,total_of_round_top_saves_league_4,total_of_round_top_saves_league_5,date_next_round,arena_next_round,first_team_home_next_round,first_team_away_next_round,            # Получение текста

            with open(f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_review_round.json') as file:
                user_text = json.load(file)

            destroyer_results = ''
            if goals_main_destroyer > goals_rival_destroyer:
                destroyer_results = 'выиграл'
            elif goals_main_destroyer < goals_rival_destroyer:
                destroyer_results = 'проиграл'
            elif goals_main_destroyer == goals_rival_destroyer:
                destroyer_results = 'сыграли в ничью'

            percent_for_round  = ''
            if total_percent_round.find('-'):
                total_percent_round.replace('-','')
                percent_for_round = 'меньше %'
            elif total_percent_round.find('+'):
                total_percent_round.replace('+','')
                percent_for_round = 'больше %'

            result_game_leader = ''
            if goal_leader > goal_rival:
                result_game_leader = 'выиграл'
            elif goal_leader < goal_rival:
                result_game_leader = 'проиграл'
            elif goal_leader == goal_rival:
                result_game_leader = 'сыграли в ничью'
            list_who_scored_of_round_name = []
            list_who_scored_of_round_amount = []
            
            total_of_round = [total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round]
            top5_name = [name_top_goals_league_1, name_top_goals_league_2, name_top_goals_league_3, name_top_goals_league_4, name_top_goals_league_5]
            
            for i in range(len(top5_name)):
                if int(total_of_round[i]) > 0:
                    list_who_scored_of_round_name.append(top5_name[i])
                    list_who_scored_of_round_amount.append(total_of_round[i])


            list_who_scored_of_round_result = ''
            for i in range(len(list_who_scored_of_round_name)):
                list_who_scored_of_round_result = list_who_scored_of_round_result + f' {list_who_scored_of_round_name[i]} ({list_who_scored_of_round_amount[i]} goals),'
           
            name_top3_fouls_of_season = name_top3_fouls_of_season.replace("+", " ").split()
            name_top3_fouls_of_season = replace_new_list(name_top3_fouls_of_season)

            # ycards_top3_fouls_of_season = str(ycards_top3_fouls_of_season).split()
            # rcards_top3_fouls_of_season = str(ycards_top3_fouls_of_season).split()
            name_teams_cards_top3_fouls_of_season =name_teams_cards_top3_fouls_of_season.replace("+", " ").split()
            name_teams_cards_top3_fouls_of_season = replace_new_list(name_teams_cards_top3_fouls_of_season)

            l1 = ['{rounds}','{league_name}','{all_rounds}','{team_home_leader}','{team_away_rival}','{goal_leader}','{goal_rival}','{table_all_matches_round}','{count_home}','{count_away}','{count_draw}','{h3_leader}','{h3_another}','{all_goals_round}','{all_penalty_round}','{total_percent_round}','{average_goals_in_season}','{average_penalty_in_season}','{time_fast_goal}','{name_fast_goal}','{team_name_fast_goal}','{team_away_fast_goal}','{scrore_fast_goal}','{team_top_destroyer}','{destroyer_interceptions}','{destroyer_blocks}','{destroyer_tackles}','{destroyer_saves}','{amount_max_destroyer}','{team_main_destroyer}','{team_rival_destroyer}','{goals_main_destroyer}','{goals_rival_destroyer}','{max_destroyer_of_season_name}','{max_destroyer_of_season_amount}','{team_top_creator}','{creator_duels}','{creator_shots_on_target}','{creator_shots_off_target}','{amount_max_creator}','{team_main_creator}','{team_rival_creator}','{goals_main_creator}','{goals_rival_creator}','{max_creator_of_season_name}','{max_creator_of_season_amount}','{name_max_accurate_in_round}','{max_accurate_in_round}','{max_total_passes_with_accurate_in_round}','{name_max_accuracy_in_season}','{percent_max_accuracy_in_season}','{name_min_accurate_in_round}','{min_accurate_in_round}','{name_min_accuracy_in_season}','{min_total_passes_with_accurate_in_round}','{percent_min_accuracy_in_season}','{name_max_saves_of_round}','{main_team_max_saves}','{round_max_saves_of_round}','{amount_max_saves_of_round}','{rival_team_max_saves}','{goals_and_info_max_saves}','{top_fouls_total_yel_card}','{top_fouls_total_red_card}','{top_fouls_team_name_home}','{top_fouls_team_name_away}','{top_fouls_goals_home}','{top_fouls_goals_away}','{name_top3_fouls_of_season}','{ycards_top3_fouls_of_season}','{rcards_top3_fouls_of_season}','{name_teams_cards_top3_fouls_of_season}','{round_injuries}','{average_injuries_in_round}','{top_round_injuries_name_team}','{top_round_injuries_amount}','{name_top_goals_league_1}','{name_top_goals_league_2}','{name_top_goals_league_3}','{name_top_goals_league_4}','{name_top_goals_league_5}','{goals_top_league_1}','{goals_top_league_2}','{goals_top_league_3}','{goals_top_league_4}','{goals_top_league_5}','{team_top_goals_league1_1}','{team_top_goals_league2_1}','{team_top_goals_league3_1}','{team_top_goals_league4_1}','{team_top_goals_league5_1}','{name_top_assists_league_1}','{assists_top_league_1}','{team_top_assists_league1}','{name_top_assists_league_2}','{assists_top_league_2}','{team_top_assists_league2}','{name_top_assists_league_3}','{assists_top_league_3}','{team_top_assists_league3}','{name_top_assists_league_4}','{assists_top_league_4}','{team_top_assists_league4}','{name_top_assists_league_5}','{assists_top_league_5}','{team_top_assists_league5}','{name_top_saves_league_1}','{saves_top_league_1}','{team_top_saves_league1}','{name_top_saves_league_2}','{saves_top_league_2}','{team_top_saves_league2}','{name_top_saves_league_3}','{saves_top_league_3}','{team_top_saves_league3}','{name_top_saves_league_4}','{saves_top_league_4}','{team_top_saves_league4}','{name_top_saves_league_5}','{saves_top_league_5}','{team_top_saves_league5}','{total_name_top_goals_league_1_round}','{total_name_top_goals_league_2_round}','{total_name_top_goals_league_3_round}','{total_name_top_goals_league_4_round}','{total_name_top_goals_league_5_round}','{total_of_round_top_assists_league_1}','{total_of_round_top_assists_league_2}','{total_of_round_top_assists_league_3}','{total_of_round_top_assists_league_4}','{total_of_round_top_assists_league_5}','{total_of_round_top_saves_league_1}','{total_of_round_top_saves_league_2}','{total_of_round_top_saves_league_3}','{total_of_round_top_saves_league_4}','{total_of_round_top_saves_league_5}','{date_next_round}','{arena_next_round}','{first_team_home_next_round}','{first_team_away_next_round}', '{list_who_scored_of_round_result}', '{result_game_leader}', '{table}','{name_top3_fouls_of_season[0]}', '{name_top3_fouls_of_season[1]}','{name_top3_fouls_of_season[2]}','{ycards_top3_fouls_of_season[0]}','{ycards_top3_fouls_of_season[1]}','{ycards_top3_fouls_of_season[2]}', '{rcards_top3_fouls_of_season[0]}','{rcards_top3_fouls_of_season[1]}','{rcards_top3_fouls_of_season[2]}', '{name_teams_cards_top3_fouls_of_season[0]}','{name_teams_cards_top3_fouls_of_season[1]}','{name_teams_cards_top3_fouls_of_season[2]}', '{destroyer_results}']
            l2 = [rounds,league_name,all_rounds,team_home_leader,team_away_rival,goal_leader,goal_rival,table_all_matches_round,count_home,count_away,count_draw,h3_leader,h3_another,all_goals_round,all_penalty_round,total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,name_fast_goal,team_name_fast_goal,team_away_fast_goal,scrore_fast_goal,team_top_destroyer,destroyer_interceptions,destroyer_blocks,destroyer_tackles,destroyer_saves,amount_max_destroyer,team_main_destroyer,team_rival_destroyer,goals_main_destroyer,goals_rival_destroyer,max_destroyer_of_season_name,max_destroyer_of_season_amount,team_top_creator,creator_duels,creator_shots_on_target,creator_shots_off_target,amount_max_creator,team_main_creator,team_rival_creator,goals_main_creator,goals_rival_creator,max_creator_of_season_name,max_creator_of_season_amount,name_max_accurate_in_round,max_accurate_in_round,max_total_passes_with_accurate_in_round,name_max_accuracy_in_season,percent_max_accuracy_in_season,name_min_accurate_in_round,min_accurate_in_round,name_min_accuracy_in_season,min_total_passes_with_accurate_in_round,percent_min_accuracy_in_season,name_max_saves_of_round,main_team_max_saves,round_max_saves_of_round,amount_max_saves_of_round,rival_team_max_saves,goals_and_info_max_saves,top_fouls_total_yel_card,top_fouls_total_red_card,top_fouls_team_name_home,top_fouls_team_name_away,top_fouls_goals_home,top_fouls_goals_away,name_top3_fouls_of_season,ycards_top3_fouls_of_season,rcards_top3_fouls_of_season,name_teams_cards_top3_fouls_of_season,round_injuries,average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_goals_league_1,name_top_goals_league_2,name_top_goals_league_3,name_top_goals_league_4,name_top_goals_league_5,goals_top_league_1,goals_top_league_2,goals_top_league_3,goals_top_league_4,goals_top_league_5,team_top_goals_league1_1,team_top_goals_league2_1,team_top_goals_league3_1,team_top_goals_league4_1,team_top_goals_league5_1,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1,name_top_assists_league_2,assists_top_league_2,team_top_assists_league2,name_top_assists_league_3,assists_top_league_3,team_top_assists_league3,name_top_assists_league_4,assists_top_league_4,team_top_assists_league4,name_top_assists_league_5,assists_top_league_5,team_top_assists_league5,name_top_saves_league_1,saves_top_league_1,team_top_saves_league1,name_top_saves_league_2,saves_top_league_2,team_top_saves_league2,name_top_saves_league_3,saves_top_league_3,team_top_saves_league3,name_top_saves_league_4,saves_top_league_4,team_top_saves_league4,name_top_saves_league_5,saves_top_league_5,team_top_saves_league5,total_name_top_goals_league_1_round,total_name_top_goals_league_2_round,total_name_top_goals_league_3_round,total_name_top_goals_league_4_round,total_name_top_goals_league_5_round,total_of_round_top_assists_league_1,total_of_round_top_assists_league_2,total_of_round_top_assists_league_3,total_of_round_top_assists_league_4,total_of_round_top_assists_league_5,total_of_round_top_saves_league_1,total_of_round_top_saves_league_2,total_of_round_top_saves_league_3,total_of_round_top_saves_league_4,total_of_round_top_saves_league_5,date_next_round,arena_next_round,first_team_home_next_round,first_team_away_next_round, list_who_scored_of_round_result, result_game_leader, table, name_top3_fouls_of_season[0], name_top3_fouls_of_season[1],name_top3_fouls_of_season[2],ycards_top3_fouls_of_season[0],ycards_top3_fouls_of_season[1],ycards_top3_fouls_of_season[2], rcards_top3_fouls_of_season[0],rcards_top3_fouls_of_season[1],rcards_top3_fouls_of_season[2], name_teams_cards_top3_fouls_of_season[0],name_teams_cards_top3_fouls_of_season[1],name_teams_cards_top3_fouls_of_season[2], destroyer_results]


            text_all = user_text['main_text']


            title = user_text['title']
            
            for i in range(len(l1)):
                if l1[i] in text_all:
                    text_all = text_all.replace(l1[i], str(l2[i]))
                if l1[i] in title:
                    title = title.replace(l1[i], str(l2[i]))




                    
        elif types == 'preview':
            # for game in variables_json:
                rounds_for_text = variables_json['title']['rounds']
                # print(rounds_for_text)
                league_id = variables_json['title']['league_id']
                all_rounds = variables_json['title']['all_rounds']
                city_first_match = variables_json['subtitle']['city']
                venue_first_match = variables_json['subtitle']['venue']
                first_date_round = variables_json['subtitle']['first_date']
                home_first_match = variables_json['subtitle']['home_first_match']
                away_first_match = variables_json['subtitle']['away_first_match']
                all_home_teams = variables_json['subtitle']['all_home_teams']
                all_away_teams = variables_json['subtitle']['all_away_teams']
                
                team_name_max_injuries = variables_json['team_stat']['team_name_injuries']
                max_injuries = variables_json['team_stat']['max_injuries']
                team_max_goals_league = variables_json['team_stat']['team_max_goals_league']
                max_goals_league = variables_json['team_stat']['max_goals_league']
                team_min_conceded_league = variables_json['team_stat']['team_min_conceded_league']
                min_conceded_top_saves = variables_json['team_stat']['min_conceded_top_saves']
                team_max_clean_sheet_league = variables_json['team_stat']['team_max_clean_sheet_league']
                max_cleen_sheet_league = variables_json['team_stat']['max_cleen_sheet_league']
                team_max_conceded_league = variables_json['team_stat']['team_max_conceded_league']
                max_conceded_saves_league = variables_json['team_stat']['max_conceded_saves_league']
                team_min_goals_attack_league = variables_json['team_stat']['team_min_goals_attack_league']
                min_goals_attack_league = variables_json['team_stat']['min_goals_attack_league']
                team_max_without_scored_league = variables_json['team_stat']['team_max_without_scored_league']
                max_without_scored_league = variables_json['team_stat']['max_without_scored_league']
                wins_without_scored = variables_json['team_stat']['wins_without_scored']
                loses_without_scored = variables_json['team_stat']['loses_without_scored']
                draws_without_scored = variables_json['team_stat']['draws_without_scored']
                team_max_conceded_goals_league = variables_json['team_stat']['team_max_conceded_goals_league']
                max_conceded_goals_league = variables_json['team_stat']['max_conceded_goals_league']
                wins_conceded_goals = variables_json['team_stat']['wins_conceded_goals']
                loses_conceded_goals = variables_json['team_stat']['loses_conceded_goals']
                draws_conceded_goals = variables_json['team_stat']['draws_conceded_goals']
                goals_top_league_1 = variables_json['players_stat']['goals_top_league_1']
                name_top_goals_league_1 = variables_json['players_stat']['name_top_goals_league_1']
                goals_top_league_2 = variables_json['players_stat']['goals_top_league_2']
                name_top_goals_league_2 = variables_json['players_stat']['name_top_goals_league_2']
                goals_top_league_3 = variables_json['players_stat']['goals_top_league_3']
                name_top_goals_league_3 = variables_json['players_stat']['name_top_goals_league_3']
                goals_top_league_4 = variables_json['players_stat']['goals_top_league_4']
                name_top_goals_league_4 = variables_json['players_stat']['name_top_goals_league_4']
                goals_top_league_5 = variables_json['players_stat']['goals_top_league_5']
                name_top_goals_league_5 = variables_json['players_stat']['name_top_goals_league_5']
                assists_top_league_1 = variables_json['players_stat']['assists_top_league_1']
                name_top_assists_league_1 = variables_json['players_stat']['name_top_assists_league_1']
                assists_top_league_2 = variables_json['players_stat']['assists_top_league_2']
                name_top_assists_league_2 = variables_json['players_stat']['name_top_assists_league_2']
                assists_top_league_3 = variables_json['players_stat']['assists_top_league_3']
                name_top_assists_league_3 = variables_json['players_stat']['name_top_assists_league_3']
                assists_top_league_4 = variables_json['players_stat']['assists_top_league_4']
                name_top_assists_league_4 = variables_json['players_stat']['name_top_assists_league_4']
                assists_top_league_5 = variables_json['players_stat']['assists_top_league_5']
                name_top_assists_league_5 = variables_json['players_stat']['name_top_assists_league_5']
                saves_top_league_1 = variables_json['players_stat']['saves_top_league_1']
                name_top_saves_league_1 = variables_json['players_stat']['name_top_saves_league_1']
                saves_top_league_2 = variables_json['players_stat']['saves_top_league_2']
                name_top_saves_league_2 = variables_json['players_stat']['name_top_saves_league_2']
                saves_top_league_3 = variables_json['players_stat']['saves_top_league_3']
                name_top_saves_league_3 = variables_json['players_stat']['name_top_saves_league_3']
                saves_top_league_4 = variables_json['players_stat']['saves_top_league_4']
                name_top_saves_league_4 = variables_json['players_stat']['name_top_saves_league_4']
                saves_top_league_5 = variables_json['players_stat']['saves_top_league_5']
                name_top_saves_league_5 = variables_json['players_stat']['name_top_saves_league_5']

                # all_matches_and_text = variables_json['subtitle']['all_matches_and_text']  #TODO Написал в дс что это
                league_name = variables_json['title']['league_name']
                odds_win_home = variables_json['BK']['odds_win_home']
                odds_win_away = variables_json['BK']['odds_win_away']
                odds_draw = variables_json['BK']['odds_draw']
                top_win_home = variables_json['BK']['top_win_home']
                top_lose_home = variables_json['BK']['top_lose_home']
                top_draw = variables_json['BK']['top_draw']
                count_matchs = variables_json['subtitle']['count_matchs']

                main_match_for_bk_team_home = variables_json['BK']['main_match_for_bk_team_home']
                main_match_for_bk_team_away = variables_json['BK']['main_match_for_bk_team_away']
                rank_for_team_home = variables_json['BK']['rank_for_team_home']
                rank_for_team_away = variables_json['BK']['rank_for_team_away']
                points_for_team_home = variables_json['BK']['points_for_team_home']
                points_for_team_away = variables_json['BK']['points_for_team_away']
                date_previous_match = variables_json['BK']['date_previous_match']
                away_previous_match = variables_json['BK']['away_previous_match'] #ПОка не нужен
                goals_home_previous_match = variables_json['BK']['goals_home_previous_match']
                goals_away_previous_match = variables_json['BK']['goals_away_previous_match']
            
                team_top_goals_league1 = variables_json['players_stat']['team_top_goals_league1']
                team_top_goals_league2 = variables_json['players_stat']['team_top_goals_league2']
                team_top_goals_league3 = variables_json['players_stat']['team_top_goals_league3']
                team_top_goals_league4 = variables_json['players_stat']['team_top_goals_league4']
                team_top_goals_league5 = variables_json['players_stat']['team_top_goals_league5']
                team_top_assists_league1 = variables_json['players_stat']['team_top_assists_league1']
                team_top_assists_league2 = variables_json['players_stat']['team_top_assists_league2']
                team_top_assists_league3 = variables_json['players_stat']['team_top_assists_league3']
                team_top_assists_league4 = variables_json['players_stat']['team_top_assists_league4']
                team_top_assists_league5 = variables_json['players_stat']['team_top_assists_league5']
                team_top_saves_league1 = variables_json['players_stat']['team_top_saves_league1']
                team_top_saves_league2 = variables_json['players_stat']['team_top_saves_league2']
                team_top_saves_league3 = variables_json['players_stat']['team_top_saves_league3']
                team_top_saves_league4 = variables_json['players_stat']['team_top_saves_league4']
                team_top_saves_league5 = variables_json['players_stat']['team_top_saves_league5']
                preview_home_teams = variables_json['subtitle']['all_home_teams']
                preview_away_teams = variables_json['subtitle']['all_away_teams']
                date_matches = variables_json['subtitle']['date_matches']
                table = variables_json['table']
                preview_home_teams = preview_home_teams.replace("+", " ").replace("'", "").replace(",", "").replace("[", "").replace("]", "").split()
                preview_away_teams = preview_away_teams.replace("+", " ").replace("'", "").replace(",", "").replace("[", "").replace("]", "").split()
                first_date_round = first_date_round.replace(" ", "T")
                date_previous_match = date_previous_match.replace(" ", "T")
                first_date_round = datetime.strptime(first_date_round[:16], "%Y-%m-%dT%H:%M").strftime('%B %d %Y')
                date_previous_match = datetime.strptime(date_previous_match[:16], "%Y-%m-%dT%H:%M").strftime('%B %d %Y')


                preview_home_teams_new = []
                preview_away_teams_new = []

                for i in range(len(preview_home_teams)):
                    
                    if '_' in preview_home_teams[i]:
                        new1 = preview_home_teams[i].replace("_", " ") 
                        preview_home_teams_new.append(new1)
                    if '_' not in preview_home_teams[i]:
                        preview_home_teams_new.append(preview_home_teams[i])
                for i in range(len(preview_away_teams)):
                    
                    if '_' in preview_away_teams[i]:
                        new2 = preview_away_teams[i].replace("_", " ") 
                        preview_away_teams_new.append(new2)

                    if '_' not in preview_away_teams[i]:
                        preview_away_teams_new.append(preview_away_teams[i])



                odds_win_home = odds_win_home.replace(",", "").split()
                odds_win_away = odds_win_away.replace(",", "").split()
                odds_draw = odds_draw.replace(",", "").split()
                date_matches = date_matches.replace("+", " ").replace("_", "T").split()



            # Цикл по всем подпискам
                with open(f'/opt/footballBot/parameters/football/users/text/{list_id[global_for]}_preview_round.json') as file:
                    user_text = json.load(file)
                    
                #TODO  Создать под универсальный текст
                data_for_title_matches = ''
                # print(all_home_teams.replace("[", "").replace("]", "").replace("'", "").split())
                for matches in range(len(preview_home_teams_new)):
                    date_for_table = date_matches[matches]
                    date_match_for = datetime.strptime(date_for_table[:15], "%Y-%m-%dT%H:%M").strftime('%B %d %Y')
                    # data_for_title_matches = data_for_title_matches + f"<li>{preview_home_teams_new[matches]} - {preview_away_teams_new[matches]} ({date_matches[matches]}), general odds: home win <b>{odds_win_home[matches]}</b>, draw <b>{odds_draw[matches]}</b>, away win <b>{odds_win_away[matches]}</b></li><br>"
                    data_for_title_matches = data_for_title_matches + f"<tr><td>{preview_home_teams_new[matches]} - {preview_away_teams_new[matches]}</td><td>{date_match_for}</td><td><b>{odds_win_home[matches]}</b></td><td><b>{odds_draw[matches]}</b></td><td><b>{odds_win_away[matches]}</b></td></tr>"
                data_for_title_matches = '<table  valign="top"><tbody><tr style= "background-color: #aedbea;"><th rowspan="2">Teams</th><th rowspan="2">Date</th><th colspan="3" rowspan="1">odds</th></tr><tr style= "background-color: #aedbea;"><th>HW</th><th>D</th><th>AW</th></tr>' + data_for_title_matches + '<tr><b><i>HW - home win, AW - away win, D - draw.</i></b></tr></tbody></table>'
                #TODO  Создать под универсальный текст
                if goals_home_previous_match > goals_away_previous_match:
                    replace_text = main_match_for_bk_team_home + ' won the previous match between this team'
                elif goals_home_previous_match == goals_away_previous_match:
                    replace_text = 'Both teams played draw last time'
                elif goals_home_previous_match < goals_away_previous_match:
                    replace_text = ''
                
                # {venue_first_game}, 
                #TODO добавить доп инфу
                match_postned = ''
                if count_matchs != '':
                    match_postned = ''


                l1=['{count_matchs}','{rounds_for_text}', '{league_id}', '{city_first_match}', '{venue_first_match}', '{first_date_round}', '{home_first_match}', '{away_first_match}', '{all_home_teams}', '{all_away_teams}', '{team_name_max_injuries}', '{max_injuries}', '{team_max_goals_league}','{max_goals_league}','{team_min_conceded_league}', '{min_conceded_top_saves}', '{team_max_clean_sheet_league}', '{max_cleen_sheet_league}','{team_max_conceded_league}','{max_conceded_saves_league}', '{team_min_goals_attack_league}', '{min_goals_attack_league}', '{team_max_without_scored_league}', '{max_without_scored_league}', '{wins_without_scored}', '{loses_without_scored}', '{draws_without_scored}', '{team_max_conceded_goals_league}', '{max_conceded_goals_league}','{wins_conceded_goals}','{loses_conceded_goals}','{draws_conceded_goals}','{goals_top_league_1}','{name_top_goals_league_1}','{goals_top_league_2}','{name_top_goals_league_2}','{goals_top_league_3}','{name_top_goals_league_3}','{goals_top_league_4}','{name_top_goals_league_4}','{goals_top_league_5}','{name_top_goals_league_5}','{assists_top_league_1}','{name_top_assists_league_1}','{assists_top_league_2}','{name_top_assists_league_2}','{assists_top_league_3}','{name_top_assists_league_3}','{assists_top_league_4}','{name_top_assists_league_4}','{assists_top_league_5}','{name_top_assists_league_5}','{saves_top_league_1}','{name_top_saves_league_1}','{saves_top_league_2}','{name_top_saves_league_2}','{saves_top_league_3}','{name_top_saves_league_3}','{saves_top_league_4}','{name_top_saves_league_4}','{saves_top_league_5}','{name_top_saves_league_5}','{league_name}', '{odds_win_home}', '{odds_win_away}', '{odds_draw}', '{top_win_home}', '{top_lose_home}', '{top_draw}', '{team_top_goals_league1}', '{team_top_goals_league2}', '{team_top_goals_league3}', '{team_top_goals_league4}', '{team_top_goals_league5}', '{team_top_assists_league1}', '{team_top_assists_league2}', '{team_top_assists_league3}', '{team_top_assists_league4}', '{team_top_assists_league5}', '{team_top_saves_league1}', '{team_top_saves_league2}', '{team_top_saves_league3}', '{team_top_saves_league4}', '{team_top_saves_league5}', '{preview_home_teams}', '{preview_away_teams}', '{date_matches}', '{table}', '{main_match_for_bk_team_home}','{main_match_for_bk_team_away}','{rank_for_team_home}','{rank_for_team_away}','{points_for_team_home}','{points_for_team_away}','{date_previous_match}','{away_previous_match}','{goals_home_previous_match}','{goals_away_previous_match}', '{replace_text}', '{data_for_title_matches}', '{all_rounds}']
                l2=[count_matchs, rounds_for_text, league_id, city_first_match, venue_first_match, first_date_round, home_first_match, away_first_match, all_home_teams, all_away_teams, team_name_max_injuries, max_injuries, team_max_goals_league,max_goals_league,team_min_conceded_league, min_conceded_top_saves, team_max_clean_sheet_league, max_cleen_sheet_league,team_max_conceded_league,max_conceded_saves_league, team_min_goals_attack_league, min_goals_attack_league, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league,wins_conceded_goals,loses_conceded_goals,draws_conceded_goals,goals_top_league_1,name_top_goals_league_1,goals_top_league_2,name_top_goals_league_2,goals_top_league_3,name_top_goals_league_3,goals_top_league_4,name_top_goals_league_4,goals_top_league_5,name_top_goals_league_5,assists_top_league_1,name_top_assists_league_1,assists_top_league_2,name_top_assists_league_2,assists_top_league_3,name_top_assists_league_3,assists_top_league_4,name_top_assists_league_4,assists_top_league_5,name_top_assists_league_5,saves_top_league_1,name_top_saves_league_1,saves_top_league_2,name_top_saves_league_2,saves_top_league_3,name_top_saves_league_3,saves_top_league_4,name_top_saves_league_4,saves_top_league_5,name_top_saves_league_5, league_name, odds_win_home, odds_win_away, odds_draw, top_win_home, top_lose_home, top_draw, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, preview_home_teams, preview_away_teams, date_matches, table, main_match_for_bk_team_home,main_match_for_bk_team_away,rank_for_team_home,rank_for_team_away,points_for_team_home,points_for_team_away,date_previous_match,away_previous_match,goals_home_previous_match,goals_away_previous_match, replace_text, data_for_title_matches, all_rounds]
                
                print(len(l1))
                print(len(l2))
                
                # l2=[rounds_for_text,league_id,city_first_match,venue_first_match,first_date_round,home_first_match,away_first_match,all_home_teams,all_away_teams,team_name_max_injuries,max_injuries,team_max_goals_league,max_goals_league,team_min_conceded_league,min_conceded_top_saves,team_max_clean_sheet_league,max_cleen_sheet_league,team_max_conceded_league,max_conceded_saves_league,team_min_goals_attack_league,min_goals_attack_league,team_max_without_scored_league,max_without_scored_league,wins_without_scored,loses_without_scored,draws_without_scored,team_max_conceded_goals_league,max_conceded_goals_league,wins_conceded_goals,loses_conceded_goals,draws_conceded_goals,goals_top_league_1,name_top_goals_league_1,goals_top_league_2,name_top_goals_league_2,goals_top_league_3,name_top_goals_league_3,goals_top_league_4,name_top_goals_league_4,goals_top_league_5,name_top_goals_league_5,assists_top_league_1,name_top_assists_league_1,assists_top_league_2,name_top_assists_league_2,assists_top_league_3,name_top_assists_league_3,assists_top_league_4,name_top_assists_league_4,assists_top_league_5,name_top_assists_league_5,saves_top_league_1,name_top_saves_league_1,saves_top_league_2,name_top_saves_league_2,saves_top_league_3,name_top_saves_league_3,saves_top_league_4,name_top_saves_league_4,saves_top_league_5,name_top_saves_league_5, league_name, odds_win_home, odds_win_away, odds_draw, top_win_home, top_lose_home, top_draw, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, preview_home_teams, preview_away_teams, date_matches, table, main_match_for_bk_team_home,main_match_for_bk_team_away,rank_for_team_home,rank_for_team_away,points_for_team_home,points_for_team_away,date_previous_match,away_previous_match,goals_home_previous_match,goals_away_previous_match, replace_text]

                text_all = user_text['main_text']
                print(type(text_all))
                title = user_text['title']
                
                for i in range(len(l1)):
                    if l1[i] in text_all:
                        text_all = text_all.replace(l1[i], str(l2[i]))
                    if l1[i] in title:
                        title = title.replace(l1[i], l2[i])







                # url = 'https://botbot.news/wp-json/wp/v2/posts'
                # user = 'botbot'
                # password = 'cGvj MT0x lqRl cEuY tddX huHk'

        #TODO  создать цикл для нескольких платформ юзеров, идея такая: переделаем стрроку в список + проверка на len > 1 + цикл по всем платформ 
        with open(f'/opt/footballBot/parameters/football/users/parameters/{list_id[global_for]}.json') as file:
            data_j = json.load(file)

        platform_name = data_j['platform_name']

        if platform_name == 'wordpress':
            url = data_j['platform_url']
            user = data_j['platform_user']
            password = data_j['platform_password']

            credentials = user + ':' + password

            token = base64.b64encode(credentials.encode())
            header = {'Authorization': 'Basic ' + token.decode('utf-8')}
            
            post = {
            'title'    : title,
            'status'   : 'publish', #тип
            'content'  : text_all,
            # 'categories': category, # category ID
            # 'date'   : f'{date}',   # время публикации --  {время матча - один день} 
            'meta' : { '_knawatfibu_url': featured_image }    
            }
            responce = requests.post(url , headers=header, json=post)
            print(responce.text)
            print(f"[INFO]  posted")

        # '2022-09-30T8:00:00'
        # print('app')









# main_publication('15', 'review', '39')

# main_publication('14', 'preview', '39')
        # list_posted_matches = ['1224', '2345']   
        # r1 = ''
        # r2 = ''     
        # if list_posted_matches != []:
            #     if team_home_id in list_posted_matches:
            #         r1 = '(Матч перенесен)'
            #     if team_away_id in list_posted_matches:
            #         r2 = '(Матч перенесен)'

            # text = '<li>{team_home_other_games}— {team_away_other_games} (date_other_games), general odds: home win **, draw **, away win **.</li>{r}'


            