---
frontmatter_id: mockup
slash_command: /mockup
description: Visitors returning on a near-daily basis, tagged as a power-user pool with a ready-to-send early-access or loyalty invite email drafted.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds visitors who return almost every day, tags them as a power-user group, and drafts a warm early-access or
    loyalty invite email for a person to review and send.
  parameters:
  - name: minSessions
    type: number
    label: Minimum session starts required
    default: 4
    required: false
  - name: windowDays
    type: duration
    label: Look-back window
    default: 4 d
    required: false
  - name: emailTone
    type: enum
    label: Email tone
    default: warm
    required: false
    options:
    - warm
    - playful
    - formal
  - name: emailSentenceCount
    type: number
    label: Number of sentences in the email body
    default: 3
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a session on the site or app
  - slot: daily_habit_user_attribute
    kind: attribute
    meaning: A user-level true/false flag marking daily habit users
  - slot: daily_habit_visitors
    kind: segment
    meaning: Users who started a session at least a set number of times in the look-back window
    creatable: true
    definition: users who did {session_start_event} at least {minSessions} times in the last {windowDays}
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - minSessions
    - windowDays
    instruction: Build a segment named "Daily Habit Visitors" of users who did {session_start_event} at least {minSessions}
      times in the last {windowDays}. Only users meeting this condition are included.
  - id: s2
    builds: attribute
    uses:
    - s1
    - daily_habit_user_attribute
    instruction: Create the user attribute {daily_habit_user_attribute} set to true for every user in the segment built in
      "Build the daily habit visitor list".
  - id: s3
    builds: email
    uses:
    - s1
    - emailTone
    - emailSentenceCount
    instruction: Generate a designed marketing email for users in the segment built in "Build the daily habit visitor list"
      inviting them to join an early-access or loyalty list in recognition of how often they visit. Use a {emailTone} tone
      with {emailSentenceCount} sentences in the body. Do not use any discount language. Include exactly one button that lets
      them join. Save as a draft only; a person reviews and sends it.
---

# Daily Habit Visitors

Slash command: /mockup

## Step 1: Build the daily habit visitor list

Build a segment of users named "Daily Habit Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 4 times in the last 4 days.

## Step 2: Tag the matched visitors

Create an attribute named "daily_habit_user" on users in "Daily Habit Visitors", set to true. Use the result of "Build the daily habit visitor list".

## Step 3: Draft an early-access invite email

Generate a designed marketing email for the users in "Daily Habit Visitors" inviting them into an early-access or loyalty list in recognition of how often they show up. Three sentences, warm and appreciative tone, no discount language, one button to join. Use the result of "Build the daily habit visitor list". This drafts the email only; a person still sends it.
