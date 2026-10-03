---
id: account-engagement-score-orchestration
title: Account engagement scoring and plays
slash_command: /account-engagement-score-orchestration
group: Journeys
owner: intempt
curator: somya
summary: Scores each account from 0 to 100 on how its whole team uses the product, then runs a different
  play for healthy, slipping, declining and inactive accounts.
description: >-
  B2B account-level engagement scoring (aggregate user activity rolled up to account) to tiered account
  journeys: green accounts get expansion-leaning content, yellow get reactivation, red get save-flow +
  CSM task, dormant get win-back. Adobe CJA B2B-style account-as-unit pattern.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - account-engagement
    - b2b-tiering
    - account-as-unit
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new attribute, from step 1 "Score each account daily"
    - A new segment, from step 2 "Group paying accounts by tier"
    - A new designed email, from step 3 "Write an email per tier"
    - A new website personalization, from step 4 "Change what the admin sees"
    - A new journey, from step 5 "Run the play for each tier"
    - A new dashboard, from step 6 "See where the book is heading"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score each account daily
    summary: >-
      A daily 0 to 100 score on the account rather than the person: how many seats are active, whether
      usage is trending up or down, how many features the team touches, whether more than one role is
      engaged, and the tone of support tickets. Banded green at 75 and up, yellow 40 to 74, red 15 to
      39, dormant under 15.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'account_engagement_score' on the Account object, refreshed daily.
      Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats);
      (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth
      (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming
      from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output:
      numeric 0-100 with tier: green (75-100 healthy growing) / yellow (40-74 stable but warning signs)
      / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation
      is the differentiator: most CDPs score users, this scores the buying entity.
  - id: s2
    title: Group paying accounts by tier
    summary: >-
      All paying B2B accounts, split by engagement tier and refreshed daily. Accounts under 30 days old
      are left out because there is no history yet, and so are accounts already in a sales led save.
    builds: segment
    description: >-
      Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned
      by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history)
      and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from
      this segment based on tier. Use the result of "Score each account daily".
    dependsOn:
      - s1
  - id: s3
    title: Write an email per tier
    summary: >-
      Four emails in your brand voice. Green goes to the champion with what high growth accounts do next.
      Yellow goes to the admin offering help re-engaging the team. Red goes to the admin and the executive
      sponsor asking for a 15 minute call. Dormant goes to the champion with what changed since they last
      logged in.
    builds: email_html
    description: >-
      Generate per-tier email content. GREEN (expansion-leaning content sent to champion: 'Your team is
      in the top 25% of [Product] users) here's what high-growth accounts do next.' Plus subtle expansion
      CTA. YELLOW (reactivation content sent to admin: 'Noticing a few of your team members aren't logging
      in as often) want help re-engaging the team?' With a CSM-meeting CTA. RED (urgent personalized content
      sent to admin + executive sponsor: 'Your team's engagement has shifted) we'd like to understand
      what's going on. 15-minute call?' Direct CSM offer. DORMANT (last-chance content sent to champion:
      'It's been a while) we miss you. Here's what's new since you last logged in.' With a fresh-start
      onboarding offer. Use the result of "Score each account daily", "Group paying accounts by tier".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Change what the admin sees
    summary: >-
      The admin dashboard shows different things by tier: an expansion roadmap for green, team health
      stats and invite nudges for yellow, a direct line to your CSM plus setup troubleshooting for red.
      Dormant accounts get nothing, because they are not logging in anyway.
    builds: personalization
    description: >-
      Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows
      expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats
      + 'invite team members' nudges + use-case templates relevant to slow-adoption rescue. Red: shows
      direct-CSM-connect button + 'troubleshoot setup' resources prominently. Dormant: doesn't render
      account-engagement personalization (won't help: the user isn't logging in anyway; reach them via
      email instead). Use the result of "Score each account daily", "Group paying accounts by tier".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Run the play for each tier
    summary: >-
      Tier is read at entry and again every week. Green gets a monthly champion email and a quarterly
      handoff to the business case journey. Yellow gets an email on day 0 and a CSM task on day 7 if the
      score has not recovered. Red gets an email and a same day CSM task, then an executive sponsor task
      on day 3 if nobody has made contact. Dormant gets an email on day 0 and a final one on day 14. Accounts
      leave when they recover to green, when they cancel, or after 60 days dormant.
    builds: journey
    description: >-
      Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement
      tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly (expansion-leaning content to champion.
      Personalization activates for admin. Touch 2 quarterly) handoff to customer-progress-business-case
      journey. YELLOW: Touch 1 Day 0 (reactivation content to admin. Touch 2 Day 7) CSM task to reach
      out if score hasn't recovered. RED: Touch 1 Day 0 (urgent content + CSM task SAME-DAY. Touch 2 Day
      3) executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 (last-chance email. Touch
      2 Day 14) final outreach + warning before suppression. Exit on: tier escalation back to green (recovered:
      log retention_win), subscription_canceled (handoff to post-cancel-winback), or sustained dormancy
      60+ days (suppress). Use the result of "Score each account daily", "Group paying accounts by tier",
      "Write an email per tier", "Change what the admin sees".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: See where the book is heading
    summary: >-
      How accounts split across the four tiers, which way they moved week over week, how much ARR sits
      in red and dormant, how often a red account recovers, and the tier mix each CSM is carrying.
    builds: dashboard
    description: >-
      Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant
      proportions: the health-of-business snapshot), tier-migration trends week-over-week (which direction
      are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered
      conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle
      red-heavy portfolios: informs workload balancing). The strategic NRR view for leadership. Use the
      result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier",
      "Change what the admin sees", "Run the play for each tier".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: personalization
    producedByStep: s4
    type: personalization
    description: Personalization produced by this recipe.
  - key: journey
    producedByStep: s5
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Account engagement scoring and plays

