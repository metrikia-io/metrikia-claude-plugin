# Metrikia Plugin: Architecture

How the plugin is built: its parts, how a skill runs, and how it talks to the Metrikia MCP server. The server itself is described by what it lists to your client ([TOOLS-REFERENCE.md](TOOLS-REFERENCE.md)) and by its commitments ([SECURITY.md](SECURITY.md)).

## Overview

```
You
 |  a question, or /metrikia:<skill>
 v
Claude Code or Cursor
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
|   |-- plugin.json          # Claude Code manifest
|   |-- marketplace.json     # Marketplace listing
|   +-- ignore               # Files left out of the package
|-- .cursor-plugin/
|   +-- plugin.json          # Cursor manifest
|-- skills/<name>/SKILL.md   # One folder per skill, with its own pages when it needs them
|-- references/
|   |-- working-method.md    # The method every skill and sub-agent follows
|   +-- errors.md            # What to do when a call is refused or comes back empty
|-- agents/
|   |-- media-buyer.md       # Sub-agent: budgets and ads
|   +-- growth-analyst.md    # Sub-agent: from the click to the sale
|-- hooks/
|   |-- hooks.json           # Session start hook
|   |-- health-check.sh      # Reachability check, prints the session context
|   +-- session-context.md   # What the client knows at session start
|-- docs/
|-- README.md
|-- CHANGELOG.md
+-- LICENSE
```

## MCP server registration

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

No key and no header is declared: the client negotiates OAuth 2.1 at the first call. The `timeout` leaves an agent the time to read the account before it answers. It is a limit in milliseconds, per call, and changes nothing for the other tools, which answer in seconds.

## How a skill runs

A skill is a markdown file that says what to ask, what to read and what to deliver. Three levels of text, loaded when needed:

1. **The description** is always in view. It says when to use the skill, never how.
2. **The skill** is read when it runs: its question, its reads, its way of working without an agent, its delivery.
3. **The working method** is read once per session, and a page such as `errors.md` or `funnel.md` only when the case comes up.

```
1. Look at the tool list
     |-- the agent of the skill is listed  --> ask it one question
     |-- another agent is listed           --> ask that one
     +-- no agent is listed                --> read tools, and say what is missing
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

The hook checks that the server is reachable, then prints `session-context.md`: the skills and when to use them, the tools, four reminders. It runs on every session start and needs no key.

## Multi-platform

| Platform | Manifest | Notes |
|----------|----------|-------|
| Claude Code | `.claude-plugin/plugin.json` | Skills, sub-agents, hook, options |
| Cursor | `.cursor-plugin/plugin.json` | Same server, same skills and sub-agents |

Both read the same files. Claude Code fills in the plugin options and the path of the plugin inside a skill. On another client, the skill falls back on the language of your message and on the relative path.

## Extending

- **A skill**: add `skills/<name>/SKILL.md`. Its description says when to use it. Its body points to the working method and holds one question, the reads it needs, the way to work without an agent and what to deliver.
- **A sub-agent**: add `agents/<name>.md`, with the same pointer.
- **A tool**: nothing to do here. The server lists its tools to the client, and a skill reads their schema at call time.
