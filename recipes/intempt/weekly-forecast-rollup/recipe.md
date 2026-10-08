---
description: Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and keeps the snapshot so last week can be checked.
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

# Weekly forecast rollup

Slash command: /weekly-forecast-rollup

## Step 1: Snapshot the pipeline

Build an insights report 'Weekly pipeline forecast snapshot' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted: sourced from deal-level forecast_category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week's forecast accurate?). Freezable: each Monday's report is preserved for historical comparison.

## Step 2: Write the leadership email

Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system). Use the result of "Snapshot the pipeline".

## Step 3: Send it Monday at 7am

Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so 'last week's forecast' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel: don't make exec emails AE-personal). Use the result of "Snapshot the pipeline", "Write the leadership email".

## Step 4: Check who forecasts honestly

Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who's optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%?: calibration health). Surfaces patterns leadership can coach on. Use the result of "Snapshot the pipeline", "Write the leadership email", "Send it Monday at 7am".
