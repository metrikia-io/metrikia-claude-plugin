# Metrikia MCP Tools Reference

Reference of the tools the Metrikia MCP server lists. The server sends the schema of every tool to your client: when this page and the schema differ, the schema is right.

**Endpoint:** `https://mcp.metrikia.io/api/v1/mcp`
**Protocol:** JSON-RPC 2.0 over HTTP
**Authentication:** OAuth 2.1 (see [SECURITY.md](SECURITY.md))

18 tools come with every account: 13 read tools, `ask_assistant` and 4 write tools. Three more, one per agent, are listed only when the account and the user have access to that agent.

| Conventions | |
|---|---|
| Account | Every call reads the account you signed in with, and nothing else |
| Dates | `YYYY-MM-DD`, both included |
| Amounts | In the currency of the account, the one `get_metrics` and `get_ads_performance` give. Some are in cents: see the table below |
| `null` | Unknown or not computable. Never zero |
| `attributionModel` | `linear` (default), `first_touch`, `last_touch`, `time_decay`, `u_shaped`, `w_shaped`, `full_path`, `markov_chain`, `shapley_value`. It changes the attributed figures only, and the answer says which model it used. `markov_chain` and `shapley_value` need enough converted journeys: below it, the attributed figures stay at 0 |
| Pages | A list gives `total`, the number of rows that match. One page is not the list |

## Amounts in cents

| Tool | In cents, to divide by 100 | In currency units |
|---|---|---|
| `compare_performance` | `spend`, `revenue`, `cpl`, `cpc` and `profit` of `current` | `attributed` and `allSources` |
| `get_campaign_performance` | `spend`, `revenue`, `cpl`, `cpc` and `profit` | `attributed` |
| `get_metrics` | `realRevenueAmount`, `platformRevenueAmount` and `spendAmount` of `roas.channelComparisons` | Every other amount |
| `get_anomalies` | `detectedValue` and `baselineValue` when `metricType` is `spend` or `spend_zero` | The same two when it is `cpl` |
| `get_budget_advice` | `total_credit_value` of `attributionInsights.channel_attribution` | Every other amount, those of the decisions included |
| `get_ads_performance`, `get_creative_report` | None | Every amount |
| `list_deals`, `get_attribution_journey` | None | `totalAmount`, `conversionValue` |
| `create_deal` | `amount`, the one you send | `totalAmount`, the one it returns |

In doubt, read the same spend over the same days in two tools: the one in cents reads 100 times more. What is not an amount: `ctr`, `roiPercent` and the changes of a comparison are in percent, `mer` and `roas` are ratios. For an anomaly, `ctr` is in percent, `roas` and `crm_roas` are ratios, and `lead_drought` counts leads a day.

---

## 1. Ads

The tools of this section follow the access of the Ads page. A role that cannot open it gets `access_denied`.

### list_campaigns

Campaigns of every connected ad account.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `limit` | int | 50 | Rows per page, 200 at most |
| `activeOnly` | bool | false | Every active campaign at once, without pages |

**Returns** `campaigns` and `total`. Each campaign: `id` (the Metrikia id the other tools take), `externalId` (the id of the ad platform), `name`, `status` (`active`, `paused`, `archived`), `platform`, `adAccountId`, `createdAt`.

### get_ads_performance

Campaigns, ad sets or ads, with the figures of the Ads page. The first tool to read for anything about ads.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | string | `campaigns` | `campaigns`, `adsets` or `ads` |
| `attributionModel` | string | `linear` | See above |
| `startDate`, `endDate` | string | the last 30 full days | Period, on the calendar of the account |
| `campaignId` | string | | Ad sets or ads of one campaign |
| `adSetId` | string | | Ads of one ad set |
| `adAccountId` | string | | One or several ad accounts, separated by commas |
| `limit` | int | 50 | Rows, 200 at most, ranked by spend |

**Returns** `level`, `attributionModel`, `period`, `currency`, `total`, `rows` and `totals`.

