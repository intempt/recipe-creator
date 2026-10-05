---
name: sunset-hygiene
description: |
  Use when a user mentions "sunset & list hygiene", or asks for related help. Re-engage long-unengaged users, then suppress them for deliverability protection.
arguments: []
intempt:
  id: sunset-hygiene
  version: 1.0.0
  slashCommand: /sunset-hygiene
  group: Journeys
  shortDescription: "Create a 180-day inactive subscriber segment, final-attempt re-engagement email, 2-touch journey, and suppression workflow for non-responders after 14 days."
  availability: coming-soon
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
      title: "Identify Unengaged"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify subscribers who have not opened or clicked any email in 180+ days."
      prompt: "Identify subscribers who have not opened or clicked any email in 180+ days."
    - step: 2
      title: "Build Final Attempt Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA."
      prompt: "Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA."
    - step: 3
      title: "Build Attempt Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a 2-touch journey sending the final-attempt email and waiting 14 days for response."
      prompt: "Build a 2-touch journey sending the final-attempt email and waiting 14 days for response."
    - step: 4
      title: "Build Suppression Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset, journey]
      description: "Create a workflow automatically adding non-responders to the suppression list after the 14-day window."
      prompt: "Create a workflow automatically adding non-responders to the suppression list after the 14-day window."
    - step: 5
      title: "Build Deliverability Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, workflow]
      description: "Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement."
      prompt: "Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Sunset & List Hygiene

## Procedure

1. **Identify Unengaged** [`create_segment`] — Identify subscribers who have not opened or clicked any email in 180+ days. → produces: segment
2. **Build Final Attempt Content** [`create_email_content`] — Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. → produces: asset
3. **Build Attempt Journey** [`create_journey`] — Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. → produces: journey
4. **Build Suppression Workflow** [`create_workflow`] — Create a workflow automatically adding non-responders to the suppression list after the 14-day window. → produces: workflow
5. **Build Deliverability Dashboard** [`create_dashboard`] — Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement. → produces: dashboard
