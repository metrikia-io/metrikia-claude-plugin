---
name: trust-check
description: Use when figures disagree or look wrong, when sales, leads or conversions dropped and nobody knows why, when the user asks whether the numbers, the tracking or the data can be trusted, or why an ad platform counts more or fewer sales than the store, the payments or the CRM.
---

# Trust check

Can I decide on these figures: what is reliable, what is read with care, what is not usable, and the first thing to fix.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`. Period: the one the user names, otherwise `${user_config.default_period}`.

## Read

1. `get_sync_status`: the last sync of each ad source.
2. `get_metrics`: the sales of the store and the other sales, `suspectedDuplicatesRemoved`, the amounts in another currency, the reason of a `null`, and `roas.channelComparisons` (in cents, divide by 100), what Metrikia credits to each platform next to what it reports.

## Ask the data scientist

`ask_data_scientist` starts from the real sales, and checks the tracking, the sources and the payments before it concludes.

> Can I decide on my figures over [period]? Check the tracking, the sources that stopped, the share of sales without a tracked visit, and the gap between what [platforms] count, Metrikia, my store and my payments. What is reliable, what is not, since when, and what should be fixed first, and by whom? [a drop: is it a real one, and what explains it?] I read [figure of the user] in [where], over [dates]. Changed on my side: [site, pixel, payment, price, or nothing known]

A drop has a day: ask the user what changed on their side that day, and send the reply with the `conversationId`.

## Without an agent

Add `get_ads_performance`: `totals.attributed` next to `totals.allSources`, the rows with `linked` false, and for a lead account the leads of the platform next to the `crm` block. Say what can be read: a late source, the reason of a `null`, duplicates set aside, an account that sells while no sale is credited, the two counts of each platform. Say what cannot be read here: the events the tracking receives, the share of sales without a tracked visit, the payments tied to a visit. `ask_assistant` tells how to check the installation.

## Deliver

1. Yes, with care, or no, in one sentence.
2. Three short lists: reliable, with care, not usable. Each line says why and since when.
3. The first thing to fix, who does it, how the user will know it is fixed, and the decisions that wait for it.
4. Ask whether the user takes it on. For a late source, offer `trigger_sync`, after a yes.

Explain the figure of the user before giving another one, over the same dates.
