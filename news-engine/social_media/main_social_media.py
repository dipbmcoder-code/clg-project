"""
Social Media Pipeline — AI News Generator
Fetches posts from Reddit and X, generates AI articles, publishes to WordPress.
Topic-agnostic scraping pipeline with multi-source support.
"""
import os
import sys
from dotenv import load_dotenv

# --- Setup environment ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()

import json
import requests
import psycopg2
import psycopg2.extras
from datetime import datetime, timezone
from time import sleep as api_delay

from publication.config import host, port, user, password, db_name
from publication.app_test import main_publication2
from publication.save_img_aws import save_image_locally
from publication.utils import check_data_exists_in_db, check_is_posted, update_post_in_db
from social_media.insert_social_media_api import insert_social_media_post, current_db_social_media_posts
from social_media.image_social_media_api import generate_post_image
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker

print("🕓 AI News Generator — Social Media Pipeline started")


# ── Database-based config (replaces Strapi CMS) ──

def get_websites_from_db():
    """Fetch enabled websites directly from PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=db_name)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM websites 
                WHERE active = true AND is_validated = true AND enable_social_media = true
            """)
            return [dict(w) for w in cur.fetchall()]
    except Exception as e:
        print(f"❌ Error fetching websites: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_prompts_from_db():
    """Fetch news prompts directly from PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=db_name)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM news_prompts ORDER BY id LIMIT 1")
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        print(f"❌ Error fetching prompts: {e}")
        return {}
    finally:
        if conn:
            conn.close()


def insert_log_to_db(news_type, title, website_name, image_generated, status, message):
    """Insert news log directly to PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=db_name)
        with conn.cursor() as cur:
            msg_json = json.dumps(message) if isinstance(message, (dict, list)) else message
            cur.execute(
                "INSERT INTO news_logs (news_type, title, website_name, image_generated, news_status, log_message) VALUES (%s, %s, %s, %s, %s, %s)",
                (news_type, title, website_name, image_generated, status, msg_json),
            )
            conn.commit()
    except Exception as e:
        print(f"⚠️ Log insert error: {e}")
    finally:
        if conn:
            conn.close()


# ── Main Pipeline ──

types = "social_media"
websites = get_websites_from_db()

if not websites:
    print("ℹ️ No enabled websites found. Exiting.")
    sys.exit(0)

prompts = get_prompts_from_db()
if prompts:
    prompt_keys = ['social_media_news_title_prompt', 'social_media_news_content_prompt', 'social_media_news_image_prompt']
    loaded = [k for k in prompt_keys if prompts.get(k)]
    missing = [k for k in prompt_keys if not prompts.get(k)]
    print(f"✅ Loaded {len(loaded)} custom prompts from DB: {loaded}")
    if missing:
        print(f"⚠️ Missing/empty prompts (will use defaults): {missing}")
else:
    print("⚠️ No prompts found in news_prompts table — using default prompts")

# Merge only prompt-specific keys into website dicts
# (avoid overwriting website.id, created_at, updated_at with prompt's values)
prompt_only_keys = [
    'social_media_news_title_prompt', 'social_media_news_content_prompt',
    'social_media_news_image_prompt', 'ai_tone', 'ai_language', 'ai_max_words',
]
for w in websites:
    for k in prompt_only_keys:
        if k in prompts:
            w[k] = prompts[k]

# Collect unique sources
handles = set()
subreddits = set()
for w in websites:
    for h in (w.get("twitter_handles") or []):
        val = None
        if isinstance(h, str) and h.strip():
            val = h.strip().replace("@", "")
        elif isinstance(h, dict):
            val = (h.get("value") or h.get("label") or "").strip().replace("@", "")
        if val:
            handles.add(val)

    if w.get("enable_reddit"):
        for s in (w.get("reddit_subreddits") or []):
            val = None
            if isinstance(s, str) and s.strip():
                val = s.strip().replace("r/", "")
            elif isinstance(s, dict):
                val = (s.get("value") or s.get("label") or "").strip().replace("r/", "")
            if val:
                subreddits.add(val)

handles = list(handles)
subreddits = list(subreddits)
print(f"📋 Sources: {len(handles)} X handles, {len(subreddits)} subreddits")

# ── Helpers for saving scraped data ──
RESULT_DIR = os.path.join(SCRIPT_DIR, "..", "result")
os.makedirs(RESULT_DIR, exist_ok=True)

