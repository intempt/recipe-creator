---
id: pql-signal-to-sdr-task
title: Product qualified lead to SDR task
slash_command: /pql-signal-to-sdr-task
group: Workflows
owner: intempt
curator: trishik
summary: When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying
  everything needed for the first touch.
description: >-
  When a free-tier user crosses a PQL behavioral threshold (feature use, depth, repeated sessions), create
  an enriched SDR task with the qualification context so the rep has everything needed for first-touch
  in one click.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - ecommerce
  vertical:
    - plg
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - pql
    - sdr-routing
    - product-led-growth
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: feature_used
      severity: blocking
    - value: session_start
      severity: recommended
touches:
  reads:
    - The feature_used event in your project
    - The session_start event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Score free users on behaviour"
    - A new segment, from step 2 "Find free users crossing 70"
    - A new workflow, from step 3 "Give the SDR the context"
    - A new dashboard, from step 4 "Hold the 24 hour first touch"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score free users on behaviour
    summary: >-
      A 0 to 100 score weighting the high value activation events most heavily, then depth, meaning sessions
      in the last 14 days, features touched and time in the product, then how many other people from the
      same domain are active. 70 and above counts as qualified, refreshed daily and whenever a feature
      is used.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'pql_score' on the User object. Composite signal: (a) high-value
      feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days,
      features touched, time-in-product); (c) account-level density (other users from same domain active).
      Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.
  - id: s2
    title: Find free users crossing 70
    summary: >-
      Free tier users who crossed 70 in the last 7 days with no SDR task open and no outreach in the last
      30 days. Paying users and anyone who has opted out are left out.
    builds: segment
    description: >-
      Build a segment 'PQL: free users score >= 70' capturing free-tier users where pql_score crossed
      70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach
      has occurred. Excludes paid users (different workflow) and users in opt-out list. Use the result
      of "Score free users on behaviour".
    dependsOn:
      - s1
  - id: s3
    title: Give the SDR the context
    summary: >-
      On crossing 70 it enriches the account if needed, gathers the top features used, how often they
      are in, the company size and the ICP tier, creates a high priority SDR task with that attached,
      assigns it by territory, then messages the SDR in Slack. Accounts below your ICP threshold go to
      self serve nurture instead.
    builds: workflow
    description: >-
      Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user's account
      if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used,
      usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach
      context attached, assigned via territory rules (geo / industry / account size); (4) post a brief
      Slack notification to the assigned SDR's DM with the task link. If account is below ICP threshold,
      route to self-serve nurture journey instead of SDR queue. Use the result of "Score free users on
      behaviour", "Find free users crossing 70".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Hold the 24 hour first touch
    summary: >-
      How many users cross the threshold each week and the trend, the median time to first contact against
      a 24 hour target, conversion to meetings and to deals by ICP tier, and a rep leaderboard, with any
      week where more than 20% go untouched for 48 hours flagged.
    builds: dashboard
    description: >-
      Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week,
      trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting
      conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs
      at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours. Use the result
      of "Score free users on behaviour", "Find free users crossing 70", "Give the SDR the context".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product qualified lead to SDR task

When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying everything needed for the first touch.

## Steps

1. **Score free users on behaviour** (builds attribute)

   A 0 to 100 score weighting the high value activation events most heavily, then depth, meaning sessions in the last 14 days, features touched and time in the product, then how many other people from the same domain are active. 70 and above counts as qualified, refreshed daily and whenever a feature is used.

2. **Find free users crossing 70** (builds segment)

   Free tier users who crossed 70 in the last 7 days with no SDR task open and no outreach in the last 30 days. Paying users and anyone who has opted out are left out.

3. **Give the SDR the context** (builds workflow)

   On crossing 70 it enriches the account if needed, gathers the top features used, how often they are in, the company size and the ICP tier, creates a high priority SDR task with that attached, assigns it by territory, then messages the SDR in Slack. Accounts below your ICP threshold go to self serve nurture instead.

4. **Hold the 24 hour first touch** (builds dashboard)

   How many users cross the threshold each week and the trend, the median time to first contact against a 24 hour target, conversion to meetings and to deals by ICP tier, and a rep leaderboard, with any week where more than 20% go untouched for 48 hours flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project
- The session_start event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Score free users on behaviour"
- A new segment, from step 2 "Find free users crossing 70"
- A new workflow, from step 3 "Give the SDR the context"
- A new dashboard, from step 4 "Hold the 24 hour first touch"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
