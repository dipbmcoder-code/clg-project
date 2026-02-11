import json
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]

def preview_match_text(fixture_match):
    from preview.db_preview import get_data


    # Запрос в БД
    insert_query = (
        f"SELECT fixture_match, name_home_preview, name_away_preview, date_match, venue, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card FROM match_preview WHERE fixture_match={fixture_match}"
    )

    r = get_data(insert_query)

    r = r[0]
    # exit()

    # Создание переменных по индексам результата
    # print(r)
    # exit()
    fixture_match, name_home_preview, name_away_preview, date_match, venue, rank_team_home, rank_team_away, players_a_name, players_a_goals_total, players_b_name, players_b_goals_total, topscorers_assists_home_name, topscorers_assists_home_amount, topscorers_assists_away_name, topscorers_assists_away_amount, topscorers_interceptions_home_name, topscorers_interceptions_home_amount, topscorers_interceptions_away_name, topscorers_interceptions_away_amount, topscorers_duels_home_name, topscorers_duels_home_amount, topscorers_duels_away_name, topscorers_duels_away_amount, topscorers_saves_home_name, topscorers_saves_home_amount, topscorers_saves_away_name, topscorers_saves_away_amount, topscorer_name_in_league_1, topscorer_name_in_league_2, topscorer_name_in_league_3, topscorer_amount_in_league_1, topscorer_amount_in_league_2, topscorer_amount_in_league_3, topscorer_team_in_league_1, topscorer_team_in_league_2, topscorer_team_in_league_3, home_play_clean_sheet, home_biggest_win_in_home, home_biggest_win_in_away, home_biggest_lose_in_home, home_biggest_lose_in_away, away_play_clean_sheet, away_biggest_win_in_home, away_biggest_win_in_away, away_biggest_lose_in_home, away_biggest_lose_in_away, home_win_once_in_home, home_lose_once_in_home, home_draws_once_in_home, away_win_once_in_away, away_lose_once_in_away, away_draws_once_in_away, list_minute, list_minute_for_goals_home, list_for_goal_home, list_minute_missed_goals_home, list_missed_goal_home, list_minute_for_goals_away, list_for_goal_away, list_minute_missed_goals_away, list_missed_goal_away, predictions_percent_home, predictions_percent_away, predictions_percent_draw, predictions_goals_home, predictions_goals_away, form_home, form_away, bk_coef_name, bk_coef_home, bk_coef_draw, bk_coef_away, h2h_home_total_games, h2h_home_total_wins_in_home, h2h_home_total_wins_in_away, h2h_home_total_draws_in_home, h2h_home_total_draws_in_away, h2h_home_total_loses_in_home, h2h_home_total_loses_in_away, h2h_away_total_wins_home, h2h_away_total_wins_away, h2h_away_total_draws_in_home, h2h_away_total_draws_in_away, h2h_away_total_loses_in_home, h2h_away_total_loses_in_away, comparison_total_home, comparison_att_home, comparison_def_home, comparison_h2h_home, comparison_goals_home, comparison_total_away, comparison_att_away, comparison_def_away, comparison_h2h_away, comparison_goals_away, name_league, topscorer_name_in_league_4, topscorer_name_in_league_5, topscorer_amount_in_league_4, topscorer_amount_in_league_5, topscorer_team_in_league_4, topscorer_team_in_league_5, name_home_top_fouls_yel_card, amount_home_fouls_yel_card, name_away_top_fouls_yel_card, amount_away_fouls_yel_card, name_home_top_fouls_red_card, amount_home_fouls_red_card, name_away_top_fouls_red_card, amount_away_fouls_red_card = r 
    # Восстановление списков
    list_for_goal_away=list_for_goal_away
    list_for_goal_home=list_for_goal_home
    list_minute=list_minute.split()
    list_minute_for_goals_home=list_minute_for_goals_home.split()
    list_minute_for_goals_away=list_minute_for_goals_away.split()
    list_minute_missed_goals_away=list_minute_missed_goals_away.split()
    list_minute_missed_goals_home=list_minute_missed_goals_home.split()
    list_missed_goal_away=list_missed_goal_away
    list_missed_goal_home=list_missed_goal_home
    bk_coef_name = bk_coef_name.split()
    bk_coef_home = bk_coef_home.split()
    bk_coef_draw = bk_coef_draw.split()
    bk_coef_away = str(bk_coef_away).split()
   
    #Ищу топ 3 букмекера с лучшими коэффициентами 
    # print(bk_coef_name)
    # print(bk_coef_home)
    # print(bk_coef_draw)
    # print(bk_coef_away)

    bk_top1_name = ''
    bk_top1_home = 0
    bk_top1_draw = 0
    bk_top1_away = 0
    index_top1 = 0
    if bk_coef_name != []:
        for bk1 in range(len(bk_coef_home) - 1):
            if float(bk_coef_home[bk1]) > bk_top1_home and float(bk_coef_away[bk1]) > bk_top1_away:
                bk_top1_name = bk_coef_name[bk1]
                bk_top1_home = float(bk_coef_home[bk1])
                bk_top1_draw = float(bk_coef_draw[bk1])
                bk_top1_away = float(bk_coef_away[bk1])
                index_top1 = bk1
        del bk_coef_name[index_top1], bk_coef_home[index_top1], bk_coef_draw[index_top1], bk_coef_away[index_top1]
    else:
        bk_top1_name = ''
        bk_top1_home = 0
        bk_top1_draw = 0
        bk_top1_away = 0


    bk_top2_name = ''
    bk_top2_home = 0
    bk_top2_draw = 0
    bk_top2_away = 0
    index_top2 = 0
    if bk_coef_name != []:
        for bk2 in range(len(bk_coef_home) - 1):
            if float(bk_coef_home[bk2]) > bk_top2_home and float(bk_coef_away[bk2]) > bk_top2_away:
                bk_top2_name = bk_coef_name[bk2]
                bk_top2_home = float(bk_coef_home[bk2])
                bk_top2_draw = float(bk_coef_draw[bk2])
                bk_top2_away = float(bk_coef_away[bk2])
                index_top2 = bk2
        del bk_coef_name[index_top2], bk_coef_home[index_top2], bk_coef_draw[index_top2], bk_coef_away[index_top2]
    else:
        bk_top2_name = ''
        bk_top2_home = 0
        bk_top2_draw = 0
        bk_top2_away = 0

    bk_top3_name = ''
    bk_top3_home = 0
    bk_top3_draw = 0
    bk_top3_away = 0
    if bk_coef_name != []:
        for bk3 in range(len(bk_coef_home)):
            if float(bk_coef_home[bk3]) > bk_top3_home and float(bk_coef_away[bk3]) > bk_top3_away:
                bk_top3_name = bk_coef_name[bk3]
                bk_top3_home = float(bk_coef_home[bk3])
                bk_top3_draw = float(bk_coef_draw[bk3])
                bk_top3_away = float(bk_coef_away[bk3])

    else:
        bk_top3_name = ''
        bk_top3_home = 0
        bk_top3_draw = 0
        bk_top3_away = 0

    # print(list_for_goal_home)



    if predictions_percent_home != '0%' and predictions_percent_away != '0%' and predictions_percent_draw != '0%':
        if int(predictions_percent_home[:2]) >= int(predictions_percent_away[:2]):
            home_win_or_lose = 'win (win or draw)'
        elif int(predictions_percent_home[:2]) <= int(predictions_percent_away[:2]):
            home_win_or_lose = 'loss (loss or draw)'
    elif predictions_percent_home == '0%' :
        predictions_percent_home = '0'
        home_win_or_lose = 'loss (loss or draw)'
    elif predictions_percent_away == '0%' :
        predictions_percent_away = '0'
        home_win_or_lose = 'win (win or draw)'

    if predictions_percent_home != '0%' and predictions_percent_away != '0%' and predictions_percent_draw != '0%':
        if int(predictions_percent_home[:2]) >= int(predictions_percent_away[:2]):
            home_win_or_lose_ru = 'победа (победа или ничья)'
        elif int(predictions_percent_home[:2]) <= int(predictions_percent_away[:2]):
            home_win_or_lose_ru = 'проигрыш (проигрыш или ничья)'
    elif predictions_percent_home == '0%' :
        predictions_percent_home_ru = '0'
        home_win_or_lose_ru = 'проигрыш (проигрыш или ничья)'
    elif predictions_percent_away == '0%' :
        predictions_percent_away_ru = '0'
        home_win_or_lose_ru = 'победа (победа или ничья)'
    # elif predictions_percent_home == '0%' and predictions_percent_away == '0%'




    data = [{
        "img_preview":"path",
        "title1": {
            "team_name_home":f"{name_home_preview}",
            "team_name_away":f"{name_away_preview}"
        },
        "subtitle_start":{
            "date":date_match[5:10], 
            "full_date":date_match,
            "venue":venue
        },
        "standings":{
            "league_name": name_league, #TODO Сделать название Лиги
            "rank_team_home":rank_team_home,
            "rank_team_away":rank_team_away
        },
            
            "title":f"Статистика по игрокам",
            "scorers_a_b": {
                "home_top_name":f"{players_a_name}",
                "home_top_total":f"{players_a_goals_total}",
                "away_top_name":f"{players_b_name}",
                "away_top_total":f"{players_b_goals_total}"
            },
            "table_scorers":{
                "title_table_scorers":f"Тройка же лидеров среди бомбардиров выглядит так:",
                "first_top_name":f"{topscorer_name_in_league_1}",
                "first_top_team":f"{topscorer_team_in_league_1}",
                "first_top_amount":f"{topscorer_amount_in_league_1}",
                "second_top_name":f"{topscorer_name_in_league_2}",
                "second_top_team":f"{topscorer_team_in_league_2}",
                "second_top_amount":f"{topscorer_amount_in_league_2}",
                "third_top_name":f"{topscorer_name_in_league_3}",
                "third_top_team":f"{topscorer_team_in_league_3}",
                "third_top_amount":f"{topscorer_amount_in_league_3}",
                "fourth_top_name":f"{topscorer_name_in_league_4}",
                "fourth_top_team":f"{topscorer_team_in_league_4}",
                "fourth_top_amount":f"{topscorer_amount_in_league_4}",
                "fifth_top_name":f"{topscorer_name_in_league_5}",
                "fifth_top_team":f"{topscorer_team_in_league_5}",
                "fifth_top_amount":f"{topscorer_amount_in_league_5}"
                },
                "title":f"Лучшие игроки обеих команд по другим основным статистическим показателям текущего сезона:",
                "assists":{
                        "topscorers_assists_home_name":topscorers_assists_home_name,
                        "topscorers_assists_home_amount":topscorers_assists_home_amount,
                        "topscorers_assists_away_name":topscorers_assists_away_name,
                        "topscorers_assists_away_amount":topscorers_assists_away_amount,
                    },
                "saves":{
                        "topscorers_saves_home_name":topscorers_saves_home_name,
                        "topscorers_saves_home_amount":topscorers_saves_home_amount,
                        "topscorers_saves_away_name":topscorers_saves_away_name,
                        "topscorers_saves_away_amount":topscorers_saves_away_amount
                    },

                "blocks":{
                        "topscorers_interceptions_home_name":topscorers_interceptions_home_name,
                        "topscorers_interceptions_home_amount":topscorers_interceptions_home_amount,
                        "topscorers_interceptions_away_name":topscorers_interceptions_away_name,
                        "topscorers_interceptions_away_amount":topscorers_interceptions_away_amount
                    },
                "duels":{
                        "topscorers_duels_home_name":topscorers_duels_home_name,
                        "topscorers_duels_home_amount":topscorers_duels_home_amount,
                        "topscorers_duels_away_name":topscorers_duels_away_name,
                        "topscorers_duels_away_amount":topscorers_duels_away_amount
                    },
                "fouls":{
                        "name_home_top_fouls_yel_card":name_home_top_fouls_yel_card,
                        "amount_home_fouls_yel_card":amount_home_fouls_yel_card,
                        "name_away_top_fouls_yel_card":name_away_top_fouls_yel_card,
                        "amount_away_fouls_yel_card":amount_away_fouls_yel_card,
                        "name_home_top_fouls_red_card":name_home_top_fouls_red_card,
                        "amount_home_fouls_red_card":amount_home_fouls_red_card,
                        "name_away_top_fouls_red_card":name_away_top_fouls_red_card,
                        "amount_away_fouls_red_card":amount_away_fouls_red_card
                    },                       

        "team_statistics":{
            "forms":{
                "home":f"{form_home}",
                "away":f"{form_away}"
            }
        },
            "clean_sheet":{
                "home_play_clean_sheet":home_play_clean_sheet,
                "away_play_clean_sheet":away_play_clean_sheet
            },
            "biggest":{
                "home":{
                    "win":{
                        "home":home_biggest_win_in_home,
                        "away":home_biggest_win_in_away
                    }
                },
                    "lose":{
                        "home":home_biggest_lose_in_home,
                        "away":home_biggest_lose_in_away
                    }
                },
                "away":{
                    "win":{
                        "home":away_biggest_win_in_home,
                        "away":away_biggest_win_in_away
                    },
                    "lose":{
                        "home":away_biggest_lose_in_home,
                        "away":away_biggest_lose_in_away
                    }
                },
            
            "win_once":{
                "home":{
                    "win":home_win_once_in_home,
                    "draws":home_draws_once_in_home,
                    "lose":home_lose_once_in_home
                },
                "away":{
                    "win":away_win_once_in_away,
                    "draws":away_draws_once_in_away,
                    "lose":away_lose_once_in_away
                }
            },
            "goals":{
                "home":{
                    "g":list_for_goal_home,
                    "m":list_missed_goal_home
                },
                "away":{
                    "g":list_for_goal_away,
                    "m":list_missed_goal_away
                }
            },
        "Table_h2h":{
            "title":"Статистика личных встреч:",
            "games":h2h_home_total_games,
            "team_home":{
                "name":name_home_preview,
                "win_home":h2h_home_total_wins_in_home,
                "win_away":h2h_home_total_wins_in_away,
                "draws_home":h2h_home_total_draws_in_home,
                "draws_away":h2h_home_total_draws_in_away,
                "loses_home":h2h_home_total_loses_in_home,
                "loses_away":h2h_home_total_loses_in_away
                },
            "team_away":{
                "name":name_away_preview,
                "win_home":h2h_away_total_wins_home,
                "win_away":h2h_away_total_wins_away,
                "draws_home":h2h_away_total_draws_in_home,
                "draws_away":h2h_away_total_draws_in_away,
                "loses_home":h2h_away_total_loses_in_home,
                "loses_away":h2h_away_total_loses_in_away
                }    
            },
        "Сomparison":{
            "title":"Вероятностные характеристики команд перед матчем:",
            "table":{
                "team_home":{
                    "name":name_home_preview,
                    "win":comparison_total_home,
                    "attack":comparison_att_home,
                    "def":comparison_def_home,
                    "t2t":comparison_h2h_home,
                    "goals":comparison_goals_home
                },
                "text":{
                    "text1":"Выигрыш игры",
                    "text2":"Потенциал в атаке",
                    "text3":"Потенциал в защите",
                    "text4":"Сила друг против друга",
                    "text5":"Потенциал голов"
                },
                "team_away":{
                    "name":name_away_preview,
                    "win":comparison_total_away,
                    "attack":comparison_att_away,
                    "def":comparison_def_away,
                    "t2t":comparison_h2h_away,
                    "goals":comparison_goals_away
                }
            }
                },
            "subtitle":{
                #TODO
                "predictions_home_goals":f"{predictions_goals_home}",
                "predictions_away_goals":f"{predictions_goals_away}",
                "predictions_win_home":f"{predictions_percent_home}", 
                "predictions_draws":f"{predictions_percent_draw}", 
                "predictions_win_away":f"{predictions_percent_away}",
                "predictions_home_win_or_lose":f"{home_win_or_lose}",

                "home_win_or_lose_ru":f"{home_win_or_lose_ru}",

                
            },
            "bk":{
                "title":"Ну и вот лучшие коэффициенты букмекеров на этот матч:",
                "table":{
                    "bk1":f"{bk_top1_name}",
                    "bk1_win_home":f"{bk_top1_home}",
                    "bk1_draw":f"{bk_top1_draw}",
                    "bk1_win_away":f"{bk_top1_away}",
                    "bk2":f"{bk_top2_name}",
                    "bk2_win_home":f"{bk_top2_home}",
                    "bk2_draw":f"{bk_top2_draw}",
                    "bk2_win_away":f"{bk_top2_away}",
                    "bk3":f"{bk_top3_name}",
                    "bk3_win_home":f"{bk_top3_home}",
                    "bk3_draw":f"{bk_top3_draw}",
                    "bk3_win_away":f"{bk_top3_away}",
                },
            },
            "end":f"Напоминаем, что матч между командами «{name_home_preview}» и «{name_away_preview}» состоится {date_match[5:10]} на {venue}."
        }]
        


    output_path = root_folder / "result" / "json" / f"{fixture_match}_preview.json"
    with open(output_path, "w+", encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
    
    # print('text')
# preview_match_text('867948')





#     text = (
#         f"**Игра** {name_home_preview} **и** {name_away_preview} **состоится** {date_match} на стадионе {venue}**.\n",
#         f"У команд уже накопилась общая история: взглянем на исходы предыдущих матчей и коэффициенты букмекерских компаний.**\n",
#         f"По очкам в чемпионате Премьер-лиги {season} {name_home_preview} по данным на сегодня занимает {rank_team_home} место, соперник — на {rank_team_away} позиции.\n",
#         f"Самые результативные игроки команд: ",
#         f"Среди игроков {name_home_preview} наибольшим количеством голов отметился {players_a_name} {players_a_goals_total}. У соперника {players_b_name} забил {players_b_goals_total}. \n",
#         f"Лидеры по количеству голов в лиге на сегодняшний день: ",
#         f"1. {topscorer_name_in_league_1} ({topscorer_team_in_league_1}) — {topscorer_amount_in_league_1}.\n2. {topscorer_name_in_league_2} ({topscorer_team_in_league_2}) — {topscorer_amount_in_league_2}.\n3. {topscorer_name_in_league_3} ({topscorer_team_in_league_3}) — {topscorer_amount_in_league_3}. \n"
#         f"Кто решал исходы прошедших матчей команд текущего сезона: ",
#         f"Голевые передачи: {topscorers_assists_home_name} ({name_home_preview}) — {topscorers_assists_home_amount} передач, {topscorers_assists_away_name} {name_away_preview} — {topscorers_assists_away_amount} передач. \n",
#         f"Сейвы голкиперов команд: {topscorers_saves_home_name} ({name_home_preview}) — {topscorers_saves_home_amount}, {topscorers_saves_away_name} {name_away_preview} — {topscorers_saves_away_amount}. \n",
#         f"Отборы мяча: {topscorers_interceptions_home_name} ({name_home_preview}) — {topscorers_interceptions_home_amount}, {topscorers_interceptions_away_name} ({name_away_preview}) — {topscorers_interceptions_away_amount}.    \n",
#         f"Больше всех выигранных дуэлей: {topscorers_duels_home_name} ({name_home_preview}) — {topscorers_duels_home_amount}, {topscorers_duels_away_name} {name_away_preview} — {topscorers_duels_away_amount}. \n",
#         f"Нарушители правил: {topscorers_fouls_home_name} ({name_home_preview}) — {topscorers_fouls_home_amount} нарушений, {topscorers_fouls_away_name} {name_away_preview} — {topscorers_fouls_away_amount}.  \n",
#         f"Командная статистика: ",
#         f"Для сравнения посмотрим результаты пяти недавних игр каждой из команд:\n{name_home_preview} {form_home} \n{name_away_preview} {form_away}  \n",
#         f"На ноль команды в этом сезоне отыграли: {name_home_preview} — {home_play_clean_sheet} раз, {name_away_preview} — {away_play_clean_sheet} раз. \n",
#         f"Самые крупные победы и поражения обеих команд: \n ",
#         f"{name_home_preview}: {home_biggest_win_in_home} — победа дома и {home_biggest_win_in_away} — победа на выезде.\n{name_home_preview}: {home_biggest_lose_in_home} — проигрыш дома и {home_biggest_lose_in_away} — проигрыш на выезде. \n",
#         f"{name_away_preview}: {away_biggest_win_in_home} — победа дома и {away_biggest_win_in_away} — победа на выезде. \n{name_away_preview}: {away_biggest_lose_in_home} — проигрыш дома и {away_biggest_lose_in_away} — проигрыш на выезде. \n",
#         f"{name_home_preview} в текущем сезоне выигрывала дома {home_win_once_in_home} раз, проигрывала {home_lose_once_in_home} и сыграла в ничью {home_draws_once_in_home} раз \n",
#         f"{name_away_preview} на выезде победила {away_win_once_in_away} раз, потерпела поражение {away_lose_once_in_away} раз и уехала с ничьей {away_draws_once_in_away} раз. \n" ,
#         f"Пиковая активность у команд в этом сезоне приходится на следующие отрезки матчей \n",
#         f"{name_home_preview} забивала с{text_home_for[:-2]} и пропускала с{text_home_missed[:-2]}",
#         f"{name_away_preview} забивала с{text_away_for[:-2]} и пропускала с{text_away_missed[:-2]}",
#         f"Статистика личных встреч за последние три сезона: \n",
#         f"Команда:{name_home_preview}, {name_away_preview} \n",
#         f"Игры: {h2h_home_total_games}, {h2h_away_total_games} \n",
#         f"Выигрыши (Дома): {h2h_home_total_wins_in_home}, {h2h_away_total_wins_home} \n",
#         f"Выигрыши (Гости): {h2h_home_total_wins_in_away}, {h2h_away_total_wins_away} \n",
#         f"Ничьи (Дома): {h2h_home_total_draws_in_home}, {h2h_away_total_draws_in_home} \n",
#         f"Ничьи (Гости): {h2h_home_total_draws_in_away}, {h2h_away_total_draws_in_away} \n",
#         f"Поражения (Дома): {h2h_home_total_loses_in_home}, {h2h_away_total_loses_in_home} \n",
#         f"Поражения (Гости): {h2h_home_total_loses_in_away}, {h2h_away_total_loses_in_away} \n",
#         f"Вероятностные характеристики команд перед матчем: \n",
#         f"{name_home_preview} {name_away_preview} \n",
#         f"{comparison_total_home} Выигрыш игры {comparison_total_away} \n",
#         f"{comparison_att_home} Потенциал в атаке {comparison_att_away} \n",
#         f"{comparison_def_home} Потенциал в защите {comparison_def_away} \n",
#         f"{comparison_h2h_home} Сила друг против друга {comparison_h2h_away} \n",
#         f"{comparison_goals_home} Потенциал голов {comparison_goals_away} \n",
#         f"Прогноз на матч следующий: победа {name_home_preview} — вероятность \n",
#         f"{predictions_percent_home}, победа {name_away_preview} — {predictions_percent_away}, вероятность \n",
#         f"ничьей — {predictions_percent_draw}. \n",
#         f"Вероятнее всего, голов от {name_home_preview} можно ожидать в количестве \n" ,
#         f"{predictions_goals_home}, а от {name_away_preview} — {predictions_goals_away}. \n",
#         f"Коэффициенты букмекеров на этот матч следующие: {bk_top1_name}: {name_home_preview} - {bk_top1_home}, ничья - {bk_top1_draw}, {name_away_preview} - {bk_top1_away} \n ",
#         f"{bk_top2_name}: {name_home_preview} - {bk_top2_home}, ничья - {bk_top2_draw}, {name_away_preview} - {bk_top2_away} \n",
#         f"{bk_top3_name}: {name_home_preview} - {bk_top3_home}, ничья - {bk_top3_draw}, {name_away_preview} - {bk_top3_away}")
        
#     #print(text)

#         #f"{name_away_preview} забивала с {list_minute_for_goals_away[0]} {list_for_goal_away[0]} vs {list_minute_for_goals_away[1]} {list_for_goal_away[1]} vs {list_minute_for_goals_away[2]} {list_for_goal_away[2]} vs {list_minute_for_goals_away[3]} {list_for_goal_away[3]} vs {list_minute_for_goals_away[4]} {list_for_goal_away[4]} vs {list_minute_for_goals_away[5]} {list_for_goal_away[5]} vs {list_minute_for_goals_away[6]} {list_for_goal_away[6]} vs {list_minute_for_goals_away[7]} {list_for_goal_away[7]} и пропускала с {list_minute_missed_goals_away[0]} {list_missed_goal_away[0]} vs {list_minute_missed_goals_away[1]} {list_missed_goal_away[1]} vs {list_minute_missed_goals_away[2]} {list_missed_goal_away[2]} vs {list_minute_missed_goals_away[3]} {list_missed_goal_away[3]} vs {list_minute_missed_goals_away[4]} {list_missed_goal_away[4]} vs {list_minute_missed_goals_away[5]} {list_missed_goal_away[5]} vs {list_minute_missed_goals_away[6]} {list_missed_goal_away[6]} vs {list_minute_missed_goals_away[7]} {list_missed_goal_away[7]}.\n",
#         # f"{name_home_preview} забивала с {list_minute_for_goals_home[i]} {list_for_goal_home[i]} vs {list_minute_for_goals_home[i]} {list_for_goal_home[i]} vs {list_minute_for_goals_home[i]} {list_for_goal_home[i]} vs {list_minute_for_goals_home[i]} {list_for_goal_home[i]} vs {list_minute_for_goals_home[i]} {list_for_goal_home[i]} vs {list_minute_for_goals_home[5]} {list_for_goal_home[5]} vs {list_minute_for_goals_home[6]} {list_for_goal_home[6]} vs {list_minute_for_goals_home[7]} {list_for_goal_home[7]} и пропускала с {list_minute_missed_goals_home[0]} {list_missed_goal_home[0]} vs {list_minute_missed_goals_home[1]} {list_missed_goal_home[1]} vs {list_minute_missed_goals_home[2]} {list_missed_goal_home[2]} vs {list_minute_missed_goals_home[3]} {list_missed_goal_home[3]} vs {list_minute_missed_goals_home[4]} {list_missed_goal_home[4]} vs {list_minute_missed_goals_home[5]} {list_missed_goal_home[5]} vs {list_minute_missed_goals_home[6]} {list_missed_goal_home[6]} vs {list_minute_missed_goals_home[7]} {list_missed_goal_home[7]}.\n",
#         # f"{name_away_preview} забивала с {list_minute_for_goals_away[0]} {list_for_goal_away[0]} vs {list_minute_for_goals_away[1]} {list_for_goal_away[1]} vs {list_minute_for_goals_away[2]} {list_for_goal_away[2]} vs {list_minute_for_goals_away[3]} {list_for_goal_away[3]} vs {list_minute_for_goals_away[4]} {list_for_goal_away[4]} vs {list_minute_for_goals_away[5]} {list_for_goal_away[5]} vs {list_minute_for_goals_away[6]} {list_for_goal_away[6]} vs {list_minute_for_goals_away[7]} {list_for_goal_away[7]} и пропускала с {list_minute_missed_goals_away[0]} {list_missed_goal_away[0]} vs {list_minute_missed_goals_away[1]} {list_missed_goal_away[1]} vs {list_minute_missed_goals_away[2]} {list_missed_goal_away[2]} vs {list_minute_missed_goals_away[3]} {list_missed_goal_away[3]} vs {list_minute_missed_goals_away[4]} {list_missed_goal_away[4]} vs {list_minute_missed_goals_away[5]} {list_missed_goal_away[5]} vs {list_minute_missed_goals_away[6]} {list_missed_goal_away[6]} vs {list_minute_missed_goals_away[7]} {list_missed_goal_away[7]}.\n",
    
 
    
#     return ''.join(text)
    #print('test')

# preview_match_text("868112")