def _save_scraped_json(data, filename_prefix):
    """Save scraped posts to a dated JSON file in result/."""
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = os.path.join(RESULT_DIR, f"{filename_prefix}_{today_str}.json")
    try:
        # Append to existing file if same day, otherwise create new
        existing = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False, default=str)
        print(f"💾 Saved {len(data)} posts → {filepath}")
    except Exception as e:
        print(f"⚠️ Failed to save {filepath}: {e}")

IMG_MATCH_DIR = os.path.join(SCRIPT_DIR, "..", "result", "img_match")
os.makedirs(IMG_MATCH_DIR, exist_ok=True)


def _check_image_exists(key, l_version, types):
    """Check if a generated image file actually exists on disk."""
    img_path = os.path.join(IMG_MATCH_DIR, f"{l_version}_{key}_{types}.png")
    return os.path.isfile(img_path) and os.path.getsize(img_path) > 0


def _cleanup_temp_image(key, l_version, types):
    """Remove temp image from img_match/ after it's been archived to result/images/."""
    try:
        temp_path = os.path.join(IMG_MATCH_DIR, f"{l_version}_{key}_{types}.png")
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception as e:
        print(f"⚠️ Temp image cleanup failed: {e}")


def _download_fallback_image(post, key, l_version, types):
    """
    Download the post's own embedded image as a fallback when AI image generation fails.
    Saves the first available image from the post to the expected img_match path
    so the WordPress upload in publish() still works.
    
    Returns True if a fallback image was saved, False otherwise.
    """
    post_images = post.get("images") or []
    if not post_images:
        print(f"⚠️ No fallback images available in post data")
        return False

    output_path = os.path.join(IMG_MATCH_DIR, f"{l_version}_{key}_{types}.png")

    for idx, img_url in enumerate(post_images):
        try:
            if not img_url or not isinstance(img_url, str):
                continue
            print(f"🖼️ Downloading fallback image ({idx+1}/{len(post_images)}): {img_url[:80]}...")
            resp = requests.get(img_url, timeout=15, stream=True)
            resp.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)

            print(f"✅ Fallback image saved → {output_path}")

            # Also archive to dated folder
            save_image_locally(key, l_version, types)

            return True
        except Exception as e:
            print(f"⚠️ Fallback image download failed for {img_url[:60]}: {e}")
            continue

    print(f"❌ All fallback image downloads failed")
    return False

# Fetch posts from all sources
all_posts = []

if subreddits:
    try:
        from social_media.reddit_scraper import fetch_reddit_data
        reddit_posts = fetch_reddit_data(subreddits, mode="hot", limit=15, hours_ago=12)
        all_posts.extend(reddit_posts)
        print(f"✅ Reddit: {len(reddit_posts)} posts")
        if reddit_posts:
            _save_scraped_json(reddit_posts, "reddit_posts")
    except Exception as e:
        print(f"❌ Reddit scraping error: {e}")

if handles:
    try:
        from social_media.x_scraper import fetch_x_data
        x_posts = fetch_x_data(handles)
        all_posts.extend(x_posts)
        print(f"✅ X: {len(x_posts)} posts")
        if x_posts:
            _save_scraped_json(x_posts, "x_posts")
    except Exception as e:
        print(f"❌ X scraping error: {e}")

if not all_posts:
    print("ℹ️ No posts fetched. Exiting.")
    sys.exit(0)

print(f"📊 Total posts to process: {len(all_posts)}")

# Optional: limit posts per run to avoid API quota exhaustion
max_posts = int(os.getenv("MAX_POSTS_PER_RUN", "0")) or len(all_posts)
if max_posts < len(all_posts):
    all_posts = all_posts[:max_posts]
    print(f"📊 Limited to {max_posts} posts per run (MAX_POSTS_PER_RUN)")

current_db_posts = current_db_social_media_posts()

