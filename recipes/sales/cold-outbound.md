---
name: Cold Outbound
description: Target list, multi-touch sequence, tailored content, deliverability protection.
intempt:
  id: cold-outbound
  version: 1.0.0
  slashCommand: /cold-outbound
  shortDescription: Target list, multi-touch sequence, tailored content, deliverability protection.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: outreach-rep
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - cold-outbound
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
  - name: scheduling_link
    type: scheduling-link
    description: Scheduling Link produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens.
    produces: content
  - id: build-sequence-journey
    describe: Build a multi-touch outbound journey with appropriate cadence and break-up logic.
    produces: journey
  - id: build-meeting-link
    describe: Configure the booking link reps include in outreach, with availability and meeting-type config.
    produces: scheduling_link
  - id: build-dashboard
    describe: Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution.
    produces: dashboard
---

# Cold Outbound

Target list, multi-touch sequence, tailored content, deliverability protection.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **scheduling_link** (scheduling-link): Scheduling Link produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens.
2. Build a multi-touch outbound journey with appropriate cadence and break-up logic.
3. Configure the booking link reps include in outreach, with availability and meeting-type config.
4. Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution.
