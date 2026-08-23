# AgentHarbor

Personal **educational showcase** of an AI agent security control plane: identity, namespaces, an RBAC gateway, audit trails, and a kill switch — demonstrated with a fictional insurance-claims workflow.

> **Disclaimer:** This is a personal learning / portfolio project. Do not use it as production security infrastructure.

## Why I started this

Enterprise IAM solved humans and apps. The **agentic world** is different: models don’t just answer — they **take actions** (tools, APIs, code changes, alerts, host config) often through loops that are not deterministic and often through runtimes (Copilot SDK, orchestrators, MCP) that hide the real effect behind “just an LLM response.”

Industry is moving fast:

- **Protocols** — MCP for tools, A2A for agent collaboration  
- **IdPs** — Okta, Microsoft Entra Agent ID, Ory/Keycloak for tokens and agent identity  
- **Startups** — control planes (e.g. Agentic Fabriq), runtime guards (e.g. Silmaril), attestation (e.g. Klaimee), sandboxes (e.g. Arga Labs)

Those pieces matter, but demos often show only the **happy path**. What was missing for me was a **visible harbor story**:

- Agents as **first-class principals** (not one shared API key)  
- **Namespaces** with blast radius (sandbox vs prod)  
- Every effect attempt checked at a **gateway** — ALLOW and **DENY**, with reasons  
- **Audit** you can show to security and platform teams  
- A **kill switch** when an agent misbehaves  

**AgentHarbor** is my independent proof of concept for that layer. It does **not** replace MCP or your IdP — it explores what **harbor control** should feel like when agents call tools today and when tomorrow’s agents mutate git, files, hosts, or prod systems through SDKs and orchestrator stages.

This repo is where I learn by building: mock brain for reproducible demos, Docker Compose for a runnable stack, and docs that spell out expected behavior (including when attestation applies and when it does not).

## Mock LLM brain (important)

AgentHarbor uses a **deterministic mock LLM** (`gateway/app/brain.py`).  

- **No** OpenAI / Anthropic / other remote model calls  
- The “brain” only returns a **fixed tool plan** for each UI task  
- The **gateway** then allows or denies each tool (RBAC, kill switch, attestation)  

That split is intentional: you can demo security decisions without paying for or depending on a real model. See [docs/mock-brain.md](docs/mock-brain.md).

## Landscape credit

AgentHarbor is an **independent learning project**. It builds on ideas from the broader ecosystem — it is not affiliated with or endorsed by these vendors:

- **Okta / Auth0 / Microsoft Entra** — agent-as-principal, MCP auth, token vault, governance  
- **Ory / Keycloak** — OAuth/OIDC for securing tool servers  
- **MCP / A2A** — how agents connect to tools and to each other  
- **Patterns from** Agentic Fabriq (identity/governance), Silmaril (runtime outcomes), Klaimee (attestation), Arga Labs (twins/sandboxes)

Planning notes and the original idea shortlist live in the sibling folder [`plan-ai-systems-ideas`](../plan-ai-systems-ideas).

## Docs (components)

| Doc | Topic |
| --- | --- |
| [docs/README.md](docs/README.md) | Doc index |
| [docs/overview.md](docs/overview.md) | End-to-end flow |
| [docs/demo-behaviors.md](docs/demo-behaviors.md) | ALLOW/DENY matrix (attestation, RBAC, kill switch) |
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
3. **Claims Intake** → **Clear attestation** → **Read claim** → still **ALLOW** (sandbox ignores attestation)  
4. **Payout Approver** → **Clear attestation** → **Read claim** → **DENY** (prod requires attestation)  
5. **Payout Approver** → **Set attested** → **Approve payout** → ALLOW  
6. **Kill switch** → Approve again → DENY  

Full matrix: [docs/demo-behaviors.md](docs/demo-behaviors.md).

Also:

- Gateway health: http://localhost:8080/health  
- Keycloak: http://localhost:8081 (admin from `.env`)  
- Claims tools: http://localhost:8090/tools  

Demo realm: **agentharbor** — user `demo` / `demo` (local only).

## License / intent

Educational showcase only. Treat credentials and compose defaults as throwaway.
