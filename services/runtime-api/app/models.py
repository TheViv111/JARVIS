from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TranscriptionRequest(BaseModel):
    audio_base64: Optional[str] = None
    language: str = "en"
    prefer_cloud: bool = True


class TranscriptionResponse(BaseModel):
    transcript: str
    provider: str
    used_fallback: bool = False


class IntelligenceRequest(BaseModel):
    input: str
    session_id: str = "default"
    context: Dict[str, Any] = Field(default_factory=dict)
    prefer_cloud: bool = True


class IntelligenceResponse(BaseModel):
    output: str
    provider: str
    used_fallback: bool = False


class FaceVerifyRequest(BaseModel):
    image_base64: Optional[str] = None
    liveness_required: bool = True
    threshold: Optional[float] = None


class FaceVerifyResponse(BaseModel):
    confidence: float
    is_verified: bool
    liveness_passed: bool
    provider: str = "local-face"


class ExecuteIntentRequest(BaseModel):
    session_id: str
    input: str = ""
    modality: str = "text"
    context: Dict[str, Any] = Field(default_factory=dict)
    audio_base64: Optional[str] = None
    image_base64: Optional[str] = None
    prefer_cloud: bool = True
    speak_response: bool = False
    tts_voice: Optional[str] = None


class ExecuteIntentResponse(BaseModel):
    run_id: str
    status: str
    plan: list[str]
    requires_approval: bool
    risk: str = "low"
    risk_reason: str = ""
    transcript: Optional[str] = None
    assistant_output: str
    trust: Optional[FaceVerifyResponse] = None
    providers: Dict[str, str] = Field(default_factory=dict)
    tts_audio_base64: Optional[str] = None
    tts_mime_type: Optional[str] = None
