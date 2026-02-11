import requests
import os
import base64
from auth.session_manager import session_manager
from auth.auth_manager import auth_manager
from datetime import datetime, timezone
import time
import unicodedata

def fetch_websites_from_api():
    """Fetch websites from API (actual API call)"""
    try:
        # Ensure we're authenticated
        if not auth_manager.ensure_authenticated():
            raise Exception("Failed to authenticate with CMS")
        
        # Use the authenticated session from session_manager
        session = session_manager.get_authenticated_session()
        
        if not session:
            raise Exception("No authenticated session available")
    
        cms_website_url = f"{os.getenv('CMS_BASE_URL')}/content-manager/collection-types/api::users-website.users-website"
        params = {
            "filters[active][$eq]": "true",
            "filters[is_validated][$eq]": "true",
            "populate": "*"
        }
        try:
            response = session.get(cms_website_url, params=params, timeout=30)
            response.raise_for_status()
            print(f"✅ Success!")
            data = response.json()
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching users websites: {e}")
            return None
    except Exception as _ex:
        print(f"Error calling auth cms: {_ex}")
        return []

def fetch_news_prompts():
    """Fetch global news prompts from CMS Single Type"""
    try:
        # Authentication is handled by session_manager, reused from fetch_websites
        if not auth_manager.ensure_authenticated():
            print("⚠️ Auth failed for news prompts")
            return None
        
        session = session_manager.get_authenticated_session()
        if not session:
            return None

        # Content Manager Single Type Endpoint
        url = f"{os.getenv('CMS_BASE_URL')}/content-manager/single-types/api::news-prompt.news-prompt"
        
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Strapi Content Manager usually returns the object directly
            return data
        else:
            print(f"⚠️ Failed to fetch news prompts. Status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching news prompts: {e}")
        return None

def get_websites():
    """
    Get websites from API and inject global news prompts.
    """
    # Fetch from API directly
    websites = fetch_websites_from_api()
    
    if websites is None:
        return []
        
    # Fetch global prompts
    prompts = fetch_news_prompts()
    
    # Inject prompts into each website configuration
    if prompts and isinstance(prompts, dict):
        print(f"ℹ️ Injecting global news prompts into {len(websites)} websites")
        for website in websites:
            website.update(prompts)
    return websites

def get_leagues_id(websites):
    leagues_ids = list({
        league.get("id")
        for website in websites
        for league in website.get("website_leagues", []) or []
    })
    return leagues_ids

def filter_websites_by_leagues(websites, league_id):
    filtered_websites = []
    for website in websites:
        website_leagues = website.get('website_leagues') or []
        if any(league.get('id') == int(league_id) for league in website_leagues):
            filtered_websites.append(website)
    return filtered_websites

def filter_websites_by_enable(websites, types):
    if types == 'transfer':
        return [w for w in websites if w.get('enable_transfer_rumors')]
    if types == 'rumour':
        return [w for w in websites if w.get('enable_transfer_rumors')]
    if types == 'player_abroad':
        return [w for w in websites if w.get('enabled_player_abroad')]
    if types == 'player_profile':
        return [w for w in websites if w.get('enable_player_profiles')]
    if types == 'social_media':
        return [w for w in websites if w.get('enable_social_media')]
    if types == 'preview':
        return [w for w in websites if w.get('enable_match_previews')]
    if types == 'review':
        return [w for w in websites if w.get('enable_match_reviews')]
    if types == 'where_to_watch':
        return [w for w in websites if w.get('enabled_where_to_watch')]
    return []

def check_enable_for(websites, types):
    if types == 'transfer':
        return any(website.get('enable_transfer_rumors') for website in websites)
    if types == 'rumour':
        return any(website.get('enable_transfer_rumors') for website in websites)
    if types == 'player_abroad':
        return any(website.get('enabled_player_abroad') for website in websites)
    if types == 'player_profile':
        return any(website.get('enable_player_profiles') for website in websites)
    if types == 'social_media':
        return any(website.get('enable_social_media') for website in websites)
    if types == 'preview':
        return any(website.get('enable_match_previews') for website in websites)
    if types == 'review':
        return any(website.get('enable_match_reviews') for website in websites)
    if types == 'where_to_watch':
        return any(website.get('enabled_where_to_watch') for website in websites)
    return False
    
