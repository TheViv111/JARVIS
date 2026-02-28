import base64
import io
from typing import Tuple

import httpx

from app.config import settings


class TranscriptionError(Exception):
    pass


def _decode_audio(audio_base64: str) -> bytes:
    try:
        return base64.b64decode(audio_base64, validate=True)
    except Exception as exc:  # noqa: BLE001
        raise TranscriptionError("Invalid audio_base64 payload.") from exc


async def _transcribe_with_groq(audio: bytes, language: str) -> str:
    if not settings.groq_api_key:
        raise TranscriptionError("GROQ_API_KEY is not configured.")

    files = {
        "file": ("audio.wav", io.BytesIO(audio), "audio/wav"),
    }
    data = {
        "model": settings.groq_stt_model,
        "language": language,
    }
    headers = {"Authorization": f"Bearer {settings.groq_api_key}"}

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            f"{settings.groq_base_url}/audio/transcriptions",
            data=data,
            files=files,
            headers=headers,
        )
    response.raise_for_status()
    payload = response.json()
    text = payload.get("text", "").strip()
    if not text:
        raise TranscriptionError("Groq STT returned empty transcript.")
    return text


def _transcribe_local_faster_whisper(audio: bytes) -> str:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise TranscriptionError("faster-whisper is not installed.") from exc

    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp:
        temp.write(audio)
        temp.flush()
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _info = model.transcribe(temp.name)
        text = " ".join(segment.text.strip() for segment in segments).strip()
    if not text:
        raise TranscriptionError("Local faster-whisper returned empty transcript.")
    return text


async def transcribe(audio_base64: str, language: str = "en", prefer_cloud: bool = True) -> Tuple[str, str, bool]:
    audio = _decode_audio(audio_base64)

    if prefer_cloud:
        try:
            text = await _transcribe_with_groq(audio, language)
            return text, "groq-stt", False
        except Exception:  # noqa: BLE001
            pass

    text = _transcribe_local_faster_whisper(audio)
    return text, "faster-whisper", True

