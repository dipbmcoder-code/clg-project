        #     f'<p><b>{team1} hosted {team2} at the {arena}. {first_goal}</b></p>'
        #     #f'<h4>Final score of the match <b>{goals_a}:{goals_b}</b></h4>'
        #     f'{title1}'
        #         f'<ul>'
        #             f'{goals}'
        #         f'</ul>'
        #     f'<h4><b>Line-ups:</b></h4>'
        #         f'{img_lineups}'
        #         f'<table align="center" border="1">'
        #             f'<tr align="center" valign="center">'
        #                 f'<td>'
        #                     f'<p><b>{team1}</b><bot>'
        #                     f'<p>{lineups_a}</p></bot>'
        #                 f'</td>'
        #                 f'<td>'
        #                     f'<p><b>{team2}</b><bot>'
        #                     f'<p>{lineups_b}</p></bot>  '
        #                 f'</td>'
        #         f'</table>'
        #     f'<h4><b>Substitutions:</b></h4>'
        #         f'<table align="center" border="1">'
        #             f'<tr align="center" valign="center">'
        #                 f'<td>'
        #                     f'<p><b>{team1}</b></p>'
        #                     f'<p>{lineups_in_game_a}<br></p>'
        #                 f'</td>'
        #                 f'<td>'
        #                     f'<p><b>{team2}</b></p>'
        #                     f'<p>{lineups_in_game_b}<br></p>'
        #                 f'</td>'
        #         f'</table>'
            
        #     f'<h4><b>Ball possession:</b></h4>'
        #         f'<ul>'
        #             f'<li>{team1} — {possession_team1}</li>'
        #             f'<li>{team2} — {possession_team2}</li>'
        #         f'</ul>'
        #     f'<p>In total two teams made {total_shots_off} shots on target and shot {total_shots_on} on goal:</p>'  #TODO 
        #         f'<ul>'
        #             f'<li><b>{team1}</b>: {shots_team1_off} shots on target, {shots_team1_on}  on goal. The most active in terms of the number of shots was — {active_shots_player_home}.</li>'
        #             f'<li><b>{team2}</b>: {shots_team2_off} shots on target, {shots_team2_on} on goal. Best in hits on goal - {active_shots_player_away}.</li>'
        #         f'</ul>'
        #     #f'<p>{team1} had {total_assists_home} chances to score and {team2} had {total_assists_away}.</p>'
        #     f'{img_graph}'
        #     f'<h4><b>Passes:</b></h4>'
        #         f'<p>Best players for each teams with pass accuracy:</p>'
        #             f'<ul>'
        #                 f'<li>{name_home_top_pass_accuracy} ({team1}) — pass accuracy <b>{top__home_precent_accuracy}%</b>, total passes {top__home_total_passes}</li>'
        #                 f'<li>{name_away_top_pass_accuracy} ({team2}) — pass accuracy <b>{top__away_precent_accuracy}%</b>, total passes {top__away_total_passes}</li>'
        #             f'</ul>'
        #         f'<p>Who made the most key passes from each teams:</p>'
        #             f'<ul>'
        #                 f'<li>{name_home_top_pass_key} ({team1}) — <b>{top__home_amount_key} key passes</b></li>'
        #                 f'<li>{name_away_top_pass_key} ({team2}) — <b>{top__away_amount_key} key passes</b></li>'
        #             f'</ul>'
        #     f'<h4><b>Defense:</b></h4>'
        #         f'<ul>'
        #             f'<li><b>Intercepts</b>. Number of interceptions for {team1} — {total_interceptions_home} (leader  — {name_top_inceptions_home}, {amount_interceptions_home}). {team2} — {total_inteceptions_away} ({name_top_inceptions_away} has the most, {amount_interseptions_away}). </li>'
        #             f'<li><b>Ball tackles</b>. {team1} — {total_blocks_home} ({name_top_blocks_home}, {amount_blocks_home}). {team2} — {total_blocks_away}  ({name_top_blocks_away} — {amount_blocks_away}).</li>'
        #         f'</ul>'
        #     f'<h4><b>Face-to-face:</b></h4>'
        #         f'<p>By the number of face-to-face fights for ball the leaders in the teams are:</p>'
        #         f'<ul>'
        #             f'<li>{name_duels_team1}, {team1} ({amount_duels_team1})</li>'
        #             f'<li>{name_duels_team2}, {team2} ({amount_duels_team2})</li>'
        #         f'</ul>  '
        #     f'{title3}'
        #         f'<ul>'
        #             f'{fouls}'
        #         f'</ul>'
        #     f'{title2}'
        #         f'<ul>'   
        #             f'{penalti}'
        #         f'</ul>'    
        #     f'<h4><b>The last five games (including this match):</b></h4>'
        #     f'<ul>'
        #             f'<li>{team1} - {form_home}</li>'
        #             f'<li>{team2} - {form_away}</li>'
        #     f'</ul>'
        #     # f'<h4><b>The {league_name1} table right now:</b></h4><h4>'
        #     # f'<table >'
        #     #     f'<tbody>'
                    
        #     #         f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
        #     #             f'<td>#</td>'
        #     #             f'<td><b>Team</b></td>'
        #     #             f'<td><b>Form</b></td>'
        #     #             f'<td>PL</td>'
        #     #             f'<td style= "background-color: #4a9460;">W</td>'
        #     #             f'<td>D</td>' #style= "background-color: #9f9c98;"
        #     #             f'<td style= "background-color: #a13c3c;">L</td>'
        #     #             f'<td>GF</td>'
        #     #             f'<td>GA</td>'
        #     #             f'<td>GD</td>'
        #     #             f'<td>Pts</td>'
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[0]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[0].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[0]}'
        #     #             f'{all_games[0]}'
        #     #             f'{win_games[0]}'
        #     #             f'{draw_games[0]}'
        #     #             f'{lose_games[0]}'
        #     #             f'{goals_for[0]}'
        #     #             f'{goals_missed[0]}'
        #     #             f'{goals_diff[0]}'
        #     #             f'{points[0]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[1]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[1].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[1]}'
        #     #             f'{all_games[1]}'
        #     #             f'{win_games[1]}'
        #     #             f'{draw_games[1]}'
        #     #             f'{lose_games[1]}'
        #     #             f'{goals_for[1]}'
        #     #             f'{goals_missed[1]}'
        #     #             f'{goals_diff[1]}'
        #     #             f'{points[1]}'        
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[2]}'     
        #     #             f'<td>'
        #     #                 f'{logo_table[2].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[2]}'
        #     #             f'{all_games[2]}'
        #     #             f'{win_games[2]}'
        #     #             f'{draw_games[2]}'
        #     #             f'{lose_games[2]}'
        #     #             f'{goals_for[2]}'
        #     #             f'{goals_missed[2]}'
        #     #             f'{goals_diff[2]}'
        #     #             f'{points[2]}'   
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[3]}'      
        #     #             f'<td>'
        #     #                 f'{logo_table[3].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[3]}'
        #     #             f'{all_games[3]}'
        #     #             f'{win_games[3]}'
        #     #             f'{draw_games[3]}'
        #     #             f'{lose_games[3]}'
        #     #             f'{goals_for[3]}'
        #     #             f'{goals_missed[3]}'
        #     #             f'{goals_diff[3]}'
        #     #             f'{points[3]}'           
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[4]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[4].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[4]}'
        #     #             f'{all_games[4]}'
        #     #             f'{win_games[4]}'
        #     #             f'{draw_games[4]}'
        #     #             f'{lose_games[4]}'
        #     #             f'{goals_for[4]}'
        #     #             f'{goals_missed[4]}'
        #     #             f'{goals_diff[4]}'
        #     #             f'{points[4]}'                
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[5]}'                
        #     #             f'<td>'
        #     #                 f'{logo_table[5].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[5]}'
        #     #             f'{all_games[5]}'
        #     #             f'{win_games[5]}'
        #     #             f'{draw_games[5]}'
        #     #             f'{lose_games[5]}'
        #     #             f'{goals_for[5]}'
        #     #             f'{goals_missed[5]}'
        #     #             f'{goals_diff[5]}'
        #     #             f'{points[5]}'                       
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[6]}'               
        #     #             f'<td>'
        #     #                 f'{logo_table[6].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[6]}'
        #     #             f'{all_games[6]}'
        #     #             f'{win_games[6]}'
        #     #             f'{draw_games[6]}'
        #     #             f'{lose_games[6]}'
        #     #             f'{goals_for[6]}'
        #     #             f'{goals_missed[6]}'
        #     #             f'{goals_diff[6]}'
        #     #             f'{points[6]}'              
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[7]}'        
        #     #             f'<td>'
        #     #                 f'{logo_table[7].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[7]}'
        #     #             f'{all_games[7]}'
        #     #             f'{win_games[7]}'
        #     #             f'{draw_games[7]}'
        #     #             f'{lose_games[7]}'
        #     #             f'{goals_for[7]}'
        #     #             f'{goals_missed[7]}'
        #     #             f'{goals_diff[7]}'
        #     #             f'{points[7]}'                       
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[8]}'               
        #     #             f'<td>'
        #     #                 f'{logo_table[8].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[8]}'
        #     #             f'{all_games[8]}'
        #     #             f'{win_games[8]}'
        #     #             f'{draw_games[8]}'
        #     #             f'{lose_games[8]}'
        #     #             f'{goals_for[8]}'
        #     #             f'{goals_missed[8]}'
        #     #             f'{goals_diff[8]}'
        #     #             f'{points[8]}'   
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[9]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[9].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[9]}'
        #     #             f'{all_games[9]}'
        #     #             f'{win_games[9]}'
        #     #             f'{draw_games[9]}'
        #     #             f'{lose_games[9]}'
        #     #             f'{goals_for[9]}'
        #     #             f'{goals_missed[9]}'
        #     #             f'{goals_diff[9]}'
        #     #             f'{points[9]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[10]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[10].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[10]}'
        #     #             f'{all_games[10]}'
        #     #             f'{win_games[10]}'
        #     #             f'{draw_games[10]}'
        #     #             f'{lose_games[10]}'
        #     #             f'{goals_for[10]}'
        #     #             f'{goals_missed[10]}'
        #     #             f'{goals_diff[10]}'
        #     #             f'{points[10]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[11]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[11].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[11]}'
        #     #             f'{all_games[11]}'
        #     #             f'{win_games[11]}'
        #     #             f'{draw_games[11]}'
        #     #             f'{lose_games[11]}'
        #     #             f'{goals_for[11]}'
        #     #             f'{goals_missed[11]}'
        #     #             f'{goals_diff[11]}'
        #     #             f'{points[11]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[12]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[12].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[12]}'
        #     #             f'{all_games[12]}'
        #     #             f'{win_games[12]}'
        #     #             f'{draw_games[12]}'
        #     #             f'{lose_games[12]}'
        #     #             f'{goals_for[12]}'
        #     #             f'{goals_missed[12]}'
        #     #             f'{goals_diff[12]}'
        #     #             f'{points[12]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[13]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[13].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[13]}'
        #     #             f'{all_games[13]}'
        #     #             f'{win_games[13]}'
        #     #             f'{draw_games[13]}'
        #     #             f'{lose_games[13]}'
        #     #             f'{goals_for[13]}'
        #     #             f'{goals_missed[13]}'
        #     #             f'{goals_diff[13]}'
        #     #             f'{points[13]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[14]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[14].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[14]}'
        #     #             f'{all_games[14]}'
        #     #             f'{win_games[14]}'
        #     #             f'{draw_games[14]}'
        #     #             f'{lose_games[14]}'
        #     #             f'{goals_for[14]}'
        #     #             f'{goals_missed[14]}'
        #     #             f'{goals_diff[14]}'
        #     #             f'{points[14]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[15]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[15].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[15]}'
        #     #             f'{all_games[15]}'
        #     #             f'{win_games[15]}'
        #     #             f'{draw_games[15]}'
        #     #             f'{lose_games[15]}'
        #     #             f'{goals_for[15]}'
        #     #             f'{goals_missed[15]}'
        #     #             f'{goals_diff[15]}'
        #     #             f'{points[15]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[16]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[16].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[16]}'
        #     #             f'{all_games[16]}'
        #     #             f'{win_games[16]}'
        #     #             f'{draw_games[16]}'
        #     #             f'{lose_games[16]}'
        #     #             f'{goals_for[16]}'
        #     #             f'{goals_missed[16]}'
        #     #             f'{goals_diff[16]}'
        #     #             f'{points[16]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[17]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[17].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[17]}'
        #     #             f'{all_games[17]}'
        #     #             f'{win_games[17]}'
        #     #             f'{draw_games[17]}'
        #     #             f'{lose_games[17]}'
        #     #             f'{goals_for[17]}'
        #     #             f'{goals_missed[17]}'
        #     #             f'{goals_diff[17]}'
        #     #             f'{points[17]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[18]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[18].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[18]}'
        #     #             f'{all_games[18]}'
        #     #             f'{win_games[18]}'
        #     #             f'{draw_games[18]}'
        #     #             f'{lose_games[18]}'
        #     #             f'{goals_for[18]}'
        #     #             f'{goals_missed[18]}'
        #     #             f'{goals_diff[18]}'
        #     #             f'{points[18]}'      
        #     #         f'</tr>'
        #     #         f'<tr align="centre" valign="top">'
        #     #             f'{rank[19]}'
        #     #             f'<td>'
        #     #                 f'{logo_table[19].replace("+", " ")}'
        #     #             f'</td>'
        #     #             f'{form_all[19]}'
        #     #             f'{all_games[19]}'
        #     #             f'{win_games[19]}'
        #     #             f'{draw_games[19]}'
        #     #             f'{lose_games[19]}'
        #     #             f'{goals_for[19]}'
        #     #             f'{goals_missed[19]}'
        #     #             f'{goals_diff[19]}'
        #     #             f'{points[19]}'      
        #     #         f'</tr>'
        #     #         f'</tbody>'
        #     #     f'</table>'
                    
        #     f'<h4><b>Top 5 {league_name1} scorers:</b></h4>'
        #         f'<ol>'
        #             f'<li>{first_top_name} ({first_top_amount}, {first_top_team})</li>'
        #             f'<li>{second_top_name} ({second_top_amount}, {second_top_team})</li>'
        #             f'<li>{third_top_name} ({third_top_amount}, {third_top_team})</li>'
        #             f'<li>{fourth_top_name} ({fourth_top_amount}, {fourth_top_team})</li>'
        #             f'<li>{fifth_top_name} ({fifth_top_amount}, {fifth_top_team})</li>'
        #         f'</ol>'
        #     f'<h4><b>Next games:</b></h4>'
        #         f'<ul>'
        #             f'<li><b>{team1}</b> will play with {next_match_team1_with}. {team1_next_match}, on {next_match_team1_venue}. </li>'
        #             f'<li><b>{team2}</b> will play with {next_match_team2_with}. {team2_next_match}, on {next_match_team2_venue}. </li>'
        #         f'</ul>'



