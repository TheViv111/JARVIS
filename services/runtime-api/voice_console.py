import base64
import difflib
import io
import json
import os
import site
import sys
import time
import urllib.error
import urllib.request
import wave
from glob import glob
from pathlib import Path

import numpy as np
import sounddevice as sd


RUNTIME_URL = "http://127.0.0.1:7777"
VOICE_URL = "http://127.0.0.1:7788"
WAKEWORD = "jarvis"
WAKEWORD_ALIASES = {"jarvis", "jervis", "jarviss", "jarves", "jarv", "jarviz"}
SAMPLE_RATE = 16000
CHUNK_SECONDS = 0.8
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_SECONDS)
SILENCE_LIMIT = 2
MAX_LISTEN_CHUNKS = 12
NO_SPEECH_START_LIMIT = 3
MIN_RMS_FOR_SPEECH = 260.0
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OWW_MODEL_NAME = os.getenv("WAKEWORD_MODEL", "hey_jarvis")
OWW_THRESHOLD = float(os.getenv("WAKEWORD_THRESHOLD", "0.20"))
OWW_DEBOUNCE_SECONDS = float(os.getenv("WAKEWORD_DEBOUNCE_SECONDS", "1.0"))
VERBOSE = True
DEBUG_WAKE = True


def _post_json(base_url: str, path: str, payload: dict, timeout: int = 90) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _is_up(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            return resp.status == 200
    except Exception:  # noqa: BLE001
        return False


def _set_orb_state(orb_state: str, visible: bool = True) -> None:
    """Notify the orb of JARVIS state (listening, processing, speaking, error, idle)."""
    try:
        _post_json(RUNTIME_URL, "/v1/orb/state", {"orb_state": orb_state, "visible": visible}, timeout=5)
    except Exception:  # noqa: BLE001
        pass


def _record_chunk() -> np.ndarray:
    audio = sd.rec(CHUNK_SAMPLES, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    return audio.reshape(-1)


def _pcm_to_wav_bytes(pcm: np.ndarray) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    return buf.getvalue()


def _audio_b64_from_pcm(pcm: np.ndarray) -> str:
    wav_bytes = _pcm_to_wav_bytes(pcm)
    return base64.b64encode(wav_bytes).decode("utf-8")


def _save_tts(audio_b64: str, mime_type: str) -> str:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ext = ".mp3" if mime_type == "audio/mpeg" else ".wav"
    path = OUTPUT_DIR / f"jarvis_voice_reply_{int(time.time() * 1000)}{ext}"
    path.write_bytes(base64.b64decode(audio_b64))
    return str(path)


def _stt_chunk(audio_b64: str) -> tuple[str, str]:
    payload = {"audio_base64": audio_b64, "language": "en", "prefer_cloud": True}
    data = _post_json(VOICE_URL, "/v1/stt/transcribe", payload, timeout=60)
    return data.get("transcript", "").strip(), data.get("provider", "unknown")


def _vad_chunk(audio_b64: str) -> bool:
    payload = {"audio_base64": audio_b64, "frame_ms": 30, "aggressiveness": 2}
    data = _post_json(VOICE_URL, "/v1/vad/detect", payload, timeout=20)
    return bool(data.get("speech_detected", False))


def _run_jarvis_intent(text: str) -> dict:
    payload = {
        "session_id": f"voice_{int(time.time())}",
        "input": text,
        "modality": "text",
        "prefer_cloud": True,
        "speak_response": True,
        "context": {"source": "voice_console"},
    }
    return _post_json(RUNTIME_URL, "/v1/intent/execute", payload, timeout=120)


def _init_openwakeword():
    try:
        import openwakeword  # type: ignore
        from openwakeword.model import Model  # type: ignore

        # Prefer installed model names first.
        try:
            model = Model(
                wakeword_models=[OWW_MODEL_NAME],
                inference_framework="onnx",
            )
            return model
        except Exception:
            pass

        # Fallback: locate an existing ONNX model file across Python installs.
        candidates: list[str] = []

        try:
            candidates.extend(openwakeword.get_pretrained_model_paths("onnx"))
        except Exception:
            pass

        roots = [sys.prefix]
        try:
            roots.extend(site.getsitepackages())
        except Exception:
            pass
        try:
            user_site = site.getusersitepackages()
            if user_site:
                roots.append(user_site)
        except Exception:
            pass
        roots.append(str(Path.home()))

        patterns = [
            "**/openwakeword/resources/models/hey_jarvis_v0.1.onnx",
            "**/openwakeword/resources/models/*jarvis*.onnx",
        ]
        for root in roots:
            for pattern in patterns:
                try:
                    candidates.extend(glob(str(Path(root) / pattern), recursive=True))
                except Exception:
                    pass

        existing = [p for p in candidates if os.path.exists(p)]
        if not existing:
            raise RuntimeError("Could not find an existing hey_jarvis ONNX model file.")

        selected = existing[0]
        model = Model(wakeword_models=[selected], inference_framework="onnx")
        return model
    except Exception as exc:  # noqa: BLE001
        print(f"Wakeword engine fallback to STT matching (openwakeword unavailable: {exc})")
        return None


OWW_CHUNK = 1280  # 80ms at 16kHz - openWakeWord's recommended streaming size


def _openwakeword_detect(model, pcm: np.ndarray) -> tuple[bool, float]:
    pcm16 = pcm.astype(np.int16)
    score = 0.0
    # Feed in 80ms chunks like openWakeWord's microphone example
    for i in range(0, len(pcm16), OWW_CHUNK):
        chunk = pcm16[i : i + OWW_CHUNK]
        if len(chunk) < OWW_CHUNK:
            break
        predictions = model.predict(chunk)
        for value in predictions.values():
            value_arr = np.asarray(value)
            value_score = float(value_arr.max()) if value_arr.size else 0.0
            score = max(score, value_score)
    return score >= OWW_THRESHOLD, score


def _has_wakeword(text: str) -> bool:
    normalized = "".join(ch.lower() if ch.isalpha() or ch.isspace() else " " for ch in text)
    words = [w for w in normalized.split() if w]
    if not words:
        return False

    for word in words:
        if word in WAKEWORD_ALIASES:
            return True
        if difflib.SequenceMatcher(None, word, WAKEWORD).ratio() >= 0.78:
            return True
    return False


def _listen_utterance() -> str:
    print("Status: Listening...")
    chunks: list[np.ndarray] = []
    partial = ""
    saw_speech = False
    silence_count = 0
    no_speech_count = 0

    for _ in range(MAX_LISTEN_CHUNKS):
        pcm = _record_chunk()
        b64 = _audio_b64_from_pcm(pcm)
        rms = float(np.sqrt(np.mean(np.square(pcm.astype(np.float64))))) if pcm.size else 0.0
        speech = _vad_chunk(b64) and rms >= MIN_RMS_FOR_SPEECH

        if speech:
            saw_speech = True
            silence_count = 0
            no_speech_count = 0
            chunks.append(pcm)
            try:
                part_text, _provider = _stt_chunk(b64)
                clean = part_text.strip()
                if clean and len(clean) > 1 and clean not in {".", ",", "?", "!"} and clean != partial:
                    partial = part_text
                    if VERBOSE:
                        print(f"Live: {partial}")
            except Exception:
                pass
        else:
            if saw_speech:
                silence_count += 1
                if silence_count >= SILENCE_LIMIT:
                    break
            else:
                no_speech_count += 1
                if no_speech_count >= NO_SPEECH_START_LIMIT:
                    print("Status: No speech detected, returning to idle")
                    return ""

    if not chunks:
        return ""
    full_pcm = np.concatenate(chunks)
    full_b64 = _audio_b64_from_pcm(full_pcm)
    final_text, _provider = _stt_chunk(full_b64)
    if VERBOSE:
        print(f"Final ({_provider}): {final_text}")
    return final_text


def main() -> int:
    if VERBOSE:
        print("JARVIS Voice Console")
        print(f"Wakeword: '{WAKEWORD}'")
        print(f"Wakeword engine: openwakeword ({OWW_MODEL_NAME}, threshold={OWW_THRESHOLD})")
        print("Press Ctrl+C to exit.\n")

    if not _is_up(f"{VOICE_URL}/v1/health"):
        print("voice-pipeline not reachable at /v1/health")
        return 1
    if not _is_up(f"{RUNTIME_URL}/v1/health"):
        print("runtime-api not reachable at /v1/health")
        return 1

    print("Status: Idle (say 'Hey Jarvis' to activate)")
    _set_orb_state("idle", visible=False)
    wake_model = _init_openwakeword()
    last_wake_time = 0.0

    try:
        while True:
            pcm = _record_chunk()
            b64 = _audio_b64_from_pcm(pcm)

            if wake_model is not None:
                try:
                    detected, score = _openwakeword_detect(wake_model, pcm)
                except Exception as exc:  # noqa: BLE001
                    print(f"openwakeword error: {exc}")
                    wake_model = None
                    detected, score = False, 0.0

                now = time.time()
                if DEBUG_WAKE and score > 0.05:
                    print(f"[wake debug] score={score:.3f} (threshold={OWW_THRESHOLD})")
                if detected and (now - last_wake_time) >= OWW_DEBOUNCE_SECONDS:
                    last_wake_time = now
                    print("Status: Wakeword detected" + (f" (score={score:.2f})" if VERBOSE else ""))
                    _set_orb_state("listening", visible=True)
                    user_text = _listen_utterance()
                    if not user_text:
                        _set_orb_state("idle", visible=False)
                        if VERBOSE:
                            print("Status: Idle (no utterance captured)")
                        continue
                    print("Status: Thinking...")
                    _set_orb_state("processing", visible=True)
                    reply = _run_jarvis_intent(user_text)
                    print(f"JARVIS: {reply.get('assistant_output', '')}")
                    if reply.get("tts_audio_base64"):
                        _set_orb_state("speaking", visible=True)
                        out = _save_tts(reply["tts_audio_base64"], reply.get("tts_mime_type", "audio/wav"))
                        if sys.platform == "win32":
                            try:
                                os.startfile(out)
                            except OSError:
                                if VERBOSE:
                                    print(f"Audio saved: {out}")
                    elif VERBOSE:
                        print("TTS unavailable (audio not played)")
                    _set_orb_state("idle", visible=True)
                    print("Status: Idle (say 'Hey Jarvis' to activate)")
                continue

            try:
                text, _provider = _stt_chunk(b64)
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                print(f"STT error {exc.code}: {body}")
                continue
            except Exception as exc:  # noqa: BLE001
                print(f"STT request failed: {exc}")
                continue

            if not text:
                continue
            if _has_wakeword(text):
                print("Status: Wakeword detected")
                _set_orb_state("listening", visible=True)
                user_text = _listen_utterance()
                if not user_text:
                    _set_orb_state("idle", visible=False)
                    print("Status: Idle (no utterance captured)")
                    continue
                print("Status: Thinking...")
                _set_orb_state("processing", visible=True)
                reply = _run_jarvis_intent(user_text)
                print(f"JARVIS: {reply.get('assistant_output', '')}")
                if reply.get("tts_audio_base64"):
                    _set_orb_state("speaking", visible=True)
                    out = _save_tts(reply["tts_audio_base64"], reply.get("tts_mime_type", "audio/wav"))
                    if sys.platform == "win32":
                        try:
                            os.startfile(out)
                        except OSError:
                            if VERBOSE:
                                print(f"Audio saved: {out}")
                elif VERBOSE:
                    print("TTS unavailable (audio not played)")
                _set_orb_state("idle", visible=True)
                print("Status: Idle (say 'Hey Jarvis' to activate)")
    except KeyboardInterrupt:
        print("\nExiting voice console.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
