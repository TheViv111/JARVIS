import asyncio
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app


async def _request(method: str, path: str, json: dict | None = None) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, json=json)


def test_health() -> None:
    response = asyncio.run(_request("GET", "/v1/health"))
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_intelligence_degraded_when_no_provider() -> None:
    response = asyncio.run(
        _request(
            "POST",
            "/v1/intelligence/respond",
            json={"input": "hello", "context": {}, "prefer_cloud": False},
        )
    )
    assert response.status_code == 200
    payload = response.json()
    assert "output" in payload
    assert payload["provider"] in {"ollama", "degraded"}


def test_intent_flags_high_risk() -> None:
    response = asyncio.run(
        _request(
            "POST",
            "/v1/intent/execute",
            json={
                "session_id": "sess_1",
                "input": "Send email to everyone now",
                "modality": "text",
                "prefer_cloud": False,
            },
        )
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["risk"] == "high"
    assert payload["requires_approval"] is True

