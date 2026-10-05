---
name: trial-expiring-soon
description: |
  Use when a user mentions "trial expiring soon", or asks for related help. Trial users approaching expiry who haven't converted to paid.
arguments: []
intempt:
  id: trial-expiring-soon
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Creates a Users segment named 'Trial Expiring Soon' for plan_name=trial with end_date within 7 days and no subscription_created in the last 14 days."
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
        Create a segment called "Trial Expiring Soon".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name = "trial"
        - AND Attribute: end_date is within next 7 days
        - AND Event: subscription_created has not occurred in last 14 days

        Description: Trial users approaching expiry without paid conversion. Trigger a final-push email or in-app upgrade prompt.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Trial Expiring Soon

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Trial Expiring Soon".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: plan_name = "trial"
   - AND Attribute: end_date is within next 7 days
   - AND Event: subscription_created has not occurred in last 14 days

   Description: Trial users approaching expiry without paid conversion. Trigger a final-push email or in-app upgrade prompt.
   ```

## Taxonomy notes

- plan_name is canonical.
- end_date is canonical Users attribute (subscription end_date — populated when the user is on a trial subscription with a defined end date). Source template referenced "trial_end_date" which is not canonical; end_date is the equivalent canonical property.
- subscription_created is canonical V2.1 event.
- For workspaces that don't model trials as subscriptions with end_date, this rule needs the merchant to populate a custom attribute via identify(). The recipe above assumes the canonical subscription model is in use.
