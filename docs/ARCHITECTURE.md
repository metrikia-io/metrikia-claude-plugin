# Metrikia Plugin -- Technical Architecture

Technical reference for the Metrikia Claude Code plugin. Covers plugin structure, MCP integration, skill execution model, agent system, security, and multi-platform support.

## Overview

The Metrikia plugin connects Claude Code (and Cursor) to Metrikia's MCP server, enabling AI assistants to read and write ad performance, CRM, and attribution data without exposing PII. The plugin provides 17 MCP tools, 6 skills, 2 agents, and a session hook.

```
+--------------------------------------------------+
|  User (Media Buyer / Performance Manager)        |
+--------------------------------------------------+
        |
        | Natural language
        v
+--------------------------------------------------+
|  Claude Code (or Cursor)                         |
|  - Loads plugin from .claude-plugin/plugin.json  |
|  - Registers MCP server                          |
|  - Injects session context via hook              |
|  - Exposes skills and agents                     |
+--------------------------------------------------+
        |                           |
        | Skill instructions        | Agent persona
        | (markdown recipes)        | (markdown identity)
        v                           v
+--------------------------------------------------+
|  MCP Tool Calls (JSON-RPC over HTTP)             |
|  OAuth 2.1 Bearer token                          |
+--------------------------------------------------+
        |
        | HTTPS
        v
+--------------------------------------------------+
|  Metrikia MCP Server                             |
|  https://mcp.metrikia.io/api/v1/mcp             |
|  (MCP-compliant backend, EU-hosted)              |
+--------------------------------------------------+
        |
        | Dependency injection
        v
+--------------------------------------------------+
|  Application Layer                               |
|  UseCase + Repository + Domain Services          |
+--------------------------------------------------+
        |
        | Data access layer
        v
+--------------------------------------------------+
|  Database (tenant-scoped) + cache layer          |
|  (sessions, circuit breaker, rate limits)        |
+--------------------------------------------------+
```

## Plugin Structure

```
metrikia-plugin/
|-- .claude-plugin/
|   |-- plugin.json          # Claude Code plugin manifest
|   |-- marketplace.json     # Marketplace listing metadata
|   |-- ignore               # Files excluded from plugin packaging
|
|-- .cursor-plugin/
|   |-- plugin.json          # Cursor plugin manifest (mirrors Claude Code)
|
|-- skills/
|   |-- weekly-report/
|   |   +-- SKILL.md         # Skill definition (frontmatter + instructions)
|   |-- campaign-audit/
|   |   +-- SKILL.md
|   |-- lead-pipeline/
|   |   +-- SKILL.md
|   |-- budget-optimizer/
|   |   +-- SKILL.md
|   |-- creative-analysis/
|   |   +-- SKILL.md
|   +-- attribution-deep-dive/
|       +-- SKILL.md
|
|-- agents/
|   |-- media-buyer.md       # Agent persona definition
|   +-- growth-analyst.md
|
|-- hooks/
|   |-- hooks.json           # Hook configuration
|   +-- session-context.md   # Injected at session start
|
|-- docs/                    # This documentation
|-- README.md
|-- CHANGELOG.md
+-- LICENSE
```

### Conventions