def decode_url_safe_base64(key_base64):
    """Convert URL-safe base64 to standard base64"""
    # Replace URL-safe characters
    standard_base64 = key_base64.replace('-', '+').replace('_', '/')
    
    # Add padding
    pad_count = (4 - len(standard_base64) % 4) % 4
    standard_base64 += '=' * pad_count
    
    return base64.b64decode(standard_base64)

def decrypt_password(encrypted_text):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    # Get key from environment
    key_base64 = os.getenv('PASSWORD_SECRET_KEY')
    
    # Decode URL-safe base64 key
    key = decode_url_safe_base64(key_base64)
    
    print(f"Key length: {len(key)} bytes")
    
    if len(key) != 32:
        raise ValueError(f"Key must be 32 bytes, got {len(key)}")
    
    # Decrypt
    ciphertext = base64.b64decode(encrypted_text)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted, AES.block_size).decode('utf-8')
    
    return decrypted

def get_websites_leagues(websites):
    return {
        league['id']
        for website in websites
        if isinstance(website, dict)
        for league in website.get('website_leagues', []) or []
        if isinstance(league, dict) and 'id' in league
    }

def filter_website_by_datetime(websites, types):
    if types == 'player_profile':
        return [
            w 
            for w in websites 
            if any('id' in player and 'datetime' in player and match_datetime(player['datetime']) for player in w.get('player_profiles', []))         
        ]
    return []  

def get_websites_players(websites):
    return {
        player['id']
        for website in websites
        for player in website.get('player_profiles', [])
        if 'id' in player and 'datetime' in player and match_datetime(player['datetime'])
    }

def match_datetime(match_dt):
    match_dt = datetime.fromisoformat(match_dt.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    print("Timezone name:", time.tzname)
    print(f"match date time: {match_dt}")
    print(f"now date time: {now}")
    return match_dt.date() == now.date() and match_dt <= now

def get_unique_field(websites, field_name):
        """
        Extracts unique values of a given field from all websites.
        Works for list fields (like twitter_handles, leagues, categories).
        """
        unique_values = set()

        for site in websites:
            if field_name in site and site[field_name]:
                values = site[field_name]

                # If it's a list of dicts (like leagues/social_media_categories)
                if isinstance(values, list) and all(isinstance(v, dict) for v in values):
                    for v in values:
                        if "shortName" in v:
                            unique_values.add(
                                unicodedata.normalize("NFKD", v["shortName"])
                                .encode("ascii", "ignore")
                                .decode("utf-8")
                                .lower()
                            )
                        elif "name" in v:
                            unique_values.add(v["name"])
                        elif "id" in v:
                            unique_values.add(v["id"])
                # If it's a simple list (like twitter_handles)
                elif isinstance(values, list):
                    for v in values:
                        if isinstance(v, str):
                            unique_values.add(v.strip())
                # If it's a single value
                else:
                    unique_values.add(values)

        return list(unique_values)

def get_max_hours(websites, types):
    if len(websites) > 0:
        if types == 'preview':
            return max(w.get('match_previews_time') or 0 for w in websites)
        return 0
    else: 0

def get_min_minutes(websites, types):
    if len(websites) > 0:
        if types == 'review':
            return max(w.get('match_reviews_time') or 0 for w in websites)
        return 0
    else: 0

def get_websites_countries(websites, types):
    countries = []
    if types == 'transfer' or types == 'rumour':
        countries = list({c['code']: c for w in websites for c in (w.get('transfer_rumour_countries') or [])}.values())
    elif types == 'player_abroad':
        countries = list({c['code']: c for w in websites for c in (w.get('player_abroad_countries') or [])}.values())
    elif types == 'where_to_watch':
        countries = list({c['code']: c for w in websites for c in (w.get('where_to_watch_countries') or [])}.values())
    return countries