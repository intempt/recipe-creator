---
description: When an existing paying account crosses usage thresholds, enroll the contact in an expansion journey and send upgrade-focused messages to that same profile. Report journey activity in dashboards.
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

# Expansion play on a usage spike

Slash command: /usage-spike-expansion-play

## Step 1: Score the expansion signals

Create an AI-derived attribute 'expansion_signal_score' on the Account object. Inputs: (a) active-user growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth expansion (count of distinct features used per active user trending up); (c) multi-team adoption (users from different functions / departments based on email domain or profile data); (d) usage-cap proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected: signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which signals are firing.

## Step 2: Find accounts outgrowing the plan

Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven). Use the result of "Score the expansion signals".

## Step 3: Write to the champion

Generate email content for the user-champion at the account (the most-active user, usually). Variants by signal type: user-growth ('Your team is growing on [Product]) here's how power-using teams stay organized at this scale.' Feature-depth ('You're using [Product] deeper than 85% of similar accounts) here's what's next.' Usage-cap: 'Your team is approaching the [resource] limit. Here are options.' Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 4: Write to the budget holder

Generate email content for the economic buyer at the account (often someone NOT actively using the product day-to-day (admin / manager / finance owner). Variants by signal type: user-growth) 'Your team's usage of [Product] grew [N%] this quarter (here's a business-case summary of value delivered.' Feature-depth) 'Your team is in the top 15% of [Product] users by depth (let's discuss expansion options.' Usage-cap) 'Cost-comparison: upgrade vs. current overage costs.' Includes ROI snapshot. Tone: business-formal, value-substantive. Reply-to: assigned AE. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion".

## Step 5: Show the plan above theirs

Configure a recommendation surface 'Expansion features' that activates when the account is in the expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features available on higher-tier plans that the account would benefit from based on current usage patterns (e.g., 'Teams using [current features] often graduate to [advanced features]: here's what they unlock'). Includes upgrade-comparison surface for plan-decision-makers. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 6: Work the account over two weeks

Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch 1 (Day 0): champion email: 'you're growing fast / using deeply / hitting limits' content. Touch 2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session. Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if no AE meeting booked, create AE task with the full account context attached (signals, decision-makers, recommended package). Recommendation surface stays active for 60 days. Exit on: meeting_scheduled (handoff to AE), upgrade_completed (success (celebrate), deal_created (AE-owned from here), or expansion_signal drops below 50 for 30 days (false signal) exit gracefully). Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs".

## Step 7: Measure the expansion it makes

Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which signals fire most: informs which expansion levers the product naturally creates), expansion-signal-to-meeting conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert better than feature-depth: informs product/marketing focus). NRR contribution from this play. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs", "Work the account over two weeks".
