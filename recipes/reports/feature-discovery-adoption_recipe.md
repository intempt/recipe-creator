---
name: feature-discovery-adoption
description: |
  Use when a user mentions "feature discovery → adoption", or asks for related help. 4-step funnel from first feature exposure to repeated use, using canonical click_on patterns.
arguments: []
intempt:
  id: feature-discovery-adoption
  version: 1.0.0
  slashCommand: /feature-discovery-adoption
  group: Reports
  shortDescription: "4-step funnel from first feature exposure to repeated use, using canonical click_on patterns."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Feature Discovery to Adoption".

        Steps:
        1. Event "page_viewed" where page_url contains the feature path — "Discovered Feature" (first exposure)
           (alternative: click_on where target_id matches a feature-tour or tooltip element)
        2. Event "click_on" where target_id matches the feature interaction handle — "Tried Feature" (first use)
        3. Event "click_on" with same target_id as Step 2, count >= 3 by the same user within 21 days — "Used 3+ Times"
        4. Event "click_on" with same target_id, frequency: at least 3 distinct days of use in the last 5 days — "Habitual User"

        Conversion window: 21 days
        Breakdown: By target_id (feature handle)
        Compare: Previous period (prior 21 days)

        For each feature, also surface:
        - Discovery → Habitual conversion rate (Step 4 / Step 1)
        - Median time-to-habitual (days from discovery to habitual)

        Annotations:
        - Flag features with discovery > 1000 users AND habitual conversion < 5% — high-discovery, low-stickiness; investigate UX.
        - Flag features where discovery → trial conversion < 20% — discovery moment isn't compelling.
        - Highlight features with discovery → habitual conversion > 25% — surface candidates for promotion.

        Surface the top 3 features by absolute habitual-user count and the top 3 by habitual-conversion rate.

        Taxonomy notes:
        - "feature_discovered" and "feature_habitual" as standalone events do not exist. Feature interactions are tracked via click_on with stable target_id values per feature.
        - Step 4 ("Habitual User") requires Lovable to compute the "3 of last 5 days" rule from click_on event timestamps grouped by user.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Feature Discovery → Adoption

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Feature Discovery to Adoption".

   Steps:
   1. Event "page_viewed" where page_url contains the feature path — "Discovered Feature" (first exposure)
      (alternative: click_on where target_id matches a feature-tour or tooltip element)
   2. Event "click_on" where target_id matches the feature interaction handle — "Tried Feature" (first use)
   3. Event "click_on" with same target_id as Step 2, count >= 3 by the same user within 21 days — "Used 3+ Times"
   4. Event "click_on" with same target_id, frequency: at least 3 distinct days of use in the last 5 days — "Habitual User"

   Conversion window: 21 days
   Breakdown: By target_id (feature handle)
   Compare: Previous period (prior 21 days)

   For each feature, also surface:
   - Discovery → Habitual conversion rate (Step 4 / Step 1)
   - Median time-to-habitual (days from discovery to habitual)

   Annotations:
   - Flag features with discovery > 1000 users AND habitual conversion < 5% — high-discovery, low-stickiness; investigate UX.
   - Flag features where discovery → trial conversion < 20% — discovery moment isn't compelling.
   - Highlight features with discovery → habitual conversion > 25% — surface candidates for promotion.

   Surface the top 3 features by absolute habitual-user count and the top 3 by habitual-conversion rate.

   Taxonomy notes:
   - "feature_discovered" and "feature_habitual" as standalone events do not exist. Feature interactions are tracked via click_on with stable target_id values per feature.
   - Step 4 ("Habitual User") requires Lovable to compute the "3 of last 5 days" rule from click_on event timestamps grouped by user.
   ```
