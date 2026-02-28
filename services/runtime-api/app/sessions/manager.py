import json
import redis
from typing import List, Dict, Any
from app.config import settings

# Redis connection
_REDIS_CLIENT = None

def _get_redis():
    global _REDIS_CLIENT
    if _REDIS_CLIENT is None:
        _REDIS_CLIENT = redis.from_url(settings.redis_url, decode_responses=True)
    return _REDIS_CLIENT

def save_message(session_id: str, role: str, content: str):
    """Save a message to the session's history in Redis."""
    r = _get_redis()
    key = f"session:{session_id}:history"
    
    # Store as a list of JSON objects
    message = json.dumps({"role": role, "content": content})
    r.rpush(key, message)
    
    # Set expiration
    r.expire(key, settings.session_ttl)
    
    # Keep only the last 20 messages for speed
    r.ltrim(key, -20, -1)

def get_history(session_id: str) -> List[Dict[str, str]]:
    """Retrieve the conversation history for a session."""
    r = _get_redis()
    key = f"session:{session_id}:history"
    
    history_raw = r.lrange(key, 0, -1)
    history = [json.loads(m) for m in history_raw]
    
    return history

def clear_session(session_id: str):
    """Clear the history for a session."""
    r = _get_redis()
    key = f"session:{session_id}:history"
    r.delete(key)
