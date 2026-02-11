"""
Global message tracker for tracking publication workflow stages.
Uses thread-safe log buffers to track messages across different stages.
Tracks 4 stages: Record Insertion, Image Generation, News Content Generation, and Publication.
"""

import threading
from typing import Dict, List, Any, Optional
from enum import Enum


class MessageStage(Enum):
    """Enum for different stages of the publication workflow."""
    RECORD_INSERTION = "record_insertion"
    IMAGE_GENERATION = "image_generation"
    IMAGE_AWS_UPLOAD = "image_aws_upload"
    IMAGE_WORDPRESS_UPLOAD = "image_wordpress_upload"
    CONTENT_GENERATION = "content_generation"
    PUBLICATION = "publication"


class MessageStatus(Enum):
    """Enum for message status."""
    SUCCESS = "success"
    ERROR = "error"


# Thread-safe global log buffers
_LOG_BUFFERS: Dict[str, List[Dict[str, Any]]] = {}
_LOG_LOCK = threading.Lock()


def add_message(
    key: str,
    stage: MessageStage,
    status: MessageStatus,
    message: str,
    error_details: Optional[str] = None
):
    """
    Add a message for a specific key and stage (thread-safe).
    
    Args:
        key: Unique identifier for the workflow (e.g., "player_id_website_id_db_id")
        stage: The stage of the workflow (MessageStage enum)
        status: Success or error status (MessageStatus enum)
        message: Human-readable message
        error_details: Optional detailed error information
    """
    with _LOG_LOCK:
        if key not in _LOG_BUFFERS:
            _LOG_BUFFERS[key] = []
        
        message_entry = {
            "stage": stage.value,
            "status": status.value,
            "message": message,
            "error_details": error_details
        }
        
        _LOG_BUFFERS[key].append(message_entry)


def get_messages(key: str) -> List[Dict]:
    """
    Get all messages for a specific key (thread-safe).
    
    Args:
        key: Unique identifier for the workflow
        
    Returns:
        List of message dictionaries
    """
    with _LOG_LOCK:
        return _LOG_BUFFERS.get(key, []).copy()


def format_messages(key: str) -> str:
    """
    Format all messages for a key into a single string for logging.
    
    Args:
        key: Unique identifier for the workflow
        
    Returns:
        Formatted message string
    """
    messages = get_messages(key)
    if not messages:
        return "No messages recorded"
    
    formatted_lines = []
    stage_names = {
        "record_insertion": "1. Record Insertion",
        "image_generation": "2. Image Generation",
        "image_aws_upload": "3. Image AWS Upload",
        "image_wordpress_upload": "4. Image WordPress Upload",
        "content_generation": "5. News Content Generation",
        "publication": "6. News Publication"
    }
    
    for msg in messages:
        stage_label = stage_names.get(msg["stage"], msg["stage"])
        status_icon = "✅" if msg["status"] == "success" else "❌"
        
        line = f"{status_icon} {stage_label}: {msg['message']}"
        if msg.get("error_details"):
            line += f" | Details: {msg['error_details']}"
        
        formatted_lines.append(line)
    
    return "\n".join(formatted_lines)


def get_messages_json(key: str) -> str:
    """
    Get all messages for a key formatted as JSON string.
    
    Args:
        key: Unique identifier for the workflow
        
    Returns:
        JSON string with status and messages
    """
    import json
    
    messages = get_messages(key)
    overall_status = get_overall_status(key)
    
    result = {
        "status": overall_status,
        "messages": messages
    }
    
    return json.dumps(result, ensure_ascii=False)



def get_overall_status(key: str) -> str:
    """
    Get the overall status based on all messages.
    
    Args:
        key: Unique identifier for the workflow
        
    Returns:
        Overall status string ("published", "failed", "partial")
    """
    messages = get_messages(key)
    if not messages:
        return "Failed"
    
    has_error = any(msg["status"] == "error" for msg in messages)
    publication_msgs = [m for m in messages if m["stage"] == "publication"]
    # Check if publication stage failed
    if publication_msgs and publication_msgs[-1]["status"] == "success":
        return "Partial" if has_error else "Published"
    else:
        return "Failed"
    

def was_image_generated(key: str) -> bool:
    """
    Check if image was successfully generated for a key.
    
    Args:
        key: Unique identifier for the workflow
        
    Returns:
        True if image was generated successfully
    """
    messages = get_messages(key)
    image_msgs = [m for m in messages if m["stage"] == "image_generation"]
    
    if image_msgs:
        return image_msgs[-1]["status"] == "success"
    
    return False


def clear_messages(key: str):
    """
    Clear all messages for a specific key (thread-safe).
    
    Args:
        key: Unique identifier for the workflow
    """
    with _LOG_LOCK:
        if key in _LOG_BUFFERS:
            del _LOG_BUFFERS[key]


def clear_all():
    """Clear all messages (thread-safe)."""
    with _LOG_LOCK:
        _LOG_BUFFERS.clear()