**Plugin manifests** (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`) declare:
- MCP server URL and authentication headers
- Paths to skills, agents, and hooks directories
- User-configurable options (`default_period`, `language`)

**Skill files** use YAML frontmatter (`name`, `description`) followed by markdown instructions that guide Claude through a sequence of MCP tool calls.

**Agent files** use YAML frontmatter (`name`, `description`, `model`) followed by a persona definition with expertise areas and communication style.

**Hooks** use `hooks.json` to declare lifecycle callbacks. Currently, a `SessionStart` hook injects context about available skills, agents, and tools.

## MCP Server Integration

### Registration

The plugin registers the Metrikia MCP server declaratively in `plugin.json`:

```json
{
  "mcpServers": {
    "metrikia": {
      "type": "http",
      "url": "https://mcp.metrikia.io/api/v1/mcp"
    }
  }
}
```

No key or header is declared. Authentication happens through OAuth 2.1, negotiated at runtime by the MCP client (see [SECURITY.md](SECURITY.md) for the full flow).

### Authentication Flow

```
1. Claude Code loads plugin.json and connects to the MCP server
2. The server responds 401 with a WWW-Authenticate header (RFC 9728)
3. Claude Code opens a one-time browser sign-in (OAuth 2.1, PKCE)
4. User logs in to Metrikia and authorizes the requested scopes
5. Claude Code receives a short-lived access token (mko_ prefix) + refresh token
6. Every MCP tool call includes: Authorization: Bearer mko_xxx
7. Metrikia validates the token, checks scopes (mcp:read / mcp:write)
8. User and tenant resolved from the token, every query scoped to that tenant
```

Two scopes exist:
- `mcp:read` -- Required. Grants access to 13 read tools.
- `mcp:write` -- Optional. Grants access to 4 write tools (create_lead, transition_lead, create_deal, trigger_sync).

### Transport

HTTP transport over TLS. The MCP server runs at `https://mcp.metrikia.io/api/v1/mcp`, scaled independently from the main API. Streamable HTTP (SSE) is planned for `ask_diana` in v1.2.

## Skill Execution Model

Skills are **markdown-based orchestration recipes** -- they do not contain executable code. Instead, they provide structured instructions that Claude follows, making MCP tool calls in the prescribed order.

### Anatomy of a Skill

```markdown
---
name: weekly-report
description: Generate a comprehensive weekly ad performance report
---

# Weekly Performance Report

## Process

1. **Fetch current period metrics**
   - Call `get_metrics` with last 7 days
   - Call `compare_performance` with comparisonType: "previous_period"

2. **Identify top performers**
   - Call `get_creative_report` with sortBy: "roas", limit: 5

...

## Output Format

### Performance Summary
- Total Spend | Revenue | Profit
- MER | ROAS | CRM ROAS
...

## Red Flags
- MER dropping >20% week-over-week ...

## Error Handling
- If rate limited (429) ...
```

### Execution Sequence

```
User: "/metrikia:weekly-report"
    |
    v
Claude reads SKILL.md instructions
    |
    v
Step 1: get_metrics(startDate="-7d") --> MCP server --> JSON response
Step 2: compare_performance(comparisonType="previous_period") --> JSON
Step 3: get_creative_report(sortBy="roas", limit=5) --> JSON
Step 4: get_anomalies() --> JSON
Step 5: get_budget_advice(period="7d") --> JSON
Step 6: ask_diana("Based on this week's performance...") --> JSON
    |
    v
Claude synthesizes all responses into the prescribed Output Format
    |
    v
Structured report presented to user
```

### Why Markdown, Not Code

Skills are intentionally markdown, not TypeScript or Python. See [ADR-002](adr/ADR-002-skill-design-philosophy.md) for the full rationale. In short:
- Claude understands intent and adapts to edge cases (empty data, errors, partial results).
- No build step, no runtime dependencies.
- Users can read and understand what a skill does before running it.
- The same skill works across Claude Code and Cursor without platform-specific code.

## Agent System

Agents are persistent personas that use MCP tools proactively rather than following a scripted sequence.

### Media Buyer Agent

Expert in campaign optimization, budget allocation, and scaling strategies. Starts with data (`get_metrics`, `list_campaigns`) before making any recommendation. Focuses on ROAS, MER, creative performance, and cross-platform synergy.

### Growth Analyst Agent

Bridges marketing spend and sales revenue. Works backwards from deals to understand true ROI. Focuses on attribution journeys, conversion paths, lead quality, and long-term trends (30-90 day windows).

### Agent vs Skill

| Aspect | Skill | Agent |
|--------|-------|-------|
| Invocation | `/metrikia:skill-name` | Selected as active agent |
| Execution | Scripted sequence of tool calls | Autonomous, goal-driven |
| Output | Structured report (prescribed format) | Conversational, adaptive |
| Best for | Repeatable analyses | Open-ended exploration |
| Tool usage | Prescribed order | Chooses tools based on context |

## Hook System

The plugin uses a `SessionStart` hook to inject context when Claude Code initializes:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cat \"${CLAUDE_PLUGIN_ROOT}/hooks/session-context.md\"",
            "async": false
          }
        ]
      }
    ]
  }
}
```

The `session-context.md` file provides Claude with:
- List of available skills and when to use each
- List of agents and their focus areas
- Categorized list of all 17 MCP tools
- Reminder to always fetch data before making recommendations

The empty `matcher` means the hook fires on every session start, regardless of project context.

## Security Model

### API Key Scopes

| Scope | Tools | Count |
|-------|-------|-------|
| `mcp:read` | list_leads, get_lead, list_campaigns, get_campaign_performance, get_creative_report, get_metrics, compare_performance, list_deals, get_attribution_journey, get_anomalies, get_budget_advice, get_sync_status, ask_diana | 13 |
| `mcp:write` | create_lead, transition_lead, create_deal, trigger_sync | 4 |

### PII Masking

The MCP server enforces a strict PII invariant at the tool level. Every tool uses explicit field mapping -- no automatic entity serialization.

**Never exposed:** email addresses, phone numbers, social media handles, hashed PII (nameHash, emailHash).

**Safe to expose:** UUIDs, full names (first + last only), statuses, source labels, campaign names, monetary amounts, timestamps, attribution data.

### Rate Limiting

| Category | Limit | Window |
|----------|-------|--------|
| Read tools | 60 requests | 1 minute |
| Diana AI | 10 requests | 5 minutes |
| Write tools | 30 requests | 1 minute |
| Sync trigger | 5 requests | 1 hour |

Implemented via a sliding window rate limiter. Returns HTTP 429 with `Retry-After` header when exceeded.

### Circuit Breaker (Diana AI)

`ask_diana` calls an AI model internally (AI-calling-AI). A circuit breaker prevents runaway loops:

```
Closed (normal) --5 failures--> Open (blocked, 30s cooldown)
                                    |
                                   30s
                                    |
                                    v
                              Half-Open (1 probe request)
                              /                         \
                         success                      failure
                            |                            |
                            v                            v
                         Closed                        Open
