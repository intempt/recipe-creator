---
frontmatter_id: expansion-candidates
slash_command: /expansion-candidates
description: Users on a plan below enterprise who log in often enough to be your clearest upgrade signal, offered the next tier by email and routed to growth for outreach.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds active users on a plan below enterprise and emails them a designed upgrade offer highlighting a higher-plan
    feature, then alerts the growth team with each candidate's email for timed outreach.
  parameters:
  - name: sessionThreshold
    type: number
    label: Minimum session starts
    default: 8
    required: false
  - name: sessionWindow
    type: duration
    label: Session lookback window
    default: 14 d
    required: false
  - name: excludedPlan
    type: string
    label: Plan excluded from upgrade targeting
    default: enterprise
    required: false
  - name: tone
    type: string
    label: Email tone
    default: confident and helpful
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on
  - slot: user_email
    kind: attribute
    meaning: The email address of a user
  - slot: upgrade_email_channel
    kind: destination
    meaning: An email channel able to send marketing emails to users
    channel: email
  - slot: growth_team_channel
    kind: destination
    meaning: A channel to notify the growth team, such as a distribution list
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - plan_attribute
    - session_start_event
    - excludedPlan
    - sessionThreshold
    - sessionWindow
    instruction: Build a new segment named "Expansion Candidates" that includes users whose {plan_attribute} has a value and
      is not {excludedPlan} and who did {session_start_event} {sessionThreshold} or more times in the last {sessionWindow}.
  - id: s2
    builds: email
    uses:
    - s1
    - upgrade_email_channel
    - tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the "Expansion Candidates" segment highlighting one
      feature available only on a higher plan. Use a {tone} tone, three sentences, and no discount language. Include one button
      linking to the upgrade page. If the brand kit has no logo, use the brand name as a plain text header. Every button links
      to a URL given for this run or named in this step; never leave a button without a link.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - growth_team_channel
    - user_email
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to the growth team distribution list ({growth_team_channel}). For each user
      in the "Expansion Candidates" segment, include their {user_email} so outreach can be timed to their actual usage instead
      of a generic drip. Take names and addresses from the member list in the result of the step that built the list (at most
      20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain
      text only: no HTML tags, no markup and no unsubscribe line.'
---

# Highly engaged users below enterprise

Slash command: /expansion-candidates

## Step 1: Build the expansion-candidate list

Build a new segment named "Expansion Candidates" that includes users whose plan attribute has a value and is not enterprise and who did session start event 8 or more times in the last 14 d.

## Step 2: Send an upgrade email

Generate a designed marketing email for the users in the "Expansion Candidates" segment highlighting one feature available only on a higher plan. Use a confident and helpful tone, three sentences, and no discount language. Include one button linking to the upgrade page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Notify growth

Generate a plain-text email to the growth team distribution list (growth team channel). For each user in the "Expansion Candidates" segment, include their user email so outreach can be timed to their actual usage instead of a generic drip. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
