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
  title: "High value versus low value paths"
  shortDescription: "Puts the journeys of big spenders next to the journeys of small spenders and non buyers, and names the steps that only show up on the profitable side."
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
      title: "Contrast big and small basket paths"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "Two 7 step journeys from a first session inside a 7 day window over the last 60 days: one ending in an order above the high value threshold (100 dollars by default), one ending below it or with no order at all. Surfaces the events unique to each side."
      prompt: |
        Create a Path report called "High-Value vs Low-Value Path Comparison".

        This recipe runs two Path reports in parallel and surfaces them side-by-side.

        Configuration:
        - Threshold for "high value": default $100 (configurable; or use the 75th-percentile order total)
        - Threshold for "low value": default <$50 OR no order placed in the window (configurable)

        Path A: High-value paths:
        - Anchor event: Session start (user's first session in the window)
        - End event: Placed order where the order total >= high-value threshold
        - Direction: forward
        - Depth: 7 steps
        - Window: 7 days
        - Loop compression: on

        Path B: Low-value paths:
        - Anchor event: Session start
        - End event: Placed order where the order total < low-value threshold OR Session end without any order placed
        - Direction: forward
        - Depth: 7 steps
        - Window: 7 days
        - Loop compression: on

        Time range: Last 60 days

        Render the two Path reports side-by-side and compute a "lift" view: events that appear in Path A's top 10 paths but NOT in Path B's top 10, and vice versa.

        Annotations:
        - Surface the top 5 events that appear disproportionately in high-value paths (the "high-value-buyer signals").
        - Surface the top 5 events that appear in low-value paths (the "low-value-buyer signals": typically discount-applied events, a single product-detail page view without category browsing, etc.).
        - Surface the median path length (number of steps) for each segment: high-value buyers typically take longer, more deliberate paths.

        Use case: identify behaviors that predict high-value purchase intent in the first session, so you can trigger personalization for users showing those signals.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# High value versus low value paths

Puts the journeys of big spenders next to the journeys of small spenders and non buyers, and names the steps that only show up on the profitable side.

## What it does

1. **Contrast big and small basket paths** (`build_paths_report`)

   Two 7 step journeys from a first session inside a 7 day window over the last 60 days: one ending in an order above the high value threshold (100 dollars by default), one ending below it or with no order at all. Surfaces the events unique to each side.

## What you end up with

- **report** (report): Report produced by this recipe.
