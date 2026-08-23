# Demo UI

**Location:** `ui/index.html` (+ `nginx.conf`)  
**Port:** `3000`

## What it shows

1. Agent selector (Intake / Fraud / Payout) with live policy card  
2. Task buttons (read, note, flag, approve, export PII)  
3. Kill switch / enable / attestation toggles  
4. Result panel with overall ALLOW/DENY + mock-brain plan  
5. Audit table for both allow and deny events  

## Proxy

Nginx routes `/api/*` → `http://gateway:8080/` so the browser stays same-origin.

## Interaction model

Buttons trigger `POST /api/runs`. There is no chat box and no background queue — each click is one on-demand agent run through the mock brain.

## Controls behavior

| Control | Effect |
| --- | --- |
| Agent buttons | Select which principal / allowlist / namespace applies |
| Task buttons | Ask mock brain to plan tools for that task, then gateway enforces policy |
| Kill switch | Disable selected agent → all tasks DENY |
| Enable agent | Re-enable |
| Clear attestation | Only blocks **Payout Approver** (`claims-prod`). Sandbox agents still ALLOW |
| Set attested | Required again for Payout Approver |

See [demo-behaviors.md](./demo-behaviors.md) for the full ALLOW/DENY matrix (including why “Clear attestation + Read claim” on Intake still allows).

