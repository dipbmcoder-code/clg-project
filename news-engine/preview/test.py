from config import host, db_name, password, user
import psycopg2

# try: 
#     # Подключаемся
#     connection = psycopg2.connect( 
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True
#     #Создаем курсор
#     with connection.cursor() as cursor:
#         insert_query = (
#             '''CREATE TABLE review_top_players (
#                 title character varying(100) COLLATE pg_catalog."default" NOT NULL,
#                 id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1),
#                 CONSTRAINT category_pkey PRIMARY KEY (id)'''
#             )
#             #     f" INSERT INTO match_review (fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, name_home_top_fouls, amount_home_fouls, name_away_top_fouls, amount_away_fouls, id_team_home_review, id_team_away_review) " 
#             #     f"VALUES ('{1}', '{'Borussia Monchengladbach'}', '{'RB Leipzig'}', '{'Y._Sommer+M._Friedrich+N._Elvedi+R._Bensebaïni+J._Scally+L._Stindl+C._Kramer+J._Hofmann+J._Weigl+K._Koné+M._Thuram'}', '{'Y._Sommer+M._Friedrich+N._Elvedi+R._Bensebaïni+J._Scally+L._Stindl+C._Kramer+J._Hofmann+J._Weigl+K._Koné+M._Thuram'}',  '{'L._Stindl+H._Wolf+J._Hofmann+J._Weigl+M._Thuram'}', '{'A._Haidara+E._Forsberg+André_Silva+B._Henrichs'}', '{'H._Wolf+P._Herrmann+S._Lainer+T._Jantschke+N._Ngoumou'}', '{'X._Schlager+T._Werner+Y._Poulsen+Hugo_Novoa'}', '{'82 86 90 90 90'}', '{'46 46 67 80'}', '{'10 35 53'}', '{'J._Hofmann+J._Hofmann+R._Bensebaïni'}', '{''}', '{''}', '{'52 66'}', '{'Julian_Weigl+Lars_Stindl'}', '{'25 66'}', '{'Kevin_Kampl+Benjamin_Henrichs'}', '{''}', '{''}', '{''}', '{''}', '{'Jonas Hofmann'}', '{'Jonas Hofmann'}', '{'Nico Elvedi'}', '{'Kevin Kampl'}', '{'Sergey Weigl'}', '{'Pavlov Henrichs'}', '{'45%'}', '{'55%'}', '{'Pavel Koné'}', '{'Andrey Szoboszlai'}', '{'Werder Bremen'}', '{'2022-10-01'}', '{'wohninvest WESERSTADION'}', '{'VfL BOCHUM'}', '{'2022-10-01'}', '{'Red Bull Arena'}', '{'S. Becker'}', '{'N. Füllkrug'}', '{'D. Kamada'}', '{'6'}', '{'5'}', '{'4'}', '{'Union Berlin'}', '{'Werder Bremen'}', '{'Eintracht Frankfurt'}', '{871224}', '{3}', '{0}', '{10}', '{5}', '{6}', '{3}', '{2}', '{0}', '{21}', '{12}', '{15}', '{9}', '{6}', '{1}', '{3}', '{2}', '{7}', '{2}', '{14}', '{4}', '{9}', '{5}', '{8}', '{4}', '{'New'}', '{2}', '{'Awa Lo'}', '{3}', '{'Ivan Slo'}', '{1}', '{'Awa ass'}', '{2}', '{'Leha Rute'}', '{1}', '{'Vova Facs'}', '{1}', '{'Vadik Ter'}', '{1}', '{'Bitya Afa'}', '{2}', '{163}', '{173}');"
#             # )
#         cursor.execute(insert_query)
#         connection.commit()
#         print('[INFO] new insert in db')

        
# except Exception as _ex:
#         print('[INFO] ERROR', _ex)
# # Финал
# finally:
#     if connection:
#         # Отключаемся
#         connection.close()

# review_top_players

# insert_query = (
#                 f" INSERT INTO test_review (fix, id_team_home_review, name_home_top_goals, amount_home_goals, name_home_top_assists, amount_home_assists, name_home_top_interceptions, amount_home_interceptions, name_home_top_duels, amount_home_duels, name_home_top_fouls, amount_home_fouls, name_home_top_saves, amount_home_saves) " 
#                 f"VALUES ('{871219}', '{163}', '{'Serge Aguero'}', '{2}', '{'Andrew Lopet'}', '{3}', '{'Sebasti Joke'}', '{1}', '{'Holy Sheetov'}', '{2}', '{'Benzema Nebenzema'}', '{6}', '{'Suarez Urod'}', '{1}');"
#             )


