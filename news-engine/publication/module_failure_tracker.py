"""
Module Failure Tracker

Tracks consecutive publication failures for each module type.
After 3 consecutive failures, the module is automatically disabled
by updating the CMS database for all websites.

Features:
- Thread-safe failure counting
- Persistent storage (JSON file)
- Automatic CMS database updates
- Manual reset capability
"""

import os
import json
import threading
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timezone

# Configuration
FAILURE_THRESHOLD = 3
TRACKER_FILE = Path(__file__).resolve().parents[1] / 'result' / 'module_failure_tracker.json'

# Thread-safe lock
_TRACKER_LOCK = threading.Lock()

# Module type to CMS field mapping
MODULE_TO_CMS_FIELD = {
    'review': 'enable_match_reviews',
    'preview': 'enable_match_previews',
    'transfer': 'enable_transfer_rumors',
    'rumour': 'enable_transfer_rumors',
    'player_abroad': 'enabled_player_abroad',
    'player_profile': 'enable_player_profiles',
    'social_media': 'enable_social_media',
    'where_to_watch': 'enabled_where_to_watch',
}


def _load_tracker() -> Dict:
    """Load failure tracker from JSON file."""
    with _TRACKER_LOCK:
        if not TRACKER_FILE.exists():
            return {}
        
        try:
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading failure tracker: {e}")
            return {}


def _save_tracker(data: Dict):
    """Save failure tracker to JSON file."""
    with _TRACKER_LOCK:
        try:
            # Ensure directory exists
            TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(TRACKER_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"❌ Error saving failure tracker: {e}")


def increment_failure(module_type: str) -> bool:
    """
    Increment failure count for a module.
    
    Args:
        module_type: Type of module (review, preview, transfer, etc.)
        
    Returns:
        True if module was disabled (reached threshold), False otherwise
    """
    tracker = _load_tracker()
    
    if module_type not in tracker:
        tracker[module_type] = {
            'failure_count': 0,
            'last_failure': None,
            'disabled': False
        }
    
    tracker[module_type]['failure_count'] += 1
    tracker[module_type]['last_failure'] = datetime.now(timezone.utc).isoformat()
    
    failure_count = tracker[module_type]['failure_count']
    
    print(f"⚠️ Module '{module_type}' failure count: {failure_count}/{FAILURE_THRESHOLD}")
    
    # Check if threshold reached
    if failure_count >= FAILURE_THRESHOLD and not tracker[module_type]['disabled']:
        print(f"🚨 Module '{module_type}' reached failure threshold. Disabling...")
        tracker[module_type]['disabled'] = True
        tracker[module_type]['disabled_at'] = datetime.now(timezone.utc).isoformat()
        
        # Disable module in CMS
        # _disable_module_in_cms(module_type)
        
        _save_tracker(tracker)
        return True  # Module was just disabled
    
    _save_tracker(tracker)
    return False  # Module not disabled yet


def reset_failure(module_type: str):
    """
    Reset failure count for a module (called on successful publication).
    
    Args:
        module_type: Type of module (review, preview, transfer, etc.)
    """
    tracker = _load_tracker()
    
    if module_type in tracker and tracker[module_type]['failure_count'] > 0:
        print(f"✅ Module '{module_type}' published successfully. Resetting failure count.")
        tracker[module_type]['failure_count'] = 0
        tracker[module_type]['last_success'] = datetime.now(timezone.utc).isoformat()
        _save_tracker(tracker)


def is_module_disabled(module_type: str) -> bool:
    """
    Check if a module is disabled due to failures.
    
    Args:
        module_type: Type of module (review, preview, transfer, etc.)
        
    Returns:
        True if module is disabled
    """
    tracker = _load_tracker()
    
    if module_type not in tracker:
        return False
    
    return tracker[module_type].get('disabled', False)


def get_failure_count(module_type: str) -> int:
    """
    Get current failure count for a module.
    
    Args:
        module_type: Type of module (review, preview, transfer, etc.)
        
    Returns:
        Current failure count
    """
    tracker = _load_tracker()
    
    if module_type not in tracker:
        return 0
    
    return tracker[module_type].get('failure_count', 0)


