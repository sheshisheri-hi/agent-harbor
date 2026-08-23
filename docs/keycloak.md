# Keycloak (IdP)

**Image:** `quay.io/keycloak/keycloak`  
**Port:** `8081` (host) → `8080` (container)  
**Realm import:** `keycloak/realm-agentharbor.json`

## Role in AgentHarbor

Keycloak is the **passport office** (OAuth/OIDC IdP stand-in for Okta-style patterns). The gateway is **harbor control**.

Today:

- Realm `agentharbor` imports on first start  
- Admin console available for exploration  
- Demo user credentials are in `.env.example` / realm JSON  

## Not fully wired yet

Gateway runs do **not** yet require a Keycloak access token. Next hardening step: validate JWTs on `/runs` and map `sub` / client id into audit `user_id` / agent client.

Until then, Keycloak proves the Compose IdP is up and ready for OIDC integration.
