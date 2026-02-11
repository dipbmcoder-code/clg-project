import requests
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def check_match_round_api(league, season, round):

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures"

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    if league != '1': round_req = f"Regular Season - {round}"
    elif league == '1': round_req = f"Group Stage - {round}"

    req_tour_review = requests.request("GET", url, headers=headers, params={
            "league": f"{league}",
            "season": f"{season}",
            "round": f"{round_req}"
        })
    data_tour_review = req_tour_review.json()
    return data_tour_review

def get_round(league, season):
    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures/rounds"


    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    req_tour_review = requests.request("GET", url, headers=headers, params={
        "league":f"{league}",
        "season":f"{season}",
        "current":"true"
    })
    data_tour_review = req_tour_review.json()
    data_tour_review = data_tour_review['response'][0]
    if 'Regular Season - ' in data_tour_review:return data_tour_review.replace("Regular Season - ", "")
    elif 'Group Stage - ' in data_tour_review:return data_tour_review.replace("Group Stage - ", "")

# get_round(39, 2022)
def check_match_list_rounds_api(league, season, round):

    data_tour_review = check_match_round_api(league, season, round)
    fixtures_mathces = []
    fixtures_mathces_postponed = []
    date_mathes_postponed = []
    date_mathes = []
    for find_mathes in range(len(data_tour_review['response'])):
        if data_tour_review['response'][find_mathes]['fixture']['status']['long'] != 'Match Postponed':
            fixtures_mathces.append(data_tour_review['response'][find_mathes]['fixture']['id'])
            date_mathes.append(data_tour_review['response'][find_mathes]['fixture']['date'][:16])
        elif data_tour_review['response'][find_mathes]['fixture']['status']['long'] == 'Match Postponed':
            fixtures_mathces_postponed.append(data_tour_review['response'][find_mathes]['fixture']['id'])
            date_mathes_postponed.append(data_tour_review['response'][find_mathes]['fixture']['date'][:16])



    return fixtures_mathces, fixtures_mathces_postponed

def get_date_next_round(league, season, round):

    data_tour_review = check_match_round_api(league, season, round)

    date_main = ''
    for find_mathes in range(len(data_tour_review['response'])):
        if data_tour_review['response'][find_mathes]['fixture']['status']['long'] != 'Match Postponed':
            date = data_tour_review['response'][find_mathes]['fixture']['date']
            date = datetime.datetime.strptime(date[:15], '%Y-%m-%dT%H:%M')
            # print(date)
            if date_main != '':
                if date < date_main:
                    date_main = date
                elif date > date_main:
                    pass
                else:
                    pass
            elif date_main == '':
                date_main = date
    # print(date_main)
    return date_main

def get_date_last_fixture_round_now(league, season, round):

    data_tour_review = check_match_round_api(league, season, round)

    date_main = ''
    fixture_main = ''
    for find_mathes in range(len(data_tour_review['response'])):
        if data_tour_review['response'][find_mathes]['fixture']['status']['long'] != 'Match Postponed':
            date = data_tour_review['response'][find_mathes]['fixture']['date']
            fixture = data_tour_review['response'][find_mathes]['fixture']['id']
            date = datetime.datetime.strptime(date[:15], '%Y-%m-%dT%H:%M')
            if date_main != '':
                if date > date_main:
                    date_main = date
                    fixture_main = fixture
                elif date < date_main:
                    pass
                else:
                    pass
            elif date_main == '':
                fixture_main = fixture
                date_main = date
    return date_main


def check_all_rounds(league_id, season):

    url = os.getenv('RAPID_API_BASE_URL')+"/fixtures/rounds"

    querystring = {"league":f"{league_id}","season":f"{season}"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
    }
    lst = []
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    for i in range(len(data['response'])):
        result = data['response'][i]
        if 'Regular Season - ' in result:lst.append(str(result).replace("Regular Season - ", ""))
        elif 'Group Stage - ' in result:lst.append(result).replace("Group Stage - ", "")
    return lst

