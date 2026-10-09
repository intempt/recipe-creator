---
description: Finds late stage deals where only one person on the buyer's side is engaged and gives the rep three other names to bring in.
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

# Single threaded deal alert

Slash command: /single-threaded-deal-alert

## Step 1: Count who is actually engaged

Create an AI-derived attribute 'threading_depth' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as 'single-threaded' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag).

## Step 2: Find the risky ones

Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles, e.g. founder-led SMB). Use the result of "Count who is actually engaged".

## Step 3: Give the rep three names

Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled 'Multi-thread this deal: 3 suggested contacts' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress: that's not single-threading risk. Use the result of "Count who is actually engaged", "Find the risky ones".

## Step 4: See what threading is worth

Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile). Use the result of "Count who is actually engaged", "Find the risky ones", "Give the rep three names".
