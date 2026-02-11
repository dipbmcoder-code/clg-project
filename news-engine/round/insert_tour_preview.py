from datetime import date, datetime
#from API import get_date_next_round #Дата первого матча тура
from API import check_match_round_api, check_match_list_rounds_api
from db import check_stat_preview, insert_db
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def main_insert_preview_round(rounds, league_id, season):

    # season = ''
    # league_id = ''

    data_tour_review = check_match_round_api(league_id, season, rounds)

    fixtures_and_date = []
   
    for find_matches in range(len(data_tour_review['response'])):
        date = datetime.strptime(data_tour_review['response'][find_matches]['fixture']['date'][:16], "%Y-%m-%dT%H:%M") #.strftime('%B %d %Y')
        
        fixtures_and_date.append([date, data_tour_review['response'][find_matches]['fixture']['id']])

    
    league_logo = data_tour_review['response'][0]['league']['logo']
    fixtures_and_date.sort()

    future_fixture_round = []
    future_date_round = [] 
    for find_future in range(len(fixtures_and_date)):
        future_fixture_round.append(str(fixtures_and_date[find_future][1]))
        future_date_round.append(str(fixtures_and_date[find_future][0]))

    future_fixture_round.sort()

    
    first_date_round = fixtures_and_date[0][0]

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }

    req_first_match_round = requests.request("GET", url, headers=headers, params={
        "id":fixtures_and_date[0][1]
        })

    data_first_match = req_first_match_round.json()

    venue_first_match = data_first_match['response'][0]['fixture']['venue']['name']
    city_first_match = data_first_match['response'][0]['fixture']['venue']['city']
    home_first_match = data_first_match['response'][0]['teams']['home']['name']
    away_first_match = data_first_match['response'][0]['teams']['away']['name']

    preview_home_teams = []
    preview_away_teams = []

    league_name = data_first_match['response'][0]['league']['name']
    if league_name == 'Premier League':
        league_name = 'English Premier League'

    for all_match_round_for_preview in range(len(fixtures_and_date)):
        req_all_match_round = requests.request("GET", url, headers=headers, params={
        "id":fixtures_and_date[all_match_round_for_preview][1]
        })

        data_all_match = req_all_match_round.json()
        
        preview_home_teams.append(data_all_match['response'][0]['teams']['home']['name'])
        preview_away_teams.append(data_all_match['response'][0]['teams']['away']['name'])


    

    #Букмекеры
    #Добавить условие с разными лигами
    title = ''
    if league_name == 'English Premier League':
        title = 'soccer_epl'
    elif league_name == 'Bundesliga':
        title = 'soccer_germany_bundesliga'
    elif league_name == 'Ligue 1':
        title = 'soccer_france_ligue_one'
    elif league_name == 'La Liga':
        title = 'soccer_spain_la_liga'
    elif league_name == 'Serie A':
        title = 'soccer_italy_serie_a'
    elif league_name == 'Primeira Liga':
        title = 'soccer_portugal_primeira_liga'

    url = f"https://odds.p.rapidapi.com/v4/sports/{title}/odds"


    querystring = {"regions":"eu","oddsFormat":"decimal"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }

    req_bk = requests.request("GET", url, headers=headers, params=querystring)

    data_bk = req_bk.json()

    all_data = []

    for bk in range(len(preview_home_teams)):
        #l = data_bk[bk]['commence_time'][:16]
        date_match1 = datetime.strptime(data_bk[bk]['commence_time'][:16], "%Y-%m-%dT%H:%M")#TODO.strftime('%B %d %Y')
        #date_match1 = datetime.datetime(int(l[:4]), int(l[5:7]), int(l[8:10]), int(l[11:13]), int(l[14:16])).strftime("%Y-%m-%H:%M")
        if data_bk[bk]['home_team'] in data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][0]['name'] and data_bk[bk]['away_team'] in data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][1]['name']:
            all_data.append([date_match1, data_bk[bk]['home_team'], data_bk[bk]['away_team'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][0]['price'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][1]['price'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][2]['price']]) #TODO 2 значение в odds победа эвей
        elif data_bk[bk]['home_team'] in data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][1]['name'] and data_bk[bk]['away_team'] in data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][0]['name']:
            all_data.append([date_match1, data_bk[bk]['home_team'], data_bk[bk]['away_team'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][1]['price'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][0]['price'], data_bk[bk]['bookmakers'][0]['markets'][0]['outcomes'][2]['price']]) #TODO 2 значение в odds победа эвей

    all_data.sort()

    odds_win_home = []
    odds_win_away = []
    odds_draw = []
    date_matches = []
    for find_odds in range(len(preview_home_teams)):
        odds_win_home.append(all_data[find_odds][3])
        odds_win_away.append(all_data[find_odds][4])
        odds_draw.append(all_data[find_odds][5])
        date_matches.append(fixtures_and_date[find_odds][0])

    
    #Главный матч по бк
    top_win_home = 0
    top_win_away = 0
    top_draw = 0
    min_num = 0
    max_num = 10
    index_main_match = 0
    for find_top_match in range(len(odds_win_home)):
        min_num = odds_win_home[find_top_match] - odds_win_away[find_top_match]
        min_num = abs(min_num)
        if min_num < max_num:
            max_num = min_num
            index_main_match = find_top_match
            top_win_home = odds_win_home[find_top_match]
            top_win_away = odds_win_away[find_top_match]
            top_draw = odds_draw[find_top_match]

    last_round = int(rounds) - 1

    top_home_team_version_bk = preview_home_teams[index_main_match]
    find_previous_fixture = []
    data_tour_review2 = check_match_round_api(league_id, season, last_round)
    for find_previous_matches in range(len(data_tour_review2['response'])):
        find_previous_fixture.append(data_tour_review2['response'][find_previous_matches]['fixture']['id'])

    
    date_previous_match = ''
    away_previous_match = ''
    goals_home_previous_match = 0
    goals_away_previous_match = 0
    for find_data_previous_matches in range(len(find_previous_fixture)):
        url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"

        headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
        req_previous_match = requests.request("GET", url, headers=headers, params={
        "id":find_previous_fixture[find_data_previous_matches]
        })

        data_previous_match = req_previous_match.json()
        if top_home_team_version_bk == data_previous_match['response'][0]['teams']['home']['name']:
            date_previous_match = datetime.strptime(data_previous_match['response'][0]['fixture']['date'][:16], "%Y-%m-%dT%H:%M")  #.strftime('%B %d %Y')
            away_previous_match = data_previous_match['response'][0]['teams']['away']['name']
            goals_home_previous_match = int(data_previous_match['response'][0]['goals']['home'])
            goals_away_previous_match = int(data_previous_match['response'][0]['goals']['away'])
        elif top_home_team_version_bk == data_previous_match['response'][0]['teams']['away']['name']:
            date_previous_match = datetime.strptime(data_previous_match['response'][0]['fixture']['date'][:16], "%Y-%m-%dT%H:%M") #.strftime('%B %d %Y')
            away_previous_match = data_previous_match['response'][0]['teams']['home']['name']
            goals_home_previous_match = int(data_previous_match['response'][0]['goals']['away'])
            goals_away_previous_match = int(data_previous_match['response'][0]['goals']['home'])


    # match_postponed
    list_match_postponed = check_match_list_rounds_api(league_id, season, rounds)
    
    count_matchs = ''
   
    list_match_postponed = list_match_postponed[1]
    if list_match_postponed != []:
        count_matchs = len(list_match_postponed)
    else:
        count_matchs = 0
   
    

    insert_query = (  #TODO протестить 
        f"SELECT max(injuries_count) AS R, name FROM teams_round WHERE round={last_round} AND league_id={league_id} GROUP BY name ORDER BY R DESC LIMIT 1;"
    )
    index_injuries = check_stat_preview(insert_query)
    index_injuries = index_injuries[0]

    max_injuries, team_name_max_injuries= index_injuries[0], index_injuries[1]


    
    insert_query = (
        f"SELECT name, max(goals) AS T, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY T DESC LIMIT 1;"
    )
    index_goals = check_stat_preview(insert_query)

    index_goals = index_goals[0]

    team_max_goals_league, max_goals_league, team_id_max_goals_league = index_goals[0], index_goals[1], index_goals[2]

    insert_query = (
        f"SELECT name, min(conceded_goals) AS Y, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY Y ASC LIMIT 1;"
    )
    index_min_conceded = check_stat_preview(insert_query)
    index_min_conceded = index_min_conceded[0]

    team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded = index_min_conceded[0], index_min_conceded[1], index_min_conceded[2]

    #Больше всего игр на ноль у...

    insert_query = (
        f"SELECT name, max(clean_sheet_count) AS Y, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY Y DESC LIMIT 1;"
    )
    index_max_clean_sheet = check_stat_preview(insert_query)
    index_max_clean_sheet = index_max_clean_sheet[0]

    team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league = index_max_clean_sheet[0], index_max_clean_sheet[1], index_max_clean_sheet[2]

    insert_query = (
        f"SELECT name, max(conceded_goals) AS U, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY U DESC LIMIT 1;"
    )
    index_max_conceded = check_stat_preview(insert_query)
    index_max_conceded = index_max_conceded[0]

    team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league = index_max_conceded[0], index_max_conceded[1], index_max_conceded[2]

    insert_query = (
        f"SELECT name, min(goals) AS I, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY I ASC LIMIT 1;"
    )
    index_min_goals = check_stat_preview(insert_query)
    index_min_goals = index_min_goals[0]

    team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack = index_min_goals[0], index_min_goals[1], index_min_goals[2]





    insert_query = (
        f"SELECT name, max(without_scored_count) AS P, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY P DESC LIMIT 1;"
    )
    index_without_scored = check_stat_preview(insert_query)
    index_without_scored = index_without_scored[0]

    team_max_without_scored_league, max_without_scored_league, id_team_max_without_scored = index_without_scored[0], index_without_scored[1], index_without_scored[2]
 
    insert_query = (
        f"SELECT wins, loses, draws FROM teams WHERE team_id_api={id_team_max_without_scored};"
    )
    index_games_without_scored = check_stat_preview(insert_query)
    index_games_without_scored = index_games_without_scored[0]

    wins_without_scored, loses_without_scored, draws_without_scored = index_games_without_scored[0], index_games_without_scored[1], index_games_without_scored[2]
    
    insert_query = (
        f"SELECT name, max(conceded_goals_count) AS A, team_id_api FROM teams WHERE league_id={league_id} GROUP BY name, team_id_api ORDER BY A DESC LIMIT 1;"
    )
    index_max_conceded_goals = check_stat_preview(insert_query)
    index_max_conceded_goals = index_max_conceded_goals[0]

    team_max_conceded_goals_league, max_conceded_goals_league, id_team_max_conceded_goals = index_max_conceded_goals[0], index_max_conceded_goals[1], index_max_conceded_goals[2]
 
    insert_query = (
        f"SELECT wins, loses, draws FROM teams WHERE team_id_api={id_team_max_conceded_goals};"
    )
    index_games_conceded_goals = check_stat_preview(insert_query)
    index_games_conceded_goals = index_games_conceded_goals[0]

    wins_conceded_goals, loses_conceded_goals, draws_conceded_goals = index_games_conceded_goals[0], index_games_conceded_goals[1], index_games_conceded_goals[2]
    


    ## Статистика игроков в сезоне. 

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

    url = os.getenv('RAPID_API_BASE_URL')+"/standings"          #V3 - Standings by league id

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }

    req_rank = requests.get(url, headers=headers, params={
        "season":season,
        "league":league_id
        })

    data_rank = req_rank.json()
    

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

    for find_rank in range(len(data_rank['response'][0]['league']['standings'][0])):
        rank_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['rank']))
        name_table_team.append(data_rank['response'][0]['league']['standings'][0][find_rank]['team']['name'])
        form_table.append(data_rank['response'][0]['league']['standings'][0][find_rank]['form'])
        all_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['played']))
        win_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['win']))
        draw_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['draw']))
        lose_matches_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['lose']))
        goals_scored_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['goals']['for']))
        goals_missed_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['all']['goals']['against']))
        goals_diff_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['goalsDiff']))
        points_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['points']))
        logo_for_table.append(str(data_rank['response'][0]['league']['standings'][0][find_rank]['team']['logo']))

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures/rounds"


    req_all_rounds = requests.get(url, headers=headers, params={
        "league":league_id,
        "season":season
        })
    data_all_rounds = req_all_rounds.json()


    all_rounds = len(data_all_rounds['response'])


    future_fixture_round = '+'.join(future_fixture_round)
    future_date_round = '+'.join(future_date_round)
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

    odds_win_home = str(odds_win_home).replace("[", '').replace("]", '')
    odds_win_away = str(odds_win_away).replace("[", '').replace("]", '')
    odds_draw = str(odds_draw).replace("[", '').replace("]", '')
    odds_win_home = str(odds_win_home).replace("[", '').replace("]", '')

    new_date = []
    for create_date in range(len(date_matches)):
        new_date.append(str(date_matches[create_date]))

    new_date = '+'.join(new_date)
    if ' ' in new_date:
        new_date = new_date.replace(' ', '_')



    

    preview_home_teams = '+'.join(preview_home_teams)
    if preview_home_teams.find(" "):
        preview_home_teams = preview_home_teams.replace(" ", "_")

    preview_away_teams = '+'.join(preview_away_teams)
    
    if preview_away_teams.find(" "):
        preview_away_teams = preview_away_teams.replace(" ", "_")
    if name_table_team.find("'"):
        name_table_team = name_table_team.replace("'", "")
    if venue_first_match.find("'"):
        venue_first_match = venue_first_match.replace("'", "")
    if city_first_match.find("'"):
        city_first_match = city_first_match.replace("'", "")
    if home_first_match.find("'"):
        home_first_match = home_first_match.replace("'", "")
    if away_first_match.find("'"):
        away_first_match = away_first_match.replace("'", "")
    if team_max_goals_league.find("'"):
        team_max_goals_league = team_max_goals_league.replace("'", "")
    if team_min_conceded_league.find("'"):
        team_min_conceded_league = team_min_conceded_league.replace("'", "")
    if team_max_clean_sheet_league.find("'"):
        team_max_clean_sheet_league = team_max_clean_sheet_league.replace("'", "")
    if team_max_conceded_league.find("'"):
        team_max_conceded_league = team_max_conceded_league.replace("'", "")
    if team_min_goals_attack_league.find("'"):
        team_min_goals_attack_league = team_min_goals_attack_league.replace("'", "")
    if name_top_goals_league_1.find("'"):
        name_top_goals_league_1 = name_top_goals_league_1.replace("'", "")
    if name_top_goals_league_2.find("'"):
        name_top_goals_league_2 = name_top_goals_league_2.replace("'", "")
    if name_top_goals_league_3.find("'"):
        name_top_goals_league_3 = name_top_goals_league_3.replace("'", "")
    if name_top_goals_league_4.find("'"):
        name_top_goals_league_4 = name_top_goals_league_4.replace("'", "")
    if name_top_goals_league_5.find("'"):
        name_top_goals_league_5 = name_top_goals_league_5.replace("'", "")
    if name_top_assists_league_1.find("'"):
        name_top_assists_league_1 = name_top_assists_league_1.replace("'", "")
    if name_top_assists_league_2.find("'"):
        name_top_assists_league_2 = name_top_assists_league_2.replace("'", "")
    if name_top_assists_league_3.find("'"):
        name_top_assists_league_3 = name_top_assists_league_3.replace("'", "")
    if name_top_assists_league_4.find("'"):
        name_top_assists_league_4 = name_top_assists_league_4.replace("'", "")
    if name_top_assists_league_5.find("'"):
        name_top_assists_league_5 = name_top_assists_league_5.replace("'", "")
    if name_top_saves_league_1.find("'"):
        name_top_saves_league_1 = name_top_saves_league_1.replace("'", "")
    if name_top_saves_league_2.find("'"):
        name_top_saves_league_2 = name_top_saves_league_2.replace("'", "")
    if name_top_saves_league_3.find("'"):
        name_top_saves_league_3 = name_top_saves_league_3.replace("'", "")
    if name_top_saves_league_4.find("'"):
        name_top_saves_league_4 = name_top_saves_league_4.replace("'", "")
    if name_top_saves_league_5.find("'"):
        name_top_saves_league_5 = name_top_saves_league_5.replace("'", "")
    if team_max_without_scored_league.find("'"):
        team_max_without_scored_league = team_max_without_scored_league.replace("'", "")
    if team_max_conceded_goals_league.find("'"):
        team_max_conceded_goals_league = team_max_conceded_goals_league.replace("'", "")

    list_v = [rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match,away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league,min_goals_attack_league,id_team_min_attack,goals_top_league_1,name_top_goals_league_1,goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3,goals_top_league_4, name_top_goals_league_4,goals_top_league_5,name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, new_date, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1 , team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds]

    for index_replace in range(len(list_v)):
        if type(list_v[index_replace]) == str:
            if "'" in list_v[index_replace]:
                list_v[index_replace] = list_v[index_replace].replace("'", "")

    rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, new_date, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds = list_v

    insert_query_for_db = (
        f"INSERT INTO round_preview (rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds)"
        f"VALUES ('{rounds}', '{season}', '{league_id}', '{first_date_round}', '{venue_first_match}', '{city_first_match}', '{home_first_match}','{away_first_match}', '{preview_home_teams}', '{preview_away_teams}', '{count_matchs}', '{last_round}', '{team_name_max_injuries}', '{max_injuries}', '{team_max_goals_league}', '{max_goals_league}', '{team_id_max_goals_league}', '{team_min_conceded_league}', '{min_conceded_top_saves}', '{team_id_top_min_conceded}', '{team_max_clean_sheet_league}', '{max_cleen_sheet_league}', '{team_id_clean_sheet_league}', '{team_max_conceded_league}', '{max_conceded_saves_league}', '{team_id_max_conceded_league}', '{team_min_goals_attack_league}','{min_goals_attack_league}','{id_team_min_attack}','{goals_top_league_1}','{name_top_goals_league_1}','{goals_top_league_2}', '{name_top_goals_league_2}', '{goals_top_league_3}', '{name_top_goals_league_3}','{goals_top_league_4}', '{name_top_goals_league_4}','{goals_top_league_5}','{name_top_goals_league_5}', '{assists_top_league_1}', '{name_top_assists_league_1}', '{assists_top_league_2}', '{name_top_assists_league_2}', '{assists_top_league_3}', '{name_top_assists_league_3}', '{assists_top_league_4}', '{name_top_assists_league_4}', '{assists_top_league_5}', '{name_top_assists_league_5}', '{saves_top_league_1}', '{name_top_saves_league_1}', '{saves_top_league_2}', '{name_top_saves_league_2}', '{saves_top_league_3}', '{name_top_saves_league_3}', '{saves_top_league_4}', '{name_top_saves_league_4}', '{saves_top_league_5}', '{name_top_saves_league_5}', '{team_max_without_scored_league}', '{max_without_scored_league}', '{wins_without_scored}', '{loses_without_scored}', '{draws_without_scored}', '{team_max_conceded_goals_league}', '{max_conceded_goals_league}', '{wins_conceded_goals}', '{loses_conceded_goals}', '{draws_conceded_goals}', '{rank_for_table}', '{name_table_team}', '{logo_for_table}', '{form_table}', '{all_matches_table}', '{win_matches_table}', '{draw_matches_table}', '{lose_matches_table}', '{goals_scored_for_table}', '{goals_missed_for_table}', '{goals_diff_table}', '{points_for_table}', '{new_date}', '{odds_win_home}', '{odds_win_away}', '{odds_draw}', '{top_win_home}', '{top_win_away}', '{top_draw}', '{index_main_match}', '{team_top_goals_league1}', '{team_top_goals_league2}', '{team_top_goals_league3}', '{team_top_goals_league4}', '{team_top_goals_league5}', '{team_top_assists_league1}', '{team_top_assists_league2}', '{team_top_assists_league3}', '{team_top_assists_league4}', '{team_top_assists_league5}', '{team_top_saves_league1}' , '{team_top_saves_league2}', '{team_top_saves_league3}', '{team_top_saves_league4}', '{team_top_saves_league5}', '{league_name}', '{date_previous_match}', '{away_previous_match}', '{goals_home_previous_match}', '{goals_away_previous_match}', '{league_logo}', '{future_fixture_round}', '{future_date_round}', '{all_rounds}')"     
    )

    insert_db(insert_query_for_db, 'preview_round')

# main_insert_preview_round('18', '39', '2022')