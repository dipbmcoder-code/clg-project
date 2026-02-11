import requests
from API import check_match_round_api
from db import take_date_in_review, check_stat, get_user_id_main, check_stat_preview, total_of_round_name, insert_db, total_summ
from datetime import date, datetime
import os
from dotenv import load_dotenv
load_dotenv()

def main_start_review_round(rounds, league_id, season):

    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    # querystring = {"league":"39","season":"2022","round":"Regular Season - 12"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    # req_tour_review = requests.request("GET", url, headers=headers, params={
    #     "league":"39",
    #     "season":"2022",
    #     "round":"Regular Season - 11"
    # })

    # data_tour_review = req_tour_review.json()
    # #data_tour_review = check_match_round_api()
    # fixtures_matches = []
    # date_matches = []
    # for find_matches in range(len(data_tour_review['response'])):
    #     fixtures_matches.append(data_tour_review['response'][find_matches]['fixture']['id'])
    #     date_matches.append(datetime.strptime(data_tour_review['response'][find_matches]['fixture']['date'][:16], "%Y-%m-%dT%H:%M"))


    # date_matches.sort()

    insert_query = (
        f"SELECT rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds FROM round_preview WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_for_review = check_stat_preview(insert_query)

    index_for_review = index_for_review[0]
    rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, new_date, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds = index_for_review

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
    future_fixture_round = future_fixture_round.replace("+", " ").split()
    future_date_round = future_date_round.replace("+", " ").split()
    
    
    # first_date_tour = date_matches[0]
    # last_date_tour = date_matches[-1]

    #Вытаскиваем с апи команду лидера
    n_round = int(rounds) + 1

    if league_id != '1':
        round_for_api = f"Regular Season - {rounds}"
        next_round = f"Regular Season - {n_round}"
    elif league_id == '1':
        round_for_api = f"Group Stage - {rounds}"
        next_round = f"Group Stage - {n_round}"

    url = os.getenv('RAPID_API_BASE_URL')+"/standings"

    req_leader = requests.request("GET", url, headers=headers, params={
        "season":season,
        "league":league_id
        })
    data_leader = req_leader.json()
    name_leader_in_table = data_leader['response'][0]['league']['standings'][0][0]['team']['name']
    


    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    req_tour_review = requests.request("GET", url, headers=headers, params={
        "league":league_id,
        "season":season,
        "round":round_for_api
    })

    data_tour_review = req_tour_review.json()

    
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures/rounds"


    req_all_rounds = requests.get(url, headers=headers, params={
        "league":league_id,
        "season":season
        })
    data_all_rounds = req_all_rounds.json()


    all_rounds = len(data_all_rounds['response'])
    
    

    id_fixture_leader_game = ''
    for find_rival_team_leader in range(len(data_tour_review['response'])):
        if name_leader_in_table == data_tour_review['response'][find_rival_team_leader]['teams']['home']['name'] or \
        name_leader_in_table == data_tour_review['response'][find_rival_team_leader]['teams']['away']['name']:
            id_fixture_leader_game = data_tour_review['response'][find_rival_team_leader]['fixture']['id']
    
    #Тут делаем запрос в бд по игре лидера
    #Запрос(против кого играл, счет)
    print(id_fixture_leader_game)
    insert_query = (
        f'SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE fixture_match_for_check={id_fixture_leader_game}'
    )

    index = take_date_in_review(insert_query)
    index = index[0]

    team1, team2, goal_home, goal_away = index[0], index[1], index[2], index[3]
    team_home_leader, team_away_rival, team_away_leader, team_home_rival = '', '', '', ''

    count_leader_game_home = 0
    count_leader_game_away = 0

    if team1 == name_leader_in_table:
        team_home_leader = team1
        team_away_rival = team2
        goal_leader = goal_home
        goal_rival = goal_away
        count_leader_game_home += 1

    elif team2 == name_leader_in_table:
        team_home_leader = team2
        team_away_rival = team1
        goal_leader = goal_away
        goal_rival = goal_home
        count_leader_game_away += 1

    
    
    for del_leader_fix in range(len(future_fixture_round)):
        if future_fixture_round[del_leader_fix] == str(id_fixture_leader_game):
            del future_fixture_round[del_leader_fix]
            break

    #Делаем запрос в бд по всем остальным матчам тура и достаем инфу
    #Запрос(кто играли и счет)
    name_home_review = []
    name_away_review = []
    goals_home = []
    goals_away = []
    who_scored_home = []
    who_scored_away = []
    print(future_fixture_round)
    for find_tour_matches in range(len(future_fixture_round)):
        insert_query = (
            f"SELECT name_home_review, name_away_review, goals_home, goals_away, player_home_goal, player_away_goal FROM match_review WHERE fixture_match_for_check={future_fixture_round[find_tour_matches]} AND fixture_match_for_check != {id_fixture_leader_game};"
        )
        
        index1 = take_date_in_review(insert_query)
        
        index1 = index1[0]
      
        name_home_review.append(index1[0])
        name_away_review.append(index1[1])
        goals_home.append(index1[2])
        goals_away.append(index1[3])
        who_scored_home.append(index1[4])
        who_scored_away.append(index1[5])


    count_home = 0
    count_away = 0
    count_draw = 0
    for count in range(len(goals_home)):
        if int(goals_home[count]) > int(goals_away[count]):
            count_home += 1
        elif int(goals_home[count]) < int(goals_away[count]):
            count_away += 1
        elif int(goals_home[count]) == int(goals_away[count]):
            count_draw += 1
    
    count_home = count_home + count_leader_game_home
    count_away = count_away + count_leader_game_away
    if count_leader_game_home == count_leader_game_away :
        count_draw += 1

    #Пока пропускаю
    # Самая интересная статистика дня матча:
    #Хетрики и тд
    # All goals of season
    insert_query_goals_of_season = (f"SELECT goals FROM teams WHERE league_id = {league_id} AND season = {season}")
    all_goals_of_season = check_stat_preview(insert_query_goals_of_season)

    result = 0
    for i in range(len(all_goals_of_season)):
        result = int(all_goals_of_season[i][0]) + result
    all_goals_of_season = result    
    # Все голы за тур
    last_round = int(rounds) - 1
    all_goals_previous_round = total_summ('goals', league_id, last_round)
    # all_goals_previous_round = get_user_id_main('goals', last_round, league_id, '2022', 'summ')
    all_goals_round = get_user_id_main('goals', rounds, league_id, '2022', 'summ')
    h3 = get_user_id_main('goals', rounds, league_id, '2022', 'h3')  #LIST   0 - name, 1 - max(goals), 2 - team_id, 3 - fixture_match
    
    h3_amounts_list, h3_names_list, h3_team_names_list, h3_fixture_match_list = h3[1], h3[0], h3[2], h3[3]
    
    h3_amounts_list = " ".join(h3_amounts_list)
    h3_names_list = "+".join(h3_names_list)
    h3_team_names_list = "+".join(h3_team_names_list)
    h3_fixture_match_list = " ".join(h3_fixture_match_list)
    
    all_penalty_round = get_user_id_main('penalty', rounds, league_id, '2022', 'summ')

    # кто забивал в этом туре
    # insert_query_who_scrored_of_round = (
    #     f"SELECT name, goals AS S FROM players_round WHERE league_id = {league_id} AND season = {season} AND round = {rounds} AND goals != 0 GROUP BY name, goals ORDER BY S DESC;"
    #     )
    # who_scrored_of_round= check_stat_preview(insert_query_who_scrored_of_round)
    
    # list_name_who_scrored_of_round = []
    # goals_who_scrored_of_round = []
    
    # for i in range(len(who_scrored_of_round)):
    #     name = who_scrored_of_round[i][0]
    #     if ' ' in name:
    #         name = str(name).replace(" ", "_")
    #     list_name_who_scrored_of_round.append(name)
    #     goals_who_scrored_of_round.append(str(who_scrored_of_round[i][1]))

    # list_name_who_scrored_of_round = "+".join(list_name_who_scrored_of_round)   # Готовый список
    # goals_who_scrored_of_round = " ".join(goals_who_scrored_of_round)   # Готовый список

#   Наибольшое количество сейвов за матч
    # insert_query_max_saves_of_round= (
    #     f"SELECT name, max(saves), fixture_match, round, team_id AS S, name FROM players_round WHERE league_id = {league_id} AND season = {season} AND round = {rounds} AND saves != 0 GROUP BY name, saves, fixture_match, round, team_id ORDER BY S DESC LIMIT 1;"
    #     )

    insert_query_max_saves_of_round= (
        f"SELECT fixture_match, name, team_id, round, max(saves) AS S, name FROM players_round WHERE league_id = {league_id} AND season = {season} AND round = {rounds} AND saves != 0 GROUP BY fixture_match, name, team_id, round ORDER BY S DESC LIMIT 1;"
        )
    max_saves_of_round= check_stat_preview(insert_query_max_saves_of_round)  #   [('David Raya', 7, 868066)]
    
    max_saves_of_round = max_saves_of_round[0]
    
    amount_max_saves_of_round = max_saves_of_round[4]
    name_max_saves_of_round = max_saves_of_round[1]
    fixture_max_saves_of_round = max_saves_of_round[0]
    round_max_saves_of_round = max_saves_of_round[3]
    team_id_max_saves_of_round = max_saves_of_round[2]
    


    insert_query_max_saves_of_round= (
        f"SELECT name FROM teams WHERE team_id_api={team_id_max_saves_of_round};"
        )
    index_find_team_max_saves = check_stat_preview(insert_query_max_saves_of_round)
    index_find_team_max_saves = index_find_team_max_saves[0]
    
    insert_query_max_saves_of_round= (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away, date_match3 FROM match_review WHERE fixture_match_for_check={fixture_max_saves_of_round};"
        )
    index_find_match_max_saves = check_stat_preview(insert_query_max_saves_of_round)
    
    index_find_match_max_saves = index_find_match_max_saves[0]
    

    main_team_max_saves = ''
    rival_team_max_saves = ''
    goals_main = ''
    goals_rival = ''
    date_game_max_saves = index_find_match_max_saves[4]
    print(date_game_max_saves)

    if index_find_team_max_saves[0] == index_find_match_max_saves[0]:
        rival_team_max_saves = index_find_match_max_saves[1]
        main_team_max_saves = index_find_match_max_saves[0]
        goals_main = index_find_match_max_saves[2]
        goals_rival = index_find_match_max_saves[3]
    elif index_find_team_max_saves[0] == index_find_match_max_saves[1]:
        rival_team_max_saves = index_find_match_max_saves[0]
        main_team_max_saves = index_find_match_max_saves[1]
        goals_main = index_find_match_max_saves[3]
        goals_rival = index_find_match_max_saves[2]

    goals_and_info_max_saves = ''
    if goals_main > goals_rival:
        goals_and_info_max_saves = f"won {goals_main} - {goals_rival}"
    elif goals_main < goals_rival:
        goals_and_info_max_saves = f"lose {goals_main} - {goals_rival}"
    elif goals_main == goals_rival:
        goals_and_info_max_saves = f"draw {goals_main} - {goals_rival}"
    
    # insert_query_max_fouls_of_round = (
    #     f"SELECT name, max(y_cards) AS S, fixture_match FROM players_round WHERE league_id = {league_id} AND season = {season} AND round = {rounds} AND y_cards != 0 GROUP BY name, saves, fixture_match ORDER BY S DESC LIMIT 1;"
    #     )
    # max_fouls_of_round= check_stat_preview(insert_query_max_fouls_of_round)  #   [('David Raya', 1, 868066)]

    # max_fouls_of_round = max_fouls_of_round[0]
    
    # amount_max_fouls_of_round = max_fouls_of_round[1]
    # name_max_fouls_of_round = max_fouls_of_round[0]
    # fixture_max_fouls_of_round = max_fouls_of_round[2]

    # insert_query_max_fouls_of_round = (
    #     f"SELECT name_home_review, name_away_review, goals_home, goals_away, max(total_cards_in_game), count_yel_card, count_red_card AS B, count_yel_card, count_red_card FROM match_review WHERE league={league_id} GROUP BY name_home_review, name_away_review, goals_home, goals_away, count_yel_card, count_red_card ORDER BY B DESC LIMIT 1;"
    # )
    insert_query_max_fouls_of_round = (
        f"SELECT fixture_match, max(total_cards_in_game) AS B FROM match_review WHERE league={league_id} GROUP BY fixture_match ORDER BY B DESC LIMIT 1;"
    )
    index_find_top_fouls_season = check_stat_preview(insert_query_max_fouls_of_round)
    
    index_find_top_fouls_season = index_find_top_fouls_season[0]

    fix_match_top_fouls_of_round, count_top_fouls_of_round = index_find_top_fouls_season[0], index_find_top_fouls_season[1]

    insert_query_max_fouls_of_round = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away, count_yel_card, count_red_card FROM match_review WHERE fixture_match_for_check={fix_match_top_fouls_of_round} ;"
    )

    index_find_top_fouls_season1 = check_stat_preview(insert_query_max_fouls_of_round)
    
    index_find_top_fouls_season1 = index_find_top_fouls_season1[0]
    top_fouls_team_name_home , top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, top_fouls_total_yel_card, top_fouls_total_red_card = index_find_top_fouls_season1[0], index_find_top_fouls_season1[1], index_find_top_fouls_season1[2], index_find_top_fouls_season1[3], index_find_top_fouls_season1[4], index_find_top_fouls_season1[5]



    insert_query_top3_fouls_players_of_season = (
        f"SELECT name, max(y_cards) AS S, team_id, r_cards FROM players WHERE league_id = {league_id} AND season = {season} AND y_cards != 0 GROUP BY name, team_id, r_cards ORDER BY S DESC LIMIT 3;"
        )
    top3_fouls_players_of_season= check_stat_preview(insert_query_top3_fouls_players_of_season)  #   [('David Raya', 1, 868066)]
    
    name_top3_fouls_of_season = []
    ycards_top3_fouls_of_season = []
    rcards_top3_fouls_of_season = []
    id_team_cards_top3_fouls_of_season = []

    for i in range(len(top3_fouls_players_of_season)):
        r_card = top3_fouls_players_of_season[i][3]
        name_top3_fouls = top3_fouls_players_of_season[i][0]
        id_team_cards_top3_fouls_of_season1 = top3_fouls_players_of_season[i][2]
        if r_card == None:
            r_card = 0
        name_top3_fouls_of_season.append(name_top3_fouls.replace(" ", "_"))
        ycards_top3_fouls_of_season.append(top3_fouls_players_of_season[i][1])
        rcards_top3_fouls_of_season.append(r_card)
        id_team_cards_top3_fouls_of_season.append(id_team_cards_top3_fouls_of_season1)

    name_teams_cards_top3_fouls_of_season = []
    for find_team_for_top3_cards in range(len(id_team_cards_top3_fouls_of_season)):
        insert_query_top3_fouls_players_of_season = (
            f"SELECT name FROM teams WHERE team_id_api={id_team_cards_top3_fouls_of_season[find_team_for_top3_cards]}"
        )
        index_find_teams_for_top3_cards= check_stat_preview(insert_query_top3_fouls_players_of_season)
        index_find_teams_for_top3_cards = index_find_teams_for_top3_cards[0][0]
        name_teams_cards_top3_fouls_of_season.append(index_find_teams_for_top3_cards.replace(" ", "_"))
    
    
    
