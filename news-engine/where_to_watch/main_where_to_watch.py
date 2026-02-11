import os
import sys
import unicodedata
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- Setup Paths & Env ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()

# --- Imports ---
from publication.app_test import main_publication2
from publication.cms_db import (
    get_websites, check_enable_for,
    filter_websites_by_enable, filter_websites_by_leagues
)
from where_to_watch.insert_where_to_watch import (
    get_current_season_leagues, insert_where_to_watch_in_db, get_current_date_db_where_to_watch, data_exists_in_db
)
from where_to_watch.image_where_to_watch import generate_where_to_watch_image
from publication.save_img_aws import save_aws, delete_img
from publication.data_scrap import scrap_current_date_data
from publication.utils import check_is_posted, update_post_in_db, check_api_quota, send_quota_alert_email
import publication.message_tracker as message_tracker
from publication.cms_logs import insert_news_log


print("🕓 Cron job started for: where_to_watch")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = "where_to_watch"
websites = get_websites()

if check_enable_for(websites, types):
    websites = filter_websites_by_enable(websites, types)
    current_date = datetime.now()

    # Precompute future publish dates per website & league
    new_dates = {
        (
            league["id"],
            new_date.strftime("%Y-%m-%d"),   # full date
            new_date.year                    # extracted year
        )
        for website in websites if website.get("website_leagues")
        for league in website["website_leagues"]
        for new_date in [
            current_date + timedelta(days=int(website.get("where_to_watch_days") or 0))
        ]
    }

    # Get leagues and DB data
    current_season_leagues = get_current_season_leagues(new_dates)
    db_where_to_watch = get_current_date_db_where_to_watch()

    # Scrape new data
    scraped_data = scrap_current_date_data(types, db_where_to_watch, [], current_season_leagues)

    for record in scraped_data:
        if not record or "league" not in record:
            continue

        league_id = int(record["league"]["id"])
        league_name = record["league"]["name"]
        season_year = int(record["seasons"][0]["year"])

        message_tracker.add_message(
            types,
            message_tracker.MessageStage.RECORD_INSERTION,
            message_tracker.MessageStatus.SUCCESS,
            f"Perform logs for league - {league_name}"
        )

        # Insert new record if not present
        db_watch = data_exists_in_db(league_id, season_year, db_where_to_watch)
        if not db_watch:
            db_watch = insert_where_to_watch_in_db(record)
            if not db_watch:
                print(f"⚠️ Failed to insert where to watch of league: {league_id}")
                continue
            db_where_to_watch.append(db_watch)

        # Get all websites that cover this league
        league_websites = filter_websites_by_leagues(websites, league_id)
        website_ids = []

        available_codes = set(record["tv_channels"].keys())

        for website in league_websites:
            # Build normalized (country_name, code3) list
            website_country_codes = []
            for c in website.get("where_to_watch_countries") or []:
                code3 = c.get("code3")
                if not code3:
                    continue

                name = unicodedata.normalize("NFKD", c["shortName"])
                name = name.encode("ascii", "ignore").decode("utf-8").lower()

                website_country_codes.append((name, code3))


            # Skip if no country codes
            if not website_country_codes:
                continue

            # Extract the required codes
            required_codes = {code for _, code in website_country_codes}

            # If there is no overlap → skip
            if available_codes.isdisjoint(required_codes):
                continue


            # Build filtered tv_channels list safely
            filtered_channels = []
            for country_name, code3 in website_country_codes:
                channels = record["tv_channels"].get(code3)
                if channels:  # only if it exists AND not empty
                    filtered_channels.append({
                        "channels": channels,
                        "country": country_name
                    })

            record["tv_channels"] = filtered_channels

            days_offset = int(website.get("where_to_watch_days") or 0)
            target_date = (current_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")

            # Skip if league start date is later than target date
            if record["seasons"][0]["start"] > target_date:
                continue

            website_ids.append(website["documentId"])

            # Skip if already posted
            if check_is_posted(db_watch, website["documentId"]):
                continue

            # --- Posting Workflow ---
            l_version = website.get('l_version') if website.get('l_version') else 'eng'
            post_id = f"{league_id}_{season_year}_{website['documentId']}"
            title = ""
            try:

                generate_where_to_watch_image(record, post_id, l_version, types, website=website)
                save_aws(post_id, l_version, types)
                published = main_publication2(record, types, post_id, website)
                if not published:
                    website_ids.pop()
                else:
                    title = published["title"]
            finally:
                delete_img(post_id, l_version, types)

                messages_json = message_tracker.get_messages_json(types)
                overall_status = message_tracker.get_overall_status(types)
                image_generated = message_tracker.was_image_generated(types)

                insert_news_log(
                    news_type=types,
                    news_title=f"{title}",
                    website_name=website.get('platform_name', 'Unknown Website'),
                    image_generated=image_generated,
                    news_status=overall_status,
                    message=messages_json
                )

                # Clear messages for this key
                message_tracker.clear_messages(types)

        # Update DB with posted websites
        if website_ids:
            update_post_in_db(db_watch["id"], 'where_to_watch', website_ids)

        # Clear messages for this key
        message_tracker.clear_messages(types)
print("cron job finished")