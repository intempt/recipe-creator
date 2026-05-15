---
name: post-conversion-onboarding-paths
description: |
  Use when a user mentions "post-conversion onboarding paths", or asks for related help. Forward path from first paid event (subscription or order) — what new paying customers do in their first session as customers.
arguments: []
intempt:
  id: post-conversion-onboarding-paths
  version: 1.0.0
  slashCommand: /post-conversion-onboarding-paths
  group: Reports
  shortDescription: "Forward path from first paid event (subscription or order) — what new paying customers do in their first session as customers."
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
      title: "Build Path Report"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Path report called "Post-Conversion Onboarding Paths".

        Anchor event:
          - For saas mode: subscription_created where trial_end is null (paid signup, not trial)
          - For ecommerce mode: order_created where this is the user's FIRST order (first order_created per customer_id)

        Direction: forward
        Depth: 7 steps forward
        Window: 7 days after the conversion event
        Loop compression: on
        Time range: Last 60 days of conversions
        Breakdown: By plan_name (saas) or first-order product category derived from order_created.items (ecommerce)

        Surface:
        - The top 10 most-common 7-step paths emerging from the conversion event
        - The % of new paying customers who took a "second value action" within the window (defined per mode: saas = goal_completed_in_journey for activation; ecommerce = page_viewed on a non-purchase page indicating ongoing engagement)
        - The % of new paying customers who emit zero further activity in the window (they paid and disappeared — potential immediate-churn signal)

        Annotations:
        - Flag if >25% of new paying customers emit zero activity in the 7-day post-conversion window — the post-purchase moment is being missed; consider triggering an onboarding journey on the conversion event.
        - Highlight the dominant first-action after conversion: in healthy products, this is a meaningful workflow event (saas: "configure setting" or "invite teammate"; ecommerce: "track order" or "browse another product"). If the dominant first-action is "log out" or "session_end," the post-purchase moment is failing.
        - Surface paths that lead to a SECOND conversion event (saas: subscription_updated for upgrade, ecommerce: second order_created) — these are the natural cross-sell / expansion patterns.

        Use case: most products focus heavily on pre-conversion onboarding and ignore the moment immediately after payment. Yet the post-purchase moment is when newly-paying customers are most engaged and most receptive to expansion. This recipe surfaces what's actually happening in that golden hour.

        Taxonomy notes:
        - subscription_created.trial_end null vs not-null distinguishes paid from trial starts.
        - "First order_created" per user is computed as the earliest order_created event for that customer_id.
        - session_end is the canonical disengagement marker.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Post-Conversion Onboarding Paths

## Procedure

1. **Build Path Report** [`build_paths_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Path report called "Post-Conversion Onboarding Paths".

   Anchor event:
     - For saas mode: subscription_created where trial_end is null (paid signup, not trial)
     - For ecommerce mode: order_created where this is the user's FIRST order (first order_created per customer_id)

   Direction: forward
   Depth: 7 steps forward
   Window: 7 days after the conversion event
   Loop compression: on
   Time range: Last 60 days of conversions
   Breakdown: By plan_name (saas) or first-order product category derived from order_created.items (ecommerce)

   Surface:
   - The top 10 most-common 7-step paths emerging from the conversion event
   - The % of new paying customers who took a "second value action" within the window (defined per mode: saas = goal_completed_in_journey for activation; ecommerce = page_viewed on a non-purchase page indicating ongoing engagement)
   - The % of new paying customers who emit zero further activity in the window (they paid and disappeared — potential immediate-churn signal)

   Annotations:
   - Flag if >25% of new paying customers emit zero activity in the 7-day post-conversion window — the post-purchase moment is being missed; consider triggering an onboarding journey on the conversion event.
   - Highlight the dominant first-action after conversion: in healthy products, this is a meaningful workflow event (saas: "configure setting" or "invite teammate"; ecommerce: "track order" or "browse another product"). If the dominant first-action is "log out" or "session_end," the post-purchase moment is failing.
   - Surface paths that lead to a SECOND conversion event (saas: subscription_updated for upgrade, ecommerce: second order_created) — these are the natural cross-sell / expansion patterns.

   Use case: most products focus heavily on pre-conversion onboarding and ignore the moment immediately after payment. Yet the post-purchase moment is when newly-paying customers are most engaged and most receptive to expansion. This recipe surfaces what's actually happening in that golden hour.

   Taxonomy notes:
   - subscription_created.trial_end null vs not-null distinguishes paid from trial starts.
   - "First order_created" per user is computed as the earliest order_created event for that customer_id.
   - session_end is the canonical disengagement marker.
   ```