| Field of a row | Content |
|---|---|
| `id`, `linked`, `kind`, `name`, `status`, `platform` | `status` is `active` or `paused`. A row with `linked` false is credit that no campaign, ad set or ad holds: it is not an object, and its id is not a filter |
| `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm` | As the platform delivers them |
| `attributed` | What Metrikia credits: `purchases`, `revenue`, `roas`, `averageOrderValue`, `costPerAttributedSale` (`null` without a sale). `cpa` is its former name |
| `crm` | `leads`, `cpl`, `appointments`, `deals`, `revenue` |
| `platformReported` | What the platform counts: `leads`, `purchases`, `purchasesClickThrough`, `purchasesViewThrough`, `revenue`, `roas` |
| Budget | `dailyBudget`, `lifetimeBudget`, `startDate`, `budgetLevel` (`campaign` or `adset`: where the budget sits), `sharedBudget` (one amount for several campaigns, never added up) |
| Platform state | `bidStrategy`, `bidTarget`, `learningStatus`, `limitedByBudget`, `platformStateSince`, as read at the last sync |
| Delivery, ad sets and ads | `outboundClicks`, `outboundCtr`, `costPerOutboundClick`, `frequencyYesterday`, `frequency7d`, `frequency30d`, `frequencyReadAt` |

Every amount is in currency units. A budget, state or delivery field is absent when the platform gives none. `totals` covers every row: `spend`, `impressions`, `clicks`, `attributed`, and `allSources` with `sales` (every won sale, whatever brought it) and `costPerSale`. `allSources` is `null` when the call is narrowed to a campaign, an ad set or an ad account. An account that also sells in store or on a marketplace gets `onlineCostPerSale` and `salesByPlace` too: judge the ads on the online one.

### get_campaign_performance

One campaign.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `campaignId` | string | required | From `list_campaigns` |
| `startDate`, `endDate` | string | the last 30 days, today included | Give both, to match the other tools |
| `adAccountId`, `dataSourceId` | string | | Filters |
| `attributionModel` | string | `linear` | See above |

**Returns** `campaignId`, `period`, `impressions`, `clicks`, `spend`, `revenue` (reported by the platform), `leads`, `conversions` (purchases the platform counts), `conversionsClickThrough` and `conversionsViewThrough` (their split, `null` when unknown), `cpl`, `cpc`, `ctr`, `roas` and `roasSource` (`mta`, `crm` or `platform`: where the ratio comes from), `crmRoas`, `currency`, `appointments`, `deals`, `profit`, `roiPercent`, `attributionModel`, `attributed`.

`spend`, `revenue`, `cpl`, `cpc` and `profit` are in cents: a `cpl` of 450 reads 4.50. The `attributed` block is in currency units.

### get_creative_report

