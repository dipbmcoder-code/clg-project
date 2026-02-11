







def db_query_list(insert_query):
    pass

def check_country_and_team(fixture_match):
    text, league, round = "", "", ""
    league, round = db_query_list(f"SELECT league, round FROM match_review WHERE fixture_match LIKE '{fixture_match}'")

    return text, league, round


def check_parameters_in_round(player_id, league, round):
    """"""
    """
    Функция для сбора данных с таблицы players_round по каждому игроку за 1 игру (1 тур) 
    """


    """ Макет players_data_json:
    {
        "name": "maks",
        "goals": "",
        "assists": "",
        "y_cards": "",
        "r_cards": "",
        "blocks": "",
        "interceptions": "",
        "saves": "",
        "duels": "",
        "conceded": "",
        "injuries": "",
        "fast_goal": "",
        "penalty": "",

    }
    """
    players_data_json = {}

    # get_parameters_in_db = db_query_list(
    #     f"SELECT name, goals, assists, y_cards, r_cards, blocks, interceptions, saves, duels, conceded, penalty FROM players_round"
    #     f" WHERE player_id_api = {player_id} AND league_id = {league} AND round = {round} "
    # )[0]
    get_parameters_in_db = ["Maks", "1", "2", "1", "2", "20", "11", "0", "12", "0", "1"]

    """ 
    parameters for update/add: 
    
    type_player: attack/goalkeeper (players_info), 
    nationalyty (players_info),
    lineups: start/subs/no_play (players_round) 
    
    """


    # type_player = db_query_list(f"SELECT type_player FROM players_info WHERE player_id_api = {player_id}")[0][0]
    type_player = "attack"
    team_player = "Liverpool"
    # team_player = db_query_list(f"SELECT team FROM players_info WHERE player_id_api = {player_id}")[0][0]
    lineups = "start"


    index = 0

    list_parameters_name = ["name", "goals", "assists", "y_cards", "r_cards", "blocks", "interceptions", "saves", "duels", "conceded", "penalty" ]

    list_varible = []


    for parameter in get_parameters_in_db:
        if str(parameter) != "0" and parameter != None:
            if players_data_json == {} :
                players_data_json = {
                    list_parameters_name[index]:parameter
                }
            else:
                players_data_json = players_data_json | {
                    list_parameters_name[index]: parameter
                }

            list_varible.append(parameter)

        index += 1

    dict_lineups = {"start":"<b>вошел в стартовый состав игры</b>", "subs":"", "no_play":"", "":""}

    text_parameter = f"{type_player} {players_data_json['name']} ({team_player}) выделился в туре по таким критериям: {dict_lineups[lineups]}"

    dict_text = {
        "goals":" забил *goals* гола в этом туре",
        "assists":"*assists* ассиста",
        "interceptions":"совершил *interceptions* ключевых паса",
        "y_cards":"*y_cards* желт. карточки",
        "r_cards":"*r_cards* красн. карточки",
        "blocks":"*blocks* блока",
        "duels":"вступил в *duels* duels",
        "conceded":"*{conceded}* ",
        "saves":"*{saves}* ",
        "penalty":"забил пенальти",
    }

    for parameter_name in players_data_json:
        if parameter_name != "name":
            text_parameter += ", "
            text_parameter = text_parameter + dict_text[parameter_name].replace(f"*{parameter_name}*", players_data_json[parameter_name])

    text_parameter += ". "

    return text_parameter



league: str or int
round: str or int
# ---------
fixture_match: []
players_id: []
# ---------
main_text: str

# Делаем цикл по файлу:  *round*_*league*_ghana_players.json

file = ""
main_text = ""

# for fixture_match in file:
#
#     for index_players in file[fixture_match]:
#         player_id = file[fixture_match][index_players]

player_text = check_parameters_in_round(1, 1, 1)
print(player_text)



