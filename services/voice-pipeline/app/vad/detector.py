import numpy as np
import torch

from app.config import settings
from app.utils import pcm_frame_size, wav_to_pcm_mono_16k

# Global VAD model instance
_SILERO_MODEL = None
_SILERO_UTILS = None


def _get_silero():
    global _SILERO_MODEL, _SILERO_UTILS
    if _SILERO_MODEL is None:
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                    model='silero_vad',
                                    force_reload=False,
                                    onnx=False)
        _SILERO_MODEL = model
        _SILERO_UTILS = utils
    return _SILERO_MODEL, _SILERO_UTILS


def _detect_with_silero(pcm: bytes) -> tuple[bool, float]:
    model, utils = _get_silero()
    
    # Convert bytes to torch tensor
    audio_int16 = np.frombuffer(pcm, dtype=np.int16)
    audio_float32 = audio_int16.astype(np.float32) / 32768.0
    
    # Silero VAD expects chunks of 512 samples for 16kHz
    chunk_size = 512
    probs = []
    
    # Process in chunks and collect probabilities
    for i in range(0, len(audio_float32) - chunk_size + 1, chunk_size):
        chunk = audio_float32[i : i + chunk_size]
        input_tensor = torch.from_numpy(chunk)
        speech_prob = model(input_tensor, 16000).item()
        probs.append(speech_prob)
    
    if not probs:
        # If audio is shorter than 512 samples, pad it
        padding = np.zeros(chunk_size - len(audio_float32), dtype=np.float32)
        chunk = np.concatenate([audio_float32, padding])
        input_tensor = torch.from_numpy(chunk)
        speech_prob = model(input_tensor, 16000).item()
        probs.append(speech_prob)
        
    max_prob = max(probs)
    return max_prob > 0.5, max_prob


def _detect_with_webrtc(pcm: bytes, frame_ms: int, aggressiveness: int) -> tuple[bool, float]:
    import webrtcvad  # type: ignore

    vad = webrtcvad.Vad(max(0, min(3, aggressiveness)))
    frame_size = pcm_frame_size(frame_ms=frame_ms)
    if frame_size <= 0:
        return False, 0.0

    total = 0
    speech = 0
    for i in range(0, len(pcm) - frame_size + 1, frame_size):
        frame = pcm[i : i + frame_size]
        total += 1
        if vad.is_speech(frame, 16000):
            speech += 1

    if total == 0:
        return False, 0.0
    ratio = speech / total
    return ratio > 0.2, ratio


def _detect_with_energy(pcm: bytes) -> tuple[bool, float]:
    samples = np.frombuffer(pcm, dtype=np.int16) if pcm else np.array([], dtype=np.int16)
    energy = float(np.sqrt(np.mean(np.square(samples, dtype=np.float64)))) if samples.size else 0.0
    ratio = min(1.0, energy / max(1, settings.vad_energy_threshold * 10))
    return energy >= settings.vad_energy_threshold, ratio


def detect_speech(audio_bytes: bytes, frame_ms: int = 30, aggressiveness: int = 2) -> tuple[bool, float, str, bool]:
    pcm = wav_to_pcm_mono_16k(audio_bytes)

    if settings.vad_primary.lower() == "silero":
        try:
            detected, prob = _detect_with_silero(pcm)
            return detected, prob, "silero", False
        except Exception:
            pass

    try:
        detected, ratio = _detect_with_webrtc(pcm, frame_ms, aggressiveness)
        return detected, ratio, "webrtc", True
    except Exception:
        detected, ratio = _detect_with_energy(pcm)
        return detected, ratio, "energy", True
