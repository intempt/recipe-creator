---
id: email-purchase
title: Email to purchase
slash_command: /email-purchase
group: Reports
owner: intempt
curator: aman
summary: Shows how many people who open an email go on to click, view a product and buy, and which campaigns
  actually earn revenue.
description: >-
  Email-to-purchase funnel using canonical email events with campaign comparison and revenue-per-email.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
    - finance
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Follow email opens to orders"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Follow email opens to orders
    summary: >-
      A four step funnel from email opened to clicked, product page viewed and order placed inside 7 days,
      split by the top 10 campaigns. Adds median time to convert and revenue per email opened, and flags
      the best and worst campaign on each step.
    builds: report
    description: |-
      Create a Funnel report called "Email to Purchase".
      Steps:
      1. Event "email_opened": "Opened Email"
      2. Event "email_clicked": "Clicked Link"
      3. Event "page_viewed" where page_url contains /products/ within session of email_clicked: "Viewed Product"
      4. Event "order_created": "Purchased"
      Conversion window: 7 days
      Breakdown: By "campaign_id": derive from email_sent.campaign_id (cross-reference: email_sent.campaign_id maps to the campaign for emails the user opened/clicked). Top 10 campaigns by send volume.
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
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Email to purchase

Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn revenue.

## Steps

1. **Follow email opens to orders** (builds report)

   A four step funnel from email opened to clicked, product page viewed and order placed inside 7 days, split by the top 10 campaigns. Adds median time to convert and revenue per email opened, and flags the best and worst campaign on each step.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Follow email opens to orders"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