# elif int(goals_a) < int(goals_b):
        #     title = f'{img}{team_a} сегодня проиграла {team_b} - {goals_a}:{goals_b}'
        #     text = (
        #         f'<h3>Составы игравших команд:</h3>'
        #             f'<table align="center" border="1">'
        #                 f'<tr align="center" valign="center">'
        #                     f'<td>'
        #                         f'<p><b>{team_a}</b><bot>'
        #                         f'<p>{lineups_a}</p></bot>'
        #                     f'</td>'
        #                     f'<td>'
        #                         f'<p><b>{team_b}</b><bot>'
        #                         f'<p>{lineups_b}</p></bot>  '
        #                     f'</td>'
        #             f'</table>'
        #         f'<h3>Замены:</h3>'
        #             f'<table align="center" border="1">'
        #                 f'<tr align="center" valign="center">'
        #                     f'<td>'
        #                         f'<p><b>{team_a}</b></p>'
        #                         f'<p>{lineups_in_game_a}<br></p>'
        #                     f'</td>'
        #                     f'<td>'
        #                         f'<p><b>{team_b}</b></p>'
        #                         f'<p>{lineups_in_game_b}<br></p>'
        #                     f'</td>'
        #             f'</table>'
        #         f'{goals}'
        #         f'<p>На двоих команды нанесли {total_shots_off} ударов в створ и {total_shots_on} по воротам:</p>'
        #             f'<ul>'
        #                 f'<li>{team_a}: {shots_team1_off} ударов в створ, {shots_team1_on}  по воротам. Самый активный по количеству ударов — {active_shots_player_home}.</li>'
        #                 f'<li>{team_b}: {shots_team2_off} ударов в створ, {shots_team2_on} по воротам. Больше всего нанёс ударов — {active_shots_player_away}.</li>'
        #             f'</ul>'
        #         f'<p>В общей сложности у {team_a} было {total_assists_home} голевых моментов, у {team_b} — {total_assists_away}.</p>'
        #         f'<h3>Оборонительные действия:</h3>'
        #             f'<ul>'
        #                 f'<li>Количество перехватов у {team_a} — {total_interceptions_home} (лидер — {name_top_inceptions_home}, {amount_interceptions_home} перехватов). У {team_b} — {total_inteceptions_away} (больше всего у {name_top_inceptions_away}, {amount_interseptions_away} перехватов). </li>'
        #                 f'<li>Отборы. {team_a} — {total_blocks_home} (больше всех у {name_top_blocks_home}, {amount_blocks_home} отборов). {team_b} — {total_blocks_away}  (у {name_top_blocks_away} — {amount_blocks_away} отборов).</li>'
        #             f'</ul>'
        #         f'<h3>Единоборства:</h3>'
        #             f'<p>По количеству выигранных единоборств лидерами в командах стали:</p>'
        #             f'<ul>'
        #                 f'<li>{name_duels_team1}, {team_a} ({amount_duels_team1})</li>'
        #                 f'<li>{name_duels_team2}, {team_b} ({amount_duels_team2})</li>'
        #             f'</ul>  '
        #         f'<h3>Процент владения мячом:</h3>     '
        #             f'<p>{team_a} — {possession_team1} процентов</p>'
        #             f'<p>{team_b} — {possession_team2} процентов</p>'
        #             f'<p>Больше всего игрового времени команды провели на половине Команды 1 / 2 / в центре поля. (Этого параметра нет)</p>'
        #         f'{fouls}'
        #         f'<h3>Тройка лидеров в гонке бомбардиров чемпионата:</h3>'
        #             f'<ol>'
        #                 f'<li>{first_top_name} ({first_top_amount}, {first_top_team})</li>'
        #                 f'<li>{second_top_name} ({second_top_amount}, {second_top_team})</li>'
        #                 f'<li>{third_top_name} ({third_top_amount}, {third_top_team})</li>'
        #             f'</ol>'
        #         f'<h3>Следующие матчи:</h3>'
        #             f'<p>Команда {team_a} играет с {next_match_team1_with}. {next_match_team1_date}, {next_match_team1_venue}.</p>'
        #             f'<p>Команда {team_b} играет с {next_match_team2_with}. {next_match_team2_date}, {next_match_team2_venue}.</p>'
        #     )
        # elif int(goals_a) == int(goals_b):
        #     title = f'{img}{team_a} сыграла в ничью с {team_b} - {goals_a}:{goals_b}'
        #     text = (
        #         f'<h3>Составы игравших команд:</h3>'
        #             f'<table align="center" border="1">'
        #                 f'<tr align="center" valign="center">'
        #                     f'<td>'
        #                         f'<p><b>{team_a}</b><bot>'
        #                         f'<p>{lineups_a}</p></bot>'
        #                     f'</td>'
        #                     f'<td>'
        #                         f'<p><b>{team_b}</b><bot>'
        #                         f'<p>{lineups_b}</p></bot>  '
        #                     f'</td>'
        #             f'</table>'
        #         f'<h3>Замены:</h3>'
        #             f'<table align="center" border="1">'
        #                 f'<tr align="center" valign="center">'
        #                     f'<td>'
        #                         f'<p><b>{team_a}</b></p>'
        #                         f'<p>{lineups_in_game_a}<br></p>'
        #                     f'</td>'
        #                     f'<td>'
        #                         f'<p><b>{team_b}</b></p>'
        #                         f'<p>{lineups_in_game_b}<br></p>'
        #                     f'</td>'
        #             f'</table>'
        #         f'{goals}'
        #         f'<p>На двоих команды нанесли {total_shots_off} ударов в створ и {total_shots_on} по воротам:</p>'
        #             f'<ul>'
        #                 f'<li>{team_a}: {shots_team1_off} ударов в створ, {shots_team1_on}  по воротам. Самый активный по количеству ударов — {active_shots_player_home}.</li>'
        #                 f'<li>{team_b}: {shots_team2_off} ударов в створ, {shots_team2_on} по воротам. Больше всего нанёс ударов — {active_shots_player_away}.</li>'
        #             f'</ul>'
        #         f'<p>В общей сложности у {team_a} было {total_assists_home} голевых моментов, у {team_b} — {total_assists_away}.</p>'
        #         f'<h3>Оборонительные действия:</h3>'
        #             f'<ul>'
        #                 f'<li>Количество перехватов у {team_a} — {total_interceptions_home} (лидер — {name_top_inceptions_home}, {amount_interceptions_home} перехватов). У {team_b} — {total_inteceptions_away} (больше всего у {name_top_inceptions_away}, {amount_interseptions_away} перехватов). </li>'
        #                 f'<li>Отборы. {team_a} — {total_blocks_home} (больше всех у {name_top_blocks_home}, {amount_blocks_home} отборов). {team_b} — {total_blocks_away}  (у {name_top_blocks_away} — {amount_blocks_away} отборов).</li>'
        #             f'</ul>'
        #         f'<h3>Единоборства:</h3>'
        #             f'<p>По количеству выигранных единоборств лидерами в командах стали:</p>'
        #             f'<ul>'
        #                 f'<li>{name_duels_team1}, {team_a} ({amount_duels_team1})</li>'
        #                 f'<li>{name_duels_team2}, {team_b} ({amount_duels_team2})</li>'
        #             f'</ul>  '
        #         f'<h3>Процент владения мячом:</h3>     '
        #             f'<p>{team_a} — {possession_team1} процентов</p>'
        #             f'<p>{team_b} — {possession_team2} процентов</p>'
        #             f'<p>Больше всего игрового времени команды провели на половине Команды 1 / 2 / в центре поля. (Этого параметра нет)</p>'
        #         f'{fouls}'
        #         f'<h3>Тройка лидеров в гонке бомбардиров чемпионата:</h3>'
        #             f'<ol>'
        #                 f'<li>{first_top_name} ({first_top_amount}, {first_top_team})</li>'
        #                 f'<li>{second_top_name} ({second_top_amount}, {second_top_team})</li>'
        #                 f'<li>{third_top_name} ({third_top_amount}, {third_top_team})</li>'
        #             f'</ol>'
        #         f'<h3>Следующие матчи:</h3>'
        #             f'<p>Команда {team_a} играет с {next_match_team1_with}. {next_match_team1_date}, {next_match_team1_venue}.</p>'
        #             f'<p>Команда {team_b} играет с {next_match_team2_with}. {next_match_team2_date}, {next_match_team2_venue}.</p>'
        #     )


