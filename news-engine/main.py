import json
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]

platform_name = 'wordpress'
platform_url = 'https://botbot.news/wp-json/wp/v2/posts'
platform_user = 'botbot'
platform_password = 'cGvj MT0x lqRl cEuY tddX'


# user_id = '1'

def create_subscribe(user_id):
    data = {
        "platform": {
            "name": f"{platform_name}",
            "url": f"{platform_url}",
            "user": f"{platform_user}",
            "password": f"{platform_password}",
        },
        "Parameters": {
            "list_teams": " ",
            "text": {
                "text_match_preview": f"/opt/footballBot/parameters/users/football/text/{user_id}_preview_match.json",
                "text_match_review": f"/opt/footballBot/parameters/users/football/text/{user_id}_review_match.json",
                "text_round_preview": f"/opt/footballBot/parameters/users/football/text/{user_id}_preview_round.json",
                "text_round_review": f"/opt/footballBot/parameters/users/football/text/{user_id}_review_round.json"
            },
            "time": {
                "preview_match": "8",
                "review_match": "0",
                "review_round": "",
                "preview_round": ""
            },
        }
    }

    with open(f"/opt/footballBot/parameters/football/users/parameters/{user_id}.json", "w",
              encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


# TODO Need to create a func which will create text for profiles
def create_text(user_id, types):
    if types == 'review' or types == 'preview':
        with open(f'/opt/footballBot/parameters/football/users/html/{user_id}_{types}_match.html') as file_html:
            text_html = file_html.read()

        if types == 'review':
            data = {
                "title": "{team1} vs {team2} {goals_a}:{goals_b}. Match details",
                "main_text": f"{text_html}",
                "y_cards": "<p><b>Yellow cards: </b></p>",
                "r_cards": "<p><b>Red cards: </b></p>",
                "fouls_title": "<h4><b>Fouls:</b></h4>",
                "penalties_title": "<h4><b>Penalties in a match:</b></h4>",
                "goalscorers": "<h4><b>Goalscorers:</b></h4>"
            }
        elif types == 'preview':
            data = {
                "title": "{team1} — {team2}. Some interesting stats before the match",
                "title_big_home_in_home": "in the home game",
                "title_big_home_in_away": "on the guest arena",
                "title_big_away_in_home": "with a biggest score",
                "title_big_home_in_away_AWAY": "and away with a score",
                "main_text": f"{text_html}"
            }
        types = types + '_match'
    elif types == 'preview_round' or types == 'review_round':

        with open(f'/opt/footballBot/parameters/football/users/html/{user_id}_{types}.html') as file_html:
            text_html = file_html.read()

        if types == 'preview_round':
            data = {
                "title": "MatchDay {rounds_for_text} of {first_date_round} will start today. Some stats before the games.",
                "main_text": f"{text_html}"
            }
        elif types == 'review_round':
            data = {
                "title": "All results and other stats of Match Day {rounds} of {all_rounds}",
                "main_text": f"{text_html}"
            }
    elif types == 'preview_round2' or types == 'review_round2':

        with open(f'/opt/footballBot/parameters/football/users/html/{user_id}_{types}.html') as file_html:
            text_html = file_html.read()

        if types == 'preview_round2':
            data = {
                "title": "Сегодня начинается {rounds_for_text} тур чемпионата {league_name}. Самая интересная статистика перед началом матчей",
                "main_text": f"{text_html}"
            }
        elif types == 'review_round2':
            data = {
                "title": "Состоялись матчи {rounds_for_text} тура чемпионата {league_name}. Все результаты и другая статистика",
                "main_text": f"{text_html}"
            }

    with open(f"/opt/footballBot/parameters/football/users/text/{user_id}_{types}.json", "w",
              encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


# create_text('2', 'preview_round2')
# create_text('2', 'preview_round2')