# session_manager.py
import os
import json
import requests
import fcntl  # File locking for Unix/Linux
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any

class TokenCache:
    """Shared token cache for cross-process communication to reduce API calls"""
    def __init__(self, cache_file='/app/.cms_token_cache.json'):
        self.cache_file = cache_file
        self.lock_file = cache_file + '.lock'
    
    def _acquire_lock(self):
        """Acquire file lock for thread-safe operations"""
        lock_fd = open(self.lock_file, 'w')
        try:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            return lock_fd
        except:
            lock_fd.close()
            raise
    
    def _release_lock(self, lock_fd):
        """Release file lock"""
        try:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
            lock_fd.close()
        except:
            pass
    
    def get_token(self) -> Optional[Dict[str, Any]]:
        """Get cached token if valid and not expired"""
        if not os.path.exists(self.cache_file):
            return None
        
        lock_fd = None
        try:
            lock_fd = self._acquire_lock()
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if token is being refreshed (another process is authenticating)
            if cache_data.get('refreshing'):
                # Another process is refreshing, return None to trigger wait/retry
                refresh_time = cache_data.get('refresh_started')
                if refresh_time:
                    try:
                        refresh_start = datetime.fromisoformat(refresh_time)
                        # If refresh has been happening for more than 30 seconds, assume it failed
                        if (datetime.now() - refresh_start).total_seconds() > 30:
                            # Refresh seems stuck, clear it and allow new refresh
                            cache_data.pop('refreshing', None)
                            cache_data.pop('refresh_started', None)
                            with open(self.cache_file, 'w') as f:
                                json.dump(cache_data, f, indent=2)
                        else:
                            # Token is being refreshed, wait for it
                            return None
                    except (ValueError, TypeError):
                        pass
            
            # Check if token is expired
            expiry_str = cache_data.get('token_expiry')
            if expiry_str:
                try:
                    expiry = datetime.fromisoformat(expiry_str)
                    if datetime.now() >= expiry:
                        # Token expired, mark as refreshing
                        cache_data['refreshing'] = True
                        cache_data['refresh_started'] = datetime.now().isoformat()
                        with open(self.cache_file, 'w') as f:
                            json.dump(cache_data, f, indent=2)
                        self._release_lock(lock_fd)
                        lock_fd = None
                        return None
                except (ValueError, TypeError):
                    # Invalid expiry format, treat as expired
                    self._release_lock(lock_fd)
                    lock_fd = None
                    self.clear_cache()
                    return None
            
            # Token is valid, clear any refreshing flag
            if 'refreshing' in cache_data:
                cache_data.pop('refreshing', None)
                cache_data.pop('refresh_started', None)
                with open(self.cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2)
            
            return cache_data
        except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
            # Silently handle cache errors - fall back to authentication
            return None
        finally:
            if lock_fd:
                self._release_lock(lock_fd)
    
    def save_token(self, token: str, expiry: datetime):
        """Save token to cache file and clear refreshing flag"""
        cache_data = {
            'token': token,
            'token_expiry': expiry.isoformat(),
            'last_updated': datetime.now().isoformat(),
            'refreshing': False  # Clear refreshing flag
        }
        
        # Remove refresh_started if it exists
        if 'refresh_started' in cache_data:
            cache_data.pop('refresh_started')
        
        lock_fd = None
        try:
            lock_fd = self._acquire_lock()
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except (IOError, OSError):
            # Silently fail - cache is optional
            pass
        finally:
            if lock_fd:
                self._release_lock(lock_fd)
    
    def clear_cache(self):
        """Clear the token cache"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except (IOError, OSError):
            pass

class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.session = requests.Session()
        self.token = None
        self.token_expiry = None
        self.user = None
        self.base_url = os.getenv('CMS_BASE_URL')
        self.last_validation = None
        # Initialize shared token cache
        self.token_cache = TokenCache()
        
        # Try to load token from cache on startup
        self._load_token_from_cache()
    
    def _load_token_from_cache(self) -> bool:
        """Load token from shared cache file"""
        cache_data = self.token_cache.get_token()
        if cache_data and cache_data.get('token'):
            self.token = cache_data.get('token')
            expiry_str = cache_data.get('token_expiry')
            if expiry_str:
                try:
                    self.token_expiry = datetime.fromisoformat(expiry_str)
                except (ValueError, TypeError):
                    return False
            
            if self.token and self.token_expiry:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                })
                print(f"✅ Loaded token from shared cache (expires: {self.token_expiry.strftime('%Y-%m-%d %H:%M:%S')})", flush=True)
                return True
        return False
        
    def set_token(self, token):
        """Store token and set expiry for 3 days, save to shared cache"""
        self.token = token
        self.token_expiry = datetime.now() + timedelta(days=3)
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        # Save to shared cache for other processes
        self.token_cache.save_token(token, self.token_expiry)
        print(f"💾 Token saved to shared cache (valid for 3 days)", flush=True)
        
    def get_token(self):
        """Get current token if valid and not expired. Check cache if no token in memory."""
        # If we have a valid token in memory, use it
        if self.token and not self.is_token_expired():
            return self.token
        
        # Try to load from shared cache if we don't have a valid token
        if not self.token or self.is_token_expired():
            if self._load_token_from_cache():
                return self.token
        
        # No valid token found
        if self.is_token_expired():
            self.reset_session()
        return None
        
    def is_token_expired(self):
        """Check if token has expired (3 days)"""
        if not self.token or not self.token_expiry:
            return True
        return datetime.now() >= self.token_expiry

    def validate_token(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate a token passed from middleware
        Returns: (is_valid, user_data, error_message)
        """
        if not token:
            return False, None, "No token provided"
        # Store original token temporarily
        original_token = self.token
        original_headers = self.session.headers.copy()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        try:
            auth_me_url = f"{self.base_url}/api/auth/me"
            response = requests.get(auth_me_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                user_data = response.json()
                return True, user_data, None
            else:
                return False, None, f"Auth me returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, None, f"Network error: {str(e)}"
        
        finally:
            # Restore original session state
            self.token = original_token
            self.session.headers = original_headers
      
    def reset_session(self):
        """Clear session data and cache"""
        self.token = None
        self.token_expiry = None
        self.user = None
        self.last_validation = None
        if 'Authorization' in self.session.headers:
            self.session.headers.pop('Authorization')
        # Clear shared cache
        self.token_cache.clear_cache()
            
    def get_authenticated_session(self):
        """Get the authenticated session object if valid"""
        if self.get_token():  # This checks expiration
            return self.session
        return None
        
    def validate_with_auth_me(self):
        """
        Validate the current session by calling /auth/me
        Returns True if valid, False otherwise
        """
        if not self.get_token():
            return False
            
        try:
            auth_me_url = f"{self.base_url}/api/auth/me"
            response = self.session.get(auth_me_url, timeout=15)
            
            if response.status_code == 200:
                user_data = response.json()
                self.user = user_data
                self.last_validation = datetime.now()
                return True
            else:
                return False
                
        except requests.exceptions.RequestException as e:
            return False
            
    def should_revalidate(self):
        """Check if we should revalidate the session (every hour)"""
        if not self.last_validation:
            return True
        return (datetime.now() - self.last_validation) > timedelta(hours=1)
    
session_manager = SessionManager()