Ads of the account, ranked.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sortBy` | string | `spend` | `spend`, `revenue` (reported by the platform), `leads`, `deals`. To rank on another figure, sort the rows you get |
| `limit` | int | 20 | Rows, 50 at most |
| `startDate`, `endDate` | string | the last 30 days, today included | Give both, to match the other tools |
| `campaignId`, `adAccountId` | string | | Filters |
| `attributionModel` | string | `linear` | See above |

**Returns** `creatives`, `total`, `currency`, `attributionModel`. Each ad: `adId`, `adName`, `platform`, `campaignName`, `isActive`, `impressions`, `clicks`, `spend`, `revenue`, `leads`, `deals`, `appointments`, `ctr`, `cpc`, `cpl`, `roas`, `roasSource` (`mta`, `crm` or `none`), `crmRoas`, `currency`. Every amount is in currency units. For the figures of the Ads page, use `get_ads_performance` with `level` `ads`.

### compare_performance

Two periods side by side.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `startDate`, `endDate` | string | the last 30 full days | Current period |
| `comparisonType` | string | `previous_period` | `previous_period`, `previous_month`, `previous_year` |
| `campaignId`, `adAccountId` | string | | Filters. `adAccountId` takes several ids |
| `attributionModel` | string | `linear` | See above |

**Returns** `period`, `current`, `changes` (in percent), `comparisonType`, `attributionModel`, `attributed` (`current` and `previous`) and `allSources` (`current` and `previous`, `null` when the call is narrowed). `current.leads` and `current.revenue` are the counts of the platforms.

`spend`, `revenue`, `cpl`, `cpc` and `profit` of `current` are in cents: a `cpl` of 450 reads 4.50. The `attributed` and `allSources` blocks are in currency units.

### get_anomalies

Anomalies found in the ad figures.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `includeAcknowledged` | bool | false | Adds the ones acknowledged over the last 30 days |

**Returns** `total`, `returned`, `bySeverity`, `byMetricType` and `anomalies` (50 at most, most severe first): `id`, `metricType`, `metricLabel`, `severity` (`info`, `warning`, `critical`), `detectedValue`, `baselineValue`, `deltaPercent`, `campaignId`, `detectedAt`, `isActive`. An open anomaly expires 7 days after its detection. `detectedValue` and `baselineValue` are in the unit of `metricType`: in cents for `spend` and `spend_zero`, in currency units for `cpl`, in percent for `ctr`, a ratio for `roas` and `crm_roas`, leads a day for `lead_drought`.

### get_budget_advice

The budget decision of the day for each campaign that spent yesterday.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | string | `30d` | Context: `7d` or `30d` |
| `language` | string | `en` | `en` or `fr` |
| `attributionModel` | string | `linear` | For `attributionInsights` only |

**Returns** `analysis`, `attributionInsights`, `advice`, `period`, `generatedAt`, `attributionModel`, `analysisAttributionModel`. The decisions are in `analysis.budgetDecisions`: `targetMissing`, `targetCpa`, `breakEvenCpa`, `currency`, `readOn` and `campaigns`, most severe first, each with `campaignName`, `platform`, `verdict` (`raise`, `hold`, `lower`, `pause`), `reason`, `dailyBudget`, `suggestedDailyBudget`, its spend, purchases and cost per purchase, and `learningStatus`. Their amounts are in currency units.

The decisions are final: no other move is to be derived from the rest of the answer, which is context. `targetMissing` true: no target cost per purchase in the brand sheet, nothing is decided. The tool follows the Budget Advisor feature of the account: off, it answers `access_denied`.

---

## 2. Sales and attribution

### get_metrics

The MER of the account and what Metrikia credits to each platform and channel. Follows the access of the Ads page.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `startDate`, `endDate` | string | the last 30 full days | Period, on the calendar of the account |
| `attributionModel` | string | `linear` | For `roas` and `attributedByChannel` |
| `comparison` | string | `previous_period` | `previous_period`, `previous_month`, `previous_year` |

| Field | Content |
|---|---|
| `mer`, `previousMer`, `merTrend` | Sales divided by spend, the same for the period before, and its change. `null` comes with a reason (`merNotComputableReason`, `merTrendNotComputableReason`) |
| `sales`, `spend`, `currency`, `period`, `previousPeriod`, `comparison` | Amounts in currency units, like every other amount of this answer but one block. Both days of a period are included |
| `storeNetRevenue`, `salesOutsideStore`, `enteredOrImportedSales` | What the sales are made of: store orders net of refunds, every other won sale, and within them the ones entered or imported by hand, with their counts and shares |
| `suspectedDuplicatesRemoved` | Payments or orders left out because they repeat a CRM sale of the same lead |
| `otherCurrencySales`, `spendInOtherCurrencies` | Given apart, never converted |
| `onlineMer`, `previousOnlineMer`, `onlineMerTrend`, `salesByPlace` | Only for an account that also sells in store or on a marketplace: `online`, `inStore` and `marketplace`. Judge the ads and compare the periods on the online figure |
| `roas.channelComparisons` | By ad platform: `realRoas` and `realRevenueAmount` (credited by Metrikia), `platformRoas` and `platformRevenueAmount` (reported by the platform), `spendAmount`. This block is the one with its amounts in cents |
| `attributedByChannel` | By channel and source: `touchpoints`, `attributedConversions`, `attributedRevenue` |

`totalRevenue`, `totalSpend` and their currencies are former names of `sales`, `spend` and `currency`.

### get_attribution_journey

The customer journey of one lead.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `leadId` | string | required | From `list_leads` |

**Returns** `leadId`, `leadName`, `dealId`, `conversionValue`, `conversionCurrency`, `convertedAt`, `touchpointCount`, `firstTouchAt`, `lastTouchAt`, `touchpoints`, `attributionByModel`. Each touchpoint: `id`, `channel`, `position`, `isFirst`, `isLast`, `isLeadCreation`, `isOpportunity`, `daysBefore`, `occurredAt`, `deviceType`, `campaignName`, `utmSource`, `utmMedium`, `utmCampaign`, `landingPageUrl`, and `attributionCredits`, its credit under each model. `attributionByModel` is the total credit shared under each model. `conversionValue` is in units of `conversionCurrency`. A credit is a share of the sale, not an amount.

Channels: `paid_search`, `paid_social`, `paid_video`, `display`, `ctv`, `retail_media`, `organic`, `email`, `sms`, `referral`, `ai_assistant`, `direct`. A journey holds clicks and visits. No touchpoint means no tracked visit.

---

## 3. CRM

### list_leads

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 20 | Rows per page, 100 at most |
| `page` | int | 1 | Page number |
| `status` | string | | `new`, `contacted`, `no_response`, `appointment_proposed`, `appointment_booked`, `no_show`, `deal_pending`, `nurturing`, `closed_won`, `disqualified` |

**Returns** `leads`, `total`, `page`, `limit`. Each lead: `id`, `fullName`, `status`, `source`, `createdAt`, `updatedAt`, `setterId`, `closerId`, `isAnonymized`. Newest first by `createdAt`.

- Any other `status` is ignored: the list comes back without a filter.
- Without a status, the `closed_won` leads are left out. Archived leads are always left out.
- There is no date filter: page through and compare `createdAt`.

### get_lead

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Lead id |

**Returns** `id`, `fullName`, `status`, `source`, `campaign`, `campaignId`, `setterId`, `closerId`, `estimatedRevenue` (a range, or `null`), `notes`, `disqualificationReason`, `isAnonymized`, `hasAttribution`, `createdAt`, `updatedAt`. Unknown id: `not_found`.

### list_deals

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 20 | Rows per page, 100 at most |
| `page` | int | 1 | Page number |
| `status` | string | | `won`, `pending`, `trial_pending`, `lost` |

**Returns** `deals`, `total`, `page`, `limit`. Each deal: `id`, `status`, `totalAmount`, `currency`, `closerId`, `closedAt`, `createdAt`, `leadId`. `totalAmount` is in units of the `currency` of the deal, not in cents. Latest first by `closedAt`. Any other `status` is ignored, and there is no date filter.

---

## 4. Data

### get_sync_status

No parameter. **Returns** `dataSources`: the active ad sources of the account with `id`, `name`, `type`, `lastSyncAt` and `lastHierarchySyncAt`. Performance data syncs every 2 hours.

---

## 5. Agents and assistant

### ask_assistant

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | string | required | A question in plain words |

**Returns** `answer` and `conversationId`. A question about your figures is answered from the data of the account by the agent of the Metrikia team it calls for, when the account can use one. Any other question is answered from the help content, which reads no figure. Credit the answer to the Metrikia Assistant. The tool takes no `conversationId`: each question stands on its own.

### ask_media_buyer, ask_creative_strategist, ask_data_scientist

Listed only when the account and the user have access to that agent.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | string | required | A question in plain words, in your language |
| `conversationId` | string | | From a previous answer of the same agent, to continue that conversation |

**Returns** `agent` (the role in words), `role`, `answer`, `conversationId`.

| Tool | Ask it about |
|---|---|
| `ask_media_buyer` | A decision on the ad accounts: cut, hold or scale a campaign, move budget, read a test, prepare a sales event |
| `ask_creative_strategist` | The ads themselves: which really sell and why, wear, hooks, variations, briefs. It reads figures, formats and texts, and never watches a video |
| `ask_data_scientist` | Whether the marketing works as a whole, the gaps between the ad platforms, Metrikia, the store and the payments, the state of the tracking |

An agent reads the account, advises, and never changes an ad account. Credit its answer to its role, for instance "the media buyer of Metrikia". An answer can take a minute or two, and counts in the daily budget of the account for the agents.

---

## 6. Write

These tools need the `mcp:write` permission.

### create_lead

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `firstName`, `lastName` | string | required | |
| `email` | string | | Links the lead to the visits of the same person |
| `phone` | string | | With its country prefix |
| `source` | string | | Id of a lead source of the account. Without it, the default source |
| `notes` | string | | Internal notes |

**Returns** `id`, `status`, `fullName`.

### transition_lead

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `leadId` | string | required | Lead id |
| `transition` | string | required | `contact`, `mark_no_response`, `resume_contact`, `propose_appointment`, `book_appointment`, `show_up`, `mark_no_show`, `reschedule`, `start_nurturing`, `resume_deal`, `close_won`, `express_win`, `direct_close`, `cross_sell`, `disqualify` |

**Returns** `success`, `fromStatus`, `toStatus`, `error`, `blockers`. A transition the workflow does not allow from the current status comes back with `success` false and its `blockers`.

### create_deal

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `leadId` | string | required | Lead id |
| `amount` | int | required | In cents |
| `currency` | string | `EUR` | Currency code |
| `notes` | string | | Notes |
| `won` | bool | false | `true` records a closed sale, fully collected, which credits the ads of the lead. It is refused when the CRM workflow cannot move the lead to won |

**Returns** `id`, `status` (`pending` or `won`), `totalAmount` (in currency units), `currency`.

### trigger_sync

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataSourceId` | string | | One source, from `get_sync_status`. Without it, every source |

