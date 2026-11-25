# Changelog

## [2.3.0] - 2026-11-26

### Added
- `/metrikia:dashboard`: one page with the account, the ads, the decisions and the proof of every figure, in the style of metrikia.io. Two views to work on (growth, creative), one that lists where each figure was read. The user keeps or refuses lines on the page and pastes the decisions back.
- A script builds that page. It refuses a figure with no source, a figure that does not add up with the ones beside it, an amount left in cents, a sentence with a number the page does not hold, and an action that can spend without saying how much. It works out what each action adds to the spend of a day, and shows it beside the total an agent announced when the two differ.
- `tests/dashboard/`: what the script refuses.

### Changed
- Working method: before any cause, the sources that are not ads (email, cart reminder, referral) are compared on the two periods. What starts something counts the whole budget it unlocks.

## [2.2.1] - 2026-11-25

### Changed
- Each skill carries the pages it reads, in its own `references/` folder, and names them by their path from that folder. A chat on claude.ai loads the folder of a skill and nothing else. `references/` stays the only source: `scripts/sync-references.sh` writes the copies, and its `--check` refuses one that differs.
- A skill holds in its body the three rules that matter most, for a client that cannot open the page.
- The MCP server is declared in `.mcp.json`, where claude.ai, Cowork and Claude Code read it. The URL is the same.
- A skill answers in the language of the message and reads the period the user names, otherwise the last 30 days.
- The session start hook prints its text and checks the server in two plain commands.
- README: how to add Metrikia on claude.ai, what to do when the sign-in is refused or the plugin is off, what the plugin runs and sends.
- The manifest gives the links to the documentation, the support, the privacy policy and the terms.
- The description of `budget-optimizer` holds more of the words people use for a sales event.

### Fixed
- Amounts in cents. `compare_performance` gives the amounts of its `current` block in cents, like `get_campaign_performance`, and its other blocks in currency units: `weekly-report` and `campaign-audit` did not say so, and a cost per lead could read 100 times too high. The skills say it where they use the field, for the spend anomalies too, and the tools reference gives the unit of every amount.
- A skill that finds no Metrikia tool says how to connect the account and stops there.

### Removed
- The `default_period` and `language` options. Claude Code replaces an option in a skill only when a value was saved: without one, the skill showed the name of the variable.

## [2.2.0] - 2026-11-25

### Added
- `/metrikia:next-actions`: a few actions for today, each on a real object with its reason.
- `/metrikia:trust-check`: whether the figures can carry a decision, what is not reliable and the first thing to fix.
- `references/`: the working method that every skill and sub-agent follows, and what to do when a call is refused. Written once, read when needed.

### Changed
- The skills are rewritten around the agents of Metrikia. A skill asks one good question to the agent whose field it is, when the account lists it, and continues the same conversation for a follow-up. Without an agent, it works with the read tools and says what is missing.
- A skill holds the method only: what to check, whom to ask, what to deliver. It holds no threshold or benchmark any more.
- Every skill answers on one screen and ends with the lines to decide on. The user decides, and nothing is applied without a yes on each line.
- The two sub-agents prepare the questions and hand back the conversations they opened. They are not the agents of Metrikia.
- The assistant tool is `ask_assistant`, to follow version 1.3.0 of the Metrikia MCP server. The former name is no longer listed and still answers. The texts speak of roles only.
- The `default_period` and `language` options have a default value and are used by the skills.
- The MCP server entry of the Claude Code manifest has a `timeout`: an agent that reads the account can take more than a minute to answer.

### Fixed
- `lead-pipeline` and `attribution-deep-dive` use the lead and deal statuses of the server, count with `total` and page through the lists. Their former filters named statuses that do not exist, so the counts were those of the whole list.
- The ads are read and ranked with the figures of the Ads page (`get_ads_performance`).
- The steps of `budget-optimizer` and its graph did not agree. The graphs of the skills are removed: they drew linear lists.
- The tools reference follows the server: tools, parameters, values, limits and error messages.
- The sample reports with invented figures are removed from the skills guide and the README.

### Removed
- Internal details of the server in the architecture and security pages.

## [2.1.0] - 2026-07-27

### Changed
- Skills moved back from flat `commands/*.md` files to `skills/<name>/SKILL.md` directories. The 1.3.0 migration to `commands/` misdiagnosed a nesting bug (`skills/metrikia/<name>/SKILL.md`) as a format problem; the nesting was actually already fixed, and the format itself was never the issue. `skills/*/SKILL.md` is Claude Code's primary skill format and is natively supported by Cursor's manifest as well. Invocations (`/metrikia:weekly-report`, etc.) are unchanged.
- `.claude-plugin/plugin.json` now explicitly declares `"skills": "./skills/"` for auditability (functionally identical to the default, which already scans `skills/`).

## [2.0.0] - 2026-06-17

### Changed (BREAKING)
- Authentication switched from a static API key (`METRIKIA_API_KEY` env var, `X-API-Key` header) to OAuth 2.1 (Authorization Code + PKCE), the mechanism defined by the MCP authorization spec. No key to configure: sign-in happens through a one-time browser flow on the first tool call, and the session renews automatically.

### Migration
- If you had `METRIKIA_API_KEY` set, it is no longer read and can be removed. On your next session, the first Metrikia tool call opens a browser sign-in instead.

## [1.3.0] - 2026-04-01

### Changed
- Skills migrated from `skills/*/SKILL.md` to flat `commands/*.md` files. The nested `SKILL.md` format loaded correctly at runtime but did not surface in Claude Code's CLI autocomplete.
- Auth header switched from `Authorization: Bearer` to `X-API-Key` (superseded by OAuth in 2.0.0).

### Added
- Usage examples in README, from simple status checks to expert-level multi-tool workflows.
- `marketplace.json` restored with corrected GitHub marketplace install instructions.

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
