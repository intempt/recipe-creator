---
frontmatter_id: failed-payment-accounts
slash_command: /failed-payment-accounts
description: Visitors currently filling out a form, surfaced to the team as a real-time draft alert so they can be reached while still on the page.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Alerts the support team in Slack when visitors are actively filling out a form, so they can be reached while still
    on the page.
  parameters:
  - name: lookback_window
    type: duration
    label: Lookback window for form activity
    default: 1 d
    required: false
  - name: form_event_name
    type: string
    label: Form interaction event name
    default: Change on
    required: false
  - name: alert_channel
    type: string
    label: Slack channel for team alerts
    default: support team
    required: false
  requirements:
  - slot: form_change_event
    kind: event
    meaning: A visitor changed a field on a form
  - slot: support_slack
    kind: destination
    meaning: Slack workspace channel where the support team receives alerts
    channel: slack
  - slot: active_form_starters
    kind: segment
    meaning: Users who triggered a form change event at least once in the lookback window
    creatable: true
    definition: users who did {form_change_event} at least once in the last {lookback_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - form_change_event
    - lookback_window
    instruction: 'Build a segment of users named "Active Form Starters". A user is in the segment only when all of these are
      true: triggered {form_change_event} at least once in the last {lookback_window}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - support_slack
    - alert_channel
    instruction: Generate a Slack message to the {alert_channel} channel in {support_slack}. State how many users are in {active_form_starters}
      right now, so the team knows someone is actively filling out a form today. Use the result of "Build the active form
      starter list". This drafts the Slack message only; a person on the team still posts it.
---

# Active Form Starters

Slash command: /failed-payment-accounts

## Step 1: Build the active form starter list

Build a segment of users named "Active Form Starters". A user is in the segment only when all of these are true: triggered "Change on" at least once in the last 1 day.

## Step 2: Draft an alert for the team

Generate a Slack message to the support team channel. Say how many users are in "Active Form Starters" right now, so the team knows someone is actively filling out a form today. Use the result of "Build the active form starter list". This drafts the Slack message only; a person on the team still posts it.
