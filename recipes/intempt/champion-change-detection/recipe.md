---
description: Flags when a deal contact goes quiet using engagement recency, and triggers a rep re-engagement workflow before the deal stalls.
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
  - media
---

# Champion change detection

Slash command: /champion-change-detection

## Step 1: Track the champion daily

Create an AI-derived attribute 'champion_status' on the Deal object. Compute the deal's current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion: separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks.

## Step 2: Find deals that lost theirs

Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately). Use the result of "Track the champion daily".

## Step 3: Get the rep moving

Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up: pulled from enrichment); (2) create an urgent task for the AE: 'Champion gone: re-engage stakeholders' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don't auto-send email: rep must reach out personally. Use the result of "Track the champion daily", "Find deals that lost theirs".

## Step 4: See the ARR behind the risk

Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile). Use the result of "Track the champion daily", "Find deals that lost theirs", "Get the rep moving".
