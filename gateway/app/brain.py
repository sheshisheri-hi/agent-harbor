"""Deterministic mock LLM brain — no real model calls.

Simulates planning: given (agent_id, task_id) return a fixed tool plan.
This makes ALLOW/DENY demos reproducible without OpenAI/Anthropic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlannedToolCall:
    tool: str
    args: dict[str, Any]
    rationale: str


# Tasks the UI can request. Each maps to what a "brain" would plan.
TASKS = {
    "read_claim": {
        "label": "Read claim",
        "description": "Fetch claim details from the claims twin",
    },
    "add_note": {
        "label": "Add note",
        "description": "Append an adjuster note on the claim",
    },
    "flag_fraud": {
        "label": "Flag fraud",
        "description": "Attach a fraud heuristic flag",
    },
    "approve_payout": {
        "label": "Approve payout",
        "description": "Approve claim payout (high risk)",
    },
    "export_pii": {
        "label": "Export PII",
        "description": "Export insured PII (should usually be denied)",
    },
}


def plan(agent_id: str, task_id: str, claim_id: str) -> list[PlannedToolCall]:
    """Return the tool calls a simulated LLM would attempt for this task.

    Intentional: plans are based on the *task*, not the agent's allowlist.
    The gateway policy layer decides ALLOW vs DENY — that is the showcase.
    """
    if task_id not in TASKS:
        raise ValueError(f"unknown task_id: {task_id}")

    if task_id == "read_claim":
        return [
            PlannedToolCall(
                tool="get_claim",
                args={"claim_id": claim_id},
                rationale="Mock brain: retrieve claim record before responding.",
            )
        ]
    if task_id == "add_note":
        return [
            PlannedToolCall(
                tool="get_claim",
                args={"claim_id": claim_id},
                rationale="Mock brain: load claim context.",
            ),
            PlannedToolCall(
                tool="add_note",
                args={
                    "claim_id": claim_id,
                    "note": f"Demo note from {agent_id} (mock LLM)",
                },
                rationale="Mock brain: write a short status note.",
            ),
        ]
    if task_id == "flag_fraud":
        return [
            PlannedToolCall(
                tool="get_claim",
                args={"claim_id": claim_id},
                rationale="Mock brain: inspect claim for anomalies.",
            ),
            PlannedToolCall(
                tool="flag_fraud",
                args={"claim_id": claim_id, "reason": "demo-heuristic-score"},
                rationale="Mock brain: raise fraud flag for adjuster review.",
            ),
        ]
    if task_id == "approve_payout":
        return [
            PlannedToolCall(
                tool="get_claim",
                args={"claim_id": claim_id},
                rationale="Mock brain: confirm claim before payout.",
            ),
            PlannedToolCall(
                tool="approve_payout",
                args={"claim_id": claim_id},
                rationale="Mock brain: approve payout amount.",
            ),
        ]
    if task_id == "export_pii":
        return [
            PlannedToolCall(
                tool="export_pii",
                args={"claim_id": claim_id},
                rationale="Mock brain: attempt to export insured PII.",
            )
        ]
    raise ValueError(f"unhandled task_id: {task_id}")
