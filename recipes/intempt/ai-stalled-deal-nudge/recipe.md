---
id: ai-stalled-deal-nudge
title: AI nudge for a stalled deal
slash_command: /ai-stalled-deal-nudge
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Drafts a personalized re-engagement email for stalled deals using CRM deal context, leaving it for the rep
  to review and send.
description: >-
  When a deal is detected as stalled, generate an AI-drafted re-engagement message referencing deal history
  and an offered next step. The rep reviews and sends, avoiding generic check-in messages.
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
    - ai-draft
    - deal-revival
    - stalled-deal
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Recall why it stalled"
    - A new workflow, from step 2 "Draft a nudge that names it"
    - A new dashboard, from step 3 "Compare against a rep's own"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Recall why it stalled
    summary: >-
      Built when a deal goes stalled: which stage it stuck at, the next step agreed at the last meeting
      that never happened, the last objection raised on a call, any deadline that may now be passing,
      and other people at the account worth approaching if the contact has gone quiet.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'nudge_context' on the Deal object, computed when the deal enters
      stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing (each
      requires different nudge angle); (b) last meeting_summary if available) most useful is the 'next
      step' that was agreed and apparently not happening; (c) most recent objection raised (from call
      summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder
      candidates if the original contact has gone quiet.
  - id: s2
    title: Draft a nudge that names it
    summary: >-
      Fires on a newly stalled deal. The email quotes the specific blocker from the meeting notes rather
      than checking in, is saved to the rep's drafts, and comes with a review task and a Slack message.
      Always sent by the rep. If the deal is still stalled 14 days later, a manager version is drafted
      for sign off.
    builds: workflow
    description: >-
      Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection
      workflow's output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email
      using the context. Distinct from the template-based nudge in stalled-deal-detection: this version
      is HIGHLY personalized using meeting-summary specifics ('Last time we talked, you mentioned [verbatim
      objection]. Has anything changed on [specific blocker]?'); (3) save draft to rep's outbox; (4) create
      rep task labeled 'Review AI-drafted nudge: deal [name]' with the draft preview; (5) Slack DM with
      deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft
      sent, escalate to manager with manager-version draft (this needs your sign-off). Use the result
      of "Recall why it stalled".
    dependsOn:
      - s1
  - id: s3
    title: Compare against a rep's own
    summary: >-
      How many stalled deals got a draft and how many are still unreviewed, the reply rate against nudges
      reps wrote themselves, how many deals move a stage afterwards, and the ARR brought back.
    builds: dashboard
    description: >-
      Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts
      not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival
      rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control:
      stalled deals where reps wrote their own nudge: typically AI-drafted personalized nudges win on
      reply rate by 1.5-2x. Use the result of "Recall why it stalled", "Draft a nudge that names it".
    dependsOn:
      - s1
      - s2
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# AI nudge for a stalled deal

Drafts a personalized re-engagement email for stalled deals using CRM deal context, leaving it for the rep to review and send.

## Steps

1. **Recall why it stalled** (builds attribute)

   Built when a deal goes stalled: which stage it stuck at, the next step agreed at the last meeting that never happened, the last objection raised on a call, any deadline that may now be passing, and other people at the account worth approaching if the contact has gone quiet.

2. **Draft a nudge that names it** (builds workflow)

   Fires on a newly stalled deal. The email quotes the specific blocker from the meeting notes rather than checking in, is saved to the rep's drafts, and comes with a review task and a Slack message. Always sent by the rep. If the deal is still stalled 14 days later, a manager version is drafted for sign off.

3. **Compare against a rep's own** (builds dashboard)

   How many stalled deals got a draft and how many are still unreviewed, the reply rate against nudges reps wrote themselves, how many deals move a stage afterwards, and the ARR brought back.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new attribute, from step 1 "Recall why it stalled"
- A new workflow, from step 2 "Draft a nudge that names it"
- A new dashboard, from step 3 "Compare against a rep's own"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
