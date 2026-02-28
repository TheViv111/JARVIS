# Project Charter v1.3 (Diamond Standard, Hybrid Online + Offline)

## 1. Product Vision
Build a single-user, agentic desktop JARVIS for Windows that understands intent, selects tools autonomously, executes across device and connected services, explains reasoning, asks clarifying questions when uncertain, and develops long-term intelligence through timeline + graph memory, with online-first and offline-capable local fallback.

## 2. Locked Decisions
1. Agentic by default.
2. Single-user profile.
3. Always-on context capture.
4. High-risk actions always require approval.
5. High-risk includes send mail/message, delete, payments, system-critical changes, installs/driver updates.
6. Email mode: detect -> ask to draft -> preview -> ask to send.
7. Music target: local-first headless playback (`mpv + yt-dlp`) with optional YouTube Music account integration later.
8. Hybrid memory storage: local encrypted primary + optional encrypted cloud sync.
9. Learned workflows require approval for first 3 runs.
10. Low-confidence behavior asks proactive clarifying questions.
11. Obsidian integration is out of scope.
12. Offline fallback is mandatory for core assistant flows.

## 3. Core Capabilities
1. Wake-word and global hotkey invocation.
2. Global orb HUD overlay.
3. React localhost control center.
4. Full-duplex voice with barge-in.
5. Full-device control (apps/windows/files/settings/browser/automation).
6. Headless integrations (calendar, mail, search, smart-home, music).
7. MCP and custom Python tools.
8. Proactivity engine (cron/events/reminders/watchers).
9. Timeline recall for prior activity.
10. Graph memory for relationship reasoning.
11. Screen context + optional webcam context.
12. Biometric trust for sensitive flows.
13. Explainable reasoning and previews.
14. Self-heal, retries, degraded mode, and offline mode.

## 4. Architecture
1. Electron desktop shell (orb, tray, global shortcuts, notifications).
2. React control center (localhost app).
3. Realtime voice chain (wake -> VAD -> STT -> LLM -> tools -> TTS).
4. FastAPI runtime (planner/executor/verifier/policy).
5. Tool layer (MCP + Python sandbox workers).
6. Proactivity engine (scheduler, event bus, retries).
7. Memory layer (timeline/vector/graph/preferences).
8. Vision layer (screen capture, OCR, UI parsing, optional webcam).
9. Identity layer (speaker + face + liveness).
10. Safety layer (risk tiering, approvals, audit, redaction).
11. Observability (latency, failures, health, weekly reports).
12. Fallback orchestrator (online provider selection + local/offline failover routing).

## 5. Technical Stack
1. Windows 11.
2. Python 3.11+ FastAPI backend.
3. Electron shell.
4. React + TypeScript localhost UI.
5. SQLite initial -> PostgreSQL migration.
6. Qdrant for semantic memory.
7. Neo4j or Postgres graph model.
8. Redis queue + APScheduler.
9. OCR: Tesseract/PaddleOCR.
10. Wake: openWakeWord primary.
11. VAD: Silero primary, WebRTC fallback.
12. STT primary: Groq Whisper; local fallback: faster-whisper.
13. TTS primary: Edge TTS; fallback: Groq/Azure; local fallback: Piper/pyttsx3.
14. LLM primary: Groq Responses API; local fallback: Ollama (`llama3.1`/`qwen2.5` class models).
15. Automation: Playwright + desktop automation.
16. Music primary: `mpv + yt-dlp` (headless local controller).
17. Secret management: OS keychain + encrypted store.

## 6. API Requisites
1. Groq Responses.
2. Groq audio transcriptions.
3. Groq audio speech fallback.
4. Edge TTS client.
5. Google Gmail/Calendar/Search APIs.
6. Optional YouTube Music account API path (if enabled later).
7. Smart-home adapter APIs.
8. MCP servers.
9. Internal Tool API.
10. Internal Policy API.
11. Internal Memory API.
12. Local provider endpoints: Ollama API, local STT/TTS executables.

## 7. Offline/Degraded Policy
1. If cloud LLM unavailable -> route to Ollama automatically.
2. If cloud STT unavailable -> route to faster-whisper local.
3. If cloud TTS unavailable -> route to local TTS engine.
4. If external music API unavailable -> continue with `mpv + yt-dlp` search/play.
5. Safety policies remain enforced in both online and offline modes.
6. Log fallback reason and recovery attempts in audit trail.
