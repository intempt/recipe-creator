---
name: demo-requested-accounts
description: |
  Use when a user mentions "demo-requested accounts", or asks for related help. Accounts where any user submitted a demo form in last 30 days — top SDR-routing priority.
arguments: []
intempt:
  id: demo-requested-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Accounts where any user submitted a demo form in last 30 days — top SDR-routing priority."
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
        Create a segment called "Demo-Requested Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Event (across users in account): submit_on a demo-request form occurred >= 1 time in last 30 days
        - AND Attribute: has_open_deal = false

        Description: Accounts where any user submitted a demo-request form in the last 30 days, with no existing open deal. Highest SDR-routing priority — research consistently shows 53% conversion rate for 1-hour response vs 17% after 24 hours. SLA: SDR contact within 1 hour, AE follow-up within 24 hours.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Demo-Requested Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Demo-Requested Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Event (across users in account): submit_on a demo-request form occurred >= 1 time in last 30 days
   - AND Attribute: has_open_deal = false

   Description: Accounts where any user submitted a demo-request form in the last 30 days, with no existing open deal. Highest SDR-routing priority — research consistently shows 53% conversion rate for 1-hour response vs 17% after 24 hours. SLA: SDR contact within 1 hour, AE follow-up within 24 hours.
   ```

## Taxonomy notes

- submit_on is canonical V2.1 event used for form submissions; the rule filters to a specific demo form by form_id (configured per merchant — e.g., form_id = "demo-request" or matching the merchant's contact-form ID).
- has_open_deal is canonical Accounts attribute.
- The has_open_deal = false filter avoids re-routing existing pipeline — these are net-new opportunities for SDR/AE engagement.
- The "across users in account" aggregation means multiple users from the same account submitting demos count as one account (right semantic for ABM routing).
- For more nuanced routing, pair with icp-match-accounts (high-fit demo requests get prioritized over low-fit) or with active-research-surge-accounts (high-intent demo requests over low-intent).
