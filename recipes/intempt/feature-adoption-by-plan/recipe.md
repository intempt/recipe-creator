---
frontmatter_id: feature-adoption-by-plan
slash_command: /feature-adoption-by-plan
description: Shows feature adoption across plan tiers using a breakdown of active users.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows which features each plan tier adopts, as a heatmap of active-user adoption rates, with trends and flags for
    upsell, deprecation and load-bearing features.
  parameters:
  - name: time_window
    type: duration
    label: Analysis window
    default: 30 d
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period
    default: 30 d
    required: false
  - name: trend_weeks
    type: number
    label: Trend lookback (weeks)
    default: 12
    required: false
  - name: high_adoption_threshold
    type: number
    label: Load-bearing adoption threshold (%)
    default: 40
    required: false
  - name: upgrade_ratio_threshold
    type: number
    label: Higher-to-lower tier adoption ratio
    default: 2
    required: false
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a page element that identifies a product feature
    properties:
    - name: target_id
      type: text
      meaning: Stable identifier of the feature surface clicked
      optional: false
    - name: target_text
      type: text
      meaning: Human-readable label of the clicked element
      optional: true
    - name: target_class
      type: text
      meaning: CSS class of the clicked element
      optional: true
    - name: target_tag
      type: text
      meaning: HTML tag of the clicked element
      optional: true
    - name: hierarchy
      type: text
      meaning: DOM hierarchy of the clicked element
      optional: true
    - name: path
      type: text
      meaning: Page path where the click happened
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription to a plan
    properties:
    - name: Plan
      type: text
      meaning: The plan tier the customer subscribed to
      optional: false
  - slot: active_users
    kind: segment
    meaning: Users active in the analysis window
  steps:
  - id: s1
    builds: report
    uses:
    - feature_click_event
    - subscription_started_event
    - active_users
    - time_window
    - comparison_window
    - high_adoption_threshold
    - upgrade_ratio_threshold
    instruction: 'Create an Insights report titled "Feature Adoption by Plan". Series A: count unique users of {feature_click_event}
      filtered by {feature_click_event.target_id}. Series B: computed as Series A divided by total {active_users} in the same
      plan tier, times 100, unit %, labeled "Adoption Rate". Resolve plan tier from each user''s most recent {subscription_started_event.Plan}.
      Break down by {feature_click_event.target_id} on the X axis and by plan tier on the Y axis. Time range: {time_window}.
      Compare against the previous period of equal length, {comparison_window}. Render as a heatmap with features on the vertical
      axis and plan tiers on the horizontal axis, cell value = adoption rate, color intensity scaled.'
---

# Feature adoption by plan

Slash command: /feature-adoption-by-plan

## Step 1: Map feature use to plan tier

Create an Insights report called "Feature Adoption by Plan".
Series A: Event "Click on" filtered by target_id (a stable identifier representing a feature surface: e.g. /feature/<feature-slug>), aggregation: Count Unique Users
Series B: Computed: Series A / total active users in the same plan tier × 100, unit: %, label: "Adoption Rate"
Breakdown: By target_id (the feature) on the X axis, secondary breakdown by Plan (resolved from the user's most-recent Subscription started.Plan) on the Y axis
Time range: Last 30 days
Compare: Previous period (prior 30 days)
Chart type: Heatmap (target_id / feature on Y axis, plan tier on X axis), cell value = adoption rate %, color intensity scaled
Also include a parallel view: per-feature adoption-rate trend over the last 12 weeks, broken down by plan tier: to show whether adoption is accelerating, flat, or declining per feature.
Annotations:
- Flag features with high adoption in higher tiers but low adoption in lower tiers (candidates to promote down-tier OR signs of plan-feature mismatch).
- Flag features with declining adoption in any tier (deprecation candidate or UX issue).
- Highlight features used by >40% of paying users: these are the load-bearing features whose performance and reliability matter most.
- Highlight features where higher-tier users adopt at >2× the rate of lower-tier users (the best upgrade-pitch features).
Taxonomy notes:
- Click on carries target_id, target_text, target_class, target_tag, hierarchy, path. The product team identifies features by stable target_id values.
- "feature_name" is not a canonical property; target_id (or target_text for human labels) is the canonical handle.
- Plan lives on Subscription started; this requires joining to the user's active subscription.
