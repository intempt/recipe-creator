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
  - slot: form_abandoners
    kind: segment
    meaning: Users who started a form and did not submit it within the window
    creatable: true
    definition: users who did {form_change_event} at least once in the last {lookback_window} and did not do {form_submit_event}
      in the last {lookback_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - form_change_event
    - form_submit_event
    - lookback_window
    instruction: Build a segment named "Form Abandoners" of users who did {form_change_event} at least once in the last {lookback_window}
      and did not do {form_submit_event} in the last {lookback_window}.
  - id: s2
    builds: attribute
    uses:
    - form_abandoners
    - attribute_name
    - s1
    instruction: Create a user attribute named {attribute_name} set to true for every user in {form_abandoners} built in "Build
      a segment named Form Abandoners".
---

# Form Abandoners

Slash command: /form-abandoners

## Step 1: Build the form abandoner list

Build a segment of users named "Form Abandoners". A user is in the segment only when all of these are true: triggered the form-field change event (a tracked edit of a field in a form on the site) at least once in the last 3 days; did not trigger the form-submit event (a tracked submission of a form on the site, not a survey or NPS answer) in the last 3 days.

## Step 2: Tag the matched users

Create an attribute named "form_abandoner" on users in "Form Abandoners", set to true. Use the result of "Build the form abandoner list".
