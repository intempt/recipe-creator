---
description: Uses AI attribute scores from first-party events to spot competitive intent and trigger a personalized email plus a CSM follow-up task.
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

# Competitor signal response

Slash command: /competitor-mention-detected-response

## Step 1: Spot competitor interest

Create an AI-derived attribute 'recent_competitor_signal' on the User/Account object. Detects: (a) visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails, (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison resource, (e) appeared on a competitor's review site as a reviewer (if data permits). Output: structured object with competitor_name, signal_type, signal_strength, recency, and inferred_intent (evaluation / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor signal.

## Step 2: Group by what they intend

Build a segment 'Active competitor signal' capturing users/accounts with recent_competitor_signal in the last 14 days where signal_strength is medium or high. Partitioned by inferred_intent so the journey branches accordingly. Excludes brand-new prospects (different motion, for prospects, competitive intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE prospects where competitor signal is a save/competitive-defend moment. Use the result of "Spot competitor interest".

## Step 3: Write a reply per intent

This step builds a designed marketing email (HTML).
Generate competitive content variants per inferred_intent. Evaluation intent (existing customer comparing (concerning but not yet leaving): 'Helpful comparison: [Product] vs [Competitor] from your team's perspective') honest comparison + specific advantages relevant to their use case. Dissatisfaction intent (existing customer with friction signals + competitor signal (leaving risk): 'Want to talk? [CSM name] would like to understand what's not working') direct outreach offer, no defensive product pitch. Curious-comparison intent (neutral exploration): 'Most teams who compare us to [Competitor] choose [Product] for [specific differentiator]: here's why' + customer case study. Leaving intent (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for low-signal exploration. Use the result of "Spot competitor interest", "Group by what they intend".

## Step 4: Show what they are missing

Configure a recommendation surface 'Capabilities you're not using yet' that activates when a user has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn't tried but their cohort uses for high-value outcomes. The surface answers the implicit question 'why stay?' with concrete unused capability: much more convincing than feature-comparison docs. Renders in-app for 30 days. Use the result of "Spot competitor interest", "Group by what they intend".

## Step 5: Respond within four hours

Build a journey wired to competitor-signal segment, branched by inferred_intent. Touch 1 (within 4 hours of signal: speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE task with full competitor intel attached (competitor name, signal type, inferred intent, suggested talking points, customer's current usage profile). Touch 4 (Day 7, if account is still showing competitive intent + hasn't engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit on: explicit positive renewal/retention signal (saved), churned (loss: feed into win-loss analysis), or 30-day timeout with no further competitor signal (signal cooled). Use the result of "Spot competitor interest", "Group by what they intend", "Write a reply per intent", "Show what they are missing".

## Step 6: See which rivals you lose to

Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors are hottest in your current customer base: strategic competitive intel for leadership), per-competitor save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution (evaluation vs. leaving: leading indicator of churn from competitive pressure), and ARR-weighted at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function with real data, not assumptions. Use the result of "Spot competitor interest", "Group by what they intend", "Write a reply per intent", "Show what they are missing", "Respond within four hours".
