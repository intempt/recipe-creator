---
name: new-paying-customers
description: |
  Use when a user mentions "new paying customers", or asks for related help. First 30 days post-subscription — paid-onboarding cohort distinct from generic recently-signed-up.
arguments: []
intempt:
  id: new-paying-customers
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "First 30 days post-subscription — paid-onboarding cohort distinct from generic recently-signed-up."
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
        Create a segment called "New Paying Customers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: subscription_created occurred >= 1 time in last 30 days
        - AND Attribute: plan_name is not "free"
        - AND Attribute: plan_name is not "trial"

        Description: Users who converted to a paid plan in the last 30 days. The paid-onboarding cohort — distinct from recently-signed-up-users (which is account creation). The first 30 days post-paid-conversion is the highest-leverage retention window; trigger CSM kickoff, premium-feature discovery, and ROI-tracking content.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# New Paying Customers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "New Paying Customers".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: subscription_created occurred >= 1 time in last 30 days
   - AND Attribute: plan_name is not "free"
   - AND Attribute: plan_name is not "trial"

   Description: Users who converted to a paid plan in the last 30 days. The paid-onboarding cohort — distinct from recently-signed-up-users (which is account creation). The first 30 days post-paid-conversion is the highest-leverage retention window; trigger CSM kickoff, premium-feature discovery, and ROI-tracking content.
   ```

## Taxonomy notes

- subscription_created is canonical V2.1 event with property plan_name.
- plan_name is canonical Users attribute.
- The "is not 'free' AND is not 'trial'" filter ensures we capture true paid conversions — not free-plan signups or trial starts that happen to fire subscription_created.
- For workspaces with non-standard plan names, adjust the exclusion list to match (e.g., "starter" or "freemium" if those are free-tier names).
- Distinct from new-customer cohorts in B2B (which use deal_closed signals on Accounts) — this one is for self-serve / PLG paid conversions where the subscription event is the canonical signal.
