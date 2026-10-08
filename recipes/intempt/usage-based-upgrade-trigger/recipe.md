---
description: Catches an account nearing its plan limits, shows the decision maker an upgrade inside the app, and calls an AE in on the bigger ones.
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

# Upgrade prompt when limits approach

Slash command: /usage-based-upgrade-trigger

## Step 1: Find the bottleneck limit

Create an AI-derived attribute 'usage_capacity_used' on the Account object. For each metered usage dimension on the account's current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling).

## Step 2: Find accounts near a limit

Build a segment 'Upgrade-ready accounts' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn't already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) to in-app prompt, (b) near-limit (0.95-1.0) to in-app prompt + AE task, (c) over-limit to urgent AE task + customer notification. Use the result of "Find the bottleneck limit".

## Step 3: Write the in app prompt

This step builds a page.
Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: 'You've used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we're charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can't approve). Use the result of "Find accounts near a limit".

## Step 4: Prompt, then call in an AE

Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don't wait for prompt-clickthrough: these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don't re-fire for the same account within 14 days even if it's still over threshold (avoid prompt fatigue). Use the result of "Find the bottleneck limit", "Find accounts near a limit", "Write the in app prompt".

## Step 5: Compare prompt against AE

Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal. Use the result of "Find the bottleneck limit", "Find accounts near a limit", "Write the in app prompt", "Prompt, then call in an AE".
