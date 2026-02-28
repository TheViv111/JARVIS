import sys
import os
import numpy as np
import base64
import io
import wave
import torch

# Add the project directory to sys.path
sys.path.append(r"C:\Users\vivaa\Documents\jarvis\services\voice-pipeline")

from app.utils import bytes_to_wav, wav_to_pcm_mono_16k

def create_dummy_wav(duration_sec=1.0, freq=440, sample_rate=16000):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # Generate a sine wave (simulating some sound)
    audio = (np.sin(freq * t * 2 * np.pi) * 32767).astype(np.int16)
    return bytes_to_wav(audio.tobytes(), sample_rate)

print("\n--- Debugging VAD ---")
try:
    from app.vad.detector import _detect_with_silero
    audio = create_dummy_wav(duration_sec=0.5, freq=440)
    pcm = wav_to_pcm_mono_16k(audio)
    res = _detect_with_silero(pcm)
    print(f"Silero Success: {res}")
except Exception as e:
    print(f"Silero Failed with error: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Debugging Wake-word ---")
try:
    from app.wakeword.engine import _get_model
    model = _get_model()
    print("openWakeWord Model loaded successfully")
    print(f"Models loaded: {list(model.models.keys())}")
    
    audio = create_dummy_wav(duration_sec=1.0)
    pcm = wav_to_pcm_mono_16k(audio)
    samples = np.frombuffer(pcm, dtype=np.int16)
    model.predict(samples)
    print("Prediction successful")
except Exception as e:
    print(f"openWakeWord Failed with error: {e}")
    import traceback
    traceback.print_exc()
