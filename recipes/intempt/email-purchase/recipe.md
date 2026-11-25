---
frontmatter_id: email-purchase
slash_command: /email-purchase
description: Builds a segment of people who clicked an email but did not buy, and emails a weekly digest of how many email
  openers click, view a product and buy, by campaign.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds the clicked-but-did-not-buy segment and emails a weekly digest of email open to click to product view to
    order conversion and revenue by campaign.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 7 d
    required: false
  - name: topCampaignCount
    type: number
    label: Campaigns listed in the digest
    default: 10
    required: false
  - name: comparisonPeriod
    type: duration
    label: Window analyzed and compared with the one before
    default: 7 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: email_opened_event
    kind: event
    meaning: A customer opened an email
    properties:
    - name: campaign_id
      type: string
      meaning: Identifier of the campaign the opened email belongs to
      optional: true
  - slot: email_clicked_event
    kind: event
    meaning: A customer clicked a link in an email
    properties:
    - name: campaign_id
      type: string
      meaning: Identifier of the campaign the clicked email belongs to
      optional: true
  - slot: page_viewed_event
    kind: event
    meaning: A customer viewed a web page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: false
  - slot: email_sent_event
    kind: event
    meaning: An email was sent to a customer
    properties:
    - name: campaign_id
      type: string
      meaning: Identifier of the campaign the email was sent for
      optional: false
  steps:
  - id: s1
    builds: segment
    uses:
    - email_clicked_event
    - order_placed_event
    - conversionWindow
    instruction: 'Build a new segment of users named "Email Clickers Who Did Not Buy": users who did {email_clicked_event}
      in the last {conversionWindow} and did not do {order_placed_event} after their latest {email_clicked_event}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - email_opened_event
    - email_clicked_event
    - page_viewed_event
    - order_placed_event
    - email_sent_event
    - conversionWindow
    - topCampaignCount
    - comparisonPeriod
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {email_opened_event}
      in the last {comparisonPeriod} and writes these figures: how many then did {email_clicked_event}, then {page_viewed_event}
      with {page_viewed_event.page_url} containing /products/, then {order_placed_event}, each within {conversionWindow},
      with the conversion rate and median time between each step, next to the {comparisonPeriod} before; revenue per email
      opened, the sum of {order_placed_event.total_price} from those orders divided by the users who opened; the same step
      rates for the top {topCampaignCount} campaigns by {email_sent_event.campaign_id} send volume, matching opens and clicks
      by campaign_id; the number of users in the segment from "Find email clickers who did not buy". Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Email to purchase

Slash command: /email-purchase

## Step 1: Find email clickers who did not buy

Build a new segment of users named "Email Clickers Who Did Not Buy": users who did email clicked event in the last 7 d and did not do order placed event after their latest email clicked event.

## Step 2: Email the weekly email-to-purchase digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did email opened event in the last 7 d and writes these figures: how many then did email clicked event, then page viewed event with page url containing /products/, then order placed event, each within 7 d, with the conversion rate and median time between each step, next to the 7 d before; revenue per email opened, the sum of total price from those orders divided by the users who opened; the same step rates for the top 10 campaigns by campaign id send volume, matching opens and clicks by campaign_id; the number of users in the segment from "Find email clickers who did not buy". Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
