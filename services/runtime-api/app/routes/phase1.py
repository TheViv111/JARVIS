from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models import (
    ExecuteIntentRequest,
    ExecuteIntentResponse,
    FaceVerifyRequest,
    FaceVerifyResponse,
    IntelligenceRequest,
    IntelligenceResponse,
    TranscriptionRequest,
    TranscriptionResponse,
)
from app.orchestrator.face_trust import evaluate_face_trust
from app.orchestrator.intelligence import generate_reply
from app.orchestrator.transcription import transcribe
from app.orchestrator.voice_client import synthesize_with_voice_pipeline, transcribe_with_voice_pipeline
from app.policy.risk import evaluate_risk

router = APIRouter(prefix="/v1", tags=["phase1"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/transcription/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(payload: TranscriptionRequest) -> TranscriptionResponse:
    if not payload.audio_base64:
        raise HTTPException(status_code=400, detail="audio_base64 is required.")

    try:
        text, provider, used_fallback = await transcribe(
            audio_base64=payload.audio_base64,
            language=payload.language,
            prefer_cloud=payload.prefer_cloud,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Transcription failed: {exc}") from exc

    return TranscriptionResponse(transcript=text, provider=provider, used_fallback=used_fallback)


@router.post("/intelligence/respond", response_model=IntelligenceResponse)
async def intelligence_respond(payload: IntelligenceRequest) -> IntelligenceResponse:
    try:
        output, provider, used_fallback = await generate_reply(
            user_input=payload.input,
            session_id=payload.session_id,
            context=payload.context,
            prefer_cloud=payload.prefer_cloud,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Intelligence failed: {exc}") from exc

    return IntelligenceResponse(output=output, provider=provider, used_fallback=used_fallback)


@router.post("/face/verify", response_model=FaceVerifyResponse)
async def face_verify(payload: FaceVerifyRequest) -> FaceVerifyResponse:
    confidence, is_verified, liveness_passed = evaluate_face_trust(
        image_base64=payload.image_base64,
        liveness_required=payload.liveness_required,
        threshold=payload.threshold,
    )
    return FaceVerifyResponse(
        confidence=confidence,
        is_verified=is_verified,
        liveness_passed=liveness_passed,
    )


@router.post("/intent/execute", response_model=ExecuteIntentResponse)
async def execute_intent(payload: ExecuteIntentRequest) -> ExecuteIntentResponse:
    run_id = f"run_{uuid4().hex[:10]}"
    transcript = None
    stt_provider = "none"
    trust = None

    user_input = payload.input.strip()
    if payload.modality.lower() == "voice":
        if payload.audio_base64:
            try:
                transcript, stt_provider = await transcribe_with_voice_pipeline(
                    audio_base64=payload.audio_base64,
                    language="en",
                    prefer_cloud=payload.prefer_cloud,
                )
                user_input = transcript
            except Exception:
                try:
                    transcript, stt_provider, _stt_fallback = await transcribe(
                        payload.audio_base64,
                        language="en",
                        prefer_cloud=payload.prefer_cloud,
                    )
                    user_input = transcript
                except Exception as exc:  # noqa: BLE001
                    raise HTTPException(status_code=500, detail=f"Voice transcription failed: {exc}") from exc
        elif not user_input:
            raise HTTPException(status_code=400, detail="Provide input text or audio_base64 for voice modality.")

    if payload.image_base64:
        confidence, is_verified, liveness_passed = evaluate_face_trust(
            image_base64=payload.image_base64,
            liveness_required=True,
            threshold=None,
        )
        trust = FaceVerifyResponse(
            confidence=confidence,
            is_verified=is_verified,
            liveness_passed=liveness_passed,
        )

    try:
        assistant_output, llm_provider, _llm_fallback = await generate_reply(
            user_input=user_input,
            session_id=payload.session_id,
            context=payload.context,
            prefer_cloud=payload.prefer_cloud,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Intelligence failed: {exc}") from exc

    risk_decision = evaluate_risk(user_input)
    plan = ["interpret_intent", "evaluate_risk", "decide_action", "prepare_response"]
    requires_approval = risk_decision.requires_approval
    tts_audio_base64 = None
    tts_mime_type = None
    tts_provider = "none"

    if payload.speak_response:
        try:
            tts_audio_base64, tts_provider, tts_mime_type = await synthesize_with_voice_pipeline(
                text=assistant_output,
                prefer_cloud=payload.prefer_cloud,
                voice=payload.tts_voice,
            )
        except Exception:
            tts_provider = "tts_unavailable"

    return ExecuteIntentResponse(
        run_id=run_id,
        status="in_progress",
        plan=plan,
        requires_approval=requires_approval,
        risk=risk_decision.risk,
        risk_reason=risk_decision.reason,
        transcript=transcript,
        assistant_output=assistant_output,
        trust=trust,
        providers={"stt": stt_provider, "llm": llm_provider, "face": "local-face", "tts": tts_provider},
        tts_audio_base64=tts_audio_base64,
        tts_mime_type=tts_mime_type,
    )
