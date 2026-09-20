---
name: at-risk-vips
description: |
  Use when a user mentions "at-risk vips", or asks for related help. High-lifetime-value customers showing recency decay — Klaviyo's Needs Attention cohort. Distinct from generic churn risk.
arguments: []
intempt:
  id: at-risk-vips
  version: 1.0.0
  slashCommand: /at-risk-vips
  group: Segments
  shortDescription: 'High-lifetime-value customers showing recency decay: Klaviyo''s Needs Attention cohort. Distinct from generic churn risk.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: "Configure Segment Rule"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Open the segment authoring surface, name the segment, and apply the rule below."
      prompt: |
        Create a segment called "At-Risk VIPs".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: lifetime_value >= 1000
        - AND Attribute: days_since_last_activity is between 45 and 90
        - AND Event: order_created occurred >= 2 times (all time)
        - AND Event: order_created occurred 0 times in last 45 days

        Description: High-LTV customers who are going quiet — the Klaviyo "Needs Attention" RFM cohort. Most expensive cohort to lose; strongest ROI for personalized win-back outreach (CSM-style email from a real person, not a discount blast).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# At-Risk VIPs

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "At-Risk VIPs".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: lifetime_value >= 1000
   - AND Attribute: days_since_last_activity is between 45 and 90
   - AND Event: order_created occurred >= 2 times (all time)
   - AND Event: order_created occurred 0 times in last 45 days

   Description: High-LTV customers who are going quiet — the Klaviyo "Needs Attention" RFM cohort. Most expensive cohort to lose; strongest ROI for personalized win-back outreach (CSM-style email from a real person, not a discount blast).
   ```

## Taxonomy notes

- lifetime_value, days_since_last_activity are canonical Users attributes (numeric, no scoring constraint applies).
- order_created is canonical V2.1 event.
- The 45-90 day window is the "going quiet" zone — past the typical buying cycle for most ecom categories but before the user is fully churned. The composite of lifetime_value >= 1000 (proven high-value) plus 0 orders in last 45 days (recency decay) plus >= 2 orders ever (not a single high-AOV one-off) defines the cohort.
- Distinct from one-time-buyers-at-risk (which requires order count = 1 — a different problem) and churn-risk-users (which is plan-based for SaaS).
- The $1000 threshold is a starter; tune to your P75 customer LTV. For higher-AOV stores, use $2000-5000.
- Klaviyo's predictive churn-risk cohort is similar but uses ML-predicted churn probability. Without a predictive layer, days_since_last_activity is the best canonical proxy.
