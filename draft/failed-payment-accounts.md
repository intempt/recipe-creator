---
description: Users whose payment was declined in the last two weeks, so you can recover the money before the subscription lapses.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
---

# Users with a failed payment

Slash command: /failed-payment-accounts

## Step 1: Build the failed-payment list

Build a segment of users named "Failed-Payment Users".
A user is in the segment when any of these is true:
- they did the Payment failed event at least once in the last 14 days
- they did the Invoice payment failed event at least once in the last 14 days
- they did the Billing failed event at least once in the last 14 days
- they did the Charge failed event at least once in the last 14 days
