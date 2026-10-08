---
description: When several people from one company start using the product in the same fortnight, it briefs an AE and asks them to open a deal.
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
  - media
---

# Account level signal to AE task

Slash command: /pqa-account-engagement-to-ae-task

## Step 1: Score the whole account

Create an AI-derived attribute 'pqa_score' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain.

## Step 2: Find accounts crossing 70

Build a segment 'PQA: accounts score >= 70' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion: see seat-expansion workflow). Use the result of "Score the whole account".

## Step 3: Brief an AE to open a deal

Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts. Use the result of "Score the whole account", "Find accounts crossing 70".

## Step 4: Compare against cold outbound

Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time: usually PQAs win 2-3x more reliably. Use the result of "Score the whole account", "Find accounts crossing 70", "Brief an AE to open a deal".