# title = f'\n{img}{team1} — {team2}. Основные расклады перед ближайшим матчем команд'

                # text = (
                # f'<p><b>{date1} {team1} принимает {team2} на {venue1}. Разбираем статистические расклады по соперникам и лучшие коэффициенты букмекеров на предстоящий матч.</b></p>'
                #     f'<p>На сегодня {team1} занимает в чемпионате {league_name1} <b>{rank1}</b> место, его соперник — <b>{rank2}</b> место.</p>'
                    
                #     f'<h3><strong>Статистика по игрокам</strong></h3>'
                #         f'<p>В списке бомбардиров лучший результат среди футболистов \n<b>{team1}</b>: {top_player_a} ({top_home_total} мячей). <b>У соперника</b> — {top_player_b} ({top_away_total} мячей).</p>'
                #         f'<p>Тройка же лидеров среди бомбардиров выглядит так:</p>'
                #     f'<ol>'
                #         f'<li>{first_in_league_name} ({first_in_league_amount}, «{first_in_league_team}»)</li>'
                #         f'<li>{second_in_league_name} ({second_in_league_amount}, «{second_in_league_team}»)</li>'
                #         f'<li>{thrid_in_league_name} ({thrid_in_league_amount}, «{thrid_in_league_team}»)</li>'
                #     f'</ol>'
                #     f'<p>Лучшие игроки обеих команд по другим основным статистическим показателям текущего сезона:</p>'
                #     f'<ul>'
                #         f'<li>Голевые передачи: {top_home_assist_name} ({team1}) — {top_home_assist_amount} передач,  {top_away_assist_name} ({team2}) — {top_away_assist_amount} передачи.</li>'
                #         f'<li>Сейвы голкиперов команд: {top_home_saves_name} ({team1}) — {top_home_saves_amount}, {top_away_saves_name} ({team2}) — {top_away_saves_amount}</li>'
                #         f'<li>Отборы мяча: {top_home_blocks_name} ({team1}) — {top_home_blocks_amount}, {top_away_blocks_name} ({team2}) — {top_away_blocks_amount}.</li>'
                #         f'<li>Больше всех выигранных дуэлей: {top_home_duels_name} ({team1}) — {top_home_duels_amount}, {top_away_duels_name} ({team2}) — {top_away_duels_amount}.</li>'
                #         f'<li>Чаще всего нарушают правила: {top_home_fouls_name} ({team1}) — {top_home_fouls_amount} нарушений, {top_away_fouls_name} ({team2}) — {top_away_fouls_amount}.</li>'
                #     f'</ul>'
                #     f'<h3><strong>Командная статистика</strong></h3>'
                #     f'<p>К завтрашнему матчу команды подходят в разной форме. Итоги предыдущих пяти матчей каждого из соперников:</p>'
                #     f'<ul>'
                #         f'<li>{team1} — {home_forms}</li>'
                #         f'<li>{team2} — {away_forms}</li>'
                #     f'</ul>'
                #     f'<p>В нынешнем сезоне {team1} не пропускал в {clean_home} матчах. Его соперник {team2} сыграл на ноль {clean_away} раз.</p>'
                #     f'<p>Самый крупный выигрыш {team1} в текущем сезоне дома — {home_biggest_win_in_home}, в гостях — {home_biggest_win_in_away}. Самый крупный проигрыш дома — {home_biggest_lose_in_home}, в гостях — {home_biggest_lose_in_away}. Что касается его соперника {team2}, то крупнейший выигрыш в сезоне дома — {away_biggest_win_in_home}, в гостях — {away_biggest_win_in_away}, а счет самого крупного проигрыша дома — {away_biggest_lose_in_home}, в гостях — {away_biggest_lose_in_away}.</p>'
                #     f'<p>В этом сезоне дома у {team1}: побед — {home_win_once_in_home}, ничьих — {home_draws_once_in_home}, проигрышей — {home_lose_once_in_home}. А {team2} в гостях в сезоне играет следующим образом: побед — {away_win_once_in_away}, ничьих — {away_draws_once_in_away}, проигрышей — {away_lose_once_in_away}.</p>'
                #     f'<p>Дома {team1} больше всего забивал в интервале с{for_goals_home} , а пропускал — с{missed_goals_home}, в то время как {team2} в гостях больше всего забивал в интервале — с{for_goals_away}, а пропускал — с{missed_goals_away} </p>'
                #     f'<h3>Статистика личных встреч за последние три сезона:</h3>'
                #     f'<table align="center" border="1">'
                #         f'<tbody>'
                #             f'<tr align="center" valign="center">'
                #                 f'<td rowspan="2">Команда</td>'
                #                 f'<td rowspan="2">Игры</td>'
                #                 f'<td colspan="2">Выигрыш</td>'
                #                 f'<td colspan="2">Ничьи</td>'
                #                 f'<td colspan="2">Поражения</td>'
                #             f'</tr>'
                #             f'<tr align="center" valign="center">'
                #                 f'<td>H</td>'
                #                 f'<td>A</td>'
                #                 f'<td>H</td>'
                #                 f'<td>A</td>'
                #                 f'<td>H</td>'
                #                 f'<td>A</td>'
                #             f'</tr>'
                #             f'<tr align="center" valign="center">'
                #                 f'<td>{team1}</td>'
                #                 f'<td rowspan="2" valign="center">{table_h2h_total_game}</td>'
                #                 f'<td>{home_table_h2h_win_in_home}</td>'
                #                 f'<td>{home_table_h2h_win_in_away}</td>'
                #                 f'<td>{home_table_h2h_draws_in_home}</td>'
                #                 f'<td>{home_table_h2h_draws_in_away}</td>'
                #                 f'<td>{home_table_h2h_lose_in_home}</td>'
                #                 f'<td>{home_table_h2h_lose_in_away}</td>'
                #             f'</tr>'
                #             f'<tr align="center" valign="center">'
                #                 f'<td>{team2}</td><td>{away_table_h2h_win_in_home}</td>'
                #                 f'<td>{away_table_h2h_win_in_away}</td>'
                #                 f'<td>{away_table_h2h_draws_in_home}</td>'
                #                 f'<td>{away_table_h2h_draws_in_away}</td>'
                #                 f'<td>{away_table_h2h_lose_in_home}</td>'
                #                 f'<td>{away_table_h2h_lose_in_away}</td>'
                #             f'</tr>'
                #         f'</tbody>'
                #     f'</table>'
                #     f'<h3><strong>Вероятностные характеристики команд перед матчем:</strong></h3>'
                #     f'<table align="center" border="1">'
                #         f'<tbody>'
                #         f'<tr align="center" valign="center">'
                #             f'<td>{team1}</td>'
                #             f'<td></td>'
                #             f'<td>{team2}</td>'
                #         f'</tr>'
                #             f'<tr><td>{home_comparison_win}</td>'
                #             f'<td>Выигрыш игры</td><td>{away_comparison_win}</td></tr>'
                #             f'<tr><td>{home_comparison_att}</td><td>Потенциал в атаке</td>'
                #             f'<td>{away_comparison_att}</td></tr><tr><td>{home_comparison_def}</td>'
                #             f'<td>Потенциал в защите</td><td>{away_comparison_def}</td></tr>'
                #             f'<tr><td>{home_comparison_t2t}</td><td>Сила друг против друга</td>'
                #             f'<td>{away_comparison_t2t}</td></tr><tr><td>{home_comparison_goals}</td>'
                #             f'<td>Потенциал голов</td><td>{away_comparison_goals}</td></tr>'
                #         f'</tbody>'
                #     f'</table>'
                #     f'<p>Таким образом, в матче {team1} – {team2} вероятность победы {team2} – {predictions_lose_home}, ничьей – {predictions_draws}, поражения – {predictions_win_home}. То есть, {team1}, скорее всего, {home_win_or_lose}</p>'
                #     f'<p>Голов {team1}, вероятно, забьет не больше {home_predictions_goals}, {team2} — не больше {away_predictions_goals}.</p>'
                #     f'<p>Ну и вот <b>лучшие коэффициенты</b> букмекеров на этот матч:</p>'
                #     f'<table align="center" border="1">'
                #         f'<tbody>'
                #             f'<tr align="center" valign="top">'
                #                 f'<td>Победа хозяев</td>'
                #                 f'<td>Ничья</td>'
                #                 f'<td>Победа гостей</td></tr>'
                #             f'<tr align="center" valign="top">'
                #                 f'<td>{bk1_name}<br>{bk1_win_home}</td>'
                #                 f'<td>{bk2_name}<br>{bk2_draw}</td>'
                #                 f'<td>{bk3_name}<br>{bk3_win_away}</td>'
                #             f'</tr>'
                #         f'</tbody>'
                #     f'</table>'
                #     f'<p>Напоминаем, что матч между командами {team1} и {team2} состоится {date1} (подправить дату) на {venue1}.</p>'
                # )
