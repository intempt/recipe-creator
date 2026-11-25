---
frontmatter_id: recently-won-accounts
slash_command: /recently-won-accounts
description: Accounts whose users just started paying, welcomed with an onboarding kickoff email and handed to the onboarding team while the account is still new.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Welcomes newly paying accounts with an onboarding kickoff email and notifies the onboarding team of each account
    while it is still new.
  parameters:
  - name: window
    type: duration
    label: Look-back window for the subscription start event
    default: 30 d
    required: false
  - name: tone
    type: enum
    label: Tone of the kickoff email
    default: warm and encouraging
    required: false
    options:
    - warm and encouraging
    - professional
    - playful
  - name: onboarding_guide_url
    type: text
    label: Link to the onboarding guide for the email button
    required: true
  requirements:
  - slot: subscription_started
    kind: event
    meaning: A customer started a paid subscription
  - slot: onboarding_team_list
    kind: destination
    meaning: The distribution list for the onboarding team that receives plain-text notifications
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_started
    - window
    instruction: Build a segment named "Recently-Won Accounts" of accounts where the users in the account together did {subscription_started}
      at least once in the last {window}.
  - id: s2
    builds: email
    uses:
    - s1
    - tone
    - onboarding_guide_url
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the accounts in s1 welcoming the team and pointing to the first milestone
      worth hitting. Write three sentences in a {tone} tone with no discount language. Include one button linking to {onboarding_guide_url}.
      If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this
      run or named in this step; never leave a button without a link.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - onboarding_team_list
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to {onboarding_team_list}. For each account in s1, name the account so implementation
      starts from one current list. Take names and addresses from the member list in the result of the step that built the
      list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text
      email is plain text only: no HTML tags, no markup and no unsubscribe line.'
---

# Recently won accounts

Slash command: /recently-won-accounts

## Step 1: Build the recently-won list

Build a segment named "Recently-Won Accounts" of accounts where the users in the account together did subscription started at least once in the last 30 d.

## Step 2: Send an onboarding kickoff email

Generate a designed marketing email for the accounts in s1 welcoming the team and pointing to the first milestone worth hitting. Write three sentences in a warm and encouraging tone with no discount language. Include one button linking to the link to the onboarding guide for the email button. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Notify onboarding

Generate a plain-text email to onboarding team list. For each account in s1, name the account so implementation starts from one current list. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
