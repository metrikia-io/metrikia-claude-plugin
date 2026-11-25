---
name: campaign-audit
description: Use when the user names one campaign and asks why it drops, whether it works, or whether to keep, change or stop it, or says "audit this campaign", "audite cette campagne".
---

# Campaign audit

One campaign, read in its account: does it hold the goal, what limits it, what to change on it.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`. Period: the one the user names, otherwise `${user_config.default_period}`.

## Read

1. `get_ads_performance` with `level: "campaigns"` and `limit: 200`: find the campaign by its name. Two names match: ask which one. None does: `list_campaigns`. Keep its `id`, its `status`, its spend, its budget, its bidding and learning state.
2. The same read on yesterday alone: does it still spend? Paused, or no spend: say it, stop there, and offer to look at what carries the sales now.
3. `compare_performance` with its `campaignId` and the dates of the period: what moved on it.

## Ask the media buyer

Cutting, holding or raising a campaign is a decision on money, and `ask_media_buyer` puts it back in the account before it answers.

> Over [period], does the campaign "[real name]" on [platform] hold my goal ([goal]), what limits it, what explains its change since [day or the period before], and what should I change on it, from what value to what value? [facts, constraints]

Follow-up with the `conversationId`: a constraint, a fact, or the one change to dig. When the answer points to the ads, or the user asks about them, the second question goes to `ask_creative_strategist` instead.

> In the campaign "[real name]", over [period], which ads carry the sales and why, which wear out, and what should replace them?

## Without an agent

Read the campaign at `level: "adsets"` then `level: "ads"` with its `campaignId`, and its line in `analysis.budgetDecisions` of `get_budget_advice` when the tool answers. Show what Metrikia credits next to what the platform reports, and the `crm` block (leads, appointments, deals) for a lead account. State no cause, say what it would take to find it.

## Deliver

1. The verdict in one sentence, against the goal of the user. No goal known: say what the verdict would need.
2. One short table: the campaign against the period before.
3. What limits it and since when, what could contradict it.
4. The changes, numbered, on the campaign or on a named ad set or ad. Ask which ones the user keeps.

Why the platform counts more sales than Metrikia credits: `get_campaign_performance` splits its count between after a click and without one, when the platform gives it.
