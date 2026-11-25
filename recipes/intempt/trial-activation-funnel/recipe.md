---
frontmatter_id: trial-activation-funnel
slash_command: /trial-activation-funnel
description: 'Emails a weekly trial activation digest: how far trial users get through setup and core feature use before the
  trial ends, time to value, and which sources bring trials that activate.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly digest of how many new trial users return, finish setup, use the core feature and fully activate,
    by source, with warnings.
  parameters:
  - name: comparisonWindow
    type: duration
    label: Comparison period (prior period length)
    default: 14 d
    required: false
  - name: firstReturnWindow
    type: duration
    label: Window for first return session after trial start
    default: 24 h
    required: false
  - name: setupWindow
    type: duration
    label: Window for reaching setup goal after trial start
    default: 24 h
    required: false
  - name: fullActivationWindow
    type: duration
    label: Window for full activation after trial start
    default: 14 d
    required: false
  - name: setupRateThreshold
    type: number
    label: Flag if share of trials reaching setup within window is below (%)
    default: 50
    required: false
  - name: timeToValueThreshold
    type: duration
    label: Flag if median time from trial start to core feature exceeds
    default: 48 h
    required: false
  - name: lowActivationThreshold
    type: number
    label: Flag any source whose full activation rate is below (%)
    default: 15
    required: false
  - name: highActivationThreshold
    type: number
    label: Highlight sources whose full activation rate exceeds (%)
    default: 35
    required: false
  - name: setupJourneyId
    type: string
    label: Journey id of the setup milestone
    required: true
  - name: coreFeatureJourneyId
    type: string
    label: Journey id of the core feature milestone
    required: true
  - name: fullActivationJourneyId
    type: string
    label: Journey id of the full activation milestone
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: trial_started_event
    kind: event
    meaning: A customer started a subscription trial
    properties:
    - name: trial_start
      type: date
      meaning: When the trial started
      optional: false
    - name: trial_end
      type: date
      meaning: When the trial ends
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a journey goal in an onboarding journey
    properties:
    - name: journey_id
      type: text
      meaning: Identifier of the onboarding journey that emitted the goal
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source of the user's acquisition
  steps:
  - id: s1
    builds: automation
    uses:
    - trial_started_event
    - session_start_event
    - journey_goal_event
    - utm_source_attribute
    - comparisonWindow
    - firstReturnWindow
    - setupWindow
    - fullActivationWindow
    - setupRateThreshold
    - timeToValueThreshold
    - lowActivationThreshold
    - highActivationThreshold
    - setupJourneyId
    - coreFeatureJourneyId
    - fullActivationJourneyId
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {trial_started_event}
      in the last {comparisonWindow} and in the {comparisonWindow} before that, and writes these figures for both windows:
      the count who started a trial; the share who did {session_start_event} within {firstReturnWindow} of it; the share who
      did {journey_goal_event} with {journey_goal_event.journey_id} equal to {setupJourneyId} within {setupWindow}; the share
      who did it with {coreFeatureJourneyId}, and the median time from trial start to that; the share who did it with {fullActivationJourneyId}
      within {fullActivationWindow}; that full activation share by {utm_source_attribute}. The email''s first line warns when
      the setup share is below {setupRateThreshold}%, the median time to the core feature is above {timeToValueThreshold},
      or a source''s full activation share is below {lowActivationThreshold}%, and names sources above {highActivationThreshold}%.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Trial activation funnel

Slash command: /trial-activation-funnel

## Step 1: Email the weekly trial activation digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did trial started event in the last 14 d and in the 14 d before that, and writes these figures for both windows: the count who started a trial; the share who did session start event within 24 h of it; the share who did journey goal event with journey id equal to the journey id of the setup milestone within 24 h; the share who did it with the journey id of the core feature milestone, and the median time from trial start to that; the share who did it with the journey id of the full activation milestone within 14 d; that full activation share by utm source attribute. The email's first line warns when the setup share is below 50%, the median time to the core feature is above 48 h, or a source's full activation share is below 15%, and names sources above 35%. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
