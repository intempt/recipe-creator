---
frontmatter_id: analytics-foundation
slash_command: /analytics-foundation
description: 'Set up core analytics from your events: Insights, Funnels, and Retention reports, plus an executive dashboard for headline numbers.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sets up core analytics from your tracked events, delivering Insights, Funnels, Retention and Paths reports plus
    an executive dashboard showing headline metrics with comparisons and trends.
  parameters: []
  requirements:
  - slot: product_events
    kind: event
    meaning: A customer performed a tracked product action that feeds analytics reports
  steps:
  - id: s1
    builds: report
    uses:
    - product_events
    instruction: Build the core report set containing an Insights report for key metrics, a Funnels report for conversion
      paths, a Retention report for cohort analysis, and a Paths report for user flows, all based on {product_events}.
  - id: s2
    builds: dashboard
    uses:
    - s1
    instruction: Compose an executive dashboard surfacing headline metrics with comparisons and trends, using the reports
      from "Build the core report set".
---

# Analytics foundation

Slash command: /analytics-foundation

## Step 1: Build the core report set

Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows).

## Step 2: Compose the exec dashboard

Compose an executive dashboard surfacing headline metrics with comparisons and trends. Use the result of "Build the core report set".
