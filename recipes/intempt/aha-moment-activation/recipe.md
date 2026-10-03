---
id: aha-moment-activation
title: Aha moment reinforcement
slash_command: /aha-moment-activation
group: Journeys
owner: intempt
summary: Follows up right after someone hits the action that predicts retention, so the first win turns
  into a habit instead of a one off.
description: >-
  When a user completes their product's defined aha-moment action (the activation event that predicts
  retention), fire a reinforcement journey, congratulate, deepen engagement with the next-step feature,
  and educate around expansion to prevent post-aha dropoff.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - activation
    - aha-moment
    - early-engagement
prerequisites:
  events:
    - value: feature_first_used
      severity: blocking
touches:
  reads:
    - The feature_first_used event in your project
  writes:
    - A new segment, from step 1 "Find people who just got value"
    - A new designed email, from step 2 "Write three follow up emails"
    - A new journey, from step 3 "Send on days 1, 5 and 10"
    - A new dashboard, from step 4 "Track activation and retention"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find people who just got value
    summary: >-
      Anyone who completed your activation event in the last 14 days and has not been through this follow
      up yet. Your product team picks that event off the retention curve, for example first message sent
      or first project published.
    builds: segment
    description: >-
      Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event
      (defined per product, e.g. 'first message sent', 'first project published', 'first deal created';
      configurable in the segment definition) in the last 14 days AND who haven't received the activation
      reinforcement yet. The aha-moment event is product-specific and should be set by Product team based
      on retention curve analysis.
  - id: s2
    title: Write three follow up emails
    summary: >-
      One that congratulates them and shows what others did after the same milestone, one that points
      to the natural next feature with a how to and a deep link, and one that shows how power users go
      further.
    builds: email_html
    description: >-
      Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone,
      frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments.
      Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the
      aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app
      deep link. Touch 3 (Day 10): introduce a power-user behavior: 'now that you've [done aha], here's
      how power users go further.' Aim: shift user from 'tried it' to 'depends on it'. Use the result
      of "Find people who just got value".
    dependsOn:
      - s1
  - id: s3
    title: Send on days 1, 5 and 10
    summary: >-
      Starts when the activation event fires, with emails on day 1, day 5 and day 10. If they find the
      next feature on their own by day 5, the middle email is skipped and they go straight to the power
      user one. They leave if they start paying, unsubscribe, or after 14 days.
    builds: journey
    description: >-
      Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch
      2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally
      by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: subscription_created
      (paid conversion: celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout.
      Use the result of "Find people who just got value", "Write three follow up emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Track activation and retention
    summary: >-
      What share of signups reach the activation event, how long it takes them, and how their 30 day retention
      compares with people who never got there or never went through this follow up.
    builds: dashboard
    description: >-
      Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation
      rate: target depends on product, but trend matters more than absolute), time-from-signup-to-aha
      distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers?:
      this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare
      30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn't (typical
      lift: 10-20% retention improvement). Use the result of "Find people who just got value", "Write
      three follow up emails", "Send on days 1, 5 and 10".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Aha moment reinforcement

Follows up right after someone hits the action that predicts retention, so the first win turns into a habit instead of a one off.

## Steps

1. **Find people who just got value** (builds segment)

   Anyone who completed your activation event in the last 14 days and has not been through this follow up yet. Your product team picks that event off the retention curve, for example first message sent or first project published.

2. **Write three follow up emails** (builds email_html)

   One that congratulates them and shows what others did after the same milestone, one that points to the natural next feature with a how to and a deep link, and one that shows how power users go further.

3. **Send on days 1, 5 and 10** (builds journey)

   Starts when the activation event fires, with emails on day 1, day 5 and day 10. If they find the next feature on their own by day 5, the middle email is skipped and they go straight to the power user one. They leave if they start paying, unsubscribe, or after 14 days.

4. **Track activation and retention** (builds dashboard)

   What share of signups reach the activation event, how long it takes them, and how their 30 day retention compares with people who never got there or never went through this follow up.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The feature_first_used event in your project

Writes:

- A new segment, from step 1 "Find people who just got value"
- A new designed email, from step 2 "Write three follow up emails"
- A new journey, from step 3 "Send on days 1, 5 and 10"
- A new dashboard, from step 4 "Track activation and retention"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
