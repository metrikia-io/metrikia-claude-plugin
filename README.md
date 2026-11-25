# Metrikia Plugin for Claude Code

Read your Metrikia account from Claude Code, ask the Metrikia agents open to your account, and get a short list of lines to decide on. Metrikia changes nothing on your ad accounts: the decision stays yours.

## What is Metrikia?

Metrikia is a SaaS platform that links what you spend on ads (Meta, Google, TikTok and other platforms) to the sales you make: store orders, payments and CRM deals. It shows what the ads really bring, next to what each ad platform reports. It is built for media buyers, creative strategists, performance managers, agencies and the brands they work for.

## Installation

### From GitHub (recommended)

No API key to configure. The plugin signs in with OAuth: the first time you call a Metrikia tool, your browser opens to connect your account, and the session renews automatically.

In Claude Code:

```bash
# Step 1: Add the marketplace
/plugin marketplace add metrikia-io/metrikia-claude-plugin

# Step 2: Install the plugin
/plugin install metrikia@metrikia-plugin

# Step 3: Restart Claude Code
exit
claude
```

On the first Metrikia tool call, a browser window opens. Sign in to Metrikia (if needed) and click **Authorize**. That is all: no key to paste.

### From Local Path

```bash
# If you cloned the repo locally
git clone https://github.com/metrikia-io/metrikia-claude-plugin.git
/plugin marketplace add /path/to/metrikia-claude-plugin
/plugin install metrikia@metrikia-plugin
```

### Verify Installation

```bash
# Open plugin manager
/plugin

# Go to "Installed" tab to see metrikia plugin
# Go to "Errors" tab if skills don't appear
```

The plugin runs an automatic health check at startup. If you see **"Metrikia Plugin Active"**, everything is connected.

### Official Marketplace (coming soon)

> When published to the official Claude Code marketplace:
>
> ```bash
> claude plugin install metrikia
> ```

## Health Check

At every session start, the plugin verifies that the MCP server at `mcp.metrikia.io` is reachable. Authentication is handled by OAuth on the first tool call (a one-time browser sign-in), so there is no key to check.

If the server is unreachable, you get a clear warning with instructions, no silent failures.

## What's Inside

### Skills

| Skill | What it answers |
|-------|-------------|
| `/metrikia:next-actions` | What do I do today? A few actions, in order |
| `/metrikia:weekly-report` | How did the week go, and what do I decide for the next one? |
| `/metrikia:budget-optimizer` | Where do I put the money, line by line? |
| `/metrikia:campaign-audit` | This campaign: does it hold my goal, what limits it, what do I change? |
| `/metrikia:creative-analysis` | Which ads sell and why, which wear out, what do we make next? |
| `/metrikia:lead-pipeline` | From the lead to the signed sale: where do people stop, which sources bring the ones who sign? |
| `/metrikia:attribution-deep-dive` | Who really brings the sales: what opens the journeys, what closes them? |
| `/metrikia:trust-check` | Can I decide on these figures, and what is the first thing to fix? |

### How a skill works

1. It asks one good question to the Metrikia agent whose field it is, when your account lists that agent. The agent reads your account and answers with your figures.
2. Without an agent, it works with the read tools and says what is missing.
3. It gives you one screen: what is true, what changed, what explains it, and the few lines to decide on.
4. You decide. If you have a tool of your ad platform connected and ask for it, a line is applied there after your explicit yes on that line.

A skill holds the method: what to check, whom to ask, what to deliver. The expertise comes with the answers of the agents.

### Agents of Metrikia

| Agent | Ask it about |
|-------|-------------|
| Media buyer | Budgets: cut, hold, raise, move, read a test, prepare a sales event |
| Creative strategist | The ads: which sell and why, which wear out, what to make next |
| Data scientist | The truth of the figures: gaps between platforms, Metrikia, store and payments, state of the tracking, does the marketing work as a whole |
| Metrikia Assistant | How the platform works. Open to every account |

The first three are listed only when your account has access to them.

### Sub-agents

| Sub-agent | Use it for |
|-------|-------------|
| `media-buyer` | A longer piece of work on campaigns, budgets and ads |
| `growth-analyst` | A longer piece of work from the click to the sale |

They work on your side, prepare the questions and hand you the list to decide. They are not the agents of Metrikia.

### MCP Tools

18 tools come with every account: 14 to read and ask, 4 to write.

**Ads:** `list_campaigns`, `get_ads_performance`, `get_campaign_performance`, `get_creative_report`, `compare_performance`, `get_budget_advice`, `get_anomalies`

**Sales and attribution:** `get_metrics`, `get_attribution_journey`

**Leads/CRM:** `list_leads`, `get_lead`, `list_deals`

**Data:** `get_sync_status`

**Metrikia Assistant:** `ask_assistant`

**Write:** `create_lead`, `transition_lead`, `create_deal`, `trigger_sync`

The full reference is in [docs/TOOLS-REFERENCE.md](docs/TOOLS-REFERENCE.md).

## Examples

> "What are my three actions for today? The grey lamp is sold out."

`/metrikia:next-actions`: the stock goes into the question, the actions come back with the object, the value today and the next one.

> "My ad platform and my store do not show the same sales. Can I decide on these figures?"

`/metrikia:trust-check`: what each side counts, what can be decided on, and what to fix first.

> "I have a fixed amount for next month. Where do I put it? The catalogue campaign stays as it is."

`/metrikia:budget-optimizer`: the plan line by line with its effect on the daily spend. Keep some lines only and ask again: the plan is sized anew.

> "What do we film next? The best ad opens on a runner lacing shoes at night."

`/metrikia:creative-analysis`: your description is what no tool can see, so it goes with the question.

> "Plenty of leads, few of them sign. What do we do?"

`/metrikia:lead-pipeline`: the leads the platforms count next to the CRM, the step where people stop, and who does what.

## Basic Workflow

1. **Every day**: `/metrikia:next-actions`
2. **A figure looks wrong**: `/metrikia:trust-check`, before any decision that rests on it
3. **Every week**: `/metrikia:weekly-report`
4. **To dig**: `/metrikia:campaign-audit`, `/metrikia:creative-analysis`, `/metrikia:attribution-deep-dive`, `/metrikia:lead-pipeline`
5. **To move money**: `/metrikia:budget-optimizer`

Ask your next question in the same conversation: the agent keeps the thread.

## Configuration

The plugin prompts for these options when enabled:

| Option | Description |
|--------|-------------|
| `default_period` | Period a skill reads when you name none: 7d, 30d, or 90d (default: 30d) |
| `language` | Language of the answers when your message does not tell: en or fr (default: en) |

## Requirements

- [Claude Code](https://claude.ai/claude-code), latest version (plugin marketplaces and MCP OAuth require a recent release)
- A Metrikia account (you authorize access with a one-time browser sign-in, no API key needed)
- `curl` (for automatic health check at startup)

## Support

- [Metrikia AI Integration](https://metrikia.io/integrations/ai)
- [MCP Server Documentation](https://api.metrikia.io/public/api/v1/docs?ui=redoc#section/MCP-Server)
- [API Documentation](https://api.metrikia.io/public/api/v1/docs?ui=redoc)
- [Support](mailto:support@metrikia.io)
- [GitHub Issues](https://github.com/metrikia-io/metrikia-claude-plugin/issues)
