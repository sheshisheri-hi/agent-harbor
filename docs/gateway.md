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

Evaluated **in order** for each planned tool:

1. Disabled agent → **DENY** (`agent disabled (kill switch)`)  
2. Namespace is `claims-prod` **and** not attested → **DENY** (`missing attestation for claims-prod namespace`)  
3. Tool not in `allowed_tools` → **DENY**  
4. Else → **ALLOW** and invoke mcp-claims  

### Attestation nuance

- **`claims-sandbox` agents** (Intake, Fraud): clearing attestation does **nothing**. Read claim still **ALLOW**.  
- **`claims-prod` agent** (Payout): clearing attestation **DENY**s every tool, including `get_claim` / Read claim.

Full click matrix: [demo-behaviors.md](./demo-behaviors.md).

State is **in-memory** (resets on container restart). Fine for the educational showcase.
