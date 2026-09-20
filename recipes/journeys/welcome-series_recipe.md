---
name: welcome-series
description: |
  Use when a user mentions "welcome series", "onboarding", "welcome series", or asks for related help. First-touch sequence for new subscribers: segment, content, journey, A/B variants, performance dashboard.
arguments: []
intempt:
  id: welcome-series
  title: "Welcome series"
  version: 1.0.0
  slashCommand: /welcome-series
  group: Journeys
  shortDescription: "Introduces your brand to new subscribers over their first week in four emails, and tests the subject lines and the opening offer."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [all]
    complexity: advanced
    executionMode: live
    tags: [welcome-series]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Find new subscribers"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who subscribed in the last 30 days and has not had a welcome email yet."
      prompt: "Identify users who subscribed within the last 30 days and have not received a welcome email yet."
    - step: 2
      title: "Write the four emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "A sequence introducing the brand, the product and what it is for, in your brand voice."
      prompt: "Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice."
    - step: 3
      title: "Send across the first week"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "The four emails go out straight away, then after a day, after three days, and after a week."
      prompt: "Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription."
    - step: 4
      title: "Test subject lines and offer"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey]
      description: "A/B variants on the subject lines and on whether the welcome offer appears at all."
      prompt: "Add A/B variants on subject lines and welcome offer presence."
    - step: 5
      title: "Track the first purchase"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, experiment]
      description: "Opens, clicks, conversion, and how long a new subscriber takes to buy."
      prompt: "Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Welcome series

Introduces your brand to new subscribers over their first week in four emails, and tests the subject lines and the opening offer.

## What it does

1. **Find new subscribers** (`create_segment`)

   Anyone who subscribed in the last 30 days and has not had a welcome email yet.

2. **Write the four emails** (`create_email_content`)

   A sequence introducing the brand, the product and what it is for, in your brand voice.

3. **Send across the first week** (`create_journey`)

   The four emails go out straight away, then after a day, after three days, and after a week.

4. **Test subject lines and offer** (`create_experiment`)

   A/B variants on the subject lines and on whether the welcome offer appears at all.

5. **Track the first purchase** (`create_dashboard`)

   Opens, clicks, conversion, and how long a new subscriber takes to buy.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
