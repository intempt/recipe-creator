---
name: Time To Aha Moment
description: Histogram of time from user_created to first activation goal — surfaces whether users hit aha in 5 min, 5 hours,
  or 5 days.
intempt:
  id: time-to-aha-moment
  version: 1.0.0
  slashCommand: /time-to-aha-moment
  shortDescription: Histogram of time from user_created to first activation goal — surfaces whether users hit aha in 5 min,
    5 hours, or 5 days.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
    complexity: quick
    executionMode: live
    tags:
    - insights
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-insights-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Time To Aha Moment

Histogram of time from user_created to first activation goal — surfaces whether users hit aha in 5 min, 5 hours, or 5 days.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
