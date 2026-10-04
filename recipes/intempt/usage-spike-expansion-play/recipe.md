---
id: usage-spike-expansion-play
title: Expansion play on a usage spike
slash_command: /usage-spike-expansion-play
group: Journeys
owner: intempt
curator: somya
summary: When an account outgrows its plan, tells the champion they are scaling, gives the budget holder
  the numbers, and hands the AE a briefed task.
description: >-
  When existing paying customers cross usage thresholds (fast user-growth on the account, feature-depth
  expansion, multi-team usage) fire a multi-stakeholder expansion journey: champion gets 'you're scaling'
  content, economic buyer gets upgrade-options content, recommendation surface highlights expansion features.
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
    - expansion
    - multi-stakeholder
    - usage-driven
prerequisites:
  events:
    - value: feature_used
      severity: blocking
    - value: user_signed_up
      severity: recommended
touches:
  reads:
    - The feature_used event in your project
    - The user_signed_up event in your project
  writes:
    - A new attribute, from step 1 "Score the expansion signals"
    - A new segment, from step 2 "Find accounts outgrowing the plan"
    - A new designed email, from step 3 "Write to the champion"
    - A new designed email, from step 4 "Write to the budget holder"
    - A new product recommendation, from step 5 "Show the plan above theirs"
    - A new journey, from step 6 "Work the account over two weeks"
    - A new dashboard, from step 7 "Measure the expansion it makes"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score the expansion signals
    summary: >-
      A 0 to 100 score on the account from how fast new users are joining from their domain against the
      last 90 days, whether each user is reaching for more features, whether several teams or functions
      have come on, how close they are to their seat, API, event or storage limits, and any new integrations.
      It also says which of those signals are firing.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'expansion_signal_score' on the Account object. Inputs: (a) active-user
      growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth
      expansion (count of distinct features used per active user trending up); (c) multi-team adoption
      (users from different functions / departments based on email domain or profile data); (d) usage-cap
      proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected:
      signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which
      signals are firing.
  - id: s2
    title: Find accounts outgrowing the plan
    summary: >-
      Paying accounts scoring 70 or more in the last 14 days with no expansion deal already running, split
      by the dominant signal: user growth, feature depth, or hitting a limit.
    builds: segment
    description: >-
      Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score
      >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate
      against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal
      (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven). Use the result of "Score the
      expansion signals".
    dependsOn:
      - s1
  - id: s3
    title: Write to the champion
    summary: >-
      To the most active user at the account, matched to the signal. Growing team: how teams at this size
      stay organised. Deeper use: they are ahead of 85% of similar accounts, and here is what comes next.
      Near a limit: the options. Peer to peer, so the champion feels proud rather than sold to.
    builds: email_html
    description: >-
      Generate email content for the user-champion at the account (the most-active user, usually). Variants
      by signal type: user-growth ('Your team is growing on [Product]) here's how power-using teams stay
      organized at this scale.' Feature-depth ('You're using [Product] deeper than 85% of similar accounts)
      here's what's next.' Usage-cap: 'Your team is approaching the [resource] limit. Here are options.'
      Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched. Use
      the result of "Score the expansion signals", "Find accounts outgrowing the plan".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Write to the budget holder
    summary: >-
      To the admin, manager or finance owner who does not use it day to day. Growing team: usage grew
      this much last quarter, here is the value delivered. Deeper use: top 15% by depth, let us talk options.
      Near a limit: upgrading against what the overage costs. Each carries an ROI snapshot, with replies
      going to the assigned AE.
    builds: email_html
    description: >-
      Generate email content for the economic buyer at the account (often someone NOT actively using the
      product day-to-day (admin / manager / finance owner). Variants by signal type: user-growth) 'Your
      team's usage of [Product] grew [N%] this quarter (here's a business-case summary of value delivered.'
      Feature-depth) 'Your team is in the top 15% of [Product] users by depth (let's discuss expansion
      options.' Usage-cap) 'Cost-comparison: upgrade vs. current overage costs.' Includes ROI snapshot.
      Tone: business-formal, value-substantive. Reply-to: assigned AE. Use the result of "Score the expansion
      signals", "Find accounts outgrowing the plan", "Write to the champion".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Show the plan above theirs
    summary: >-
      An in app panel on the admin dashboard, also used inside the emails, listing the higher tier features
      this account would benefit from given how they already work, with a plan comparison for whoever
      decides.
    builds: recommendation
    description: >-
      Configure a recommendation surface 'Expansion features' that activates when the account is in the
      expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features
      available on higher-tier plans that the account would benefit from based on current usage patterns
      (e.g., 'Teams using [current features] often graduate to [advanced features]: here's what they unlock').
      Includes upgrade-comparison surface for plan-decision-makers. Use the result of "Score the expansion
      signals", "Find accounts outgrowing the plan".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Work the account over two weeks
    summary: >-
      Champion email on day 0. The upgrade comparison appears for admins at their next session on day
      3. The budget holder gets the ROI email on day 7. If no meeting is booked by day 14, the AE gets
      a task carrying the signals, the decision makers and a recommended package. The panel stays up for
      60 days. It closes on a meeting, an upgrade, a new deal, or the score falling under 50 for 30 days.
    builds: journey
    description: >-
      Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch
      1 (Day 0): champion email: 'you're growing fast / using deeply / hitting limits' content. Touch
      2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session.
      Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if
      no AE meeting booked, create AE task with the full account context attached (signals, decision-makers,
      recommended package). Recommendation surface stays active for 60 days. Exit on: meeting_scheduled
      (handoff to AE), upgrade_completed (success (celebrate), deal_created (AE-owned from here), or expansion_signal
      drops below 50 for 30 days (false signal) exit gracefully). Use the result of "Score the expansion
      signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder",
      "Show the plan above theirs".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: Measure the expansion it makes
    summary: >-
      Signals per week by type, how many turn into meetings and into deals, the ARR added against a control,
      which signal converts best, and what this play contributes to net revenue retention.
    builds: dashboard
    description: >-
      Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which
      signals fire most: informs which expansion levers the product naturally creates), expansion-signal-to-meeting
      conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion
      (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert
      better than feature-depth: informs product/marketing focus). NRR contribution from this play. Use
      the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the
      champion", "Write to the budget holder", "Show the plan above theirs", "Work the account over two
      weeks".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
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
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s5
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Expansion play on a usage spike

