---
name: expansion-candidates
description: |
  Use when a user mentions "expansion candidates — near plan limit", or asks for related help. Users approaching their plan limit who are ready for an upgrade conversation.
arguments: []
intempt:
  id: expansion-candidates
  version: 1.0.0
  slashCommand: /expansion-candidates
  group: Segments
  shortDescription: "Users approaching their plan limit who are ready for an upgrade conversation."
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
        Create a segment called "Expansion Candidates".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name is not "enterprise"
        - AND Attribute: usage_pct >= 80

        Description: Users approaching plan limits — prime upgrade candidates. Trigger in-app upgrade prompt or AE outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Expansion Candidates — Near Plan Limit

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Expansion Candidates".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: plan_name is not "enterprise"
   - AND Attribute: usage_pct >= 80

   Description: Users approaching plan limits — prime upgrade candidates. Trigger in-app upgrade prompt or AE outreach.
   ```

## Taxonomy notes

- plan_name is canonical.
- usage_pct is a CUSTOM attribute. The merchant must populate it via identify() — the platform does not natively compute plan-usage percentages. Without the integration, this segment will be empty.
- The source template also referenced rate_limit_hit as an event signal. That event is NOT canonical in V2.1 taxonomy and was removed from this recipe. If the merchant emits a paywall_hit or limit_reached custom event, it can be added as an additional condition (custom event).
