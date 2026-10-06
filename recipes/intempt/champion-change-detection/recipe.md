---
id: champion-change-detection
title: Champion change detection
slash_command: /champion-change-detection
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Flags when a deal contact goes quiet using engagement recency, and triggers a rep re-engagement workflow
  before the deal stalls.
description: >-
  Use engagement recency to identify contacts on open deals who have stopped responding. Segment those
  contacts, launch a re-engagement workflow for the rep, and track activity in a dashboard.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
    - media
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - champion-tracking
    - deal-health
    - early-warning
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: email_bounced
      severity: recommended
    - value: user_identified
      severity: recommended
touches:
  reads:
    - The email_bounced event in your project
    - The user_identified event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Track the champion daily"
    - A new segment, from step 2 "Find deals that lost theirs"
    - A new workflow, from step 3 "Get the rep moving"
    - A new dashboard, from step 4 "See the ARR behind the risk"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track the champion daily
    summary: >-
      Active means they replied in the last 21 days, quiet means 21 to 45 days of silence, and gone means
      a bounced email, a departure signal, or enrichment showing a new company or a new title. Deals with
      nobody identified are flagged separately.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'champion_status' on the Deal object. Compute the deal's current
      champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days),
      GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new
      title at same company), or UNCLEAR (deal has no identified champion: separate flag). Refreshed daily.
      The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh,
      and account-domain consistency checks.
  - id: s2
    title: Find deals that lost theirs
    summary: >-
      Open deals whose champion went to gone in the last 7 days, plus deals quiet for 45 days or more,
      which amounts to the same thing. Closed lost deals are handled elsewhere.
    builds: segment
    description: >-
      Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned
      to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively
      gone). Excludes deals already in closed-lost (handled separately). Use the result of "Track the
      champion daily".
    dependsOn:
      - s1
  - id: s3
    title: Get the rep moving
    summary: >-
      It pulls replacement candidates from the account, peers, a manager or the same role elsewhere, raises
      an urgent task for the AE with that list and the deal history, alerts the AE and their manager in
      Slack, tags the deal as at risk so the forecast tells the truth, and points at any other contact
      active in the last 30 days as the warm way in. No email goes out automatically: the rep reaches
      out personally.
    builds: workflow
    description: >-
      Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion
      candidates from the account (similar role, peer, manager up: pulled from enrichment); (2) create
      an urgent task for the AE: 'Champion gone: re-engage stakeholders' with the candidate list and prior
      deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving
      moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5)
      IF account has any other active contact (engagement signal in last 30 days), prioritize that contact
      as warm-handoff. Don't auto-send email: rep must reach out personally. Use the result of "Track
      the champion daily", "Find deals that lost theirs".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: See the ARR behind the risk
    summary: >-
      Open deals by champion status, the ARR sitting behind departed champions, how often champions leave,
      how many deals survive it, and how quickly reps act, with anything left 14 days without action pulled
      out.
    builds: dashboard
    description: >-
      Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions
      (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered
      after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where
      champion has been GONE 14+ days with no rep action (escalation pile). Use the result of "Track the
      champion daily", "Find deals that lost theirs", "Get the rep moving".
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

# Champion change detection

Flags when a deal contact goes quiet using engagement recency, and triggers a rep re-engagement workflow before the deal stalls.

## Steps

1. **Track the champion daily** (builds attribute)

   Active means they replied in the last 21 days, quiet means 21 to 45 days of silence, and gone means a bounced email, a departure signal, or enrichment showing a new company or a new title. Deals with nobody identified are flagged separately.

2. **Find deals that lost theirs** (builds segment)

   Open deals whose champion went to gone in the last 7 days, plus deals quiet for 45 days or more, which amounts to the same thing. Closed lost deals are handled elsewhere.

3. **Get the rep moving** (builds workflow)

   It pulls replacement candidates from the account, peers, a manager or the same role elsewhere, raises an urgent task for the AE with that list and the deal history, alerts the AE and their manager in Slack, tags the deal as at risk so the forecast tells the truth, and points at any other contact active in the last 30 days as the warm way in. No email goes out automatically: the rep reaches out personally.

4. **See the ARR behind the risk** (builds dashboard)

   Open deals by champion status, the ARR sitting behind departed champions, how often champions leave, how many deals survive it, and how quickly reps act, with anything left 14 days without action pulled out.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The email_bounced event in your project
- The user_identified event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Track the champion daily"
- A new segment, from step 2 "Find deals that lost theirs"
- A new workflow, from step 3 "Get the rep moving"
- A new dashboard, from step 4 "See the ARR behind the risk"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
