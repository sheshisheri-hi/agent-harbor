"""Fake MCP-style claims tools for the AgentHarbor insurance demo."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="AgentHarbor MCP Claims", version="0.1.0")


class ClaimLookupRequest(BaseModel):
    claim_id: str = Field(..., examples=["CLM-10042"])


class PolicyLookupRequest(BaseModel):
    policy_number: str = Field(..., examples=["POL-77821"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "mcp-claims"}


@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "get_claim",
                "description": "Return a fake claim record by id",
                "path": "/tools/get_claim",
            },
            {
                "name": "get_policy",
                "description": "Return a fake policy summary",
                "path": "/tools/get_policy",
            },
            {
                "name": "list_open_claims",
                "description": "List open demo claims",
                "path": "/tools/list_open_claims",
            },
        ]
    }


@app.post("/tools/get_claim")
def get_claim(body: ClaimLookupRequest):
    return {
        "claim_id": body.claim_id,
        "status": "open",
        "type": "auto-collision",
        "amount_estimate_usd": 4200,
        "insured": "Alex Demo",
        "note": "Synthetic data for AgentHarbor showcase",
    }


@app.post("/tools/get_policy")
def get_policy(body: PolicyLookupRequest):
    return {
        "policy_number": body.policy_number,
        "product": "personal-auto",
        "coverage": {"liability": True, "collision": True, "comprehensive": False},
        "effective": "2025-01-01",
        "note": "Synthetic data for AgentHarbor showcase",
    }


@app.get("/tools/list_open_claims")
def list_open_claims():
    return {
        "claims": [
            {"claim_id": "CLM-10042", "status": "open", "type": "auto-collision"},
            {"claim_id": "CLM-10088", "status": "open", "type": "property-water"},
            {"claim_id": "CLM-10103", "status": "open", "type": "auto-theft"},
        ]
    }
