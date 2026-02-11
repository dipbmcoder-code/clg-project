from datetime import date
from publication.rapidapi import get_leagues
from publication.utils import parse_date
from publication.db import insert_db, get_data_one, get_data
from publication.utils import sql_value
import json


current_date = date.today()

def get_current_season_leagues(leagues):
    # Extract all season years from the input "leagues"
    seasons = {s[2] for s in leagues if len(s) > 2}

    # Fetch all league metadata
    current_season_leagues = get_leagues()

    # Preprocess: convert start/end date objects once + index seasons by year
    leagues_by_id = {}

    for league_info in current_season_leagues:
        season_map = {}

        for s in league_info["seasons"]:
            # Only process relevant seasons
            if s["year"] in seasons:
                start = s["start"]
                end = s["end"]

                # Normalize to "YYYY-MM-DD"
                if isinstance(start, date):
                    start = start.strftime("%Y-%m-%d")
                if isinstance(end, date):
                    end = end.strftime("%Y-%m-%d")

                # Save normalized data
                season_map[s["year"]] = {
                    "start": start,
                    "end": end,
                    "year": s["year"]
                }

        league_info["_season_map"] = season_map
        leagues_by_id[league_info["league"]["id"]] = league_info

    # Final selection
    results = []

    for league_id, publish_date, season_year in leagues:
        league_info = leagues_by_id.get(league_id)
        if not league_info:
            continue

        # Ensure publish_date is a parsed date
        publish_dt = parse_date(publish_date)
        if not publish_dt:
            continue

        # Fetch matching season
        season = league_info["_season_map"].get(season_year)
        if not season:
            continue

        start_dt = parse_date(season["start"])
        end_dt = parse_date(season["end"])

        # Filter by season window
        if start_dt <= publish_dt <= end_dt and end_dt >= current_date:
            results.append(league_info)

    return results

def get_current_date_db_where_to_watch():
    db_query = (
        f"SELECT id, league_id, season_year, is_posted, website_ids FROM where_to_watch;"
    )
    where_to_watch = get_data(db_query)
    if where_to_watch:
        return where_to_watch
    else: return []

def insert_where_to_watch_in_db(league_data):
    if not league_data:
        print("No match preview data to insert")
        return

    # Map incoming dict -> DB fields
    mapped = {
        "league_id": league_data["league"]["id"],
        "league_name": league_data["league"]["name"],

        "country_name": league_data["country"]["name"],
        "country_code": league_data["country"]["code"],

        "season_year": league_data["seasons"][0]["year"] if league_data.get("seasons") else None,
        "season_start": league_data["seasons"][0]["start"] if league_data.get("seasons") else None,
        "season_end": league_data["seasons"][0]["end"] if league_data.get("seasons") else None,
        "season_current": league_data["seasons"][0]["current"] if league_data.get("seasons") else False,

        "tv_channels": json.dumps(league_data.get("tv_channels")) if league_data.get("tv_channels") else None,
        "scrap_date": league_data.get("scrap_date", date.today().isoformat())
    }

    # Remove None values to insert only available fields
    filtered = {k: v for k, v in mapped.items() if v is not None}

    # Build dynamic SQL string
    columns = ", ".join(filtered.keys())
    values = ", ".join([sql_value(v) for v in filtered.values()])

    insert_query = (
        f"INSERT INTO where_to_watch ({columns}) "
        f"VALUES ({values});"
    )

    # Execute the insert
    insert_db(insert_query, 'where_to_watch')

    # Optional: fetch the newly inserted record
    db_query = f"""
        SELECT id, league_id, season_year, is_posted, website_ids 
        FROM where_to_watch 
        WHERE league_id={league_data['league']['id']} 
        AND season_year={league_data['seasons'][0]['year']};
    """
    return get_data_one(db_query)

def data_exists_in_db(league_id, season_year, db_data):
    return next((d for d in db_data if d['league_id'] == int(league_id) and d['season_year'] == int(season_year)), None)
