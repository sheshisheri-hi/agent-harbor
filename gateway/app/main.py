"""AgentHarbor gateway stub — identity/RBAC/audit/kill-switch placeholders ahead."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AgentHarbor Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_AGENTS = [
    {
        "id": "claims-triage",
        "name": "Claims Triage Agent",
        "namespace": "insurance/claims",
        "status": "ready",
        "description": "Routes incoming FNOL to severity queues (demo).",
    },
    {
        "id": "policy-lookup",
        "name": "Policy Lookup Agent",
        "namespace": "insurance/policy",
        "status": "ready",
        "description": "Fetches policy coverage summaries via MCP tools (demo).",
    },
    {
        "id": "fraud-signal",
        "name": "Fraud Signal Agent",
        "namespace": "insurance/fraud",
        "status": "ready",
        "description": "Surfaces heuristic fraud signals for adjuster review (demo).",
    },
]


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}


@app.get("/agents")
def list_agents():
    """Stub agent catalog — authZ and audit not enforced yet."""
    return {"agents": DEMO_AGENTS, "count": len(DEMO_AGENTS)}
