import base64
import io
import wave
import numpy as np


def decode_base64_audio(audio_base64: str) -> bytes:
    return base64.b64decode(audio_base64, validate=True)


def encode_base64_audio(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode("utf-8")


def wav_to_pcm_mono_16k(audio_bytes: bytes) -> bytes:
    with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())

    if sample_width == 1:
        audio = np.frombuffer(frames, dtype=np.uint8).astype(np.int16)
        audio = (audio - 128) << 8
    elif sample_width == 2:
        audio = np.frombuffer(frames, dtype=np.int16)
    elif sample_width == 4:
        audio32 = np.frombuffer(frames, dtype=np.int32)
        audio = (audio32 >> 16).astype(np.int16)
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")

    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1).astype(np.int16)

    if sample_rate != 16000 and len(audio) > 0:
        duration = len(audio) / sample_rate
        old_x = np.linspace(0, duration, num=len(audio), endpoint=False)
        new_len = int(duration * 16000)
        new_x = np.linspace(0, duration, num=max(new_len, 1), endpoint=False)
        audio = np.interp(new_x, old_x, audio).astype(np.int16)

    return audio.tobytes()


def pcm_frame_size(frame_ms: int, sample_rate: int = 16000, sample_width: int = 2, channels: int = 1) -> int:
    return int(sample_rate * frame_ms / 1000) * sample_width * channels


def bytes_to_wav(audio_pcm: bytes, sample_rate: int = 16000) -> bytes:
    buff = io.BytesIO()
    with wave.open(buff, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_pcm)
    return buff.getvalue()
