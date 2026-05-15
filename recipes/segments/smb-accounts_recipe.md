---
name: smb-accounts
description: |
  Use when a user mentions "smb accounts (under 100 employees)", or asks for related help. Small businesses (under 100 employees) — self-serve / low-touch routing.
arguments: []
intempt:
  id: smb-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Small businesses (under 100 employees) — self-serve / low-touch routing."
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
        Create a segment called "SMB Accounts".

        Object: Accounts

        Rules:
        - Attribute: employees < 100

        Description: Small businesses with under 100 employees. Foundation for self-serve / low-touch routing — these accounts go through automated nurture flows, in-product upgrade prompts, and minimal direct sales engagement. The PLG sweet spot.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# SMB Accounts (Under 100 Employees)

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "SMB Accounts".

   Object: Accounts

   Rules:
   - Attribute: employees < 100

   Description: Small businesses with under 100 employees. Foundation for self-serve / low-touch routing — these accounts go through automated nurture flows, in-product upgrade prompts, and minimal direct sales engagement. The PLG sweet spot.
   ```

## Taxonomy notes

- employees is canonical Accounts attribute.
- The under-100 threshold captures the SMB / startup segment that typically buys self-serve. For solopreneur or 1-10-employee filtering, layer with employees < 10.
- Pair with engagement signals (multi-stakeholder-engaged-accounts) to identify SMB accounts ready for sales-assisted intervention vs. those that should stay self-serve.
- This is the largest segment by account count for most B2B SaaS — the routing volume here justifies investing in automated nurture, in-product PLG, and self-serve-friendly UX rather than human outreach.
