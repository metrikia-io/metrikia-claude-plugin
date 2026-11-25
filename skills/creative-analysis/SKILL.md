---
name: creative-analysis
description: Use when the user asks which ads or creatives sell and why, whether one ad beats another or is wearing out, what to test or produce next, or wants hooks, variations, scripts or a brief for the team that makes the ads.
---

# Creative analysis

What sells among the ads and why, what is tired, and what to make next, written out.

First read `${CLAUDE_PLUGIN_ROOT}/references/working-method.md`, once per session (from this file, `../../references/working-method.md`). Language: the one the user writes in, otherwise `${user_config.language}`. Period: the one the user names, otherwise `${user_config.default_period}`.

## Read

`get_ads_performance` with `level: "ads"`, narrowed by `campaignId` or `adSetId` when the user names one: spend, credited sales and their cost (the `crm` block for a lead account), and where the platform gives them, frequency and clicks to the site. Rows come by spend: the ads that count are at the top. Rank on these rows.

## Ask the creative strategist

`ask_creative_strategist` starts from what people are shown and ties it to the real sales. It reads the figures, formats and texts of the ads, and never watches a video.

> Over [period], which of my ads really sell and why, which are wearing out, and what are the next [number] ads to make, with the hook, the script and the text written out? Product and customer: [words of the user]. Offer to show, if any: [offer and end date]. On screen in "[ad name]": [description, if given]. Constraints: [claims to avoid, people available to film]

Before a follow-up, ask the user for what no tool holds: what happens first in the ads with the most spend, and a few reviews or comments in the customers' own words. Send them with the `conversationId`. The budget of an ad is a question for the media buyer, only if the user asks.

## Without an agent

Show the ads with the most spend and the most credited sales, side by side, what each figure shows and which ones are paused. Stop there: no winner is named, no wear is declared. An idea of yours is presented as an idea, not as a reading of the account.

## Deliver

1. What to understand about the ads, in one sentence.
2. The ads that count, by their real name: what each sells, the reason given, what would confirm it.
3. The next ads, numbered: what is new in each, what is taken from the ads that sell, how its result will be judged. Hook and text ready to copy.
4. Ask which ones go to production. A full script or brief comes on request.

A new ad proves nothing before it sells. Never copy another brand, never invent a review, an offer, an urgency or a scene.
