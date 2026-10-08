---
description: Shows feature adoption across plan tiers using a breakdown of active users.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Feature adoption by plan

Slash command: /feature-adoption-by-plan

## Step 1: Map feature use to plan tier

Create an Insights report called "Feature Adoption by Plan".
Series A: Event "click_on" filtered by target_id (a stable identifier representing a feature surface: e.g. /feature/<feature-slug>), aggregation: Count Unique Users
Series B: Computed: Series A / total active users in the same plan tier × 100, unit: %, label: "Adoption Rate"
Breakdown: By target_id (the feature) on the X axis, secondary breakdown by plan_name (resolved from the user's most-recent subscription_created.plan_name) on the Y axis
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
- click_on carries target_id, target_text, target_class, target_tag, hierarchy, path. The product team identifies features by stable target_id values.
- "feature_name" is not a canonical property; target_id (or target_text for human labels) is the canonical handle.
- plan_name lives on subscription_created; this requires joining to the user's active subscription.
