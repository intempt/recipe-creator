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
    instruction: Build a new segment named "Power Users" of users whose {lifetime_value} is more than {minLifetimeValue} and
      who did {session_start_event} {sessionThreshold} or more times in the last {sessionWindow}.
  - id: s2
    builds: push
    uses:
    - referral_push_channel
    - referralPageLink
    - pushTone
    - pushTitleMaxChars
    - s1
    dependsOn:
    - s1
    instruction: Generate a push notification for the users in the segment from "Build the power-user list" inviting them
      to join the referral program. Title must be under {pushTitleMaxChars} characters, with one short body line, in a {pushTone}
      tone, and deep link to {referralPageLink}. Write no template tag or placeholder (such as a deeplink tag) in the push
      title or body; a link, if any, is the URL given for this run.
  - id: s3
    builds: email_plain
    uses:
    - customer_email
    - growthTeamList
    - s1
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to {growthTeamList} listing, for each user in the segment from "Build the power-user
      list", their {customer_email}, as candidates for case studies and advocacy, not just referrals. Take names and addresses
      from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder
      or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe
      line.'
---

# Power users

Slash command: /power-users

## Step 1: Build the power-user list

Build a new segment named "Power Users" of users whose lifetime value is more than 0 and who did session start event 10 or more times in the last 30 d.

## Step 2: Invite them to the referral program

Generate a push notification for the users in the segment from "Build the power-user list" inviting them to join the referral program. Title must be under 40 characters, with one short body line, in a friendly and appreciative tone, and deep link to the referral program page deep link. Write no template tag or placeholder (such as a deeplink tag) in the push title or body; a link, if any, is the URL given for this run.

## Step 3: Share the shortlist with growth

Generate a plain-text email to the growth team distribution list listing, for each user in the segment from "Build the power-user list", their customer email, as candidates for case studies and advocacy, not just referrals. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
