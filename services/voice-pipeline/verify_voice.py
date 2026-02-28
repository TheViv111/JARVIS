import sys
import os
import numpy as np
import base64
import io
import wave

# Add the project directory to sys.path
sys.path.append(r"C:\Users\vivaa\Documents\jarvis\services\voice-pipeline")

from app.utils import bytes_to_wav

def create_dummy_wav(duration_sec=1.0, freq=440, sample_rate=16000):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # Generate a sine wave (simulating some sound)
    audio = (np.sin(freq * t * 2 * np.pi) * 32767).astype(np.int16)
    return bytes_to_wav(audio.tobytes(), sample_rate)

print("\n--- Testing Imports ---")
try:
    import torch
    print(f"Torch version: {torch.__version__}")
except Exception as e:
    print(f"Torch import failed: {e}")

try:
    import openwakeword
    print(f"openwakeword imported")
except Exception as e:
    print(f"openwakeword import failed: {e}")

try:
    import silero_vad
    print(f"silero_vad imported")
except Exception as e:
    print(f"silero_vad import failed: {e}")

from app.vad.detector import detect_speech
from app.wakeword.engine import detect_wakeword

def test_vad():
    print("\n--- Testing VAD ---")
    silent_audio = create_dummy_wav(duration_sec=0.5, freq=0)
    detected, prob, provider, fallback = detect_speech(silent_audio)
    print(f"Silent Audio: Detected={detected}, Prob={prob:.4f}, Provider={provider}, Fallback={fallback}")
    
    sound_audio = create_dummy_wav(duration_sec=0.5, freq=440)
    detected, prob, provider, fallback = detect_speech(sound_audio)
    print(f"Sine Wave: Detected={detected}, Prob={prob:.4f}, Provider={provider}, Fallback={fallback}")

def test_wakeword():
    print("\n--- Testing Wake-word ---")
    dummy_audio = create_dummy_wav(duration_sec=1.0)
    detected, score, threshold, provider = detect_wakeword(dummy_audio)
    print(f"Dummy Audio: Detected={detected}, Score={score:.4f}, Threshold={threshold}, Provider={provider}")

if __name__ == "__main__":
    test_vad()
    test_wakeword()
