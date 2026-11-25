# Metrikia Plugin: Security and Privacy

What the plugin and the MCP server commit to: sign-in, permissions, isolation, what is returned and what never is, limits, and what to do when something goes wrong.

## Sign-in

The plugin signs in with OAuth 2.1 (Authorization Code with PKCE), as the MCP authorization specification defines it. There is no API key to configure or to store.

When you connect, your client opens a Metrikia page in your browser: from `/mcp` in Claude Code, from **Customize**, **Connectors** on claude.ai. You sign in, read the permissions, and authorize or refuse. The client then keeps a short-lived access token and renews it on its own.

- The access token is opaque: it carries no data, and the server can end it at any time.
- A session is bound to one person and one account. Each member of a team signs in on their own.
- To stop: clear the sign-in of the Metrikia server in your client (`/mcp` in Claude Code, **Customize**, **Connectors** on claude.ai), or remove the plugin.

## Permissions

| Permission | What it opens |
|---|---|
| `mcp:read` | The read tools, the Metrikia Assistant, and the agents open to the account |
| `mcp:write` | `create_lead`, `transition_lead`, `create_deal`, `trigger_sync` |

The authorization page lists what is asked before you accept. A write tool refuses a session that does not hold `mcp:write`.

On top of these permissions, each tool follows the role of the person in the account: a role that cannot open a page of the app does not get its figures here. The answer is then `access_denied` with the reason.

## One account per session

Your session reads your account, and no other. Knowing the id of something in another account gives nothing: the server answers that it does not exist.

## What the tools return

| Never returned as a field | Returned |
|---|---|
| Email addresses of leads and customers | Names of leads |
| Phone numbers | Status, source, dates, setter and closer ids of a lead |
| Social profiles | Internal notes written on a lead |
| Payment details | Amounts, currency and dates of deals |
| | Customer journeys: channels, campaigns, landing pages |
| | Ad figures, sales figures, campaign and ad names |

Names and notes are personal data. They reach your AI client when you ask for a lead: use them as you would in the app, and keep free text clean of contact details.

`create_lead` accepts an email address and a phone number that you give, to link the lead to its visits. No tool gives them back.

An erased lead stays erased: its personal data is removed for good, it is absent from the lists, and no change applies to it.

## Writing

- Metrikia and its agents change nothing on an ad account.
- The four write tools are used after an explicit yes on each line, never by a skill on its own.
- A change on an ad platform is made by the tool of that platform, if you connected one and asked for it, after the same yes.

## Untrusted text

The dashboard page shows every name as text, never as HTML, and its own policy forbids any request to the network.

A campaign name, a note or a page title can contain anything. The server tells the client to treat every tool result as data, and the skills repeat it: a text that reads like an order is reported, never followed.

An agent reads the account through read tools only: no question makes it change anything.

## Limits

| What | Limit |
|---|---|
| Tool calls | 60 calls per minute per user, with bursts up to 120 calls |
| `ask_assistant` | 10 questions per 5 minutes per user |
| Each agent | 10 questions per 5 minutes per user, 30 questions per 5 minutes for the whole account, and the daily budget of the account |
| `trigger_sync` | 10 syncs per 5 minutes for the whole account, shared with the app |
| Any request to the server | 600 requests per minute per user |

A refused call comes back as a tool error that names the limit and the delay: `Rate limit reached (...). Retry in N seconds.` The response also carries `Retry-After`.

When an agent or the Metrikia Assistant is temporarily unavailable, its tool says so and every other tool keeps working.

## Privacy

- Metrikia processes the data of your account as your processor, under the data processing agreement of your contract. The sub-processors, the AI providers that write the answers of the agents and of the assistant among them, are listed on the [Trust page](https://metrikia.io/trust).
- The tool results you read are sent to the AI client you chose. Its own terms apply to them.
- Application servers and databases are hosted in the European Union.

## If something goes wrong

1. Clear the sign-in of the Metrikia server in the client, then remove the plugin.
2. Write to support@metrikia.io with the dates you suspect.
3. Sign in again once it is settled.

## Checklist

- [ ] Authorize the write permission only if you need it
- [ ] Each member signs in on their own
- [ ] Clear the sign-in on a computer that changes hands
- [ ] Keep contact details out of notes and campaign names
