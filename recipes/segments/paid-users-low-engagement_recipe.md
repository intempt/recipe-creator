---
name: paid-users-low-engagement
description: |
  Use when a user mentions "paid users — low engagement", or asks for related help. Paying customers showing early disengagement signals. Engagement bucketed enum.
arguments: []
intempt:
  id: paid-users-low-engagement
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Creates a segment filtering paid users with low activity and engagement scores."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
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
        Create a segment called "Paid Users — Low Engagement".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name is not in ["free", "trial"]
        - AND Attribute: days_since_last_activity is between 7 and 21
        - AND Attribute: engagement_score = "Low"

        Description: Paid customers showing early disengagement before they become full churn risk. Trigger CSM check-in or feature-rediscovery campaign.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Paid Users — Low Engagement

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Paid Users — Low Engagement".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: plan_name is not in ["free", "trial"]
   - AND Attribute: days_since_last_activity is between 7 and 21
   - AND Attribute: engagement_score = "Low"

   Description: Paid customers showing early disengagement before they become full churn risk. Trigger CSM check-in or feature-rediscovery campaign.
   ```

## Taxonomy notes

- plan_name is canonical.
- days_since_last_activity is canonical Users attribute (numeric, no scoring constraint applies).
- engagement_score uses canonical enum (replaces source template's numeric "<= 30" with the enum equivalent "Low" per scoring constraint).
- The 7-to-21-day window is the early-warning zone — before they hit the >30-day silent-user threshold that defines actual churn risk.
