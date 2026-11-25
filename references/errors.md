# When a call is refused or comes back empty

Say what happened in plain words, go on with what is left, and end with what is missing. One retry at most.

| What comes back | What to do |
|---|---|
| No Metrikia tool is listed | The account is not connected. Say it, say how to connect it, and stop there: no figure, no advice, no other way to get the data, no agent announced. Claude Code: `/plugin` to enable metrikia, `/reload-plugins`, then `/mcp` to sign in. claude.ai and the Claude app: Customize, Connectors, Add, Add custom connector, `https://mcp.metrikia.io/api/v1/mcp`, then Connect |
| Sign-in required | The user signs in again: `/mcp` in Claude Code, Customize then Connectors on claude.ai |
| Sign-in refused | The user checks which Metrikia account the browser is signed in to, and tries once more. Refused again: support@metrikia.io, with the message as it reads |
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
| An empty list | Check the dates, then `get_sync_status`. An empty result is not a zero |
