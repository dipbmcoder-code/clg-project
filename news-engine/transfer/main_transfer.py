import os
import sys
import unicodedata
from datetime import date
from dotenv import load_dotenv

# --- Setup environment ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()

# --- Imports ---
from publication.app_test import main_publication2
from publication.cms_db import (
    get_websites,
    check_enable_for,
    filter_websites_by_enable,
    get_websites_countries
)
from transfer.insert_transfer_api import (
    current_db_transfer,
    insert_transfer_in_db,
    update_transfer_post_in_db
)
from transfer.image_transfer_api import generate_transfer_image
from publication.save_img_aws import save_aws, delete_img
from publication.utils import check_data_exists_in_db, check_is_posted, check_api_quota, send_quota_alert_email
from publication.data_scrap import scrap_current_date_data
from publication.cms_logs import insert_news_log
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker

print("🕓 Cron job started for: transfers")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'transfer'
websites = get_websites()
current_date = date.today()

if check_enable_for(websites, types):
    # Load data
    current_date_db_transfers = current_db_transfer()
    print("current db transfer", current_date_db_transfers)
    enabled_websites = filter_websites_by_enable(websites, types)
    countries = get_websites_countries(enabled_websites, types)
    country_names = {
        unicodedata.normalize("NFKD", c[key]).encode("ascii", "ignore").decode().lower()
        for c in countries
        for key in ("shortName", "name")
        if c.get(key)
    }

    # Scrape latest transfer data
    current_date_transfers = scrap_current_date_data(types, current_date_db_transfers, country_names)

    for transfer in current_date_transfers:
        player = transfer.get("player")
        if not player:
            continue

        player_id = int(player["id"])
        player_name = player.get("name", "Unknown Player")
        player_nationalities = [
            n.strip().lower()
            for n in (player.get("nationality") or "").split(",")
            if n.strip()
        ]

        message_tracker.add_message(
            types,
            message_tracker.MessageStage.RECORD_INSERTION,
            message_tracker.MessageStatus.SUCCESS,
            f"Perform logs for player - {player_name}"
        )
        
        # Insert new record if not present
        if not check_data_exists_in_db(current_date_db_transfers, player_id, 'player_id'):
            db_record = insert_transfer_in_db(transfer)
            if not db_record:
                print(f"⚠️ Failed to insert transfer of player: {player_id}")
                continue
            current_date_db_transfers.append(db_record)

        transfers_by_id = {d['player_id']: d for d in current_date_db_transfers}
        db_transfer = transfers_by_id.get(player_id)

        # Process for each enabled website
        website_ids = []
        website_country_codes = []
        for website in enabled_websites:
            website_country_codes = [
                unicodedata.normalize("NFKD", c[key]).encode("ascii", "ignore").decode().lower()
                for c in (website.get("transfer_rumour_countries") or [])
                for key in ("shortName", "name")
                if c.get(key)
            ]

            if not website_country_codes:
                continue
            
            if not set(player_nationalities) & set(website_country_codes):
                continue

            website_ids.append(website["documentId"])

            if check_is_posted(db_transfer, website["documentId"]):
                continue

            l_version = website.get('l_version') or 'eng'
            key = f"{player_id}_{website['documentId']}_{current_date}"
            title = ""
            workflow_success = False

            try:

                # Generate transfer image
                generate_transfer_image(transfer, key, l_version, types, website)

                # Upload to AWS
                save_aws(key, l_version, types)

                # Publish news
                published = main_publication2(transfer, types, key, website)
                if not published:
                    website_ids.pop()
                else:
                    title = published.get("title")
                    workflow_success = True
            except Exception as e:
                print(f"❌ Error in transfer workflow: {e}")
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.PUBLICATION,
                    message_tracker.MessageStatus.ERROR,
                    f"Workflow error: {str(e)}"
                )
            finally:
                # Cleanup local image
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
        
        # Update transfer post status for all processed websites
        if website_ids:
            update_transfer_post_in_db(player_id, website_ids)

        # Clear messages for this key
        message_tracker.clear_messages(types)
print("cron job finished")