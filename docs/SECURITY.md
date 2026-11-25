# Metrikia Plugin -- Security and Compliance

Security architecture for the Metrikia Claude Code plugin and MCP server integration. Covers authentication, authorization, data isolation, PII protection, rate limiting, and GDPR considerations.

## OAuth Authentication

The plugin authenticates with OAuth 2.1 (Authorization Code + PKCE), the mechanism defined by the MCP authorization specification. There is no API key to configure or store.

### Sign-in flow

On the first tool call, Claude Code discovers the authorization server from the MCP endpoint (a `401` with a `WWW-Authenticate` header pointing to the Protected Resource Metadata, RFC 9728), then runs a one-time browser sign-in: you log in to Metrikia and authorize the requested scopes. Claude Code receives a short-lived access token and a refresh token, and renews the session automatically.

### Token handling

| Property | Value |
|----------|-------|
| Access token | Opaque, `mko_` prefix (never a JWT), short-lived |
| Transport | `Authorization: Bearer mko_...` |
| Refresh | Automatic, with refresh-token rotation (reused tokens revoke the whole chain) |
| Storage | Managed by Claude Code's MCP client, not by a shell environment variable |

The access token is opaque and validated server-side by lookup, so it can be revoked immediately. The server stores only a keyed hash of each token, never the raw value.

### Best practices

1. **Authorize only the scopes you need.** The consent screen lists the requested access before you approve.
2. **Revoke access when no longer needed.** In **Metrikia Settings**, security and access section, revoke the connected application. Revocation cuts off access immediately.
3. **Sign in per account.** Each sign-in binds the session to your tenant.

## Scopes

The OAuth access token is scoped to control access:

| Scope | Purpose | Tools Granted |
|-------|---------|---------------|
| `mcp:read` | Read-only access to all data | list_leads, get_lead, list_campaigns, get_campaign_performance, get_creative_report, get_metrics, compare_performance, list_deals, get_attribution_journey, get_anomalies, get_budget_advice, get_sync_status, ask_assistant |
| `mcp:write` | CRM write operations | create_lead, transition_lead, create_deal, trigger_sync |

MCP scopes are separate from REST API scopes (`leads:read`, `deals:write`, etc.). An MCP token cannot access REST API endpoints and vice versa.

Write tools require **both** `mcp:read` and `mcp:write` scopes. A token with only `mcp:write` will be rejected.

### Scope Enforcement

Scope checking happens at two levels:

1. **Authentication layer:** the token authenticator validates the token and loads the authenticated user.
2. **Tool level:** write tools explicitly check for the `mcp:write` scope before executing.

If a tool is called without the required scope, the server returns HTTP 403 Forbidden.

## Multi-Tenancy and Data Isolation

Every MCP request is bound to a single tenant. Cross-tenant data access is impossible by design.

### Triple Enforcement

| Layer | Mechanism | Description |
|-------|-----------|-------------|
| Data layer | Tenant filter | Every repository query includes a tenant filter |
| ORM | Global filter | Active on all entities, applied automatically |
| Tool | Explicit resolution | Every tool explicitly resolves and passes the tenant |

### Isolation Guarantee

- A user's session is bound to their tenant at sign-in.
- The authenticated user and their tenant are resolved from the security token on every request.
- Tools pass the tenant to every repository method. There is no way to query across tenants -- it does not exist in the repository interfaces.
- Even if a user knows another tenant's UUID, the query will return no results because the tenant filter is applied at the data layer.

## PII Masking

The MCP server enforces a strict PII invariant: **no personally identifiable information is ever returned in MCP responses.**

This is a design invariant, not a configurable option.

### What is NEVER Exposed

| Data | Reason |
|------|--------|
| Email addresses | PII -- direct identifier |
| Phone numbers | PII -- direct identifier |
| Social media handles | PII -- can identify individuals |
| Hashed PII (emailHash, nameHash, phoneHash) | Hashes are reversible with rainbow tables for common values |
| IP addresses | PII under GDPR |
| Social profiles (JSON) | May contain identifiers |

### What IS Exposed

| Data | Reason |
|------|--------|
| Lead UUID | Non-identifying internal identifier |
| Full name (firstName + lastName) | Necessary for human context; non-unique identifier |
| Lead status | Business state, not PII |
| Source label | Acquisition channel, not PII |
| Estimated revenue | Business metric |
| Timestamps (createdAt, updatedAt) | Operational data |
| Campaign names | Business label |
| Deal amounts and currency | Financial metric |
| Attribution data (touchpoints, credits) | Anonymized journey data |
| Ad performance metrics | Aggregated business data |

### Enforcement Mechanism

PII exclusion is enforced by **explicit field mapping** in every tool. There is no automatic entity serialization -- every field returned to the MCP client is deliberately chosen from an allowlist. Fields like email, phone, and any hashed PII are never on that allowlist, so they cannot leak through a future change by omission.