# insert_query = (
#                 f" INSERT INTO Test_review (fixture_match, name_home_review, name_away_review, lineups_home, lineups_away,  gone_player_home, gone_player_away, came_player_home, came_player_away, time_subst_home, time_subst_away, time_home_goal, player_home_goal, time_away_goal, player_away_goal, time_home_yellow, player_home_yellow, time_away_yellow, player_away_yellow, time_home_red, player_home_red, time_away_red, player_away_red, name_home_top_shots, name_away_top_shots, name_home_top_block, name_away_top_block, name_home_top_interceptions, name_away_top_interceptions, ball_possession_home, ball_possession_away, name_home_top_duels, name_away_top_duels, home_next_match_rival, home_date_match_vs_rival, home_next_venue_vs_rival, away_next_match_rival, away_date_match_vs_rival, away_venue_vs_rival, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, fixture_match_for_check, goals_home, goals_away, shots_on_goal_home, shots_off_goal_home, amount_home_shots, amount_away_shots, total_assists_home, total_assists_away, total_shots_home, total_shots_away, total_shots_on, total_shots_off, total_blocks_home, amount_home_block, total_blocks_away, amount_away_block, total_interceptions_home, amount_home_interceptions, total_interceptions_away, amount_away_interceptions, amount_home_duels, amount_away_duels, shots_on_goal_away, shots_off_goal_away, name_home_top_goals, amount_home_goals, name_away_top_goals, amount_away_goals, name_home_top_assists, amount_home_assists, name_away_top_assists, amount_away_assists, name_home_top_saves, amount_home_saves, name_away_top_saves, amount_away_saves, name_home_top_fouls, amount_home_fouls, name_away_top_fouls, amount_away_fouls, id_team_home_review, id_team_away_review) " 
#                 f"VALUES ('{871219999}', '{'Borussia Monchengladbach'}', '{'RB Leipzig'}', '{'Y._Sommer+M._Friedrich+N._Elvedi+R._Bensebaïni+J._Scally+L._Stindl+C._Kramer+J._Hofmann+J._Weigl+K._Koné+M._Thuram'}', '{'Y._Sommer+M._Friedrich+N._Elvedi+R._Bensebaïni+J._Scally+L._Stindl+C._Kramer+J._Hofmann+J._Weigl+K._Koné+M._Thuram'}',  '{'L._Stindl+H._Wolf+J._Hofmann+J._Weigl+M._Thuram'}', '{'A._Haidara+E._Forsberg+André_Silva+B._Henrichs'}', '{'H._Wolf+P._Herrmann+S._Lainer+T._Jantschke+N._Ngoumou'}', '{'X._Schlager+T._Werner+Y._Poulsen+Hugo_Novoa'}', '{'82 86 90 90 90'}', '{'46 46 67 80'}', '{'10 35 53'}', '{'J._Hofmann+J._Hofmann+R._Bensebaïni'}', '{''}', '{''}', '{'52 66'}', '{'Julian_Weigl+Lars_Stindl'}', '{'25 66'}', '{'Kevin_Kampl+Benjamin_Henrichs'}', '{''}', '{''}', '{''}', '{''}', '{'Jonas Hofmann'}', '{'Jonas Hofmann'}', '{'Nico Elvedi'}', '{'Kevin Kampl'}', '{'Sergey Weigl'}', '{'Pavlov Henrichs'}', '{'45%'}', '{'55%'}', '{'Pavel Koné'}', '{'Andrey Szoboszlai'}', '{'Werder Bremen'}', '{'2022-10-01'}', '{'wohninvest WESERSTADION'}', '{'VfL BOCHUM'}', '{'2022-10-01'}', '{'Red Bull Arena'}', '{'S. Becker'}', '{'N. Füllkrug'}', '{'D. Kamada'}', '{'6'}', '{'5'}', '{'4'}', '{'Union Berlin'}', '{'Werder Bremen'}', '{'Eintracht Frankfurt'}', '{871219999}', '{3}', '{0}', '{10}', '{5}', '{6}', '{3}', '{2}', '{0}', '{21}', '{12}', '{15}', '{9}', '{6}', '{1}', '{3}', '{2}', '{7}', '{2}', '{14}', '{4}', '{9}', '{5}', '{8}', '{4}', '{'Artem2 Arte'}', '{8}', '{''}', '{0}', '{'Ivan Slo'}', '{3}', '{''}', '{0}', '{'Leha Rute'}', '{4}', '{'Vova Facs'}', '{1}', '{'Vadik Ter'}', '{13}', '{'Bitya Afa'}', '{6}', '{163}', '{173}');"
#             )



#players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_fouls_home_name,  topscorers_fouls_home_amount, topscorers_saves_home_name, topscorers_saves_home_amount = g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8],g[9],g[10],g[11]


