---
description: Treats a click on pricing, a feature page or a case study as interest and sends more on that exact topic, at most once a week.
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
---

# Email click follow up

Slash command: /email-click-retargeting

## Step 1: Log what they clicked

Create an AI-derived attribute 'recent_click_topics' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about: log it and act on it.

## Step 2: Find the meaningful clicks

Build a segment 'Recent email clickers - last 14 days' capturing users with email_clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study, not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial, those are getting other journeys). Use the result of "Log what they clicked".

## Step 3: Write a reply per topic

Generate retargeting email content per click topic. Pricing-page click: 'You looked at pricing: want to talk it through? Or here's a pricing FAQ.' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive 'we saw you!' creepiness. Send-from: marketing@ or the original email's sender. Use the result of "Log what they clicked", "Find the meaningful clicks".

## Step 4: Follow up once, nudge once

Build a 2-touch journey triggered when email_clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: meeting_scheduled, deal_created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user: clicks happen constantly, don't bombard. Use the result of "Log what they clicked", "Find the meaningful clicks", "Write a reply per topic".

## Step 5: Compare against no follow up

Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original: they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting): typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value. Use the result of "Log what they clicked", "Find the meaningful clicks", "Write a reply per topic", "Follow up once, nudge once".
