"""AgentHarbor gateway — registry, RBAC, audit, kill switch, mock-brain runs."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app import brain

MCP_CLAIMS_URL = os.getenv("MCP_CLAIMS_URL", "http://mcp-claims:8090").rstrip("/")

app = FastAPI(
    title="AgentHarbor Gateway",
    version="0.2.0",
    description="Policy gateway + mock LLM brain for AgentHarbor showcase",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRecord(BaseModel):
    id: str
    name: str
    namespace: str
    allowed_tools: list[str]
    enabled: bool = True
    attested: bool = False
    description: str = ""


class RunRequest(BaseModel):
    agent_id: str
    task_id: str
    claim_id: str = "CLM-10042"
    user_id: str = "demo-user"


class AuditEvent(BaseModel):
    audit_id: str
    timestamp: str
    run_id: str
    agent_id: str
    namespace: str
    user_id: str
    tool: str
    args: dict[str, Any]
    decision: str
    reason: str


# In-memory control plane state (demo only)
AGENTS: dict[str, AgentRecord] = {
    "claims-intake-bot": AgentRecord(
        id="claims-intake-bot",
        name="Claims Intake",
        namespace="claims-sandbox",
        allowed_tools=["get_claim", "add_note"],
        attested=True,
        description="Sandbox intake agent — read + notes only",
    ),
    "fraud-scanner-bot": AgentRecord(
        id="fraud-scanner-bot",
        name="Fraud Scanner",
        namespace="claims-sandbox",
        allowed_tools=["get_claim", "flag_fraud"],
        attested=True,
        description="Sandbox fraud heuristics",
    ),
    "payout-approver-bot": AgentRecord(
        id="payout-approver-bot",
        name="Payout Approver",
        namespace="claims-prod",
        allowed_tools=["get_claim", "approve_payout"],
        attested=True,
        description="Prod payout agent — requires attestation + allowlist",
    ),
}

AUDIT: list[AuditEvent] = []

TOOL_PATHS = {
    "get_claim": "/tools/get_claim",
    "add_note": "/tools/add_note",
    "flag_fraud": "/tools/flag_fraud",
    "approve_payout": "/tools/approve_payout",
    "export_pii": "/tools/export_pii",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _evaluate(agent: AgentRecord, tool: str) -> tuple[bool, str]:
    if not agent.enabled:
        return False, "agent disabled (kill switch)"
    if agent.namespace == "claims-prod" and not agent.attested:
        return False, "missing attestation for claims-prod namespace"
    if tool not in agent.allowed_tools:
        return False, f"tool '{tool}' not on allowlist {agent.allowed_tools}"
    return True, "policy allow"


def _audit(
    run_id: str,
    agent: AgentRecord,
    user_id: str,
    tool: str,
    args: dict[str, Any],
    allowed: bool,
    reason: str,
) -> AuditEvent:
    event = AuditEvent(
        audit_id=str(uuid.uuid4()),
        timestamp=_now(),
        run_id=run_id,
        agent_id=agent.id,
        namespace=agent.namespace,
        user_id=user_id,
        tool=tool,
        args=args,
        decision="ALLOW" if allowed else "DENY",
        reason=reason,
    )
    AUDIT.append(event)
    return event


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "gateway",
        "brain": "mock-llm-deterministic",
        "mcp_claims_url": MCP_CLAIMS_URL,
    }


@app.get("/agents")
def list_agents():
    return {"agents": list(AGENTS.values()), "count": len(AGENTS)}


@app.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")
    return agent


@app.post("/agents/{agent_id}/disable")
def disable_agent(agent_id: str):
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")
    agent.enabled = False
    return agent


@app.post("/agents/{agent_id}/enable")
def enable_agent(agent_id: str):
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")
    agent.enabled = True
    return agent


@app.post("/agents/{agent_id}/attestation")
def set_attestation(agent_id: str, attested: bool = Query(True)):
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")
    agent.attested = attested
    return agent


@app.get("/tasks")
def list_tasks():
    return {"tasks": brain.TASKS}


@app.get("/audit")
def list_audit(limit: int = 50):
    return list(reversed(AUDIT[-limit:]))


@app.post("/runs")
async def run_agent(body: RunRequest):
    """On-demand agent run: mock brain plans tools → gateway enforces policy → MCP twin."""
    agent = AGENTS.get(body.agent_id)
    if not agent:
        raise HTTPException(404, f"unknown agent_id {body.agent_id}")

    run_id = str(uuid.uuid4())
    try:
        planned = brain.plan(body.agent_id, body.task_id, body.claim_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

    steps: list[dict[str, Any]] = []
    overall = "ALLOW"

    async with httpx.AsyncClient(timeout=15.0) as client:
        for call in planned:
            allowed, reason = _evaluate(agent, call.tool)
            event = _audit(
                run_id, agent, body.user_id, call.tool, call.args, allowed, reason
            )
            step: dict[str, Any] = {
                "tool": call.tool,
                "args": call.args,
                "brain_rationale": call.rationale,
                "decision": event.decision,
                "reason": reason,
                "audit_id": event.audit_id,
                "result": None,
            }
            if not allowed:
                overall = "DENY"
                steps.append(step)
                break

            path = TOOL_PATHS.get(call.tool)
            if not path:
                step["decision"] = "DENY"
                step["reason"] = f"unknown tool route for {call.tool}"
                overall = "DENY"
                steps.append(step)
                break

            try:
                resp = await client.post(f"{MCP_CLAIMS_URL}{path}", json=call.args)
                step["result"] = resp.json() if resp.content else None
                step["mcp_status"] = resp.status_code
                if resp.status_code >= 400:
                    overall = "DENY"
                    step["reason"] = f"mcp twin returned HTTP {resp.status_code}"
                    steps.append(step)
                    break
            except httpx.HTTPError as exc:
                overall = "DENY"
                step["reason"] = f"mcp twin unreachable: {exc}"
                steps.append(step)
                break

            steps.append(step)

    return {
        "run_id": run_id,
        "agent": agent,
        "task_id": body.task_id,
        "task": brain.TASKS.get(body.task_id),
        "claim_id": body.claim_id,
        "brain": {
            "mode": "mock-llm-deterministic",
            "note": "No remote LLM was called. Tool plans are fixed for reproducible demos.",
            "planned_tools": [c.tool for c in planned],
        },
        "overall_decision": overall,
        "steps": steps,
    }