<table>
	    <tbody>
			
	         <tr align='center' valign='top' style= 'background-color: #aedbea;'>
	             <td>#</td>
	             <td><b>Team</b></td>
	             <td><b>Form</b></td>
	             <td>PL</td>
	             <td style= 'background-color: #4a9460;'>W</td>
	             <td>D</td> #style= 'background-color: #9f9c98;'
	             <td style= 'background-color: #a13c3c;'>L</td>
	             <td>GF</td>
	             <td>GA</td>
	             <td>GD</td>
	             <td>Pts</td>
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[0]}
	             <td>
	                 {logo_table[0].replace('+', ' ')}
	             </td>
	             {form_all[0]}
	             {all_games[0]}
	             {win_games[0]}
	             {draw_games[0]}
	             {lose_games[0]}
	             {goals_for[0]}
	             {goals_missed[0]}
	             {goals_diff[0]}
	             {points[0]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[1]}
	             <td>
	                 {logo_table[1].replace('+', ' ')}
	             </td>
	             {form_all[1]}
	             {all_games[1]}
	             {win_games[1]}
	             {draw_games[1]}
	             {lose_games[1]}
	             {goals_for[1]}
	             {goals_missed[1]}
	             {goals_diff[1]}
	             {points[1]}        
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[2]}     
	             <td>
	                 {logo_table[2].replace('+', ' ')}
	             </td>
	             {form_all[2]}
	             {all_games[2]}
	             {win_games[2]}
	             {draw_games[2]}
	             {lose_games[2]}
	             {goals_for[2]}
	             {goals_missed[2]}
	             {goals_diff[2]}
	             {points[2]}   
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[3]}      
	             <td>
	                 {logo_table[3].replace('+', ' ')}
	             </td>
	             {form_all[3]}
	             {all_games[3]}
	             {win_games[3]}
	             {draw_games[3]}
	             {lose_games[3]}
	             {goals_for[3]}
	             {goals_missed[3]}
	             {goals_diff[3]}
	             {points[3]}           
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[4]}
	             <td>
	                 {logo_table[4].replace('+', ' ')}
	             </td>
	             {form_all[4]}
	             {all_games[4]}
	             {win_games[4]}
	             {draw_games[4]}
	             {lose_games[4]}
	             {goals_for[4]}
	             {goals_missed[4]}
	             {goals_diff[4]}
	             {points[4]}                
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[5]}                
	             <td>
	                 {logo_table[5].replace('+', ' ')}
	             </td>
	             {form_all[5]}
	             {all_games[5]}
	             {win_games[5]}
	             {draw_games[5]}
	             {lose_games[5]}
	             {goals_for[5]}
	             {goals_missed[5]}
	             {goals_diff[5]}
	             {points[5]}                       
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[6]}               
	             <td>
	                 {logo_table[6].replace('+', ' ')}
	             </td>
	             {form_all[6]}
	             {all_games[6]}
	             {win_games[6]}
	             {draw_games[6]}
	             {lose_games[6]}
	             {goals_for[6]}
	             {goals_missed[6]}
	             {goals_diff[6]}
	             {points[6]}              
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[7]}        
	             <td>
	                 {logo_table[7].replace('+', ' ')}
	             </td>
	             {form_all[7]}
	             {all_games[7]}
	             {win_games[7]}
	             {draw_games[7]}
	             {lose_games[7]}
	             {goals_for[7]}
	             {goals_missed[7]}
	             {goals_diff[7]}
	             {points[7]}                       
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[8]}               
	             <td>
	                 {logo_table[8].replace('+', ' ')}
	             </td>
	             {form_all[8]}
	             {all_games[8]}
	             {win_games[8]}
	             {draw_games[8]}
	             {lose_games[8]}
	             {goals_for[8]}
	             {goals_missed[8]}
	             {goals_diff[8]}
	             {points[8]}   
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[9]}
	             <td>
	                 {logo_table[9].replace('+', ' ')}
	             </td>
	             {form_all[9]}
	             {all_games[9]}
	             {win_games[9]}
	             {draw_games[9]}
	             {lose_games[9]}
	             {goals_for[9]}
	             {goals_missed[9]}
	             {goals_diff[9]}
	             {points[9]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[10]}
	             <td>
	                 {logo_table[10].replace('+', ' ')}
	             </td>
	             {form_all[10]}
	             {all_games[10]}
	             {win_games[10]}
	             {draw_games[10]}
	             {lose_games[10]}
	             {goals_for[10]}
	             {goals_missed[10]}
	             {goals_diff[10]}
	             {points[10]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[11]}
	             <td>
	                 {logo_table[11].replace('+', ' ')}
	             </td>
	             {form_all[11]}
	             {all_games[11]}
	             {win_games[11]}
	             {draw_games[11]}
	             {lose_games[11]}
	             {goals_for[11]}
	             {goals_missed[11]}
	             {goals_diff[11]}
	             {points[11]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[12]}
	             <td>
	                 {logo_table[12].replace('+', ' ')}
	             </td>
	             {form_all[12]}
	             {all_games[12]}
	             {win_games[12]}
	             {draw_games[12]}
	             {lose_games[12]}
	             {goals_for[12]}
	             {goals_missed[12]}
	             {goals_diff[12]}
	             {points[12]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[13]}
	             <td>
	                 {logo_table[13].replace('+', ' ')}
	             </td>
	             {form_all[13]}
	             {all_games[13]}
	             {win_games[13]}
	             {draw_games[13]}
	             {lose_games[13]}
	             {goals_for[13]}
	             {goals_missed[13]}
	             {goals_diff[13]}
	             {points[13]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[14]}
	             <td>
	                 {logo_table[14].replace('+', ' ')}
	             </td>
	             {form_all[14]}
	             {all_games[14]}
	             {win_games[14]}
	             {draw_games[14]}
	             {lose_games[14]}
	             {goals_for[14]}
	             {goals_missed[14]}
	             {goals_diff[14]}
	             {points[14]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[15]}
	             <td>
	                 {logo_table[15].replace('+', ' ')}
	             </td>
	             {form_all[15]}
	             {all_games[15]}
	             {win_games[15]}
	             {draw_games[15]}
	             {lose_games[15]}
	             {goals_for[15]}
	             {goals_missed[15]}
	             {goals_diff[15]}
	             {points[15]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[16]}
	             <td>
	                 {logo_table[16].replace('+', ' ')}
	             </td>
	             {form_all[16]}
	             {all_games[16]}
	             {win_games[16]}
	             {draw_games[16]}
	             {lose_games[16]}
	             {goals_for[16]}
	             {goals_missed[16]}
	             {goals_diff[16]}
	             {points[16]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[17]}
	             <td>
	                 {logo_table[17].replace('+', ' ')}
	             </td>
	             {form_all[17]}
	             {all_games[17]}
	             {win_games[17]}
	             {draw_games[17]}
	             {lose_games[17]}
	             {goals_for[17]}
	             {goals_missed[17]}
	             {goals_diff[17]}
	             {points[17]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[18]}
	             <td>
	                 {logo_table[18].replace('+', ' ')}
	             </td>
	             {form_all[18]}
	             {all_games[18]}
	             {win_games[18]}
	             {draw_games[18]}
	             {lose_games[18]}
	             {goals_for[18]}
	             {goals_missed[18]}
	             {goals_diff[18]}
	             {points[18]}      
	         </tr>
	         <tr align='centre' valign='top'>
	             {rank[19]}
	             <td>
	                 {logo_table[19].replace('+', ' ')}
	             </td>
	             {form_all[19]}
	             {all_games[19]}
	             {win_games[19]}
	             {draw_games[19]}
	             {lose_games[19]}
	             {goals_for[19]}
	             {goals_missed[19]}
	             {goals_diff[19]}
	             {points[19]}      
	         </tr>
	         </tbody>
	     </table>
