---
name: second-purchase-window
description: |
  Use when a user mentions "second-purchase window", or asks for related help. First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases happen here.
arguments: []
intempt:
  id: second-purchase-window
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases happen here."
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
        Create a segment called "Second-Purchase Window".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred = 1 time (all time)
        - AND Event: order_created occurred >= 1 time in last 30 days

        Description: Customers who just bought for the first time and are in the highest-conversion repurchase window. 50.3% of all repeat purchases happen in the first 30 days post-purchase, yet most brands suppress recent buyers from campaigns. This segment fixes that by giving you a clean cohort to target with personalized cross-sells, "complete-the-set" offers, and second-purchase nudges (not discount blasts — handwritten-style notes outperform).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Second-Purchase Window

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Second-Purchase Window".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created occurred = 1 time (all time)
   - AND Event: order_created occurred >= 1 time in last 30 days

   Description: Customers who just bought for the first time and are in the highest-conversion repurchase window. 50.3% of all repeat purchases happen in the first 30 days post-purchase, yet most brands suppress recent buyers from campaigns. This segment fixes that by giving you a clean cohort to target with personalized cross-sells, "complete-the-set" offers, and second-purchase nudges (not discount blasts — handwritten-style notes outperform).
   ```

## Taxonomy notes

- order_created is canonical.
- The "= 1 time AND in last 30 days" combination ensures freshness: brand-new customers actively in the highest-conversion window.
- This segment EXCLUDES one-time-buyers-at-risk (which requires 60+ days of inactivity) — these are complementary cohorts capturing the same user type at different lifecycle moments.
- Per BS&Co's 156K-customer benchmark: 6.3% of repeat buyers order again the same day, 15.9% within a week, 50.3% within 30 days. Targeting this window aggressively (rather than suppressing recent buyers) is the highest-leverage retention play.
- Recommended messaging: "complete the set" / "what others bought with this" cross-sell flows in days 0-7; replenishment-style framing in days 14-30 if applicable; light-touch product-care content throughout. Avoid steep discounts — they train second-purchase price-shopping.
- For a related cohort capturing first-time buyers who DIDN'T return in time, use one-time-buyers-at-risk.
