---
name: email-purchase
description: |
  Use when a user mentions "email → purchase", or asks for related help. Email-to-purchase funnel using canonical email events with campaign comparison and revenue-per-email.
arguments: []
intempt:
  id: email-purchase
  version: 1.0.0
  slashCommand: /email-purchase
  group: Reports
  shortDescription: "Materialize a Funnel report 'Email to Purchase' of email_opened → email_clicked → product page_viewed → order_created over a 7-day window, broken down by campaign_id."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Email to Purchase".

        Steps:
        1. Event "email_opened" — "Opened Email"
        2. Event "email_clicked" — "Clicked Link"
        3. Event "page_viewed" where page_url contains /products/ within session of email_clicked — "Viewed Product"
        4. Event "order_created" — "Purchased"

        Conversion window: 7 days
        Breakdown: By "campaign_id" — derive from email_sent.campaign_id (cross-reference: email_sent.campaign_id maps to the campaign for emails the user opened/clicked). Top 10 campaigns by send volume.
        Compare: Previous period (prior 7 days)

        For each step, also surface:
        - Median time-to-convert (days from email_opened to next step)
        - Per-campaign conversion rate at each step
        - Revenue per email opened (Sum of order_created.total_price / Step 1 user count)

        Annotations:
        - Flag the campaign with the highest revenue-per-open (best ROI).
        - Flag the campaign with the highest open-to-click rate but lowest click-to-purchase (good creative, broken landing page).
        - Flag the campaign with the lowest open-to-click rate (subject-line / preheader issue).

        Taxonomy notes:
        - email_sent has campaign_id and sent_at. email_opened and email_clicked are separate events keyed by email/masterID.
        - Linking the open/click to a specific campaign requires joining via the email's campaign_id from the sending event.
        - "campaign_name" is not a property; campaign_id is the canonical handle.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Email → Purchase

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Email to Purchase".

   Steps:
   1. Event "email_opened" — "Opened Email"
   2. Event "email_clicked" — "Clicked Link"
   3. Event "page_viewed" where page_url contains /products/ within session of email_clicked — "Viewed Product"
   4. Event "order_created" — "Purchased"

   Conversion window: 7 days
   Breakdown: By "campaign_id" — derive from email_sent.campaign_id (cross-reference: email_sent.campaign_id maps to the campaign for emails the user opened/clicked). Top 10 campaigns by send volume.
   Compare: Previous period (prior 7 days)

   For each step, also surface:
   - Median time-to-convert (days from email_opened to next step)
   - Per-campaign conversion rate at each step
   - Revenue per email opened (Sum of order_created.total_price / Step 1 user count)

   Annotations:
   - Flag the campaign with the highest revenue-per-open (best ROI).
   - Flag the campaign with the highest open-to-click rate but lowest click-to-purchase (good creative, broken landing page).
   - Flag the campaign with the lowest open-to-click rate (subject-line / preheader issue).

   Taxonomy notes:
   - email_sent has campaign_id and sent_at. email_opened and email_clicked are separate events keyed by email/masterID.
   - Linking the open/click to a specific campaign requires joining via the email's campaign_id from the sending event.
   - "campaign_name" is not a property; campaign_id is the canonical handle.
   ```
