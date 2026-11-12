---
frontmatter_id: recent-page-viewers-segment
slash_command: /recent-page-viewers-segment
description: This recipe helps marketers automatically identify and group users who have viewed any page on their site or app within the past week, tagging them with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Groups users who viewed any page on your site or app in the past week and tags them with a reusable attribute so
    later segments and campaigns can target them.
  parameters:
  - name: viewWindow
    type: duration
    label: Lookback window for page views
    default: 7 d
    required: false
  - name: taggedAttributeName
    type: string
    label: Name of the tag attribute
    default: recent_page_viewer
    required: false
  - name: tagValue
    type: boolean
    label: Value written to the tag attribute
    default: true
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the site or app (default autotracked page load event)
  - slot: recent_page_viewers_segment
    kind: segment
    meaning: Users who viewed a page within the lookback window, built by this recipe
    creatable: true
    definition: users who did {page_view_event} at least once in the last {viewWindow}
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - viewWindow
    instruction: 'Create a segment named "Recent Page Viewers" for users. Add one group with one condition: users who triggered
      {page_view_event} at least once in the last {viewWindow}.'
  - id: s2
    builds: attribute
    uses:
    - s1
    - taggedAttributeName
    - tagValue
    - recent_page_viewers_segment
    instruction: Create a user attribute named {taggedAttributeName} set to {tagValue} for every user in {recent_page_viewers_segment}.
      Use the segment built in "Create Recent Page Viewers Segment" as the audience.
---

# Recent Page Viewers Segment

Slash command: /recent-page-viewers-segment

## Step 1: Create Recent Page Viewers Segment

Create a segment called "Recent Page Viewers" for users. Base it on the "View page" event — the default autotracked event that fires on every page load. Add one group with one condition: triggered "View page" at least once in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "recent_page_viewer" on users in "Recent Page Viewers", set to true. Use the result of "Create Recent Page Viewers Segment".
