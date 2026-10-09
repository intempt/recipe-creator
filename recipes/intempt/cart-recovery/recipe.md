---
description: Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
  - media
---

# Abandoned cart recovery

Slash command: /cart-recovery

## Step 1: Find who abandoned a cart

This step builds a segment.
Identify users with cart_abandoned event in last 30 days who have NOT placed an order for that cart.

## Step 2: Write the three emails

Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. Use the result of "Find who abandoned a cart".

## Step 3: Schedule the sequence

Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. Use the result of "Find who abandoned a cart", "Write the three emails".

## Step 4: Test subject lines and offers

Add A/B variants on subject lines and incentive levels for the recovery journey. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence".

## Step 5: Track recovered revenue

Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence", "Test subject lines and offers".

## Step 6: Alert when it stops working

Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence", "Test subject lines and offers", "Track recovered revenue".
