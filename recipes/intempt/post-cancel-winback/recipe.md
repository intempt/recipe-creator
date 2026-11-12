---
frontmatter_id: post-cancel-winback
slash_command: /post-cancel-winback
description: Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Wins back customers who cancelled at 30, 60 and 90 days with product updates, a 50% discount, and a free trial
    month, then tracks recoveries.
  parameters:
  - name: discount_percent
    type: number
    label: Winback discount percent
    default: 50
    required: false
  - name: discount_months
    type: number
    label: Number of months the discount applies
    default: 3
    required: false
  - name: free_trial_days
    type: number
    label: Free reactivation trial length (days)
    default: 30
    required: false
  - name: lookback_window
    type: duration
    label: Cancellation lookback window
    default: 120 d
    required: false
  - name: min_days_since_cancel
    type: duration
    label: Earliest days after cancel to start outreach
    default: 30 d
    required: false
  - name: timeout_window
    type: duration
    label: Days after cancel before moving to long-term lapsed nurture
    default: 120 d
    required: false
  - name: winback_window
    type: duration
    label: Window used to measure winback rate
    default: 90 d
    required: false
  requirements:
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer's subscription was canceled
    properties:
    - name: cancel_reason
      type: string
      meaning: The reason the customer gave when cancelling
      optional: false
    - name: plan
      type: string
      meaning: The subscription plan that was canceled
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started or restarted a subscription
  - slot: email_replied_event
    kind: event
    meaning: A customer replied to an email
  - slot: unsubscribed_event
    kind: event
    meaning: A customer unsubscribed from marketing emails
  - slot: winback_won_event
    kind: event
    meaning: A customer was won back after cancelling; recorded by this recipe
    optional: true
  - slot: no_marketing_request
    kind: attribute
    meaning: A customer explicitly requested no marketing messages in the cancellation form
  - slot: recently_cancelled_segment
    kind: segment
    meaning: Customers who cancelled recently, excluding those who gave a non-recoverable reason or have already won back
    creatable: true
    definition: users who did {subscription_canceled_event} between {min_days_since_cancel} and {lookback_window} ago, where
      {subscription_canceled_event.cancel_reason} is not 'wrong-fit' or 'company-shutdown', excluding users who did {subscription_started_event}
      after the cancellation and users with {no_marketing_request}
  - slot: sending_account_owner
    kind: attribute
    meaning: The customer's original customer success manager, if known
    optional: true
  - slot: success_sender
    kind: integration
    meaning: A sending address for the success team used when no original CSM is known
    channel: email
  - slot: prior_use_case
    kind: attribute
    meaning: The customer's prior use case, if known
    optional: true
  - slot: last_used_features
    kind: attribute
    meaning: Features the customer last used before cancelling
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - recently_cancelled_segment
    - subscription_canceled_event
    - subscription_started_event
    - no_marketing_request
    - min_days_since_cancel
    - lookback_window
    instruction: 'Build the segment {recently_cancelled_segment}: users who did {subscription_canceled_event} between {min_days_since_cancel}
      and {lookback_window} ago, where {subscription_canceled_event.cancel_reason} is not ''wrong-fit'' or ''company-shutdown''.
      Exclude users who did {subscription_started_event} after the cancellation and users with {no_marketing_request}.'
  - id: s2
    builds: email
    uses:
    - s1
    - sending_account_owner
    - success_sender
    - prior_use_case
    - discount_percent
    - discount_months
    - free_trial_days
    instruction: 'Write three winback emails for the segment from "Find recent cancellations". Touch 1 (sent at {min_days_since_cancel}
      after cancel), subject ''A lot has changed since you left: here''s what''s new.'': lead with 2 to 3 specific product
      improvements shipped after the cancellation, matched to {subscription_canceled_event.cancel_reason}. Touch 2 (sent at
      60 days after cancel), subject ''Come back for {discount_months} months at {discount_percent}% off'': present the winback
      discount and personalize the call-out with {prior_use_case} when known. Touch 3 (sent at 90 days after cancel, final),
      subject ''One last invitation'': a softer, more emotional message acknowledging they left for a reason, offering a free
      {free_trial_days}-day reactivation trial with no charge until they confirm, presented as the final offer. Send from
      {sending_account_owner} when known, otherwise from {success_sender}.'
  - id: s3
    builds: automation
    uses:
    - s2
    - subscription_canceled_event
    - subscription_started_event
    - winback_won_event
    - email_replied_event
    - unsubscribed_event
    - last_used_features
    - timeout_window
    instruction: 'Build a three-touch journey entering users with {subscription_canceled_event} fired 30 or more days earlier.
      Send touch 1 from "Write three winback emails" at day 30, touch 2 at day 60 and touch 3 at day 90, each personalized
      with {subscription_canceled_event.cancel_reason}, {subscription_canceled_event.plan} and {last_used_features}. Exit
      on any of: {subscription_started_event} (record {winback_won_event}), {email_replied_event} (warm handoff to sales),
      {unsubscribed_event}, or {timeout_window} after cancel (then hand the user to the long-term lapsed nurture, a separate
      motion).'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - winback_won_event
    - subscription_canceled_event
    - winback_window
    instruction: 'Build a winback dashboard for the segment from "Find recent cancellations" and the journey from "Send at
      30, 60 and 90 days" showing: winback rate (percent of cancellers who re-subscribe within {winback_window}; benchmark
      5 to 10 percent); winback rate by touch; winback rate by original {subscription_canceled_event.cancel_reason}; ARR recovered
      through winback this quarter; and time-to-winback distribution. Note that most winbacks typically occur within the first
      60 days and users dormant 90+ days rarely return without a major external trigger.'
---

# Win back after cancellation

Slash command: /post-cancel-winback

## Step 1: Find recent cancellations

Build a segment 'Recently cancelled - last 120 days' capturing users with Subscription canceled in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form.

## Step 2: Write three win back emails

Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): 'A lot has changed since you left: here's what's new.' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): 'Come back for [N] months at 50% off': winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): 'One last invitation' (softer, more emotional appeal) acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address. Use the result of "Find recent cancellations".

## Step 3: Send at 30, 60 and 90 days

Build a 3-touch journey triggered when Subscription canceled fired 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: Subscription started (won back: record winback_won event), email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion). Use the result of "Find recent cancellations", "Write three win back emails".

## Step 4: See who comes back

Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days: baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger). Use the result of "Find recent cancellations", "Write three win back emails", "Send at 30, 60 and 90 days".
