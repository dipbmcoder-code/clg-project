import os
import json
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Imports from sibling modules
from publication.db_for_app import upload_image_to_wordpress
from publication.cms_db import decrypt_password
from publication.utils import generate_openai_content, replace_vars
from publication.message_tracker import add_message, MessageStage, MessageStatus

load_dotenv()
root_folder = Path(__file__).resolve().parents[1]

def publish(data_j, title, text_all, types, key, l_version, **kwargs):
    """
    Publish content to WordPress via REST API.

    Args:
        data_j: Website config dict (platform_url, platform_user, etc.)
        title: Article headline
        text_all: Article HTML body
        types: Module type string (e.g. 'social_media')
        key: Unique key for image file naming
        l_version: Language version (eng, ru, etc.)
    """
    try:
        platform_name = data_j.get('platform_name', 'wordpress')
        url = data_j['platform_url'].strip()
        user = data_j['platform_user'].strip()
        password = data_j['platform_password'].strip()
        
        # Determine post status (default to publish if not specified)
        type_status = data_j.get('post_status', 'publish')

        auth_type = data_j.get('auth_type', 'json')
        application_password = data_j.get('application_password', '')
        author = data_j.get('website_author') or []

        # Try to decrypt password; fall back to plain text if decryption fails
        decryptPassword = None
        try:
            decryptPassword = decrypt_password(password)
        except Exception:
            pass
        if not decryptPassword:
            # Password stored as plain text — use as-is
            decryptPassword = password
            print(f"ℹ️ Using plain text password for {platform_name}")

        if auth_type == 'json':
            credentials = user + ':' + decryptPassword
        else:
            credentials = user + ':' + (application_password or decryptPassword)

        category = "1"
        tags = ''
        if data_j.get('categories'):
            try:
                category_ids = []
                for cat in data_j['categories']:
                    if isinstance(cat, dict):
                        cat_id = cat.get('id') or cat.get('value')
                        if cat_id:
                            category_ids.append(str(cat_id))
                    else:
                        category_ids.append(str(cat))
                if category_ids:
                    category = ','.join(category_ids)
            except Exception as e:
                print(f"⚠️ Category parsing warning: {e}")
                category = "1"

        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        
        # Image handling
        img_id = 0
        feature_img_mode = data_j.get('featured_image', 'upload') 
        
        post = {
            'title': title,
            'status': f'{type_status}',
            'content': text_all,
            'categories': category,
            'tags': tags,
        }

        if feature_img_mode == 'upload' or feature_img_mode is None:
            # Construct path to generated image
            # Image is saved locally by generate_post_image => publication.utils.generate_gemini_image
            # Path: root_folder / result / img_match / {l_version}_{key}_{types}.png
            img_path = root_folder / f'result/img_match/{l_version}_{key}_{types}.png'
            
            if os.path.exists(img_path):
                print(f"📤 Uploading image: {img_path}")
                img_id = upload_image_to_wordpress(
                    img_path,
                    url + '/wp-json/wp/v2/media',
                    header, key, types
                )
                print(f"✅ Image ID: {img_id}")
                post['featured_media'] = img_id
            else:
                print(f"⚠️ Image file not found: {img_path}")
        
        if author and isinstance(author, list) and len(author) > 0:
            author_id = author[0].get('id') or author[0].get('value')
            if author_id:
                post['author'] = author_id

        # Send Post Request
        response = requests.post(url + '/wp-json/wp/v2/posts', headers=header, json=post)
        
        if response.status_code >= 400:
             raise Exception(f"WP API Error {response.status_code}: {response.text}")
        
        response_json = response.json()
        post_id = response_json.get("id")
        
        site_posted_data = {
            "website": data_j.get('platform_url'),
            "Post Id": post_id,
            "time": response_json.get('date'),
            "website_name": data_j.get('platform_name'),
            "website_id": data_j.get('id'),
            "title": title,
        }
        
        print(f"✅ Posted to {site_posted_data['website_name']} (ID: {post_id})")

        add_message(
            types,
            MessageStage.PUBLICATION,
            MessageStatus.SUCCESS,
            f"News published successfully to {data_j.get('platform_name')}"
        )

        return site_posted_data

    except Exception as e:
        print(f"❌ Publication error for {data_j.get('platform_url')}: {e}")
        add_message(
            types,
            MessageStage.PUBLICATION,
            MessageStatus.ERROR,
            f"Publication failed for {data_j.get('platform_name', 'unknown site')}",
            error_details=str(e)
        )
        return None


