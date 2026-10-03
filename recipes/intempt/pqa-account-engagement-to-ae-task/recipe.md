---
id: pqa-account-engagement-to-ae-task
title: Account level signal to AE task
slash_command: /pqa-account-engagement-to-ae-task
group: Workflows
owner: intempt
summary: When several people from one company start using the product in the same fortnight, it briefs
  an AE and asks them to open a deal.
description: >-
  When multiple users from the same account engage with the product in a short window (PQA signal) create
  an AE deal-creation task with the account's full engagement picture, because account-level signals are
  stronger than single-user signals.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - pqa
    - account-signal
    - ae-routing
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: user_signed_up
      severity: blocking
    - value: feature_used
      severity: blocking
steps:
  - id: s1
    title: Score the whole account
    summary: >-
      A 0 to 100 score per account from how many different people were active in the last 14 days, where
      three or more is a strong signal, the total feature events across them, whether any look like decision
      makers by title or email pattern, and how deeply the team uses it. 70 and above counts as qualified,
      updated daily and whenever someone new signs up from the domain.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'pqa_score' on the Account object. Composite: (a) count of distinct
      users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature
      events across the account; (c) seniority of users (any decision-makers based on title/email pattern);
      (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated
      daily and on new user signups from the domain.
  - id: s2
    title: Find accounts crossing 70
    summary: >-
      Accounts that crossed 70 in the last 14 days with no open deal and no AE engaged in the last 60
      days. Existing paying customers are left out, because expansion is a different play.
    builds: segment
    description: >-
      Build a segment 'PQA: accounts score >= 70' capturing accounts where pqa_score crossed 70 in the
      last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged
      in the last 60 days. Excludes existing paid customers (different motion: see seat-expansion workflow).
      Use the result of "Score the whole account".
    dependsOn:
      - s1
  - id: s3
    title: Brief an AE to open a deal
    summary: >-
      On crossing 70 it refreshes the account's firmographics, technographics and decision maker contacts,
      writes a summary of who is active, what each of them uses, who can sign, the headcount and the ICP
      fit, creates a high priority task to open a deal and start outreach with that attached, and notifies
      the AE and their manager in Slack. Only accounts matching your ICP fire.
    builds: workflow
    description: >-
      Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment
      (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute
      account context summary: active user count, key features used per user, decision-makers identified,
      employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach,
      with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with
      a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts. Use
      the result of "Score the whole account", "Find accounts crossing 70".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Compare against cold outbound
    summary: >-
      Accounts crossing the threshold each month, how long AEs take to open a deal, conversion to deals
      and to meetings, the ARR behind them, and how they compare with cold sourced deals on win rate and
      cycle time.
    builds: dashboard
    description: >-
      Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month),
      AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting
      rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs.
      cold-outbound-sourced deals on win-rate and cycle time: usually PQAs win 2-3x more reliably. Use
      the result of "Score the whole account", "Find accounts crossing 70", "Brief an AE to open a deal".
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

# Account level signal to AE task

When several people from one company start using the product in the same fortnight, it briefs an AE and asks them to open a deal.

## Steps

1. **Score the whole account** (builds attribute)

   A 0 to 100 score per account from how many different people were active in the last 14 days, where three or more is a strong signal, the total feature events across them, whether any look like decision makers by title or email pattern, and how deeply the team uses it. 70 and above counts as qualified, updated daily and whenever someone new signs up from the domain.

2. **Find accounts crossing 70** (builds segment)

   Accounts that crossed 70 in the last 14 days with no open deal and no AE engaged in the last 60 days. Existing paying customers are left out, because expansion is a different play.

3. **Brief an AE to open a deal** (builds workflow)

   On crossing 70 it refreshes the account's firmographics, technographics and decision maker contacts, writes a summary of who is active, what each of them uses, who can sign, the headcount and the ICP fit, creates a high priority task to open a deal and start outreach with that attached, and notifies the AE and their manager in Slack. Only accounts matching your ICP fire.

4. **Compare against cold outbound** (builds dashboard)

   Accounts crossing the threshold each month, how long AEs take to open a deal, conversion to deals and to meetings, the ARR behind them, and how they compare with cold sourced deals on win rate and cycle time.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
