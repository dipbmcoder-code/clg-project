import os
import sys
from dotenv import load_dotenv
import requests
from datetime import date, datetime
import json
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
from publication.db import get_data, insert_db, get_data_one
from publication.utils import sql_value
from publication.rapidapi import get_player_profile_info, get_player_info_with_statistics, get_player_transfers, get_player_trophies

current_date = date.today()

def insert_player_profiles_api(player_ids):
    player_data = []
    filename = f'{root_folder}/result/json/player_profiles_{current_date}.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
        return player_data
    for player_id in player_ids:
        profile_info = get_player_profile_info(player_id)
        player_statistics = get_player_info_with_statistics(player_id)
        player_transfers = get_player_transfers(player_id)
        player_trophies = get_player_trophies(player_id)
        player_data.append({
            **profile_info,
            'player_id': player_id,
            **(player_statistics.get('player', {}) if player_statistics else {}),
            'statistics': player_statistics.get('statistics', []) if player_statistics else [],
            'last_updated_transfer': player_transfers.get('update') if player_transfers else None,
            'transfers': player_transfers.get('transfers', []) if player_transfers else [],
            'trophies': player_trophies if player_trophies else []
        })
    
    if len(player_data) > 0:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(player_data, f, indent=2, ensure_ascii=False)
    return player_data

def current_db_player_profiles():
    db_query = (
        f"SELECT id, player_id, is_posted, website_ids FROM player_profiles WHERE DATE(create_datetime)='{current_date}';"
    )
    player_profiles = get_data(db_query)
    if player_profiles:
        return player_profiles
    else: return []

def check_data_exists_in_db(player, db_player_abroads):
    return any(pa['player_id'] == player['id'] for pa in db_player_abroads)

def insert_db_player_profile(data):
    mapped = {
        "player_id": int(data.get("player_id")),
        "name": data.get("name"),
        "firstname": data.get("firstname"),
        "lastname": data.get("lastname"),
        "age": data.get("age"),
        "birth_date": data.get("birth", {}).get("date"),
        "birth_place": data.get("birth", {}).get("place"),
        "birth_country": data.get("birth", {}).get("country"),
        "nationality": data.get("nationality"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "number": data.get("number"),
        "position": data.get("position"),
        "photo": data.get("photo"),
        "injured": data.get("injured"),

        # Store nested data as JSONB strings
        "statistics": json.dumps(data.get("statistics", [])),
        "transfers": json.dumps(data.get("transfers", [])),
        "trophies": json.dumps(data.get("trophies", [])),

        # Extra fields
        "last_updated_transfer": data.get("last_updated_transfer"),
        #"website_ids": json.dumps(data.get("website_ids", [])),  # keep as JSON if list

        # Post status
        "create_datetime": datetime.utcnow()
    }

    # Keep only fields that are not None
    filtered = {k: v for k, v in mapped.items() if v is not None}

    # Build dynamic SQL string directly
    columns = ", ".join(filtered.keys())
    values = ", ".join([sql_value(v) for v in filtered.values()])

    insert_query = (
        f"INSERT INTO player_profiles ({columns}) "
        f"VALUES ({values});"
    )
    insert_db(insert_query)

    db_query = (
        f"SELECT id, player_id, is_posted, website_ids "
        f"FROM player_profiles "
        f"WHERE player_id={mapped['player_id']} "
        f"AND DATE(create_datetime)='{current_date}' ;"
    )
    db_player_abroad = get_data_one(db_query)
    return db_player_abroad

def check_is_posted(player, db_player_abroads, website_id):
    return any(pa['player_id'] == player['id'] and pa['is_posted'] == True and website_id in pa['website_ids'] for pa in db_player_abroads)

def update_player_profile_post_in_db(player, websiteIds):
    website_ids = f"'{json.dumps(websiteIds)}'::jsonb"
    update_query = (
        f"UPDATE player_profiles "
        f"SET is_posted = TRUE, "
        f"posted_datetime = NOW(), "
        f"website_ids = {website_ids} "
        f"WHERE player_id = {int(player['id'])} "
        f"AND DATE(create_datetime)='{current_date}' ;"
    )
    insert_db(update_query)
