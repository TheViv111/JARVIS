import sys

from fastapi import APIRouter, HTTPException

from app.models import (
    SttRequest,
    SttResponse,
    TtsRequest,
    TtsResponse,
    VadRequest,
    VadResponse,
    WakewordRequest,
    WakewordResponse,
)
from app.stt.transcriber import transcribe
from app.tts.synth import synthesize
from app.utils import decode_base64_audio, encode_base64_audio
from app.vad.detector import detect_speech
from app.wakeword.engine import detect_wakeword

router = APIRouter(prefix="/v1", tags=["voice"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/wakeword/detect", response_model=WakewordResponse)
async def wakeword_detect(payload: WakewordRequest) -> WakewordResponse:
    try:
        audio_bytes = decode_base64_audio(payload.audio_base64)
        detected, score, threshold, provider = detect_wakeword(audio_bytes, payload.threshold)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Wakeword detection failed: {exc}") from exc
    return WakewordResponse(detected=detected, score=score, threshold=threshold, provider=provider)


@router.post("/vad/detect", response_model=VadResponse)
async def vad_detect(payload: VadRequest) -> VadResponse:
    try:
        audio_bytes = decode_base64_audio(payload.audio_base64)
        speech_detected, speech_ratio, provider, used_fallback = detect_speech(
            audio_bytes=audio_bytes,
            frame_ms=payload.frame_ms,
            aggressiveness=payload.aggressiveness,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"VAD failed: {exc}") from exc
    return VadResponse(
        speech_detected=speech_detected,
        speech_ratio=speech_ratio,
        provider=provider,
        used_fallback=used_fallback,
    )


@router.post("/stt/transcribe", response_model=SttResponse)
async def stt_transcribe(payload: SttRequest) -> SttResponse:
    try:
        audio_bytes = decode_base64_audio(payload.audio_base64)
        text, provider, used_fallback = await transcribe(
            audio_bytes=audio_bytes,
            language=payload.language,
            prefer_cloud=payload.prefer_cloud,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"STT failed: {exc}") from exc
    return SttResponse(transcript=text, provider=provider, used_fallback=used_fallback)


@router.post("/tts/speak", response_model=TtsResponse)
async def tts_speak(payload: TtsRequest) -> TtsResponse:
    try:
        audio_bytes, provider, used_fallback = await synthesize(
            text=payload.text,
            voice=payload.voice,
            prefer_cloud=payload.prefer_cloud,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"TTS error: {exc}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"TTS failed: {exc}") from exc

    mime_type = "audio/mpeg" if provider == "edge-tts" else "audio/wav"
    return TtsResponse(
        audio_base64=encode_base64_audio(audio_bytes),
        mime_type=mime_type,
        provider=provider,
        used_fallback=used_fallback,
    )

