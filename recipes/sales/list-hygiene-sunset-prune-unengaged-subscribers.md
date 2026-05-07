---
name: List Hygiene Sunset Prune Unengaged Subscribers
description: Identify long-inactive subscribers, run a 'last chance to stay in touch' re-permission ask, and auto-unsubscribe
  non-responders. Protects sender reputation and improves deliverability.
intempt:
  id: list-hygiene-sunset-prune-unengaged-subscribers
  version: 1.0.0
  slashCommand: /list-hygiene-sunset-prune-unengaged-subscribers
  shortDescription: Identify long-inactive subscribers, run a 'last chance to stay in touch' re-permission ask, and auto-unsubscribe
    non-responders. Protects sender reputation and improves deliverability.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - list
    - list-hygiene
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
    describe: 'Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. (Tailored for:
      List-hygiene sunset — prune unengaged subscribers.)'
    produces: content
  - id: build-attempt-journey
    describe: 'Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. (Tailored for: List-hygiene
      sunset — prune unengaged subscribers.)'
    produces: journey
  - id: build-suppression-workflow
    describe: 'Create a workflow automatically adding non-responders to the suppression list after the 14-day window. (Tailored
      for: List-hygiene sunset — prune unengaged subscribers.)'
    produces: workflow
  - id: build-deliverability-dashboard
    describe: 'Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement.
      (Tailored for: List-hygiene sunset — prune unengaged subscribers.)'
    produces: dashboard
---

# List Hygiene Sunset Prune Unengaged Subscribers

Identify long-inactive subscribers, run a 'last chance to stay in touch' re-permission ask, and auto-unsubscribe non-responders. Protects sender reputation and improves deliverability.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. (Tailored for: List-hygiene sunset — prune unengaged subscribers.)
2. Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. (Tailored for: List-hygiene sunset — prune unengaged subscribers.)
3. Create a workflow automatically adding non-responders to the suppression list after the 14-day window. (Tailored for: List-hygiene sunset — prune unengaged subscribers.)
4. Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement. (Tailored for: List-hygiene sunset — prune unengaged subscribers.)
