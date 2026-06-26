# Changelog

## [2.1.0] - 2026-06-26

### Added
- `ads-ops` command: an execution layer that turns a Metrikia-informed decision into an action (pause, scale, shift budget, create draft) on Meta / Google Ads / TikTok via official or unified (Pipeboard) provider MCPs. Decisions are driven by Metrikia attribution; created entities land PAUSED; every write is confirmed.
- ADR-003: Ads Execution Layer. Documents adding provider MCPs on top of Metrikia, and the explicit rejection of a BigQuery warehouse layer (niche, out of product scope) and of a separate ads plugin (DRY violation).

### Changed
- Plugin positioning extended from measurement-only to a media-buyer command center: measure with Metrikia, act through provider MCPs. Metrikia remains the source of truth and the only hard MCP dependency; provider MCPs are opt-in.

## [1.2.1] - 2026-04-01

### Fixed
- Revert nested `skills/metrikia/` directory - Claude Code resolves namespace from plugin.json `name`, not directory structure
- Skills now correctly register as `/metrikia:weekly-report` instead of `/weekly-report (metrikia)`

## [1.2.0] - 2026-04-01

### Changed
- Skills restructured under `skills/metrikia/` namespace directory for proper `/metrikia:*` prefixing in Claude Code
- Skills now register as `/metrikia:weekly-report`, `/metrikia:campaign-audit`, etc. instead of `/weekly-report (metrikia)`

### Fixed
- Skill namespace alignment with Claude Code plugin convention (matching ai-craftsman-superpowers pattern)

## [1.1.0] - 2026-04-01

### Added
- MCP health check at SessionStart (validates API key + server connectivity)
- Defensive guards in health check (CLAUDE_PLUGIN_ROOT, session-context.md existence)

### Fixed
- `userConfig` aligned with official Claude Code plugin schema (`type`/`title`/`description`/`sensitive`)
- Agent frontmatter: removed undocumented `model: inherit`
- `homepage` updated to `https://metrikia.io/integrations/ai`

### Changed
- README rewritten: local-first installation, correct CLI commands (`claude --plugin-dir`), health check section
- Installation docs now distinguish local install (current) from marketplace (coming soon)

### Removed
- `marketplace.json` (not needed for official marketplace submission)

## [1.0.0] - 2026-04-01

### Added
- Initial release
- 6 skills: weekly-report, campaign-audit, lead-pipeline, budget-optimizer, creative-analysis, attribution-deep-dive
- 2 agents: media-buyer, growth-analyst
- MCP server integration (17 tools: 13 read + 4 write)
- SessionStart hook for context injection
- Multi-platform support (Claude Code + Cursor)
