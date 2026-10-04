---
id: single-threaded-deal-alert
title: Single threaded deal alert
slash_command: /single-threaded-deal-alert
group: Workflows
owner: intempt
curator: trishik
summary: Finds late stage deals where only one person on the buyer's side is engaged and gives the rep
  three other names to bring in.
description: >-
  Detect deals where only one contact from the buyer side is engaged, single-threaded deals lose 3x more
  often when the lone champion leaves or doesn't have authority. Surface them with a multi-threading task
  and a recommended contact list.
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
    - multi-threading
    - deal-health
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: deal_stage_changed
      severity: recommended
    - value: meeting_completed
      severity: recommended
touches:
  reads:
    - The deal_stage_changed event in your project
    - The meeting_completed event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Count who is actually engaged"
    - A new segment, from step 2 "Find the risky ones"
    - A new workflow, from step 3 "Give the rep three names"
    - A new dashboard, from step 4 "See what threading is worth"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Count who is actually engaged
    summary: >-
      The number of people on the buyer's side who have attended a meeting on this deal, replied to an
      email on it, or been added as a contact. One person at demo, proposal or closing stage is flagged.
      One person early on is normal.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'threading_depth' on the Deal object. Count distinct buyer-side contacts
      who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been
      explicitly added as a deal contact. Output: integer count. Flag as 'single-threaded' if count =
      1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage
      is a red flag).
  - id: s2
    title: Find the risky ones
    summary: >-
      Open deals with a single engaged contact at demo, proposal or closing. Deals under 14 days old are
      left out, because multi threading takes time, and so are deals marked as a genuine single buyer,
      such as a founder led small business.
    builds: segment
    description: >-
      Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth
      = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for
      multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some
      buyer profiles, e.g. founder-led SMB). Use the result of "Count who is actually engaged".
    dependsOn:
      - s1
  - id: s3
    title: Give the rep three names
    summary: >-
      Daily, for newly flagged deals, it recounts the contacts, pulls suggested additions from enrichment,
      peers, the manager above and related team members, ranked by likely influence on the decision, creates
      a task with that list attached, and messages the rep. If the lone contact is the decision maker,
      it stays quiet.
    builds: workflow
    description: >-
      Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute
      threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional
      contacts from account enrichment (peer roles, manager up, related team members), prioritized by
      likely-buying-influence; (3) create a task for the rep labeled 'Multi-thread this deal: 3 suggested
      contacts' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone
      champion is the decision-maker (CEO of a small co, etc.), suppress: that's not single-threading
      risk. Use the result of "Count who is actually engaged", "Find the risky ones".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: See what threading is worth
    summary: >-
      The share of mid and late stage deals with more than one contact against a 70% target, where under
      50% is a coaching gap, the depth by stage, the win rate of single threaded deals against multi threaded
      ones, a rep leaderboard, and the deals single threaded for over 30 days.
    builds: dashboard
    description: >-
      Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+;
      below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win
      rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth,
      and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile). Use the result
      of "Count who is actually engaged", "Find the risky ones", "Give the rep three names".
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

# Single threaded deal alert

Finds late stage deals where only one person on the buyer's side is engaged and gives the rep three other names to bring in.

## Steps

1. **Count who is actually engaged** (builds attribute)

   The number of people on the buyer's side who have attended a meeting on this deal, replied to an email on it, or been added as a contact. One person at demo, proposal or closing stage is flagged. One person early on is normal.

2. **Find the risky ones** (builds segment)

   Open deals with a single engaged contact at demo, proposal or closing. Deals under 14 days old are left out, because multi threading takes time, and so are deals marked as a genuine single buyer, such as a founder led small business.

3. **Give the rep three names** (builds workflow)

   Daily, for newly flagged deals, it recounts the contacts, pulls suggested additions from enrichment, peers, the manager above and related team members, ranked by likely influence on the decision, creates a task with that list attached, and messages the rep. If the lone contact is the decision maker, it stays quiet.

4. **See what threading is worth** (builds dashboard)

   The share of mid and late stage deals with more than one contact against a 70% target, where under 50% is a coaching gap, the depth by stage, the win rate of single threaded deals against multi threaded ones, a rep leaderboard, and the deals single threaded for over 30 days.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The deal_stage_changed event in your project
- The meeting_completed event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Count who is actually engaged"
- A new segment, from step 2 "Find the risky ones"
- A new workflow, from step 3 "Give the rep three names"
- A new dashboard, from step 4 "See what threading is worth"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
