---
frontmatter_id: active-form-starters
slash_command: /active-form-starters
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
  - name: alert_channel
    type: string
    label: Slack channel for team alerts
    default: support team
    required: false
  requirements:
  - slot: form_change_event
    kind: event
    meaning: A user edited a field in a form on the site (the project's form-field change event)
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
      starter list". This drafts the Slack message only; a person on the team still posts it. Use the segment's current member
      count from the step that built it; never write a placeholder in square brackets. If no count is available, name the
      segment and say it can be opened in Segments.
---

# Active Form Starters

Slash command: /active-form-starters

## Step 1: Build the active form starter list

Build a segment of users named "Active Form Starters". A user is in the segment only when all of these are true: triggered the form-field change event (a tracked edit of a field in a form on the site) at least once in the last 1 day.

## Step 2: Draft an alert for the team

Generate a Slack message to the support team channel. State how many users are in "Active Form Starters" right now, using the member count in the result of "Build the active form starter list". If that result carries no count, write no number and no placeholder in square brackets; say instead that the list is saved as the segment "Active Form Starters" and can be opened in Segments. Say someone is actively filling out a form today. This drafts the Slack message only; a person on the team still posts it.
