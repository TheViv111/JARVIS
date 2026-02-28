import os
import sys
import numpy as np
import sounddevice as sd
import wave
import io
import time

# Add the project directory to sys.path
sys.path.append(r"C:\Users\vivaa\Documents\jarvis\services\voice-pipeline")

from app.biometrics.speaker_id import extract_embedding

def record_audio(duration=3, sample_rate=16000):
    print(f"Recording for {duration} seconds... speak now.")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording stopped.")
    
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(recording.tobytes())
    return buffer.getvalue()

def enroll():
    print("=== JARVIS Speaker Enrollment ===")
    print("We will record your voice 3 times to create a robust fingerprint.")
    
    embeddings = []
    for i in range(3):
        input(f"
Press Enter to start recording #{i+1}...")
        audio = record_audio()
        print("Extracting embedding...")
        try:
            emb = extract_embedding(audio)
            embeddings.append(emb)
            print(f"Embedding #{i+1} captured.")
        except Exception as e:
            print(f"Error: {e}")
            return

    # Average the embeddings
    master_embedding = np.mean(embeddings, axis=0)
    
    # Save to assets
    target_path = r"C:\Users\vivaa\Documents\jarvis\assets\biometrics\vivaa_voice_master.npy"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    np.save(target_path, master_embedding)
    
    print(f"
SUCCESS! Voice fingerprint saved to {target_path}")
    print("JARVIS now knows your voice.")

if __name__ == "__main__":
    enroll()
