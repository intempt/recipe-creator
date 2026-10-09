---
description: Tells the AE when a customer is running out of seats or people from their domain keep signing up, which is the clearest upsell signal there is.
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

# Seat expansion signal to AE

Slash command: /seat-expansion-signal-to-ae-task

## Step 1: Measure how full the plan is

Create an AI-derived attribute 'seat_capacity_used' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account's domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.).

## Step 2: Find accounts near a limit

Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE). Use the result of "Measure how full the plan is".

## Step 3: Raise the expansion task

Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip: they're on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue. Use the result of "Measure how full the plan is", "Find accounts near a limit".

## Step 4: Track the expansion pipeline

Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target. Use the result of "Measure how full the plan is", "Find accounts near a limit", "Raise the expansion task".
