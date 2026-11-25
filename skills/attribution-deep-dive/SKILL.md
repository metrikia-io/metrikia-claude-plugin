---
name: attribution-deep-dive
description: Use when the user asks which channels really bring the sales, which one opens or closes the customer journeys, whether a channel is credited too much or too little, or wants to compare attribution models or read a customer journey.
---

# Attribution deep dive

Who brings the sales: what opens the journeys, what closes them, and what that changes.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`. Period: the one the user names, otherwise `${user_config.default_period}`.

## Read

`get_metrics` once: MER and its trend, `attributedByChannel`, and `roas.channelComparisons`, what Metrikia credits to each platform next to what the platform reports. The amounts of `channelComparisons` are in cents: divide them by 100. Those of `attributedByChannel` are not. Take the dates from `period`.

## Ask the data scientist

`ask_data_scientist` starts from the real sales, sees which source opens and closes the journeys, and knows how far each figure can be trusted.

> Over [period], what really brings my sales: which platforms and sources open the customer journeys, which ones close them, which ones are credited too much or too little, and does the marketing hold as a whole? What would you change, and what would prove you wrong? My goal: [goal]. [facts: launch, email, influencers, promotion]

Follow-up with the `conversationId`: one channel, or a figure the user reads elsewhere, with where it is read and its dates.

## Without an agent

Compare the models, and read one journey if the user wants an example. Say what is missing: the role of each source over all the journeys, and how far the figures can be trusted.

## On request

- **Compare models**: `get_metrics` again with the same dates and `attributionModel: "first_touch"` for what opens, then `attributionModel: "last_touch"` for what closes. The default is `linear`. `markov_chain` and `shapley_value` need enough converted journeys: below it they read 0, which means unknown. Only the attributed figures follow the model, and no model says what would have happened without the ads.
- **Read a journey**: `list_leads` with `status: "closed_won"`, then `get_attribution_journey` on the one the user wants. Each touchpoint carries its credit by model in `attributionCredits`. A journey holds clicks and visits: a mere view leaves no trace, and no touchpoint means no tracked visit.

## Deliver

1. What brings the sales, in one sentence, with what the whole returns.
2. One table by channel: what it opens, what it closes, what Metrikia credits, what the platform reports. Leave a column out rather than fill it with a guess.
3. Why the counts differ, and what could contradict the reading.
4. The decisions, numbered. Ask which ones the user keeps.

Read the channels together, never one alone. A platform counts its own way: say how, do not call it wrong.
