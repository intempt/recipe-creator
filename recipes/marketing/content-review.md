---
name: Content Review
description: Performance pull, winners/losers diagnosis, improvement queue.
intempt:
  id: content-review
  version: 1.0.1
  slashCommand: /content-review
  shortDescription: Performance pull, winners/losers diagnosis, improvement queue.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    - design
    agent: creative-assistant
    mode:
    - all
    complexity: standard
    executionMode: oneshot
    tags:
    - content-review
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: compile-performance
    describe: Compile content performance across the review period — opens, clicks, conversions, engagement by content type.
    produces: report
  - id: generate-improvement-queue
    describe: Generate rewrite suggestions for underperforming content based on what works in winning content.
    produces: content
---

# Content Review

Performance pull, winners/losers diagnosis, improvement queue.

## Outputs

- **report** (report): Report produced by this recipe.
- **content** (content): Content produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Compile content performance across the review period — opens, clicks, conversions, engagement by content type.
2. Generate rewrite suggestions for underperforming content based on what works in winning content.
