---
frontmatter_id: pre-cancellation-save
slash_command: /pre-cancellation-save
description: Catches people who open the cancel flow but have not finished it, and answers the reason they gave with a pause, a downgrade, a discount or a call.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Catches customers who open the cancel flow but do not finish it, and answers their stated reason with a matched
    save offer (pause, downgrade, discount or call).
  parameters:
  - name: cancel_window
    type: duration
    label: Lookback window for cancel-page visits
    default: 14 d
    required: false
  - name: signal_expiry
    type: duration
    label: Cancel intent signal expiry after no activity
    default: 7 d
    required: false
  - name: save_cooldown
    type: duration
    label: Cooldown since last cancel-save offer
    default: 90 d
    required: false
  - name: retention_discount_percent
    type: number
    label: Retention discount percent (price reason)
    default: 20
    required: false
  - name: retention_discount_months
    type: number
    label: Retention discount duration in months
    default: 3
    required: false
  - name: pause_duration_days
    type: number
    label: Maximum pause length in days (pause reason)
    default: 60
    required: false
  - name: max_pause_days
    type: number
    label: Maximum one-click pause length in days (pause-needed reason)
    default: 90
    required: false
  - name: followup_delay
    type: duration
    label: Delay before follow-up touch
    default: 2 d
    required: false
  - name: journey_timeout
    type: duration
    label: Journey timeout without save or cancel
    default: 14 d
    required: false
  - name: save_measure_window
    type: duration
    label: Window to check whether user cancels after intent
    default: 30 d
    required: false
  - name: high_ltv_percentile
    type: number
    label: Top ARR percentile treated as high-LTV
    default: 10
    required: false
  - name: brand_tone
    type: enum
    label: Email tone
    default: warm
    required: false
    options:
    - warm
    - direct
    - formal
  requirements:
  - slot: cancel_flow_visit
    kind: event
    meaning: A customer visited the cancel or downgrade page
    properties:
    - name: page
      type: text
      meaning: Page path visited
      optional: false
  - slot: cancel_button_click
    kind: event
    meaning: A customer clicked the cancel subscription button and opened the cancel modal
  - slot: cancel_reason_submitted
    kind: event
    meaning: A customer submitted a cancel reason in the cancel flow without confirming cancellation
    properties:
    - name: reason
      type: enum
      meaning: 'Stated cancel reason: price, unused, competitor, feature-gap, pause-needed, or other'
      optional: false
  - slot: subscription_canceled
    kind: event
    meaning: A customer's subscription was canceled
  - slot: save_offer_accepted
    kind: event
    meaning: A customer accepted a cancel-save offer
  - slot: cancel_intent_signal
    kind: attribute
    meaning: A real-time user attribute holding cancel intent level and stated reason
    properties:
    - name: intent_level
      type: enum
      meaning: browsing, interacting, or committing
      optional: false
    - name: stated_reason
      type: text
      meaning: Stated cancel reason if captured
      optional: true
    - name: timestamp
      type: date
      meaning: When the intent level was last updated
      optional: false
  - slot: paying_subscriber_status
    kind: attribute
    meaning: Whether a user is a paying subscriber with an active subscription, not on trial
  - slot: cancel_offer_sent_history
    kind: attribute
    meaning: The date a user last received a cancel-save offer
  - slot: arr_value
    kind: attribute
    meaning: Annual recurring revenue of a customer, used to rank top-decile accounts
  - slot: cancel_intent_active_segment
    kind: segment
    meaning: Paying customers with active subscriptions who are interacting or committing to cancel and have not recently
      received a save offer
    creatable: true
    definition: users who are paying with an active subscription, where cancel_intent_signal.intent_level is interacting or
      committing, and who have not received a cancel-save offer in the last {save_cooldown}, excluding trial users
  - slot: retention_win_event
    kind: event
    meaning: A customer accepted a save offer and was recorded as a retention win
  - slot: customer_success_manager
    kind: attribute
    meaning: The customer's assigned customer success manager, if any
    optional: true
  - slot: success_mailbox
    kind: integration
    meaning: Shared customer success email sender used when no manager is assigned
    channel: email
  - slot: csm_task_destination
    kind: destination
    meaning: Task system where urgent customer success tasks are created for high-value accounts
    optional: true
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - cancel_flow_visit
    - cancel_button_click
    - cancel_reason_submitted
    - cancel_window
    - signal_expiry
    instruction: 'Create an AI-derived real-time attribute {cancel_intent_signal} on the user record. Inputs: (a) visited
      a cancel or downgrade page in the last {cancel_window}; (b) clicked the cancel subscription button, which opens the
      cancel modal but does not cancel; (c) submitted a cancel reason in the cancel flow without confirming. Output an object
      with intent_level (browsing, interacting, committing), stated_reason if captured (price, unused, competitor, feature-gap,
      pause-needed, other), and timestamp. The signal expires after {signal_expiry} with no further activity.'
  - id: s2
    builds: segment
    uses:
    - cancel_intent_signal
    - paying_subscriber_status
    - cancel_offer_sent_history
    - cancel_intent_active_segment
    - save_cooldown
    - s1
    instruction: 'Build segment {cancel_intent_active_segment}: paying users whose {cancel_intent_signal.intent_level} is
      interacting or committing and whose subscription is still active and not yet canceled. Exclude users on trial and users
      who received a cancel-save offer in the last {save_cooldown}. Canceled users move to the post-cancel winback flow instead.'
  - id: s3
    builds: email
    uses:
    - brand_tone
    - retention_discount_percent
    - retention_discount_months
    - pause_duration_days
    - max_pause_days
    - customer_success_manager
    - success_mailbox
    - s1
    - s2
    instruction: 'Design one HTML save-offer email per stated reason, in a {brand_tone} tone. Price: offer a {retention_discount_percent}%
      retention discount for {retention_discount_months} months, or a option to downgrade to a lighter plan. Unused: offer
      a pause of up to {pause_duration_days} days, or a 1:1 onboarding call to drive activation. Competitor: offer a 1:1 call
      with a product manager to address feature gaps, plus a competitive comparison sheet. Feature-gap: share roadmap visibility
      for the specific missing feature plus an interim workaround. Pause-needed: offer a one-click pause of up to {max_pause_days}
      days that preserves data. Other or no reason: ask what would have made the customer stay, and offer a 1:1 call. Send
      from the customer''s assigned customer success manager if one exists, otherwise from the shared success mailbox.'
  - id: s4
    builds: automation
    uses:
    - cancel_intent_signal
    - arr_value
    - high_ltv_percentile
    - csm_task_destination
    - followup_delay
    - save_offer_accepted
    - retention_win_event
    - subscription_canceled
    - journey_timeout
    - s1
    - s2
    - s3
    instruction: 'Build a journey triggered when {cancel_intent_signal.intent_level} becomes interacting or committing. Branch
      on {cancel_intent_signal.stated_reason} so each user gets one save offer matched to their reason, using the emails from
      "Write one offer per reason". Touch 1: send the matched save-offer email within 1 hour of the intent signal. Touch 2:
      after {followup_delay} with no engagement, send a softer follow-up reinforcing the same offer. For customers in the
      top {high_ltv_percentile}% by {arr_value}, also create an urgent task in {csm_task_destination} at intent detection
      so a human save attempt runs in parallel with the email. Record accepted offers as {retention_win_event} when {save_offer_accepted}
      fires. Exit on save offer accepted, on {subscription_canceled} (hand off to post-cancel winback), or after {journey_timeout}.'
  - id: s5
    builds: dashboard
    uses:
    - cancel_intent_signal
    - save_measure_window
    - retention_win_event
    - arr_value
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build a save-flow dashboard showing: cancel-intent volume by week; save rate (intent users who do not cancel
      within {save_measure_window}); save rate by stated reason; save rate by offer type (discount, pause, downgrade, 1:1
      call); ARR saved this quarter from {retention_win_event}. Also show the distribution of stated cancel reasons, and cohorts
      where save attempts fail consistently, flagged as a product-fix signal rather than a save-offer problem.'
---

# Save them before they cancel

Slash command: /pre-cancellation-save

## Step 1: Catch cancel intent live

Create an AI-derived attribute 'cancel_intent_signal' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked 'cancel subscription' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity.

## Step 2: Find who is halfway out

Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled, once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam). Use the result of "Catch cancel intent live".

## Step 3: Write one offer per reason

This step builds a designed marketing email (HTML).
Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask 'what would have made you stay?' + offer 1:1 call. Send-from: the customer's CSM if assigned, else success@ address. Use the result of "Catch cancel intent live", "Find who is halfway out".

## Step 4: Make one matched offer

Build a branched journey triggered when cancel_intent_signal becomes 'interacting' or 'committing'. Branch on stated_reason: each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection: human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), Subscription canceled (proceed to post-cancel-winback), or 14-day timeout. Use the result of "Catch cancel intent live", "Find who is halfway out", "Write one offer per reason".

## Step 5: See which saves actually work

Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON'T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call: informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal: those segments need product fixes, not save offers). Use the result of "Catch cancel intent live", "Find who is halfway out", "Write one offer per reason", "Make one matched offer".
