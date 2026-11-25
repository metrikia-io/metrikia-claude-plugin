---
name: lead-pipeline
description: Use when the user asks about leads, appointments, deals or the sales pipeline, which sources bring leads that sign, why leads do not turn into sales, or who to follow up first.
---

# Lead pipeline

From the lead to the signed sale: where people stop, which sources bring the ones who sign, what to do first.

First read `references/working-method.md`, in the folder of this skill. Every Metrikia skill holds the same page: once per session is enough. Answer in the language of the user. Period: the one the user names, otherwise the last 30 days, ending yesterday.

Three rules hold even without that page: every call on a period carries the same first and last day, the figures of an agent stay as written, and the user decides line by line. No Metrikia tool is listed: the account is not connected (`/mcp` in Claude Code, Customize then Connectors on claude.ai), give no figure and no advice of your own. `references/errors.md` has the steps, and what to do when a call is refused or empty.

## Ask the data scientist

`ask_data_scientist` sets the leads the platforms count against the CRM, and it answers the sales roles that cannot open the ads.

> Over [period], from the lead to the signed sale, which sources and campaigns bring the leads that become appointments and sales, where do they stop and since when, and what are the three things to do first? Compare the leads the platforms count with the CRM. My goal: [goal]. [facts: call-back, team, offer]

Follow-up with the `conversationId`: one source, one step, or a cause the user brings. A change on the ads is a question for the media buyer, only if the user asks.

With an agent, read the CRM only for what the user asks to see.

## Without an agent

Read `funnel.md`, in the folder of this skill, before any call: it holds the statuses that exist and how to count. Then:

1. Count the leads and the deals at each status.
2. Read the period the user asks for, page by page.
3. `get_ads_performance` with `level: "campaigns"`: for each campaign, the leads the platform counts next to the `crm` block (leads, cost per lead, appointments, deals).
4. Say what is missing: the time between two steps, the cause of a weak one.

The same file serves "who do I call first" and "how did this lead come".

## Deliver

1. Where the pipeline loses people, in one sentence.
2. One table: the steps with their counts, or the sources with their leads, appointments and sales. Say the period, or "today" for the state of the day.
3. What explains the weak step, and what could contradict it: the ads, the call-back, the offer or the tracking.
4. The actions, numbered, with who does each one. Ask which ones the user keeps.

A lead counts for what it becomes. A cost per lead that a platform gives is its own count. Names of leads appear when the user asks for the list, not before, and nothing changes in the CRM without a yes on each lead.
