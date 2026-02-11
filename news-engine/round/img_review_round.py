import boto3
import os
from time import sleep
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from db import get_data_round
from urllib.request import urlopen
import requests
load_dotenv()

# Сохранение на aws
def save_preview_aws(rounds, league_id):
    access_key = 'KEY'
    secret_access_key = 'KEY'

    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    list_l = ['eng', 'ru']
    for i in range(len(list_l)):
        client.upload_file(f"/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_review.png","buckets-botbot-football", f"match/{list_l[i]}_{league_id}_{rounds}_review.png", ExtraArgs={'ACL':'public-read'})

def delete(league_id, rounds, types):
    list_l = ['eng', 'ru']
    for i in range(len(list_l)):
        os.remove(f'/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_{types}.png')   

def start_create_img_review_round(rounds, league_id):

    """
    Создает фьючерс картинку для раунда
    Вытаскиваем данные с бд
    Создаем фон и наносим нужные данные на
    Меняем язык, если требуется

    """

    insert_query = (
        f"SELECT rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home, goals_away, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves FROM round_review WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_review_round = get_data_round(insert_query)
    
    index_text_review_round = index_text_review_round[0]

    rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader,goal_rival, name_home_review,  name_away_review, count_home,count_away,count_draw, h3_amounts_list, h3_names_list, h3_team_names_list,h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4 , team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1,all_goals_round,all_penalty_round,all_goals_previous_round, total_percent_round,average_goals_in_season,average_penalty_in_season,time_fast_goal,team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer , max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator , goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount , name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round , name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round,top_round_injuries_name_team,top_round_injuries_amount,name_top_assists_league_1,assists_top_league_1,team_top_assists_league1, name_top_assists_league_2,assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3 , team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5 , rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table , win_matches_table , draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds, total_of_round_top_assists_league_1, total_of_round_top_assists_league_2, total_of_round_top_assists_league_3, total_of_round_top_assists_league_4, total_of_round_top_assists_league_5, total_of_round_top_saves_league_1, total_of_round_top_saves_league_2, total_of_round_top_saves_league_3, total_of_round_top_saves_league_4, total_of_round_top_saves_league_5, goals_home, goals_away, goals_and_info_max_saves, total_name_top_goals_league_1_round, total_name_top_goals_league_2_round, total_name_top_goals_league_3_round, total_name_top_goals_league_4_round, total_name_top_goals_league_5_round, city_next_round, date_game_max_saves = index_text_review_round


    insert_query = (
        f"SELECT league_logo FROM round_preview WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_preview_round = get_data_round(insert_query)
    
    index_text_preview_round = index_text_preview_round[0]

    league_logo = index_text_preview_round[0]


    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures/rounds"

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }

    req_all_rounds = requests.get(url, headers=headers, params={
        "league":league_id,
        "season":season
        })
    data_all_rounds = req_all_rounds.json()


    all_rounds = len(data_all_rounds['response'])

    font_for_league = ImageFont.truetype('/opt/footballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=40)
    font_for_round = ImageFont.truetype('/opt/footballBot/tools/fonts/Kanit-SemiBoldItalic.ttf', size=20)
    list_l = ['eng', 'ru']
  
    

    logo_league = Image.open(urlopen(league_logo))

    if league_name == "Premier League":
        league_name = "English Premier League"

    for i in range(len(list_l)):

        background = ''
        if league_name == "Premier League" or league_name == "English Premier League":
            background = Image.open('/opt/footballBot/tools/img/EPL.png')
        elif league_name == "Bundesliga":
            background = Image.open('/opt/footballBot/tools/img/bundesliga.png')
        elif league_name == "Ligue 1":
            background = Image.open('/opt/footballBot/tools/img/ligue_1.png')
        elif league_name == "La Liga":
            background = Image.open('/opt/footballBot/tools/img/la_liga.png')
        elif league_name == "Serie A":
            background = Image.open('/opt/footballBot/tools/img/seria_a.png')
        elif league_name == "Primeira Liga":
            background = Image.open('/opt/footballBot/tools/img/primeira_liga.png')
        
        round_text = ImageDraw.Draw(background)
        # round_text.line(((725, 200), (725, 200)), "red") #якорь, метка откуда начинается текст
        # round_text.line(((600, 1350), (900, 1350)), "red")
        
        if list_l[i] == 'eng':
            round_text.text((320, 80), f"Match Day {rounds}: Results and stats", anchor="ms", font=font_for_round, fill='white')
        elif list_l[i] == 'ru':
            
            font_for_round = ImageFont.truetype('/opt/footballBot/tools/fonts/days2.ttf', size=20)
            font_for_league = ImageFont.truetype('/opt/footballBot/tools/fonts/days2.ttf', size=35)
            
            round_text.text((320, 80), f"Тур {rounds}: Результат и статистика", anchor="ms", font=font_for_round, fill='white')
            
            
            # if league_name == "English Premier League":
            #     league_name = "Английская премьер-лига"
            # elif league_name == "Bundesliga":
            #     league_name = "Бундеслига"
            # elif league_name == "Ligue 1":
            #     league_name = "Французкая Лига-1"
            # elif league_name == "La Liga":
            #     league_name = "Ла Лига"
            # elif league_name == "Serie A":
            #     league_name = "Сериа-А"
            # elif league_name == "Primeira Liga":
            #     league_name = "Португальская премьер-лига"


        league_text = ImageDraw.Draw(background)
        # league_text.line(((320, 200), (320, 200)), "red") #якорь, метка откуда начинается текст
        # league_text.line(((100, 180), (200, 180)), "red")
        league_text.text((320, 280), league_name, anchor="ms", font=font_for_league, fill='white')


        new_size_logo1 = logo_league.resize((130, 130))
        
        background.paste(new_size_logo1, (250, 100), mask=new_size_logo1.convert('RGBA'))

        #Сохранение
        new_image = background.resize((1778, 1000))
        new_image.save(f'/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_review.png')
        
        sleep(2)

    # Сохранение на aws
    save_preview_aws(rounds, league_id)



# start_create_img_review_round(19, 140)

    