**Returns** `dispatched`, `message`, `dataSourceId`. The sync runs in the background: read `get_sync_status` a few minutes later.

---

## Limits

| What | Limit |
|---|---|
| Tool calls | 60 calls per minute per user, with bursts up to 120 calls |
| `ask_assistant` | 10 questions per 5 minutes per user |
| Each agent | 10 questions per 5 minutes per user, 30 questions per 5 minutes for the whole account, and the daily budget of the account |
| `trigger_sync` | 10 syncs per 5 minutes for the whole account, shared with the app |
| Any request to the server | 600 requests per minute per user |

## Errors

| What comes back | Meaning |
|---|---|
| Tool error `Rate limit reached (...). Retry in N seconds.` | The limit named in the message is reached. The response also carries `Retry-After` |
| Tool error on the budget of the day | The agents of the account come back at the time the message gives |
| Tool error on an agent | The agent is not available for this account, or the owner turned the AI agents off |
| `{"error": "access_denied", "message": ...}` | The role of the user, or a feature of the account, closes the figures |
| `{"error": "invalid_id" ...}`, `{"error": "not_found" ...}` | Use an id returned by a Metrikia tool for this account |
| `{"error": "invalid_date_range" ...}` | Dates are `YYYY-MM-DD`, the first one not after the second |
| `{"error": "invalid_level" ...}`, `{"error": "invalid_attribution_model" ...}`, `{"error": "invalid_comparison" ...}` | The message gives the accepted values |
| `Invalid parameters for tool ...` | A parameter has the wrong type or is missing |
| `Error while executing tool` | The call failed, for instance a write tool without the write permission |
| HTTP `401` | Sign in again |
