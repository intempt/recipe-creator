---
id: stalled-deal-detection
title: Stalled deal detection
slash_command: /stalled-deal-detection
group: Workflows
owner: intempt
summary: Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits
  the stage, and escalates if they stay stuck.
description: >-
  Detect deals stuck in a stage longer than typical for that stage's median age, with no recent activity,
  and surface them with AI-drafted re-engagement nudges so reps can either revive or honestly close-lost
  (no more pipeline lying).
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
    - deal-hygiene
    - stalled-deals
    - pipeline-quality
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: deal_stage_changed
      severity: recommended
touches:
  reads:
    - The deal_stage_changed event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Measure how long it has sat"
    - A new segment, from step 2 "Find the genuinely stuck ones"
    - A new designed email, from step 3 "Write a nudge per stage"
    - A new workflow, from step 4 "Draft it and chase the rep"
    - A new dashboard, from step 5 "See what is really dead"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Measure how long it has sat
    summary: >-
      Refreshed daily: the days since the deal last changed stage, and where that sits against the historical
      median for that stage among similar deals by size, segment and rep. Anything in the top quartile
      is flagged, alongside the days since any meeting, email reply or completed task.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'days_in_current_stage' on the Deal object, refreshed daily. Compute:
      (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage's
      historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile
      (75th+ percentile) for that stage. Also compute 'days_since_last_activity' (any meeting / email
      reply / task completion on the deal).
  - id: s2
    title: Find the genuinely stuck ones
    summary: >-
      Open deals in the top quartile for time in stage with no activity for 14 days or more. Deals a rep
      has deliberately paused, for a restart next quarter or similar, are left out. Refreshed daily.
    builds: segment
    description: >-
      Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top
      quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep
      has manually set a 'paused' flag (legitimate pause, coming back next quarter, etc.). Refreshed daily.
      Use the result of "Measure how long it has sat".
    dependsOn:
      - s1
  - id: s3
    title: Write a nudge per stage
    summary: >-
      Discovery re-asks the qualifying question that never got answered. Demo offers a technical deep
      dive or a proof of concept. Proposal names the likely truth, that pricing pushback usually means
      the decision maker is not sold, and offers to align. Closing asks directly about the timeline and
      what is still in the way. Personalised from the last meeting summary, and sent by the rep.
    builds: email_html
    description: >-
      Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage:
      (a) Discovery stalled (re-ask the qualifying question that wasn't answered; (b) Demo stalled) offer
      technical deep-dive or POC; (c) Proposal stalled (surface that pricing pushback usually means decision-maker
      isn't bought in, offer to align; (d) Closing stalled) explicit clarity-ask about timeline + remaining
      blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest.
      The rep reviews and sends: not auto-send. Use the result of "Measure how long it has sat", "Find
      the genuinely stuck ones".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Draft it and chase the rep
    summary: >-
      Daily, for deals that became stalled in the last 24 hours: it writes the nudge from the template
      and the deal context, creates a review task for the owner with the draft attached, messages them
      in Slack with a preview, and escalates to their manager if the same deal is still stalled 14 days
      after the first nudge, which usually means it should be closed lost. Nothing sends automatically.
    builds: workflow
    description: >-
      Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment
      in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal
      context; (2) create a task for the deal owner labeled 'Review and send: stalled deal nudge' with
      the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + 'review' button;
      (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal:
      deal should probably be closed-lost). Don't auto-send the email: rep must review. Use the result
      of "Measure how long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: See what is really dead
    summary: >-
      Stalled deals by stage and rep, the ARR sitting in them, their median age, how many recover and
      move forward, and how many sit stalled for 30 days or more before being marked lost, which shows
      which reps let deals linger instead of closing them out honestly.
    builds: dashboard
    description: >-
      Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum
      of stalled deals' values), median age of stalled deals, recovery rate (stalled deals that re-engaged
      and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost:
      measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view:
      which reps consistently let deals stall vs. honestly close-lost. Use the result of "Measure how
      long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage", "Draft it and chase
      the rep".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s4
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Stalled deal detection

Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits the stage, and escalates if they stay stuck.

## Steps

1. **Measure how long it has sat** (builds attribute)

   Refreshed daily: the days since the deal last changed stage, and where that sits against the historical median for that stage among similar deals by size, segment and rep. Anything in the top quartile is flagged, alongside the days since any meeting, email reply or completed task.

2. **Find the genuinely stuck ones** (builds segment)

   Open deals in the top quartile for time in stage with no activity for 14 days or more. Deals a rep has deliberately paused, for a restart next quarter or similar, are left out. Refreshed daily.

3. **Write a nudge per stage** (builds email_html)

   Discovery re-asks the qualifying question that never got answered. Demo offers a technical deep dive or a proof of concept. Proposal names the likely truth, that pricing pushback usually means the decision maker is not sold, and offers to align. Closing asks directly about the timeline and what is still in the way. Personalised from the last meeting summary, and sent by the rep.

4. **Draft it and chase the rep** (builds workflow)

   Daily, for deals that became stalled in the last 24 hours: it writes the nudge from the template and the deal context, creates a review task for the owner with the draft attached, messages them in Slack with a preview, and escalates to their manager if the same deal is still stalled 14 days after the first nudge, which usually means it should be closed lost. Nothing sends automatically.

5. **See what is really dead** (builds dashboard)

   Stalled deals by stage and rep, the ARR sitting in them, their median age, how many recover and move forward, and how many sit stalled for 30 days or more before being marked lost, which shows which reps let deals linger instead of closing them out honestly.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The deal_stage_changed event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Measure how long it has sat"
- A new segment, from step 2 "Find the genuinely stuck ones"
- A new designed email, from step 3 "Write a nudge per stage"
- A new workflow, from step 4 "Draft it and chase the rep"
- A new dashboard, from step 5 "See what is really dead"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
