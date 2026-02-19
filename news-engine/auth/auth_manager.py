# auth_manager.py
import os
import json
import time
import threading
import requests
from datetime import datetime
from auth.session_manager import session_manager
from typing import Tuple, Optional, Dict, Any

class AuthManager:
    _lock = threading.Lock()  # Lock to prevent concurrent authentication attempts
    
    def __init__(self):
        self.base_url = os.getenv('CMS_BASE_URL')
        self._last_auth_time = 0
        self._min_auth_interval = 2  # Minimum 2 seconds between auth attempts
        
    def login(self, email=None, password=None, max_retries=3):
        """Perform login to get backend token with retry logic and rate limiting"""
        login_url = f"{self.base_url}/api/auth/login"
        
        # Use provided credentials or fall back to env vars
        login_data = {
            "email": email or os.getenv('CMS_ADMIN_USER_EMAIL'),
            "password": password or os.getenv('CMS_ADMIN_USER_PASSWORD')
        }
        
        if not login_data['email'] or not login_data['password']:
            print(f"❌ Authentication failed: Missing credentials", flush=True)
            print(f"   Email: {'Set' if login_data['email'] else 'MISSING'}", flush=True)
            print(f"   Password: {'Set' if login_data['password'] else 'MISSING'}", flush=True)
            print(f"   CMS_BASE_URL: {self.base_url or 'MISSING'}", flush=True)
            return False
        
        # Use lock to serialize authentication attempts across threads
        with self._lock:
            # Rate limiting: ensure minimum time between auth attempts
            current_time = time.time()
            time_since_last_auth = current_time - self._last_auth_time
            if time_since_last_auth < self._min_auth_interval:
                wait_time = self._min_auth_interval - time_since_last_auth
                print(f"⏳ Rate limiting: waiting {wait_time:.1f}s before next auth attempt...", flush=True)
                time.sleep(wait_time)
            
            self._last_auth_time = time.time()
            
            # Retry logic with exponential backoff for rate limit errors
            for attempt in range(max_retries):
                try:
                    response = requests.post(login_url, json=login_data, timeout=10)
                    
                    # Handle rate limiting (429 Too Many Requests)
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', 5 + attempt * 2))
                        if attempt < max_retries - 1:
                            print(f"⚠️ Rate limited (429). Retrying after {retry_after}s (attempt {attempt + 1}/{max_retries})...", flush=True)
                            time.sleep(retry_after)
                            continue
                        else:
                            print(f"❌ Rate limited (429). Max retries reached.", flush=True)
                            return False
                    
                    response.raise_for_status()
                    response_data = response.json()
                    token = response_data.get('data', {}).get('token') if isinstance(response_data, dict) else None
                    
                    if token:
                        session_manager.set_token(token)
                        print("✅ Successfully authenticated with CMS", flush=True)
                        return True
                    else:
                        print(f"❌ Authentication failed: No token in response", flush=True)
                        print(f"   Status code: {response.status_code}", flush=True)
                        print(f"   Response: {str(response_data)[:200]}", flush=True)
                        return False
                        
                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                        print(f"⚠️ Auth request timeout. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...", flush=True)
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Auth request timeout after {max_retries} attempts", flush=True)
                        return False
                        
                except requests.exceptions.RequestException as e:
                    # Check if it's a 429 rate limit error
                    is_rate_limit = False
                    retry_after = 5 + attempt * 2
                    status_code = None
                    
                    # Try to get status code from exception response if available
                    if hasattr(e, 'response') and e.response is not None:
                        status_code = e.response.status_code
                        if status_code == 429:
                            is_rate_limit = True
                            retry_after = int(e.response.headers.get('Retry-After', retry_after))
                        elif status_code == 401:
                            print(f"❌ Authentication failed: Invalid credentials (401 Unauthorized)", flush=True)
                            print(f"   Please check CMS_ADMIN_USER_EMAIL and CMS_ADMIN_USER_PASSWORD", flush=True)
                        elif status_code:
                            print(f"⚠️ Auth request failed with status {status_code}: {e}", flush=True)
                    
                    if attempt < max_retries - 1 and is_rate_limit:
                        print(f"⚠️ Rate limited (429) in auth request: {e}. Retrying after {retry_after}s (attempt {attempt + 1}/{max_retries})...", flush=True)
                        time.sleep(retry_after)
                        continue
                    elif attempt < max_retries - 1 and status_code not in [401]:
                        # Don't retry on 401 (bad credentials) - it won't help
                        wait_time = 2 ** attempt
                        print(f"⚠️ Auth request failed: {e}. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...", flush=True)
                        time.sleep(wait_time)
                        continue
                    else:
                        if status_code == 401:
                            print(f"❌ Authentication failed after {max_retries} attempts: Invalid credentials", flush=True)
                        else:
                            print(f"❌ Auth request failed after {max_retries} attempts: {e}", flush=True)
                        return False
            
            return False
            
    def validate_with_auth_me(self):
        """Validate current session with auth/me endpoint"""
        return session_manager.validate_with_auth_me()

    def validate_token_for_middleware(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Comprehensive token validation for middleware use
        Returns: (is_valid, user_data, error_message)
        """
        #self.ensure_authenticated()
        return session_manager.validate_token(token)
            
    def ensure_authenticated(self, force_revalidate=False):
        """
        Ensure we have a valid authenticated session
        Checks session, validates with auth/me, logs in if needed
        Handles expired tokens by re-authenticating with refreshing flag check
        """
        import time
        import json
        
        # Check if we have a valid token (not expired)
        token = session_manager.get_token()
        
        # If token is None, it might be expired or being refreshed
        if not token:
            # Check cache file directly to see if another process is refreshing
            # (get_token() might return None even if refreshing is true)
            cache_file = session_manager.token_cache.cache_file
            if os.path.exists(cache_file):
                try:
                    lock_fd = session_manager.token_cache._acquire_lock()
                    try:
                        with open(cache_file, 'r') as f:
                            cache_data = json.load(f)
                        
                        # Check if another process is refreshing
                        if cache_data.get('refreshing'):
                            refresh_started = cache_data.get('refresh_started')
                            if refresh_started:
                                try:
                                    refresh_start = datetime.fromisoformat(refresh_started)
                                    elapsed = (datetime.now() - refresh_start).total_seconds()
                                    
                                    # Wait for refresh if it's recent (within 60 seconds)
                                    if elapsed < 60:
                                        session_manager.token_cache._release_lock(lock_fd)
                                        lock_fd = None
                                        print(f"⏳ Token expired. Another process is refreshing (started {elapsed:.0f}s ago). Waiting...", flush=True)
                                        
                                        # Wait up to 60 seconds for refresh, checking every 2 seconds
                                        for wait in range(30):  # 30 iterations × 2 seconds = 60 seconds max
                                            time.sleep(2)
                                            
                                            # Check cache again
                                            if os.path.exists(cache_file):
                                                check_lock = None
                                                try:
                                                    check_lock = session_manager.token_cache._acquire_lock()
                                                    with open(cache_file, 'r') as check_f:
                                                        check_data = json.load(check_f)
                                                    
                                                    if not check_data.get('refreshing'):
                                                        # Refresh completed or failed
                                                        break
                                                    
                                                    # Check if new token exists
                                                    if check_data.get('token') and check_data.get('token_expiry'):
                                                        expiry_str = check_data.get('token_expiry')
                                                        try:
                                                            expiry = datetime.fromisoformat(expiry_str)
                                                            if datetime.now() < expiry:
                                                                # New valid token found!
                                                                token = session_manager.get_token()
                                                                if token:
                                                                    print("✅ Token refreshed by another process!", flush=True)
                                                                    session_manager.token_cache._release_lock(check_lock)
                                                                    return True
                                                        except (ValueError, TypeError):
                                                            pass
                                                except (IOError, OSError, json.JSONDecodeError, KeyError):
                                                    pass
                                                finally:
                                                    if check_lock:
                                                        session_manager.token_cache._release_lock(check_lock)
                                            
                                            # Try to get token
                                            token = session_manager.get_token()
                                            if token:
                                                print("✅ Token refreshed by another process!", flush=True)
                                                return True
                                        
                                        print("⚠️ Refresh timeout. Proceeding with authentication...", flush=True)
                                    else:
                                        # Refresh took too long, assume it failed
                                        print(f"⚠️ Refresh seems stuck ({elapsed:.0f}s). Proceeding with authentication...", flush=True)
                                except (ValueError, TypeError):
                                    pass
                    finally:
                        if lock_fd:
                            session_manager.token_cache._release_lock(lock_fd)
                except (IOError, OSError, json.JSONDecodeError, KeyError):
                    # Cache read error, proceed with authentication
                    pass
            
            # Token expired or refresh failed, re-authenticate (with lock protection)
            print("🔄 Authenticating with CMS...", flush=True)
            session_manager.reset_session()
            return self.login()
        
        # Check if we need to validate with auth/me
        if force_revalidate or session_manager.should_revalidate():
            if self.validate_with_auth_me():
                return True
            else:
                session_manager.reset_session()
                return self.login()
        else:
            return True
        
    def get_headers(self):
        """Get authenticated headers if session is valid"""
        if session_manager.get_token():
            return {
                "Authorization": f"Bearer {session_manager.token}",
                "Content-Type": "application/json"
            }
        return None
        
    def get_user_info(self):
        """Get current user information from validated session"""
        if session_manager.user and session_manager.get_token():
            return session_manager.user
        return None
        
    def cleanup_expired_sessions(self):
        """Clean up any expired sessions"""
        if session_manager.is_token_expired():
            session_manager.reset_session()

auth_manager = AuthManager()