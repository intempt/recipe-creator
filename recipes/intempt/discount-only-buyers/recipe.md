---
frontmatter_id: discount-only-buyers
slash_command: /discount-only-buyers
description: Visitors who have come back in more than one session, tagged with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tags visitors who returned in two or more sessions within 30 days, so later segments and campaigns can target them
    without rebuilding the match.
  parameters:
  - name: minSessions
    type: number
    label: Minimum session starts
    default: 2
    required: false
  - name: windowDays
    type: duration
    label: Lookback window
    default: 30 d
    required: false
  - name: attributeName
    type: string
    label: Tag attribute name
    default: returning_visitor
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a session on the site or app
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - minSessions
    - windowDays
    instruction: 'Build a segment of users named "Returning Visitors". A user is in the segment only when all of these are
      true: triggered {session_start_event} at least {minSessions} times in the last {windowDays}.'
  - id: s2
    builds: attribute
    uses:
    - s1
    - attributeName
    instruction: Create an attribute named {attributeName} on users in "Returning Visitors", set to true. Use the result of
      "Build the returning visitor list".
---

# Returning Visitors

Slash command: /discount-only-buyers

## Step 1: Build the returning visitor list

Build a segment of users named "Returning Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 2 times in the last 30 days.

## Step 2: Tag the matched visitors

Create an attribute named "returning_visitor" on users in "Returning Visitors", set to true. Use the result of "Build the returning visitor list".
