import os
import sys
from dotenv import load_dotenv
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()
from publication.cms_db import get_websites, check_enable_for, filter_websites_by_enable, get_websites_leagues, get_unique_field
from publication.save_img_aws import delete_img, save_aws
from player_abroad.insert_player_abroad_api import get_current_completed_fixtures, insert_player_abroad_api, current_db_abroad_players, check_data_exists_in_db, insert_db_player_abroad, check_is_posted, update_player_abroad_post_in_db
from datetime import date
from player_abroad.image_player_abroad_api import generate_player_abroad_image
from publication.app_test import main_publication2
from publication.cms_logs import insert_news_log
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker
from publication.utils import check_api_quota, send_quota_alert_email

print("🕓 Cron job started for: player_abroad")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'player_abroad'
websites = get_websites()
current_date = date.today()
if check_enable_for(websites, types):    
    fixtures = get_current_completed_fixtures()
    if len(fixtures) > 0:
        filter_websites = filter_websites_by_enable(websites, types)
        league_ids = get_websites_leagues(filter_websites)
        countries = get_unique_field(filter_websites, 'player_abroad_countries')
        abroad_players = insert_player_abroad_api(fixtures,league_ids, types, countries)
        if len(abroad_players) > 0:
            player_abroad_db_data = current_db_abroad_players()
            for player in abroad_players:
                player_id = player['playerId']
                player_name = player.get('playerName', 'Unknown Player')
                fixture_id = player['fixtureId']
                event_type = player['eventType']
                event_detail = player["eventDetail"].replace(" ", "_")
                key = f"{fixture_id}_{player_id}_{event_type}_{event_detail}"
                
                # Add initial log message
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.RECORD_INSERTION,
                    message_tracker.MessageStatus.SUCCESS,
                    f"Log perform for player - {player_name}"
                )
                
                if check_data_exists_in_db(player, player_abroad_db_data) == False:
                    db_record = insert_db_player_abroad(player)
                    if db_record:
                        player_abroad_db_data.append(db_record)
                    else:
                        print(f"Failed to insert transfer of player: {player['player_id']}")
                        continue
                website_ids = []
                for website in filter_websites:
                    website_ids.append(website["documentId"])
                    if check_is_posted(player, player_abroad_db_data, website['documentId']) == False:
                        l_version = website.get('l_version') if website.get('l_version') else 'eng'
                        title = ""
                        workflow_success = False
                        try:
                           
                            # Generate image
                            generate_player_abroad_image(player, l_version, types, key, website)

                            # Saving image into aws
                            save_aws(key, l_version, types)

                            # publish news
                            published = main_publication2(player, types, key, website)
                            if not published:
                                website_ids.pop()
                            else:
                                title = published.get("title", "")
                                workflow_success = True
                        except Exception as e:
                            print(f"❌ Error in player_abroad workflow: {e}")
                            message_tracker.add_message(
                                types,
                                message_tracker.MessageStage.PUBLICATION,
                                message_tracker.MessageStatus.ERROR,
                                f"Workflow error: {str(e)}"
                            )
                        finally:
                            # delete image
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
                        
                # update player post
                if len(website_ids) > 0:
                    update_player_abroad_post_in_db(player, website_ids)

                # Clear messages for this key
                message_tracker.clear_messages(types)
print("cron job finished")
    