def _build_source_embed(data):
    """
    Build an embed of the original social media post.
    Uses official oEmbed blockquote formats that WordPress renders natively.

    Returns HTML string — Twitter blockquote or Reddit blockquote.
    """
    source = data.get("source", "")
    permalink = data.get("permalink", "")

    if source == "x" and permalink:
        # Official Twitter/X oEmbed blockquote format
        handler = data.get("handler") or data.get("source_handle", "")
        clean_handle = handler.replace("@", "")
        tweet_text = data.get("tweet_text", "")
        embedded_url = data.get("embedded_url", "")
        timestamp = data.get("timestamp", "")

        # Format date as "March 6, 2026"
        display_date = timestamp
        try:
            from datetime import datetime as _dt
            for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
                try:
                    dt = _dt.strptime(timestamp[:26], fmt)
                    display_date = dt.strftime("%B %-d, %Y")
                    break
                except ValueError:
                    continue
        except Exception:
            pass

        # Convert newlines to <br> in tweet text
        tweet_html = tweet_text.replace("\n", "<br> ")

        # Append embedded URL as link if present
        if embedded_url:
            tweet_html += f'<br> <a href="{embedded_url}">{embedded_url}</a>'

        # Build twitter.com permalink with ref_src param
        twitter_url = permalink.replace("https://x.com/", "https://twitter.com/")
        if "?" not in twitter_url:
            twitter_url += "?ref_src=twsrc%5Etfw"

        return (
            f'<blockquote class="twitter-tweet">'
            f'<p lang="en" dir="ltr">{tweet_html}</p>'
            f'&mdash; {clean_handle} (@{clean_handle}) '
            f'<a href="{twitter_url}">{display_date}</a>'
            f'</blockquote>'
            f' <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        )

    elif source == "reddit" and permalink:
        # Official Reddit oEmbed blockquote format
        post_title = data.get("post_title", data.get("tweet_text", ""))
        # Extract subreddit from source_handle (e.g. "r/technology")
        subreddit = data.get("source_handle", data.get("handler", ""))
        if not subreddit.startswith("r/"):
            subreddit = ""
        subreddit_name = subreddit.replace("r/", "") if subreddit else ""
        # Get the Reddit author username
        author_name = data.get("reddit_author", data.get("author", ""))
        # Ensure permalink uses www.reddit.com
        reddit_permalink = permalink.replace("https://reddit.com", "https://www.reddit.com")
        if not reddit_permalink.startswith("https://www.reddit.com"):
            reddit_permalink = f"https://www.reddit.com{permalink}" if permalink.startswith("/") else permalink

        return (
            f'<blockquote class="reddit-embed-bq" style="height:500px" data-embed-height="240">\n'
            f'<a href="{reddit_permalink}">{post_title}</a><br> by\n'
            f'<a href="https://www.reddit.com/user/{author_name}/">u/{author_name}</a> in\n'
            f'<a href="https://www.reddit.com/{subreddit}/">{subreddit_name}</a>\n'
            f'</blockquote>'
            f'<script async="" src="https://embed.reddit.com/widgets.js" charset="UTF-8"></script>'
        )

    # No embed possible — return empty
    return ""


def main_publication2(data, types, key, website, image_ready=True):
    """
    Main logic to generate and publish content.
    When image_ready=False, embeds the original social media post (iframe/blockquote)
    into the article as a visual source reference.
    """
    if types != 'social_media':
        print(f"ℹ️ main_publication2 called with unsupported type: {types}")
        return None

    # Determine categories
    # Copy social_media_categories to categories as expected by publish logic
    website.setdefault('categories', [])
    if website.get('social_media_categories'):
        website['categories'] = website['social_media_categories']

    # Extract Data
    handler = data.get('handler') or data.get('source_handle') or 'Unknown'
    tweet_text = data.get("tweet_text", "")
    tweeted_time = data.get("timestamp", "")
    url = data.get("embedded_url", "")
    
    # Check l_version
    l_version = website.get('l_version') or 'eng'

    # Prepare Prompts
    prompt_vars = {
        "tweet_text": tweet_text,
        "handler": handler,
        "timestamp": tweeted_time,
        "all_data": json.dumps(data, default=str)
    }
    
    # Use prompts from DB (injected into website dict) or defaults
    custom_title = website.get('social_media_news_title_prompt')
    custom_news = website.get('social_media_news_content_prompt')
    
    if custom_news and custom_title:
        print(f"📝 Using custom prompts from DB for content generation")
        news_prompt = replace_vars(custom_news, prompt_vars)
        title_prompt = replace_vars(custom_title, prompt_vars)
        list_text = [title_prompt, news_prompt]
    else:
        print(f"⚠️ Custom prompts missing (title={bool(custom_title)}, content={bool(custom_news)}), using default prompts")
        # Fallback prompts
        list_text = [
            f"Write a professional, SEO-optimized headline for a news story based on this content: '{tweet_text[:100]}'. The headline should be compelling and journalistic. Do NOT mention social media.",
            f"You are a professional journalist. Turn the following content into a professional news article (300 words). Content: '{tweet_text}'. Source: {handler}. Tone: Neutral, informative."
        ]

    # Generate Content
    index_openai = 0
    main_text_list = []
    title_openAI = ""
    additional_text = "" 

    for text in list_text:
        index_openai += 1
        result = generate_openai_content(text, types)

        if not result:
            print("⚠️ OpenAI returned empty result.")
            return None
        
        if len(list_text) == 1:
            # Single prompt case
            paragraphs = result.split("\n\n")
            title_openAI = paragraphs[0]
            if len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    paragraph = paragraph.replace('*',"").strip()
                    if paragraph:
                        main_text_list.append(f"<p>{paragraph}</p>\n")
        else:
            # Multi prompt case (Head + Body)
            if index_openai != 1:
                # Body
                for paragraph in result.split("\n\n"):
                    paragraph = paragraph.replace('*',"").strip()
                    if paragraph:
                        main_text_list.append(f"<p>{paragraph}</p>\n")
            else:
                # Title
                title_openAI = result

    # Clean Title
    for i in ['"', "'",'*']:
        title_openAI = title_openAI.replace(i, "") if i in title_openAI else title_openAI

    # ── Always embed original social media post as source reference ──
    source_embed = _build_source_embed(data)
    if source_embed:
        source_label = "X (Twitter)" if data.get("source") == "x" else "Reddit"
        print(f"📌 Embedding original {source_label} post")
    else:
        print(f"⚠️ Could not build embed for source={data.get('source')}")

    # Construct HTML
    article_html = f"""
        <article>
        {''.join(main_text_list)}
        {additional_text}
        </article>
        {source_embed}
        """
    
    # Publish
    return publish(website, title_openAI, article_html, types, key, l_version)