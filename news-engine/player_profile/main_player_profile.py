import os
import sys
from dotenv import load_dotenv
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()
from publication.app_test import main_publication2
from publication.cms_db import get_websites, check_enable_for, filter_websites_by_enable, get_websites_players, filter_website_by_datetime
from player_profile.insert_player_profile_api import insert_player_profiles_api, insert_db_player_profile, current_db_player_profiles, update_player_profile_post_in_db
from player_profile.image_player_profile_api import generate_player_profile_image
from publication.save_img_aws import save_aws, delete_img
from publication.utils import check_data_exists_in_db, check_is_posted, check_api_quota, send_quota_alert_email

print("🕓 Cron job started for: player_profile")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'player_profile'
websites = get_websites()

if check_enable_for(websites, types):
    filter_websites = filter_websites_by_enable(websites, types)
    filter_websites = filter_website_by_datetime(filter_websites, types)
    player_ids = get_websites_players(filter_websites)
    player_profiles = insert_player_profiles_api(player_ids)
    if len(player_profiles) > 0:
        current_date_db_player_profiles = current_db_player_profiles()
        for player_profile in player_profiles:
            if "id" in player_profile:
                player_id = int(player_profile['id'])
                if check_data_exists_in_db(current_date_db_player_profiles, player_id, 'player_id') == False:
                    db_record = insert_db_player_profile(player_profile)
                    if db_record:
                        current_date_db_player_profiles.append(db_record)
                    else:
                        print(f"Failed to insert player profile of player: {player_id}")
                        continue
                website_ids = []
                for website in filter_websites:
                    website_ids.append(website["documentId"])
                    if check_is_posted(current_date_db_player_profiles, player_id, 'player_id', website["documentId"]) == False:
                        l_version = website.get('l_version') if website.get('l_version') else 'eng'
                        
                        # Generate image
                        generate_player_profile_image(player_profile, l_version, types, player_id, website=website)

                        # Saving image into aws
                        save_aws(player_id, l_version, types)

                        # publish news
                        main_publication2(player_profile, types, player_id, website)

                        # delete image
                        delete_img(player_id, l_version, types)
                        
                # update player post
                update_player_profile_post_in_db(player_profile, website_ids)

print("cron job finished")