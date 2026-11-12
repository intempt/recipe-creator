---
frontmatter_id: engaged-non-buyers
slash_command: /engaged-non-buyers
description: Visitors who click around the site a lot, tagged with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tags visitors who click around the site often, so later segments and campaigns can target them without rebuilding
    the match.
  parameters:
  - name: click_threshold
    type: number
    label: Minimum number of click events
    default: 5
    required: false
  - name: window
    type: duration
    label: Lookback window for clicks
    default: 7 d
    required: false
  - name: segment_name
    type: string
    label: Name of the highly engaged segment
    default: Highly Engaged Visitors
    required: false
  - name: attribute_name
    type: string
    label: Name of the tagging attribute
    default: highly_engaged
    required: false
  requirements:
  - slot: click_event
    kind: event
    meaning: A visitor clicked on the site
  steps:
  - id: s1
    builds: segment
    uses:
    - click_event
    - click_threshold
    - window
    - segment_name
    instruction: Build a segment named "{segment_name}" of users who triggered {click_event} at least {click_threshold} times
      in the last {window}.
  - id: s2
    builds: attribute
    uses:
    - s1
    - attribute_name
    - segment_name
    instruction: Create an attribute named "{attribute_name}" on users in "{segment_name}", set to true. Use the result of
      "Build the highly engaged visitor list".
---

# Highly Engaged Visitors

Slash command: /engaged-non-buyers

## Step 1: Build the highly engaged visitor list

Build a segment of users named "Highly Engaged Visitors". A user is in the segment only when all of these are true: triggered "Click on" at least 5 times in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "highly_engaged" on users in "Highly Engaged Visitors", set to true. Use the result of "Build the highly engaged visitor list".
