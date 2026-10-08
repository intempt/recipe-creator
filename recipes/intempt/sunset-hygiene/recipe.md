---
description: Gives subscribers who have ignored six months of email one chance to say they still want it, then stops mailing them to protect deliverability.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
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

# Sunset inactive subscribers

Slash command: /sunset-hygiene

## Step 1: Find who stopped reading

This step builds a segment.
Identify subscribers who have not opened or clicked any email in 180+ days.

## Step 2: Write the last chance email

Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. Use the result of "Find who stopped reading".

## Step 3: Send it, then wait 14 days

Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. Use the result of "Find who stopped reading", "Write the last chance email".

## Step 4: Suppress anyone who ignores it

Create a workflow automatically adding non-responders to the suppression list after the 14-day window. Use the result of "Find who stopped reading", "Write the last chance email", "Send it, then wait 14 days".

## Step 5: Watch your deliverability

Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement. Use the result of "Find who stopped reading", "Write the last chance email", "Send it, then wait 14 days", "Suppress anyone who ignores it".
