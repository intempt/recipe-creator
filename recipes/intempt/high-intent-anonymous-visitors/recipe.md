---
frontmatter_id: high-intent-anonymous-visitors
slash_command: /high-intent-anonymous-visitors
description: Visitors who keep coming back to your site and product, with a feature-nudge push drafted and a retargeting audience drafted for growth.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds visitors who keep returning to the site and product, then drafts a feature-nudge push and a plain-text retargeting
    audience email for the growth team; a person still sends both.
  parameters:
  - name: pageViewWindow
    type: duration
    label: Window for page view and session counts
    default: 7 d
    required: false
  - name: pageViewMinCount
    type: number
    label: Minimum page view count in window
    default: 3
    required: false
  - name: sessionStartMinCount
    type: number
    label: Minimum session start count in window
    default: 2
    required: false
  - name: pushTitleMaxChars
    type: number
    label: Maximum push title length (characters)
    default: 40
    required: false
  - name: pushTone
    type: enum
    label: Tone of the feature-nudge push
    default: friendly_curious
    required: false
    options:
    - friendly_curious
    - neutral
    - enthusiastic
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page of the site or product
    properties:
    - name: page
      type: text
      meaning: Page or screen that was viewed
      optional: true
  - slot: session_start_event
    kind: event
    meaning: A user started a session on the site or product
  - slot: frequent_repeat_visitors
    kind: segment
    meaning: Users who viewed pages 3 or more times and started 2 or more sessions in the last 7 days
    creatable: true
    definition: users who did {page_view_event} at least {pageViewMinCount} times in the last {pageViewWindow} and did {session_start_event}
      at least {sessionStartMinCount} times in the last {pageViewWindow}
  - slot: user_email
    kind: attribute
    meaning: The email address of a user
  - slot: push_channel
    kind: integration
    meaning: A push notification channel to send messages to users
    channel: push
  - slot: growth_team_list
    kind: destination
    meaning: Distribution list for the growth team email
    channel: email
  - slot: product_features
    kind: knowledge
    meaning: Description of the product's features and their deep links, used to pick one feature worth trying
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - session_start_event
    - pageViewWindow
    - pageViewMinCount
    - sessionStartMinCount
    instruction: 'Build a segment named "Frequent Repeat Visitors". Include a user only when all of these are true: they did
      {page_view_event} at least {pageViewMinCount} times in the last {pageViewWindow}; they did {session_start_event} at
      least {sessionStartMinCount} times in the last {pageViewWindow}.'
  - id: s2
    builds: push
    uses:
    - s1
    - frequent_repeat_visitors
    - push_channel
    - product_features
    - pushTone
    - pushTitleMaxChars
    instruction: Generate a push notification for the users in "Frequent Repeat Visitors" highlighting one product feature
      worth trying, chosen for this run given how often they are showing up. Title under {pushTitleMaxChars} characters, one
      short body line, {pushTone} tone, with a deep link to that feature. Use the result of "Build the frequent-visitor list".
      Draft the push only; a person still sends it.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - frequent_repeat_visitors
    - user_email
    - growth_team_list
    instruction: Generate a plain-text email to the growth team distribution list. For each user in "Frequent Repeat Visitors",
      list their {user_email} as a retargeting audience worth running ads against. Use the result of "Build the frequent-visitor
      list". Draft the email only; a person still sends it.
---

# Frequent repeat visitors

Slash command: /high-intent-anonymous-visitors

## Step 1: Build the frequent-visitor list

Build a segment of users named "Frequent Repeat Visitors". A user is in the segment only when all of these are true: they did the View page event 3 or more times in the last 7 days; they did the Session start event 2 or more times in the last 7 days.

## Step 2: Draft a feature-nudge push

Generate a push notification for the users in "Frequent Repeat Visitors" highlighting one feature of the product worth trying, chosen for this run given how often they are showing up. Title under 40 characters, one short body line, friendly and curious tone, deep link to that feature. Use the result of "Build the frequent-visitor list". This drafts the push only; a person still sends it.

## Step 3: Draft the retargeting audience email

Generate a plain-text email to the growth team distribution list. For each user in "Frequent Repeat Visitors", name their email address, as a retargeting audience worth running ads against. Use the result of "Build the frequent-visitor list". This drafts the email only; a person still sends it.
