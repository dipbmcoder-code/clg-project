import boto3
import os
from time import sleep

from PIL import Image, ImageDraw, ImageFont
from db import get_data_round
from urllib.request import urlopen
import requests


# Сохранение на aws
def save_preview_aws(rounds, league_id):
    access_key = 'KEY'
    secret_access_key = 'KEY'

    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

    list_l = ['eng', 'ru']
    for i in range(len(list_l)):
        client.upload_file(f"/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_preview.png","buckets-botbot-football", f"match/{list_l[i]}_{league_id}_{rounds}_preview.png", ExtraArgs={'ACL':'public-read'})

def delete(league_id, rounds, types):
    list_l = ['eng', 'ru']
    for i in range(len(list_l)):
        os.remove(f'/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_{types}.png')



def start_create_img_preview_round(rounds, league_id):

    """
    Создает фьючерс картинку для раунда
    Вытаскиваем данные с бд
    Создаем фон и наносим нужные данные на
    Меняем язык, если требуется

    """
    

    insert_query = (
        f"SELECT rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds FROM round_preview WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_preview_round = get_data_round(insert_query)
    
    index_text_preview_round = index_text_preview_round[0]

    rounds, season, league_id, first_date_round, venue_first_match, city_first_match, home_first_match, away_first_match, preview_home_teams, preview_away_teams, count_matchs, last_round, team_name_max_injuries, max_injuries, team_max_goals_league, max_goals_league, team_id_max_goals_league, team_min_conceded_league, min_conceded_top_saves, team_id_top_min_conceded, team_max_clean_sheet_league, max_cleen_sheet_league, team_id_clean_sheet_league, team_max_conceded_league, max_conceded_saves_league, team_id_max_conceded_league, team_min_goals_attack_league, min_goals_attack_league, id_team_min_attack, goals_top_league_1, name_top_goals_league_1, goals_top_league_2, name_top_goals_league_2, goals_top_league_3, name_top_goals_league_3, goals_top_league_4, name_top_goals_league_4, goals_top_league_5, name_top_goals_league_5, assists_top_league_1, name_top_assists_league_1, assists_top_league_2, name_top_assists_league_2, assists_top_league_3, name_top_assists_league_3, assists_top_league_4, name_top_assists_league_4, assists_top_league_5, name_top_assists_league_5, saves_top_league_1, name_top_saves_league_1, saves_top_league_2, name_top_saves_league_2, saves_top_league_3, name_top_saves_league_3, saves_top_league_4, name_top_saves_league_4, saves_top_league_5, name_top_saves_league_5, team_max_without_scored_league, max_without_scored_league, wins_without_scored, loses_without_scored, draws_without_scored, team_max_conceded_goals_league, max_conceded_goals_league, wins_conceded_goals, loses_conceded_goals, draws_conceded_goals, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_matches, odds_win_home, odds_win_away, odds_draw, top_win_home, top_win_away, top_draw, index_main_match, team_top_goals_league1, team_top_goals_league2, team_top_goals_league3, team_top_goals_league4, team_top_goals_league5, team_top_assists_league1, team_top_assists_league2, team_top_assists_league3, team_top_assists_league4, team_top_assists_league5, team_top_saves_league1, team_top_saves_league2, team_top_saves_league3, team_top_saves_league4, team_top_saves_league5, league_name, date_previous_match, away_previous_match, goals_home_previous_match, goals_away_previous_match, league_logo, future_fixture_round, future_date_round, all_rounds = index_text_preview_round

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

        logo_league = Image.open(urlopen(league_logo))

        if league_name == "Premier League":
            league_name = "English Premier League"

        round_text = ImageDraw.Draw(background)
        # round_text.line(((725, 200), (725, 200)), "red") #якорь, метка откуда начинается текст
        # round_text.line(((600, 1350), (900, 1350)), "red")

        if list_l[i] == 'eng':
            round_text.text((320, 80), f"Regular season. Match Day {rounds} of {all_rounds}", anchor="ms", font=font_for_round, fill='white')

        elif list_l[i] == 'ru':
            
            font_for_round = ImageFont.truetype('/opt/footballBot/tools/fonts/days2.ttf', size=20)
            font_for_league = ImageFont.truetype('/opt/footballBot/tools/fonts/days2.ttf', size=35)

            round_text.text((320, 80), f"Регулярный сезон. Тур {rounds} из {all_rounds}", anchor="ms", font=font_for_round, fill='white')

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
        new_image.save(f'/opt/footballBot/result/img_match/{list_l[i]}_{league_id}_{rounds}_preview.png')

        sleep(2)

    # Сохранение на aws
    save_preview_aws(rounds, league_id)



# start_create_img_preview_round(18, 39)

    
