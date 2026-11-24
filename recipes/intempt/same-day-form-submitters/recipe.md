---
frontmatter_id: same-day-form-submitters
slash_command: /same-day-form-submitters
description: Visitors who just submitted a form today, surfaced to sales as a same-day lead alert draft while interest is highest.
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
  summary: Alerts sales with a draft Slack message when visitors submitted a form today, so reps can follow up while interest
    is highest; a teammate still posts it.
  parameters:
  - name: form_window
    type: duration
    label: Look-back window for form submissions
    default: 1 d
    required: false
  - name: sales_channel_name
    type: string
    label: Sales team Slack channel
    default: sales team channel
    required: false
  requirements:
  - slot: form_submit_event
    kind: event
    meaning: A user submitted a form on the site (the project's form-submit event, never a survey or NPS answer)
  - slot: slack_workspace
    kind: integration
    meaning: A connected Slack workspace for posting sales alerts
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - form_submit_event
    - form_window
    instruction: Build a segment named "Same-Day Form Submitters". A user is in the segment only when they triggered {form_submit_event}
      at least once in the last {form_window}.
  - id: s2
    builds: slack
    uses:
    - s1
    - slack_workspace
    - sales_channel_name
    instruction: Draft a Slack message to {sales_channel_name} in {slack_workspace}. State how many users are in "Same-Day
      Form Submitters" right now, so reps know when a form submission just came in. Use the result of "Build the form submitter
      list". This drafts the Slack message only; a person on the team still posts it. Use the segment's current member count
      from the step that built it; never write a placeholder in square brackets. If no count is available, name the segment
      and say it can be opened in Segments.
---

# Same-Day Form Submitters

Slash command: /same-day-form-submitters

## Step 1: Build the form submitter list

Build a segment of users named "Same-Day Form Submitters". A user is in the segment only when all of these are true: triggered the form-submit event (a tracked submission of a form on the site, not a survey or NPS answer) at least once in the last 1 day.

## Step 2: Draft a sales alert

Generate a Slack message to the sales team channel. State how many users are in "Same-Day Form Submitters" right now, using the member count in the result of "Build the form submitter list". If that result carries no count, write no number and no placeholder in square brackets; say instead that the list is saved as the segment "Same-Day Form Submitters" and can be opened in Segments. Say a form submission just came in today. This drafts the Slack message only; a person on the team still posts it.
