import json
import logging
import re
from typing import Any, Dict, List, Tuple

import httpx

from app.config import settings
from app.sessions.manager import get_history, save_message


class IntelligenceError(Exception):
    pass


logger = logging.getLogger(__name__)


def _summarize_exception(exc: Exception) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code if exc.response is not None else "unknown"
        body = (exc.response.text or "").strip() if exc.response is not None else ""
        if len(body) > 240:
            body = body[:240] + "..."
        return f"HTTP {status} - {body}"
    return str(exc)


def _sanitize_output(user_input: str, output: str) -> str:
    """
    Prevent high-impact hallucinations about security incidents or privilege
    escalation when no verified security telemetry is integrated in this flow.
    """
    text = (output or "").strip()
    if not text:
        return text

    suspicious_patterns = [
        r"\bsecurity breach\b",
        r"\bbreach detected\b",
        r"\bescalat(e|ing|ion)\b.{0,40}\bprivilege",
        r"\brequesting authorization\b.{0,40}\bescalat(e|ion)",
        r"\broot access\b",
        r"\badmin access\b",
    ]
    if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in suspicious_patterns):
        return (
            "I cannot confirm a real security incident from current runtime data. "
            "No verified security telemetry is connected to this chat path yet. "
            "If you want, I can help run explicit checks and report factual results."
        )

    return text


async def _chat_groq(messages: List[Dict[str, str]]) -> str:
    if not settings.groq_api_key:
        raise IntelligenceError("GROQ_API_KEY is not configured.")

    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    
    # Prepend system prompt
    full_messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS. Be concise, safe, and action-oriented. "
                "Do not claim security incidents, breaches, or privilege escalation "
                "unless explicitly supported by verified tool/telemetry results."
            ),
        }
    ] + messages

    payload = {
        "model": settings.groq_model,
        "messages": full_messages,
        "temperature": 0.2,
        "max_tokens": 512, # Increased for longer conversations
    }

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            f"{settings.groq_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    if not content:
        raise IntelligenceError("Groq returned empty response.")
    return content


async def _chat_ollama(messages: List[Dict[str, str]]) -> str:
    # Prepend system prompt
    full_messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS. Be concise and precise. "
                "Do not invent operational alerts. "
                "Do not claim security breaches or privilege escalation unless "
                "you have verified tool/telemetry evidence."
            ),
        }
    ] + messages

    payload = {
        "model": settings.ollama_model,
        "messages": full_messages,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": 0.2,
            "num_predict": 128,
        },
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    content = data.get("message", {}).get("content", "").strip()
    if not content:
        raise IntelligenceError("Ollama returned empty response.")
    return content


async def generate_reply(
    user_input: str, 
    session_id: str = "default", 
    context: Dict[str, Any] = None, 
    prefer_cloud: bool = True
) -> Tuple[str, str, bool]:
    
    # 1. Retrieve history
    history = get_history(session_id)
    
    # 2. Add current user input to history (ephemeral for now)
    current_messages = history + [{"role": "user", "content": user_input}]
    
    # If context is provided (e.g. from screen OCR), inject it into the latest message
    if context:
        context_str = f"\n\nContext: {json.dumps(context)}"
        current_messages[-1]["content"] += context_str

    # 3. Call LLM
    try:
        if prefer_cloud and settings.llm_provider.lower() == "groq":
            output = await _chat_groq(current_messages)
            provider = "groq"
            fallback = False
        else:
            output = await _chat_ollama(current_messages)
            provider = "ollama"
            fallback = True
    except Exception as primary_exc:
        logger.warning(
            "Primary LLM path failed. provider=%s reason=%s",
            settings.llm_provider.lower(),
            _summarize_exception(primary_exc),
        )
        # Fallback to Ollama if Groq fails
        try:
            output = await _chat_ollama(current_messages)
            provider = "ollama"
            fallback = True
            logger.info("LLM fallback succeeded via Ollama.")
        except Exception as fallback_exc:
            logger.error(
                "LLM fallback failed. reason=%s",
                _summarize_exception(fallback_exc),
            )
            degraded = (
                "No LLM backend available. Start Ollama or set GROQ_API_KEY. "
                f"Request captured: {user_input}"
            )
            return degraded, "degraded", True

    # 4. Save to Redis
    save_message(session_id, "user", user_input)
    save_message(session_id, "assistant", output)
    
    output = _sanitize_output(user_input, output)
    return output, provider, fallback
