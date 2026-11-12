---
frontmatter_id: engaged-free-users
slash_command: /engaged-free-users
description: Free-plan users logging in often enough to be ready for a paid plan, offered the upgrade by email and queued for growth outreach.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds free-plan users who log in often and emails them a paid-plan upgrade offer, while alerting the growth team
    with the list to prioritize outreach.
  parameters:
  - name: session_threshold
    type: number
    label: Minimum session starts
    default: 5
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 14 d
    required: false
  - name: upgrade_tone
    type: string
    label: Email tone
    default: encouraging
    required: false
  requirements:
  - slot: plan_attribute
    kind: attribute
    meaning: The plan a user is on, such as free or paid
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product by logging in
  - slot: engaged_free_users
    kind: segment
    meaning: Free-plan users with frequent recent session starts
    creatable: true
    definition: users whose {plan_attribute} is free and who did {session_start_event} at least {session_threshold} times
      in the last {lookback_window}
  - slot: growth_team_list
    kind: integration
    meaning: A distribution list that reaches the growth team
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - plan_attribute
    - session_start_event
    - session_threshold
    - lookback_window
    instruction: Build a segment named {engaged_free_users} of users whose {plan_attribute} is "free" and who did {session_start_event}
      5 or more times in the last {lookback_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - engaged_free_users
    - upgrade_tone
    instruction: Generate a designed marketing email for the users in {engaged_free_users} introducing the paid plan's feature
      most relevant to someone already using the product this often. Write three sentences in an {upgrade_tone} tone, with
      no discount language. Include one button linking to the pricing page.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - engaged_free_users
    - growth_team_list
    instruction: Generate a plain-text email to the {growth_team_list} distribution list. For each user in {engaged_free_users},
      include their email address so outreach can be prioritized by how active each one already is.
---

# Engaged free users

Slash command: /engaged-free-users

## Step 1: Build the engaged free list

Build a segment of users named "Engaged Free Users".
A user is in the segment only when all of these are true:
- their Plan attribute is "free"
- they did the Session start event 5 or more times in the last 14 days

## Step 2: Send an upgrade email

Generate a designed marketing email for the users in "Engaged Free Users" introducing the paid plan's feature most relevant to someone already using the product this often. Three sentences, encouraging tone, no discount language, one button linking to the pricing page. Use the result of "Build the engaged free list".

## Step 3: Notify growth

Generate a plain-text email to the growth team distribution list For each user in "Engaged Free Users", name their email address, so outreach can be prioritized by how active each one already is. Use the result of "Build the engaged free list".
