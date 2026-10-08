---
description: Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached, and puts the rest into nurture.
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
---

# Lead qualification and handoff

Slash command: /lead-qualification

## Step 1: Score every lead

Define a Qualification attribute weighting firmographic fit, intent, and engagement.

## Step 2: Split into hot, warm and cold

Segment leads into hot/warm/cold tiers based on qualification score. Use the result of "Score every lead".

## Step 3: Route hot leads round robin

Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. Use the result of "Score every lead", "Split into hot, warm and cold".

## Step 4: Nurture warm and cold leads

Build nurture journeys for warm and cold leads with appropriate cadence. Use the result of "Score every lead", "Split into hot, warm and cold", "Route hot leads round robin".

## Step 5: Track handoff to opportunity

Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. Use the result of "Score every lead", "Split into hot, warm and cold", "Route hot leads round robin", "Nurture warm and cold leads".
