---
frontmatter_id: email-purchase
slash_command: /email-purchase
description: Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn revenue.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn
    revenue.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 7 d
    required: false
  - name: topCampaignCount
    type: number
    label: Number of top campaigns to break down by send volume
    default: 10
    required: false
  - name: comparisonPeriod
    type: duration
    label: Comparison period (previous period)
    default: 7 d
    required: false
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
    - name: sent_at
      type: date
      meaning: Time the email was sent
      optional: false
  steps:
  - id: s1
    builds: report
    instruction: 'Create a funnel report named "Email to Purchase" with these steps in order: {email_opened_event}, then {email_clicked_event},
      then {page_viewed_event} where page_url contains "/products/" performed within the session of {email_clicked_event},
      then {order_placed_event}. Set the conversion window to {conversionWindow}. Break down by campaign_id, derived from
      {email_sent_event}.campaign_id by joining each open and click to the campaign_id of the sending event for that email,
      and show the top {topCampaignCount} campaigns by send volume. Compare against the previous {comparisonPeriod}. For each
      step, show median time to convert from the prior step, per-campaign conversion rate at each step, and revenue per email
      opened, calculated as the sum of {order_placed_event.total_price} divided by the step 1 user count.'
---

# Email to purchase

Slash command: /email-purchase

## Step 1: Follow email opens to orders

Create a Funnel report called "Email to Purchase".
Steps:
1. Event "Email opened": "Opened Email"
2. Event "Email clicked": "Clicked Link"
3. Event "View page" where Page URL contains /products/ within session of Email clicked: "Viewed Product"
4. Event "Placed order": "Purchased"
Conversion window: 7 days
Breakdown: By "campaign_id": derive from Email sent.campaign_id (cross-reference: Email sent.campaign_id maps to the campaign for emails the user opened/clicked). Top 10 campaigns by send volume.
Compare: Previous period (prior 7 days)
For each step, also surface:
- Median time-to-convert (days from Email opened to next step)
- Per-campaign conversion rate at each step
- Revenue per email opened (Sum of Placed order.total_price / Step 1 user count)
Annotations:
- Flag the campaign with the highest revenue-per-open (best ROI).
- Flag the campaign with the highest open-to-click rate but lowest click-to-purchase (good creative, broken landing page).
- Flag the campaign with the lowest open-to-click rate (subject-line / preheader issue).
Taxonomy notes:
- Email sent has campaign_id and sent_at. Email opened and Email clicked are separate events keyed by email/masterID.
- Linking the open/click to a specific campaign requires joining via the email's campaign_id from the sending event.
- "campaign_name" is not a property; campaign_id is the canonical handle.
