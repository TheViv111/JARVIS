import io
import tempfile

import httpx

from app.config import settings


class SttError(Exception):
    pass


async def _transcribe_groq(audio_bytes: bytes, language: str) -> str:
    if not settings.groq_api_key:
        raise SttError("GROQ_API_KEY is not set.")

    headers = {"Authorization": f"Bearer {settings.groq_api_key}"}
    files = {"file": ("audio.wav", io.BytesIO(audio_bytes), "audio/wav")}
    data = {"model": settings.groq_stt_model, "language": language}

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            f"{settings.groq_base_url}/audio/transcriptions",
            headers=headers,
            files=files,
            data=data,
        )
    response.raise_for_status()
    payload = response.json()
    text = payload.get("text", "").strip()
    if not text:
        raise SttError("Groq STT returned empty transcript.")
    return text


def _transcribe_local(audio_bytes: bytes) -> str:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise SttError("faster-whisper is not installed.") from exc

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp:
        temp.write(audio_bytes)
        temp.flush()
        model = WhisperModel(settings.stt_local_model, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(temp.name)
        text = " ".join(seg.text.strip() for seg in segments).strip()
    if not text:
        raise SttError("Local STT returned empty transcript.")
    return text


async def transcribe(audio_bytes: bytes, language: str = "en", prefer_cloud: bool = True) -> tuple[str, str, bool]:
    if prefer_cloud:
        try:
            return await _transcribe_groq(audio_bytes, language), "groq-stt", False
        except Exception:
            pass
    return _transcribe_local(audio_bytes), "faster-whisper", True

