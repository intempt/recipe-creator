---
description: Posts revenue wins to one Slack channel and at-risk events to another through a configurable workflow. Notifications are static channel posts, with no dynamic owner mentions or DMs.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
  - media
---

# Revenue notifications in Slack

Slash command: /slack-purchase-notifications

## Step 1: Write the celebration posts

Generate Slack message content for revenue celebrations. Variants: (a) deal_won (include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B)) first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) (large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion) upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.

## Step 2: Write the operational alerts

Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) payment_failed: customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear.

## Step 3: Route wins and problems apart

Create a workflow firing on revenue events. Step sequence: (1) classify event type: celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don't ping the team at 2am for routine wins). Use the result of "Write the celebration posts", "Write the operational alerts".
