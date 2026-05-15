---
name: post-demo-nurture
description: Use when a user mentions "post-demo nurture", "post-demo cadence", "after demo follow-up", or asks for related help. After a demo meeting completes, fire a multi-touch nurture cadence over 90 days — value content at Day 7, case study at Day 14, ROI calculator at Day 30, customer story at Day 60, decision-stage check-in at Day 90 — branching on engagement signals.
arguments: []
intempt:
  id: post-demo-nurture
  version: 1.0.0
  slashCommand: /post-demo-nurture
  group: Journeys
  shortDescription: "After a demo meeting completes, fire a multi-touch nurture cadence over 90 days — value content at Day 7, case study at Day 14, ROI calculator at Day 30, customer story at Day 60, decision-stage check-in at Day 90 — branching on engagement signals."
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
      title: Identify Recent Demo Attendees
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually).
      prompt: Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually).
    - step: 2
      title: Build Cadence Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: 'Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect''s industry + company size. Touch 3 (Day 30): ROI calculator link with prospect''s discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting_summary signals from the original demo.'
      prompt: 'Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect''s industry + company size. Touch 3 (Day 30): ROI calculator link with prospect''s discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting_summary signals from the original demo.'
    - step: 3
      title: Build Nurture Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: 'Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: deal_created, meeting_scheduled (re-engagement), or unsubscribe.'
      prompt: 'Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: deal_created, meeting_scheduled (re-engagement), or unsubscribe.'
    - step: 4
      title: Build Post-Demo Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey]
      description: 'Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal).'
      prompt: 'Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Post Demo Nurture

## Procedure

1. **Identify Recent Demo Attendees** [`create_segment`] — Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually). → produces: segment
2. **Build Cadence Content** [`create_email_content`] — Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect's industry + company size. Touch 3 (Day 30): ROI calculator link with prospect's discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting_summary signals from the original demo. → produces: asset
3. **Build Nurture Journey** [`create_journey`] — Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: deal_created, meeting_scheduled (re-engagement), or unsubscribe. → produces: journey
4. **Build Post-Demo Performance Dashboard** [`create_dashboard`] — Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal). → produces: dashboard
