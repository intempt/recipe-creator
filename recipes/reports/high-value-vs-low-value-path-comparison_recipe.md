---
name: high-value-vs-low-value-path-comparison
description: |
  Use when a user mentions "high-value vs low-value path comparison", or asks for related help. Two Path reports side-by-side: paths taken by users who placed >$X orders vs <$X or non-converters.
arguments: []
intempt:
  id: high-value-vs-low-value-path-comparison
  version: 1.0.0
  slashCommand: /high-value-vs-low-value-path-comparison
  group: Reports
  shortDescription: "A single report with two side-by-side Path analyses: paths for users with >$X orders versus paths for <$X/non-converters."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [path]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_paths_report
  procedure:
    - step: 1
      title: "Build Path Report"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Path report called "High-Value vs Low-Value Path Comparison".

        This recipe runs two Path reports in parallel and surfaces them side-by-side.

        Configuration:
        - Threshold for "high value": default $100 (configurable; or use the 75th-percentile order_created.total_price)
        - Threshold for "low value": default <$50 OR no order placed in the window (configurable)

        Path A — High-value paths:
        - Anchor event: session_start (user's first session in the window)
        - End event: order_created where total_price >= high-value threshold
        - Direction: forward
        - Depth: 7 steps
        - Window: 7 days
        - Loop compression: on

        Path B — Low-value paths:
        - Anchor event: session_start
        - End event: order_created where total_price < low-value threshold OR session_end without any order_created
        - Direction: forward
        - Depth: 7 steps
        - Window: 7 days
        - Loop compression: on

        Time range: Last 60 days

        Render the two Path reports side-by-side and compute a "lift" view: events that appear in Path A's top 10 paths but NOT in Path B's top 10, and vice versa.

        Annotations:
        - Surface the top 5 events that appear disproportionately in high-value paths (the "high-value-buyer signals").
        - Surface the top 5 events that appear in low-value paths (the "low-value-buyer signals" — typically discount_applied events, single product detail page_viewed without category browsing, etc.).
        - Surface the median path length (number of steps) for each segment — high-value buyers typically take longer, more deliberate paths.

        Use case: identify behaviors that predict high-value purchase intent in the first session, so you can trigger personalization for users showing those signals.

        Taxonomy notes:
        - session_start, order_created, session_end are all canonical. order_created.total_price is the value used for the threshold filter.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# High-Value vs Low-Value Path Comparison

## Procedure

1. **Build Path Report** [`build_paths_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Path report called "High-Value vs Low-Value Path Comparison".

   This recipe runs two Path reports in parallel and surfaces them side-by-side.

   Configuration:
   - Threshold for "high value": default $100 (configurable; or use the 75th-percentile order_created.total_price)
   - Threshold for "low value": default <$50 OR no order placed in the window (configurable)

   Path A — High-value paths:
   - Anchor event: session_start (user's first session in the window)
   - End event: order_created where total_price >= high-value threshold
   - Direction: forward
   - Depth: 7 steps
   - Window: 7 days
   - Loop compression: on

   Path B — Low-value paths:
   - Anchor event: session_start
   - End event: order_created where total_price < low-value threshold OR session_end without any order_created
   - Direction: forward
   - Depth: 7 steps
   - Window: 7 days
   - Loop compression: on

   Time range: Last 60 days

   Render the two Path reports side-by-side and compute a "lift" view: events that appear in Path A's top 10 paths but NOT in Path B's top 10, and vice versa.

   Annotations:
   - Surface the top 5 events that appear disproportionately in high-value paths (the "high-value-buyer signals").
   - Surface the top 5 events that appear in low-value paths (the "low-value-buyer signals" — typically discount_applied events, single product detail page_viewed without category browsing, etc.).
   - Surface the median path length (number of steps) for each segment — high-value buyers typically take longer, more deliberate paths.

   Use case: identify behaviors that predict high-value purchase intent in the first session, so you can trigger personalization for users showing those signals.

   Taxonomy notes:
   - session_start, order_created, session_end are all canonical. order_created.total_price is the value used for the threshold filter.
   ```
