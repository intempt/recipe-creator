---
name: acquisition-channel-cohort
description: |
  Use when a user mentions "acquisition channel cohort", or asks for related help. Customers acquired through a specific channel (parameterized by utm_source/medium) — for channel-quality analysis.
arguments: []
intempt:
  id: acquisition-channel-cohort
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Customers acquired through a specific channel (parameterized by utm_source/medium) — for channel-quality analysis."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce, saas]
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
        Create a segment called "Acquisition Channel — <Channel Name>".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: utm_source = "<source>"  (e.g., "google", "facebook", "tiktok", "klaviyo", "newsletter")
        - AND Attribute: utm_medium = "<medium>"  (e.g., "cpc", "social", "email", "referral", "organic")
        - AND Event: order_created occurred >= 1 time (all time)

        Example concrete instances merchants typically build:
        - "Paid Social Acquired" — utm_source IN ["facebook", "instagram", "tiktok"] AND utm_medium IN ["cpc", "paid_social", "social"]
        - "Google Paid Acquired" — utm_source = "google" AND utm_medium = "cpc"
        - "Organic Search Acquired" — utm_source = "google" AND utm_medium = "organic"
        - "Email/Newsletter Acquired" — utm_medium = "email"
        - "Referral Acquired" — utm_medium IN ["referral", "affiliate"]

        Description: Channel-specific cohorts for retention analysis and channel-quality measurement. Customers acquired through different channels behave differently — organic and referral acquisitions typically have 30-50% higher repeat purchase rates than paid-social acquisitions. Building these cohorts lets you measure channel ROI by retention (not just acquisition cost) and tune retention investment per channel.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Acquisition Channel Cohort

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Acquisition Channel — <Channel Name>".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: utm_source = "<source>"  (e.g., "google", "facebook", "tiktok", "klaviyo", "newsletter")
   - AND Attribute: utm_medium = "<medium>"  (e.g., "cpc", "social", "email", "referral", "organic")
   - AND Event: order_created occurred >= 1 time (all time)

   Example concrete instances merchants typically build:
   - "Paid Social Acquired" — utm_source IN ["facebook", "instagram", "tiktok"] AND utm_medium IN ["cpc", "paid_social", "social"]
   - "Google Paid Acquired" — utm_source = "google" AND utm_medium = "cpc"
   - "Organic Search Acquired" — utm_source = "google" AND utm_medium = "organic"
   - "Email/Newsletter Acquired" — utm_medium = "email"
   - "Referral Acquired" — utm_medium IN ["referral", "affiliate"]

   Description: Channel-specific cohorts for retention analysis and channel-quality measurement. Customers acquired through different channels behave differently — organic and referral acquisitions typically have 30-50% higher repeat purchase rates than paid-social acquisitions. Building these cohorts lets you measure channel ROI by retention (not just acquisition cost) and tune retention investment per channel.
   ```

## Taxonomy notes

- utm_source, utm_medium are canonical Users attributes (first-touch attribution stored on the user record from session_start).
- order_created is canonical event.
- This is a TEMPLATE recipe — the merchant clones it once per channel they want to track. Five concrete instances are typically built (paid-social, paid-search, organic-search, email, referral).
- Channel attribution requires that utm_source and utm_medium be populated on landing pages. If your acquisition channels don't add proper UTM parameters, this segment will be empty for the majority of users.
- For SaaS, layer this with subscription_created instead of order_created to capture trial-to-paid conversions per channel.
- Channel-quality insight pattern: compare the average lifetime_value, avg_order_value, and days_since_last_activity across your channel cohorts. A channel with low CAC but bad retention is often a worse investment than a channel with higher CAC and strong retention. This segment is what makes that comparison legible to your retention team.
