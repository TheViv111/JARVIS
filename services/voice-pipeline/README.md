# Voice Pipeline Service

Phase implementation for:
- Wakeword detection (`openWakeWord` primary)
- VAD (`Silero` primary, `WebRTC` fallback)
- STT (Groq Whisper primary, `faster-whisper` fallback)
- TTS (`edge-tts` primary, `Piper` fallback)

## Run

```powershell
cd C:\Users\vivaa\Documents\jarvis\services\voice-pipeline
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 7788 --reload
```

or

```powershell
.\run_voice.ps1
```

## Endpoints

- `GET /v1/health`
- `POST /v1/wakeword/detect`
- `POST /v1/vad/detect`
- `POST /v1/stt/transcribe`
- `POST /v1/tts/speak`

## Notes

- Wakeword and Silero are dependency-optional. If not available, service uses fallback behavior and reports provider used.
- TTS returns base64-encoded audio bytes (`audio_base64`) for easy transport.
