---
name: churn-risk-users
description: |
  Use when a user mentions "churn risk users", or asks for related help. Previously active paid users who have gone silent in the last month.
arguments: []
intempt:
  id: churn-risk-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Creates a Users segment named 'Churn Risk Users' for paid users with at least 5 session_start events 60-90 days ago and 0 in the last 30 days."
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
        Create a segment called "Churn Risk Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: session_start occurred >= 5 times between 60 and 90 days ago
        - AND Event: session_start occurred 0 times in last 30 days
        - AND Attribute: plan_name is not "free"

        Description: Previously active paid users who have gone silent. Trigger CSM outreach or save-offer journey before they churn.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Churn Risk Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Churn Risk Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: session_start occurred >= 5 times between 60 and 90 days ago
   - AND Event: session_start occurred 0 times in last 30 days
   - AND Attribute: plan_name is not "free"

   Description: Previously active paid users who have gone silent. Trigger CSM outreach or save-offer journey before they churn.
   ```

## Taxonomy notes

- session_start is canonical.
- plan_name is canonical (replaces source template's "plan" which is not the canonical attribute name).
- The "between 60 and 90 days ago" + "0 times in last 30 days" pattern combines two windowed rules to capture the silent-after-active behavior.
