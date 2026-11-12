---
frontmatter_id: cart-recovery
slash_command: /cart-recovery
description: Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails shoppers who left items in their cart three times over three days, then reports how much revenue is recovered
    and alerts the team if recovery drops.
  parameters:
  - name: abandon_window
    type: duration
    label: Lookback window for abandoned carts
    default: 30 d
    required: false
  - name: touch1_delay
    type: duration
    label: Delay before first email
    default: 1 h
    required: false
  - name: touch2_delay
    type: duration
    label: Delay before second email
    default: 24 h
    required: false
  - name: touch3_delay
    type: duration
    label: Delay before third email
    default: 72 h
    required: false
  - name: alert_threshold
    type: number
    label: Recovery rate alert threshold (percent)
    default: 15
    required: false
  - name: alert_window
    type: duration
    label: Window for recovery rate check
    default: 7 d
    required: false
  - name: brand_tone
    type: string
    label: Brand voice for emails
    default: brand voice
    required: false
  requirements:
  - slot: abandoned_cart_event
    kind: event
    meaning: A customer abandoned a cart without placing an order
    properties:
    - name: cart_id
      type: string
      meaning: Identifier of the abandoned cart
      optional: false
  - slot: order_event
    kind: event
    meaning: A customer completed an order
    properties:
    - name: cart_id
      type: string
      meaning: Identifier of the cart the order came from
      optional: true
  - slot: cart_abandoners_segment
    kind: segment
    meaning: Users who abandoned a cart in the last 30 days and have not placed an order for that cart
    creatable: true
    definition: users who did {abandoned_cart_event} in the last {abandon_window} and did not do {order_event} for that cart
  - slot: email_channel
    kind: destination
    meaning: Email sending channel for recovery messages
    channel: email
  - slot: team_alert_channel
    kind: destination
    meaning: Channel used to alert the team when recovery drops
    optional: true
    channel: slack
  - slot: brand_voice
    kind: brand
    meaning: Brand voice and tone guidelines for written emails
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - abandoned_cart_event
    - order_event
    - abandon_window
    - cart_abandoners_segment
    instruction: Identify users with {abandoned_cart_event} in the last {abandon_window} who have NOT done {order_event} for
      that cart. Save as {cart_abandoners_segment}.
  - id: s2
    builds: email
    uses:
    - brand_voice
    - brand_tone
    - s1
    instruction: 'Write three cart-recovery emails in {brand_tone} using {brand_voice}, for the audience in "Identify users
      with abandoned cart". Touch 1: gentle reminder. Touch 2: urgency and social proof. Touch 3: final reminder with an optional
      discount.'
  - id: s3
    builds: automation
    uses:
    - cart_abandoners_segment
    - email_channel
    - touch1_delay
    - touch2_delay
    - touch3_delay
    - s1
    - s2
    instruction: Build a three-touch journey for {cart_abandoners_segment} that sends the emails from "Write three cart-recovery
      emails" through {email_channel} at {touch1_delay}, {touch2_delay}, and {touch3_delay} after abandonment.
  - id: s4
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    instruction: Add A/B variants to the recovery journey from "Schedule the sequence" testing subject lines and incentive
      levels, sent to the audience from "Identify users with abandoned cart".
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    instruction: Create a dashboard for the journey in "Schedule the sequence" showing recovery rate, revenue recovered, and
      time-to-recover, including results from "Test subject lines and offers".
  - id: s6
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - alert_threshold
    - alert_window
    - team_alert_channel
    instruction: Create a workflow that alerts the team on {team_alert_channel} when the recovery rate from the dashboard
      in "Compose a dashboard showing recovery rate" drops below {alert_threshold} percent over a {alert_window} window.
---

# Abandoned cart recovery

Slash command: /cart-recovery

## Step 1: Find who abandoned a cart

This step builds a segment.
Identify users with Abandoned cart event in last 30 days who have NOT placed an order for that cart.

## Step 2: Write the three emails

Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. Use the result of "Find who abandoned a cart".

## Step 3: Schedule the sequence

Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. Use the result of "Find who abandoned a cart", "Write the three emails".

## Step 4: Test subject lines and offers

Add A/B variants on subject lines and incentive levels for the recovery journey. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence".

## Step 5: Track recovered revenue

Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence", "Test subject lines and offers".

## Step 6: Alert when it stops working

Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence", "Test subject lines and offers", "Track recovered revenue".
