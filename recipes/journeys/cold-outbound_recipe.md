---
name: cold-outbound
description: |
  Use when a user mentions "cold outbound campaign", or asks for related help. Target list, multi-touch sequence, tailored content, deliverability protection.
arguments: []
intempt:
  id: cold-outbound
  title: "Cold outbound sequence"
  version: 1.0.0
  slashCommand: /cold-outbound
  group: Journeys
  shortDescription: "Builds a target list from your ICP, runs a multi touch sequence with a booking link in it, and shows what pipeline came out."
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
      title: "Build the target list"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Prospects matched to your ICP on company fit and intent signals."
      prompt: "Build target prospect list from ICP criteria (firmographic + intent signals)."
    - step: 2
      title: "Write the outbound emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Cold email templates in your brand voice, with tokens for the details specific to each prospect."
      prompt: "Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens."
    - step: 3
      title: "Run the touches, then break off"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "A multi touch sequence with a set cadence and breakup logic for prospects who stay silent."
      prompt: "Build a multi-touch outbound journey with appropriate cadence and break-up logic."
    - step: 4
      title: "Set up the booking link"
      command: get_booking_link
      produces: scheduling_link
      bindsAs: scheduling_link
      dependsOn: [segment, asset, journey]
      description: "The link reps drop into outreach, with your availability and meeting types configured."
      prompt: "Configure the booking link reps include in outreach, with availability and meeting-type config."
    - step: 5
      title: "Track replies and meetings"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, scheduling_link]
      description: "Outreach volume, reply rate, meetings booked, and the pipeline it contributed."
      prompt: "Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: scheduling_link, type: scheduling_link, cardinality: single, description: "Scheduling Link produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cold outbound sequence

Builds a target list from your ICP, runs a multi touch sequence with a booking link in it, and shows what pipeline came out.

## What it does

1. **Build the target list** (`create_segment`)

   Prospects matched to your ICP on company fit and intent signals.

2. **Write the outbound emails** (`create_email_content`)

   Cold email templates in your brand voice, with tokens for the details specific to each prospect.

3. **Run the touches, then break off** (`create_journey`)

   A multi touch sequence with a set cadence and breakup logic for prospects who stay silent.

4. **Set up the booking link** (`get_booking_link`)

   The link reps drop into outreach, with your availability and meeting types configured.

5. **Track replies and meetings** (`create_dashboard`)

   Outreach volume, reply rate, meetings booked, and the pipeline it contributed.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **scheduling_link** (scheduling_link): Scheduling Link produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
