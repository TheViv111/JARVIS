import os
import subprocess
import tempfile

from app.config import settings


class TtsError(Exception):
    pass


async def _speak_edge_tts(text: str, voice: str | None = None) -> bytes:
    try:
        import edge_tts
    except Exception as exc:  # noqa: BLE001
        raise TtsError("edge-tts is not installed.") from exc

    selected_voice = voice or settings.edge_tts_voice
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
        output_path = temp.name
    try:
        communicate = edge_tts.Communicate(text=text, voice=selected_voice)
        await communicate.save(output_path)
        with open(output_path, "rb") as audio_file:
            return audio_file.read()
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def _speak_piper(text: str) -> bytes:
    if not settings.piper_exe or not settings.piper_model_path:
        raise TtsError("PIPER_EXE or PIPER_MODEL_PATH is not configured.")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
        output_path = temp.name
    try:
        proc = subprocess.run(
            [settings.piper_exe, "--model", settings.piper_model_path, "--output_file", output_path],
            input=text,
            text=True,
            check=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            raise TtsError("Piper process failed.")
        with open(output_path, "rb") as audio_file:
            return audio_file.read()
    except subprocess.CalledProcessError as exc:
        raise TtsError(f"Piper failed: {exc.stderr}") from exc
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


async def synthesize(text: str, voice: str | None = None, prefer_cloud: bool = True) -> tuple[bytes, str, bool]:
    if prefer_cloud:
        try:
            return await _speak_edge_tts(text=text, voice=voice), "edge-tts", False
        except Exception:
            pass
    return _speak_piper(text), "piper", True

