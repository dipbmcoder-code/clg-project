from publication.db import get_data, insert_db, get_data_one
from datetime import datetime, date, timedelta
from publication.utils import sql_value
import json

current_date = date.today()
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def insert_rumour_in_db(rumour):
    if rumour and 'player' in rumour:

        # Map dict -> DB fields
        mapped = {
            "player_id": int(rumour["player"]["id"]) if rumour["player"].get("id") else None,
            "player_name": rumour["player"].get("name"),
            "profile_url": rumour["player"].get("url"),
            "position": rumour["player"].get("position"),
            "age": rumour["player"].get("age"),
            "nationality": rumour["player"].get("nationality"),
            "current_club": rumour["player"].get("current_club"),
            "date_of_birth_text": rumour["player"].get("date_of_birth_text"),
            "date_of_birth": (
                datetime.strptime(rumour["player"]["date_of_birth"], "%d %b %Y").date()
                if rumour["player"].get("date_of_birth") else None
            ),
            "calculated_age": rumour["player"].get("calculated_age"),
            "place_of_birth": rumour["player"].get("place_of_birth"),
            "height": rumour["player"].get("height"),
            "nationalities": rumour["player"].get("nationalities"),
            "main_position": rumour["player"].get("main_position"),
            "preferred_foot": rumour["player"].get("preferred_foot"),
            "national_team": rumour["player"].get("national_team"),
            "date_of_joined": (
                datetime.strptime(rumour["player"]["date_of_joined"], "%d %b %Y").date()
                if rumour["player"].get("date_of_joined") else None
            ),
            "social_media": json.dumps(rumour["player"].get("social_media")) if rumour["player"].get("social_media") else None,
            "market_value": rumour["player"].get("market_value"),
            "last_update_mv": (
                datetime.strptime(rumour["player"]["last_update_mv"], "%d %b %Y").date()
                if rumour["player"].get("last_update_mv") else None
            ),
            "contract_expires": (
                datetime.strptime(rumour["player"]["contract_expires"], "%d %b %Y").date()
                if rumour["player"].get("contract_expires") else None
            ),
            "transfer_history": json.dumps(rumour["transfer_history"]) if rumour.get("transfer_history") else None,
            "mv_history": json.dumps(rumour["market_value_history"]) if rumour.get("market_value_history") else None,
            "current_rumour": json.dumps(rumour["rumour"]) if rumour.get("rumour") else None,
            "scraped_timestamp": (
                datetime.fromisoformat(rumour["metadata"]["scraped_timestamp"])
                if rumour["metadata"].get("scraped_timestamp") else None
            ),
            "last_reply_time": datetime.strptime(rumour["rumour"]['last_reply_text'], "%d.%m.%Y - %H:%M") if rumour["rumour"]['last_reply_text'] else None
        }

        # Keep only fields that are not None
        filtered = {k: v for k, v in mapped.items() if v is not None}

        # Build dynamic SQL string directly
        columns = ", ".join(filtered.keys())
        values = ", ".join([sql_value(v) for v in filtered.values()])

        insert_query = (
            f"INSERT INTO rumours ({columns}) "
            f"VALUES ({values});"
        )
        insert_db(insert_query, "rumour")  # Pass key for message tracking

        db_query = (
                f"SELECT id, player_id, is_posted, website_ids, current_rumour FROM rumours WHERE player_id={rumour["player"]["id"]} AND DATE(scraped_timestamp)='{current_date}';"
            )
        db_rumours = get_data(db_query)
        print(current_date)
        print("db rumours", db_rumours)
        if not db_rumours:
            return None
        
        db_rumour = None
        for item in db_rumours:
            if (
                item['current_rumour']['from_club']['name'] == rumour["rumour"]['from_club']['name']
                and item['current_rumour']['to_club']['name'] == rumour["rumour"]['to_club']['name']
            ):
                db_rumour = item
                break
        print(db_rumour)
        return db_rumour
    else:
        print("Didn't get transfer data")
        return

def current_db_rumour():
    db_query = (
        f"SELECT id, player_id, is_posted, website_ids, current_rumour FROM rumours WHERE DATE(scraped_timestamp)='{current_date}' OR DATE(scraped_timestamp)='{yesterday_date}';"
    )
    rumours = get_data(db_query)
    if rumours:
        return rumours
    else: return []

def data_exists_in_db(data, id, rumour):
    return next((item for item in data if item['player_id'] == id and item['current_rumour']['from_club']['name'] == rumour['from_club']['name'] and item['current_rumour']['to_club']['name'] == rumour['to_club']['name']), None)

    