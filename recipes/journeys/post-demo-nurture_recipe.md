---
name: post-demo-nurture
description: Use when a user mentions "post-demo nurture", "post-demo cadence", "after demo follow-up", or asks for related help. After a demo meeting completes, fire a multi-touch nurture cadence over 90 days, value content at Day 7, case study at Day 14, ROI calculator at Day 30, customer story at Day 60, decision-stage check-in at Day 90, branching on engagement signals.
arguments: []
intempt:
  id: post-demo-nurture
  title: "Post demo nurture"
  version: 1.0.0
  slashCommand: /post-demo-nurture
  group: Journeys
  shortDescription: "Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer story, and pulls the AE in early if they bite."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [post-demo, nurture]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: meeting_completed, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find recent demo attendees"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "People who attended a demo in the last 90 days with no deal won yet. Anyone already in an AE run deal cadence is left out."
      prompt: Build a segment 'Recent demo attendees - last 90 days' capturing users with a completed meeting of type demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually).
    - step: 2
      title: "Write five follow ups"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Day 7 a playbook on the use case from the demo. Day 14 a case study matched to their industry and size. Day 30 an ROI calculator prefilled with the numbers discussed. Day 60 a customer story showing six month outcomes. Day 90 a direct, low pressure note from the AE about timing, budget and who else is involved. All of it drawing on the demo summary."
      prompt: 'Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect''s industry + company size. Touch 3 (Day 30): ROI calculator link with prospect''s discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting summary signals from the original demo.'
    - step: 3
      title: "Send over 90 days"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Emails at day 7, 14, 30, 60 and 90 after the demo. Anyone who clicks the first or second is handed to the AE as a task and drops out of the automated run. They also leave on a new deal, a new meeting, or unsubscribe."
      prompt: 'Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to the completed meeting. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: Deal created, Meeting scheduled (re-engagement), or unsubscribe.'
    - step: 4
      title: "Track demo to deal"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey]
      description: "Demo to deal conversion at 60 and 90 days, which email loses the most people, how many AE handoffs it creates, and deal speed against demos that never went through it. Any email under a 1% reply rate is flagged."
      prompt: 'Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Post demo nurture

Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer story, and pulls the AE in early if they bite.

## Before you run it

- Send the `meeting_completed` event

## What it does

1. **Find recent demo attendees** (`create_segment`)

   People who attended a demo in the last 90 days with no deal won yet. Anyone already in an AE run deal cadence is left out.

2. **Write five follow ups** (`create_email_content`)

   Day 7 a playbook on the use case from the demo. Day 14 a case study matched to their industry and size. Day 30 an ROI calculator prefilled with the numbers discussed. Day 60 a customer story showing six month outcomes. Day 90 a direct, low pressure note from the AE about timing, budget and who else is involved. All of it drawing on the demo summary.

3. **Send over 90 days** (`create_journey`)

   Emails at day 7, 14, 30, 60 and 90 after the demo. Anyone who clicks the first or second is handed to the AE as a task and drops out of the automated run. They also leave on a new deal, a new meeting, or unsubscribe.

4. **Track demo to deal** (`create_dashboard`)

   Demo to deal conversion at 60 and 90 days, which email loses the most people, how many AE handoffs it creates, and deal speed against demos that never went through it. Any email under a 1% reply rate is flagged.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
