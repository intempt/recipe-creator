---
name: Sunset Hygiene
description: Re-engage long-unengaged users, then suppress them for deliverability protection.
intempt:
  id: sunset-hygiene
  version: 1.0.0
  slashCommand: /sunset-hygiene
  shortDescription: Re-engage long-unengaged users, then suppress them for deliverability protection.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - all
    complexity: advanced
    executionMode: live
    tags:
    - sunset-hygiene
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-final-attempt-content
    describe: Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA.
    produces: content
  - id: build-attempt-journey
    describe: Build a 2-touch journey sending the final-attempt email and waiting 14 days for response.
    produces: journey
  - id: build-suppression-workflow
    describe: Create a workflow automatically adding non-responders to the suppression list after the 14-day window.
    produces: workflow
  - id: build-deliverability-dashboard
    describe: 'Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement.'
    produces: dashboard
---

# Sunset Hygiene

Re-engage long-unengaged users, then suppress them for deliverability protection.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA.
2. Build a 2-touch journey sending the final-attempt email and waiting 14 days for response.
3. Create a workflow automatically adding non-responders to the suppression list after the 14-day window.
4. Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement.
