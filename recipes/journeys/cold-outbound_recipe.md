---
name: cold-outbound
description: |
  Use when a user mentions "cold outbound campaign", or asks for related help. Target list, multi-touch sequence, tailored content, deliverability protection.
arguments: []
intempt:
  id: cold-outbound
  version: 1.0.0
  slashCommand: /cold-outbound
  group: Journeys
  shortDescription: "Target list, multi-touch sequence, tailored content, deliverability protection."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: outreach-rep
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [cold-outbound]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - get_booking_link
    - create_dashboard
  procedure:
    - step: 1
      title: "Build Target List"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Build target prospect list from ICP criteria (firmographic + intent signals)."
      prompt: "Build target prospect list from ICP criteria (firmographic + intent signals)."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens."
      prompt: "Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens."
    - step: 3
      title: "Build Sequence Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a multi-touch outbound journey with appropriate cadence and break-up logic."
      prompt: "Build a multi-touch outbound journey with appropriate cadence and break-up logic."
    - step: 4
      title: "Build Meeting Link"
      command: get_booking_link
      produces: scheduling_link
      bindsAs: scheduling_link
      dependsOn: [segment, asset, journey]
      description: "Configure the booking link reps include in outreach, with availability and meeting-type config."
      prompt: "Configure the booking link reps include in outreach, with availability and meeting-type config."
    - step: 5
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, scheduling_link]
      description: "Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution."
      prompt: "Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: scheduling_link, type: scheduling_link, cardinality: single, description: "Scheduling Link produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Cold Outbound Campaign

## Procedure

1. **Build Target List** [`create_segment`] — Build target prospect list from ICP criteria (firmographic + intent signals). → produces: segment
2. **Build Content** [`create_email_content`] — Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens. → produces: asset
3. **Build Sequence Journey** [`create_journey`] — Build a multi-touch outbound journey with appropriate cadence and break-up logic. → produces: journey
4. **Build Meeting Link** [`get_booking_link`] — Configure the booking link reps include in outreach, with availability and meeting-type config. → produces: scheduling_link
5. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution. → produces: dashboard
