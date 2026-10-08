---
description: Shows how many people who open an email go on to click, view a product and buy, and which campaigns actually earn revenue.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Email to purchase

Slash command: /email-purchase

## Step 1: Follow email opens to orders

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
