---
description: Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks anyone who reads all three.
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
  - media
  - social
---

# Content download nurture

Slash command: /content-download-nurture

## Step 1: Find recent downloaders

Build a segment 'Recent content downloaders - last 30 days' capturing users with Form submitted where form_type = content_download in the last 30 days, partitioned by the content_topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture).

## Step 2: Write three emails per topic

Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): 'Thanks for downloading [content title] (here's a related piece you might like') second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA: 'Want to see how this works in your context? Book a 30-min demo' or 'Try it free for 14 days'. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3. Use the result of "Find recent downloaders".

## Step 3: Send on days 1, 7 and 14

Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: Meeting scheduled, Deal created, or 21-day timeout. Use the result of "Find recent downloaders", "Write three emails per topic".

## Step 4: See which topics make pipeline

Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads: informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline: informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals: flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value). Use the result of "Find recent downloaders", "Write three emails per topic", "Send on days 1, 7 and 14".
