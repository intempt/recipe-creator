---
frontmatter_id: form-abandoners
slash_command: /form-abandoners
description: Users who started filling out a form and never finished, tagged while their intent is still fresh for a quick nudge or retargeting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tags users who started filling out a form but did not submit it within three days, so they can get a quick nudge
    or retargeting while intent is fresh.
  parameters:
  - name: lookback_window
    type: duration
    label: Window for form activity and submission check
    default: 3 d
    required: false
  - name: attribute_name
    type: string
    label: Attribute name used to tag matched users
    default: form_abandoner
    required: false
  requirements:
  - slot: form_change_event
    kind: event
    meaning: A user edited a field in a form on the site (the project's form-field change event)
  - slot: form_submit_event
    kind: event
    meaning: A user submitted a form on the site (the project's form-submit event, never a survey or NPS answer)
  steps:
  - id: s1
    builds: segment
    uses:
    - form_change_event
    - form_submit_event
    - lookback_window
    instruction: Build a new segment named "Form Abandoners" of users who did {form_change_event} at least once in the last
      {lookback_window} and did not do {form_submit_event} in the last {lookback_window}.
  - id: s2
    builds: attribute
    uses:
    - attribute_name
    - s1
    dependsOn:
    - s1
    instruction: Create a user attribute named {attribute_name} set to true for every user in the segment from "Build the
      form abandoner list" built in "Build a segment named Form Abandoners".
---

# Form Abandoners

Slash command: /form-abandoners

## Step 1: Build the form abandoner list

Build a new segment named "Form Abandoners" of users who did form change event at least once in the last 3 d and did not do form submit event in the last 3 d.

## Step 2: Tag the matched users

Create a user attribute named form_abandoner set to true for every user in the segment from "Build the form abandoner list" built in "Build a segment named Form Abandoners".