#TODO BETA Сделать по fixture_id
    insert_query_injuries= (
        f"SELECT sum(injuries) FROM players_round WHERE league_id = {league_id} AND injuries != 0 AND round = {rounds};"
        )
    
    count_injuries = check_stat_preview(insert_query_injuries)
    if count_injuries[0][0] != None:
        count_injuries = count_injuries[0]
        round_injuries = count_injuries[0]
    else:
        count_injuries = '0'
        round_injuries = '0'

    #average_injuries_in_round = int(round_injuries) // int(len(preview_home_teams))

    insert_query_injuries= (
        f"SELECT sum(injuries) FROM players_round WHERE league_id = {league_id} AND injuries != 0 AND season = {season};"
        )
    index_injuries_season = check_stat_preview(insert_query_injuries)
    print(index_injuries_season)
    if index_injuries_season[0][0] != None:
        index_injuries_season = index_injuries_season[0]
        season_injuries = index_injuries_season[0]

        average_injuries_in_round = int(season_injuries) // int(rounds)
    else:
        season_injuries = '0'
        average_injuries_in_round = '0'

    insert_query_injuries = (
    f"SELECT max(injuries_count) AS K, name FROM teams_round WHERE league_id={league_id} AND round={rounds} GROUP BY name ORDER BY K DESC LIMIT 1;"
    )
    index_injuries_team_round = check_stat_preview(insert_query_injuries)
    if index_injuries_team_round[0][0] != None:
        index_injuries_team_round = index_injuries_team_round[0]

        top_round_injuries_amount, top_round_injuries_name_team = index_injuries_team_round[0], index_injuries_team_round[1]
    else:
        top_round_injuries_amount, top_round_injuries_name_team = '0', '0'


    insert_query_destroyer = (
            f"SELECT max(destroyer_total) AS S, team_id_api FROM teams_round WHERE league_id = {league_id} AND season = {season} AND destroyer_total != 0 AND round = {rounds} GROUP BY team_id_api ORDER BY S DESC LIMIT 1;"
        )
    max_destroyer= check_stat_preview(insert_query_destroyer) 
    team_id_max_destroyer = max_destroyer[0][1]
    amount_max_destroyer = max_destroyer[0][0]

    insert_query_destroyer = (
            f"SELECT name FROM teams_round WHERE team_id_api={team_id_max_destroyer};"
        )
    index_find_team_destroyer = check_stat_preview(insert_query_destroyer) 
    index_find_team_destroyer = index_find_team_destroyer[0]
    team_top_destroyer = index_find_team_destroyer[0]
    
    

    insert_query_destroyer = (
            f"SELECT interceptions, blocks, tackles, saves FROM teams_round WHERE league_id = {league_id} AND season = {season} AND team_id_api = {team_id_max_destroyer} AND round = {rounds};"
        )
    data_for_max_destroyer= check_stat_preview(insert_query_destroyer) 
    data_for_max_destroyer = data_for_max_destroyer[0] #(8, 9, 23, 5)

    destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves = data_for_max_destroyer[0], data_for_max_destroyer[1], data_for_max_destroyer[2], data_for_max_destroyer[3]
    
    insert_query_destroyer = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE id_team_home_review={team_id_max_destroyer} OR id_team_away_review={team_id_max_destroyer} AND round={rounds}"
    )
    index_find_game_destroyer = check_stat_preview(insert_query_destroyer)
    index_find_game_destroyer = index_find_game_destroyer[0]
    team_main_destroyer = ''
    team_rival_destroyer = ''
    goals_main_destroyer = ''
    goals_rival_destroyer = ''
    
    if team_top_destroyer == index_find_game_destroyer[0]:
        team_main_destroyer = index_find_game_destroyer[0]
        team_rival_destroyer = index_find_game_destroyer[1]
        goals_main_destroyer = index_find_game_destroyer[2]
        goals_rival_destroyer = index_find_game_destroyer[3]

    elif team_top_destroyer == index_find_game_destroyer[1]:
        team_main_destroyer = index_find_game_destroyer[1]
        team_rival_destroyer = index_find_game_destroyer[0]
        goals_main_destroyer = index_find_game_destroyer[3]
        goals_rival_destroyer = index_find_game_destroyer[2]


    insert_query_destroyer = (
            f"SELECT max(destroyer_total) AS S, name FROM teams WHERE league_id = {league_id} AND season = {season} AND destroyer_total != 0 GROUP BY name ORDER BY S DESC LIMIT 1;"
        )
    max_destroyer_of_season= check_stat_preview(insert_query_destroyer)
    #DESTROY
    max_destroyer_of_season_amount =  max_destroyer_of_season[0][0]
    max_destroyer_of_season_name =  max_destroyer_of_season[0][1]

    max_destroyer_of_season_amount = int(max_destroyer_of_season_amount) #TODO123






    insert_query_creator = (
            f"SELECT max(creator_total) AS S, team_id_api FROM teams_round WHERE league_id = {league_id} AND season = {season} AND creator_total != 0 AND round = {rounds} GROUP BY team_id_api ORDER BY S DESC LIMIT 1;"
        )
    max_creator= check_stat_preview(insert_query_creator) 
    team_id_max_creator = max_creator[0][1]
    amount_max_creator = max_creator[0][0]

    insert_query_creator = (
            f"SELECT name FROM teams_round WHERE team_id_api={team_id_max_creator};"
        )
    index_find_team_creator = check_stat_preview(insert_query_creator) 
    index_find_team_creator = index_find_team_creator[0]
    team_top_creator = index_find_team_creator[0]

    insert_query_creator = (
            f"SELECT duels, shots_on_target, shots_of_target FROM teams_round WHERE league_id = {league_id} AND season = {season} AND team_id_api = {team_id_max_creator} AND round = {rounds};"
        )
    data_for_max_creator= check_stat_preview(insert_query_creator) 
    data_for_max_creator = data_for_max_creator[0] #(110, 4, 8)
    creator_duels, creator_shots_on_target, creator_shots_off_target = data_for_max_creator[0], data_for_max_creator[1], data_for_max_creator[2]


    insert_query_creator = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE id_team_home_review={team_id_max_creator} OR id_team_away_review={team_id_max_creator} AND round={rounds}"
    )
    index_find_game_creator = check_stat_preview(insert_query_creator)
    index_find_game_creator = index_find_game_creator[0]

    team_main_creator = ''
    team_rival_creator = ''
    goals_main_creator = ''
    goals_rival_creator = ''
    
    if team_top_creator == index_find_game_creator[0]:
        team_main_creator = index_find_game_creator[0]
        team_rival_creator = index_find_game_creator[1]
        goals_main_creator = index_find_game_creator[2]
        goals_rival_creator = index_find_game_creator[3]

    elif team_top_creator == index_find_game_creator[1]:
        team_main_creator = index_find_game_creator[1]
        team_rival_creator = index_find_game_creator[0]
        goals_main_creator = index_find_game_creator[3]
        goals_rival_creator = index_find_game_creator[2]


    insert_query_creator = (
            f"SELECT max(creator_total) AS S, name FROM teams WHERE league_id = {league_id} AND season = {season} AND creator_total != 0 GROUP BY name ORDER BY S DESC LIMIT 1;"
        )
    max_creator_of_season= check_stat_preview(insert_query_creator) 
    max_creator_of_season_amount =  max_creator_of_season[0][0]
    max_creator_of_season_name =  max_creator_of_season[0][1]


    


    #Если мы посмотрим на 5 лучших бомбардиров лиги 
    # insert_query = (
    #     f'SELECT topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, topscorer_team_in_league_4, topscorer_team_in_league_5 FROM match_review WHERE fixture_match_for_check={future_fixture_round[-1]};'
    # )

    # index2 = take_date_in_review(insert_query)
    # index2 = index2[0]

    # topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, topscorer_team_in_league_4, topscorer_team_in_league_5 = index2[0], index2[1], index2[2], index2[3], index2[4], index2[5], index2[6], index2[7], index2[8], index2[9], index2[10], index2[11], index2[12], index2[13], index2[14]

    # topscorer_name_in_league_1 = topscorer_name_in_league_1.replace(" ", "")
    # topscorer_name_in_league_2 = topscorer_name_in_league_2.replace(" ", "")
    # topscorer_name_in_league_3 = topscorer_name_in_league_3.replace(" ", "")
    # topscorer_name_in_league_4 = topscorer_name_in_league_4.replace(" ", "")
    # topscorer_name_in_league_5 = topscorer_name_in_league_5.replace(" ", "")


    # topscorer_team = []
    # topscorer_team.append(topscorer_team_in_league_1)
    # topscorer_team.append(topscorer_team_in_league_2)
    # topscorer_team.append(topscorer_team_in_league_3)
    # topscorer_team.append(topscorer_team_in_league_4)
    # topscorer_team.append(topscorer_team_in_league_5)
    # topscorer_name = []
    # topscorer_name.append(topscorer_name_in_league_1)
    # topscorer_name.append(topscorer_name_in_league_2)
    # topscorer_name.append(topscorer_name_in_league_3)
    # topscorer_name.append(topscorer_name_in_league_4)
    # topscorer_name.append(topscorer_name_in_league_5)
    # count_top = [0, 0, 0, 0, 0]
    # count_all = []

    # def check_goals_top_players(team, name, count):
    #     test = []
    #     for find_team in range(len(name_home_review)):
    #         if team == name_home_review[find_team]:
    #             for i in range(len(who_scored_home)):
    #                 for find_goals in range(len(who_scored_home[i].replace("+", " ").replace("_", "").split())):
    #                     if name in who_scored_home[i].replace("+", " ").replace("_", "").split()[find_goals]:
    #                         count += 1
    #         elif team == name_away_review[find_team]:
    #             for i in range(len(who_scored_away)):
    #                 for find_goals in range(len(who_scored_away[i].replace("+", " ").replace("_", "").split())):
    #                     if name in who_scored_away[i].replace("+", " ").replace("_", "").split()[find_goals]:
    #                         count += 1    
    #     test.append(count)
    #     return test

    # for find_top_scorers in range(5):
    #     check_goals_top_players(topscorer_team[find_top_scorers], topscorer_name[find_top_scorers], count_top[find_top_scorers])

    # count_all = check_goals_top_players
    # count_top1 = count_all[0]
    # count_top2 = count_all[1]
    # count_top3 = count_all[2]
    # count_top4 = count_all[3]
    # count_top5 = count_all[4]

     
    insert_query = (
        f"SELECT max(goals) AS S , name, team_id FROM players WHERE league_id={league_id} AND goals != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
    )
    index_top_player_goals = check_stat_preview(insert_query)
    goals1 = index_top_player_goals[0]
    goals2 = index_top_player_goals[1]
    goals3 = index_top_player_goals[2]
    goals4 = index_top_player_goals[3]
    goals5 = index_top_player_goals[4]

    goals_top_league_1, name_top_goals_league_1, team_id_top_goals_league1  = goals1[0], goals1[1], goals1[2]
    goals_top_league_2, name_top_goals_league_2, team_id_top_goals_league2  = goals2[0], goals2[1], goals2[2]
    goals_top_league_3, name_top_goals_league_3, team_id_top_goals_league3 = goals3[0], goals3[1], goals3[2]
    goals_top_league_4, name_top_goals_league_4, team_id_top_goals_league4 = goals4[0], goals4[1], goals4[2]
    goals_top_league_5, name_top_goals_league_5, team_id_top_goals_league5 = goals5[0], goals5[1], goals5[2]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league1};"
    )
    index_top_goals_team1 = check_stat_preview(insert_query)
    index_top_goals_team1 = index_top_goals_team1[0]
    team_top_goals_league1_1 = index_top_goals_team1[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league2};"
    )
    index_top_goals_team2 = check_stat_preview(insert_query)
    index_top_goals_team2 = index_top_goals_team2[0]
    team_top_goals_league2_1 = index_top_goals_team2[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league3};"
    )
    index_top_goals_team3 = check_stat_preview(insert_query)
    index_top_goals_team3 = index_top_goals_team3[0]
    team_top_goals_league3_1 = index_top_goals_team3[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league4};"
    )
    index_top_goals_team4 = check_stat_preview(insert_query)
    index_top_goals_team4 = index_top_goals_team4[0]
    team_top_goals_league4_1 = index_top_goals_team4[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league5};"
    )
    index_top_goals_team5 = check_stat_preview(insert_query)
    index_top_goals_team5 = index_top_goals_team5[0]
    team_top_goals_league5_1 = index_top_goals_team5[0]



    # goals_top_league_1, name_top_goals_league_1,team_top_goals_league1_1
    # goals_top_league_2, name_top_goals_league_2,team_top_goals_league2_1
    # goals_top_league_3, name_top_goals_league_3,team_top_goals_league3_1
    # goals_top_league_4, name_top_goals_league_4,team_top_goals_league4_1
    # goals_top_league_5, name_top_goals_league_5,team_top_goals_league5_1



    #Всего забили за тур
    #Запрос в бд на прошлые голы, чтобы посчитать процент
    # last_round = int(rounds) - 1

    # insert_query = (
    #     f'SELECT all_goals_round FROM players_round WHERE number_tour={last_round};'
    # )

    # index_all_goals_last_round = check_stat(insert_query)
    # index_all_goals_last_round = index_all_goals_last_round[0]

    # last_round_all_goals = index_all_goals_last_round[0]

    

    total_num = 0
    total_percent_round = 0
    # total_percent_last_round = 0
    # total_percent_draw = 0
 

    if all_goals_round > all_goals_previous_round:
        total_num = all_goals_round - all_goals_previous_round
        total_percent_round = (total_num / all_goals_round) * 100
        total_percent_round = f"+{int(total_percent_round)}"

    elif all_goals_round < all_goals_previous_round:
        total_num = all_goals_previous_round - all_goals_round
        total_percent_round = (total_num / all_goals_previous_round) * 100
        total_percent_round = f"-{int(total_percent_round)}"

    elif all_goals_round == all_goals_previous_round:
        total_percent_round = 0
        total_percent_round = f"{total_percent_round}"

    
    insert_query = (
        f"SELECT sum(penalty) AS S FROM players_round WHERE season={season} AND league_id={league_id} AND penalty != 0 ORDER BY S DESC LIMIT 1"
    )
    index_for_average_penalty = check_stat(insert_query)
    if index_for_average_penalty != []:
        index_for_average_penalty = index_for_average_penalty[0]
        sum_penalty_season = index_for_average_penalty[0]

    insert_query = (
        f"SELECT max(penalty) AS S, team_id FROM players_round WHERE season={season} AND league_id={league_id} AND penalty != 0 GROUP BY team_id ORDER BY S DESC LIMIT 1"
    )
    team_id_for_average_penalty, index_for_average_penalty2 = '', 0
    average_goals_in_season, average_penalty_in_season = 0, 0
    index_for_average_penalty2 = check_stat(insert_query) 
    print(index_for_average_penalty2)
    if index_for_average_penalty2 != []:
        index_for_average_penalty2 = index_for_average_penalty2[0]
        team_id_for_average_penalty = index_for_average_penalty2[1]

        insert_query1 = (
            f"SELECT COUNT(team_id_api) FROM teams_round WHERE team_id_api={team_id_for_average_penalty}"
        )
        index_count_games = check_stat(insert_query1)
        
        average_goals_in_season = all_goals_of_season // int(rounds)     #average_goals_in_season = all_goals_of_season // int(index_count_games[0][0])
        average_penalty_in_season = int(sum_penalty_season) // int(rounds)       #average_penalty_in_season = int(sum_penalty_season) // int(index_count_games[0][0])
        

    
    #Самый быстрый гол в туре
    insert_query = (
        f'SELECT name, min(fast_goal) AS S, team_id, fixture_match FROM players_round WHERE round={rounds} AND league_id={league_id} AND fast_goal != 0 GROUP BY name, team_id, fixture_match ORDER BY S ASC LIMIT 1;'
    )
    name_fast_goal, time_fast_goal, team_name_fast_goal, team_away_fast_goal, scrore_fast_goal = '' , 0, '', '', 0
    index_fast_goal = check_stat(insert_query)
    if index_fast_goal != []:
        index_fast_goal = index_fast_goal[0]

        insert_query = (
            f"SELECT name FROM teams WHERE team_id_api={index_fast_goal[2]};"
        )
        team_name_fast_goal = check_stat_preview(insert_query)
        name_fast_goal, time_fast_goal, team_name_fast_goal, fixture_fast_goal = index_fast_goal[0], index_fast_goal[1], team_name_fast_goal[0][0], index_fast_goal[3]
        insert_query = (
            f"SELECT goals_home, goals_away, name_home_review, name_away_review FROM match_review WHERE fixture_match_for_check = {fixture_fast_goal};"
        )
        fast_goal_game = check_stat_preview(insert_query)
        if team_name_fast_goal != fast_goal_game[0][2]:
            team_away_fast_goal = fast_goal_game[0][2]
            scrore_fast_goal = f"{fast_goal_game[0][0]} - {fast_goal_game[0][1]}"
            
        if team_name_fast_goal != fast_goal_game[0][3]:
            team_away_fast_goal = fast_goal_game[0][3]
            scrore_fast_goal = f"{fast_goal_game[0][1]} - {fast_goal_game[0][0]}"
    
    # insert_query = (
    #     f"SELECT goals_home, goals_away, name_home_review, name_away_review FROM teams WHERE team_id_api={index_fast_goal[2]};"
    # )
    # fast_goal_game = check_stat_preview(insert_query)
    # for i in range(len(fast_goal_game[0])):
        

    #Команда с лучшей точностью паса 

    # insert_query = (
    #                 f"SELECT name_home_review, team_home_passes_accurate, max(team_home_percent_passes_accurate), team_home_total_passes AS Q FROM match_review WHERE round={rounds} GROUP BY name_home_review ORDER BY Q DESC LIMIT 1;"
    #             )
    # index0 = check_stat(insert_query)
    # index0 = index0[0]

    # max_team_home_for_passes, team_home_max_passes_accurate, team_home_max_percent_passes_accurate, team_home_max_total_passes = index0[0], index0[1],index0[2], index0[3]

    # insert_query = (
    #                 f"SELECT name_away_review, team_away_passes_accurate, max(team_away_percent_passes_accurate), team_away_total_passes AS W FROM match_review WHERE round={rounds} GROUP BY name_away_review ORDER BY W DESC LIMIT 1;"
    #             )
    # index1 = check_stat(insert_query)
    # index1 = index1[0]

    # max_team_away_for_passes, team_away_max_passes_accurate, team_away_max_percent_passes_accurate, team_max_away_total_passes = index1[0], index1[1],index1[2], index1[3]

    # insert_query = (
    #                 f"SELECT name_home_review, team_home_passes_accurate, min(team_home_percent_passes_accurate), team_home_total_passes AS E FROM match_review WHERE round={rounds} GROUP BY name_home_review ORDER BY E DESC LIMIT 1;"
    #             )
    # index2 = check_stat(insert_query)
    # index2 = index2[0]

    # min_team_home_for_passes, team_home_min_passes_accurate, team_home_min_percent_passes_accurate, team_home_min_total_passes = index2[0], index2[1],index2[2], index2[3]

    # insert_query = (
    #                 f"SELECT name_away_review, team_away_passes_accurate, min(team_away_percent_passes_accurate), team_away_total_passes AS R FROM match_review WHERE round={rounds} GROUP BY name_away_review ORDER BY R DESC LIMIT 1;"
    #             )
    # index3 = check_stat(insert_query)
    # index3 = index3[0]

    # min_team_away_for_passes, team_away_min_passes_accurate, team_away_min_percent_passes_accurate, team_min_away_total_passes = index3[0], index3[1],index3[2], index3[3]
    #Команда с лучшей точностью паса 
    
    insert_query = (
        f"SELECT max(team_home_percent_passes_accurate), team_home_total_passes AS L, name_home_review FROM match_review WHERE round={rounds} AND league={league_id} GROUP BY team_home_total_passes, name_home_review ORDER BY L DESC LIMIT 1;"
    )
    index_find_max_percent_accurate_home = check_stat(insert_query)
    
    index_find_max_percent_accurate_home = index_find_max_percent_accurate_home[0]

    max_percent_accurate_home, total_passes_home, name_home_max_percent_accurate = index_find_max_percent_accurate_home[0], index_find_max_percent_accurate_home[1], index_find_max_percent_accurate_home[2]

    insert_query = (
        f"SELECT max(team_away_percent_passes_accurate), team_away_total_passes AS J, name_away_review FROM match_review WHERE round={rounds} AND league={league_id} GROUP BY team_away_total_passes, name_away_review ORDER BY J DESC LIMIT 1;"
    )
    index_find_max_percent_accurate_away = check_stat(insert_query)
    index_find_max_percent_accurate_away = index_find_max_percent_accurate_away[0]

    max_percent_accurate_away, total_passes_away, name_away_max_percent_accurate = index_find_max_percent_accurate_away[0], index_find_max_percent_accurate_away[1], index_find_max_percent_accurate_away[2]

    max_accurate_in_round = ''
    name_max_accurate_in_round = ''
    max_total_passes_with_accurate_in_round = ''
    if int(max_percent_accurate_home) > int(max_percent_accurate_away):
        max_accurate_in_round = max_percent_accurate_home
        name_max_accurate_in_round = name_home_max_percent_accurate
        max_total_passes_with_accurate_in_round = total_passes_home
    elif int(max_percent_accurate_home) < int(max_percent_accurate_away):
        max_accurate_in_round = max_percent_accurate_away
        name_max_accurate_in_round = name_away_max_percent_accurate
        max_total_passes_with_accurate_in_round = total_passes_away

    elif int(max_percent_accurate_home) == int(max_percent_accurate_away):
        max_accurate_in_round = max_percent_accurate_away
        name_max_accurate_in_round = name_away_max_percent_accurate
        max_total_passes_with_accurate_in_round = total_passes_away


    insert_query = (
        f"SELECT min(team_home_percent_passes_accurate), team_home_total_passes AS Z, name_home_review FROM match_review WHERE round={rounds} AND league={league_id} GROUP BY team_home_total_passes, name_home_review ORDER BY Z ASC LIMIT 1;"
    )
    index_find_min_percent_accurate_home = check_stat(insert_query)
    index_find_min_percent_accurate_home = index_find_min_percent_accurate_home[0]

    min_percent_accurate_home, min_total_passes_home, name_home_min_percent_accurate = index_find_min_percent_accurate_home[0], index_find_min_percent_accurate_home[1], index_find_min_percent_accurate_home[2]

    insert_query = (
        f"SELECT min(team_away_percent_passes_accurate), team_away_total_passes AS X, name_away_review FROM match_review WHERE round={rounds} AND league={league_id} GROUP BY team_away_total_passes, name_away_review ORDER BY X ASC LIMIT 1;"
    )
    index_find_min_percent_accurate_away = check_stat(insert_query)
    index_find_min_percent_accurate_away = index_find_min_percent_accurate_away[0]

    min_percent_accurate_away, min_total_passes_away, name_away_min_percent_accurate = index_find_min_percent_accurate_away[0], index_find_min_percent_accurate_away[1], index_find_min_percent_accurate_away[2]

    min_accurate_in_round = ''
    name_min_accurate_in_round = ''
    min_total_passes_with_accurate_in_round = ''
    if int(min_percent_accurate_home) < int(min_percent_accurate_away):
        min_accurate_in_round = min_percent_accurate_home
        name_min_accurate_in_round = name_home_min_percent_accurate
        min_total_passes_with_accurate_in_round = min_total_passes_home
    elif int(min_percent_accurate_home) > int(min_percent_accurate_away):
        min_accurate_in_round = min_percent_accurate_away
        name_min_accurate_in_round = name_away_min_percent_accurate
        min_total_passes_with_accurate_in_round = min_total_passes_away
    elif int(min_percent_accurate_home) == int(min_percent_accurate_away):
        min_accurate_in_round = min_percent_accurate_away
        name_min_accurate_in_round = name_away_min_percent_accurate
        min_total_passes_with_accurate_in_round = min_total_passes_away

    print(preview_away_teams)
    #Эффективность команд:
    #Команда с самой высокой точностью пасов
    team_id_home = []
    for find_team_id in range(len(preview_home_teams)):
        insert_query = (
            f"SELECT team_id_api FROM teams_round WHERE name LIKE '{preview_home_teams[find_team_id]}'"
        )

        index_find_team_id = check_stat(insert_query)
        
        team_id_home.append(index_find_team_id[0][0])
    
    for find_team_id2 in range(len(preview_away_teams)):
        insert_query = (
            f"SELECT team_id_api FROM teams_round WHERE name LIKE '{preview_away_teams[find_team_id2]}'"
        )

        index_find_team_id2 = check_stat(insert_query)
        
        team_id_home.append(index_find_team_id2[0][0])

    sum_accuracy = []
    sum_accuracy_name = []
    for find_sum_accuracy in range(len(team_id_home)):
        insert_query1 = (
            f"SELECT COUNT(team_id_api) FROM teams_round WHERE team_id_api={team_id_home[find_sum_accuracy]}"
        )
        index_count_games = check_stat(insert_query1)
        

        insert_query = (
            f"SELECT sum(precent_accuracy) AS W, name FROM teams_round WHERE team_id_api={team_id_home[find_sum_accuracy]}  GROUP BY name ORDER BY W DESC LIMIT 1;"
        )
        index_sum_accuracy = check_stat(insert_query)
        index_sum_accuracy = index_sum_accuracy[0]
        name_sum_a = index_sum_accuracy[1]
        sum_accuracy_name.append(name_sum_a.replace(" ", "_"))
        sum_accuracy.append(int(index_sum_accuracy[0]) // int(index_count_games[0][0]))
 
    
    
    name_max_accuracy_in_season = ''
    percent_max_accuracy_in_season = 0

    name_min_accuracy_in_season = ''
    percent_min_accuracy_in_season = 100
    
    for i in range(len(sum_accuracy)):
        if sum_accuracy[i] > percent_max_accuracy_in_season:
            name_max_accuracy_in_season = sum_accuracy_name[i]
            percent_max_accuracy_in_season = sum_accuracy[i]

    for k in range(len(sum_accuracy)):
        if sum_accuracy[k] < percent_min_accuracy_in_season:
            name_min_accuracy_in_season = sum_accuracy_name[k]
            percent_min_accuracy_in_season = sum_accuracy[k]
    
    

    #Самый длинный матч 
    insert_query = (
        f"SELECT fixture_match, max(match_lasted), referee_time AS M, referee_time FROM match_review WHERE league={league_id} AND round={rounds} GROUP BY fixture_match, referee_time ORDER BY M DESC LIMIT 1;"
    )
    index_find_longest_time = check_stat_preview(insert_query)
    referee_time_in_longest_game = ''
    if index_find_longest_time != []:
        index_find_longest_time = index_find_longest_time[0]

        referee_time_in_longest_game = index_find_longest_time[2]

    insert_query = (
        f"SELECT name_home_review, name_away_review FROM match_review WHERE fixture_match_for_check={index_find_longest_time[0]};"
    )
    index_long_match_teams = check_stat_preview(insert_query)
    longest_match_team_home, longest_match_team_away = '', ''
    print(index_long_match_teams)
    if index_long_match_teams != []:
        index_long_match_teams = index_long_match_teams[0]

        longest_match_team_home = index_long_match_teams[0]
        longest_match_team_away = index_long_match_teams[1]


    # Статистика игроков:
    #Вытаскиваем топ по сейвам

    insert_query = (
        f"SELECT max(goals) AS S , name, team_id FROM players WHERE league_id={league_id} AND goals != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
    )
    index_top_player_goals = check_stat_preview(insert_query)
    goals1 = index_top_player_goals[0]
    goals2 = index_top_player_goals[1]
    goals3 = index_top_player_goals[2]
    goals4 = index_top_player_goals[3]
    goals5 = index_top_player_goals[4]

    goals_top_league_1, name_top_goals_league_1, team_id_top_goals_league1  = goals1[0], goals1[1], goals1[2]
    goals_top_league_2, name_top_goals_league_2, team_id_top_goals_league2  = goals2[0], goals2[1], goals2[2]
    goals_top_league_3, name_top_goals_league_3, team_id_top_goals_league3 = goals3[0], goals3[1], goals3[2]
    goals_top_league_4, name_top_goals_league_4, team_id_top_goals_league4 = goals4[0], goals4[1], goals4[2]
    goals_top_league_5, name_top_goals_league_5, team_id_top_goals_league5 = goals5[0], goals5[1], goals5[2]

    #!!!!
    total_name_top_goals_league_1_round = total_of_round_name(name_top_goals_league_1, 'goals', rounds)
    if total_name_top_goals_league_1_round == None:
        total_name_top_goals_league_1_round = 0
    total_name_top_goals_league_2_round = total_of_round_name(name_top_goals_league_2, 'goals', rounds)
    if total_name_top_goals_league_2_round == None:
        total_name_top_goals_league_2_round = 0
    total_name_top_goals_league_3_round = total_of_round_name(name_top_goals_league_3, 'goals', rounds)
    if total_name_top_goals_league_3_round == None:
        total_name_top_goals_league_3_round = 0
    total_name_top_goals_league_4_round = total_of_round_name(name_top_goals_league_4, 'goals', rounds)
    if total_name_top_goals_league_4_round == None:
        total_name_top_goals_league_4_round = 0
    total_name_top_goals_league_5_round = total_of_round_name(name_top_goals_league_5, 'goals', rounds)
    if total_name_top_goals_league_5_round == None:
        total_name_top_goals_league_5_round = 0

    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league1};"
    )
    index_top_goals_team1 = check_stat_preview(insert_query)
    index_top_goals_team1 = index_top_goals_team1[0]
    team_top_goals_league1 = index_top_goals_team1[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league2};"
    )
    index_top_goals_team2 = check_stat_preview(insert_query)
    index_top_goals_team2 = index_top_goals_team2[0]
    team_top_goals_league2 = index_top_goals_team2[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league3};"
    )
    index_top_goals_team3 = check_stat_preview(insert_query)
    index_top_goals_team3 = index_top_goals_team3[0]
    team_top_goals_league3 = index_top_goals_team3[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league4};"
    )
    index_top_goals_team4 = check_stat_preview(insert_query)
    index_top_goals_team4 = index_top_goals_team4[0]
    team_top_goals_league4 = index_top_goals_team4[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_goals_league5};"
    )
    index_top_goals_team5 = check_stat_preview(insert_query)
    index_top_goals_team5 = index_top_goals_team5[0]
    team_top_goals_league5 = index_top_goals_team5[0]




    insert_query = (
        f"SELECT max(assists) AS S , name, team_id FROM players WHERE league_id={league_id} AND assists != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
    )
    index_top_assists_goals = check_stat_preview(insert_query)
    assists1 = index_top_assists_goals[0]
    assists2 = index_top_assists_goals[1]
    assists3 = index_top_assists_goals[2]
    assists4 = index_top_assists_goals[3]
    assists5 = index_top_assists_goals[4]

    assists_top_league_1, name_top_assists_league_1, team_id_top_assists_league1  = assists1[0], assists1[1], assists1[2]
    assists_top_league_2, name_top_assists_league_2, team_id_top_assists_league2 = assists2[0], assists2[1], assists2[2]
    assists_top_league_3, name_top_assists_league_3, team_id_top_assists_league3 = assists3[0], assists3[1], assists3[2]
    assists_top_league_4, name_top_assists_league_4, team_id_top_assists_league4 = assists4[0], assists4[1], assists4[2]
    assists_top_league_5, name_top_assists_league_5, team_id_top_assists_league5 = assists5[0], assists5[1], assists5[2]

