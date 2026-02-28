# Runtime API (Phase 1)

Phase 1 delivers three core capabilities:
- Transcription (cloud-first, local fallback path)
- Intelligence routing (cloud LLM, Ollama fallback)
- Face trust (local evaluator)

## Run

```powershell
cd C:\Users\vivaa\Documents\jarvis\services\runtime-api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 7777 --reload
```

## Chat Interface (Terminal)

If the API is already running:

```powershell
cd C:\Users\vivaa\Documents\jarvis\services\runtime-api
python .\chat_cli.py
```

If you want one command that starts server + chat:

```powershell
cd C:\Users\vivaa\Documents\jarvis\services\runtime-api
.\run_chat.ps1
```

If you want voice-pipeline + runtime + chat together:

```powershell
.\run_jarvis.ps1
```

For voice-first interaction (wakeword + live transcription in same terminal):

```powershell
.\run_voice_console.ps1
```

Voice console status flow:
- `Idle (say 'Jarvis' to activate)`
- `Wakeword detected`
- `Listening...`
- `Live: <partial transcript>`
- `Final: <final transcript>`
- `Thinking...`
- `JARVIS: <response>`

The CLI shows:
- assistant response
- plan steps
- risk classification
- approval requirement
- provider usage (LLM/STT/face)
- request latency

CLI commands:
- `/meta` toggles detailed telemetry
- `/think` toggles the thinking indicator
- `/raw` toggles full JSON
- `/speak` toggles reply audio generation (saved under `outputs/`)

Speed tip:
- Use a faster Groq model in your env, for example:
  - `GROQ_MODEL=llama-3.1-8b-instant`

## Endpoints

- `GET /health`
- `POST /v1/transcription/transcribe`
- `POST /v1/intelligence/respond`
- `POST /v1/face/verify`
- `POST /v1/intent/execute`

## Notes

- TTS is intentionally not included in this Phase 1 service.
- `edge-tts` primary and `piper` fallback will be added in Voice phase.
- Current face trust module is local and lightweight; you can replace internals later with a stronger verifier.
- Intent execution now performs basic risk classification and flags high-risk prompts for approval.
