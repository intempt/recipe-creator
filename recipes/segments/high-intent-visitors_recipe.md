---
name: high-intent-visitors
description: |
  Use when a user mentions "high-intent visitors", or asks for related help. Non-customers who viewed both pricing and documentation in the last 14 days — strong buying signals.
arguments: []
intempt:
  id: high-intent-visitors
  version: 1.0.0
  slashCommand: /high-intent-visitors
  group: Segments
  shortDescription: 'Non-customers who viewed both pricing and documentation in the last 14 days: strong buying signals.'
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
        Create a segment called "High-Intent Visitors".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 14 days
        - AND Event: page_viewed where page_url contains "/docs" occurred >= 1 time in last 14 days
        - AND Attribute: plan_name is empty OR plan_name = "free"

        Description: Non-customers (or free-plan users) showing strong buying signals across pricing and docs. Prioritize for sales outreach or in-app upgrade prompt.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# High-Intent Visitors

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "High-Intent Visitors".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 14 days
   - AND Event: page_viewed where page_url contains "/docs" occurred >= 1 time in last 14 days
   - AND Attribute: plan_name is empty OR plan_name = "free"

   Description: Non-customers (or free-plan users) showing strong buying signals across pricing and docs. Prioritize for sales outreach or in-app upgrade prompt.
   ```

## Taxonomy notes

- page_viewed is canonical. The filter property is page_url (not "page" — the source template used the non-canonical property name).
- plan_name is canonical (replaces "plan").
- 14-day window captures recent intent without including stale browsing history.
