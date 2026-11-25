# Counting leads and deals

## Statuses

`list_leads`: `new`, `contacted`, `no_response`, `appointment_proposed`, `appointment_booked`, `no_show`, `deal_pending`, `nurturing`, `closed_won`, `disqualified`.

`list_deals`: `won`, `pending`, `trial_pending`, `lost`.

Any other value is ignored: the list comes back without a filter and its `total` counts everything. Use these values only.

## How many at each step, today

One call per status with `limit: 1`, and read `total`. It counts every lead at that status, whatever its date. Archived leads are never counted. A call without a status leaves the won leads out: read `closed_won` on its own.

This is the state of the day, not a conversion rate: the leads of one status did not all come in at the same time.

## Over a period

The two lists take no date. Read them with `limit: 100` and `page: 1`, then `2`, and so on. Leads come newest first by `createdAt`, deals by `closedAt`. Stop at the first row before the period, or when the rows read reach `total`. Say it when you stop before the end.

A `pending` or `trial_pending` deal is not a sale. `totalAmount` is in the `currency` of the deal, not in cents: never add two currencies.

## By source

Group the leads read over the period by `source`, then match the deals on `leadId`. A deal without `leadId` has no source here: count it apart.

## Who to call first

The open leads of one status, with `fullName`, `source`, `createdAt` and `updatedAt`. `updatedAt` is the last change of the lead, not the day it entered the status. The order is the user's: oldest first unless they say otherwise.

## How one lead came

`get_attribution_journey` with the id of the lead. It holds clicks and visits, and no touchpoint means no tracked visit. A few journeys illustrate, they prove nothing.

## Changing the CRM

`transition_lead` moves one lead by one step, `create_deal` records a sale with its amount in cents. Show the lead, its current status and the change, and wait for a yes on each one.