for post in all_posts:
    post_id = post.get("post_id") or post.get("twitter_id")
    source = post.get("source", "x")
    source_handle = post.get("source_handle") or post.get("handler", "unknown")
    tweet_text = post.get("tweet_text", "No text")

    if not post_id:
        print(f"⚠️ Skipping post without ID from {source_handle}")
        continue

    message_tracker.add_message(
        types,
        message_tracker.MessageStage.RECORD_INSERTION,
        message_tracker.MessageStatus.SUCCESS,
        f"Processing {source} post from {source_handle} — {post_id}",
    )

    # Insert if new
    db_post = None
    if not check_data_exists_in_db(current_db_posts, post_id, "twitter_id"):
        db_post = insert_social_media_post(post, types)
        if not db_post:
            print(f"⚠️ Failed to insert {post_id}")
            message_tracker.add_message(
                types,
                message_tracker.MessageStage.RECORD_INSERTION,
                message_tracker.MessageStatus.ERROR,
                f"DB insert failed for {post_id}",
            )
            continue
        current_db_posts.append(db_post)
        print(f"✅ Inserted: [{source}] {post_id}")
    else:
        db_post = next((p for p in current_db_posts if p.get("twitter_id") == post_id), None)
        if not db_post:
            continue

    # Publish to each enabled website
    website_ids = []
    db_id = db_post.get("id")

    for website in websites:
        website_ids.append(str(website["id"]))

        if check_is_posted(db_post, str(website["id"])):
            print(f"ℹ️ Already posted {post_id} to {website.get('platform_name')}")
            continue

        l_version = website.get("l_version") or "eng"
        key = f"{post_id}_{website['id']}_{db_id}"
        title = ""
        workflow_success = False

        try:
            # ── Step 1: Image generation (non-blocking) ──
            # NOTE: generate_post_image → generate_gemini_image swallows exceptions
            # internally (logs via message_tracker), so we MUST verify the file
            # actually exists on disk rather than relying on exceptions.
            image_ready = False
            try:
                generate_post_image(post, key, l_version, types, website=website)
            except Exception as img_err:
                print(f"⚠️ AI image generation threw: {img_err}")

            # Verify the image file was actually created on disk
            if _check_image_exists(key, l_version, types):
                saved = save_image_locally(key, l_version, types)
                if saved:
                    image_ready = True
                    print(f"✅ AI image generated & saved")
                else:
                    print(f"⚠️ AI image generated but local save failed")
            else:
                print(f"⚠️ AI image generation produced no file — will try fallback")

            # ── Step 2: Fallback to post's own images if AI image failed ──
            if not image_ready:
                print(f"🖼️ Attempting fallback: using post's embedded images...")
                image_ready = _download_fallback_image(post, key, l_version, types)
                if image_ready:
                    message_tracker.add_message(
                        types,
                        message_tracker.MessageStage.IMAGE_GENERATION,
                        message_tracker.MessageStatus.SUCCESS,
                        "Using post's original image as fallback",
                    )
                else:
                    print(f"⚠️ No image available — publishing without featured image")
                    message_tracker.add_message(
                        types,
                        message_tracker.MessageStage.IMAGE_GENERATION,
                        message_tracker.MessageStatus.ERROR,
                        "No image available (AI gen failed + no post images). Publishing without image.",
                    )

            # Brief delay before content generation to avoid API rate limits
            api_delay(5)

            # ── Step 3: Content generation & publish (always runs) ──
            published = main_publication2(data=post, types=types, key=key, website=website, image_ready=image_ready)

            if not published:
                website_ids.pop()
                message_tracker.add_message(
                    types,
                    message_tracker.MessageStage.PUBLICATION,
                    message_tracker.MessageStatus.ERROR,
                    f"Publication failed: {website.get('platform_name')}",
                )
            else:
                title = published.get("title", f"Post from {source_handle}")
                workflow_success = True
                print(f"✅ Published to {website.get('platform_name')}")

        except Exception as e:
            print(f"❌ Error: {website.get('platform_name')}: {e}")
            message_tracker.add_message(
                types,
                message_tracker.MessageStage.PUBLICATION,
                message_tracker.MessageStatus.ERROR,
                f"Workflow error: {str(e)}",
            )
            wid = str(website["id"])
            if wid in website_ids:
                website_ids.remove(wid)

        finally:
            # Clean up temp image from img_match/ (permanent copy is in result/images/)
            _cleanup_temp_image(key, l_version, types)

            messages_json = message_tracker.get_messages_json(types)
            overall_status = message_tracker.get_overall_status(types)
            image_generated = message_tracker.was_image_generated(types)

            insert_log_to_db(
                news_type=types,
                title=title,
                website_name=website.get("platform_name", "Unknown"),
                image_generated=image_generated,
                status=overall_status,
                message=messages_json,
            )

            if overall_status == "Failed" or not workflow_success:
                module_disabled = module_failure_tracker.increment_failure(types)
                if module_disabled:
                    print(f"🛑 Module '{types}' disabled. Exiting.")
                    sys.exit(1)
            else:
                module_failure_tracker.reset_failure(types)

            message_tracker.clear_messages(types)

    if website_ids:
        update_post_in_db(db_id, "social_media_posts", website_ids)
        
        # Clear messages for this post
        message_tracker.clear_messages(types)

print("✅ Social media pipeline finished")
print("cron job finished")
