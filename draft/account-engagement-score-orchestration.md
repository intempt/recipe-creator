---
description: Scores each account from 0 to 100 on how its whole team uses the product, then runs a different play for healthy, slipping, declining and inactive accounts.
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
  - ecommerce
  - media
---

# Account engagement scoring and plays

Slash command: /account-engagement-score-orchestration

## Step 1: Score each account daily

Create an AI-derived attribute 'account_engagement_score' on the Account object, refreshed daily. Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats); (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output: numeric 0-100 with tier: green (75-100 healthy growing) / yellow (40-74 stable but warning signs) / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation is the differentiator: most CDPs score users, this scores the buying entity.

## Step 2: Group paying accounts by tier

Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history) and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from this segment based on tier. Use the result of "Score each account daily".

## Step 3: Write an email per tier

Generate per-tier email content. GREEN (expansion-leaning content sent to champion: 'Your team is in the top 25% of [Product] users) here's what high-growth accounts do next.' Plus subtle expansion CTA. YELLOW (reactivation content sent to admin: 'Noticing a few of your team members aren't logging in as often) want help re-engaging the team?' With a CSM-meeting CTA. RED (urgent personalized content sent to admin + executive sponsor: 'Your team's engagement has shifted) we'd like to understand what's going on. 15-minute call?' Direct CSM offer. DORMANT (last-chance content sent to champion: 'It's been a while) we miss you. Here's what's new since you last logged in.' With a fresh-start onboarding offer. Use the result of "Score each account daily", "Group paying accounts by tier".

## Step 4: Change what the admin sees

Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats + 'invite team members' nudges + use-case templates relevant to slow-adoption rescue. Red: shows direct-CSM-connect button + 'troubleshoot setup' resources prominently. Dormant: doesn't render account-engagement personalization (won't help: the user isn't logging in anyway; reach them via email instead). Use the result of "Score each account daily", "Group paying accounts by tier".

## Step 5: Run the play for each tier

Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly (expansion-leaning content to champion. Personalization activates for admin. Touch 2 quarterly) handoff to customer-progress-business-case journey. YELLOW: Touch 1 Day 0 (reactivation content to admin. Touch 2 Day 7) CSM task to reach out if score hasn't recovered. RED: Touch 1 Day 0 (urgent content + CSM task SAME-DAY. Touch 2 Day 3) executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 (last-chance email. Touch 2 Day 14) final outreach + warning before suppression. Exit on: tier escalation back to green (recovered: log retention_win), Subscription canceled (handoff to post-cancel-winback), or sustained dormancy 60+ days (suppress). Use the result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier", "Change what the admin sees".

## Step 6: See where the book is heading

Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant proportions: the health-of-business snapshot), tier-migration trends week-over-week (which direction are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle red-heavy portfolios: informs workload balancing). The strategic NRR view for leadership. Use the result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier", "Change what the admin sees", "Run the play for each tier".