```

- Threshold: 5 consecutive failures within 5 minutes
- Cooldown: 30 seconds
- Storage: shared cache, keyed per tenant, cross-instance

### Multi-Tenancy

Every MCP query is filtered by tenant at three levels:
1. **Data layer:** every repository query is scoped to the tenant
2. **ORM layer:** a global tenant filter is active on all entities
3. **Tool layer:** every tool explicitly resolves and passes the tenant

## Multi-Platform Support

The plugin ships with two manifest directories:

| Platform | Manifest | Key Differences |
|----------|----------|-----------------|
| Claude Code | `.claude-plugin/plugin.json` | Includes `skills`, `agents`, `hooks` paths |
| Cursor | `.cursor-plugin/plugin.json` | Same MCP server config, same `userConfig` |

Both platforms share the same MCP server URL and authentication mechanism. Skills and agents are available wherever the platform supports them. The MCP tool calls are identical regardless of client.

## Data Flow

Complete data flow for a skill execution:

```
User: "/metrikia:weekly-report"
  |
  v
Claude Code
  |-- Reads skills/weekly-report/SKILL.md
  |-- Follows Process steps 1-6
  |
  |-- Step 1: POST https://mcp.metrikia.io/api/v1/mcp
  |     Body: {"jsonrpc":"2.0","method":"tools/call",
  |            "params":{"name":"get_metrics",
  |                      "arguments":{"startDate":"2026-03-25","endDate":"2026-04-01"}}}
  |     Auth: Bearer mko_xxx
  |
  v
Metrikia MCP Server
  |-- Validates the session token, checks mcp:read scope
  |-- Resolves the authenticated user and tenant
  |-- Dispatches to the metrics use cases
  |     |-- Computes MER for the date range
  |     |-- Computes real ROAS for the date range
  |     +-- Returns: {period, mer, totalRevenue, totalSpend, roas, ...}
  |
  v
Database (tenant-scoped queries)
  |-- Performance data filtered by tenant and date range
  |-- Deals filtered by tenant and close date
  |
  v
JSON response -> Claude Code -> Synthesized report -> User
```

## Extension Points

### Adding a New Skill

1. Create `skills/my-skill/SKILL.md` with YAML frontmatter and process instructions.
2. The plugin auto-discovers skills from the `skills/` directory.
3. No code changes needed -- just markdown.

### Adding a New Agent

1. Create `agents/my-agent.md` with YAML frontmatter and persona definition.
2. Auto-discovered from the `agents/` directory.

### Server-Side Tool Additions

When new MCP tools are added to the Metrikia backend, they are auto-discovered at boot time. The plugin picks them up automatically on the next session -- no plugin update needed for new tools.

---

**Version:** 1.0.0
**Last Updated:** April 2026
**Transport:** HTTP (Streamable HTTP planned v1.2)
