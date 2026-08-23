# MCP Claims twin

**Location:** `mcp-claims/app/main.py`  
**Port:** `8090`

## What it is

A **fake insurance claims tool server** shaped like MCP-style HTTP tools. It is not a full MCP SDK transport yet; it exposes REST endpoints the gateway calls after policy ALLOW.

## Tools

| Tool | Method | Effect |
| --- | --- | --- |
| `get_claim` | POST `/tools/get_claim` | Read synthetic claim |
| `add_note` | POST `/tools/add_note` | Append note |
| `flag_fraud` | POST `/tools/flag_fraud` | Append fraud flag |
| `approve_payout` | POST `/tools/approve_payout` | Mark payout approved |
| `export_pii` | POST `/tools/export_pii` | Return synthetic PII (deny-path demo) |
| `list_open_claims` | GET `/tools/list_open_claims` | List seed claims |

Seed claims: `CLM-10042`, `CLM-10088`, `CLM-10103`.

## Security note

This service trusts the gateway to enforce RBAC. In a hardened design, tools would also validate OAuth tokens from Keycloak. Token enforcement is a later phase; today the **gateway is the choke point**.