Scores each account from 0 to 100 on how its whole team uses the product, then runs a different play for healthy, slipping, declining and inactive accounts.

## Steps

1. **Score each account daily** (builds attribute)

   A daily 0 to 100 score on the account rather than the person: how many seats are active, whether usage is trending up or down, how many features the team touches, whether more than one role is engaged, and the tone of support tickets. Banded green at 75 and up, yellow 40 to 74, red 15 to 39, dormant under 15.

2. **Group paying accounts by tier** (builds segment)

   All paying B2B accounts, split by engagement tier and refreshed daily. Accounts under 30 days old are left out because there is no history yet, and so are accounts already in a sales led save.

3. **Write an email per tier** (builds email_html)

   Four emails in your brand voice. Green goes to the champion with what high growth accounts do next. Yellow goes to the admin offering help re-engaging the team. Red goes to the admin and the executive sponsor asking for a 15 minute call. Dormant goes to the champion with what changed since they last logged in.

4. **Change what the admin sees** (builds personalization)

   The admin dashboard shows different things by tier: an expansion roadmap for green, team health stats and invite nudges for yellow, a direct line to your CSM plus setup troubleshooting for red. Dormant accounts get nothing, because they are not logging in anyway.

5. **Run the play for each tier** (builds journey)

   Tier is read at entry and again every week. Green gets a monthly champion email and a quarterly handoff to the business case journey. Yellow gets an email on day 0 and a CSM task on day 7 if the score has not recovered. Red gets an email and a same day CSM task, then an executive sponsor task on day 3 if nobody has made contact. Dormant gets an email on day 0 and a final one on day 14. Accounts leave when they recover to green, when they cancel, or after 60 days dormant.

6. **See where the book is heading** (builds dashboard)

   How accounts split across the four tiers, which way they moved week over week, how much ARR sits in red and dormant, how often a red account recovers, and the tier mix each CSM is carrying.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new attribute, from step 1 "Score each account daily"
- A new segment, from step 2 "Group paying accounts by tier"
- A new designed email, from step 3 "Write an email per tier"
- A new website personalization, from step 4 "Change what the admin sees"
- A new journey, from step 5 "Run the play for each tier"
- A new dashboard, from step 6 "See where the book is heading"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, personalization.
