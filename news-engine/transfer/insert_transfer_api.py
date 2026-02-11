from publication.db import get_data, insert_db, get_data_one
from datetime import datetime, date, timedelta
from publication.utils import sql_value
import json

current_date = date.today()
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def insert_transfer_in_db(transfer):
    if transfer and 'player' in transfer:

        # Map dict -> DB fields
        mapped = {
            "player_id": int(transfer["player"]["id"]) if transfer["player"].get("id") else None,
            "player_name": transfer["player"].get("name"),
            "profile_url": transfer["player"].get("url"),
            "position": transfer["player"].get("position"),
            "age": transfer["player"].get("age"),
            "nationality": transfer["player"].get("nationality"),
            "current_club": transfer["player"].get("current_club"),
            "date_of_birth_text": transfer["player"].get("date_of_birth_text"),
            "date_of_birth": (
                datetime.strptime(transfer["player"]["date_of_birth"], "%d %b %Y").date()
                if transfer["player"].get("date_of_birth") else None
            ),
            "calculated_age": transfer["player"].get("calculated_age"),
            "place_of_birth": transfer["player"].get("place_of_birth"),
            "height": transfer["player"].get("height"),
            "nationalities": transfer["player"].get("nationalities"),
            "main_position": transfer["player"].get("main_position"),
            "preferred_foot": transfer["player"].get("preferred_foot"),
            "national_team": transfer["player"].get("national_team"),
            "date_of_joined": (
                datetime.strptime(transfer["player"]["date_of_joined"], "%d %b %Y").date()
                if transfer["player"].get("date_of_joined") else None
            ),
            "social_media": json.dumps(transfer["player"].get("social_media")) if transfer["player"].get("social_media") else None,
            "market_value": transfer["player"].get("market_value"),
            "last_update_mv": (
                datetime.strptime(transfer["player"]["last_update_mv"], "%d %b %Y").date()
                if transfer["player"].get("last_update_mv") else None
            ),
            "contract_expires": (
                datetime.strptime(transfer["player"]["contract_expires"], "%d %b %Y").date()
                if transfer["player"].get("contract_expires") else None
            ),
            "transfer_history": json.dumps(transfer["transfer_history"]) if transfer.get("transfer_history") else None,
            "mv_history": json.dumps(transfer["market_value_history"]) if transfer.get("market_value_history") else None,
            "current_transfer": json.dumps(transfer["transfer"]) if transfer.get("transfer") else None,
            "scraped_timestamp": (
                datetime.fromisoformat(transfer["metadata"]["scraped_timestamp"])
                if transfer["metadata"].get("scraped_timestamp") else None
            ),
        }

        # Keep only fields that are not None
        filtered = {k: v for k, v in mapped.items() if v is not None}

        # Build dynamic SQL string directly
        columns = ", ".join(filtered.keys())
        values = ", ".join([sql_value(v) for v in filtered.values()])

        insert_query = (
            f"INSERT INTO transfers ({columns}) "
            f"VALUES ({values}) ;"
        )
        insert_db(insert_query, 'transfer')

        db_query = (
                f"SELECT player_id, is_posted, website_ids, current_transfer FROM transfers WHERE player_id={transfer["player"]["id"]} AND DATE(scraped_timestamp)='{current_date}';"
            )
        db_transfer = get_data_one(db_query)
        return db_transfer
    else:
        print("Didn't get transfer data")
        return

def current_db_transfer():
    db_query = (
        f"SELECT player_id, is_posted, website_ids, current_transfer FROM transfers WHERE DATE(scraped_timestamp)='{current_date}' or DATE(scraped_timestamp)='{yesterday_date}';"
    )
    transfers = get_data(db_query)
    if transfers:
        return transfers
    else: return []
    
def update_transfer_post_in_db(id, websiteIds):
    website_ids = f"'{json.dumps(websiteIds)}'::jsonb"
    update_query = (
        f"UPDATE transfers "
        f"SET is_posted = TRUE, "
        f"posted_datetime = NOW(), "
        f"website_ids = {website_ids} "
        f"WHERE player_id = {id} "
        f"AND (DATE(scraped_timestamp)='{current_date}' OR DATE(scraped_timestamp)='{yesterday_date}') ;"
    )
    insert_db(update_query)

