from __future__ import annotations

from dataclasses import dataclass


ALWAYS_HIGH_KEYWORDS = {
    "send email",
    "email",
    "send message",
    "message",
    "delete",
    "remove permanently",
    "payment",
    "pay",
    "install",
    "driver",
    "registry",
    "system setting",
}


@dataclass(slots=True)
class RiskDecision:
    risk: str
    requires_approval: bool
    reason: str


def evaluate_risk(user_input: str) -> RiskDecision:
    text = user_input.lower().strip()
    if not text:
        return RiskDecision(risk="low", requires_approval=False, reason="empty_input")

    for token in ALWAYS_HIGH_KEYWORDS:
        if token in text:
            return RiskDecision(risk="high", requires_approval=True, reason=f"matched:{token}")

    if any(token in text for token in ("open", "summarize", "check", "read", "find")):
        return RiskDecision(risk="low", requires_approval=False, reason="read_or_navigation")

    return RiskDecision(risk="medium", requires_approval=False, reason="default_medium")

