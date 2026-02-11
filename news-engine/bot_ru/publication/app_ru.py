import os
from time import sleep
import requests
import json
import base64
from datetime import datetime, timedelta





# url = str(os.getenv("url"))
# user = str(os.getenv("user"))
# password = str(os.getenv("password"))


def main_publication_ru(fixture_match, types):



    with open(f'/root/result/json/{fixture_match}_{types}.json') as file:
        text = json.load(file)
    
    
    featured_image_url = f"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_{types}.png"
    


    if types == "review":
        img_graph = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_graph_{types}.png\" alt=\"\">"
        img_lineups = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/{fixture_match}_lineups_{types}.png\" alt=\"\">"

        for game in text:
            team1= game['title']['team_a']
            team2= game['title']['team_b']
            goals_a= game['title']['goal_a']
            goals_b= game['title']['goal_b']
            league_name1 = game['title']['league_name']
            lineups_a=game['subtitle_lineups']['lineups_a']
            if lineups_a.find('rating'):
                lineups_a = lineups_a.replace('(rating', '(оценка')
            lineups_b=game['subtitle_lineups']['lineups_b']
            if lineups_b.find('rating'):
                lineups_b = lineups_b.replace('(rating', '(оценка')
            
            lineups_in_game_a=game['subtitle_lineups']['lineups_in_game_a']
            lineups_in_game_b=game['subtitle_lineups']['lineups_in_game_b']
            first_goal = game['goals_scorers']['goals']['first_goal']
            if first_goal.find('drop first goal at'):
                first_goal = first_goal.replace('drop first goal at', 'забил мяч на')
                first_goal = first_goal.replace('minute of the match.', 'минуте матча.')
            all_scorers=game['goals_scorers']['goals']['all_scorers']
            if all_scorers.find('at'):
                all_scorers = all_scorers.replace('at', 'на')
                all_scorers = all_scorers.replace('minute', 'минуте')
            total_shots_off=game['goals_scorers']['goals']['total_shots_off']
            total_shots_on=game['goals_scorers']['goals']['total_shots_on']
            shots_team1_off=game['goals_scorers']['goals']['shots_team1_off']
            shots_team1_on=game['goals_scorers']['goals']['shots_team1_on']
            active_shots_player_home=game['goals_scorers']['goals']['active_shots_player_home']
            shots_team2_off=game['goals_scorers']['goals']['shots_team2_off']
            shots_team2_on=game['goals_scorers']['goals']['shots_team2_on']
            active_shots_player_away=game['goals_scorers']['goals']['active_shots_player_away']
            total_assists_home=game['goals_scorers']['goals']['total_assists_home']
            total_assists_away=game['goals_scorers']['goals']['total_assists_away']
            total_interceptions_home=game['goals_scorers']['defensive']['total_interceptions_home']
            name_top_inceptions_home=game['goals_scorers']['defensive']['name_top_inceptions_home']
            amount_interceptions_home=game['goals_scorers']['defensive']['amount_interceptions_home']
            total_inteceptions_away=game['goals_scorers']['defensive']['total_inteceptions_away']
            name_top_inceptions_away=game['goals_scorers']['defensive']['name_top_inceptions_away']
            amount_interseptions_away=game['goals_scorers']['defensive']['amount_interseptions_away']
            total_blocks_home=game['goals_scorers']['defensive']['total_blocks_home']
            name_top_blocks_home=game['goals_scorers']['defensive']['name_top_blocks_home']
            amount_blocks_home=game['goals_scorers']['defensive']['amount_blocks_home']
            total_blocks_away=game['goals_scorers']['defensive']['total_blocks_away']
            name_top_blocks_away=game['goals_scorers']['defensive']['name_top_blocks_away']
            amount_blocks_away=game['goals_scorers']['defensive']['amount_blocks_away']
            name_duels_team1=game['goals_scorers']['duels']['name_duels_team1']
            amount_duels_team1=game['goals_scorers']['duels']['amount_duels_team1']
            name_duels_team2=game['goals_scorers']['duels']['name_duels_team2']
            amount_duels_team2=game['goals_scorers']['duels']['amount_duels_team2']
            possession_team1=game['goals_scorers']['ball_pos']['possession_team1']
            possession_team2=game['goals_scorers']['ball_pos']['possession_team2']
            fouls_yel_team1=game['goals_scorers']['fouls']['fouls_yel_team1']
            if fouls_yel_team1.find('at'):
                fouls_yel_team1 = fouls_yel_team1.replace('at', 'на')
                fouls_yel_team1 = fouls_yel_team1.replace('minute', 'минуте')
            fouls_yel_team2=game['goals_scorers']['fouls']['fouls_yel_team2']
            if fouls_yel_team2.find('at'):
                fouls_yel_team2 = fouls_yel_team2.replace('at', 'на')
                fouls_yel_team2 = fouls_yel_team2.replace('minute', 'минуте')
            fouls_red_team1=game['goals_scorers']['fouls']['fouls_red_team1']
            if fouls_red_team1.find('at'):
                fouls_red_team1 = fouls_red_team1.replace('at', 'на')
                fouls_red_team1 = fouls_red_team1.replace('minute', 'минуте')
            fouls_red_team2=game['goals_scorers']['fouls']['fouls_red_team2']
            if fouls_red_team2.find('at'):
                fouls_red_team2 = fouls_red_team2.replace('at', 'на')
                fouls_red_team2 = fouls_red_team2.replace('minute', 'минуте')
            first_top_name=game['top_players_league']['top3']['first_top_name']
            first_top_team=game['top_players_league']['top3']['first_top_team']
            first_top_amount=game['top_players_league']['top3']['first_top_amount']
            second_top_name=game['top_players_league']['top3']['second_top_name']
            second_top_team=game['top_players_league']['top3']['second_top_team']
            second_top_amount=game['top_players_league']['top3']['second_top_amount']
            third_top_name=game['top_players_league']['top3']['third_top_name']
            third_top_team=game['top_players_league']['top3']['third_top_team']
            third_top_amount=game['top_players_league']['top3']['third_top_amount']
            next_match_team1_with=game['next_matches']['show_next_matches']['next_match_team1_with']
            next_match_team1_date=game['next_matches']['show_next_matches']['next_match_team1_date']
            next_match_team1_venue=game['next_matches']['show_next_matches']['next_match_team1_venue']
            next_match_team2_with=game['next_matches']['show_next_matches']['next_match_team2_with']
            next_match_team2_date=game['next_matches']['show_next_matches']['next_match_team2_date']
            next_match_team2_venue=game['next_matches']['show_next_matches']['next_match_team2_venue']
            arena= game['title']['venue']
            date= game['title']['date_match3']
            form_home= game['title']['form_home']
            form_away= game['title']['form_away']
            penalti_home = game['goals_scorers']['fouls']['penalti_home']
            penalti_away = game['goals_scorers']['fouls']['penalti_away']
            fourth_top_name=game['top_players_league']['top3']['fourth_top_name']
            fourth_top_team=game['top_players_league']['top3']['fourth_top_team']
            fourth_top_amount=game['top_players_league']['top3']['fourth_top_amount']
            fifth_top_name=game['top_players_league']['top3']['fifth_top_name']
            fifth_top_team=game['top_players_league']['top3']['fifth_top_team']
            fifth_top_amount=game['top_players_league']['top3']['fifth_top_amount']
            rank=game['goals_scorers']['table']['rank']
            rank = rank.split()
            all_games=game['goals_scorers']['table']['all_games']
            all_games = all_games.split()
            win_games=game['goals_scorers']['table']['win_games']
            win_games = win_games.split()
            draw_games=game['goals_scorers']['table']['draw_games']
            draw_games = draw_games.split()
            lose_games=game['goals_scorers']['table']['lose_games']
            lose_games = lose_games.split()
            goals_for=game['goals_scorers']['table']['goals_for']
            goals_for = goals_for.split()
            goals_missed=game['goals_scorers']['table']['goals_missed']
            goals_missed = goals_missed.split()
            goals_diff=game['goals_scorers']['table']['goals_diff']
            goals_diff = goals_diff.split()
            points=game['goals_scorers']['table']['points']
            points = points.split()
            name_teams=game['goals_scorers']['table']['name_teams']
            name_teams = name_teams.split()
            form_all=game['goals_scorers']['table']['form_all']
            form_all = form_all.split()
            logo_table=game['goals_scorers']['table']['logo_table']
            logo_table=''.join(logo_table)
            logo_table = logo_table.split()
            name_home_top_pass_accuracy = game['goals_scorers']['passes']['name_home_top_pass_accuracy']
            top__home_precent_accuracy = game['goals_scorers']['passes']['top__home_precent_accuracy']
            top__home_total_passes = game['goals_scorers']['passes']['top__home_total_passes']
            name_away_top_pass_accuracy = game['goals_scorers']['passes']['name_away_top_pass_accuracy']
            top__away_precent_accuracy = game['goals_scorers']['passes']['top__away_precent_accuracy']
            top__away_total_passes = game['goals_scorers']['passes']['top__away_total_passes']
            name_home_top_pass_key = game['goals_scorers']['passes']['name_home_top_pass_key']
            top__home_amount_key = game['goals_scorers']['passes']['top__home_amount_key']
            name_away_top_pass_key = game['goals_scorers']['passes']['name_away_top_pass_key']
            top__away_amount_key = game['goals_scorers']['passes']['top__away_amount_key']

            team1_next_match = datetime(int(next_match_team1_date[:4]), int(next_match_team1_date[5:7]), int(next_match_team1_date[8:10])).strftime('%A %B %d %Y')
            team2_next_match = datetime(int(next_match_team2_date[:4]), int(next_match_team2_date[5:7]), int(next_match_team2_date[8:10])).strftime('%A %B %d %Y')
            


            #logo_table = str(logo_table).replace("+", " ")
            # print(logo_table[0].replace("+", " "))

        
        yellow_card = f"<p><b>Желтые карточки: </b></p><p>{fouls_yel_team1} {fouls_yel_team2}</p>"
        #yellow_away = f"<p><b>Yellow cards: </b></p><p>{fouls_yel_team2}</p>"
        red_card = f"<p><b>Красные карточки: </b></p><p>{fouls_red_team1} {fouls_red_team2}</p>"
        #red_away = f"<p><b>Red cards: </b></p><p>{fouls_red_team2}</p>"

        if fouls_yel_team1 != '' or fouls_yel_team2 != '' or fouls_red_team1 != '' or fouls_red_team2 != '':
            title3 = f"<h4><b>Нарушения правил:</b></h4>"
            
            if fouls_yel_team1 != '' or fouls_yel_team2 != '':
                fouls_y_card = f'{yellow_card}'
            elif fouls_yel_team1 == '' and fouls_yel_team2 == '':
                fouls_y_card = ''

            # if fouls_yel_team2 != '':
            #     fouls_y_away = f"{yellow_home}"
            # elif fouls_yel_team2 == '':
            #     fouls_y_away = ''

            if fouls_red_team1 != '' or fouls_red_team2 != '':
                fouls_r_card = f"{red_card}"
            elif fouls_red_team1 == '' and fouls_red_team2 == '':
                fouls_r_card = ''

            # if fouls_red_team2 != '':
            #     fouls_r_away = f"{red_home}"
            # elif fouls_red_team2 == '':
            #     fouls_r_away = ''
            
            fouls = (
                f"{fouls_y_card}{fouls_r_card}"
            )
        else:
            fouls = f""
            title3 = ''
        # print(fouls)

        if penalti_home != '' or penalti_away != '':
            title2 = f"<h4><b>Пенальти в матче:</b></h4>"
            
            if penalti_home != '':
                penalti_home = f'{penalti_home}'
            elif penalti_home == '':
                penalti_home = ''

            if penalti_away != '':
                penalti_away = f"{penalti_away}"
            elif penalti_away == '':
                penalti_away = ''

            
            penalti = (
                f"{penalti_home}{penalti_away}"
            )
        else:
            penalti = ''
            title2 = ''



        if all_scorers != '':
            title1 = f'<h4><b>Авторы голов:</b></h4>'
            goals = f"<p>{all_scorers}</p>"
        else:
            title1 = ''
            goals = ''



        title = f'{team1} - {team2} {goals_a}:{goals_b}. Статистика матча'
        text = (
            f'<p><b>{team1} принимал {team2} на {arena}. {first_goal}</b></p>'
            #f'<h4>Final score of the match <b>{goals_a}:{goals_b}</b></h4>'
            f'{title1}'
                f'<ul>'
                    f'{goals}'
                f'</ul>'
            f'<h4><b>Составы команд:</b></h4>'
                f'{img_lineups}'
                f'<table align="center" border="1">'
                    f'<tr align="center" valign="center">'
                        f'<td>'
                            f'<p><b>{team1}</b><bot>'
                            f'<p>{lineups_a}</p></bot>'
                        f'</td>'
                        f'<td>'
                            f'<p><b>{team2}</b><bot>'
                            f'<p>{lineups_b}</p></bot>  '
                        f'</td>'
                f'</table>'
            f'<h4><b>Замены:</b></h4>'
                f'<table align="center" border="1">'
                    f'<tr align="center" valign="center">'
                        f'<td>'
                            f'<p><b>{team1}</b></p>'
                            f'<p>{lineups_in_game_a}<br></p>'
                        f'</td>'
                        f'<td>'
                            f'<p><b>{team2}</b></p>'
                            f'<p>{lineups_in_game_b}<br></p>'
                        f'</td>'
                f'</table>'
            
            f'<h4><b>Владение мячом:</b></h4>'
                f'<ul>'
                    f'<li>{team1} — {possession_team1}</li>'
                    f'<li>{team2} — {possession_team2}</li>'
                f'</ul>'
            f'<p>В общей сложности обе команды нанесли {total_shots_on} ударов в сторону ворот и {total_shots_off} в створ:</p>'  #TODO 
                f'<ul>'
                    f'<li><b>{team1}</b>: {shots_team1_on} ударов в сторону, {shots_team1_off} в створ. Самый активный по ударам —  {active_shots_player_home}.</li>'
                    f'<li><b>{team2}</b>: {shots_team2_on} в сторону, {shots_team2_off} в створ. Лучшим стал — {active_shots_player_away}.</li>'
                f'</ul>'
            #f'<p>{team1} had {total_assists_home} chances to score and {team2} had {total_assists_away}.</p>'
            f'{img_graph}'
            f'<h4><b>Передачи:</b></h4>'
                f'<p>Лучшие игроки команд по точности пасов:</p>'
                    f'<ul>'
                        f'<li>{name_home_top_pass_accuracy} ({team1}) — точность <b>{top__home_precent_accuracy}%</b>, всего пассов {top__home_total_passes}</li>'
                        f'<li>{name_away_top_pass_accuracy} ({team2}) — точность <b>{top__away_precent_accuracy}%</b>, всего пассов {top__away_total_passes}</li>'
                    f'</ul>'
                f'<p>Кто сделал больше всего ключевых передач:</p>'
                    f'<ul>'
                        f'<li>{name_home_top_pass_key} ({team1}) —  <b>{top__home_amount_key}</b></li>'
                        f'<li>{name_away_top_pass_key} ({team2}) —  <b>{top__away_amount_key}</b></li>'
                    f'</ul>'
            f'<h4><b>Защита:</b></h4>'
                f'<ul>'
                    f'<li><b>Перехваты</b>. Количество перехватов у {team1} — {total_interceptions_home} (лидер  — {name_top_inceptions_home}, {amount_interceptions_home}). {team2} — {total_inteceptions_away} ({name_top_inceptions_away} сделал больше всего, {amount_interseptions_away}). </li>'
                    f'<li><b>Подкаты</b>. {team1} — {total_blocks_home} ({name_top_blocks_home}, {amount_blocks_home}). {team2} — {total_blocks_away}  ({name_top_blocks_away} — {amount_blocks_away}).</li>'
                f'</ul>'
            f'<h4><b>Единоборства:</b></h4>'
                f'<p>Лидеры команд по количеству единоборств:</p>'
                f'<ul>'
                    f'<li>{name_duels_team1}, {team1} ({amount_duels_team1})</li>'
                    f'<li>{name_duels_team2}, {team2} ({amount_duels_team2})</li>'
                f'</ul>  '
            f'{title3}'
                f'<ul>'
                    f'{fouls}'
                f'</ul>'
            f'{title2}'
                f'<ul>'   
                    f'{penalti}'
                f'</ul>'    
            f'<h4><b>Последние 5 игр команд (исключая этот матч):</b></h4>'
            f'<ul>'
                    f'<li>{team1} - {form_home}</li>'
                    f'<li>{team2} - {form_away}</li>'
            f'</ul>'
            # f'<h4><b>В {league_name1} таблица прямо сейчас:</b></h4><h4>'
            # f'<table >'
            #     f'<tbody>'
                    
            #         f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
            #             f'<td>#</td>'
            #             f'<td><b>Команды</b></td>'
            #             f'<td><b>Form</b></td>'
            #             f'<td>PL</td>'
            #             f'<td style= "background-color: #4a9460;">W</td>'
            #             f'<td>D</td>' #style= "background-color: #9f9c98;"
            #             f'<td style= "background-color: #a13c3c;">L</td>'
            #             f'<td>GF</td>'
            #             f'<td>GA</td>'
            #             f'<td>GD</td>'
            #             f'<td>Pts</td>'
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[0]}'
            #             f'<td>'
            #                 f'{logo_table[0].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[0]}'
            #             f'{all_games[0]}'
            #             f'{win_games[0]}'
            #             f'{draw_games[0]}'
            #             f'{lose_games[0]}'
            #             f'{goals_for[0]}'
            #             f'{goals_missed[0]}'
            #             f'{goals_diff[0]}'
            #             f'{points[0]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[1]}'
            #             f'<td>'
            #                 f'{logo_table[1].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[1]}'
            #             f'{all_games[1]}'
            #             f'{win_games[1]}'
            #             f'{draw_games[1]}'
            #             f'{lose_games[1]}'
            #             f'{goals_for[1]}'
            #             f'{goals_missed[1]}'
            #             f'{goals_diff[1]}'
            #             f'{points[1]}'        
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[2]}'     
            #             f'<td>'
            #                 f'{logo_table[2].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[2]}'
            #             f'{all_games[2]}'
            #             f'{win_games[2]}'
            #             f'{draw_games[2]}'
            #             f'{lose_games[2]}'
            #             f'{goals_for[2]}'
            #             f'{goals_missed[2]}'
            #             f'{goals_diff[2]}'
            #             f'{points[2]}'   
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[3]}'      
            #             f'<td>'
            #                 f'{logo_table[3].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[3]}'
            #             f'{all_games[3]}'
            #             f'{win_games[3]}'
            #             f'{draw_games[3]}'
            #             f'{lose_games[3]}'
            #             f'{goals_for[3]}'
            #             f'{goals_missed[3]}'
            #             f'{goals_diff[3]}'
            #             f'{points[3]}'           
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[4]}'
            #             f'<td>'
            #                 f'{logo_table[4].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[4]}'
            #             f'{all_games[4]}'
            #             f'{win_games[4]}'
            #             f'{draw_games[4]}'
            #             f'{lose_games[4]}'
            #             f'{goals_for[4]}'
            #             f'{goals_missed[4]}'
            #             f'{goals_diff[4]}'
            #             f'{points[4]}'                
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[5]}'                
            #             f'<td>'
            #                 f'{logo_table[5].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[5]}'
            #             f'{all_games[5]}'
            #             f'{win_games[5]}'
            #             f'{draw_games[5]}'
            #             f'{lose_games[5]}'
            #             f'{goals_for[5]}'
            #             f'{goals_missed[5]}'
            #             f'{goals_diff[5]}'
            #             f'{points[5]}'                       
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[6]}'               
            #             f'<td>'
            #                 f'{logo_table[6].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[6]}'
            #             f'{all_games[6]}'
            #             f'{win_games[6]}'
            #             f'{draw_games[6]}'
            #             f'{lose_games[6]}'
            #             f'{goals_for[6]}'
            #             f'{goals_missed[6]}'
            #             f'{goals_diff[6]}'
            #             f'{points[6]}'              
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[7]}'        
            #             f'<td>'
            #                 f'{logo_table[7].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[7]}'
            #             f'{all_games[7]}'
            #             f'{win_games[7]}'
            #             f'{draw_games[7]}'
            #             f'{lose_games[7]}'
            #             f'{goals_for[7]}'
            #             f'{goals_missed[7]}'
            #             f'{goals_diff[7]}'
            #             f'{points[7]}'                       
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[8]}'               
            #             f'<td>'
            #                 f'{logo_table[8].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[8]}'
            #             f'{all_games[8]}'
            #             f'{win_games[8]}'
            #             f'{draw_games[8]}'
            #             f'{lose_games[8]}'
            #             f'{goals_for[8]}'
            #             f'{goals_missed[8]}'
            #             f'{goals_diff[8]}'
            #             f'{points[8]}'   
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[9]}'
            #             f'<td>'
            #                 f'{logo_table[9].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[9]}'
            #             f'{all_games[9]}'
            #             f'{win_games[9]}'
            #             f'{draw_games[9]}'
            #             f'{lose_games[9]}'
            #             f'{goals_for[9]}'
            #             f'{goals_missed[9]}'
            #             f'{goals_diff[9]}'
            #             f'{points[9]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[10]}'
            #             f'<td>'
            #                 f'{logo_table[10].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[10]}'
            #             f'{all_games[10]}'
            #             f'{win_games[10]}'
            #             f'{draw_games[10]}'
            #             f'{lose_games[10]}'
            #             f'{goals_for[10]}'
            #             f'{goals_missed[10]}'
            #             f'{goals_diff[10]}'
            #             f'{points[10]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[11]}'
            #             f'<td>'
            #                 f'{logo_table[11].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[11]}'
            #             f'{all_games[11]}'
            #             f'{win_games[11]}'
            #             f'{draw_games[11]}'
            #             f'{lose_games[11]}'
            #             f'{goals_for[11]}'
            #             f'{goals_missed[11]}'
            #             f'{goals_diff[11]}'
            #             f'{points[11]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[12]}'
            #             f'<td>'
            #                 f'{logo_table[12].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[12]}'
            #             f'{all_games[12]}'
            #             f'{win_games[12]}'
            #             f'{draw_games[12]}'
            #             f'{lose_games[12]}'
            #             f'{goals_for[12]}'
            #             f'{goals_missed[12]}'
            #             f'{goals_diff[12]}'
            #             f'{points[12]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[13]}'
            #             f'<td>'
            #                 f'{logo_table[13].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[13]}'
            #             f'{all_games[13]}'
            #             f'{win_games[13]}'
            #             f'{draw_games[13]}'
            #             f'{lose_games[13]}'
            #             f'{goals_for[13]}'
            #             f'{goals_missed[13]}'
            #             f'{goals_diff[13]}'
            #             f'{points[13]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[14]}'
            #             f'<td>'
            #                 f'{logo_table[14].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[14]}'
            #             f'{all_games[14]}'
            #             f'{win_games[14]}'
            #             f'{draw_games[14]}'
            #             f'{lose_games[14]}'
            #             f'{goals_for[14]}'
            #             f'{goals_missed[14]}'
            #             f'{goals_diff[14]}'
            #             f'{points[14]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[15]}'
            #             f'<td>'
            #                 f'{logo_table[15].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[15]}'
            #             f'{all_games[15]}'
            #             f'{win_games[15]}'
            #             f'{draw_games[15]}'
            #             f'{lose_games[15]}'
            #             f'{goals_for[15]}'
            #             f'{goals_missed[15]}'
            #             f'{goals_diff[15]}'
            #             f'{points[15]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[16]}'
            #             f'<td>'
            #                 f'{logo_table[16].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[16]}'
            #             f'{all_games[16]}'
            #             f'{win_games[16]}'
            #             f'{draw_games[16]}'
            #             f'{lose_games[16]}'
            #             f'{goals_for[16]}'
            #             f'{goals_missed[16]}'
            #             f'{goals_diff[16]}'
            #             f'{points[16]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[17]}'
            #             f'<td>'
            #                 f'{logo_table[17].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[17]}'
            #             f'{all_games[17]}'
            #             f'{win_games[17]}'
            #             f'{draw_games[17]}'
            #             f'{lose_games[17]}'
            #             f'{goals_for[17]}'
            #             f'{goals_missed[17]}'
            #             f'{goals_diff[17]}'
            #             f'{points[17]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[18]}'
            #             f'<td>'
            #                 f'{logo_table[18].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[18]}'
            #             f'{all_games[18]}'
            #             f'{win_games[18]}'
            #             f'{draw_games[18]}'
            #             f'{lose_games[18]}'
            #             f'{goals_for[18]}'
            #             f'{goals_missed[18]}'
            #             f'{goals_diff[18]}'
            #             f'{points[18]}'      
            #         f'</tr>'
            #         f'<tr align="centre" valign="top">'
            #             f'{rank[19]}'
            #             f'<td>'
            #                 f'{logo_table[19].replace("+", " ")}'
            #             f'</td>'
            #             f'{form_all[19]}'
            #             f'{all_games[19]}'
            #             f'{win_games[19]}'
            #             f'{draw_games[19]}'
            #             f'{lose_games[19]}'
            #             f'{goals_for[19]}'
            #             f'{goals_missed[19]}'
            #             f'{goals_diff[19]}'
            #             f'{points[19]}'      
            #         f'</tr>'
            #         f'</tbody>'
            #     f'</table>'
                    
            f'<h4><b>Топ 5 лидеров бомбардиров {league_name1}:</b></h4>'
                f'<ol>'
                    f'<li>{first_top_name} ({first_top_amount}, {first_top_team})</li>'
                    f'<li>{second_top_name} ({second_top_amount}, {second_top_team})</li>'
                    f'<li>{third_top_name} ({third_top_amount}, {third_top_team})</li>'
                    f'<li>{fourth_top_name} ({fourth_top_amount}, {fourth_top_team})</li>'
                    f'<li>{fifth_top_name} ({fifth_top_amount}, {fifth_top_team})</li>'
                f'</ol>'
            f'<h4><b>Следующие матчи команд:</b></h4>'
                f'<ul>'
                    f'<li><b>{team1}</b> сыграет с {next_match_team1_with}. {team1_next_match}, на {next_match_team1_venue}. </li>'
                    f'<li><b>{team2}</b> будет играть с {next_match_team2_with}. {team2_next_match}, на {next_match_team2_venue}. </li>'
                f'</ul>'
        )
        
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:00")
        # print(date)

    elif types == 'preview':
            # preview
        img_graph_preview_home = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/graph_home_{fixture_match}_{types}.png\" alt=\"\">"
        img_graph_preview_away = f"<img src=\"https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/graph_away_{fixture_match}_{types}.png\" alt=\"\">"

        # Type == Preview
        for game in text: 
            team1 = game['title1']['team_name_home']
            team2 = game['title1']['team_name_away']
            date1 = game['subtitle_start']['date']
            full_date = game['subtitle_start']['full_date']
            venue1 = game['subtitle_start']['venue']
            league_name1 = game['standings']['league_name']
            rank1 = game['standings']['rank_team_home']
            rank2 = game['standings']['rank_team_away']
            top_player_a = game['scorers_a_b']['home_top_name']
            top_home_total = game['scorers_a_b']['home_top_total']
            top_player_b = game['scorers_a_b']['away_top_name']
            top_away_total = game['scorers_a_b']['away_top_total']
            first_in_league_name = game['table_scorers']['first_top_name']
            first_in_league_team = game['table_scorers']['first_top_team']
            first_in_league_amount = game['table_scorers']['first_top_amount']
            second_in_league_name = game['table_scorers']['second_top_name']
            second_in_league_team = game['table_scorers']['second_top_team']
            second_in_league_amount = game['table_scorers']['second_top_amount']
            thrid_in_league_name = game['table_scorers']['third_top_name']
            thrid_in_league_team = game['table_scorers']['third_top_team']
            thrid_in_league_amount = game['table_scorers']['third_top_amount']
            fourth_in_league_name = game['table_scorers']['fourth_top_name']
            fourth_in_league_team = game['table_scorers']['fourth_top_team']
            fourth_in_league_amount = game['table_scorers']['fourth_top_amount']
            fifth_in_league_name = game['table_scorers']['fifth_top_name']
            fifth_in_league_team = game['table_scorers']['fifth_top_team']
            fifth_in_league_amount = game['table_scorers']['fifth_top_amount']
            top_home_assist_name = game['assists']['topscorers_assists_home_name']
            top_home_assist_amount = game['assists']['topscorers_assists_home_amount']
            top_away_assist_name = game['assists']['topscorers_assists_away_name']
            top_away_assist_amount = game['assists']['topscorers_assists_away_amount']
            top_home_saves_name = game['saves']['topscorers_saves_home_name']
            top_home_saves_amount = game['saves']['topscorers_saves_home_amount']
            top_away_saves_name = game['saves']['topscorers_saves_away_name']
            top_away_saves_amount = game['saves']['topscorers_saves_away_amount']
            top_home_blocks_name = game['blocks']['topscorers_interceptions_home_name']
            top_home_blocks_amount = game['blocks']['topscorers_interceptions_home_amount']
            top_away_blocks_name = game['blocks']['topscorers_interceptions_away_name']
            top_away_blocks_amount = game['blocks']['topscorers_interceptions_away_amount']
            top_home_duels_name = game['duels']['topscorers_duels_home_name']
            top_home_duels_amount = game['duels']['topscorers_duels_home_amount']
            top_away_duels_name = game['duels']['topscorers_duels_away_name']
            top_away_duels_amount = game['duels']['topscorers_duels_away_amount']

            name_home_top_fouls_yel_card = game['fouls']['name_home_top_fouls_yel_card']
            amount_home_fouls_yel_card = game['fouls']['amount_home_fouls_yel_card']
            name_away_top_fouls_yel_card = game['fouls']['name_away_top_fouls_yel_card']
            amount_away_fouls_yel_card = game['fouls']['amount_away_fouls_yel_card']
            name_home_top_fouls_red_card = game['fouls']['name_home_top_fouls_red_card']
            amount_home_fouls_red_card = game['fouls']['amount_home_fouls_red_card']
            name_away_top_fouls_red_card = game['fouls']['name_away_top_fouls_red_card']
            amount_away_fouls_red_card = game['fouls']['amount_away_fouls_red_card']

            home_forms = game['team_statistics']['forms']['home']
            away_forms = game['team_statistics']['forms']['away']
            clean_home = game['clean_sheet']['home_play_clean_sheet']
            clean_away = game['clean_sheet']['away_play_clean_sheet']
            home_biggest_win_in_home = game['biggest']['home']['win']['home']
            home_biggest_win_in_away = game['biggest']['home']['win']['away']
            home_biggest_lose_in_home = game['biggest']['lose']['home']
            home_biggest_lose_in_away = game['biggest']['lose']['away']
            away_biggest_win_in_home = game['away']['win']['home']
            away_biggest_win_in_away = game['away']['win']['away']
            away_biggest_lose_in_home = game['away']['lose']['home']
            away_biggest_lose_in_away = game['away']['lose']['away']
            home_win_once_in_home = game['win_once']['home']['win']
            home_draws_once_in_home = game['win_once']['home']['draws']
            home_lose_once_in_home = game['win_once']['home']['lose']
            away_win_once_in_away = game['win_once']['away']['win']
            away_draws_once_in_away = game['win_once']['away']['draws']
            away_lose_once_in_away = game['win_once']['away']['lose']
            for_goals_home = game['goals']['home']['g'].split()
            missed_goals_home = game['goals']['home']['m'].split()
            for_goals_away = game['goals']['away']['g'].split()
            missed_goals_away = game['goals']['away']['m'].split()
            list_minute = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
            table_h2h_total_game = game['Table_h2h']['games']
            home_table_h2h_win_in_home = game['Table_h2h']['team_home']['win_home']
            home_table_h2h_win_in_away = game['Table_h2h']['team_home']['win_away']
            home_table_h2h_draws_in_home = game['Table_h2h']['team_home']['draws_home']
            home_table_h2h_draws_in_away = game['Table_h2h']['team_home']['draws_away']
            home_table_h2h_lose_in_home = game['Table_h2h']['team_home']['loses_home']
            home_table_h2h_lose_in_away = game['Table_h2h']['team_home']['loses_away']
            away_table_h2h_win_in_home = game['Table_h2h']['team_away']['win_home']
            away_table_h2h_win_in_away = game['Table_h2h']['team_away']['win_away']
            away_table_h2h_draws_in_home = game['Table_h2h']['team_away']['draws_home']
            away_table_h2h_draws_in_away = game['Table_h2h']['team_away']['draws_away']
            away_table_h2h_lose_in_home = game['Table_h2h']['team_away']['loses_home']
            away_table_h2h_lose_in_away = game['Table_h2h']['team_away']['loses_away']
            home_comparison_win = game['Сomparison']['table']['team_home']['win']
            home_comparison_att = game['Сomparison']['table']['team_home']['attack']
            home_comparison_def = game['Сomparison']['table']['team_home']['def']
            home_comparison_t2t = game['Сomparison']['table']['team_home']['t2t']
            home_comparison_goals = game['Сomparison']['table']['team_home']['goals']
            away_comparison_win = game['Сomparison']['table']['team_away']['win']
            away_comparison_att = game['Сomparison']['table']['team_away']['attack']
            away_comparison_def = game['Сomparison']['table']['team_away']['def']
            away_comparison_t2t = game['Сomparison']['table']['team_away']['t2t']
            away_comparison_goals = game['Сomparison']['table']['team_away']['goals']
            predictions_win_home = game['subtitle']['predictions_win_home']
            predictions_draws = game['subtitle']['predictions_draws']
            predictions_lose_home = game['subtitle']['predictions_win_away']
            home_win_or_lose = game['subtitle']['predictions_home_win_or_lose']
            home_predictions_goals = game['subtitle']['predictions_home_goals']
            away_predictions_goals = game['subtitle']['predictions_away_goals']
            bk1_name = game['bk']['table']['bk1']
            bk1_win_home = game['bk']['table']['bk1_win_home']
            bk1_draw = game['bk']['table']['bk1_draw']
            bk1_win_away = game['bk']['table']['bk1_win_away']
            bk2_name = game['bk']['table']['bk2']
            bk2_win_home = game['bk']['table']['bk2_win_home']
            bk2_draw = game['bk']['table']['bk2_draw']
            bk2_win_away = game['bk']['table']['bk2_win_away']
            bk3_name = game['bk']['table']['bk3']
            bk3_win_home = game['bk']['table']['bk3_win_home']
            bk3_draw = game['bk']['table']['bk3_draw']
            bk3_win_away = game['bk']['table']['bk3_win_away']
            
        if str(home_biggest_win_in_home) == '0':
            title_big_home_in_home = ''
        else:
            title_big_home_in_home = f'в домашних матчах - <b>{home_biggest_win_in_home}</b>,'

        if str(home_biggest_win_in_home) == '0':
            title_big_home_in_away = ''
        else:
            title_big_home_in_away = f'на выезде — <b>{home_biggest_win_in_away}</b>'
        
        if str(away_biggest_win_in_home) == '0':
            title_big_away_in_home = ''
        else:
            title_big_away_in_home = f', самая крупная победа дома была - {away_biggest_win_in_home}'
        
        if str(away_biggest_win_in_away) == '0':
            title_big_home_in_away = ''
        else:
            title_big_home_in_away = f', а крупнейшая гостевая победа в текущем сезоне - <b>{away_biggest_win_in_away}</b>.'
            
        date = datetime.strptime(full_date, "%Y-%m-%dT%H:%M")  
        date = date - timedelta(days=1) 
        new_date = datetime(int(full_date[:4]), int(full_date[5:7]), int(full_date[8:10])).strftime('%A %B %d %Y')
        new_date = new_date.split()
        # print(new_date[1])
        # print(new_date[2])

        title = f'\n{team1} — {team2}. Основные расклады перед ближайшим матчем команд'
        text = (
        f'<p><b>{new_date[1]} {new_date[2]} {team1} сыграет  {team2} на {venue1}. Вот самая интересная информация о соперниках.</b></p>'
            f'<p>В этом сезоне <b>{team1}</b> в {league_name1} занимает  <b>{rank1}</b> место, его соперник — на <b>{rank2}</b> место.</p>'
            f'<p><h3><strong>Top 5 бомбардиров этого сезона:</strong></h3></p>'
                f'<ol>'
                    f'<li><b>{first_in_league_name}</b> (<b>{first_in_league_amount}</b>, {first_in_league_team})</li>'
                    f'<li><b>{second_in_league_name}</b> (<b>{second_in_league_amount}</b>, {second_in_league_team})</li>'
                    f'<li><b>{thrid_in_league_name}</b> (<b>{thrid_in_league_amount}</b>, {thrid_in_league_team})</li>'
                    f'<li><b>{fourth_in_league_name}</b> (<b>{fourth_in_league_amount}</b>, {fourth_in_league_team})</li>'
                    f'<li><b>{fifth_in_league_name}</b> (<b>{fifth_in_league_amount}</b>, {fifth_in_league_team})</li>'
                f'</ol>'
            f'<h3><strong>Статистика по лучшим игрокам обеих команд:</strong></h3>'
                f'<p>Больше всего голов за <b>{team1}</b>: <b>{top_player_a}</b> ({top_home_total}), за <b>{team2}</b> — <b>{top_player_b}</b> ({top_away_total}).</p>'
                
            f'<p>Ключевые статистистические показатели игроков:</p>'
            f'<ul>'
                f'<li><b>Голевые передачи:</b> {top_home_assist_name} ({team1}) — <b>{top_home_assist_amount}</b> assists,  {top_away_assist_name} ({team2}) — <b>{top_away_assist_amount}</b> assists.</li>'
                f'<li><b>Сейвы голкиперов команд:</b> {top_home_saves_name} ({team1}) — <b>{top_home_saves_amount}</b>, {top_away_saves_name} ({team2}) — <b>{top_away_saves_amount}</b>.</li>'
                f'<li><b>Подкасты:</b> {top_home_blocks_name} ({team1}) — <b>{top_home_blocks_amount}</b>, {top_away_blocks_name} ({team2}) — <b>{top_away_blocks_amount}</b>.</li>'
                f'<li><b>Выигранные противоборства:</b> {top_home_duels_name} ({team1}) — <b>{top_home_duels_amount}</b>, {top_away_duels_name} ({team2}) — <b>{top_away_duels_amount}</b>.</li>'
                f'<li><b>Желтые карточки:</b> {name_home_top_fouls_yel_card} ({team1}) — <b>{amount_home_fouls_yel_card}</b>, {name_away_top_fouls_yel_card} ({team2}) — <b>{amount_away_fouls_yel_card}</b>.</li>'
                f'<li><b>Красные карточки:</b> {name_home_top_fouls_red_card} ({team1}) — <b>{amount_home_fouls_red_card}</b>, {name_away_top_fouls_red_card} ({team2}) — <b>{amount_away_fouls_red_card}</b>.</li>'
            f'</ul>'
            f'<h3><strong>Командная статистика:</strong></h3>'
            f'<p>Результаты пяти предыдущих игр обеих команд:</p>'
            f'<ul>'
                f'<li>{team1} — <b>{home_forms}</b></li>'
                f'<li>{team2} — <b>{away_forms}</b></li>'
            f'</ul>'
            f'<p>В этом сезоне <b>{team1}</b> сыграл <b>{clean_home}</b> матча, в которых не смог забить ни одного гола. <b>{team2}</b> не пропускала в <b>{clean_away}</b> матчах за сезон.</p>'
            f'<p>Самый крупный счёт у <b>{team1}</b> {title_big_home_in_home} {title_big_home_in_away}. Количество крупных поражений дома — <b>{home_biggest_lose_in_home}</b>, в гостевых матчах — <b>{home_biggest_lose_in_away}</b>.</p>' 
            f'<p>У <b>{team2}</b> {title_big_away_in_home} {title_big_home_in_away} Самое крупное поражение дома — <b>{away_biggest_lose_in_home}</b>, на выезде — <b>{away_biggest_lose_in_away}</b>.</p>'
            f'<p><b>{team1}</b> этом сезоне дома выступает так: победы — <b>{home_win_once_in_home}</b>, ничьи — <b>{home_draws_once_in_home}</b>, проигрыши — <b>{home_lose_once_in_home}</b>. <b>{team2}</b> в гостях: победы — <b>{away_win_once_in_away}</b>, ничьи — <b>{away_draws_once_in_away}</b>, поражения — <b>{away_lose_once_in_away}</b>.</p>'
            f'<p>Согласно статистике домашних матчей, распределение забитых и пропущенных мячей по двум таймам у {team1} выглядит следующим образом: </p>'
            f'<table align="center" border="1">'
                        f'<tbody>'
                        f'<tr align="center" valign="center">'
                            f'<td style= "background-color: #e0d3d3;"><b>Intervals</b></td>'
                            f'<td style= "background-color: #b1e0b8;"><b>Goal Scored, %</b></td>'
                            f'<td style= "background-color: #ebc996;"><b>Goals conceded, %</b></td>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[0]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[0]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[0]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[1]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[1]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[1]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[2]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[2]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[2]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[3]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[3]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[3]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[4]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[4]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[4]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[5]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[5]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[5]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[6]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_home[6]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_home[6]}</td>'
                        f'</tr>' 
                        f'</tbody>'
                    f'</table>'
            f'<p>У {team2} временные интервалы двух таймов по забитым и пропущенным голам — такие: </p>'
            f'<table align="center" border="1">'
                        f'<tbody>'
                        f'<tr align="center" valign="center">'
                            f'<td style= "background-color: #e0d3d3;"><b>Intervals</b></td>'
                            f'<td style= "background-color: #b1e0b8;"><b>Goal Scored, %</b></td>'
                            f'<td style= "background-color: #ebc996;"><b>Goals conceded, %</b></td>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[0]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[0]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[0]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[1]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[1]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[1]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[2]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[2]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[2]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[3]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[3]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[3]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[4]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[4]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[4]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[5]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[5]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[5]}</td>'
                        f'</tr>'
                        f'</tr>'
                            f'<tr><td style= "background-color: #e0d3d3;">{list_minute[6]}</td>'
                            f'<td style= "background-color: #b1e0b8;">{for_goals_away[6]}</td>'
                            f'<td style= "background-color: #ebc996;">{missed_goals_away[6]}</td>'
                        f'</tr>'  
                        f'</tbody>'
                    f'</table>'       
            f'<h3><strong>Очная статистика:</strong></h3>'
            f'<table align="center" border="1">'
                f'<tbody>'
                    f'<tr align="center" valign="center">'
                        f'<td rowspan="2"><b>Команда</b></td>'
                        f'<td rowspan="2"><b>Игры</b></td>'
                        f'<td colspan="2"><b>Выигрыш</b></td>'
                        f'<td colspan="2"><b>Ничьи</b></td>'
                        f'<td colspan="2"><b>Поражения</b></td>'
                    f'</tr>'
                    f'<tr align="center" valign="center">'
                        f'<td>H</td>'
                        f'<td>A</td>'
                        f'<td>H</td>'
                        f'<td>A</td>'
                        f'<td>H</td>'
                        f'<td>A</td>'
                    f'</tr>'
                    f'<tr align="center" valign="center">'
                        f'<td><b>{team1}</b></td>'
                        f'<td rowspan="2" valign="center">{table_h2h_total_game}</td>'
                        f'<td>{home_table_h2h_win_in_home}</td>'
                        f'<td>{home_table_h2h_win_in_away}</td>'
                        f'<td>{home_table_h2h_draws_in_home}</td>'
                        f'<td>{home_table_h2h_draws_in_away}</td>'
                        f'<td>{home_table_h2h_lose_in_home}</td>'
                        f'<td>{home_table_h2h_lose_in_away}</td>'
                    f'</tr>'
                    f'<tr align="center" valign="center">'
                        f'<td><b>{team2}</b></td>'
                        f'<td>{away_table_h2h_win_in_home}</td>'
                        f'<td>{away_table_h2h_win_in_away}</td>'
                        f'<td>{away_table_h2h_draws_in_home}</td>'
                        f'<td>{away_table_h2h_draws_in_away}</td>'
                        f'<td>{away_table_h2h_lose_in_home}</td>'
                        f'<td>{away_table_h2h_lose_in_away}</td>'
                    f'</tr>'
                f'</tbody>'
            f'</table>'
            f'<h3><strong>Вероятностные характеристики перед матчем:</strong></h3>'
            f'<table align="center" border="1">'
                f'<tbody>'
                f'<tr align="center" valign="center">'
                    f'<td><b>{team1}</b></td>'
                    f'<td></td>'
                    f'<td><b>{team2}</b></td>'
                f'</tr>'
                    f'<tr><td>{home_comparison_win}</td>'
                    f'<td>Выигрыш игры</td><td>{away_comparison_win}</td></tr>'
                    f'<tr><td>{home_comparison_att}</td><td>Потенциал в атаке</td>'
                    f'<td>{away_comparison_att}</td></tr><tr><td>{home_comparison_def}</td>'
                    f'<td>Потенциал в защите</td><td>{away_comparison_def}</td></tr>'
                    f'<tr><td>{home_comparison_t2t}</td><td>Сила друг против друга</td>'
                    f'<td>{away_comparison_t2t}</td></tr>' #f'<td>{away_comparison_t2t}</td></tr><tr><td>{home_comparison_goals}</td>'
                    #f'<td>Потенциал голов</td><td>{away_comparison_goals}</td></tr>'
                f'</tbody>'
            f'</table>'
            f'<p><b>Вывод:</b> вероятность победы <b>{team2}</b> – <b>{predictions_lose_home}</b>, ничьи – <b>{predictions_draws}</b>, поражения – <b>{predictions_win_home}</b>. Таким образом, <b>{team1}</b>, скорее всего, {home_win_or_lose}</p>'
            f'<p><b>Прогноз по голам:</b> <b>{team1}</b>, вероятно, забьет не больше {home_predictions_goals}, <b>{team2}</b> — не больше {away_predictions_goals}.</p>'
            f'<p><b>Лучшие коэффициенты букмекеров на этот матч:</b></p>'
            f'<table align="center" border="1">'
                f'<tbody>'
                    f'<tr align="center" valign="top">'
                        f'<td><b>Победа хозяев</b></td>'
                        f'<td><b>Ничья</b></td>'
                        f'<td><b>Победа гостей</b></td></tr>'
                    f'<tr align="center" valign="top">'
                        f'<td>{bk1_name}<br>{bk1_win_home}</td>'
                        f'<td>{bk2_name}<br>{bk2_draw}</td>'
                        f'<td>{bk3_name}<br>{bk3_win_away}</td>'
                    f'</tr>'
                f'</tbody>'
            f'</table>'
            f'<h3><strong>Не пропустите</strong></h3>'
            f'<p>Матч между командами <b>{team1}</b> и <b>{team2}</b> состоится <b>{new_date[1]} {new_date[2]} {full_date[11:]}</b> на {venue1}.</p>'
        )

                

    
    # JSON вариант всех команд Лиг
    data_tags = {
            "English Premier League": {
                "id":"3",
                "Manchester City":"8",
                "Liverpool":"11"
                },
            "La Liga" : {
                "id":"4",
                "Barcelona":"12", 
                "Real Madrid":"13"
                },
            "Ligue 1" : {
                "id":"7",
                "PSG":"14", 
                "Marseille":"15"
                },
            "Serie A" :{
                "id":"5",
                "Napoli":"16", 
                "Atalanta":"17"
                },
            "Bundesliga" : {
                "id":"6",
                "Union Berlin":"18", 
                "Freiburg":"19"
                }
    }
    

    # Список всех команд
    l = ['Manchester City', 'Liverpool','Barcelona', 'Real Madrid','PSG', 'Marseille','Napoli', 'Atalanta','Union Berlin', 'Freiburg']

    category = data_tags[league_name1]['id']

    team1_tags = ""
    team2_tags = ""
    
    # получение id команд тега 
    if team1 in l:
        team1_tags = data_tags[league_name1][team1]
    if team2 in l:
        team2_tags = data_tags[league_name1][team2]
    
    # Создания тега
    if team1_tags != "" and team2_tags != "":
        tags = f"{team1_tags}, {team1_tags}"
    elif team1_tags != "":
        tags = team1_tags
    elif team2_tags != "":
        tags = team2_tags
    else:
        tags = ""
    
    url = 'https://botbot.news/wp-json/wp/v2/posts'
    user = 'botbot'
    password = 'cGvj MT0x lqRl cEuY tddX huHk'

    credentials = user + ':' + password

    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    
    post = {
    'title'    : title,
    'status'   : 'publish', #тип
    'content'  : text,
    'categories': category, # category ID
    'tags'       : tags,
    'date'   : f'{date}',   # время публикации --  {время матча - один день} 
    'meta' : { '_knawatfibu_url': featured_image_url }    
    }
    if team1 in l or team2 in l:
        responce = requests.post(url , headers=header, json=post)
        # print(responce.text)
    else:
        pass
    # '2022-09-30T8:00:00'

# main_publication_ru('867961', 'review')