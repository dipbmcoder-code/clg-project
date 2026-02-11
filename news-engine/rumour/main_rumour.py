import os
import sys
import unicodedata
from dotenv import load_dotenv

# --- Setup environment ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()


from publication.app_test import main_publication2
from publication.cms_db import (
    get_websites, check_enable_for,
    filter_websites_by_enable,
    get_websites_countries
)
from rumour.insert_rumour_api import (
    current_db_rumour,
    insert_rumour_in_db,
    data_exists_in_db,
)
from rumour.image_rumour_api import generate_rumours_image
from publication.save_img_aws import save_aws, delete_img
from publication.data_scrap import scrap_current_date_data
from publication.utils import update_post_in_db, check_is_posted, check_api_quota, send_quota_alert_email
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker
from publication.cms_logs import insert_news_log

print("🕓 Cron job started for: rumours")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'rumour'
websites = get_websites()

if check_enable_for(websites, types):
    # Load data
    current_date_db_rumours = current_db_rumour()
    filter_websites = filter_websites_by_enable(websites, types)
    countries = get_websites_countries(filter_websites, types)

    country_names = {
        unicodedata.normalize("NFKD", c[key]).encode("ascii", "ignore").decode().lower()
        for c in countries
        for key in ("shortName", "name")
        if c.get(key)
    }

    # Scrap latest rumours
    current_date_rumours= scrap_current_date_data(types, current_date_db_rumours, country_names)
    
    for rumour in current_date_rumours:
        player = rumour.get("player")
        if not player:
            continue

        player_id = int(player["id"])
        player_name = player.get("name", "Unknown Player")
        player_nationalities = [n.strip().lower() for n in player["nationality"].split(",")]
        current_rumour = rumour['rumour']

        # Add initial log message 
        message_tracker.add_message(
            types,
            message_tracker.MessageStage.RECORD_INSERTION,
            message_tracker.MessageStatus.SUCCESS,
            f"Log perform for player - {player_name}"
        )

        # Insert new record if not present
        db_rumour = data_exists_in_db(current_date_db_rumours, player_id, current_rumour)
        if not db_rumour:
            db_rumour = insert_rumour_in_db(rumour)
            if not db_rumour:
                print(f"⚠️ Failed to insert rumour of player: {player_id}")
                continue
            current_date_db_rumours.append(db_rumour)

        # Process for each enabled website
        website_ids = []
        db_id = db_rumour["id"]
        for website in filter_websites:
            website_country_codes = {
                unicodedata.normalize("NFKD", c[key]).encode("ascii", "ignore").decode().lower()
                for c in (website.get("transfer_rumour_countries") or [])
                for key in ("shortName", "name")
                if c.get(key)
            }

            # Skip if no country names
            if not website_country_codes:
                continue
            
            if not set(player_nationalities) & website_country_codes:
                continue
            
            website_ids.append(website["documentId"])

            # Skip if already posted
            if check_is_posted(db_rumour, website["documentId"]):
                continue
            
            # --- Posting Workflow ---
            l_version = website.get('l_version') or 'eng'
            key = f"{player_id}_{website['documentId']}_{db_id}"
            title = ""
            workflow_success = False
            
            try:
                
                generate_rumours_image(rumour, key, l_version, types, website)
                save_aws(key, l_version, types)
                published = main_publication2(rumour, types, key, website)
                if not published:
                    website_ids.pop()
                else:
                    title = published.get('title')
                    workflow_success = True

            except Exception as e:
                print(f"❌ Error during publication workflow: {e}")
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.PUBLICATION,
                    message_tracker.MessageStatus.ERROR,
                    f"Workflow error: {str(e)}"
                )
            finally:
                delete_img(key, l_version, types)
                
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
                
                # Track failure/success for module deactivation
                # Failure if: overall status is Failed OR workflow had exception
                if overall_status == 'Failed' or not workflow_success:
                    module_disabled = module_failure_tracker.increment_failure(types)
                    if module_disabled:
                        print(f"🛑 Module '{types}' has been disabled. Exiting workflow...")
                        sys.exit(1)  # Exit immediately when module is disabled
                else:
                    module_failure_tracker.reset_failure(types)

                # Clear messages for this key
                message_tracker.clear_messages(types)

        # Update DB with posted websites
        if website_ids:
            update_post_in_db(db_id, 'rumours', website_ids)

        # Clear messages for this key
        message_tracker.clear_messages(types)

print("cron job finished")