import httpx

from app.config import settings


class VoiceClientError(Exception):
    pass


async def transcribe_with_voice_pipeline(
    audio_base64: str,
    language: str = "en",
    prefer_cloud: bool = True,
) -> tuple[str, str]:
    payload = {
        "audio_base64": audio_base64,
        "language": language,
        "prefer_cloud": prefer_cloud,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.voice_pipeline_url}/v1/stt/transcribe",
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    text = (data.get("transcript") or "").strip()
    if not text:
        raise VoiceClientError("Voice pipeline returned empty transcript.")
    provider = data.get("provider", "voice-pipeline-stt")
    return text, provider


async def synthesize_with_voice_pipeline(
    text: str,
    prefer_cloud: bool = True,
    voice: str | None = None,
) -> tuple[str, str, str]:
    payload = {"text": text, "prefer_cloud": prefer_cloud}
    if voice:
        payload["voice"] = voice

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.voice_pipeline_url}/v1/tts/speak",
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    audio_base64 = data.get("audio_base64")
    if not audio_base64:
        raise VoiceClientError("Voice pipeline returned empty audio.")
    provider = data.get("provider", "voice-pipeline-tts")
    mime_type = data.get("mime_type", "audio/wav")
    return audio_base64, provider, mime_type

