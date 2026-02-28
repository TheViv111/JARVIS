from typing import Optional

from pydantic import BaseModel, Field


class AudioPayload(BaseModel):
    audio_base64: str
    sample_rate: int = 16000


class WakewordRequest(AudioPayload):
    threshold: Optional[float] = None


class WakewordResponse(BaseModel):
    detected: bool
    score: float
    threshold: float
    provider: str


class VadRequest(AudioPayload):
    frame_ms: int = 30
    aggressiveness: int = 2


class VadResponse(BaseModel):
    speech_detected: bool
    speech_ratio: float
    provider: str
    used_fallback: bool = False


class SttRequest(AudioPayload):
    language: str = "en"
    prefer_cloud: bool = True


class SttResponse(BaseModel):
    transcript: str
    provider: str
    used_fallback: bool = False


class TtsRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    voice: Optional[str] = None
    prefer_cloud: bool = True


class TtsResponse(BaseModel):
    audio_base64: str
    mime_type: str = "audio/wav"
    provider: str
    used_fallback: bool = False

