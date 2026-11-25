---
frontmatter_id: trial-activation
slash_command: /trial-activation
description: Scores each trial's health, builds the active trials segment, writes an activation email and an upgrade email,
  and sends each trial the one that fits its score.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores each trial's health and sends trial users an activation or upgrade email by score, leading them toward paid
    conversion.
  parameters:
  - name: login_window
    type: duration
    label: Window the score looks at
    default: 30 d
    required: false
  - name: tier_high_min_score
    type: number
    label: Score from which a trial counts as highly engaged
    default: 70
    required: false
  - name: tone
    type: enum
    label: Tone of onboarding emails
    default: encouraging
    required: false
    options:
    - encouraging
    - neutral
    - direct
  requirements:
  - slot: trial_signup_event
    kind: event
    meaning: A customer signed up for a trial
  - slot: paid_conversion_event
    kind: event
    meaning: A trial customer converted to a paid subscription
  - slot: trial_login_event
    kind: event
    meaning: A customer logged into the product
  - slot: key_feature_event
    kind: event
    meaning: A customer used a key product feature
    properties:
    - name: feature_name
      type: string
      meaning: Which key feature was used
      optional: false
  - slot: team_invite_event
    kind: event
    meaning: A customer invited a teammate to the product
  - slot: data_upload_event
    kind: event
    meaning: A customer uploaded data into the product
  - slot: onboarding_email_channel
    kind: destination
    channel: email
    meaning: Channel used to send onboarding emails to trial users
  steps:
  - id: s1
    builds: attribute
    uses:
    - trial_login_event
    - key_feature_event
    - team_invite_event
    - data_upload_event
    - login_window
    instruction: 'Build a computed user attribute named "Trial health score", a number from 0 to 100 over the last {login_window}:
      30 points scaled by the number of distinct days with {trial_login_event} (full at 10 days), 30 points scaled by the
      number of distinct {key_feature_event.feature_name} values used (full at 3), 20 points when the user did {team_invite_event}
      at least once, 20 points when the user did {data_upload_event} at least once.'
  - id: s2
    builds: segment
    uses:
    - trial_signup_event
    - paid_conversion_event
    instruction: 'Build a new segment of users named "Active Trial Users": users who did {trial_signup_event} in the last
      30 days and have not done {paid_conversion_event}.'
  - id: s3
    builds: email
    uses:
    - key_feature_event
    - tone
    instruction: 'Write an onboarding email in a {tone} tone for trial users who have not found their footing yet: it shows
      the 2-3 key features ({key_feature_event}) that deliver value fastest, one short how-to each, and one button to open
      the product. If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s4
    builds: email
    uses:
    - tone
    instruction: 'Write an email in a {tone} tone for highly engaged trial users: it recognizes how much they have set up,
      names what they keep by moving to a paid plan before the trial ends, and has one button to upgrade. If the brand kit
      has no logo, use the brand name as a plain text header.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - tier_high_min_score
    - paid_conversion_event
    - onboarding_email_channel
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build an automation that starts when a user enters the segment from "Find the active trials". It waits 3
      days, then splits on the attribute from "Score how the trial is going": score at least {tier_high_min_score}: send the
      email from "Write the upgrade email"; score below {tier_high_min_score}: send the email from "Write the activation email".
      Sends go through {onboarding_email_channel}. Then it waits 7 days and, if the user has not done {paid_conversion_event}
      and the score is now at least {tier_high_min_score}, sends the email from "Write the upgrade email" once if they have
      not had it. Then Blu asks to start it.'
---

# Trial to paid activation

Slash command: /trial-activation

## Step 1: Score how the trial is going

Build a computed user attribute named "Trial health score", a number from 0 to 100 over the last 30 d: 30 points scaled by the number of distinct days with trial login event (full at 10 days), 30 points scaled by the number of distinct feature name values used (full at 3), 20 points when the user did team invite event at least once, 20 points when the user did data upload event at least once.

## Step 2: Find the active trials

Build a new segment of users named "Active Trial Users": users who did trial signup event in the last 30 days and have not done paid conversion event.

## Step 3: Write the activation email

Write an onboarding email in a encouraging tone for trial users who have not found their footing yet: it shows the 2-3 key features (key feature event) that deliver value fastest, one short how-to each, and one button to open the product. If the brand kit has no logo, use the brand name as a plain text header.

## Step 4: Write the upgrade email

Write an email in a encouraging tone for highly engaged trial users: it recognizes how much they have set up, names what they keep by moving to a paid plan before the trial ends, and has one button to upgrade. If the brand kit has no logo, use the brand name as a plain text header.

## Step 5: Send each trial the email that fits

Build an automation that starts when a user enters the segment from "Find the active trials". It waits 3 days, then splits on the attribute from "Score how the trial is going": score at least 70: send the email from "Write the upgrade email"; score below 70: send the email from "Write the activation email". Sends go through onboarding email channel. Then it waits 7 days and, if the user has not done paid conversion event and the score is now at least 70, sends the email from "Write the upgrade email" once if they have not had it. Then Blu asks to start it.