When an account outgrows its plan, tells the champion they are scaling, gives the budget holder the numbers, and hands the AE a briefed task.

## Steps

1. **Score the expansion signals** (builds attribute)

   A 0 to 100 score on the account from how fast new users are joining from their domain against the last 90 days, whether each user is reaching for more features, whether several teams or functions have come on, how close they are to their seat, API, event or storage limits, and any new integrations. It also says which of those signals are firing.

2. **Find accounts outgrowing the plan** (builds segment)

   Paying accounts scoring 70 or more in the last 14 days with no expansion deal already running, split by the dominant signal: user growth, feature depth, or hitting a limit.

3. **Write to the champion** (builds email_html)

   To the most active user at the account, matched to the signal. Growing team: how teams at this size stay organised. Deeper use: they are ahead of 85% of similar accounts, and here is what comes next. Near a limit: the options. Peer to peer, so the champion feels proud rather than sold to.

4. **Write to the budget holder** (builds email_html)

   To the admin, manager or finance owner who does not use it day to day. Growing team: usage grew this much last quarter, here is the value delivered. Deeper use: top 15% by depth, let us talk options. Near a limit: upgrading against what the overage costs. Each carries an ROI snapshot, with replies going to the assigned AE.

5. **Show the plan above theirs** (builds recommendation)

   An in app panel on the admin dashboard, also used inside the emails, listing the higher tier features this account would benefit from given how they already work, with a plan comparison for whoever decides.

6. **Work the account over two weeks** (builds journey)

   Champion email on day 0. The upgrade comparison appears for admins at their next session on day 3. The budget holder gets the ROI email on day 7. If no meeting is booked by day 14, the AE gets a task carrying the signals, the decision makers and a recommended package. The panel stays up for 60 days. It closes on a meeting, an upgrade, a new deal, or the score falling under 50 for 30 days.

7. **Measure the expansion it makes** (builds dashboard)

   Signals per week by type, how many turn into meetings and into deals, the ARR added against a control, which signal converts best, and what this play contributes to net revenue retention.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project
- The user_signed_up event in your project

Writes:

- A new attribute, from step 1 "Score the expansion signals"
- A new segment, from step 2 "Find accounts outgrowing the plan"
- A new designed email, from step 3 "Write to the champion"
- A new designed email, from step 4 "Write to the budget holder"
- A new product recommendation, from step 5 "Show the plan above theirs"
- A new journey, from step 6 "Work the account over two weeks"
- A new dashboard, from step 7 "Measure the expansion it makes"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, recommendation.
