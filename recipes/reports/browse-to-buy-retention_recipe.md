---
name: browse-to-buy-retention
description: |
  Use when a user mentions "browse-to-buy retention", or asks for related help. First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.
arguments: []
intempt:
  id: browse-to-buy-retention
  version: 1.0.0
  slashCommand: /browse-to-buy-retention
  group: Reports
  shortDescription: "First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_retention_report
  procedure:
    - step: 1
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Retention report called "Browse to Buy Retention".

        Anchor event: session_start (each user's first session_start)
        Return event: order_created
        Cohort granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By Users.utm_source (top 6 sources)
        Compare: Previous period (prior 12 weeks of cohorts)
        Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns

        Annotations:
        - Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
        - Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
        - Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
        - Highlight the source with the highest W12 conversion (best overall, even if slower).

        Surface which sources produce "fast converters" vs "slow converters."

        Taxonomy notes:
        - session_start and order_created are canonical. Users.utm_source is canonical.
        - "first session" per-user is determined by the earliest session_start for that customer_id.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Browse-to-Buy Retention

## Procedure

1. **Build Retention Report** [`build_retention_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Retention report called "Browse to Buy Retention".

   Anchor event: session_start (each user's first session_start)
   Return event: order_created
   Cohort granularity: Weekly
   Time range: Last 12 weeks
   Breakdown: By Users.utm_source (top 6 sources)
   Compare: Previous period (prior 12 weeks of cohorts)
   Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns

   Annotations:
   - Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
   - Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
   - Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
   - Highlight the source with the highest W12 conversion (best overall, even if slower).

   Surface which sources produce "fast converters" vs "slow converters."

   Taxonomy notes:
   - session_start and order_created are canonical. Users.utm_source is canonical.
   - "first session" per-user is determined by the earliest session_start for that customer_id.
   ```
