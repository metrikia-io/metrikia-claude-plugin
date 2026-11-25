# Metrikia Plugin: Architecture

How the plugin is built: its parts, how a skill runs, and how it talks to the Metrikia MCP server. The server itself is described by what it lists to your client ([TOOLS-REFERENCE.md](TOOLS-REFERENCE.md)) and by its commitments ([SECURITY.md](SECURITY.md)).

## Overview

```
You
 |  a question, or /metrikia:<skill>
 v
Claude Code, Cowork, a chat on claude.ai, or Cursor
 |  skills, sub-agents and session context of the plugin (text files)
 |  your other tools, for instance the one of an ad platform
 v
Metrikia MCP server (https, OAuth 2.1)
 |  read tools, write tools, Metrikia Assistant, agents open to your account
 v
Your Metrikia account
```

The plugin runs no code of its own besides a reachability check at session start. Skills, sub-agents and session context are text that the client reads.

## Structure

```
metrikia-plugin/
|-- .claude-plugin/
|   |-- plugin.json          # Manifest for Claude
|   |-- marketplace.json     # Marketplace listing
|   +-- ignore               # Files left out of the package
|-- .cursor-plugin/
|   +-- plugin.json          # Cursor manifest
|-- .mcp.json                # The Metrikia MCP server
|-- skills/<name>/
|   |-- SKILL.md             # The skill, with its own pages when it needs them
|   +-- references/          # Copies of the shared pages, written by a script
|-- references/
|   |-- working-method.md    # The method every skill and sub-agent follows
|   +-- errors.md            # What to do when a call is refused or comes back empty
|-- agents/
|   |-- media-buyer.md       # Sub-agent: budgets and ads
|   +-- growth-analyst.md    # Sub-agent: from the click to the sale
|-- hooks/
|   |-- hooks.json           # Session start: prints the context, checks the server
|   |-- health-check.sh      # Reachability check
|   +-- session-context.md   # What the client knows at session start
|-- scripts/
|   |-- sync-references.sh   # Writes the copies of references/, or checks them
|   +-- bump-version.sh      # Writes the version in the three manifests
|-- docs/
|-- README.md
|-- CHANGELOG.md
+-- LICENSE
```

## MCP server registration

In `.mcp.json`, at the root of the plugin: Claude Code, Cowork and claude.ai read it there. Cursor has the same server in its own manifest.

```json
{
  "mcpServers": {
    "metrikia": {
      "type": "http",
      "url": "https://mcp.metrikia.io/api/v1/mcp",
      "timeout": 180000
    }
  }
}
```

No key and no header is declared: the client negotiates OAuth 2.1 when the user connects. The URL is the same everywhere, so a person who has both the connector of claude.ai and the plugin sees one set of tools. The `timeout` leaves an agent the time to read the account before it answers. It is a limit in milliseconds, per call, and changes nothing for the other tools, which answer in seconds.

## How a skill runs

A skill is a markdown file that says what to ask, what to read and what to deliver. Three levels of text, loaded when needed:

1. **The description** is always in view. It says when to use the skill, never how.
2. **The skill** is read when it runs: its question, its reads, its way of working without an agent, its delivery.
3. **The working method** is read once per session, and a page such as `errors.md` or `funnel.md` only when the case comes up.

Every page a skill reads is in its own folder, and the skill names it by its path from that folder. A chat on claude.ai loads the folder of a skill and nothing else, so `scripts/sync-references.sh` copies `references/` into each one. The body of a skill also holds the three rules that matter most, for a client that cannot open the page. A skill uses no plugin variable: a client that does not know it would show its name instead of its value.

```
1. Look at the tool list
     |-- the agent of the skill is listed  --> ask it one question
     |-- another agent is listed           --> ask that one
     |-- no agent is listed                --> read tools, and say what is missing
     +-- no Metrikia tool is listed        --> say how to connect the account
2. Read only what must be shown
3. Answer on one screen: what is true, what changed, what explains it, what to decide
4. The user decides, line by line
```

The plugin holds the method. Thresholds, benchmarks and rules of thumb are not in it: the agents of Metrikia apply theirs to the data of the account, on the server. See [ADR-002](adr/ADR-002-skill-design-philosophy.md).

## Skills, sub-agents, agents of Metrikia

| | Where it runs | What it does |
|---|---|---|
| Skill | Your client | One analysis, one screen, one decision |
| Sub-agent | Your client, in its own context | A longer piece of work. Hands back the lines to decide and the conversations opened with the agents |
| Agent of Metrikia | The server | Reads the account and answers a question. Listed when your account has access to it |

## Session start

The hook has two commands that run side by side: one prints `session-context.md` (the skills and when to use them, the tools, four reminders), the other checks that the server answers. It runs on every session start and needs no key.

## Where it runs

| Client | Manifest | What it loads |
|----------|----------|-------|
| Claude Code | `.claude-plugin/plugin.json`, `.mcp.json` | Skills, sub-agents, hook, server |
| Cowork | The same | Skills, sub-agents, hook. The server from the Connectors tab of the plugin |
| Chat on claude.ai | The same | Skills. The server from the Connectors tab of the plugin |
| Cursor | `.cursor-plugin/plugin.json` | Same server, same skills and sub-agents |

They read the same files. A sub-agent reads the method through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code fills in.

## Extending

- **A skill**: add `skills/<name>/SKILL.md`, then run `./scripts/sync-references.sh`. Its description says when to use it. Its body points to `references/working-method.md` and `references/errors.md`, and holds one question, the reads it needs, the way to work without an agent and what to deliver.
- **A shared page**: edit it in `references/`, then run the same script. `--check` refuses a copy that differs.
- **A sub-agent**: add `agents/<name>.md`, with a pointer to `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`.
- **A tool**: nothing to do here. The server lists its tools to the client, and a skill reads their schema at call time.
