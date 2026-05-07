---
name: Sales Coaching
description: Scorecards, talk-listen tracking, rep benchmarking, and low-score review queue.
intempt:
  id: sales-coaching
  version: 1.0.0
  slashCommand: /sales-coaching
  shortDescription: Scorecards, talk-listen tracking, rep benchmarking, and low-score review queue.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    - analytics
    agent: meeting-notetaker
    mode:
    - b2b
    complexity: standard
    executionMode: live
    tags:
    - sales-coaching
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: build-coaching-scorecard
    describe: Build a coaching scorecard tracking talk-listen ratio, question frequency, discovery depth, and next-step clarity
      per call.
    produces: report
  - id: build-coaching-dashboard
    describe: Compose a dashboard benchmarking reps and surfacing improvement areas.
    produces: dashboard
  - id: build-review-workflow
    describe: Create a workflow flagging low-scoring calls for manager review and coaching follow-up.
    produces: workflow
---

# Sales Coaching

Scorecards, talk-listen tracking, rep benchmarking, and low-score review queue.

## Outputs

- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Build a coaching scorecard tracking talk-listen ratio, question frequency, discovery depth, and next-step clarity per call.
2. Compose a dashboard benchmarking reps and surfacing improvement areas.
3. Create a workflow flagging low-scoring calls for manager review and coaching follow-up.
