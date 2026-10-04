---
id: post-cancel-winback
title: Win back after cancellation
slash_command: /post-cancel-winback
group: Journeys
owner: intempt
curator: somya
summary: Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and
  a free month, then stops.
description: >-
  After a user cancels, fire a 30/60/90-day winback sequence, staggered re-engagement at increasing intervals
  with product updates, win-back incentives, and a final 'one last try' message, to recover formerly-paying
  customers.
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
    - winback
    - post-cancel
    - lapsed-customer
prerequisites:
  events:
    - value: subscription_canceled
      severity: blocking
touches:
  reads:
    - The subscription_canceled event in your project
  writes:
    - A new segment, from step 1 "Find recent cancellations"
    - A new designed email, from step 2 "Write three win back emails"
    - A new journey, from step 3 "Send at 30, 60 and 90 days"
    - A new dashboard, from step 4 "See who comes back"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find recent cancellations
    summary: >-
      People who cancelled between 30 and 120 days ago, unless the reason was wrong fit or the company
      shutting down. Anyone who has already resubscribed or asked for no marketing is left out.
    builds: segment
    description: >-
      Build a segment 'Recently cancelled - last 120 days' capturing users with subscription_canceled
      in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't
      winback). Excludes users who have already won back (subscribed again) and users who explicitly requested
      no-marketing in cancel form.
  - id: s2
    title: Write three win back emails
    summary: >-
      Day 30 leads with two or three improvements shipped since they left, matched to why they went. Day
      60 offers 50% off for a set number of months, tied to how they used to work. Day 90 is softer: it
      accepts they had a reason and offers a free 30 day reactivation with no charge until they confirm.
      From their old CSM where there was one.
    builds: email_html
    description: >-
      Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): 'A lot has changed since
      you left: here's what's new.' Lead with 2-3 specific product improvements shipped post-cancel, relevant
      to their stated cancel reason. Touch 2 (Day 60): 'Come back for [N] months at 50% off': winback
      discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final):
      'One last invitation' (softer, more emotional appeal) acknowledges you understand they left for
      a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever.
      Send-from: their original CSM if known, else success@ address. Use the result of "Find recent cancellations".
    dependsOn:
      - s1
  - id: s3
    title: Send at 30, 60 and 90 days
    summary: >-
      Three emails counted from the cancellation, each using their old plan, their stated reason and the
      features they last used. They leave when they resubscribe, when they reply, on unsubscribe, or after
      120 days, when they move to long term lapsed nurture.
    builds: journey
    description: >-
      Build a 3-touch journey triggered when subscription_canceled fired 30+ days ago. Touch 1: Day 30.
      Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel
      reason, plan, last-used features). Exit on: subscription_created (won back: record winback_won event),
      email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to
      long-term lapsed nurture, separate motion). Use the result of "Find recent cancellations", "Write
      three win back emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: See who comes back
    summary: >-
      The share of cancellations that resubscribe within 90 days, which email drives it, which reasons
      for leaving are recoverable, the ARR recovered this quarter, and how long people take to return.
    builds: dashboard
    description: >-
      Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90
      days: baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries),
      winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered
      via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60
      days; users dormant 90+ days rarely return without a major external trigger). Use the result of
      "Find recent cancellations", "Write three win back emails", "Send at 30, 60 and 90 days".
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

# Win back after cancellation

Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops.

## Steps

1. **Find recent cancellations** (builds segment)

   People who cancelled between 30 and 120 days ago, unless the reason was wrong fit or the company shutting down. Anyone who has already resubscribed or asked for no marketing is left out.

2. **Write three win back emails** (builds email_html)

   Day 30 leads with two or three improvements shipped since they left, matched to why they went. Day 60 offers 50% off for a set number of months, tied to how they used to work. Day 90 is softer: it accepts they had a reason and offers a free 30 day reactivation with no charge until they confirm. From their old CSM where there was one.

3. **Send at 30, 60 and 90 days** (builds journey)

   Three emails counted from the cancellation, each using their old plan, their stated reason and the features they last used. They leave when they resubscribe, when they reply, on unsubscribe, or after 120 days, when they move to long term lapsed nurture.

4. **See who comes back** (builds dashboard)

   The share of cancellations that resubscribe within 90 days, which email drives it, which reasons for leaving are recoverable, the ARR recovered this quarter, and how long people take to return.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The subscription_canceled event in your project

Writes:

- A new segment, from step 1 "Find recent cancellations"
- A new designed email, from step 2 "Write three win back emails"
- A new journey, from step 3 "Send at 30, 60 and 90 days"
- A new dashboard, from step 4 "See who comes back"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
