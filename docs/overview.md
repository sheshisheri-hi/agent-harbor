# Overview — how a demo run works

```text
Browser UI (button)
    │  POST /api/runs  { agent_id, task_id, claim_id }
    ▼
Nginx → AgentHarbor Gateway
    │  1. Load agent registry (namespace, allowlist, enabled, attested)
    │  2. Mock brain plans tool calls (deterministic — not a real LLM)
    │  3. For each tool: RBAC / kill switch / attestation check → audit
    │  4. If ALLOW → call mcp-claims twin; if DENY → stop
    ▼
mcp-claims (fake tools + in-memory claim data)
```

**On-demand:** agents are not queue workers. Each UI click starts one run.

**Showcase intent:** the brain may *plan* a privileged tool (e.g. `approve_payout`); the **gateway** decides whether that agent is allowed to execute it.

Expected click results (including attestation): [demo-behaviors.md](./demo-behaviors.md).
