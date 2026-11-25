---
name: budget-optimizer
description: Use when the user asks where to put the ad money, which budgets to raise, lower or cut, how to split an amount between campaigns or platforms, or how to prepare the budgets of a sales event.
---

# Budget optimizer

A budget plan to decide line by line: each object, its value today, its next value, and what the whole plan changes.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`. Period: the one the user names, otherwise `${user_config.default_period}`.

## Read

`get_ads_performance` with `level: "campaigns"`: spend, credited sales and current budget, and in `totals` whether the sales of the account reach the ads. With `budgetLevel: "adset"`, the amounts sit on the ad sets: read `level: "adsets"` once. With `sharedBudget: true`, one amount covers several campaigns: never add it up.

## Ask the media buyer

`ask_media_buyer` looks at what limits each campaign before it moves money, and it sizes the plan as a whole.

> What should I do with my budgets for [horizon], campaign by campaign, from what daily amount to what daily amount, and what is the net change of my daily spend? Read [period]. My goal: [goal]. Total I can spend: [amount, if given]. Do not touch: [constraints]. [facts: promotion, stock, launch]

Follow-up with the `conversationId` when the user keeps some lines only, adds a constraint or brings a fact: the agent sizes the plan again. Never subtract a line yourself.

## Without an agent

`get_budget_advice`, with `language` set to the language of the answer. Use `analysis.budgetDecisions` as it stands: verdict, current and suggested budget of each campaign that spent yesterday, reason in plain words. Its amounts are in the currency of the account, not in cents. These decisions are final, add no other move. Leave the `advice` text aside: it comments, it does not decide.

- `targetMissing: true`: nothing is decided. The target cost per purchase is missing in the brand sheet, and `ask_assistant` tells where to fill it.
- `access_denied`, or no decision: show the spend and the sales by campaign (leads, appointments and deals for a lead account), and say what is missing to decide.

## Deliver

1. The plan in one sentence: what it does to the daily spend.
2. One table: object, budget today, next budget, the figure that justifies it, when to stop. Lines to raise, hold, lower and stop, in that order. A hold has its reason too.
3. What could contradict the plan, in two sentences at most.
4. Ask which lines the user keeps.