#!!!!
    total_of_round_top_assists_league_1 = total_of_round_name(name_top_assists_league_1, 'assists',rounds)
    if total_of_round_top_assists_league_1 == None:
        total_of_round_top_assists_league_1 = 0
    total_of_round_top_assists_league_2 = total_of_round_name(name_top_assists_league_2, 'assists', rounds)
    if total_of_round_top_assists_league_2 == None:
        total_of_round_top_assists_league_2 = 0
    total_of_round_top_assists_league_3 = total_of_round_name(name_top_assists_league_3, 'assists', rounds)
    if total_of_round_top_assists_league_3 == None:
        total_of_round_top_assists_league_3 = 0
    total_of_round_top_assists_league_4 = total_of_round_name(name_top_assists_league_4, 'assists', rounds)
    if total_of_round_top_assists_league_4 == None:
        total_of_round_top_assists_league_4 = 0
    total_of_round_top_assists_league_5 = total_of_round_name(name_top_assists_league_5, 'assists', rounds)
    if total_of_round_top_assists_league_5 == None:
        total_of_round_top_assists_league_5 = 0
     
    

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_assists_league1};"
    )
    index_top_assists_team1 = check_stat_preview(insert_query)
    index_top_assists_team1 = index_top_assists_team1[0]
    team_top_assists_league1 = index_top_assists_team1[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_assists_league2};"
    )
    index_top_assists_team2 = check_stat_preview(insert_query)
    index_top_assists_team2 = index_top_assists_team2[0]
    team_top_assists_league2 = index_top_assists_team2[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_assists_league3};"
    )
    index_top_assists_team3 = check_stat_preview(insert_query)
    index_top_assists_team3 = index_top_assists_team3[0]
    team_top_assists_league3 = index_top_assists_team3[0]
    
    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_assists_league4};"
    )
    index_top_assists_team4 = check_stat_preview(insert_query)
    index_top_assists_team4 = index_top_assists_team4[0]
    team_top_assists_league4 = index_top_assists_team4[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_assists_league5};"
    )
    index_top_assists_team5 = check_stat_preview(insert_query)
    index_top_assists_team5 = index_top_assists_team5[0]
    team_top_assists_league5 = index_top_assists_team5[0]
    



    insert_query = (
        f"SELECT max(saves) AS S , name, team_id FROM players WHERE league_id={league_id} AND saves != 0 GROUP BY name, team_id ORDER BY S DESC LIMIT 5;"
    )
    index_top_saves_goals = check_stat_preview(insert_query)
    saves1 = index_top_saves_goals[0]
    saves2 = index_top_saves_goals[1]
    saves3 = index_top_saves_goals[2]
    saves4 = index_top_saves_goals[3]
    saves5 = index_top_saves_goals[4]

    saves_top_league_1, name_top_saves_league_1, team_id_top_saves_league1 = saves1[0], saves1[1], saves1[2]
    saves_top_league_2, name_top_saves_league_2, team_id_top_saves_league2 = saves2[0], saves2[1], saves2[2]
    saves_top_league_3, name_top_saves_league_3, team_id_top_saves_league3 = saves3[0], saves3[1], saves3[2]
    saves_top_league_4, name_top_saves_league_4, team_id_top_saves_league4 = saves4[0], saves4[1], saves4[2]
    saves_top_league_5, name_top_saves_league_5, team_id_top_saves_league5 = saves5[0], saves5[1], saves5[2]
