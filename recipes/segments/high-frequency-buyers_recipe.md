---
name: high-frequency-buyers
description: |
  Use when a user mentions "high-frequency buyers", or asks for related help. Customers who purchase 4+ times per quarter — most loyal cohort.
arguments: []
intempt:
  id: high-frequency-buyers
  version: 1.0.0
  slashCommand: /high-frequency-buyers
  group: Segments
  shortDescription: 'Customers who purchase 4+ times per quarter: most loyal cohort.'
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
        Create a segment called "High-Frequency Buyers".

        Object: Users

        Rules:
        - Event: order_created occurred >= 4 times in last 90 days

        Description: High-frequency buyers — the most loyal cohort. Priority for loyalty program enrollment, early access, and brand-ambassador outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# High-Frequency Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "High-Frequency Buyers".

   Object: Users

   Rules:
   - Event: order_created occurred >= 4 times in last 90 days

   Description: High-frequency buyers — the most loyal cohort. Priority for loyalty program enrollment, early access, and brand-ambassador outreach.
   ```

## Taxonomy notes

- order_created is canonical.
- This is the cleanest segment in the bundle — a single rule on a single canonical event. Add Attribute: lifetime_value >= <threshold> as an optional refinement to filter out high-frequency low-value buyers (e.g., subscribers using credits).
