---
name: next-actions
description: Use when the user wants a few actions rather than a report, asks what to do today or this week on the account, where to start or what changed since yesterday, or says "mes trois actions du jour".
---

# Next actions

Three actions to take today, on real objects, each with its reason. Another number when the user gives one.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`.

## Ask the media buyer

The actions of the day are mostly about money, and `ask_media_buyer` reads what moved and the open alerts before it proposes. No read tool comes first.

> What moved on my account yesterday and this past week, what is still alerting, and what are the three actions to take today, in order? My goal: [goal]. [facts: stock, promotion, launch, outage, constraint]

A question about the ads alone goes to `ask_creative_strategist`, a doubt on the figures to `ask_data_scientist`, with the same wording.

Follow-up with the `conversationId`: the action the user refuses, with the reason, or the one already done.

## Without an agent

1. `get_sync_status`: a late source is the first action.
2. `get_ads_performance` with `level: "campaigns"`: what runs, and whether the sales of the account reach the ads.
3. `get_anomalies`: the open ones, most severe first. The values of a `spend` or `spend_zero` anomaly are in cents: divide them by 100.
4. The decisions of the day from `get_budget_advice` when it answers (see the budget-optimizer skill). Their amounts are not in cents.
5. For an account that sells through leads: how many wait at `new`, `no_response` and `no_show` (`list_leads` with `limit: 1`, read `total`).

Give what these tools show or decide, even if it makes fewer than three actions.

## Deliver

1. What moved, in one sentence.
2. The actions, numbered: the object by its real name, from what value to what value, the figure that justifies it, the estimate as a range, when to stop.
3. Ask which ones the user keeps.

An action changes something today: a check or a wait is not one. Nothing to change is an answer: say it and why.
