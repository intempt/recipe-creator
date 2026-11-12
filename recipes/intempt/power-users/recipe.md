---
frontmatter_id: power-users
slash_command: /power-users
description: Paying users who log in constantly, invited to join the referral program by push notification and shared with growth as advocacy candidates.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds paying users who log in constantly, sends them a friendly push inviting them to the referral program, and
    emails growth their details as advocacy candidates.
  parameters:
  - name: minLifetimeValue
    type: number
    label: Minimum lifetime value (exclusive)
    default: 0
    required: false
  - name: sessionThreshold
    type: number
    label: Minimum session starts
    default: 10
    required: false
  - name: sessionWindow
    type: duration
    label: Session count window
    default: 30 d
    required: false
  - name: pushTitleMaxChars
    type: number
    label: Push title maximum characters
    default: 40
    required: false
  - name: pushTone
    type: enum
    label: Push notification tone
    default: friendly and appreciative
    required: false
    options:
    - friendly and appreciative
    - neutral
    - playful
    - formal
  - name: referralPageLink
    type: text
    label: Referral program page deep link
    required: true
  - name: growthTeamList
    type: text
    label: Growth team distribution list
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the app or site
  - slot: lifetime_value
    kind: attribute
    meaning: The total lifetime value a customer has paid
  - slot: customer_email
    kind: attribute
    meaning: The email address of a customer
  - slot: power_users
    kind: segment
    meaning: Users with paid lifetime value who started sessions frequently in the recent window
    creatable: true
    definition: users where {lifetime_value} is more than {minLifetimeValue} and who did {session_start_event} {sessionThreshold}
      or more times in the last {sessionWindow}
  - slot: referral_push_channel
    kind: destination
    meaning: A push notification channel to reach customers on their devices
    channel: push
  steps:
  - id: s1
    builds: segment
    uses:
    - lifetime_value
    - session_start_event
    - minLifetimeValue
    - sessionThreshold
    - sessionWindow
    - power_users
    instruction: Build a segment named {power_users} of users whose {lifetime_value} is more than {minLifetimeValue} and who
      did {session_start_event} {sessionThreshold} or more times in the last {sessionWindow}.
  - id: s2
    builds: push
    uses:
    - power_users
    - referral_push_channel
    - referralPageLink
    - pushTone
    - pushTitleMaxChars
    - s1
    instruction: Generate a push notification for the users in the segment from "Build the power-user list" inviting them
      to join the referral program. Title must be under {pushTitleMaxChars} characters, with one short body line, in a {pushTone}
      tone, and deep link to {referralPageLink}.
  - id: s3
    builds: email_plain
    uses:
    - power_users
    - customer_email
    - growthTeamList
    - s1
    instruction: Generate a plain-text email to {growthTeamList} listing, for each user in the segment from "Build the power-user
      list", their {customer_email}, as candidates for case studies and advocacy, not just referrals.
---

# Power users

Slash command: /power-users

## Step 1: Build the power-user list

Build a segment of users named "Power Users".
A user is in the segment only when all of these are true:
- their Lifetime value attribute is more than 0
- they did the Session start event 10 or more times in the last 30 days

## Step 2: Invite them to the referral program

Generate a push notification for the users in "Power Users" inviting them to join the referral program. Title under 40 characters, one short body line, friendly and appreciative tone, deep link to the referral program page. Use the result of "Build the power-user list".

## Step 3: Share the shortlist with growth

Generate a plain-text email to the growth team distribution list For each user in "Power Users", name their email address, as candidates for case studies and advocacy, not just referrals. Use the result of "Build the power-user list".
