# Gateway (control plane)

**Location:** `gateway/app/main.py`  
**Port:** `8080` (Compose)

## Responsibilities

1. **Agent registry** — id, name, namespace, allowlist, enabled, attested  
2. **Policy evaluation** — kill switch, prod attestation, tool allowlist  
3. **Mock brain orchestration** — plan → enforce → call tools  
4. **Audit log** — every ALLOW and DENY  

## Demo agents

| Agent ID | Namespace | Allowlist |
| --- | --- | --- |
| `claims-intake-bot` | `claims-sandbox` | `get_claim`, `add_note` |
| `fraud-scanner-bot` | `claims-sandbox` | `get_claim`, `flag_fraud` |
| `payout-approver-bot` | `claims-prod` | `get_claim`, `approve_payout` |

## Key endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Liveness + brain mode |
| GET | `/agents` | List agents / policy |
| POST | `/agents/{id}/disable` | Kill switch |
| POST | `/agents/{id}/enable` | Re-enable |
| POST | `/agents/{id}/attestation?attested=` | Toggle attestation |
| GET | `/tasks` | Task catalog |
| POST | `/runs` | On-demand mock-brain run |
| GET | `/audit` | Recent decisions |

## Policy rules (v1)

1. Disabled agent → DENY (`kill switch`)  
2. `claims-prod` without `attested` → DENY  
3. Tool not in `allowed_tools` → DENY  
4. Else → ALLOW and invoke mcp-claims  

State is **in-memory** (resets on container restart). Fine for the educational showcase.
