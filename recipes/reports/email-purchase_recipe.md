---
name: email-purchase
description: |
  Use when a user mentions "email to purchase", or asks for related help. Email-to-purchase funnel with campaign comparison and revenue-per-email.
arguments: []
intempt:
  id: email-purchase
  version: 1.0.0
  slashCommand: /email-purchase
  group: Reports
  title: "Email to purchase"
  shortDescription: "Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn revenue."
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
      title: "Follow email opens to orders"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel from email opened to clicked, product page viewed and order placed inside 7 days, split by the top 10 campaigns. Adds median time to convert and revenue per email opened, and flags the best and worst campaign on each step."
      prompt: |
        Create a Funnel report called "Email to Purchase".

        Steps:
        1. Event "Email opened": "Opened Email"
        2. Event "Email clicked": "Clicked Link"
        3. Event "View page" where the page URL contains /products/ within the session of the email click: "Viewed Product"
        4. Event "Placed order": "Purchased"

        Conversion window: 7 days
        Breakdown: By campaign, taken from the campaign that sent the email the user opened or clicked. Top 10 campaigns by send volume.
        Compare: Previous period (prior 7 days)

        For each step, also surface:
        - Median time-to-convert (days from email opened to next step)
        - Per-campaign conversion rate at each step
        - Revenue per email opened (sum of order total / Step 1 user count)

        Annotations:
        - Flag the campaign with the highest revenue-per-open (best ROI).
        - Flag the campaign with the highest open-to-click rate but lowest click-to-purchase (good creative, broken landing page).
        - Flag the campaign with the lowest open-to-click rate (subject-line / preheader issue).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Email to purchase

Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn revenue.

## What it does

1. **Follow email opens to orders** (`build_funnel_report`)

   A four step funnel from email opened to clicked, product page viewed and order placed inside 7 days, split by the top 10 campaigns. Adds median time to convert and revenue per email opened, and flags the best and worst campaign on each step.

## What you end up with

- **report** (report): Report produced by this recipe.
