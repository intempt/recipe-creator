---
frontmatter_id: acquisition-channel-cohort
slash_command: /acquisition-channel-cohort
description: Visitors who keep coming back to the same pages, tagged with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds visitors who view pages repeatedly within a short window and tags them with a reusable attribute so later
    segments and campaigns can target them.
  parameters:
  - name: min_views
    type: number
    label: Minimum page views
    default: 3
    required: false
  - name: view_window
    type: duration
    label: Look-back window
    default: 7 d
    required: false
  - name: segment_name
    type: string
    label: Segment name
    default: Repeat Page Visitors
    required: false
  - name: attribute_name
    type: string
    label: Attribute name
    default: repeat_visitor
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the website
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - min_views
    - view_window
    - segment_name
    instruction: Build a segment named "{segment_name}" of users who triggered {page_view_event} at least {min_views} times
      in the last {view_window}.
  - id: s2
    builds: attribute
    uses:
    - s1
    - attribute_name
    - segment_name
    instruction: Create an attribute named "{attribute_name}" on users in "{segment_name}", set to true, using the segment
      built in "Build the repeat visitor list".
---

# Repeat Page Visitors

Slash command: /acquisition-channel-cohort

## Step 1: Build the repeat visitor list

Build a segment of users named "Repeat Page Visitors". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "repeat_visitor" on users in "Repeat Page Visitors", set to true. Use the result of "Build the repeat visitor list".
