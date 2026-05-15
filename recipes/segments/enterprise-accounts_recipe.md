---
name: enterprise-accounts
description: |
  Use when a user mentions "enterprise accounts (1000+ employees)", or asks for related help. Large companies (1000+ employees) — AE white-glove sales-motion routing.
arguments: []
intempt:
  id: enterprise-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Large companies (1000+ employees) — AE white-glove sales-motion routing."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
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
        Create a segment called "Enterprise Accounts".

        Object: Accounts

        Rules:
        - Attribute: employees >= 1000

        Description: Companies with 1000+ employees. Foundation for enterprise sales-motion routing — these accounts get AE white-glove engagement: dedicated account plans, executive-sponsor outreach, and quarterly business reviews. Universal B2B routing pattern.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Enterprise Accounts (1000+ Employees)

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Enterprise Accounts".

   Object: Accounts

   Rules:
   - Attribute: employees >= 1000

   Description: Companies with 1000+ employees. Foundation for enterprise sales-motion routing — these accounts get AE white-glove engagement: dedicated account plans, executive-sponsor outreach, and quarterly business reviews. Universal B2B routing pattern.
   ```

## Taxonomy notes

- employees is canonical Accounts attribute.
- The 1000-employee threshold is the standard enterprise definition (Demandbase, Gartner, Salesforce all use this benchmark). Adjust for your market — some merchants raise to 5000+ for "strategic enterprise" segmentation.
- Pair with industry filter (industry IN ["Banking", "Insurance", "Pharmaceuticals"]) for vertical-enterprise segments where deal sizes warrant specialized AE focus.
- For tier-1 strategic accounts (top 10-20 named), build a separate segment using account_id IN [...] explicit list — that pattern doesn't generalize as a recipe but layers on top of this base.
