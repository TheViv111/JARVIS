import os
import torch
import numpy as np
import torchaudio

# Monkey-patch torchaudio for SpeechBrain 1.0.3 compatibility
if not hasattr(torchaudio, "list_audio_backends"):
    torchaudio.list_audio_backends = lambda: []

from speechbrain.inference.speaker import EncoderClassifier
from app.config import settings

# Global model instance
_SPEAKER_ENCODER = None

def _get_encoder():
    global _SPEAKER_ENCODER
    if _SPEAKER_ENCODER is None:
        # Load the pre-trained ECAPA-TDNN model from SpeechBrain
        _SPEAKER_ENCODER = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir=os.path.join(os.path.expanduser("~"), ".cache", "speechbrain", "spkrec-ecapa-voxceleb")
        )
    return _SPEAKER_ENCODER

def extract_embedding(audio_bytes: bytes) -> np.ndarray:
    """Extract a 192-dim speaker embedding from audio bytes."""
    encoder = _get_encoder()
    
    # Convert bytes to torch tensor (requires PCM 16k mono)
    # We already have utils for this
    from app.utils import wav_to_pcm_mono_16k
    pcm = wav_to_pcm_mono_16k(audio_bytes)
    audio_int16 = np.frombuffer(pcm, dtype=np.int16)
    audio_float32 = audio_int16.astype(np.float32) / 32768.0
    input_tensor = torch.from_numpy(audio_float32).unsqueeze(0) # Batch dim
    
    # Extract embedding
    with torch.no_grad():
        embedding = encoder.encode_batch(input_tensor)
        # embedding is (1, 1, 192), we want (192,)
        embedding = embedding.squeeze().cpu().numpy()
        
    return embedding

def verify_speaker(current_audio: bytes, master_embedding: np.ndarray, threshold: float = 0.85) -> tuple[bool, float]:
    """Verify if the current audio belongs to the user."""
    current_embedding = extract_embedding(current_audio)
    
    # Cosine Similarity
    # (A dot B) / (||A|| * ||B||)
    similarity = np.dot(current_embedding, master_embedding) / (
        np.linalg.norm(current_embedding) * np.linalg.norm(master_embedding)
    )
    
    return bool(similarity >= threshold), float(similarity)
