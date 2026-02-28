import os
import numpy as np
import openwakeword
from openwakeword.model import Model

from app.config import settings
from app.utils import wav_to_pcm_mono_16k

# Global model instance
_OWW_MODEL = None

def _get_model():
    global _OWW_MODEL
    if _OWW_MODEL is None:
        # Load the local "hey_jarvis" model downloaded to assets
        local_model_path = r"C:\Users\vivaa\Documents\jarvis\assets\models\hey_jarvis_v0.1.onnx"
        if os.path.exists(local_model_path):
            _OWW_MODEL = Model(wakeword_models=[local_model_path], inference_framework="onnx")
        else:
            # Fallback to default search if local file missing
            model_paths = [settings.wakeword_model_path] if settings.wakeword_model_path else ["hey_jarvis"]
            _OWW_MODEL = Model(wakeword_models=model_paths)
    return _OWW_MODEL

def detect_wakeword(audio_bytes: bytes, threshold: float | None = None) -> tuple[bool, float, float, str]:
    effective_threshold = threshold if threshold is not None else settings.wakeword_threshold

    try:
        model = _get_model()
        provider = "openwakeword"
        
        pcm = wav_to_pcm_mono_16k(audio_bytes)
        samples = np.frombuffer(pcm, dtype=np.int16)
        
        # openwakeword processes in chunks. We'll pass the whole buffer and it'll chunk internally.
        model.predict(samples)
        
        # Get the latest score for the first model loaded
        wakeword_name = list(model.models.keys())[0]
        # Check if we have anything in the prediction buffer
        if model.prediction_buffer[wakeword_name]:
            score = float(model.prediction_buffer[wakeword_name][-1])
        else:
            score = 0.0
        detected = score >= effective_threshold
        
    except Exception as e:
        # In a real environment, you'd log this: print(f"Wake-word failed: {e}")
        provider = "energy-heuristic"
        pcm = wav_to_pcm_mono_16k(audio_bytes)
        samples = np.frombuffer(pcm, dtype=np.int16) if pcm else np.array([], dtype=np.int16)
        energy = float(np.sqrt(np.mean(np.square(samples, dtype=np.float64)))) if samples.size else 0.0
        score = min(0.99, energy / 6000.0)
        detected = score >= effective_threshold

    return detected, float(score), float(effective_threshold), provider
