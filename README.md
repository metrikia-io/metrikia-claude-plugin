# Metrikia plugin for Claude

Read your Metrikia account from Claude, ask the Metrikia agents open to your account, and get a short list of lines to decide on. Metrikia changes nothing on your ad accounts: the decision stays yours.

## What is Metrikia?

Metrikia is a SaaS platform that links what you spend on ads (Meta, Google, TikTok and other platforms) to the sales you make: store orders, payments and CRM deals. It shows what the ads really bring, next to what each ad platform reports. It is built for media buyers, creative strategists, performance managers, agencies and the brands they work for.

## Install

### Claude Code

In a session:

```bash
/plugin marketplace add metrikia-io/metrikia-claude-plugin
/plugin install metrikia@metrikia-plugin
/reload-plugins
```

From a clone, give its path to the first command: `/plugin marketplace add /path/to/metrikia-claude-plugin`. When a skill runs, Claude Code may ask to read one of its pages: they are text files of the plugin.

### claude.ai and the Claude app

The connector opens your account, the plugin brings the skills. Add both, in this order.

1. **The connector.** Open **Customize**, then **Connectors**. Select **Add**, then **Add custom connector**. Name it Metrikia, give this URL, and keep the settings marked **Detected**:

   ```
   https://mcp.metrikia.io/api/v1/mcp
   ```

   Select **Add**, then **Connect**, and sign in to Metrikia. On a Team or Enterprise plan, an Owner adds the connector once in **Organization settings**, **Connectors**, and each member connects with their own account.

2. **The plugin.** Open **Customize**, then **Plugins**, and select **Add**. Choose **Add marketplace** and enter `metrikia-io/metrikia-claude-plugin`, or choose **Upload plugin** and give the ZIP of this repository (on GitHub: **Code**, **Download ZIP**). Add **Metrikia**. Its **Connectors** tab shows the connector of step 1: the URL is the same, so you have one set of tools.

The skills need **Code execution and file creation**, in **Settings**, **Capabilities**.

| | Chat | Cowork | Claude Code |
|---|---|---|---|
| Skills | Yes | Yes | Yes |
| Metrikia tools | Once connected | Once connected | Once signed in |
| Sub-agents, session start | No | Yes | Yes |

## Sign in

There is no API key. In Claude Code, run `/mcp`, select the Metrikia server (`plugin:metrikia:metrikia`), then **Authenticate**. Your browser opens Metrikia: sign in if needed, read the permissions and click **Authorize**. The session renews on its own. On claude.ai, the connector asks you to sign in when you select **Connect**.

### The sign-in is refused, or never opens

1. The browser does not open: copy the address that Claude Code shows and open it yourself. The browser ends on a connection error: paste the whole address of that page in Claude Code.
2. Check which Metrikia account the browser is signed in to. Then try again: `/mcp`, the Metrikia server, **Clear authentication** if it shows, **Authenticate**.
3. Still refused in Claude Code: add the connector on claude.ai, as above. Claude Code gets it when you sign in to it with the same claude.ai account. The plugin goes first when both give the same URL, so `/mcp` lists the connector as hidden and says how to use it instead.
4. Write to support@metrikia.io with the message as it reads, and the time.

### The plugin is off

1. Run `/plugin`, open the **Installed** tab, select **Metrikia**, then **Enable plugin**, and close the panel.
2. Run `/reload-plugins`, or `/reload-plugins --force` when Claude Code says that the reload changes the MCP tools.
3. Run `/mcp`: the Metrikia server is listed. Sign in there if it asks.

On claude.ai, open the plugin in **Customize**, **Plugins**, and turn its switch on. The **Errors** tab of `/plugin` says why a plugin does not load.

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

Ask your question in plain words: Claude picks the skill. In the chat of claude.ai, `/` lists them too.

### How a skill works

1. It asks one good question to the Metrikia agent whose field it is, when your account lists that agent. The agent reads your account and answers with your figures.
2. Without an agent, it works with the read tools and says what is missing.
3. It gives you one screen: what is true, what changed, what explains it, and the few lines to decide on.
4. You decide. If you have a tool of your ad platform connected and ask for it, a line is applied there after your explicit yes on that line.

A skill holds the method: what to check, whom to ask, what to deliver. The expertise comes with the answers of the agents. It answers in the language of your message and reads the period you name, otherwise the last 30 days. There is no option to set.

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

## What the plugin runs and sends

- At session start, in Claude Code and Cowork, it prints `hooks/session-context.md`, then runs `hooks/health-check.sh`. This script sends one request to `https://mcp.metrikia.io/api/v1/mcp`, with no credential and no data, to say whether the server answers.
- When Claude calls a Metrikia tool, the call goes to that same server with your sign-in: dates, ids, filters, the question for an agent, and the lead or the sale you ask it to write. The answer comes back to Claude.
- It sends nothing anywhere else. It stores nothing and installs nothing.

What the server commits to is in [docs/SECURITY.md](docs/SECURITY.md) and in the [privacy policy](https://metrikia.io/privacy).

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

## Requirements

- A recent [Claude Code](https://claude.ai/claude-code), or claude.ai on a plan that has skills
- A Metrikia account
- `curl` for the check at session start. Without it, the check is skipped

## For contributors

`references/` holds the pages that every skill shares, and it is their only source. A chat on claude.ai loads the folder of a skill and nothing else, so each skill carries a copy. Edit `references/`, never a copy, then:

```bash
./scripts/sync-references.sh           # write the copies
./scripts/sync-references.sh --check   # exit 1 when a skill does not stand on its own
```

The check refuses a copy that differs, is missing or has no source, a skill that does not point to its pages, and a variable or a path that only some clients resolve. Run it before every commit, and `claude plugin validate . --strict` from a clean checkout before a release.

## Support

- [Metrikia AI Integration](https://metrikia.io/integrations/ai)
- [MCP Server Documentation](https://api.metrikia.io/public/api/v1/docs?ui=redoc#section/MCP-Server)
- [API Documentation](https://api.metrikia.io/public/api/v1/docs?ui=redoc)
- [Support](mailto:support@metrikia.io)
- [GitHub Issues](https://github.com/metrikia-io/metrikia-claude-plugin/issues)
