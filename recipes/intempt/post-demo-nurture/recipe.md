---
id: post-demo-nurture
title: Post demo nurture
slash_command: /post-demo-nurture
group: Journeys
owner: intempt
summary: Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer
  story, and pulls the AE in early if they bite.
description: >-
  After a demo meeting completes, fire a multi-touch nurture cadence over 90 days, value content at Day
  7, case study at Day 14, ROI calculator at Day 30, customer story at Day 60, decision-stage check-in
  at Day 90, branching on engagement signals.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - post-demo
    - nurture
prerequisites:
  events:
    - value: meeting_completed
      severity: blocking
steps:
  - id: s1
    title: Find recent demo attendees
    summary: >-
      People who attended a demo in the last 90 days with no deal won yet. Anyone already in an AE run
      deal cadence is left out.
    builds: segment
    description: >-
      Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed
      event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes
      users already in active deal-stage cadences (handled by AE manually).
  - id: s2
    title: Write five follow ups
    summary: >-
      Day 7 a playbook on the use case from the demo. Day 14 a case study matched to their industry and
      size. Day 30 an ROI calculator prefilled with the numbers discussed. Day 60 a customer story showing
      six month outcomes. Day 90 a direct, low pressure note from the AE about timing, budget and who
      else is involved. All of it drawing on the demo summary.
    builds: email_html
    description: >-
      Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly
      relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect's industry
      + company size. Touch 3 (Day 30): ROI calculator link with prospect's discussed metrics pre-filled
      where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from
      a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure
      questions about timing/budget/champion status. Personalize using meeting_summary signals from the
      original demo. Use the result of "Find recent demo attendees".
    dependsOn:
      - s1
  - id: s3
    title: Send over 90 days
    summary: >-
      Emails at day 7, 14, 30, 60 and 90 after the demo. Anyone who clicks the first or second is handed
      to the AE as a task and drops out of the automated run. They also leave on a new deal, a new meeting,
      or unsubscribe.
    builds: journey
    description: >-
      Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch
      3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement
      branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of
      continuing the automated cadence (signal of buying intent). Exit conditions: deal_created, meeting_scheduled
      (re-engagement), or unsubscribe. Use the result of "Find recent demo attendees", "Write five follow
      ups".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Track demo to deal
    summary: >-
      Demo to deal conversion at 60 and 90 days, which email loses the most people, how many AE handoffs
      it creates, and deal speed against demos that never went through it. Any email under a 1% reply
      rate is flagged.
    builds: dashboard
    description: >-
      Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d),
      drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count
      of high-engagement branches), and deal-velocity comparison between demos that went through the cadence
      vs not. Flag touches with reply rate below 1% (content failure signal). Use the result of "Find
      recent demo attendees", "Write five follow ups", "Send over 90 days".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Post demo nurture

Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer story, and pulls the AE in early if they bite.

## Steps

1. **Find recent demo attendees** (builds segment)

   People who attended a demo in the last 90 days with no deal won yet. Anyone already in an AE run deal cadence is left out.

2. **Write five follow ups** (builds email_html)

   Day 7 a playbook on the use case from the demo. Day 14 a case study matched to their industry and size. Day 30 an ROI calculator prefilled with the numbers discussed. Day 60 a customer story showing six month outcomes. Day 90 a direct, low pressure note from the AE about timing, budget and who else is involved. All of it drawing on the demo summary.

3. **Send over 90 days** (builds journey)

   Emails at day 7, 14, 30, 60 and 90 after the demo. Anyone who clicks the first or second is handed to the AE as a task and drops out of the automated run. They also leave on a new deal, a new meeting, or unsubscribe.

4. **Track demo to deal** (builds dashboard)

   Demo to deal conversion at 60 and 90 days, which email loses the most people, how many AE handoffs it creates, and deal speed against demos that never went through it. Any email under a 1% reply rate is flagged.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
