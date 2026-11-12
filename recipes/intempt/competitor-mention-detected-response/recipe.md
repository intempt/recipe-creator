---
frontmatter_id: competitor-mention-detected-response
slash_command: /competitor-mention-detected-response
description: Uses AI attribute scores from first-party events to spot competitive intent and trigger a personalized email plus a CSM follow-up task.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Spots competitor interest from first-party signals and responds with an intent-matched email, in-app capability
    prompts, and a CSM follow-up task, plus a competitive win/loss dashboard.
  parameters:
  - name: signal_window
    type: duration
    label: Recent signal window for segment
    default: 14 d
    required: false
  - name: attribute_active_window
    type: duration
    label: How long the competitor signal stays active after last signal
    default: 30 d
    required: false
  - name: min_signal_strength
    type: enum
    label: Minimum signal strength for segment
    default: medium
    required: false
    options:
    - medium
    - high
  - name: csm_task_delay
    type: duration
    label: Delay before CSM/AE task for high-signal accounts
    default: 2 d
    required: false
  - name: exec_outreach_delay
    type: duration
    label: Delay before executive-sponsor outreach
    default: 7 d
    required: false
  - name: first_response_window
    type: duration
    label: Target time to first email after signal
    default: 4 h
    required: false
  - name: product_name
    type: string
    label: Your product name
    default: <UNKNOWN>
    required: false
  - name: cooldown_timeout
    type: duration
    label: Exit timeout with no further competitor signal
    default: 30 d
    required: false
  requirements:
  - slot: competitor_signal_attribute
    kind: attribute
    meaning: An AI-derived attribute on users or accounts that records competitor signals with competitor name, signal type,
      signal strength, recency and inferred intent.
    properties:
    - name: competitor_name
      type: string
      meaning: Name of the competitor the signal refers to
      optional: false
    - name: signal_type
      type: string
      meaning: Kind of signal such as comparison page visit, competitor link click, support mention, resource download, or
        review site activity
      optional: false
    - name: signal_strength
      type: enum
      meaning: 'Strength of the competitor signal: low, medium or high'
      optional: false
    - name: recency
      type: date
      meaning: When the most recent competitor signal occurred
      optional: false
    - name: inferred_intent
      type: enum
      meaning: 'Inferred intent: evaluation, dissatisfaction, curious-comparison or leaving'
      optional: false
  - slot: competitor_signal_event
    kind: event
    meaning: A customer or prospect showed a competitor comparison or competitor-related action on first-party channels.
    properties:
    - name: competitor_name
      type: string
      meaning: Competitor referenced by the action
      optional: true
    - name: signal_type
      type: string
      meaning: Kind of competitor action observed
      optional: true
  - slot: active_competitor_signal_segment
    kind: segment
    meaning: Existing customers or late-stage prospects with a recent competitor signal of medium or high strength.
    creatable: true
    definition: users/accounts with {competitor_signal_attribute} in the last {signal_window} where signal_strength is at
      least {min_signal_strength}, excluding brand-new prospects
  - slot: cancel_page_visit_event
    kind: event
    meaning: A customer visited the cancellation page of the product.
  - slot: customer_success_owner
    kind: attribute
    meaning: The CSM or AE assigned to the account, used as the sender and task owner.
  - slot: account_arr
    kind: attribute
    meaning: Annual recurring revenue of the account.
  - slot: email_channel
    kind: destination
    meaning: An email sending channel the project uses to send marketing emails.
    channel: email
  - slot: in_app_recommendation_surface
    kind: destination
    meaning: An in-app surface that can show product recommendations to users.
    channel: email
  - slot: product_usage_feed
    kind: attribute
    meaning: Feature usage profile and cohort data for each user or account.
  - slot: crm_task_integration
    kind: integration
    meaning: A connected CRM where CSM or AE follow-up tasks can be created with attached competitive intel.
    channel: salesforce
  steps:
  - id: s1
    builds: attribute
    uses:
    - competitor_signal_attribute
    - competitor_signal_event
    - attribute_active_window
    instruction: 'Create an AI-derived attribute {competitor_signal_attribute} on the user/account object. It detects: (a)
      visits to competitor comparison pages, (b) clicks on competitor-named links in marketing emails, (c) competitor mentions
      in support conversations or AI agent chats, (d) downloads of competitor-comparison resources, and (e) activity as a
      reviewer on a competitor''s review site where data permits. Output a structured object with competitor_name, signal_type,
      signal_strength, recency and inferred_intent (evaluation, dissatisfaction, curious-comparison or leaving). The attribute
      stays active for {attribute_active_window} after the last competitor signal.'
  - id: s2
    builds: segment
    uses:
    - s1
    - active_competitor_signal_segment
    - competitor_signal_attribute
    - signal_window
    - min_signal_strength
    instruction: 'Build the segment {active_competitor_signal_segment} of users/accounts with {competitor_signal_attribute}
      in the last {signal_window} where signal_strength is {min_signal_strength} or higher. Partition it by inferred_intent
      so each journey branch can respond differently. Exclude brand-new prospects: this motion is for existing customers or
      late-stage prospects only, since competitive intel for new prospects goes into the account executive''s sales process.'
  - id: s3
    builds: email
    uses:
    - s2
    - active_competitor_signal_segment
    - email_channel
    - customer_success_owner
    - product_name
    - competitor_signal_attribute
    - cancel_page_visit_event
    instruction: 'Write a designed HTML marketing email for each inferred_intent in {active_competitor_signal_segment}. Evaluation
      intent (existing customer comparing, concerning but not yet leaving): subject ''Helpful comparison: {product_name} vs
      {competitor_signal_attribute.competitor_name} from your team''s perspective''; give an honest comparison and specific
      advantages relevant to their use case. Dissatisfaction intent (friction signals plus competitor signal, leaving risk):
      subject ''Want to talk? [CSM name] would like to understand what''s not working''; make a direct outreach offer with
      no defensive product pitch. Curious-comparison intent (neutral exploration): subject ''Most teams who compare us to
      {competitor_signal_attribute.competitor_name} choose {product_name} for [specific differentiator]: here''s why''; include
      a customer case study. Leaving intent (strong signals plus cancel-page visit plus competitor signal): offer an executive
      business review meeting and open a retention discussion. Send from the matched {customer_success_owner} for high-signal
      cases; send from marketing for low-signal exploration.'
  - id: s4
    builds: recommendation
    uses:
    - s1
    - s2
    - in_app_recommendation_surface
    - product_usage_feed
    - competitor_signal_attribute
    - product_name
    - attribute_active_window
    instruction: Configure an in-app recommendation surface titled 'Capabilities you're not using yet' that activates when
      a user has an active {competitor_signal_attribute}. It pulls differentiator features of {product_name} that the user
      or account has not tried but that its cohort uses for high-value outcomes, answering 'why stay?' with concrete unused
      capability rather than feature-comparison documents. It renders in-app for {attribute_active_window}.
  - id: s5
    builds: automation
    uses:
    - s2
    - s3
    - s4
    - active_competitor_signal_segment
    - first_response_window
    - csm_task_delay
    - exec_outreach_delay
    - attribute_active_window
    - cooldown_timeout
    - crm_task_integration
    - customer_success_owner
    - product_usage_feed
    - account_arr
    - competitor_signal_attribute
    instruction: 'Build a journey on {active_competitor_signal_segment}, branched by inferred_intent. Touch 1, within {first_response_window}
      of the signal: send the intent-matched email from "Write a designed HTML marketing email for each inferred_intent".
      Touch 2, on the same day as touch 1: activate the "Capabilities you''re not using yet" surface for {attribute_active_window}.
      Touch 3, after {csm_task_delay}, only for high signal_strength accounts: create a task in {crm_task_integration} for
      the {customer_success_owner} with full competitor intel attached (competitor_name, signal_type, inferred_intent, suggested
      talking points, and the customer''s current usage profile from {product_usage_feed}). Touch 4, after {exec_outreach_delay},
      only if the account still shows competitive intent and has not engaged with the CSM: send an executive-sponsor outreach
      offer to high-ARR accounts, using {account_arr} to qualify. Exit when there is an explicit positive renewal or retention
      signal (saved), when the account churns (loss, to be fed into win-loss analysis), or after {cooldown_timeout} with no
      further competitor signal (signal cooled).'
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - competitor_signal_attribute
    - account_arr
    instruction: 'Compose a competitive defense dashboard with four views: competitor signal volume per competitor, showing
      which competitors are hottest in the current customer base for leadership; per-competitor save rate, showing which competitors
      the team saves customers from versus loses them to; inferred-intent distribution between evaluation and leaving as a
      leading churn indicator; and an ARR-weighted at-risk pile built from competitor signals using {account_arr}. The data
      feeds the product-marketing competitive-positioning function.'
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
