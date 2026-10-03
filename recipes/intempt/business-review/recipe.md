---
id: business-review
title: Weekly business review pack
slash_command: /business-review
group: Dashboards
owner: intempt
summary: Builds the weekly scorecard, writes the narrative on what moved and why, and posts both to Slack
  on the cadence you pick.
description: >-
  Headline metrics, week-over-week deltas, wins, concerns, recommended actions, scheduled Slack digest.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - all
  complexity: standard
  executionMode: live
  tags:
    - business-review
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new dashboard, from step 1 "Build the headline scorecard"
    - A new report, from step 2 "Write the period narrative"
    - A new workflow, from step 3 "Send it to Slack on a cadence"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the headline scorecard
    summary: >-
      Headline KPIs with week-over-week change, the top wins and the top concerns.
    builds: dashboard
    description: >-
      Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns.
  - id: s2
    title: Write the period narrative
    summary: >-
      A written summary of what changed over the period, why it changed, and what to do next.
    builds: report
    description: >-
      Generate a narrative report summarizing the period: what changed, why, and recommended actions.
      Use the result of "Build the headline scorecard".
    dependsOn:
      - s1
  - id: s3
    title: Send it to Slack on a cadence
    summary: >-
      Delivers the dashboard and the narrative to Slack on the schedule you choose.
    builds: workflow
    description: >-
      Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen
      cadence. Use the result of "Build the headline scorecard", "Write the period narrative".
    dependsOn:
      - s1
      - s2
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dashboard produced by this recipe.
  - key: report
    producedByStep: s2
    type: report
    description: Report produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly business review pack

Builds the weekly scorecard, writes the narrative on what moved and why, and posts both to Slack on the cadence you pick.

## Steps

1. **Build the headline scorecard** (builds dashboard)

   Headline KPIs with week-over-week change, the top wins and the top concerns.

2. **Write the period narrative** (builds report)

   A written summary of what changed over the period, why it changed, and what to do next.

3. **Send it to Slack on a cadence** (builds workflow)

   Delivers the dashboard and the narrative to Slack on the schedule you choose.

## What you end up with

- **dashboard** (dashboard): Dashboard produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new dashboard, from step 1 "Build the headline scorecard"
- A new report, from step 2 "Write the period narrative"
- A new workflow, from step 3 "Send it to Slack on a cadence"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, report, workflow.
