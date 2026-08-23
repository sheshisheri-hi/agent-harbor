# Mock LLM brain

**Location:** `gateway/app/brain.py`  
**Mode:** `mock-llm-deterministic`

## What it is

A **simulated LLM planner**. It does **not** call OpenAI, Anthropic, or any remote model. Given `(agent_id, task_id, claim_id)` it returns a fixed list of tool calls with short rationales.

## Why

- Reproducible ALLOW / DENY demos  
- No API keys or cost  
- Clear separation: **planning** (brain) vs **authorization** (gateway)

## Behavior

| Task | Planned tools |
| --- | --- |
| `read_claim` | `get_claim` |
| `add_note` | `get_claim` → `add_note` |
| `flag_fraud` | `get_claim` → `flag_fraud` |
| `approve_payout` | `get_claim` → `approve_payout` |
| `export_pii` | `export_pii` |

Plans are based on the **task**, not the agent allowlist. That way Intake can *attempt* Approve payout and the UI shows a clear **DENY**.

## API surface

Runs are started via `POST /runs` on the gateway. The response includes:

```json
"brain": {
  "mode": "mock-llm-deterministic",
  "note": "No remote LLM was called...",
  "planned_tools": ["get_claim", "approve_payout"]
}
```

## Future

A feature flag could swap this module for a real LLM later. The gateway policy path should stay the same.
