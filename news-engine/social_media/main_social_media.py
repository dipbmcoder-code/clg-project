"""
Social Media Module - X API Integration
Fetches tweets from X API and publishes to websites with proper error handling and logging
"""
import os
import sys
from dotenv import load_dotenv

# --- Setup environment ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()

from publication.app_test import main_publication2
from publication.cms_db import (
    get_websites, 
    check_enable_for,
    filter_websites_by_enable,
    get_unique_field
)
from social_media.insert_social_media_api import (
    current_db_social_media_posts, 
    insert_social_media_post,
)
from social_media.image_social_media_api import generate_tweet_image

from publication.utils import (
    check_data_exists_in_db, 
    check_is_posted, 
    check_api_quota, 
    send_quota_alert_email,
    update_post_in_db
)
from publication.save_img_aws import (
    delete_img,
    save_aws
)
from social_media.twitter_api import fetch_twitter_data
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker
from publication.cms_logs import insert_news_log

print("🕓 Cron job started for: social_media (X API)")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'social_media'
websites = get_websites()

if check_enable_for(websites, types):
    # Load data
    filter_websites = filter_websites_by_enable(websites, types)
    unique_handles = get_unique_field(websites, "twitter_handles")
    
    print(f"📋 Fetching tweets for {len(unique_handles)} Twitter handles: {unique_handles}")
    
    # Fetch tweets from X API
    try:
        scraped_posts = fetch_twitter_data(unique_handles)
        print(f"✅ Fetched {len(scraped_posts)} tweets from X API")
    except Exception as e:
        print(f"❌ Error fetching tweets from X API: {e}")
        scraped_posts = []
    
    current_db_posts = current_db_social_media_posts()
    
    for post in scraped_posts:
        handler = post.get('handler')
        twitter_id = post.get('twitter_id')
        tweet_text = post.get('tweet_text', 'No text')
        
        if not twitter_id:
            print(f"⚠️ Skipping post without Twitter ID from @{handler}")
            continue
        
        # Add initial log message
        message_tracker.add_message(
            types,
            message_tracker.MessageStage.RECORD_INSERTION,
            message_tracker.MessageStatus.SUCCESS,
            f"Log perform for tweet from @{handler} - {twitter_id}"
        )
        
        # Insert new record if not present
        db_post = None
        if not check_data_exists_in_db(current_db_posts, twitter_id, 'twitter_id'):
            db_post = insert_social_media_post(post, types)
            if not db_post:
                print(f"⚠️ Failed to insert post from @{handler}: {twitter_id}")
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.RECORD_INSERTION,
                    message_tracker.MessageStatus.ERROR,
                    f"Failed to insert tweet {twitter_id} into database"
                )
                continue
            current_db_posts.append(db_post)
            print(f"✅ Inserted new post from @{handler}: {twitter_id}")
        else:
            # Find existing post
            db_post = next((p for p in current_db_posts if p.get('twitter_id') == twitter_id), None)
            if not db_post:
                print(f"⚠️ Post exists but couldn't be retrieved: {twitter_id}")
                continue
        
        # Process for each enabled website
        website_ids = []
        db_id = db_post.get("id")
        
        for website in filter_websites:
            website_ids.append(website["documentId"])
            
            # Skip if already posted
            if check_is_posted(db_post, website["documentId"]):
                print(f"ℹ️ Tweet {twitter_id} already posted to {website.get('platform_name', 'Unknown')}")
                continue
            
            # --- Posting Workflow ---
            l_version = website.get('l_version') or 'eng'
            key = f"{twitter_id}_{website['documentId']}_{db_id}"
            title = ""
            workflow_success = False
            
            try:
                generate_tweet_image(post, key, l_version, types, website=website)
                save_aws(key, l_version, types)
                # Publish the content
                published = main_publication2(
                    data=post, 
                    types=types, 
                    key=key, 
                    website=website
                )
                
                if not published:
                    website_ids.pop()
                    message_tracker.add_message(
                        types,
                        message_tracker.MessageStage.PUBLICATION,
                        message_tracker.MessageStatus.ERROR,
                        f"Publication failed for website {website.get('platform_name', 'Unknown')}"
                    )
                else:
                    title = published.get('title', f"Tweet from @{handler}")
                    workflow_success = True
                    print(f"✅ Published tweet {twitter_id} to {website.get('platform_name', 'Unknown')}")
                    
            except Exception as e:
                print(f"❌ Error during publication workflow for {website.get('platform_name', 'Unknown')}: {e}")
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.PUBLICATION,
                    message_tracker.MessageStatus.ERROR,
                    f"Workflow error: {str(e)}"
                )
                if website["documentId"] in website_ids:
                    website_ids.remove(website["documentId"])
                    
            finally:
                delete_img(key, l_version, types)
                
                # Get message tracking data
                messages_json = message_tracker.get_messages_json(types)
                overall_status = message_tracker.get_overall_status(types)
                image_generated = message_tracker.was_image_generated(types)
                
                # Insert log entry
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
                
                # Clear messages for this website
                message_tracker.clear_messages(types)
        
        # Update DB with posted websites
        if website_ids:
            update_post_in_db(db_id, 'social_media_posts', website_ids)
        
        # Clear messages for this post
        message_tracker.clear_messages(types)
    
    print("✅ Social media cron job finished (X API)")
else:
    print("ℹ️ Social media module not enabled for any websites")

print("cron job finished")
