import base64
from typing import Tuple

from app.config import settings


class FaceTrustError(Exception):
    pass


def _decode_image(image_base64: str) -> bytes:
    try:
        return base64.b64decode(image_base64, validate=True)
    except Exception as exc:  # noqa: BLE001
        raise FaceTrustError("Invalid image_base64 payload.") from exc


def evaluate_face_trust(
    image_base64: str | None,
    liveness_required: bool = True,
    threshold: float | None = None,
) -> Tuple[float, bool, bool]:
    if not image_base64:
        return 0.0, False, not liveness_required

    image_bytes = _decode_image(image_base64)
    if not image_bytes:
        return 0.0, False, False

    # Placeholder local estimator for Phase 1. Replace with production model in Phase 6.
    confidence = min(0.99, 0.55 + (len(image_bytes) % 45) / 100)
    liveness_passed = True if not liveness_required else len(image_bytes) > 1024
    effective_threshold = threshold if threshold is not None else settings.face_trust_threshold

    verified = liveness_passed and confidence >= effective_threshold
    return confidence, verified, liveness_passed

