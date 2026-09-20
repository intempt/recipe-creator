---
name: active-research-surge-accounts
description: |
  Use when a user mentions "active research surge accounts", or asks for related help. Accounts with 3+ pricing-page visits in last 7 days — active buying-cycle signal.
arguments: []
intempt:
  id: active-research-surge-accounts
  version: 1.0.0
  slashCommand: /active-research-surge-accounts
  group: Segments
  shortDescription: 'Accounts with 3+ pricing-page visits in last 7 days: active buying-cycle signal.'
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
        Create a segment called "Active Research Surge Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Event (across users in account): page_viewed where page_url contains "/pricing" occurred >= 3 times in last 7 days
        - AND Attribute: has_open_deal = false

        Description: Accounts where users have visited the pricing page 3+ times in the last 7 days — the active-research-surge signal. Sharper than single-visit indicators; multi-visit pricing review within a tight window is one of the strongest predictors of an in-flight buying decision. Trigger AE personalized outreach within 24 hours.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Active Research Surge Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Active Research Surge Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Event (across users in account): page_viewed where page_url contains "/pricing" occurred >= 3 times in last 7 days
   - AND Attribute: has_open_deal = false

   Description: Accounts where users have visited the pricing page 3+ times in the last 7 days — the active-research-surge signal. Sharper than single-visit indicators; multi-visit pricing review within a tight window is one of the strongest predictors of an in-flight buying decision. Trigger AE personalized outreach within 24 hours.
   ```

## Taxonomy notes

- page_viewed is canonical V2.1 event with property page_url.
- has_open_deal is canonical Accounts attribute.
- The 3+ visits in 7 days threshold distinguishes active buyers from casual researchers — single visits often happen during routine browsing or competitor research, while clustered repeat visits indicate evaluation.
- For sharper signal, layer with: comparison-page visits (page_url contains "/compare"), competitor-page visits, or feature-deep-dive page visits — the "decision-stage" content cluster.
- Distinct from high-intent-icp-prospects (which requires 1+ visit AND ICP fit). This recipe is INTENT-FIRST regardless of fit; merchants who want surge-AND-fit can layer with icp-match-accounts.
