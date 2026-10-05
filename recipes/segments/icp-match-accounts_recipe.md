---
name: icp-match-accounts
description: |
  Use when a user mentions "icp match accounts", or asks for related help. Accounts matching ideal customer profile by company size, industry, and geography.
arguments: []
intempt:
  id: icp-match-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a single Accounts segment named 'ICP Match Accounts' where employees is 50-500 AND industry is SaaS/Technology/Financial Services AND country is US/UK/CA/AU."
  availability: available
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
        Create a segment called "ICP Match Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees is between 50 and 500
        - AND Attribute: industry is one of ["SaaS", "Technology", "Financial Services"]
        - AND Attribute: country is one of ["US", "UK", "CA", "AU"]

        Description: Accounts matching the ideal customer profile by size, industry, and geography. Foundation segment for ABM targeting.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# ICP Match Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "ICP Match Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: employees is between 50 and 500
   - AND Attribute: industry is one of ["SaaS", "Technology", "Financial Services"]
   - AND Attribute: country is one of ["US", "UK", "CA", "AU"]

   Description: Accounts matching the ideal customer profile by size, industry, and geography. Foundation segment for ABM targeting.
   ```

## Taxonomy notes

- employees is the canonical Accounts attribute (replaces source template's "employee_count" — the canonical property name is "employees").
- industry is canonical on Accounts.
- country is canonical on Accounts (also canonical on Users, but for an Accounts segment this is the Accounts.country property).
- The industry list and country list are starting points; merchants tune to match their actual ICP definition.
