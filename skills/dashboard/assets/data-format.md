# The data of the dashboard

One JSON file. A block with no data is left out: the page leaves out its section. A figure nobody gave is left out, never 0.

| Key | Holds |
|---|---|
| `lang` | `fr` or `en`: the words of the page. The texts are in the language of the user |
| `account`, `currency`, `readOn` | Name of the account, ISO code, day of the reading (`YYYY-MM-DD`) |
| `notice` | The team access notice, word for word, when a result opens with one |
| `period`, `comparedWith` | `start` and `end` (`YYYY-MM-DD`) |
| `accountRoas` | `totals.attributed.roas` of the same reading of the ads |
| `sources` | Each reading under a short name: `tool` (or the agent by its role) and `reads` (the period and what was asked) |
| `headline`, `creativeHeadline` | `sentence`, `accent` (a part of the sentence), `tone` (`bad` for bad news), `lead`. Their figures are figures of the page. Words of an agent: `wordsOf` holds its source |
| `kpis` | Below |
| `actions` | Below |
| `planTotal` | `daily` (the change of spend a day the agent announced) and `by` |
| `trend` | Series: `label`, `hint`, `format`, `source`, `field`, `points` (`label`, `value`), three points at least |
| `campaigns`, `creatives` | Rows, below |
| `platforms` | `name`, `platform`, `claimed`, `credited`, `claimedField`, `creditedField`, `source` |
| `reliability` | `level` (`ok`, `watch`, `broken`), `text`, `source` |
| `briefs` | `title`, `format`, `hook`, `beats` (list), `copy`, `isNew`, `taken`, `judgedOn`, `source` |
| `open` | `creative` to open on that view |

`source` is a name of `sources`, and every item has one. `field` is the name of the field in the result.

## kpis

`label`, `value`, `previous`, `format` (`money`, `number`, `ratio`, `percent`), `better` (`up`, `down`, `none`), `source`, `field`, and `hero: true` on one of them.

`key` names the figures the build cross-checks: `sales`, `spend`, `mer`, `salesCount`, `costPerSale`, `onlineSales`, `onlineMer`, `onlineCount`, `onlineCostPerSale`. The spend is `better: "none"`.

## actions

`kind`, `object` (real name), `what` (from what to what), `why` (with its figure), `by` (the agent, by its role), `estimate`, `stopWhen`, `source`.

| `kind` | Money, read from the budgets |
|---|---|
| `raise`, `lower` | `fromDaily`, `toDaily` |
| `pause` | `fromDaily`, or `insideBudget: true` when it spends the budget of its campaign |
| `start` | `unlocksDaily`: the budget that can be spent once it runs, its own or the one of its campaign. Otherwise `moneyUnknown`: the reason |
| `make`, `fix` | None |

`raise` and `start` need `stopWhen`. The build works out what each line adds to the spend of a day: never type it.

## campaigns and creatives

`name` (real name), `platform` (`meta`, `google_ads`, `tiktok`, other), `platformName`, `spend`, `sales` and `revenue` (credited by Metrikia), `roas`, `costPerSale`, `platformRoas`, `source`.

A campaign may have `note`. An ad may have `short` (a name that fits a card), `format`, `frequency`, `ctr`, `onMap: false` (a text ad on the search network).

`verdict` (two words at most), `tone` (`good`, `watch`, `bad`) and `reason` are the words of an agent on the same period, named in `verdictBy`. No agent spoke of the row: no verdict.
