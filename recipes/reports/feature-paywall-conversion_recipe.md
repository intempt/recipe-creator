---
name: feature-paywall-conversion
description: |
  Use when a user mentions "feature → paywall conversion", or asks for related help. Per-feature: % of free users who interact with it and subsequently view pricing AND subscribe — informs feature-gating strategy.
arguments: []
intempt:
  id: feature-paywall-conversion
  version: 1.0.0
  slashCommand: /feature-paywall-conversion
  group: Reports
  shortDescription: 'Per-feature: % of free users who interact with it and subsequently view pricing AND subscribe: informs feature-gating strategy.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Feature to Paywall Conversion".

        Series A: Event "click_on" filtered by target_id matching a feature pattern, scoped to free-plan users (users without a paid subscription_created), aggregation: Count Unique Users per target_id, label: "Free Users Who Tried Feature"
        Series B: Of the users in Series A, those who subsequently emitted a page_viewed where page_url contains "/pricing" within 30 days of the feature click, label: "Reached Paywall"
        Series C: Of the users in Series A, those who subsequently emitted subscription_created (with trial_end null — paid, non-trial) within 30 days, label: "Converted to Paid"
        Series D: Computed — Series B / Series A × 100, unit: %, label: "Feature → Paywall Rate"
        Series E: Computed — Series C / Series A × 100, unit: %, label: "Feature → Paid Rate"

        Breakdown: By target_id (the specific feature)
        Time range: Last 90 days
        Compare: Previous period (prior 90 days)
        Chart type: Scatter plot — X axis = Feature → Paywall Rate (Series D), Y axis = Feature → Paid Rate (Series E), bubble size = Series A volume (free users who tried). Each bubble is a feature.

        Annotations:
        - Quadrant labeling on the scatter:
          - High Paywall + High Paid: features that drive monetization (gate them, or use them as the upgrade pitch). Promote in upgrade prompts.
          - High Paywall + Low Paid: features that intrigue but don't close (paywall view is happening but pricing isn't compelling — pricing/positioning issue).
          - Low Paywall + High Paid: stealth-monetization features (users convert without going through pricing — already sold; no need to gate).
          - Low Paywall + Low Paid: low-monetization features (giveaways — keep in free tier, don't gate, but also don't over-invest).
        - Flag any feature with high free-tier usage AND zero conversion lift — these features are pure cost; consider deprecating or gating.
        - Highlight the top 3 features by Feature → Paid Rate (Series E) — these are the paywall-optimal features.
        - Surface the feature with the largest Free → Paywall conversion gap (Series D much higher than Series E) — pricing-perception issue specific to that feature.

        Use case: Kyle Poyar's (OpenView) most-shared Amplitude template. Tells the product team which features to gate behind the paywall vs. which to give away vs. which to deprecate. The single most-actionable monetization analysis a SaaS product can run.

        Taxonomy notes:
        - click_on.target_id is the canonical feature handle.
        - page_viewed.page_url filtered to /pricing identifies paywall views.
        - subscription_created.trial_end null distinguishes paid from trial.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Feature → Paywall Conversion

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Feature to Paywall Conversion".

   Series A: Event "click_on" filtered by target_id matching a feature pattern, scoped to free-plan users (users without a paid subscription_created), aggregation: Count Unique Users per target_id, label: "Free Users Who Tried Feature"
   Series B: Of the users in Series A, those who subsequently emitted a page_viewed where page_url contains "/pricing" within 30 days of the feature click, label: "Reached Paywall"
   Series C: Of the users in Series A, those who subsequently emitted subscription_created (with trial_end null — paid, non-trial) within 30 days, label: "Converted to Paid"
   Series D: Computed — Series B / Series A × 100, unit: %, label: "Feature → Paywall Rate"
   Series E: Computed — Series C / Series A × 100, unit: %, label: "Feature → Paid Rate"

   Breakdown: By target_id (the specific feature)
   Time range: Last 90 days
   Compare: Previous period (prior 90 days)
   Chart type: Scatter plot — X axis = Feature → Paywall Rate (Series D), Y axis = Feature → Paid Rate (Series E), bubble size = Series A volume (free users who tried). Each bubble is a feature.

   Annotations:
   - Quadrant labeling on the scatter:
     - High Paywall + High Paid: features that drive monetization (gate them, or use them as the upgrade pitch). Promote in upgrade prompts.
     - High Paywall + Low Paid: features that intrigue but don't close (paywall view is happening but pricing isn't compelling — pricing/positioning issue).
     - Low Paywall + High Paid: stealth-monetization features (users convert without going through pricing — already sold; no need to gate).
     - Low Paywall + Low Paid: low-monetization features (giveaways — keep in free tier, don't gate, but also don't over-invest).
   - Flag any feature with high free-tier usage AND zero conversion lift — these features are pure cost; consider deprecating or gating.
   - Highlight the top 3 features by Feature → Paid Rate (Series E) — these are the paywall-optimal features.
   - Surface the feature with the largest Free → Paywall conversion gap (Series D much higher than Series E) — pricing-perception issue specific to that feature.

   Use case: Kyle Poyar's (OpenView) most-shared Amplitude template. Tells the product team which features to gate behind the paywall vs. which to give away vs. which to deprecate. The single most-actionable monetization analysis a SaaS product can run.

   Taxonomy notes:
   - click_on.target_id is the canonical feature handle.
   - page_viewed.page_url filtered to /pricing identifies paywall views.
   - subscription_created.trial_end null distinguishes paid from trial.
   ```
