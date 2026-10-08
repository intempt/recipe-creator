---
description: When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying everything needed for the first touch.
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
---

# Product qualified lead to SDR task

Slash command: /pql-signal-to-sdr-task

## Step 1: Score free users on behaviour

Create an AI-derived attribute 'pql_score' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.

## Step 2: Find free users crossing 70

Build a segment 'PQL: free users score >= 70' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list. Use the result of "Score free users on behaviour".

## Step 3: Give the SDR the context

Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user's account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR's DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue. Use the result of "Score free users on behaviour", "Find free users crossing 70".

## Step 4: Hold the 24 hour first touch

Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours. Use the result of "Score free users on behaviour", "Find free users crossing 70", "Give the SDR the context".
