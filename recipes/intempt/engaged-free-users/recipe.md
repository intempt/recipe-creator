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
    instruction: Build a new segment named "Engaged Free Users" of users whose {plan_attribute} is "free" and who did {session_start_event}
      5 or more times in the last {lookback_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - upgrade_tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the segment from "Build the engaged free list" introducing
      the paid plan's feature most relevant to someone already using the product this often. Write three sentences in an {upgrade_tone}
      tone, with no discount language. Include one button linking to the pricing page. If the brand kit has no logo, use the
      brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave
      a button without a link.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - growth_team_list
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to the {growth_team_list} distribution list. For each user in the segment from
      "Build the engaged free list", include their email address so outreach can be prioritized by how active each one already
      is. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how
      many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only:
      no HTML tags, no markup and no unsubscribe line.'
---

# Engaged free users

Slash command: /engaged-free-users

## Step 1: Build the engaged free list

Build a new segment named "Engaged Free Users" of users whose plan attribute is "free" and who did session start event 5 or more times in the last 14 d.

## Step 2: Send an upgrade email

Generate a designed marketing email for the users in the segment from "Build the engaged free list" introducing the paid plan's feature most relevant to someone already using the product this often. Write three sentences in an encouraging tone, with no discount language. Include one button linking to the pricing page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Notify growth

Generate a plain-text email to the growth team list distribution list. For each user in the segment from "Build the engaged free list", include their email address so outreach can be prioritized by how active each one already is. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