#amount_home_goals, amount_home_assists, amount_home_interceptions, amount_home_duels, amount_home_fouls, amount_home_saves

#  output_query_home = (   
#         f"SELECT name_home_top_goals, amount_home_goals, name_home_top_assists, amount_home_assists, name_home_top_interceptions, amount_home_interceptions, name_home_top_duels, amount_home_duels,  name_home_top_fouls, amount_home_fouls, name_home_top_saves, amount_home_saves FROM match_review WHERE id_team_home_review={id_team_home_preview};"
#     )
#     g = get_test_home(output_query_home)
#     g = g[0]
    
    
#     players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_fouls_home_name,  topscorers_fouls_home_amount, topscorers_saves_home_name, topscorers_saves_home_amount = g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8],g[9],g[10],g[11]


#     output_query_away = (
#         f"SELECT name_away_top_goals, amount_away_goals, name_away_top_assists, amount_away_assists, name_away_top_interceptions, amount_away_interceptions, name_away_top_duels, amount_away_duels, name_away_top_fouls, amount_away_fouls, name_away_top_saves, amount_away_saves FROM match_review WHERE id_team_away_review={id_team_away_preview};"
#     )
#     k = get_test_away(output_query_away)
#     k = k[0]
    
    
#     players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_fouls_away_name, topscorers_fouls_away_amount, topscorers_saves_away_name, topscorers_saves_away_amount = k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11]

# output_query_home = (   
#         f"SELECT name_home_top_goals, sum(amount_home_goals), name_home_top_assists, sum(amount_home_assists), name_home_top_interceptions, sum(amount_home_interceptions), name_home_top_duels, sum(amount_home_duels),  name_home_top_fouls, sum(amount_home_fouls), name_home_top_saves, sum(amount_home_saves) AS Total FROM match_review WHERE id_team_home_review={id_team_home_preview};"
#     )
#     g = get_test_home(output_query_home)
#     g = g[0]
    
import psycopg2
def get_user_id_main(types, rounds, league_id, season, view):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host='localhost',
            user='db_user',
            password='PASS',
            database='db_match'
        )
        # Создаем курсор
        with connection.cursor() as cursor:

            if view == 'summ':
                insert_query = (
                        f"SELECT {types} FROM players_round WHERE round = {rounds} AND league_id = {league_id} AND season = {season};"
                )
                cursor.execute(insert_query)
                result = cursor.fetchall()
                l=[]
                for i in range(len(result)):
                    l.append(result[i][0])

                result2 = 0
                for i2 in range(len(l)):
                    if l[i2] != None:
                        result2 = int(l[i2]) + result2

                return result2
            elif view == 'h3':
                insert_query = (
                        f"SELECT name, max(goals), team_id AS Test FROM players_round WHERE round = {rounds} AND league_id = {league_id} AND season = {season} AND {types} != 0 AND {types} >= 2 GROUP BY name ,team_id ORDER BY Test DESC;"
                )
                cursor.execute(insert_query)
                result = cursor.fetchall()
                l1= []  #leader
                l2 =[]  # another
                for i in range(len(result)):
                    if i == 0:
                        l1.append(result[i])
                    elif i != 0:
                        l2.append(result[i])

                return l1, l2
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()
get_user_id_main('goals', '9', '39', '2022', 'h3')

# print(get_user_id_main('goals', '10','39', '2022'))

# import json

# text = ''

# with open('/root/football_bot/preview/text.txt', 'r') as file:
#     text = file.read()
    
# name = 'gooood'
# year = '2022'


# l = ['{name}', '{year}']
# l2 = [name, year]

# for i in range(len(l)):
#     if l[i] in text:
#         text = text.replace(l[i], l2[i])


# print(f"{text}")





date_match_api = []
l = []
date = ''
for i in range(len(date_match_api)):
    if date_match_api[i] > date:
        pass
    else:
        date = date_match_api[i]












# if check_match_for_insert(id_team= id_team_home_preview, id_team_in_db= 'id_team_home_review') == True:
#         output_query_home = (   
#             f"SELECT name_home_top_goals, sum(amount_home_goals) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_goals ORDER BY S DESC LIMIT 1;"
#         )   
#         g = get_request_db(output_query_home)
#         #print(g)
#         g = g[0]

#         output_query_home1 = (   
#             f"SELECT name_home_top_assists, sum(amount_home_assists) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_assists ORDER BY S DESC LIMIT 1;"
#         )
    
#         g1 = get_request_db(output_query_home1)
#         g1 = g1[0]
#         output_query_home2 = (   
#             f"SELECT name_home_top_interceptions, sum(amount_home_interceptions) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_interceptions ORDER BY S DESC LIMIT 1;"
#         )
    
