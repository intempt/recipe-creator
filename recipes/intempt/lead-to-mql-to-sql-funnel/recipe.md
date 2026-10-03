---
id: lead-to-mql-to-sql-funnel
title: Lead qualification funnel
slash_command: /lead-to-mql-to-sql-funnel
group: Reports
owner: intempt
summary: Shows how leads move through MQL, SQL, demo and closed won, where they stall, and how long the
  whole cycle takes.
description: >-
  Qualification funnel built on lead_stage_changed transitions with per-stage velocity.
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
    - A new report, from step 1 "Track leads through qualification"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track leads through qualification
    summary: >-
      A five step funnel over 90 days from lead created to MQL, deal created, completed demo and closed
      won, split by the top 6 sources, with median time per stage. Flags sources under 20% from MQL to
      SQL or under 15% from SQL to won.
    builds: report
    description: |-
      Create a Funnel report called "Lead Qualification Funnel".
      Steps:
      1. Event "user_created" where Users.utm_source is not empty: "Lead Created"
      2. Event "lead_stage_changed" where new_stage indicates MQL (lead_stage relation matches MQL stage in the project's lead-stage configuration), aggregation: Count Unique Users per lead: "Reached MQL"
      3. Event "deal_created" linked to the user (via primary_user_id or user_ids): "SQL Created"
      4. Event "meeting_scheduled" where canceled_at is null AND end_time < now: "Demo Completed"
      5. Event "deal_won": "Closed Won"
      Conversion window: 90 days
      Breakdown: By Users.utm_source (top 6 sources)
      Compare: Previous period (prior 90 days)
      For each step, also surface:
      - Median time-to-convert from previous step
      - Per-source conversion rate at each stage
      - Stage velocity from Step 1 to Step 5 (full sales-cycle length)
      Annotations:
      - Flag the largest stage drop-off.
      - Flag any source where MQL-to-SQL conversion is below 20% (MQL definition issue for that source).
      - Flag any source where SQL-to-Closed-Won is below 15% (deal-execution issue).
      - Highlight sources with high volume AND end-to-end conversion >5%.
      Surface the median sales-cycle length and whether it's increasing or decreasing.
      Taxonomy notes:
      - "lead_score" as a property is not canonical. Lead progression is tracked via lead_stage_changed events (which include score, intent_trend, stage_changed_by properties). The lead_stage relation on the User points to a configured lead-stage record.
      - The MQL/SQL boundary is project-specific; the recipe uses the lead_stage_changed.new_stage relation against the project's stage configuration.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Lead qualification funnel

Shows how leads move through MQL, SQL, demo and closed won, where they stall, and how long the whole cycle takes.

## Steps

1. **Track leads through qualification** (builds report)

   A five step funnel over 90 days from lead created to MQL, deal created, completed demo and closed won, split by the top 6 sources, with median time per stage. Flags sources under 20% from MQL to SQL or under 15% from SQL to won.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track leads through qualification"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
