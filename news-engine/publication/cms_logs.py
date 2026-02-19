import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Union

import requests

from auth.auth_manager import auth_manager
from auth.session_manager import session_manager


CMS_NEWS_LOG_URL = (
    f"{os.getenv('CMS_BASE_URL')}/api/news-logs"
)


def insert_news_log(
    news_type: str,
    news_title: str,
    website_name: str,
    image_generated: bool,
    news_status: str,
    message: Optional[Union[str, Dict]] = None,
    log_time: Optional[str] = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Insert a news log entry into the CMS so every module can reuse it.

    Args:
        news_type: Module or news type (e.g. transfer, preview, review).
        news_title: Title of the news article.
        website_name: Name of the website where news was published.
        image_generated: Whether an image was generated.
        news_status: Status indicator (Published, Failed, Partial, Unknown, etc.).
        message: JSON string or dict containing status and messages array.
        log_time: ISO-formatted timestamp. Defaults to current UTC time.
        extra_fields: Additional CMS fields to include in the payload.

    Returns:
        bool: True if the log was created successfully, False otherwise.
    """
    try:
        if not CMS_NEWS_LOG_URL:
            print("⚠️ CMS_BASE_URL is not configured; cannot create news log.")
            return False

        # if not auth_manager.ensure_authenticated():
        #     print("⚠️ Unable to authenticate with CMS; skipping news log creation.")
        #     return False

        session = session_manager.get_authenticated_session()
        if not session:
            print("⚠️ CMS session unavailable; skipping news log creation.")
            return False

        # Format datetime (ISO 8601 with 'Z' suffix)
        if log_time:
            formatted_time = log_time
        else:
            formatted_time = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        
        # Parse message if it's a JSON string
        message_data = None
        if message:
            if isinstance(message, str):
                try:
                    message_data = json.loads(message)
                except json.JSONDecodeError:
                    # If it's not valid JSON, treat it as a plain string
                    message_data = {"status": news_status, "messages": [{"message": message}]}
            elif isinstance(message, dict):
                message_data = message
        
        payload = {
            "news_type": news_type,
            "title": news_title,
            "website_name": website_name,
            "image_generated": image_generated,
            "log_message": message_data,  # Send as JSON object
            "news_status": news_status,
            "log_time": formatted_time,
        }

        if extra_fields:
            payload.update(extra_fields)

        # print(f"📤 Sending payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

        response = session.post(CMS_NEWS_LOG_URL, json=payload, timeout=20)
        response.raise_for_status()
        # Log response details for debugging
        print(f"📥 Response status: {response.status_code}")
        return True
        
    except requests.exceptions.RequestException as exc:
        print(f"❌ Failed to create news log: {exc}")
    except Exception as exc:
        print(f"❌ Unexpected error while creating news log: {exc}")

    return False

