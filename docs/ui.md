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
