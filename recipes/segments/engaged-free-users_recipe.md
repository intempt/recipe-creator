---
name: engaged-free-users
description: |
  Use when a user mentions "engaged free users", or asks for related help. Free-plan users with high engagement — prime upgrade-targeting cohort.
arguments: []
intempt:
  id: engaged-free-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Free-plan users with high engagement — prime upgrade-targeting cohort."
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
        Create a segment called "Engaged Free Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name = "free"
        - AND Attribute: engagement_score = "High"
        - AND Attribute: days_since_last_activity <= 7
        - AND Event: session_start occurred >= 5 times in last 14 days

        Description: Free users showing strong engagement and recent activity. Prime cohort for upgrade prompts, premium-feature trials, and account-expansion outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Engaged Free Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Engaged Free Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: plan_name = "free"
   - AND Attribute: engagement_score = "High"
   - AND Attribute: days_since_last_activity <= 7
   - AND Event: session_start occurred >= 5 times in last 14 days

   Description: Free users showing strong engagement and recent activity. Prime cohort for upgrade prompts, premium-feature trials, and account-expansion outreach.
   ```

## Taxonomy notes

- plan_name is canonical.
- engagement_score uses canonical enum (Low | Medium | High) per scoring constraint.
- days_since_last_activity is canonical numeric.
- session_start is canonical event.
- This segment is the foundation for product-qualified-lead (PQL) workflows — these are users actively getting value but not paying.
