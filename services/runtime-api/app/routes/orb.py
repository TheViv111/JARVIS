"""Orb state API - used by the desktop shell to show/hide and display JARVIS status."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/orb", tags=["orb"])

# In-memory orb state (orb_state, visible)
_orb_state = "idle"
_orb_visible = False


@router.get("/state")
async def get_orb_state() -> dict:
    """Return current orb state for the desktop shell to poll."""
    return {
        "orb_state": _orb_state,
        "visible": _orb_visible,
    }


@router.post("/state")
async def post_orb_state(payload: dict) -> dict:
    """Update orb state (called by voice_console and other JARVIS components)."""
    global _orb_state, _orb_visible
    _orb_state = payload.get("orb_state", _orb_state)
    _orb_visible = payload.get("visible", _orb_visible)
    return {"orb_state": _orb_state, "visible": _orb_visible}
