# AgentHarbor

Personal **educational showcase** of an AI agent security control plane: identity, namespaces, an RBAC gateway, audit trails, and a kill switch — demonstrated with a fictional insurance-claims workflow.

> **Disclaimer:** This is a personal learning / portfolio project. Do not use it as production security infrastructure.

## Landscape credit

AgentHarbor borrows ideas from the broader identity and agent-tooling ecosystem:

- **Okta / Microsoft Entra** — enterprise IdP patterns (OIDC, RBAC, app roles)
- **Ory** — open-source identity & access building blocks
- **MCP (Model Context Protocol)** — tool-oriented agent interfaces

Vision and planning notes live in the sibling repo/folder [`plan-ai-systems-ideas`](../plan-ai-systems-ideas) (not published as part of this compose stack).

## Stack (local)

| Service     | Role                         | Port  |
|-------------|------------------------------|-------|
| `ui`        | Static demo UI               | 3000  |
| `gateway`   | FastAPI RBAC gateway stub    | 8080  |
| `keycloak`  | IdP (dev mode + realm import)| 8081  |
| `mcp-claims`| Fake MCP claims tools API    | 8090  |
| `postgres`  | Keycloak database            | 5432  |

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- UI: http://localhost:3000  
- Gateway: http://localhost:8080/health  
- Keycloak: http://localhost:8081 (admin from `.env`)  
- MCP claims: http://localhost:8090/health  

Demo realm: **agentharbor** — user `demo` / `demo` (change in realm JSON / `.env` for anything beyond local play).

Optional wait helper:

```bash
./scripts/wait-for.sh localhost 8080
```

## What’s stubbed vs next

- Gateway lists three demo agents; authZ/audit/kill-switch are placeholders.
- MCP claims exposes fake tool endpoints for claims workflows.
- UI buttons say “coming soon” — branded shell only.

## License / intent

Educational showcase only. Treat credentials and compose defaults as throwaway.
