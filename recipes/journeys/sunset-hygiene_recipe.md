---
name: sunset-hygiene
description: |
  Use when a user mentions "sunset & list hygiene", or asks for related help. Re-engage long-unengaged users, then suppress them for deliverability protection.
arguments: []
intempt:
  id: sunset-hygiene
  title: "Sunset inactive subscribers"
  version: 1.0.0
  slashCommand: /sunset-hygiene
  group: Journeys
  shortDescription: "Gives subscribers who have ignored six months of email one chance to say they still want it, then stops mailing them to protect deliverability."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [all]
    complexity: advanced
    executionMode: live
    tags: [sunset-hygiene]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Find who stopped reading"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Subscribers who have not opened or clicked anything in 180 days or more."
      prompt: "Identify subscribers who have not opened or clicked any email in 180+ days."
    - step: 2
      title: "Write the last chance email"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "One email asking them to confirm they still want to hear from you, with a clear opt in."
      prompt: "Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA."
    - step: 3
      title: "Send it, then wait 14 days"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "The email goes out and the journey waits a fortnight for a response."
      prompt: "Build a 2-touch journey sending the final-attempt email and waiting 14 days for response."
    - step: 4
      title: "Suppress anyone who ignores it"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset, journey]
      description: "After the 14 days, everyone who did not respond is added to the suppression list."
      prompt: "Create a workflow automatically adding non-responders to the suppression list after the 14-day window."
    - step: 5
      title: "Watch your deliverability"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, workflow]
      description: "Send rate, open rate, complaints, bounces and inbox placement."
      prompt: "Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Sunset inactive subscribers

Gives subscribers who have ignored six months of email one chance to say they still want it, then stops mailing them to protect deliverability.

## What it does

1. **Find who stopped reading** (`create_segment`)

   Subscribers who have not opened or clicked anything in 180 days or more.

2. **Write the last chance email** (`create_email_content`)

   One email asking them to confirm they still want to hear from you, with a clear opt in.

3. **Send it, then wait 14 days** (`create_journey`)

   The email goes out and the journey waits a fortnight for a response.

4. **Suppress anyone who ignores it** (`create_workflow`)

   After the 14 days, everyone who did not respond is added to the suppression list.

5. **Watch your deliverability** (`create_dashboard`)

   Send rate, open rate, complaints, bounces and inbox placement.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
