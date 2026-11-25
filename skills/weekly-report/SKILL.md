---
name: weekly-report
description: Use when the user asks how the week went, wants a weekly report or a recap for a Monday meeting or a client update, or says "weekly report", "bilan de la semaine", "how did we do this week".
---

# Weekly report

The week on one screen: what is true, what moved, what to decide.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`.

The week: the 7 days that end yesterday, or the one the user names, against the same number of days before.

## Read

1. `get_sync_status`: a source that is late is said before any figure.
2. `get_metrics` for the week, then for the `previousPeriod` it returns: sales, spend and MER of both.
3. `compare_performance` with `comparisonType: "previous_period"`: cost per sale, credited sales, and the leads the platforms count.

## Ask the media buyer

A week ends on decisions about money, and `ask_media_buyer` looks for what moved before it proposes.

> Over my week from [first day] to [last day], what moved against the week before and since which day, what explains it, and what three decisions should I take for next week? My goal: [goal]. This week: [facts].

Follow-up with the `conversationId`: the point that stays unexplained, or the decision the user wants to change.

## Without an agent

Add `get_ads_performance` with `level: "campaigns"` for who carries the spend and the sales, `get_anomalies` for the open ones, most severe first, and the decisions of the day from `get_budget_advice` when it answers (see the budget-optimizer skill). Say that the causes are not read here: nothing is explained, only shown.

## Deliver

1. The week in one sentence.
2. One table, this week against the week before: sales, spend, MER, cost per sale. Add leads and cost per lead for an account that sells through leads.
3. What moved and since when, what explains it, what could contradict it.
4. The decisions, numbered. Ask which ones the user keeps.

Name a platform or a campaign only when it changes a decision.
