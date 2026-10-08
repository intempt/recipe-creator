---
description: Enriches and scores every inbound lead, then assigns it by named account, territory or round robin so nothing rots in an unassigned queue.
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
---

# Inbound lead routing

Slash command: /inbound-lead-routing

## Step 1: Score the lead out of 100

Create an AI-derived attribute 'lead_score' on the User object. Composite: (a) ICP fit (firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal) form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal (title seniority + role relevance, 0-20 points; (d) brand engagement) prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).

## Step 2: Assign it to the right rep

Create a workflow firing on form_submitted OR user_signed_up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue. Use the result of "Score the lead out of 100".

## Step 3: Check the balance and the SLA

Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check: variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers. Use the result of "Score the lead out of 100", "Assign it to the right rep".
