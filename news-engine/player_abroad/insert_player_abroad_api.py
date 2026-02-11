import os
import sys
from dotenv import load_dotenv
import requests
import re
from datetime import date, datetime, timedelta
import json, gzip
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
from publication.db import get_data, insert_db, get_data_one
from publication.utils import sql_value
from publication.data_scrap import scrap_current_date_data
from publication.rapidapi import get_completed_fixtures, get_fixture_events, get_player_info_with_statistics, get_player_profile_info

current_date = date.today()
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_current_completed_fixtures():
    try:
        data = get_completed_fixtures(current_date)
        data2 = get_completed_fixtures(yesterday_date)
        return data2.extend(data)
    except Exception as _ex:
        print("Error in fetching fixtures")
        return []
    
def insert_player_abroad_api(fixtures, league_ids, types, countries):
    data = []
    existing_data = []
    filename = f'{root_folder}/result/json/{types}s.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

    for league_id in league_ids:
        for fixture in fixtures:
            if int(fixture['league']['id']) == int(league_id):
                fixture_id = fixture['fixture']['id']
                if any(int(ed['fixtureId']) == fixture_id for ed in existing_data):
                    continue
                try:
                    fixture_data = {
                        "fixtureId": fixture_id,
                        "date": fixture['fixture'].get('date', "") if 'fixture' in fixture else None,
                        "venue": fixture['fixture']['venue'].get('name', "") if 'venue' in fixture['fixture'] else None,
                        "city": fixture['fixture']['venue'].get('city', "") if 'venue' in fixture['fixture'] else None,
                        "leagueId": fixture['league'].get('id', 0) if 'league' in fixture else 0,
                        "league": fixture['league'].get('name', "") if 'league' in fixture else None,
                        "leagueCountry": fixture['league'].get('country', "") if 'league' in fixture else None,
                        "leagueSeason": fixture['league'].get('season', "") if 'league' in fixture else None,
                        "homeTeam": fixture.get("teams", {}).get("home", {}).get("name"),
                        "awayTeam": fixture.get("teams", {}).get("away", {}).get("name"),
                        "score": fixture.get("score", {}).get("fulltime", {})
                    }
                    
                    events = get_fixture_events(fixture_id)
                    if len(events) > 0:
                        event_data = {}
                        for event in events:
                            if event['type'] == 'Goal' or (event['type'] == 'Card' and event['detail'] == 'Red Card'):
                                player_id = event['player'].get('id', None) if 'player' in event else None
                                if not player_id:
                                    continue
                                key = f"{fixture_id}_${player_id}_${event['type']}_${event['detail']}"
                                if not key in event_data:
                                    event_data[key] = {
                                        "fixtureId": fixture_id,
                                        "playerId": player_id,
                                        "playerName": event.get('player',"").get('name'),
                                        "eventType": event['type'],
                                        "eventDetail": event['detail'],
                                        "team": event.get('team',"").get('name'),
                                        "teamId": event.get('team',"").get('id'),
                                        "minutes": [],
                                        "goalsCount": 0
                                    }

                                if event['time']['elapsed']:
                                    event_data[key]['minutes'].append(event['time']['elapsed'])
                                if event['type'] == 'Goal':
                                    event_data[key]['goalsCount'] += 1
                        for g in event_data.values():
                            data.append({
                                **fixture_data,
                                **g,
                                "minutes": ", ".join(map(str, g["minutes"])),
                            })

                except Exception as _ex:
                    print(f"[INFO] Error in player abroad api: {_ex}")
                    return []           
    
    new_data = []
    player_data={}
    if len(data) > 0:
        player_abroad_countries_data = []
        if len(countries) > 0:
            json_filename = f'{root_folder}/result/json/scrap_{types}s.json'
            country_json_data = []
            json_data = []
            if os.path.exists(json_filename):
                countries = set(c.lower() for c in countries)
                with open(json_filename, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            
            recent_countries = set()
            seven_days_ago = datetime.now() - timedelta(days=7)
            for d in json_data:
                parts = d.get("nationality", "").split(",", 1)
                if len(parts) < 2:
                    continue

                second = parts[1].strip().lower()
                if second not in countries:
                    continue

                # Check recent scrap_date (<7 days)
                sd = d.get("scrap_date")
                if sd:
                    try:
                        if datetime.strptime(sd, "%Y-%m-%d") >= seven_days_ago:
                            recent_countries.add(second)
                        else:
                            d['scrap_date'] = current_date
                    except:
                        pass
                
                country_json_data.append(d)

            countries -= recent_countries
            #player_abroad_countries_data = country_json_data
            player_abroad_countries_data = scrap_current_date_data(types, country_json_data, countries)
        for d in data:
            player_id = d['playerId']       
            if player_id:
                if not player_id in player_data:
                    pl = get_player_info_with_statistics(player_id)
                    if pl:
                        player_data[player_id] = {
                            **pl.get("player", {}),
                            "statistics": pl.get("statistics", [])
                        }
                    else:
                        pl = get_player_profile_info(player_id)
                        if pl:
                            player_data[player_id] = {
                                **pl,
                            }
                if player_id in player_data and player_data[player_id]['nationality']:
                    print(f"player id: {player_id} firstname: {player_data[player_id]['firstname']} lastname: {player_data[player_id]['lastname']} name: {player_data[player_id]['name']}")
                    match_with_scrap_abroad_player = False
                    if len(player_abroad_countries_data) > 0:
                        filter_player_data_by_nationality = [d for d in player_abroad_countries_data if len(d['nationality'].split(',')) > 0 and player_data[player_id]['nationality'].split(',')[0].lower() == d['nationality'].split(',')[0].lower()]
                        if len(filter_player_data_by_nationality) > 0:
                            first_name = player_data[player_id]['firstname']
                            last_name = player_data[player_id]['lastname']
                            if last_name:
                                #first match with whole word of first name + first word of last name
                                match_player_name = first_name.lower() + " " + last_name.split(" ")[0].lower()
                                matched_data = next((p for p in filter_player_data_by_nationality if match_player_name == p['name'].lower()), None)
                                if not matched_data:
                                    # second match with first word of first name + first word of last name
                                    match_player_name = first_name.split(" ")[0].lower() + " " + last_name.split(" ")[0].lower()
                                    matched_data = next((p for p in filter_player_data_by_nationality if match_player_name == p['name'].lower()), None)

                            if not match_with_scrap_abroad_player:
                                birth_date = player_data[player_id]['birth']['date']
                                if birth_date:
                                    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', birth_date)
                                    if date_match:
                                        day, month, year = date_match.groups()
                                        birth_date = f"{day}/{month}/{year}"
                                    # Third match with short name like M. Rollando along with birth date
                                    # match_player_name = player_data[player_id]['name'].lower()
                                    # if any(match_player_name == f"{p['name'][0].lower()}. {p['lastname'].split(' ')[0].lower()}" and birth_date == p['date_of_birth_text'] for p in filter_player_data_by_nationality):
                                    #     match_with_scrap_abroad_player = True
                                    # else: 
                                        # Fourth match with first word of first name and birth date
                                        match_player_name = first_name.split(" ")[0].lower()
                                        matched_data = next((p for p in filter_player_data_by_nationality if match_player_name == p['name'].lower() and birth_date == p['date_of_birth_text']), None)
                            if matched_data:
                                match_with_scrap_abroad_player = True
                                player_data[player_id].update(matched_data)
                    match_with_api_abroad_player = False
                    if d['leagueCountry'].lower() != 'world' and player_data[player_id]['nationality'].lower() != d['leagueCountry'].lower():
                        match_with_api_abroad_player = True
                    
                    if match_with_api_abroad_player or match_with_scrap_abroad_player:
                        statistics = {}
                        for p in player_data[player_id].get('statistics',[]):
                            if p['league']['id'] and int(p['league']['id']) == int(d['leagueId']):
                                statistics = p
                                break
                        new_data.append({
                            **d,
                            "playing_for_abroad": match_with_api_abroad_player,
                            "match_with_scrap_abroad_player": match_with_scrap_abroad_player,
                            "playerDetails": {
                                **player_data[player_id],
                                "statistics": statistics
                            }
                        })

                    

        if len(new_data) > 0:
            new_data.extend(existing_data)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
    return new_data

def current_db_abroad_players():
    db_query = (
        f"SELECT player_id, is_posted, fixture_id, event_type, event_detail, website_ids FROM player_abroads WHERE DATE(create_datetime)='{current_date}' OR DATE(create_datetime)='{yesterday_date}';"
    )
    abroad_players = get_data(db_query)
    if abroad_players:
        return abroad_players
    else: return []

def check_data_exists_in_db(player, db_player_abroads):
    return any(pa['fixture_id'] == player['fixtureId'] and pa['player_id'] == player['playerId'] and pa['event_type'] == player['eventType'] and pa['event_detail'] == player['eventDetail'] for pa in db_player_abroads)

def insert_db_player_abroad(player):
    data = player
    pd = data['playerDetails']
    mapped = {
        "fixture_id": int(data["fixtureId"]),
        "match_date": data["date"],
        "venue": data["venue"],
        "city": data["city"],
        "league_id": int(data["leagueId"]),
        "league_name": data["league"],
        "league_country": data["leagueCountry"],
        "league_season": data["leagueSeason"],
        "home_team": data["homeTeam"],
        "away_team": data["awayTeam"],
        "home_score": data["score"]["home"],
        "away_score": data["score"]["away"],
        "player_id": int(data["playerId"]),
        "player_name": data["playerName"],
        "event_type": data["eventType"],
        "event_detail": data["eventDetail"],
        "team_name": data["team"],
        "team_id": int(data["teamId"]),
        "minutes_played": data["minutes"],
        "goals_count": data["goalsCount"],
        "firstname": pd.get("firstname"),
        "lastname": pd.get("lastname"),
        "age": pd.get("age"),
        "birth_date": pd["birth"].get("date"),
        "birth_place": pd["birth"].get("place"),
        "birth_country": pd["birth"].get("country"),
        "nationality": pd.get("nationality"),
        "height": pd.get("height"),
        "weight": pd.get("weight"),
        "injured": pd.get("injured"),
        "photo": pd.get("photo"),
        "statistics": json.dumps(pd.get("statistics")),
        "is_posted": False,
        "posted_datetime": None,
        "create_datetime": datetime.utcnow()
    }

    # Keep only fields that are not None
    filtered = {k: v for k, v in mapped.items() if v is not None}

    # Build dynamic SQL string directly
    columns = ", ".join(filtered.keys())
    values = ", ".join([sql_value(v) for v in filtered.values()])

    insert_query = (
        f"INSERT INTO player_abroads ({columns}) "
        f"VALUES ({values});"
    )
    insert_db(insert_query, 'player_abroad')

    db_query = (
        f"SELECT player_id, is_posted, fixture_id, event_type, event_detail, website_ids "
        f"FROM player_abroads "
        f"WHERE player_id={mapped['player_id']} "
        f"AND fixture_id={mapped['fixture_id']} "
        f"AND event_type='{mapped['event_type']}' "
        f"AND event_detail='{mapped['event_detail']}';"
    )
    db_player_abroad = get_data_one(db_query)
    return db_player_abroad

def check_is_posted(player, db_player_abroads, website_id):
    return any(pa['fixture_id'] == player['fixtureId'] and pa['player_id'] == player['playerId'] and pa['event_type'] == player['eventType'] and pa['event_detail'] == player['eventDetail'] and pa['is_posted'] == True and website_id in pa['website_ids'] for pa in db_player_abroads)

def update_player_abroad_post_in_db(player, websiteIds):
    website_ids = f"'{json.dumps(websiteIds)}'::jsonb"
    update_query = (
        f"UPDATE player_abroads "
        f"SET is_posted = TRUE, "
        f"posted_datetime = NOW(), "
        f"website_ids = {website_ids} "
        f"WHERE player_id = {int(player['playerId'])} "
        f"AND fixture_id = {int(player['fixtureId'])} "
        f"AND event_type = '{player['eventType']}' "
        f"AND event_detail = '{player['eventDetail']}';"
    )
    insert_db(update_query)