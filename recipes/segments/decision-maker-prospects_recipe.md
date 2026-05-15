---
name: decision-maker-prospects
description: |
  Use when a user mentions "decision-maker prospects", or asks for related help. Senior-title users (C-level, VP, Director) showing intent — priority routing for AE outreach.
arguments: []
intempt:
  id: decision-maker-prospects
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Senior-title users (C-level, VP, Director) showing intent — priority routing for AE outreach."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
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
        Create a segment called "Decision-Maker Prospects".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: title contains any of ["CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of", "Chief"]
        - AND Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 30 days
        - AND Attribute: email is not empty

        Description: Senior-title users (C-level, VP, Director) who have visited pricing in the last 30 days. The economic-buyer signal — these are budget-holders actively researching. Highest priority for AE-led outreach, executive-sponsor engagement, and ROI-focused content delivery.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Decision-Maker Prospects

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Decision-Maker Prospects".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: title contains any of ["CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of", "Chief"]
   - AND Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 30 days
   - AND Attribute: email is not empty

   Description: Senior-title users (C-level, VP, Director) who have visited pricing in the last 30 days. The economic-buyer signal — these are budget-holders actively researching. Highest priority for AE-led outreach, executive-sponsor engagement, and ROI-focused content delivery.
   ```

## Taxonomy notes

- title is a CUSTOM Users attribute populated via enrichment (Clearbit, ZoomInfo, Apollo) or via identify() at signup. NOT canonical V2.1 — but the merchant adds it as a custom attribute. Without enrichment, this segment will be empty.
- page_viewed and email are canonical.
- The "title contains" filter captures common senior-title patterns. For more precision, the merchant can replace with a curated job-title list specific to their ICP (e.g., "VP of Engineering", "Head of Marketing", "Chief Revenue Officer").
- For non-English markets, expand the title list with localized equivalents (e.g., "Geschäftsführer" for German CEO, "Direktor" for Director).
- This segment compounds with active-research-surge-accounts and demo-requested-accounts — a senior-title user from a surge account who requested a demo is the single highest-priority lead in your pipeline. AE response time on this combination should be measured in minutes, not hours.
