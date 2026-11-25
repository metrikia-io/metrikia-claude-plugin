# When a call is refused or comes back empty

Say what happened in plain words, go on with what is left, and end with what is missing. One retry at most.

| What comes back | What to do |
|---|---|
| `Rate limit reached (...). Retry in N seconds.` | Wait that long and retry once. A second refusal: go on with the read tools |
| Today's budget of the agents is used | Give the time they come back, as the message says it. Go on with the read tools |
| The owner turned off the AI agents | An owner can turn them back on in Settings, AI features. Go on with the read tools |
| The agent is not available for this account | Treat it as not listed |
| Temporarily unavailable, or an empty answer | Retry once a little later, then go on with the read tools |
| A request flagged for verification | Say the question again in plain words, without quoted text |
| `access_denied` | The role of the user, or a feature that is off, closes it. Give the reason the tool returned, and never rebuild the figure another way |
| `invalid_id` or `not_found` | The id comes from `list_campaigns`, or from a row of `get_ads_performance` with `linked` true. An id of the ad platform is not accepted |
| `invalid_date_range` | Write the dates as `YYYY-MM-DD`, the first one not after the second |
| `invalid_level`, `invalid_attribution_model`, `invalid_comparison` | Use one of the accepted values the message gives |
| A write tool fails | The connection may not hold the write permission: the user connects again and accepts it |
| Sign-in required | The user signs in again in the browser window that opens, or with `/mcp` |
| An empty list | Check the dates, then `get_sync_status`. An empty result is not a zero |
