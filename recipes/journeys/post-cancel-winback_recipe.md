---
name: post-cancel-winback
description: Use when a user mentions "post-cancel winback", "after cancel winback", "30/60/90 day winback sequence", or asks for related help. After a user cancels, fire a 30/60/90-day winback sequence, staggered re-engagement at increasing intervals with product updates, win-back incentives, and a final 'one last try' message, to recover formerly-paying customers.
arguments: []
intempt:
  id: post-cancel-winback
  title: "Win back after cancellation"
  version: 1.0.0
  slashCommand: /post-cancel-winback
  group: Journeys
  shortDescription: "Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [winback, post-cancel, lapsed-customer]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: subscription_canceled, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find recent cancellations"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "People who cancelled between 30 and 120 days ago, unless the reason was wrong fit or the company shutting down. Anyone who has already resubscribed or asked for no marketing is left out."
      prompt: Build a segment 'Recently cancelled - last 120 days' capturing users who canceled their subscription 30 to 120 days ago AND whose cancel reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form.
    - step: 2
      title: "Write three win back emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "Day 30 leads with two or three improvements shipped since they left, matched to why they went. Day 60 offers 50% off for a set number of months, tied to how they used to work. Day 90 is softer: it accepts they had a reason and offers a free 30 day reactivation with no charge until they confirm. From their old CSM where there was one."
      prompt: 'Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): ''A lot has changed since you left: here''s what''s new.'' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): ''Come back for [N] months at 50% off'': winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): ''One last invitation'' (softer, more emotional appeal) acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address.'
    - step: 3
      title: "Send at 30, 60 and 90 days"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: "Three emails counted from the cancellation, each using their old plan, their stated reason and the features they last used. They leave when they resubscribe, when they reply, on unsubscribe, or after 120 days, when they move to long term lapsed nurture."
      prompt: 'Build a 3-touch journey triggered when the subscription was canceled 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: Subscription started (won back: record a winback-won event), Email replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion).'
    - step: 4
      title: "See who comes back"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: "The share of cancellations that resubscribe within 90 days, which email drives it, which reasons for leaving are recoverable, the ARR recovered this quarter, and how long people take to return."
      prompt: 'Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days: baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Win back after cancellation

Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops.

## Before you run it

- Send the `subscription_canceled` event

## What it does

1. **Find recent cancellations** (`create_segment`)

   People who cancelled between 30 and 120 days ago, unless the reason was wrong fit or the company shutting down. Anyone who has already resubscribed or asked for no marketing is left out.

2. **Write three win back emails** (`create_email_content`)

   Day 30 leads with two or three improvements shipped since they left, matched to why they went. Day 60 offers 50% off for a set number of months, tied to how they used to work. Day 90 is softer: it accepts they had a reason and offers a free 30 day reactivation with no charge until they confirm. From their old CSM where there was one.

3. **Send at 30, 60 and 90 days** (`create_journey`)

   Three emails counted from the cancellation, each using their old plan, their stated reason and the features they last used. They leave when they resubscribe, when they reply, on unsubscribe, or after 120 days, when they move to long term lapsed nurture.

4. **See who comes back** (`create_dashboard`)

   The share of cancellations that resubscribe within 90 days, which email drives it, which reasons for leaving are recoverable, the ARR recovered this quarter, and how long people take to return.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
