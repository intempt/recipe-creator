---
frontmatter_id: friction-point-detected-intervention
slash_command: /friction-point-detected-intervention
description: Detects friction from behavioral signals, segments those users, and sends email, SMS, push, or Slack follow- ups through a journey. Reply-agent adds 3-way sentiment tags to replies for triage.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Detects where users get stuck in the product and rescues them with in-app help, a tutorial email, an offer of agent-led
    walkthrough, and graduated escalation, plus a friction dashboard.
  parameters:
  - name: friction_window
    type: duration
    label: Lookback window for active friction signals
    default: 7 d
    required: false
  - name: abandon_return_hours
    type: number
    label: Hours without return that counts as an abandoned setup step
    default: 24
    required: false
  - name: repeat_attempt_threshold
    type: number
    label: Failed attempts on same element that count as repeated failure
    default: 3
    required: false
  - name: email_delay
    type: duration
    label: Delay before email fallback
    default: 4 h
    required: false
  - name: escalation_delay
    type: duration
    label: Delay before agent or CSM escalation
    default: 24 h
    required: false
  - name: dismiss_limit
    type: number
    label: Help dismissals before stopping help
    default: 3
    required: false
  - name: help_tone
    type: enum
    label: Tone of help content
    default: helpful_colleague
    required: false
    options:
    - helpful_colleague
    - neutral
    - concise
  requirements:
  - slot: friction_signal_attribute
    kind: attribute
    meaning: An AI-derived user attribute holding the detected friction type, friction location, severity and recommended
      intervention
    properties:
    - name: friction_type
      type: string
      meaning: Kind of friction detected
      optional: false
    - name: friction_location
      type: string
      meaning: Where in the product the user is stuck
      optional: false
    - name: severity
      type: enum
      meaning: Mild, moderate or severe friction level
      optional: false
    - name: recommended_intervention
      type: string
      meaning: Suggested intervention for this friction
      optional: true
  - slot: product_usage_event
    kind: event
    meaning: A customer performed an action or hit an error inside the product (form submits, button clicks, errors, help
      views, back-button or rage-click patterns, setup step starts and completions)
    properties:
    - name: element
      type: string
      meaning: UI element the action happened on
      optional: true
    - name: location
      type: string
      meaning: Product location of the action
      optional: true
    - name: outcome
      type: string
      meaning: Whether the action succeeded or failed
      optional: true
  - slot: active_friction_segment
    kind: segment
    meaning: Users with recent friction at moderate or severe level, excluding users already in active intervention
    creatable: true
    definition: users with recent_friction_signal in the last {friction_window} where severity is moderate or severe, excluding
      users already in active intervention, real-time refresh
  - slot: in_app_messaging
    kind: destination
    meaning: A destination that can deliver in-app help and emails to users
    channel: email
  - slot: sms_channel
    kind: integration
    meaning: An SMS integration for sending messages to users
    optional: true
    channel: sms
  - slot: push_channel
    kind: integration
    meaning: A push notification integration for sending messages to users
    optional: true
    channel: push
  - slot: slack_channel
    kind: integration
    meaning: A Slack integration for internal alerts or customer messages
    optional: true
    channel: slack
  - slot: support_agent
    kind: integration
    meaning: An AI agent that can chat with users and hand off to human support
    channel: email
  - slot: crm_tasks
    kind: integration
    meaning: A CRM where CSM outreach tasks can be created for high-value users
    optional: true
    channel: hubspot
  - slot: high_value_flag
    kind: attribute
    meaning: A user attribute marking high-value accounts
    optional: true
  - slot: product_brand
    kind: brand
    meaning: The company brand voice and product name used in messages
  - slot: help_content_library
    kind: knowledge
    meaning: Product help articles and tutorial videos for common blockers
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - friction_signal_attribute
    - product_usage_event
    - abandon_return_hours
    - repeat_attempt_threshold
    instruction: 'Create an AI-derived attribute {friction_signal_attribute} on the User object, refreshed in real time. Detect
      these patterns: (a) repeated failed actions on the same UI element ({repeat_attempt_threshold}+ attempts at the same
      form or button within a session); (b) abandoned setup step (multi-step flow started, not completed, no return for {abandon_return_hours}+
      hours); (c) error events without a subsequent successful retry; (d) help-content visits without a subsequent action;
      (e) rage-click or rapid back-button patterns. Output a structured object with friction_type, friction_location (where
      in the product), severity (mild, moderate or severe based on time stuck and repetition), and recommended_intervention.'
  - id: s2
    builds: segment
    uses:
    - s1
    - active_friction_segment
    - friction_signal_attribute
    - friction_window
    instruction: Build the segment {active_friction_segment} of users with {friction_signal_attribute} in the last {friction_window}
      where severity is moderate or severe. Refresh in real time. Exclude users already in active intervention from this journey.
      Partition by friction_location so the journey routes contextually.
  - id: s3
    builds: page
    uses:
    - s1
    - s2
    - friction_signal_attribute
    - help_content_library
    - help_tone
    instruction: 'Generate in-app contextual help variants per {friction_signal_attribute.friction_location}. Setup abandonment:
      contextual tooltip at the abandoned step with the answer to the common blocker. Repeated failed action: floating help
      bubble reading ''Looks like you''re stuck: here''s what most users do'' with a GIF or short video. Error encountered:
      helpful error explainer rendered where the error appeared. Long dwell time on a critical step (decision paralysis):
      comparison guide or recommendation card. Each renders mid-session when friction is freshest. Tone: {help_tone}, not
      aggressive sales. Draw content from {help_content_library} where relevant.'
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - s3
    - friction_signal_attribute
    - help_content_library
    - product_brand
    instruction: 'Generate email fallback content sent if the user does not engage with the in-app help from ''Help them inside
      the app'' or left the session before help was shown. Create variants per {friction_signal_attribute.friction_location}.
      Subject directly addresses the issue, for example ''Stuck on [specific step]? Here''s the fix.'' Body is a 60-second
      tutorial (video link or step-by-step screenshots) with a one-click resume-where-you-left-off deep link. Tone: specific
      to the exact friction, not a generic ''we noticed you got stuck'' message. Brand: {product_brand}.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - support_agent
    - friction_signal_attribute
    instruction: 'Configure an AI agent scenario named ''Friction rescue'' that engages users with severe {friction_signal_attribute}
      who have not responded to ''Help them inside the app'' or ''Email the fix if that misses''. The agent opens by naming
      the specific friction, for example ''I see you''ve been working on [step]: happy to help walk through it'', and offers
      to: (a) co-pilot the action with screen-share or step-by-step chat guidance, (b) escalate to human support if the problem
      is technical or account-level, (c) flag the friction as a product bug for the engineering queue. The agent never claims
      to be human. Offer handoff to a human when the agent cannot resolve within 3 turns. Agent: {support_agent}.'
  - id: s6
    builds: automation
    uses:
    - s2
    - s3
    - s4
    - s5
    - active_friction_segment
    - friction_signal_attribute
    - email_delay
    - escalation_delay
    - dismiss_limit
    - high_value_flag
    - crm_tasks
    instruction: 'Build a graduated-escalation journey triggered when {friction_signal_attribute} becomes moderate or severe.
      Touch 1 (mid-session, immediate): in-app contextual help from ''Help them inside the app'' renders at the friction location.
      Touch 2 ({email_delay} later, if the user left without resolving): email fallback from ''Email the fix if that misses''
      with tutorial and resume link. Touch 3 ({escalation_delay} later, if friction signal is still active or the user has
      not returned): trigger the ''Friction rescue'' agent scenario from ''Offer to walk them through''; for severe-tier users
      flagged {high_value_flag}, create a CSM task in {crm_tasks} for direct outreach. Exit when the friction signal resolves
      (user completed the step), when the user dismisses help {dismiss_limit} times, or on unsubscribe. Audience: {active_friction_segment}.'
  - id: s7
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - s6
    - friction_signal_attribute
    - active_friction_segment
    instruction: 'Compose a friction intervention dashboard showing: top 10 friction locations by frequency (product-team
      priority signal for UX issues); in-app help dismiss rate (high suggests irrelevant help, low suggests useful help);
      friction-to-resolution rate by intervention touch to show which escalation level resolves friction; correlation between
      severe-tier friction and churn; and journey-attributed activation lift. Source fields come from {friction_signal_attribute},
      {active_friction_segment} and the touch results of ''Escalate if they stay stuck''.'