## Rate Limiting

Rate limits prevent abuse and protect shared infrastructure. They are implemented per token using a sliding window rate limiter.

### Limits by Category

| Category | Limit | Window | Applies To |
|----------|-------|--------|------------|
| `mcp_read` | 60 requests | 1 minute | All 12 read tools |
| Metrikia Assistant | 10 requests | 5 minutes | ask_assistant only |
| `mcp_write` | 30 requests | 1 minute | create_lead, transition_lead, create_deal |
| `mcp_sync` | 5 requests | 1 hour | trigger_sync only |

### Rate Limit Response

When a limit is exceeded:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 42
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Retry after 42 seconds.",
  "retryAfter": 42
}
```

Most AI clients (Claude Code, Cursor) automatically respect the `Retry-After` header and retry transparently.

### Why Different Limits

- **Read tools (60/min):** AI agents are bursty -- a skill may chain 5-10 tool calls in rapid succession. 60/min accommodates this while preventing abuse.
- **Metrikia Assistant (10/5min):** An answer takes longer than a data read. Ask one strategic question instead of many tactical ones.
- **Write tools (30/min):** Lower than read to prevent accidental bulk operations (e.g., an agent creating 100 leads in a loop).
- **Sync (5/hour):** Syncs trigger external API calls to Meta/Google/TikTok. Too many syncs can exhaust platform rate limits.

## Circuit Breaker

The `ask_assistant` tool is protected by a circuit breaker to prevent cascading failures when the Metrikia Assistant is unavailable.

### State Machine

```
         normal operation
              |
              v
+--------+  5 consecutive  +---------+
| CLOSED | ---failures----> |  OPEN   |
+--------+                  +---------+
    ^                           |
    |                          30s cooldown
    |                           |
    |                           v
    |                     +-----------+
    +----success---------| HALF-OPEN |
                          +-----------+
                               |
                            failure
                               |
                               v
                          +---------+
                          |  OPEN   |
                          +---------+
```

### Parameters

| Parameter | Value |
|-----------|-------|
| Failure threshold | 5 consecutive failures |
| Failure window | 5 minutes |
| Cooldown period | 30 seconds |
| Half-open probes | 1 request |
| Storage | Shared cache, keyed per tenant |

### Behavior When Open

When the Metrikia Assistant is temporarily unavailable, `ask_assistant` returns immediately:

```json
{
  "answer": "Metrikia Assistant is temporarily unavailable. Please try again in a moment.",
  "conversationId": null
}
```

This is not an error -- it is a graceful degradation. The rest of the MCP tools continue working normally.

## Prompt Injection Protection

For a question asked through `ask_assistant`, the Metrikia Assistant can:

1. Apply MCP-specific guardrails (e.g., refuse to execute commands).
2. Adapt response format for AI client consumption.
3. Sandbox the conversation separately from the web UI conversations.

The Metrikia Assistant also has its own prompt injection defenses, which are not documented here as they are part of the main Metrikia platform.

## GDPR Considerations

### Data Processing

- **MCP tools do not process PII.** Emails, phones, and hashes are never transmitted to the AI client.
- **Names are exposed** for operational context. Under GDPR, names alone are contextual identifiers, not unique identifiers.
- **Anonymized leads** are marked with `isAnonymized: true`. Their name fields contain placeholder values after GDPR anonymization.

### Data Residency

- The MCP server runs on EU-hosted infrastructure.
- Tenant data, sessions, and authentication data are all hosted in the EU.

### Right to Erasure

When a lead exercises their right to erasure:
1. `Lead::archive()` purges firstName, email, phone, and all hash fields.
2. The lead's `isAnonymized` field is set to true.
3. MCP tools will return the anonymized lead with placeholder data.
4. Attribution data is retained but de-linked from PII.

### Data Retention

- MCP sessions: short-lived, capped TTL.
- Access tokens: short-lived; refresh tokens are revoked immediately on sign-out.
- Anomaly data: 30 days rolling window.
- Performance data: retained per tenant retention policy.

## Incident Response

### Compromised Access

1. Immediately revoke the connected application in **Metrikia Settings**, security and access section.
2. Sign in again to issue a fresh token.
3. Review audit logs for unauthorized access.

### Suspicious Activity

Rate limiting and circuit breaker automatically mitigate most abuse patterns. If you suspect unauthorized access:

1. Revoke the connected application's access.
2. Contact support@metrikia.io with the suspected timeframe.
3. Metrikia can provide access logs for your tenant.

## Security Checklist

- [ ] Only the scopes you actually need are authorized (`mcp:read` only if write is not needed)
- [ ] The connected application is reviewed periodically in **Metrikia Settings**
- [ ] Team members sign in individually, not through a shared account
- [ ] Unused connected applications are revoked promptly
