"""Fake MCP-style claims tools for the AgentHarbor insurance demo."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AgentHarbor MCP Claims", version="0.2.0")

CLAIMS: dict[str, dict] = {
    "CLM-10042": {
        "claim_id": "CLM-10042",
        "status": "open",
        "type": "auto-collision",
        "amount_estimate_usd": 4200,
        "insured": "Alex Demo",
        "notes": [],
        "fraud_flags": [],
        "payout_approved": False,
    },
    "CLM-10088": {
        "claim_id": "CLM-10088",
        "status": "open",
        "type": "property-water",
        "amount_estimate_usd": 9100,
        "insured": "Jordan Sample",
        "notes": [],
        "fraud_flags": [],
        "payout_approved": False,
    },
    "CLM-10103": {
        "claim_id": "CLM-10103",
        "status": "open",
        "type": "auto-theft",
        "amount_estimate_usd": 15500,
        "insured": "Sam Example",
        "notes": [],
        "fraud_flags": [],
        "payout_approved": False,
    },
}


class ClaimLookupRequest(BaseModel):
    claim_id: str = Field(..., examples=["CLM-10042"])


class AddNoteRequest(BaseModel):
    claim_id: str
    note: str = Field(..., min_length=1)


class FlagFraudRequest(BaseModel):
    claim_id: str
    reason: str = Field(default="heuristic-demo")


class ApprovePayoutRequest(BaseModel):
    claim_id: str
    amount_usd: float | None = None


class ExportPiiRequest(BaseModel):
    claim_id: str


def _claim(claim_id: str) -> dict:
    claim = CLAIMS.get(claim_id)
    if not claim:
        raise HTTPException(404, f"unknown claim_id {claim_id}")
    return claim


@app.get("/health")
def health():
    return {"status": "ok", "service": "mcp-claims"}


@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "get_claim", "path": "/tools/get_claim"},
            {"name": "add_note", "path": "/tools/add_note"},
            {"name": "flag_fraud", "path": "/tools/flag_fraud"},
            {"name": "approve_payout", "path": "/tools/approve_payout"},
            {"name": "export_pii", "path": "/tools/export_pii"},
            {"name": "list_open_claims", "path": "/tools/list_open_claims"},
        ]
    }


@app.post("/tools/get_claim")
def get_claim(body: ClaimLookupRequest):
    claim = _claim(body.claim_id)
    return {**claim, "note": "Synthetic data for AgentHarbor showcase"}


@app.post("/tools/add_note")
def add_note(body: AddNoteRequest):
    claim = _claim(body.claim_id)
    claim["notes"].append(body.note)
    return {"claim_id": body.claim_id, "notes": claim["notes"], "ok": True}


@app.post("/tools/flag_fraud")
def flag_fraud(body: FlagFraudRequest):
    claim = _claim(body.claim_id)
    claim["fraud_flags"].append(body.reason)
    return {"claim_id": body.claim_id, "fraud_flags": claim["fraud_flags"], "ok": True}


@app.post("/tools/approve_payout")
def approve_payout(body: ApprovePayoutRequest):
    claim = _claim(body.claim_id)
    amount = body.amount_usd if body.amount_usd is not None else claim["amount_estimate_usd"]
    claim["payout_approved"] = True
    claim["status"] = "payout-approved"
    return {
        "claim_id": body.claim_id,
        "payout_approved": True,
        "amount_usd": amount,
        "ok": True,
    }


@app.post("/tools/export_pii")
def export_pii(body: ExportPiiRequest):
    claim = _claim(body.claim_id)
    return {
        "claim_id": body.claim_id,
        "pii": {
            "insured_full_name": claim["insured"],
            "ssn_last4": "0000",
            "address": "123 Demo Street",
            "email": "demo@example.invalid",
        },
        "warning": "Synthetic PII for deny-path demos only",
    }


@app.get("/tools/list_open_claims")
def list_open_claims():
    return {
        "claims": [
            {"claim_id": c["claim_id"], "status": c["status"], "type": c["type"]}
            for c in CLAIMS.values()
        ]
    }