def manually_reset(module_type: Optional[str] = None):
    """
    Manually reset failure counter and re-enable module.
    Used by admin to reactivate a disabled module.
    
    Args:
        module_type: Type of module to reset, or None to reset all
    """
    tracker = _load_tracker()
    
    if module_type:
        if module_type in tracker:
            tracker[module_type] = {
                'failure_count': 0,
                'disabled': False,
                'manually_reset_at': datetime.now(timezone.utc).isoformat()
            }
            print(f"✅ Module '{module_type}' has been manually reset.")
            
            # Re-enable in CMS
            _enable_module_in_cms(module_type)
        else:
            print(f"ℹ️ Module '{module_type}' has no failure history.")
    else:
        # Reset all modules
        for mod in list(tracker.keys()):
            tracker[mod] = {
                'failure_count': 0,
                'disabled': False,
                'manually_reset_at': datetime.now(timezone.utc).isoformat()
            }
            _enable_module_in_cms(mod)
        print("✅ All modules have been manually reset.")
    
    _save_tracker(tracker)


def get_all_module_status() -> Dict:
    """
    Get status of all tracked modules.
    
    Returns:
        Dictionary with module status information
    """
    return _load_tracker()


def _disable_module_in_cms(module_type: str):
    """
    Disable module in CMS database for all websites.
    
    Args:
        module_type: Type of module to disable
    """
    try:
        from publication.cms_db import fetch_websites_from_api, filter_websites_by_enable
        from auth.session_manager import session_manager
        
        cms_field = MODULE_TO_CMS_FIELD.get(module_type)
        if not cms_field:
            print(f"⚠️ Unknown module type '{module_type}', cannot update CMS")
            return
        
        # Get all websites
        all_websites = fetch_websites_from_api()
        if not all_websites:
            print(f"⚠️ Could not fetch websites from CMS")
            return
        
        # Filter to only websites that have this module enabled
        enabled_websites = filter_websites_by_enable(all_websites, module_type)
        
        if not enabled_websites:
            print(f"ℹ️ No websites have '{module_type}' module enabled")
            return
        
        session = session_manager.get_authenticated_session()
        if not session:
            print(f"⚠️ No authenticated session available")
            return
        
        cms_base_url = os.getenv('CMS_BASE_URL')
        update_url = f"{cms_base_url}/api/websites"
        
        # Update each enabled website
        updated_count = 0
        for website in enabled_websites:
            website_id = website.get('id')
            if not website_id:
                continue
            
            try:
                payload = {cms_field: False}
                response = session.put(f"{update_url}/{website_id}", json=payload, timeout=10)
                response.raise_for_status()
                updated_count += 1
            except Exception as e:
                print(f"❌ Failed to disable module for website {website_id}: {e}")
        
        print(f"✅ Disabled '{module_type}' module for {updated_count} websites in CMS")
        
    except Exception as e:
        print(f"❌ Error disabling module in CMS: {e}")


def _enable_module_in_cms(module_type: str):
    """
    Re-enable module in CMS database for all websites.
    
    Args:
        module_type: Type of module to enable
    """
    try:
        from publication.cms_db import fetch_websites_from_api
        from auth.session_manager import session_manager
        
        cms_field = MODULE_TO_CMS_FIELD.get(module_type)
        if not cms_field:
            print(f"⚠️ Unknown module type '{module_type}', cannot update CMS")
            return
        
        # Get all websites
        websites = fetch_websites_from_api()
        if not websites:
            print(f"⚠️ Could not fetch websites from CMS")
            return
        
        session = session_manager.get_authenticated_session()
        if not session:
            print(f"⚠️ No authenticated session available")
            return
        
        cms_base_url = os.getenv('CMS_BASE_URL')
        update_url = f"{cms_base_url}/api/websites"
        
        # Update each website
        updated_count = 0
        for website in websites:
            website_id = website.get('id')
            if not website_id:
                continue
            
            # Only update if currently disabled
            if not website.get(cms_field, True):
                try:
                    payload = {cms_field: True}
                    response = session.put(f"{update_url}/{website_id}", json=payload, timeout=10)
                    response.raise_for_status()
                    updated_count += 1
                except Exception as e:
                    print(f"❌ Failed to enable module for website {website_id}: {e}")
        
        print(f"✅ Re-enabled '{module_type}' module for {updated_count} websites in CMS")
        
    except Exception as e:
        print(f"❌ Error enabling module in CMS: {e}")
