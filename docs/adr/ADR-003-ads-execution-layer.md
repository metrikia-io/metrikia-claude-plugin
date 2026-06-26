# ADR-003: Ads Execution Layer -- Provider MCPs on Top of Metrikia

## Status

Accepted

## Date

2026-06-26

## Context

Metrikia is the attribution source of truth: it computes MTA + CRM attributed ROAS, MER, and budget advice, exposed through the Metrikia MCP. Until now this plugin was measurement-only: it reads and analyzes, it does not act on platforms.

By 2026 every ad platform ships an official MCP (Meta `mcp.facebook.com/ads`, Google Ads, TikTok), plus a mature unified community server (Pipeboard). This makes it cheap to add an execution layer: turn a Metrikia-informed decision into an action (pause, scale, shift budget, create draft) on the platform, without the plugin maintaining raw API clients.

Two adjacent options were considered and rejected, to keep the plugin coherent and DRY.

## Options Considered

### Option A: Add an execution layer via provider MCPs (CHOSEN)

A single `ads-ops` command that decides from Metrikia attribution and acts through a provider MCP the user wires (Pipeboard recommended). Provider MCPs are opt-in, not a hard dependency: Metrikia stays the only wired server. Created entities land PAUSED.

This turns the plugin into a media-buyer command center: measure (Metrikia) plus act (provider MCPs), while attribution stays exclusively in Metrikia.

### Option B: Add a BigQuery deep-SQL warehouse layer (REJECTED)

Wire a BigQuery MCP and ship a warehouse-setup runbook so the agent can run arbitrary cross-platform historical SQL.

Rejected because:
- It is niche (analyst-grade arbitrary SQL), not a media-buyer daily need.
- It contradicts the product: a Metrikia plugin telling the user to build a parallel ads warehouse undercuts the attribution layer and invites un-attributed platform numbers to be treated as truth.
- It carries real ingestion cost and ops (Data Transfer Service, third-party for TikTok) for a rare need.

Arbitrary historical cross-platform SQL is a legitimate but separate data-warehouse concern, intentionally out of scope here.

### Option C: A separate ads plugin (REJECTED -- DRY violation)

Ship execution and BigQuery as a second plugin alongside this one. Rejected: two plugins both centered on Metrikia is duplication. The execution value belongs inside the Metrikia plugin, not beside it.

## Decision

Add the execution layer (Option A) as the `ads-ops` command. Keep Metrikia as the source of truth and the only hard MCP dependency. Provider MCPs are opt-in. Reject BigQuery (Option B) and a separate plugin (Option C).

## Consequences

Positive:
- One coherent plugin: measure + act, around Metrikia. DRY.
- No new hard dependency: Metrikia stays the only wired server; provider MCPs are opt-in.
- Safety: created entities land PAUSED; every write is confirmed.

Negative / trade-offs:
- Scope expands from measurement to execution. The plugin now positions as a media-buyer command center, not only an attribution reader.
- Provider MCPs are beta; the `ads-ops` command must degrade gracefully when a provider tool changes or fails.
- Arbitrary historical cross-platform analysis is not served here by design; users needing it use a separate warehouse.