---

# Friction rescue

Slash command: /friction-point-detected-intervention

## Step 1: Detect where people get stuck

Create an AI-derived attribute 'recent_friction_signal' on the User object, refreshed in real-time. Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form / button within a session); (b) abandoned setup step (started a multi-step flow, didn't complete, didn't return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured object with friction_type, friction_location (where in product), severity (mild / moderate / severe based on time-stuck and repetition), and recommended_intervention.

## Step 2: Group by where they got stuck

Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last 7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active intervention from this journey (no double-poking). Partitions by friction_location so the journey routes contextually. Use the result of "Detect where people get stuck".

## Step 3: Help them inside the app

This step builds a page.
Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action: floating help bubble with 'Looks like you're stuck: here's what most users do' + GIF or short video. For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session when the friction is freshest. Tone: helpful colleague, not aggressive sales. Use the result of "Detect where people get stuck", "Group by where they got stuck".

## Step 4: Email the fix if that misses

Generate email fallback content sent if the user doesn't engage with the in-app help OR has left the session before help was shown. Variants per friction_location. Format: subject directly addresses the issue ('Stuck on [specific step]? Here's the fix.'), body is a 60-second tutorial (video link or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic 'we noticed you got stuck': specific to the exact friction. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app".

## Step 5: Offer to walk them through

Configure an AI agent scenario 'Friction rescue' that engages users with severe friction signal who haven't responded to in-app help OR email. Scenario: agent opens with awareness of the specific friction ('I see you've been working on [step]: happy to help walk through it'), offers to: (a) co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if the problem is technical/account-level, (c) flag the friction as a product bug for the engineering queue. Agent NEVER pretends to be human; handoff to human is offered when agent can't resolve in 3 turns. Use the result of "Detect where people get stuck", "Group by where they got stuck".

## Step 6: Escalate if they stay stuck

Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe. Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch 2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch 3 (24 hours later, if friction signal still active OR user hasn't returned): trigger agent scenario or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal resolves (user completed the step (success), user explicitly dismisses help 3 times (respect) don't pester), unsubscribe. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app", "Email the fix if that misses", "Offer to walk them through".

## Step 7: See where the product traps people

Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority signal: these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn: proves the intervention's necessity), and journey-attributed activation lift (does this play meaningfully move activation rate). The product team gets a free UX-research stream as a side effect. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app", "Email the fix if that misses", "Offer to walk them through", "Escalate if they stay stuck".
