import json

def preview_round_text(rounds, league_id):
    from db import get_data_round

    # Запрос в БД
    insert_query = (
        f"SELECT rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds FROM round_preview WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_preview_round = get_data_round(insert_query)

    index_text_preview_round = index_text_preview_round[0]

    #id, rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name = index_text_preview_round[0], index_text_preview_round[1], index_text_preview_round[2], index_text_preview_round[3], index_text_preview_round[4], index_text_preview_round[5], index_text_preview_round[6], index_text_preview_round[7], index_text_preview_round[8], index_text_preview_round[9], index_text_preview_round[10], index_text_preview_round[11], index_text_preview_round[12], index_text_preview_round[13], index_text_preview_round[14], index_text_preview_round[15], index_text_preview_round[16], index_text_preview_round[17], index_text_preview_round[18], index_text_preview_round[19], index_text_preview_round[20], index_text_preview_round[21], index_text_preview_round[22], index_text_preview_round[23], index_text_preview_round[24], index_text_preview_round[25], index_text_preview_round[26], index_text_preview_round[27], index_text_preview_round[28], index_text_preview_round[29], index_text_preview_round[30], index_text_preview_round[31], index_text_preview_round[32], index_text_preview_round[33], index_text_preview_round[34], index_text_preview_round[35], index_text_preview_round[36], index_text_preview_round[37], index_text_preview_round[38], index_text_preview_round[39], index_text_preview_round[40], index_text_preview_round[41], index_text_preview_round[42], index_text_preview_round[43], index_text_preview_round[44], index_text_preview_round[45], index_text_preview_round[46], index_text_preview_round[47], index_text_preview_round[48], index_text_preview_round[49], index_text_preview_round[50], index_text_preview_round[51], index_text_preview_round[52], index_text_preview_round[53], index_text_preview_round[54], index_text_preview_round[55], index_text_preview_round[56], index_text_preview_round[57], index_text_preview_round[58], index_text_preview_round[59], index_text_preview_round[60], index_text_preview_round[61], index_text_preview_round[62], index_text_preview_round[63], index_text_preview_round[64], index_text_preview_round[65], index_text_preview_round[66], index_text_preview_round[67], index_text_preview_round[68], index_text_preview_round[69], index_text_preview_round[70], index_text_preview_round[71], index_text_preview_round[72], index_text_preview_round[73], index_text_preview_round[74], index_text_preview_round[75], index_text_preview_round[76], index_text_preview_round[77], index_text_preview_round[78], index_text_preview_round[79], index_text_preview_round[80], index_text_preview_round[81], index_text_preview_round[82], index_text_preview_round[83], index_text_preview_round[84], index_text_preview_round[85], index_text_preview_round[86], index_text_preview_round[87], index_text_preview_round[88], index_text_preview_round[89], index_text_preview_round[90], index_text_preview_round[91], index_text_preview_round[92], index_text_preview_round[93], index_text_preview_round[94], index_text_preview_round[95], index_text_preview_round[96], index_text_preview_round[97], index_text_preview_round[98], index_text_preview_round[99], index_text_preview_round[100], index_text_preview_round[101], index_text_preview_round[102], index_text_preview_round[103], index_text_preview_round[103], index_text_preview_round[104]
    rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds = index_text_preview_round

    if ' ' in preview_away_teams:
        preview_away_teams = preview_away_teams.replace(" ", "_")
    if ' ' in preview_home_teams:
        preview_home_teams = preview_home_teams.replace(" ", "_")

    
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
    preview_home_teams = preview_home_teams.replace("+", " ").split()
    preview_away_teams = preview_away_teams.replace("+", " ").split()
    
    
    preview_home_teams_new = []
    preview_away_teams_new = []
    name_table_team_new = []

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

    # for i in range(len(name_table_team)):
        
    #     if '_' in name_table_team[i]:
    #         new2 = name_table_team[i].replace("_", " ") 
    #         name_table_team_new.append(new2)
    #     if '_' not in name_table_team[i]:
    #         name_table_team_new.append(name_table_team[i])


    # odds_win_home = odds_win_home.replace(",", "").split()
    # odds_win_away = odds_win_away.replace(",", "").split()
    # odds_draw = odds_draw.replace(",", "").split()
    # date_matches = date_matches.replace("+", " ").replace("_", "T").split()
    for i in range(len(name_table_team)):
                
        if '_' in name_table_team[i]:
            new2 = name_table_team[i].replace("_", " ") 
            name_table_team_new.append(new2)
        if '_' not in name_table_team[i]:
            name_table_team_new.append(name_table_team[i])

    index_main_match = int(index_main_match)


    # data_for_title_matches = ''
    # for matches in range(len(preview_home_teams)):
    #     data_for_title_matches = data_for_title_matches + f"<li>{preview_home_teams[matches]} - {preview_away_teams[matches]} ({date_matches[matches]}), general odds: home win {odds_win_home[matches]}, draw {odds_draw[matches]}, away win {odds_win_away[matches]}</li><br>"
    main_match_for_bk_team_home = preview_home_teams_new[index_main_match]
    main_match_for_bk_team_away = preview_away_teams_new[index_main_match]
    print(preview_home_teams_new)
    rank_for_team_home = ''
    rank_for_team_away = ''
    points_for_team_home = ''
    points_for_team_away = ''

    for i in range(len(rank_for_table)):
        
        if main_match_for_bk_team_home == name_table_team_new[i]:
            rank_for_team_home = rank_for_table[i]
            points_for_team_home = points_for_table[i]
        if main_match_for_bk_team_away == name_table_team_new[i]:
            rank_for_team_away = rank_for_table[i]
            points_for_team_away = points_for_table[i]
    best_team_of_the_season = name_table_team_new[0]
    f = ''
    for table in range(len(rank_for_table)):
        f = f + f"<tr align='centre' valign='top'><td>{rank_for_table[table]}</td><td><img src='{logo_for_table[table]}' alt=''></td><td>{name_table_team_new[table]}</td><td>{form_table[table]}</td><td>{all_matches_table[table]}</td><td>{win_matches_table[table]}</td><td>{draw_matches_table[table]}</td><td>{lose_matches_table[table]}</td><td>{goals_scored_for_table[table]}</td><td>{goals_missed_for_table[table]}</td><td>{goals_diff_table[table]}</td><td>{points_for_table[table]}</td></tr>"
    


    data = {
        "title":{
            "rounds":f"{rounds}",
            "league_id":f"{league_id}",
            "league_name":f"{league_name}",
            "all_rounds":f"{all_rounds}"
        },
        "subtitle":{
            "city":f"{city_first_match}",
            "venue":f"{venue_first_match}",
            "first_date":f"{first_date_round}",
            "home_first_match":f"{home_first_match}",
            "away_first_match":f"{away_first_match}",
            "all_home_teams":f"{preview_home_teams}",
            "all_away_teams":f"{preview_away_teams}",
            "date_matches":f"{date_matches}",
            "count_matchs":f"{count_matchs}"
            # "all_matches_and_text":f"{data_for_title_matches}"
        },
        "BK":{
            "odds_win_home":f"{odds_win_home}",
            "odds_win_away":f"{odds_win_away}",
            "odds_draw":f"{odds_draw}",
            "top_win_home":f"{top_win_home}",
            "top_lose_home":f"{top_win_away}",
            "top_draw":f"{top_draw}",
            "index_main_match":f"{index_main_match}",
            "rank_for_team_home":f"{rank_for_team_home}",
            "rank_for_team_away":f"{rank_for_team_away}",
            "points_for_team_home":f"{points_for_team_home}",
            "points_for_team_away":f"{points_for_team_away}",
            "main_match_for_bk_team_home":f"{main_match_for_bk_team_home}",
            "main_match_for_bk_team_away":f"{main_match_for_bk_team_away}", 
            "date_previous_match":f"{date_previous_match}",
            "away_previous_match":f"{away_previous_match}",
            "goals_home_previous_match":f"{goals_home_previous_match}",
            "goals_away_previous_match":f"{goals_away_previous_match}"

        },
        "team_stat":{
            "team_name_injuries":f"{team_name_max_injuries}",
            "max_injuries":f"{max_injuries}",
            "team_max_goals_league":f"{team_max_goals_league}",
            "max_goals_league":f"{max_goals_league}", 
            "team_min_conceded_league":f"{team_min_conceded_league}",
            "min_conceded_top_saves":f"{min_conceded_top_saves}",
            "team_max_clean_sheet_league":f"{team_max_clean_sheet_league}",
            "max_cleen_sheet_league":f"{max_cleen_sheet_league}",
            "team_max_conceded_league":f"{team_max_conceded_league}",
            "max_conceded_saves_league":f"{max_conceded_saves_league}",
            "team_min_goals_attack_league":f"{team_min_goals_attack_league}",
            "min_goals_attack_league":f"{min_goals_attack_league}",
            "team_max_without_scored_league":f"{team_max_without_scored_league}",
            "max_without_scored_league":f"{max_without_scored_league}",
            "wins_without_scored":f"{wins_without_scored}",
            "loses_without_scored":f"{loses_without_scored}",
            "draws_without_scored":f"{draws_without_scored}",
            "team_max_conceded_goals_league":f"{team_max_conceded_goals_league}",
            "max_conceded_goals_league":f"{max_conceded_goals_league}",
            "wins_conceded_goals":f"{wins_conceded_goals}",
            "loses_conceded_goals":f"{loses_conceded_goals}",
            "draws_conceded_goals":f"{draws_conceded_goals}",
            "best_team_of_the_season":f"{best_team_of_the_season}"
        },
        "players_stat":{
            "goals_top_league_1":f"{goals_top_league_1}",  
            "name_top_goals_league_1":f"{name_top_goals_league_1}",
            "team_top_goals_league1":f"{team_top_goals_league1}",
            "goals_top_league_2":f"{goals_top_league_2}",
            "name_top_goals_league_2":f"{name_top_goals_league_2}",
            "team_top_goals_league2":f"{team_top_goals_league2}",
            "goals_top_league_3":f"{goals_top_league_3}",
            "name_top_goals_league_3":f"{name_top_goals_league_3}",
            "team_top_goals_league3":f"{team_top_goals_league3}",
            "goals_top_league_4":f"{goals_top_league_4}",
            "name_top_goals_league_4":f"{name_top_goals_league_4}",
            "team_top_goals_league4":f"{team_top_goals_league4}",
            "goals_top_league_5":f"{goals_top_league_5}",
            "name_top_goals_league_5":f"{name_top_goals_league_5}",
            "team_top_goals_league5":f"{team_top_goals_league5}",
            
            "assists_top_league_1":f"{assists_top_league_1}", 
            "name_top_assists_league_1":f"{name_top_assists_league_1}",
            "team_top_assists_league1":f"{team_top_assists_league1}",
            "assists_top_league_2":f"{assists_top_league_2}", 
            "name_top_assists_league_2":f"{name_top_assists_league_2}",
            "team_top_assists_league2":f"{team_top_assists_league2}",
            "assists_top_league_3":f"{assists_top_league_3}", 
            "name_top_assists_league_3":f"{name_top_assists_league_3}",
            "team_top_assists_league3":f"{team_top_assists_league3}",
            "assists_top_league_4":f"{assists_top_league_4}", 
            "name_top_assists_league_4":f"{name_top_assists_league_4}",
            "team_top_assists_league4":f"{team_top_assists_league4}",
            "assists_top_league_5":f"{assists_top_league_5}", 
            "name_top_assists_league_5":f"{name_top_assists_league_5}",
            "team_top_assists_league5":f"{team_top_assists_league5}",

            "saves_top_league_1":f"{saves_top_league_1}",
            "name_top_saves_league_1":f"{name_top_saves_league_1}",
            "team_top_saves_league1":f"{team_top_saves_league1}",
            "saves_top_league_2":f"{saves_top_league_2}",
            "name_top_saves_league_2":f"{name_top_saves_league_2}",
            "team_top_saves_league2":f"{team_top_saves_league2}",
            "saves_top_league_3":f"{saves_top_league_3}",
            "name_top_saves_league_3":f"{name_top_saves_league_3}",
            "team_top_saves_league3":f"{team_top_saves_league3}",
            "saves_top_league_4":f"{saves_top_league_4}",
            "name_top_saves_league_4":f"{name_top_saves_league_4}",
            "team_top_saves_league4":f"{team_top_saves_league4}",
            "saves_top_league_5":f"{saves_top_league_5}",
            "name_top_saves_league_5":f"{name_top_saves_league_5}", 
            "team_top_saves_league5":f"{team_top_saves_league5}" 
        }, 
        "f":f"{f}"
    }    
        
        # {
        #         "rank":f"{rank}:",
        #         "all_games":f"{all_games}",
        #         "win_games":f"{win_games}",
        #         "draw_games":f"{draw_games}",
        #         "lose_games":f"{lose_games}",
        #         "goals_for":f"{goals_for}",
        #         "goals_missed":f"{goals_missed}:",
        #         "goals_diff":f"{goals_diff}",
        #         "points":f"{points}",
        #         "name_teams":f"{name_teams}",
        #         "form_all":f"{form_all}",
        #         "logo_table":f"{logo_table}",
        #         }
    

    with open(f"/opt/footballBot/result/json/{league_id}_{rounds}_preview_round.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


# preview_round_text(18, 39)