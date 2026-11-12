---
frontmatter_id: churn-risk-users
slash_command: /churn-risk-users
description: Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds paying users who logged in regularly two to three months ago but have not logged in during the last month,
    so they can be contacted before cancelling.
  parameters:
  - name: min_sessions
    type: number
    label: Minimum session starts in the earlier window
    default: 5
    required: false
  - name: earlier_window_start
    type: duration
    label: Earlier window start (days ago)
    default: 90 d
    required: false
  - name: earlier_window_end
    type: duration
    label: Earlier window end (days ago)
    default: 60 d
    required: false
  - name: silence_window
    type: duration
    label: Recent silence window
    default: 30 d
    required: false
  - name: free_plan_value
    type: string
    label: Plan value that counts as free
    default: free
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product (login or app open)
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on, such as free or paid
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - plan_attribute
    - min_sessions
    - earlier_window_start
    - earlier_window_end
    - silence_window
    - free_plan_value
    instruction: 'Build a segment named "Churn Risk Users" containing users who meet all of these conditions: they performed
      {session_start_event} at least {min_sessions} times between {earlier_window_start} and {earlier_window_end} ago; they
      did not perform {session_start_event} in the last {silence_window}; and their {plan_attribute} is not "{free_plan_value}".'
---

# Paid users going quiet

Slash command: /churn-risk-users

## Step 1: Build the silent paid-user list

Build a segment of users named "Churn Risk Users".
A user is in the segment only when all of these are true:
- they did the Session start event 5 or more times between 60 and 90 days ago
- they did not do the Session start event in the last 30 days
- their Plan attribute is not "free"
