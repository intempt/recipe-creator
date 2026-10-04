---
id: seat-expansion-signal-to-ae-task
title: Seat expansion signal to AE
slash_command: /seat-expansion-signal-to-ae-task
group: Workflows
owner: intempt
curator: trishik
summary: Tells the AE when a customer is running out of seats or people from their domain keep signing
  up, which is the clearest upsell signal there is.
description: >-
  When an existing customer adds users approaching their plan limit OR multiple new users from the same
  domain self-serve sign up, create an AE expansion task, the strongest predictor of a seat upsell opportunity.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - expansion
    - seat-upsell
    - ae-routing
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: user_signed_up
      severity: blocking
touches:
  reads:
    - The user_signed_up event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Measure how full the plan is"
    - A new segment, from step 2 "Find accounts near a limit"
    - A new workflow, from step 3 "Raise the expansion task"
    - A new dashboard, from step 4 "Track the expansion pipeline"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Measure how full the plan is
    summary: >-
      Active seats as a share of the plan limit, flagged at 80% and again above 100%, where the overage
      is being billed. It also shows net seat growth over 30 days, how many people from the domain signed
      up in the last 14 days without a seat, and how close they are to any other cap such as API calls
      or contacts.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'seat_capacity_used' on the Account object. Compute: (active_seats
      / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed
      as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the
      account's domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts,
      etc.).
  - id: s2
    title: Find accounts near a limit
    summary: >-
      Paying accounts at 80% of their seats or more, or with three or more unprovisioned signups from
      the domain in the last 14 days, or at 90% of any other cap. Accounts already in an expansion conversation
      are left out.
    builds: segment
    description: >-
      Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used
      >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR
      (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations
      (handled by AE). Use the result of "Measure how full the plan is".
    dependsOn:
      - s1
  - id: s3
    title: Raise the expansion task
    summary: >-
      When seats cross 80%, or a new signup arrives from a customer domain, it refreshes the account,
      checks whether an AE has engaged in the last 30 days and skips if so, then creates an expansion
      task naming which trigger fired, the current ARR, the plan and the likely upsell size, and messages
      the AE. Accounts with no AE go to the RevOps queue.
    builds: workflow
    description: >-
      Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event
      comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether
      AE already engaged this account in last 30 days (if so, skip: they're on it); (3) create an AE expansion
      task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current
      ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned
      AE, route to RevOps queue. Use the result of "Measure how full the plan is", "Find accounts near
      a limit".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Track the expansion pipeline
    summary: >-
      Signals per week by trigger, how fast AEs respond, how many tasks become deals, how long those deals
      take, which is usually two to three times faster than new business, the win rate, and the ARR added
      so far this year against target.
    builds: dashboard
    description: >-
      Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap
      / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion
      deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift
      from expansion signals YTD vs. target. Use the result of "Measure how full the plan is", "Find accounts
      near a limit", "Raise the expansion task".
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

# Seat expansion signal to AE

Tells the AE when a customer is running out of seats or people from their domain keep signing up, which is the clearest upsell signal there is.

## Steps

1. **Measure how full the plan is** (builds attribute)

   Active seats as a share of the plan limit, flagged at 80% and again above 100%, where the overage is being billed. It also shows net seat growth over 30 days, how many people from the domain signed up in the last 14 days without a seat, and how close they are to any other cap such as API calls or contacts.

2. **Find accounts near a limit** (builds segment)

   Paying accounts at 80% of their seats or more, or with three or more unprovisioned signups from the domain in the last 14 days, or at 90% of any other cap. Accounts already in an expansion conversation are left out.

3. **Raise the expansion task** (builds workflow)

   When seats cross 80%, or a new signup arrives from a customer domain, it refreshes the account, checks whether an AE has engaged in the last 30 days and skips if so, then creates an expansion task naming which trigger fired, the current ARR, the plan and the likely upsell size, and messages the AE. Accounts with no AE go to the RevOps queue.

4. **Track the expansion pipeline** (builds dashboard)

   Signals per week by trigger, how fast AEs respond, how many tasks become deals, how long those deals take, which is usually two to three times faster than new business, the win rate, and the ARR added so far this year against target.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The user_signed_up event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Measure how full the plan is"
- A new segment, from step 2 "Find accounts near a limit"
- A new workflow, from step 3 "Raise the expansion task"
- A new dashboard, from step 4 "Track the expansion pipeline"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
