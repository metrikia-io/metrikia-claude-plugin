---
description: Execute ad operations across platforms (pause, scale, shift budget, create draft) via official provider MCPs, deciding from Metrikia attribution and acting with a PAUSED-by-default guardrail
---

# Ads Ops

Act on ad platforms. Metrikia tells you the truth (attributed ROAS); this command turns a decision into an action on Meta, Google Ads, or TikTok. Decide from attribution, act through the provider, never the other way around.

## When to use

Pause, scale, shift budget, or create a draft on a platform. For "what should I do" (analysis), use the analysis commands (budget-optimizer, campaign-audit). This command is the execution step.

## Prerequisite: a provider MCP

Metrikia is the source of truth but does not push changes to platforms. Wire one provider MCP into Claude Code `.mcp.json` (or Hermes `~/.hermes/config.yaml`):

- Unified (recommended): **Pipeboard** (`github.com/pipeboard-co/meta-ads-mcp`) covers Meta + Google + TikTok + Snap + Reddit with one auth.
- Official per-platform: Meta `mcp.facebook.com/ads` (read+write), Google Ads MCP (read-only), TikTok Ads MCP (read+write).

These are beta: pin versions, expect churn. None of them computes attribution: that stays in Metrikia.

## Process

1. **Decide from truth.** Pull the attributed picture first: `get_campaign_performance`, `get_budget_advice`, `get_attribution_journey`, `get_anomalies`. A campaign that looks weak in platform last-click can be a key assist in MTA. Never base the action on platform self-reported numbers.
2. **Resolve the target.** List accounts/campaigns via the provider MCP. Confirm the exact id with the user (account, campaign, current value).
3. **State the action.** Account, campaign, current state/value, proposed change. One action at a time. No bulk destructive changes without an itemized approved list.
4. **Confirm, then write.** Ask the user before any write. Execute via the provider MCP.
5. **Verify.** Read the new state back from the provider MCP and report it.

## Guardrails (non-negotiable)

- **Created entities land PAUSED.** The official MCPs create in a paused state on purpose. Never auto-activate. Surface the draft and require an explicit human go.
- **Confirm before every write.** State the exact target and the before/after value.
- **Truth from Metrikia, action from the provider.** If asked for ROAS, call Metrikia. Provider numbers are a sanity check, not the decision basis.

## Output Format

### Decision basis (Metrikia)
Attributed ROAS / MER and the reason for the action

### Proposed action
Platform | Account | Campaign | Current -> Proposed

### Confirmation
Explicit ask before executing

### Result
New state read back from the provider, plus any created entity left PAUSED

## Process Flow

```
Metrikia (truth) -> decide -> resolve target -> state action -> CONFIRM -> provider MCP write -> verify
```

## Notes

- This command adds an execution layer on top of Metrikia measurement. See ADR-003.
- For arbitrary historical cross-platform SQL beyond Metrikia's schema, that is a separate data-warehouse concern, intentionally out of scope for this plugin (ADR-003).
