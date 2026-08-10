---
name: high-intent-anonymous-visitors
description: |
  Use when a user mentions "high-intent anonymous visitors", or asks for related help. Unidentified visitors with strong engagement signals — ad retargeting cohort.
arguments: []
intempt:
  id: high-intent-anonymous-visitors
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Unidentified visitors with strong engagement signals — ad retargeting cohort."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, b2b, ecommerce]
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
        Create a segment called "High-Intent Anonymous Visitors".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: total_events >= 5
        - AND Attribute: email is empty
        - AND Event: page_viewed occurred >= 3 times in last 7 days
        - AND Event: session_start occurred >= 2 times in last 7 days

        Description: Unidentified visitors with multiple sessions and substantial activity. Ad-retargeting cohort — also a candidate for an email-capture popup or content offer.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# High-Intent Anonymous Visitors

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "High-Intent Anonymous Visitors".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: total_events >= 5
   - AND Attribute: email is empty
   - AND Event: page_viewed occurred >= 3 times in last 7 days
   - AND Event: session_start occurred >= 2 times in last 7 days

   Description: Unidentified visitors with multiple sessions and substantial activity. Ad-retargeting cohort — also a candidate for an email-capture popup or content offer.
   ```

## Taxonomy notes

- total_events is canonical Users attribute.
- email is canonical Users attribute; "is empty" filter captures unidentified users.
- page_viewed and session_start are canonical events.
- Anonymous-but-engaged is the sweet spot for retargeting spend, so the natural next move is a paid-audience sync. There is no Meta or Google Ads connector today, so the segment exports rather than syncs. An earlier version of this note pointed at an "add-users-to-facebook-custom-audiences" workflow as though it existed; it never has, and naming an asset a customer cannot find is the same failure as naming a connector we do not have.
