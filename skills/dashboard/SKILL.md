---
name: dashboard
description: Use when the user wants a dashboard, a board to look at or to show to a client or a team, a visual page of the account or of the ads, or says "tableau de bord", "dashboard growth", "dashboard créa", "montre-moi mes pubs".
---

# Dashboard

One page to decide on: what is true, what to do, what to make next, and where each figure comes from. It has three views: growth, creative, and the proof of every figure.

First read `references/working-method.md`, in the folder of this skill. Every Metrikia skill holds the same page: once per session is enough. Answer in the language of the user. Period: the one the user names, otherwise the 7 days that end yesterday, against the 7 days before.

Three rules hold even without that page: every call on a period carries the same first and last day, the figures of an agent stay as written, and the user decides line by line. No Metrikia tool is listed: the account is not connected (`/mcp` in Claude Code, Customize then Connectors on claude.ai), give no figure and no advice of your own. `references/errors.md` has the steps, and what to do when a call is refused or empty. Build no page then.

## Read

1. `get_sync_status`: a late source is a line of `reliability`.
2. `get_metrics` for the period. It gives the period before as well. With `onlineMer` or `salesByPlace`, the online figures lead and the total stands beside them.
3. `compare_performance` with `comparisonType: "previous_period"`: cost per sale in `allSources`. The amounts of `current` are in cents, those of `allSources` and `attributed` are not.
4. `get_ads_performance` with `level: "campaigns"`, then with `level: "ads"`. Rows come by spend: keep those that carry it.
5. The trend, when it helps to decide: `get_metrics` on earlier weeks, one call for two weeks (each call returns the week before).

Look at `attributedByChannel` of both periods before any cause: a source that is not an ad (email, cart reminder, referral) and that moved is a line of `reliability`, and it goes into the question to the agent.

## Ask

Two questions, on the same period as the page, so the page never shows the verdict of another one.

> To `ask_media_buyer`: From [first day] to [last day], what moved against the period before, since which day, what explains it, and what are the decisions to take, in order? For each one: the object, from what budget to what budget, what it adds to the spend of a day at most, the expected effect, when to stop. My goal: [goal]. Facts: [stock, sale, launch, the sources that moved]

> To `ask_creative_strategist`: From [first day] to [last day], which of my ads sell, which are wearing out and why, and what are the next three ads to make, with the hook, the script, the text, what is new, and what each one is judged on? Constraints: [claims to avoid, people available]

An action that starts something needs its money: without the budget it unlocks, ask the media buyer once with the `conversationId`. Still nothing: the page says the amount is to be confirmed.

## Without an agent

The page has the figures, the trend and the proof, but no action, no verdict and no next ad. Say that this part is missing.

## Build

1. Write the data file as `assets/data-format.md` gives it. Copy each figure from the result of its tool, in currency units: some come in cents.
2. Run `python3 scripts/build_dashboard.py data.json metrikia-dashboard.html`, from the folder of this skill. Write both files where the user keeps private documents, outside any repository.
3. A refused figure: read the result of the tool again and correct the copy. Never change a figure to make it pass, never remove the check. Two figures of the tools that disagree: leave both out, say it.
4. A `WARNING` on the plan: the total an agent announced is not the one of its lines. Ask the agent again with the `conversationId`. Still different: the page shows both, and your message says it first.

No way to run a script: put the data in place of `__METRIKIA_DATA__` in `assets/dashboard.html`, write each `<` of a text as `\u003c`, and change nothing else. The page then says that its figures were not checked. Say it too.

Never write another page, style or chart by hand. Nothing in the data comes from outside the account.

## Deliver

1. The page: an artifact where the client has them, otherwise the file and its path.
2. One sentence, the decisions as numbered lines, and what the page could not show.
3. The user keeps or refuses lines on the page and pastes them back: that is the yes of `references/working-method.md`, line by line. A line with an amount to confirm is never applied.

The page holds the figures of the account: never publish or send it without an explicit yes.