#!!!!
    total_of_round_top_saves_league_1 = total_of_round_name(name_top_saves_league_1, 'saves', rounds)
    if total_of_round_top_saves_league_1 == None:
        total_of_round_top_saves_league_1 = 0
    total_of_round_top_saves_league_2 = total_of_round_name(name_top_saves_league_2, 'saves', rounds)
    if total_of_round_top_saves_league_2 == None:
        total_of_round_top_saves_league_2 = 0
    total_of_round_top_saves_league_3 = total_of_round_name(name_top_saves_league_3, 'saves', rounds)
    if total_of_round_top_saves_league_3 == None:
        total_of_round_top_saves_league_3 = 0
    total_of_round_top_saves_league_4 = total_of_round_name(name_top_saves_league_4, 'saves', rounds)
    if total_of_round_top_saves_league_4 == None:
        total_of_round_top_saves_league_4 = 0
    total_of_round_top_saves_league_5 = total_of_round_name(name_top_saves_league_5, 'saves', rounds)
    if total_of_round_top_saves_league_5 == None:
        total_of_round_top_saves_league_5 = 0

    
    

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_saves_league1};"
    )
    index_top_saves_team1 = check_stat_preview(insert_query)
    index_top_saves_team1 = index_top_saves_team1[0]
    team_top_saves_league1 = index_top_saves_team1[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_saves_league2};"
    )
    index_top_saves_team2 = check_stat_preview(insert_query)
    index_top_saves_team2 = index_top_saves_team2[0]
    team_top_saves_league2 = index_top_saves_team2[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_saves_league3};"
    )
    index_top_saves_team3 = check_stat_preview(insert_query)
    index_top_saves_team3 = index_top_saves_team3[0]
    team_top_saves_league3 = index_top_saves_team3[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_saves_league4};"
    )
    index_top_saves_team4 = check_stat_preview(insert_query)
    index_top_saves_team4 = index_top_saves_team4[0]
    team_top_saves_league4 = index_top_saves_team4[0]

    insert_query = (
        f"SELECT name FROM teams WHERE team_id_api={team_id_top_saves_league5};"
    )
    index_top_saves_team5 = check_stat_preview(insert_query)
    index_top_saves_team5 = index_top_saves_team5[0]
    team_top_saves_league5 = index_top_saves_team5[0]

    rank_for_table = []
    name_table_team = []
    form_table = []
    all_matches_table = []
    win_matches_table = []
    draw_matches_table = []
    lose_matches_table = []
    goals_scored_for_table = []
    goals_missed_for_table = []
    goals_diff_table = []
    points_for_table = []
    logo_for_table = []

    for find_rank in range(len(data_leader['response'][0]['league']['standings'][0])):
        rank_for_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['rank']))
        name_table_team.append(data_leader['response'][0]['league']['standings'][0][find_rank]['team']['name'])
        form_table.append(data_leader['response'][0]['league']['standings'][0][find_rank]['form'])
        all_matches_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['played']))
        win_matches_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['win']))
        draw_matches_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['draw']))
        lose_matches_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['lose']))
        goals_scored_for_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['goals']['for']))
        goals_missed_for_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['all']['goals']['against']))
        goals_diff_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['goalsDiff']))
        points_for_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['points']))
        logo_for_table.append(str(data_leader['response'][0]['league']['standings'][0][find_rank]['team']['logo']))

    max_destroyer_of_season_amount = int(max_destroyer_of_season_amount) / int(all_matches_table[name_table_team.index(max_destroyer_of_season_name)])
    max_destroyer_of_season_amount = round(max_destroyer_of_season_amount)

    max_creator_of_season_amount = int(max_creator_of_season_amount) / int(all_matches_table[name_table_team.index(max_creator_of_season_name)])
    max_creator_of_season_amount = round(max_creator_of_season_amount)

    #Find next Match Day
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"
    req_next_round = requests.get( url, headers=headers, params={
        "league":league_id,
        "season":season,
        "round":next_round
        })
    
    
    data_next_round = req_next_round.json()

    date_next_round = data_next_round['response'][0]['fixture']['date'][:16]
    arena_next_round = data_next_round['response'][0]['fixture']['venue']['name']
    first_team_home_next_round = data_next_round['response'][0]['teams']['home']['name']
    first_team_away_next_round = data_next_round['response'][0]['teams']['away']['name']
    city_next_round = data_next_round['response'][0]['fixture']['venue']['city']
    
    
    rank_for_table = ' '.join(rank_for_table)
    name_table_team = '+'.join(name_table_team)
    name_table_team = name_table_team.replace(" ", "_")
    logo_for_table = '+'.join(logo_for_table)
    logo_for_table = logo_for_table.replace(" ", "_")
    form_table = '+'.join(form_table)
    form_table = form_table.replace(" ", "_")
    all_matches_table = ' '.join(all_matches_table)
    win_matches_table = ' '.join(win_matches_table)
    draw_matches_table = ' '.join(draw_matches_table)
    lose_matches_table = ' '.join(lose_matches_table)
    goals_scored_for_table = ' '.join(goals_scored_for_table)
    goals_missed_for_table = ' '.join(goals_missed_for_table)
    goals_diff_table = ' '.join(goals_diff_table)
    points_for_table = ' '.join(points_for_table)

    
    goals_home2 = []
    for j in range(len(goals_home)):
        goals_home2.append(str(goals_home[j]))

    goals_away2 = []
    for k in range(len(goals_away)):
        goals_away2.append(str(goals_away[k]))
    
    ycards_top3_fouls_of_season2 = []
    for v in range(len(ycards_top3_fouls_of_season)):
        ycards_top3_fouls_of_season2.append(str(ycards_top3_fouls_of_season[v]))

    rcards_top3_fouls_of_season2 = []
    for c in range(len(rcards_top3_fouls_of_season)):
        rcards_top3_fouls_of_season2.append(str(rcards_top3_fouls_of_season[c]))
    
    
    name_home_review = '+'.join(name_home_review)
    name_home_review = name_home_review.replace(" ", "_")
    name_away_review = '+'.join(name_away_review)
    name_away_review = name_away_review.replace(" ", "_")
    goals_home2 = ' '.join(goals_home2)
    goals_away2 = ' '.join(goals_away2)
    who_scored_home = '+'.join(who_scored_home)
    who_scored_home = who_scored_home.replace(" ", "_")
    who_scored_away = '+'.join(who_scored_away)
    who_scored_away = who_scored_away.replace(" ", "_")
    name_top3_fouls_of_season = "+".join(name_top3_fouls_of_season)   # Готовый список
    ycards_top3_fouls_of_season2 = " ".join(ycards_top3_fouls_of_season2)   # Готовый список
    rcards_top3_fouls_of_season2 = " ".join(rcards_top3_fouls_of_season2)   # Готовый список
    name_teams_cards_top3_fouls_of_season = "+".join(name_teams_cards_top3_fouls_of_season)
    sum_accuracy = " ".join(str(sum_accuracy))
    sum_accuracy_name= "+".join(sum_accuracy_name)
  
    list_v = [rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season2, rcards_top3_fouls_of_season2, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds,  total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5  ,  total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home2, goals_away2, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves]

    for index_replace in range(len(list_v)):
        if type(list_v[index_replace]) == str:
            if "'" in list_v[index_replace]:
                list_v[index_replace] = list_v[index_replace].replace("'", "")

    rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader, goal_rival, name_home_review, name_away_review, count_home, count_away, count_draw, h3_amounts_list, h3_names_list, h3_team_names_list, h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4, team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1, all_goals_round, all_penalty_round, all_goals_previous_round, total_percent_round, average_goals_in_season, average_penalty_in_season, time_fast_goal, team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer, max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator, goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount, name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round, name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season2, rcards_top3_fouls_of_season2, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round, top_round_injuries_name_team, top_round_injuries_amount, name_top_assists_league_1, assists_top_league_1, team_top_assists_league1, name_top_assists_league_2, assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3, team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home2, goals_away2, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves = list_v
    # goals_top_league_1, name_top_goals_league_1, team_top_goals_league1,total_name_top_goals_league_1_round, goals_top_league_2, name_top_goals_league_2, team_top_goals_league2, total_name_top_goals_league_2_round ,goals_top_league_3, name_top_goals_league_3, team_top_goals_league3, total_name_top_goals_league_3_round, goals_top_league_4, name_top_goals_league_4, team_top_goals_league4, total_name_top_goals_league_4_round, goals_top_league_5, name_top_goals_league_5, team_top_goals_league5, total_name_top_goals_league_5_round
    # assists_top_league_1, name_top_assists_league_1,total_of_round_top_assists_league_1,team_top_assists_league1, assists_top_league_2, name_top_assists_league_2,total_of_round_top_assists_league_2, team_top_assists_league2, assists_top_league_3, name_top_assists_league_3,total_of_round_top_assists_league_3, team_top_assists_league3, assists_top_league_4, name_top_assists_league_4,total_of_round_top_assists_league_4, team_top_assists_league4, assists_top_league_5, name_top_assists_league_5,total_of_round_top_assists_league_5,team_top_assists_league5
    # saves_top_league_1, name_top_saves_league_1,total_of_round_top_saves_league_1, team_top_saves_league1, saves_top_league_2, name_top_saves_league_2,total_of_round_top_saves_league_2, team_top_saves_league2, saves_top_league_3, name_top_saves_league_3,total_of_round_top_saves_league_3,team_top_saves_league3, saves_top_league_4, name_top_saves_league_4,total_of_round_top_saves_league_4,team_top_saves_league4, saves_top_league_5, name_top_saves_league_5,total_of_round_top_saves_league_5,team_top_saves_league5
    # name_max_accuracy,percent_max_accuracy, sum_accuracy, min_team_away_for_passes, team_away_min_passes_accurate, team_away_min_percent_passes_accurate, team_min_away_total_passes, min_team_home_for_passes, team_home_min_passes_accurate, team_home_min_percent_passes_accurate, team_home_min_total_passes, max_team_away_for_passes, team_away_max_passes_accurate, team_away_max_percent_passes_accurate, team_max_away_total_passes, max_team_home_for_passes, team_home_max_passes_accurate, team_home_max_percent_passes_accurate, team_home_max_total_passes, name_fast_goal, time_fast_goal, team_name_fast_goal,fixture_fast_goal, average_penalty_in_season, average_goals_in_season, total_num, total_percent_now_round, total_percent_last_round, total_percent_draw
    
    
    # all_goals_of_season, all_goals_previous_round, all_goals_round, h3_amounts_list, h3_names_list, h3_team_names_list, h3_fixture_match_list, all_penalty_round, list_name_who_scrored_of_round, goals_who_scrored_of_round, amount_max_saves_of_round, name_max_saves_of_round, fixture_max_saves_of_round, amount_max_fouls_of_round , name_max_fouls_of_round, fixture_max_fouls_of_round, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, team_id_max_destroyer, amount_max_destroyer,data_for_max_destroyer, team_id_max_creator, amount_max_creator,data_for_max_creator
    insert_query_for_db = (
        f"INSERT INTO round_review (rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home, goals_away, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves)"             
        f"VALUES ('{rounds}', '{season}', '{league_id}', '{league_name}', '{team_home_leader}', '{team_away_rival}', '{goal_leader}','{goal_rival}', '{name_home_review}',  '{name_away_review}', '{count_home}','{count_away}','{count_draw}', '{h3_amounts_list}', '{h3_names_list}', '{h3_team_names_list}','{h3_fixture_match_list}', '{name_top_goals_league_1}', '{goals_top_league_1}', '{team_top_goals_league1_1}', '{name_top_goals_league_2}', '{goals_top_league_2}', '{team_top_goals_league2_1}', '{name_top_goals_league_3}', '{goals_top_league_3}', '{team_top_goals_league3_1}', '{name_top_goals_league_4}', '{goals_top_league_4}' , '{team_top_goals_league4_1}', '{name_top_goals_league_5}', '{goals_top_league_5}', '{team_top_goals_league5_1}','{all_goals_round}','{all_penalty_round}','{all_goals_previous_round}', '{total_percent_round}','{average_goals_in_season}','{average_penalty_in_season}','{time_fast_goal}','{team_name_fast_goal}', '{name_fast_goal}', '{team_away_fast_goal}', '{scrore_fast_goal}', '{team_top_destroyer}', '{destroyer_interceptions}', '{destroyer_blocks}', '{destroyer_tackles}', '{destroyer_saves}', '{amount_max_destroyer}', '{team_main_destroyer}', '{team_rival_destroyer}', '{goals_main_destroyer}', '{goals_rival_destroyer}' , '{max_destroyer_of_season_name}', '{max_destroyer_of_season_amount}', '{team_top_creator}', '{creator_duels}', '{creator_shots_on_target}', '{creator_shots_off_target}', '{team_main_creator}', '{team_rival_creator}' , '{goals_main_creator}', '{goals_rival_creator}', '{amount_max_creator}', '{max_creator_of_season_name}', '{max_creator_of_season_amount}' , '{name_max_accurate_in_round}', '{max_accurate_in_round}', '{max_total_passes_with_accurate_in_round}' , '{name_min_accurate_in_round}', '{min_accurate_in_round}', '{min_total_passes_with_accurate_in_round}', '{name_max_accuracy_in_season}', '{percent_max_accuracy_in_season}', '{name_min_accuracy_in_season}', '{percent_min_accuracy_in_season}', '{name_max_saves_of_round}', '{main_team_max_saves}', '{round_max_saves_of_round}', '{rival_team_max_saves}', '{amount_max_saves_of_round}', '{top_fouls_total_yel_card}', '{top_fouls_total_red_card}', '{top_fouls_team_name_home}', '{top_fouls_team_name_away}', '{top_fouls_goals_home}', '{top_fouls_goals_away}', '{name_top3_fouls_of_season}', '{ycards_top3_fouls_of_season2}', '{rcards_top3_fouls_of_season2}', '{name_teams_cards_top3_fouls_of_season}', '{round_injuries}', '{average_injuries_in_round}','{top_round_injuries_name_team}','{top_round_injuries_amount}','{name_top_assists_league_1}','{assists_top_league_1}','{team_top_assists_league1}', '{name_top_assists_league_2}','{assists_top_league_2}', '{team_top_assists_league2}', '{name_top_assists_league_3}', '{assists_top_league_3}', '{team_top_assists_league3}', '{name_top_assists_league_4}', '{assists_top_league_4}', '{team_top_assists_league4}', '{name_top_assists_league_5}', '{assists_top_league_5}', '{team_top_assists_league5}', '{name_top_saves_league_1}', '{saves_top_league_1}', '{team_top_saves_league1}', '{name_top_saves_league_2}', '{saves_top_league_2}', '{team_top_saves_league2}', '{name_top_saves_league_3}', '{saves_top_league_3}' , '{team_top_saves_league3}', '{name_top_saves_league_4}', '{saves_top_league_4}', '{team_top_saves_league4}', '{name_top_saves_league_5}', '{saves_top_league_5}', '{team_top_saves_league5}' , '{rank_for_table}', '{name_table_team}', '{logo_for_table}', '{form_table}', '{all_matches_table}' , '{win_matches_table}' , '{draw_matches_table}', '{lose_matches_table}', '{goals_scored_for_table}', '{goals_missed_for_table}', '{goals_diff_table}', '{points_for_table}', '{date_next_round}', '{arena_next_round}', '{first_team_home_next_round}', '{first_team_away_next_round}', '{sum_accuracy_name}', '{all_rounds}',  '{total_of_round_top_assists_league_1}', '{total_of_round_top_assists_league_2}', '{total_of_round_top_assists_league_3}', '{total_of_round_top_assists_league_4}', '{total_of_round_top_assists_league_5}'  ,  '{total_of_round_top_saves_league_1}', '{total_of_round_top_saves_league_2}', '{total_of_round_top_saves_league_3}', '{total_of_round_top_saves_league_4}', '{total_of_round_top_saves_league_5}', '{goals_home2}', '{goals_away2}', '{goals_and_info_max_saves}', '{total_name_top_goals_league_1_round}', '{total_name_top_goals_league_2_round}', '{total_name_top_goals_league_3_round}', '{total_name_top_goals_league_4_round}', '{total_name_top_goals_league_5_round}', '{city_next_round}', '{date_game_max_saves}');"               
    )
    insert_db(insert_query_for_db, 'review_round')


# main_start_review_round(24, 39, '2022') ycards_top3_fouls_of_season ycards_top3_fouls_of_season2