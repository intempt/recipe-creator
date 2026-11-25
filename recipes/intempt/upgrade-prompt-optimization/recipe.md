---
frontmatter_id: upgrade-prompt-optimization
slash_command: /upgrade-prompt-optimization
description: Builds the free-users segment and tests four placements of an upgrade prompt for them, split by account age,
  to find which placement best drives subscriptions without adding prompt fatigue.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests four placements of an upgrade prompt for free users, with account-age cohorts, to find which placement and
    timing best drives subscriptions without adding prompt fatigue.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Upgrade Prompt Optimization
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: min_account_age
    type: duration
    label: Minimum account age
    default: 3 d
    required: false
  - name: goal_window
    type: duration
    label: Subscription window after exposure
    default: 14 d
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - always
  - name: nps_drop_threshold
    type: number
    label: Max drop in average feedback score (points)
    default: 5
    required: false
  requirements:
  - slot: upgrade_prompt_click
    kind: event
    meaning: A user clicked a button on the in-app upgrade prompt
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked button, upgrade-prompt-cta or upgrade-prompt-dismiss
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started a paid subscription
  - slot: feedback_event
    kind: event
    meaning: A customer submitted feedback with a score
    optional: true
    properties:
    - name: score
      type: number
      meaning: Feedback score
      optional: false
  - slot: user_created
    kind: event
    meaning: A user account was created
  - slot: subscription_plan
    kind: attribute
    meaning: The user's current subscription plan, free for free users
  steps:
  - id: s1
    builds: segment
    uses:
    - user_created
    - subscription_plan
    - min_account_age
    instruction: Build a new segment of users named "Free Users for Upgrade Prompt". A user is in it when their {subscription_plan}
      is empty or equals free, and they did {user_created} more than {min_account_age} ago.
  - id: s2
    builds: experiment
    uses:
    - s1
    - upgrade_prompt_click
    - subscription_started
    - feedback_event
    - user_created
    - experiment_title
    - test_duration
    - goal_window
    - display_frequency
    - nps_drop_threshold
    dependsOn:
    - s1
    instruction: 'Create a client-side experiment named "{experiment_title}" for users in the segment from "Find free users
      old enough for a prompt", on every in-app page, all devices, shown {display_frequency}, running {test_duration}. Four
      variants at 25% each, all with a button id upgrade-prompt-cta and a dismiss button id upgrade-prompt-dismiss: Control
      is the current banner at the top of the app home ("Upgrade to Pro for unlimited features"); Variant B is an inline prompt
      shown when the user clicks a paid-only feature ("You''ve hit your free plan limit"); Variant C is a card at the bottom
      of the sidebar ("Unlock Pro features"); Variant D is a floating pill in the bottom-right corner ("Upgrade"). Report
      results split by account age at exposure: 3 to 7 days, 8 to 14 days and over 14 days since {user_created}. Primary metric:
      users who did {subscription_started} within {goal_window} of exposure. Secondary metrics: {upgrade_prompt_click} per
      {upgrade_prompt_click.target_id}. Guardrail: average {feedback_event.score} over the last 30 days must not drop more
      than {nps_drop_threshold} points.'
---

# Upgrade prompt test

Slash command: /upgrade-prompt-optimization

## Step 1: Find free users old enough for a prompt

Build a new segment of users named "Free Users for Upgrade Prompt". A user is in it when their subscription plan is empty or equals free, and they did user created more than 3 d ago.

## Step 2: Set up the upgrade prompt test

Create a client-side experiment named "Upgrade Prompt Optimization" for users in the segment from "Find free users old enough for a prompt", on every in-app page, all devices, shown once_per_session, running 21 d. Four variants at 25% each, all with a button id upgrade-prompt-cta and a dismiss button id upgrade-prompt-dismiss: Control is the current banner at the top of the app home ("Upgrade to Pro for unlimited features"); Variant B is an inline prompt shown when the user clicks a paid-only feature ("You've hit your free plan limit"); Variant C is a card at the bottom of the sidebar ("Unlock Pro features"); Variant D is a floating pill in the bottom-right corner ("Upgrade"). Report results split by account age at exposure: 3 to 7 days, 8 to 14 days and over 14 days since user created. Primary metric: users who did subscription started within 14 d of exposure. Secondary metrics: upgrade prompt click per target id. Guardrail: average score over the last 30 days must not drop more than 5 points.
