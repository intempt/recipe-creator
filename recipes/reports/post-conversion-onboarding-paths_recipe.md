---
name: post-conversion-onboarding-paths
description: |
  Use when a user mentions "post-conversion onboarding paths", or asks for related help. Forward path from first paid event (subscription or order): what new paying customers do in their first session as customers.
arguments: []
intempt:
  id: post-conversion-onboarding-paths
  version: 1.0.0
  slashCommand: /post-conversion-onboarding-paths
  group: Reports
  title: "Paths after first payment"
  shortDescription: "Shows what new paying customers do in their first week, and how many pay and then vanish."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas, ecommerce]
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
      title: "Watch the first week after paying"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "The 7 steps after a first paid subscription or first order, inside a 7 day window over the last 60 days, split by plan or first order category, with the share taking a second meaningful action and the share going silent. Flags silence above 25%."
      prompt: |
        Create a Path report called "Post-Conversion Onboarding Paths".

        Anchor event:
          - For saas mode: Subscription started where the trial end is empty (paid signup, not trial)
          - For ecommerce mode: Placed order where this is the user's FIRST order (first Placed order per customer)

        Direction: forward
        Depth: 7 steps forward
        Window: 7 days after the conversion event
        Loop compression: on
        Time range: Last 60 days of conversions
        Breakdown: By Plan (saas) or first-order product category derived from the order's items (ecommerce)

        Surface:
        - The top 10 most-common 7-step paths emerging from the conversion event
        - The % of new paying customers who took a "second value action" within the window (defined per mode: saas = Completed a journey goal for activation; ecommerce = View page on a non-purchase page indicating ongoing engagement)
        - The % of new paying customers who emit zero further activity in the window (they paid and disappeared: potential immediate-churn signal)

        Annotations:
        - Flag if >25% of new paying customers emit zero activity in the 7-day post-conversion window: the post-purchase moment is being missed; consider triggering an onboarding journey on the conversion event.
        - Highlight the dominant first-action after conversion: in healthy products, this is a meaningful workflow event (saas: "configure setting" or "invite teammate"; ecommerce: "track order" or "browse another product"). If the dominant first-action is "log out" or "Session end," the post-purchase moment is failing.
        - Surface paths that lead to a SECOND conversion event (saas: Subscription updated for upgrade, ecommerce: second Placed order): these are the natural cross-sell / expansion patterns.

        Use case: most products focus heavily on pre-conversion onboarding and ignore the moment immediately after payment. Yet the post-purchase moment is when newly-paying customers are most engaged and most receptive to expansion. This recipe surfaces what's actually happening in that golden hour.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paths after first payment

Shows what new paying customers do in their first week, and how many pay and then vanish.

## What it does

1. **Watch the first week after paying** (`build_paths_report`)

   The 7 steps after a first paid subscription or first order, inside a 7 day window over the last 60 days, split by plan or first order category, with the share taking a second meaningful action and the share going silent. Flags silence above 25%.

## What you end up with

- **report** (report): Report produced by this recipe.
