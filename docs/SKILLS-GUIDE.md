# Metrikia Plugin: Skills Guide

What each skill is for, whom it asks, what it reads and what you get. Every skill follows the same [working method](../references/working-method.md).

## What every skill does

1. **Looks at your tool list.** It asks the Metrikia agent whose field it is, when your account lists it. Another agent is listed: it asks that one. None is: it works with the read tools and says what is missing.
2. **Asks one good question**: the decision to make, the period, the real names, your goal and what you told it. A follow-up continues the same conversation with the agent.
3. **Reads only what it must show.** It keeps the figures and the ranges of the agent as written and says who gave them.
4. **Answers on one screen**, in your language. The detail comes when you ask.
5. **Leaves the decision to you.** It ends with numbered lines. Nothing changes on an ad account, and nothing is written in Metrikia, without your yes on each line.

What you tell the skill changes the answer: a stock-out, a promotion, a price, an outage, a constraint ("do not touch this campaign"). Say it in the question.

---

## /metrikia:next-actions

**When:** you want to know what to do today or this week, not a report.

**Asks:** the media buyer. A question on the ads alone goes to the creative strategist, a doubt on the figures to the data scientist.

**Reads:** nothing first. Without an agent: the sync dates, the open anomalies and the budget decisions of the day.

**You get:** what moved in one sentence, then the actions in order, each with its object, its value today, the next one, the reason and when to stop.

**Then:** refuse a line with its reason, or say what is already done. The agent adapts the rest.

## /metrikia:weekly-report

**When:** a Monday meeting, a client update, "how did the week go".

**Asks:** the media buyer.

**Reads:** the sync dates, the sales, spend and MER of the two weeks, and the change of the cost per sale and of the leads. Without an agent, also the campaigns, the open anomalies and the budget decisions of the day.

**You get:** the week in one sentence, one table against the week before, what moved and why, and the decisions to take.

**Then:** `/metrikia:campaign-audit` or `/metrikia:creative-analysis` on what the report points to.

## /metrikia:dashboard

**When:** a page to look at, or to show to a client or a team: the account, the ads, the decisions.

**Asks:** the media buyer for the decisions, the creative strategist for the ads, both on the period of the page.

**Reads:** the sync dates, the sales, spend and MER of the two periods, the cost per sale, the campaigns and the ads.

**You get:** one page in three views. Growth: what is true, the decisions with the spend each one can add, what moved, where the money goes. Creative: the ads that sell, the ones that wear out, the next ones written out. Proof: every figure with the reading it comes from. A short script builds it: it refuses a figure with no source or that does not add up with the ones beside it, and loads nothing from the network.

**Then:** keep or refuse lines on the page, copy your decisions and paste them in the chat.

## /metrikia:budget-optimizer

**When:** where to put the money, which budgets to raise, lower or cut, how to split an amount, how to prepare a sales event.

**Asks:** the media buyer, for a whole plan and its effect on what you spend a day.

**Reads:** the campaigns, their spend, their sales and their current budget. Without an agent, the budget decisions of the day, as they stand. They need a target cost per purchase in your brand sheet.

**You get:** the plan in one sentence, then one table: object, budget today, next budget, why, when to stop.

**Then:** keep some lines only, and the agent sizes the plan again.

## /metrikia:campaign-audit

**When:** you name one campaign.

**Asks:** the media buyer. The creative strategist too, when the answer points to the ads or you ask about them.

**Reads:** the campaign in its account, and what moved on it. Without an agent, its ad sets and its ads.

**You get:** the verdict against your goal, what limits the campaign and since when, and the changes to decide on. A campaign that no longer runs gets no advice.

## /metrikia:creative-analysis

**When:** which ads sell and why, whether an ad wears out, what to make next, a brief.

**Asks:** the creative strategist. It reads the figures, formats and texts of the ads and never watches a video: describe the first seconds, paste a few customer reviews, and the answer gets sharper.

**Reads:** the ads with their spend, their credited sales and their clicks.

**You get:** what to understand, the ads that count, then the next ads with hook and text ready to copy. Scripts and full briefs on request.

## /metrikia:lead-pipeline

**When:** leads, appointments, deals, which sources bring leads that sign, who to call first.

**Asks:** the data scientist, who also answers sales roles.

**Reads:** with an agent, only what you ask to see. Without one, the leads and the deals at each status, then the period page by page.

**You get:** where people stop, one table, what explains the weak step, and who does what.

**Good to know:** the count of a status is the state of the day. It is not a conversion rate.

## /metrikia:attribution-deep-dive

**When:** which channels bring the sales, what opens and closes the journeys, a comparison of attribution models, one customer journey.

**Asks:** the data scientist.

**Reads:** the MER, what Metrikia credits to each platform next to what it reports, and the credit by channel.

**You get:** what brings the sales, one table by channel, why the counts differ, and the decisions.

**Good to know:** an attribution model shares the credit of sales that happened. It does not say what would have happened without the ads.

## /metrikia:trust-check

**When:** two figures disagree, the tracking is in doubt, sales or leads dropped and nobody knows why.

**Asks:** the data scientist.

**Reads:** the sync dates and the parts of the sales figure. Without an agent, also the credited sales next to all the sales.

**You get:** yes, with care or no, then what is reliable, what is not, the first thing to fix and who does it.

**Then:** the decisions that were waiting for it.

---

## Which one first

| You have | Start with |
|---|---|
| Ten minutes in the morning | `/metrikia:next-actions` |
| A meeting | `/metrikia:weekly-report` |
| A page to show, or to keep open | `/metrikia:dashboard` |
| A figure you do not believe | `/metrikia:trust-check` |
| An amount to spend | `/metrikia:budget-optimizer` |
| One campaign on your mind | `/metrikia:campaign-audit` |
| A shoot to prepare | `/metrikia:creative-analysis` |
| Leads that do not sign | `/metrikia:lead-pipeline` |
| A channel in question | `/metrikia:attribution-deep-dive` |

## Limits to know

- The questions to an agent are limited per five minutes and count in the daily budget of your account. A skill asks two at most per run, follow-up included, unless you ask for more.
- An agent advises and never changes an ad account.
- Never a promised result: an estimate is a range.