#         g2 = get_request_db(output_query_home2)
#         g2 = g2[0]
        
#         output_query_home3 = (   
#             f"SELECT name_home_top_duels, sum(amount_home_duels) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_duels ORDER BY S DESC LIMIT 1;"
#         )
    
#         g3 = get_request_db(output_query_home3)
#         g3 = g3[0]
#         #print(g3[0])
#         output_query_home4 = (   
#             f"SELECT name_home_top_fouls_yel_card, sum(amount_home_fouls_yel_card) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_fouls_yel_card ORDER BY S DESC LIMIT 1;"
#         )
    
#         g4 = get_request_db(output_query_home4)
#         g4 = g4[0]
#         #print(g4[0])

#         output_query_home5 = (   
#             f"SELECT name_home_top_fouls_red_card, sum(amount_home_fouls_red_card) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_fouls_red_card ORDER BY S DESC LIMIT 1;"
#         )
    
#         g5 = get_request_db(output_query_home5)
#         g5 = g5[0]


#         output_query_home6 = (   
#             f"SELECT name_home_top_saves, sum(amount_home_saves) AS S FROM match_review WHERE id_team_home_review={id_team_home_preview} GROUP BY name_home_top_saves ORDER BY S DESC LIMIT 1;"
#         )
    
#         g6 = get_request_db(output_query_home6)
#         g6 = g6[0]

#         # print(g1, g2, g3, g4, g5)
#         players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, topscorers_saves_home_name, topscorers_saves_home_amount = g[0],g[1],g1[0],g1[1],g2[0],g2[1],g3[0],g3[1],g4[0],g4[1],g5[0],g5[1],g6[0],g6[1]
#     elif check_match_for_insert(id_team_home_preview, 'id_team_home_review') == False:
#         players_a_name, players_a_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_duels_home_name, topscorers_duels_home_amount, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, topscorers_saves_home_name, topscorers_saves_home_amount = '',0,'',0,'',0,'',0,'',0,'',0,'',0

#     if check_match_for_insert(id_team_away_preview, 'id_team_away_review') == True:
#         output_query_away = (   
#             f"SELECT name_away_top_goals, sum(amount_away_goals) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_goals ORDER BY X DESC LIMIT 1;"
#         )   
#         k = get_request_db(output_query_away)
#         k = k[0]
#         output_query_away1 = (   
#             f"SELECT name_away_top_assists, sum(amount_away_assists) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_assists ORDER BY X DESC LIMIT 1;"
#         )   
#         k1 = get_request_db(output_query_away1)
#         k1 = k1[0]

#         output_query_away2 = (   
#             f"SELECT name_away_top_interceptions, sum(amount_away_interceptions) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_interceptions ORDER BY X DESC LIMIT 1;"
#         )   
#         k2 = get_request_db(output_query_away2)
#         k2 = k2[0]

#         output_query_away3 = (   
#             f"SELECT name_away_top_duels, sum(amount_away_duels) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_duels ORDER BY X DESC LIMIT 1;"
#         )   
#         k3 = get_request_db(output_query_away3)
#         k3 = k3[0]

#         output_query_away4 = (   
#             f"SELECT name_away_top_fouls_yel_card, sum(amount_away_fouls_yel_card) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_fouls_yel_card ORDER BY X DESC LIMIT 1;"
#         )   
#         k4 = get_request_db(output_query_away4)
#         k4 = k4[0]

#         output_query_away5 = (   
#             f"SELECT name_away_top_fouls_red_card, sum(amount_away_fouls_red_card) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_fouls_red_card ORDER BY X DESC LIMIT 1;"
#         )   
#         k5 = get_request_db(output_query_away5)
#         k5 = k5[0]

#         output_query_away6 = (   
#             f"SELECT name_away_top_saves, sum(amount_away_saves) AS X FROM match_review WHERE id_team_away_review={id_team_away_preview} GROUP BY name_away_top_saves ORDER BY X DESC LIMIT 1;"
#         )   
#         k6 = get_request_db(output_query_away6)
#         k6 = k6[0]
        
#         players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, topscorers_saves_away_name, topscorers_saves_away_amount = k[0],k[1],k1[0],k1[1],k2[0],k2[1],k3[0],k3[1],k4[0],k4[1],k5[0],k5[1],k6[0],k6[1]
#     elif check_match_for_insert(id_team_away_preview, 'id_team_away_review') == False:
#         players_b_name, players_b_goals_total, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_away_name, topscorers_duels_away_amount, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_away_top_fouls_red_card, amount_away_fouls_red_card, topscorers_saves_away_name, topscorers_saves_away_amount = '',0,'',0,'',0,'',0,'',0,'',0,'',0

