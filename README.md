# AgentHarbor

Personal **educational showcase** of an AI agent security control plane: identity, namespaces, an RBAC gateway, audit trails, and a kill switch — demonstrated with a fictional insurance-claims workflow.

> **Disclaimer:** This is a personal learning / portfolio project. Do not use it as production security infrastructure.

## Mock LLM brain (important)

AgentHarbor uses a **deterministic mock LLM** (`gateway/app/brain.py`).  

- **No** OpenAI / Anthropic / other remote model calls  
- The “brain” only returns a **fixed tool plan** for each UI task  
- The **gateway** then allows or denies each tool (RBAC, kill switch, attestation)  

That split is intentional: you can demo security decisions without paying for or depending on a real model. See [docs/mock-brain.md](docs/mock-brain.md).

## Landscape credit

AgentHarbor borrows ideas from the broader identity and agent-tooling ecosystem:

- **Okta / Microsoft Entra** — enterprise IdP / agent-identity patterns  
- **Ory / Keycloak** — open-source OAuth/OIDC building blocks  
- **MCP** — tool-oriented agent interfaces  

## Docs (components)

| Doc | Topic |
| --- | --- |
| [docs/README.md](docs/README.md) | Doc index |
| [docs/overview.md](docs/overview.md) | End-to-end flow |
| [docs/mock-brain.md](docs/mock-brain.md) | Simulated LLM planner |
| [docs/gateway.md](docs/gateway.md) | Policy gateway |
| [docs/mcp-claims.md](docs/mcp-claims.md) | Claims tool twin |
| [docs/ui.md](docs/ui.md) | Demo UI |
| [docs/keycloak.md](docs/keycloak.md) | IdP in Compose |

## Stack (local)

| Service | Role | Port |
| --- | --- | --- |
| `ui` | Demo UI (buttons, ALLOW/DENY, audit) | 3000 |
| `gateway` | Mock brain + RBAC + audit + kill switch | 8080 |
| `keycloak` | IdP (dev + realm import) | 8081 |
| `mcp-claims` | Fake claims tools | 8090 |
| `postgres` | Keycloak database | 5432 |

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open **http://localhost:3000**

Suggested clicks:

1. **Claims Intake** → **Read claim** → ALLOW  
2. **Claims Intake** → **Approve payout** → DENY (not on allowlist)  
3. **Payout Approver** → **Approve payout** → ALLOW  
4. **Kill switch** → Approve again → DENY  

Also:

- Gateway health: http://localhost:8080/health  
- Keycloak: http://localhost:8081 (admin from `.env`)  
- Claims tools: http://localhost:8090/tools  

Demo realm: **agentharbor** — user `demo` / `demo` (local only).

## License / intent

Educational showcase only. Treat credentials and compose defaults as throwaway.
