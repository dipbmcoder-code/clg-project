import os
from dotenv import load_dotenv
import requests
from datetime import date, datetime

current_date = date.today()
headers = {
    "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
    "X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
}

def get_rapidapi_url(endpoint):
    baseUrl = os.getenv('RAPID_API_BASE_URL')
    if baseUrl:
        return f"{os.getenv('RAPID_API_BASE_URL').rstrip('/')}/{endpoint.lstrip('/')}"
    raise KeyError(f"Failed to get rapidapi base url")

def rapidapi_get_request(endpoint, params):
    url = get_rapidapi_url(endpoint)
    req_check = requests.get(url, headers=headers, params=params)
    return req_check.json()

def get_player_profile_info(player_id):
    if not player_id:
        return {}
    try:
        params = {
            'player':{player_id}
        }
        data = rapidapi_get_request('players/profiles', params)
        if 'response' in data:
            for res in data['response']:
                if 'player' in res:
                    return res['player']
                else:
                    return {}
        else:
            return {}
    except Exception as e:
        print(f"Error in getting player profile info: {e}")
        return {}

def get_player_info_with_statistics(player_id, season = current_date.year):
    if not player_id:
        return {}
    try:
        params = {
            'season': season,
            'id': player_id
        }
        data = rapidapi_get_request('players', params)
        if 'response' in data:
            for res in data['response']:
                return res
        else:
            return {}

    except Exception as e:
        print(f"Error in getting player statistics: {e}")
        return []

def get_player_transfers(player_id):
    if not player_id:
        return []
    try:
        params = {
            'player': player_id
        }
        data = rapidapi_get_request('transfers', params)
        if 'response' in data:
            for res in data['response']:
                return res
        else:
            return []

    except Exception as e:
        print(f"Error in getting player statistics: {e}")
        return []

def get_player_trophies(player_id):
    if not player_id:
        return []
    try:
        params = {
            'player': player_id
        }
        data = rapidapi_get_request('trophies', params)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting player statistics: {e}")
        return []

def get_completed_fixtures(completed_date):
    if not completed_date:
        completed_date = current_date
    try:
        params = {
            'date':{completed_date},
            'status': 'FT'
        }
        data = rapidapi_get_request('fixtures', params)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting completed fixtures: {e}")
        return []

def get_fixture_events(fixture):
    if not fixture:
        return []
    try:
        params = {
            'fixture': fixture
        }
        data = rapidapi_get_request('fixtures/events', params)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting fixture events: {e}")
        return []

def get_fixtures_by_league(league_id, season = current_date.year, match_date = None):
    if not league_id:
        return []
    try:
        params = {
            "league": league_id,
            "season": str(season),
        }
        if match_date:
            params['date'] = match_date
        data = rapidapi_get_request('fixtures', params)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting fixtures: {e}")
        return []

def get_fixture_by_id(fixture):
    if not fixture:
        return {}
    try:
        params = {
            'id':{fixture}
        }
        data = rapidapi_get_request('fixtures', params)
        if 'response' in data:
            for res in data['response']:
                return res
        else:
            return {}
    except Exception as e:
        print(f"Error in getting fixture details: {e}")
        return {}

def get_league_by_id(league_id):
    if not league_id:
        return {}
    try:
        params = {
            'id':{league_id}
        }
        data = rapidapi_get_request('leagues', params)
        if 'response' in data:
            for res in data['response']:
                return res
        else:
            return {}
    except Exception as e:
        print(f"Error in getting league details: {e}")
        return {}

def get_leagues_by_season(season=current_date.year):
    try:
        params = {
            "season": str(season),
        }
        data = rapidapi_get_request('leagues', params)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting league by season: {e}")
        return []
    
def get_leagues():
    try:
        data = rapidapi_get_request('leagues', None)
        if 'response' in data:
            return data['response']
        else:
            return []

    except Exception as e:
        print(f"Error in getting fixtures: {e}")
        return []