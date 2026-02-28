# API Contracts v1

## 1. Runtime Service
Base URL: `http://localhost:7777`

### 1.1 Execute Intent
- `POST /v1/intent/execute`
- Purpose: natural-language task execution with planning and tool calls.
- Request:
```json
{
  "session_id": "sess_123",
  "input": "Check my calendar and summarize tomorrow",
  "modality": "voice",
  "context": {
    "active_app": "chrome",
    "orb_state": "listening"
  }
}
```
- Response:
```json
{
  "run_id": "run_abc",
  "status": "in_progress",
  "plan": ["fetch_calendar", "summarize", "speak"],
  "requires_approval": false
}
```

### 1.2 Approval Action
- `POST /v1/approval/respond`
- Request:
```json
{
  "approval_id": "apr_001",
  "decision": "approve",
  "reason": "Looks correct"
}
```

### 1.3 Mission State
- `GET /v1/mission/{run_id}`
- Returns plan, active step, confidence, tools used, and verifier status.

## 2. Tool Service

### 2.1 Tool Registration
- `POST /v1/tools/register`
- Payload must satisfy `schemas/tool.schema.json`.

### 2.2 Tool Execute
- `POST /v1/tools/{tool_id}/execute`
- Request:
```json
{
  "run_id": "run_abc",
  "input": {
    "query": "unread important emails"
  },
  "idempotency_key": "idem_789"
}
```

## 3. Memory Service

### 3.1 Write Event
- `POST /v1/memory/events`
- Payload must satisfy `schemas/memory_event.schema.json`.

### 3.2 Query Timeline
- `POST /v1/memory/timeline/query`
- Request:
```json
{
  "from": "2026-02-17T12:00:00Z",
  "to": "2026-02-17T16:00:00Z",
  "filters": {
    "apps": ["code", "chrome"]
  }
}
```

### 3.3 Graph Query
- `POST /v1/memory/graph/query`
- Request supports entity lookup, relationship traversal, and confidence thresholds.

## 4. Workflow Service

### 4.1 Learn Workflow
- `POST /v1/workflows/learn`
- Payload must satisfy `schemas/workflow.schema.json`.

### 4.2 Run Workflow
- `POST /v1/workflows/{workflow_id}/run`
- Enforces first-3-run approval policy.

## 5. Policy Service

### 5.1 Evaluate Action Risk
- `POST /v1/policy/evaluate`
- Request:
```json
{
  "action": "send_email",
  "tool_id": "gmail.send",
  "context": {
    "biometric": {
      "voice_score": 0.88,
      "face_score": 0.91
    }
  }
}
```
- Response: `{ "risk": "high", "requires_approval": true }`

### 5.2 Policy Upsert
- `PUT /v1/policy`
- Payload must satisfy `schemas/policy.schema.json`.

## 6. Realtime Voice Interface (Internal)
1. `voice.start`
2. `voice.partial_transcript`
3. `voice.final_transcript`
4. `voice.barge_in`
5. `voice.tts_chunk`
6. `voice.stop`

## 7. Integration APIs
1. Groq Responses/STT/TTS APIs.
2. Google Gmail/Calendar/Search APIs.
3. YouTube Music integration bridge.
4. Smart-home adapters.
5. MCP remote/local servers.

## 8. Error Contract
All endpoints return:
```json
{
  "error": {
    "code": "TOOL_TIMEOUT",
    "message": "Tool execution timed out",
    "retryable": true,
    "trace_id": "trc_123"
  }
}
```
