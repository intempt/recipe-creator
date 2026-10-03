---
id: lead-customer-sales
title: Lead to customer
slash_command: /lead-customer-sales
group: Reports
owner: intempt
summary: Shows how many demo requests turn into booked meetings, completed demos, proposals and closed
  deals, and which lead sources actually convert.
description: >-
  Sales pipeline funnel using deal_stage_changed and meeting events with stage velocity and forecasted
  revenue.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Trace demo requests to closed deals"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Trace demo requests to closed deals
    summary: >-
      A five step funnel over 60 days from a demo request form to a scheduled meeting, a meeting that
      actually happened, a proposal stage change and a won deal, split by the top 8 lead sources, with
      median time between stages and forecast revenue per stage.
    builds: report
    description: |-
      Create a Funnel report called "Lead to Customer".
      Steps:
      1. Event "form_submitted" where form_id matches a demo-request form: "Requested Demo"
       (alternative: deal_created with stage matching "Discovery" or similar)
      2. Event "meeting_scheduled" linked to the user (via primary_user_id or user_ids): "Scheduled Demo"
      3. Event "meeting_scheduled" where canceled_at is null AND end_time < now (i.e. meeting actually happened, no subsequent meeting_canceled): "Completed Demo"
      4. Event "deal_stage_changed" where new_stage matches a "Proposal" pattern: "Proposal Sent"
      5. Event "deal_won": "Deal Closed"
      Conversion window: 60 days
      Breakdown: By Users.utm_source attribute (first-touch lead source on the User record). Top 8 sources.
      Compare: Previous period (prior 60 days)
      For each step, also surface:
      - Median time-to-convert from previous step (stage velocity)
      - Per-source conversion rate at each stage
      - Forecast revenue: Sum of deal_created.amount (or current deal_stage_changed.amount) for deals currently at this stage × historical conversion-to-won rate
      Annotations:
      - Flag the lead source with highest end-to-end win rate AND volume: invest more there.
      - Flag any stage where median velocity exceeded 14 days (deal-stalled signal).
      - Highlight any source with rising volume but falling win rate (lead-quality erosion).
      Surface the projected closed-won revenue for the period based on current pipeline volumes.
      Taxonomy notes:
      - "demo_requested", "demo_completed", "proposal_sent" as standalone events do not exist. They are derived from form_submitted, meeting_scheduled, and deal_stage_changed.new_stage respectively.
      - deal_stage_changed has previous_stage and new_stage properties; deal stages are project-configured (the Deals object has stage as a relation attribute).
      - meeting_scheduled has canceled_at, start_time, end_time: completion is derived from these.
      - Users.utm_source is the canonical lead-source User attribute.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Lead to customer

Shows how many demo requests turn into booked meetings, completed demos, proposals and closed deals, and which lead sources actually convert.

## Steps

1. **Trace demo requests to closed deals** (builds report)

   A five step funnel over 60 days from a demo request form to a scheduled meeting, a meeting that actually happened, a proposal stage change and a won deal, split by the top 8 lead sources, with median time between stages and forecast revenue per stage.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Trace demo requests to closed deals"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
