---
description: Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits the stage, and escalates if they stay stuck.
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

# Stalled deal detection

Slash command: /stalled-deal-detection

## Step 1: Measure how long it has sat

Create an AI-derived attribute 'days_in_current_stage' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage's historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute 'days_since_last_activity' (any meeting / email reply / task completion on the deal).

## Step 2: Find the genuinely stuck ones

Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause, coming back next quarter, etc.). Refreshed daily. Use the result of "Measure how long it has sat".

## Step 3: Write a nudge per stage

Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled (re-ask the qualifying question that wasn't answered; (b) Demo stalled) offer technical deep-dive or POC; (c) Proposal stalled (surface that pricing pushback usually means decision-maker isn't bought in, offer to align; (d) Closing stalled) explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends: not auto-send. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones".

## Step 4: Draft it and chase the rep

Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled 'Review and send: stalled deal nudge' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + 'review' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don't auto-send the email: rep must review. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage".

## Step 5: See what is really dead

Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost: measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage", "Draft it and chase the rep".
