---
frontmatter_id: renewal-window-90-day
slash_command: /renewal-window-90-day
description: Paying subscriptions that started roughly a year ago and are likely due for renewal, flagged to the renewals team and sent a value recap, so the conversation starts early instead of the week before.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Flags paying subscribers whose subscription started about a year ago to the renewals team, and sends them a warm
    value recap with a button to book a call with their account manager.
  parameters:
  - name: plan_excluded
    type: string
    label: Plan value to exclude
    default: free
    required: false
  - name: window_min
    type: duration
    label: Minimum days since subscription started
    default: 275 d
    required: false
  - name: window_max
    type: duration
    label: Maximum days since subscription started
    default: 365 d
    required: false
  - name: recap_sentences
    type: number
    label: Number of sentences in the value recap
    default: 3
    required: false
  - name: recap_tone
    type: string
    label: Tone of the value recap
    default: warm and appreciative
    required: false
  - name: call_booking_link_label
    type: string
    label: Button label for the call booking
    default: Book a call with your account manager
    required: false
  requirements:
  - slot: paying_user_plan
    kind: attribute
    meaning: The plan a user is on, used to exclude free-plan users
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
  - slot: renewals_team_list
    kind: destination
    meaning: Distribution list for the renewals team that receives renewal flags by email
    channel: email
  - slot: user_email
    kind: attribute
    meaning: The email address of a user
  - slot: account_manager_booking_page
    kind: destination
    meaning: Call-booking page where a customer can schedule time with their account manager
    channel: email
  - slot: product_results
    kind: knowledge
    meaning: Record of meaningful results each user has gotten from the product this year
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - paying_user_plan
    - subscription_started
    - plan_excluded
    - window_min
    - window_max
    instruction: 'Build a new segment of users named "Renewal Window 90 Days" who meet all of these conditions: their {paying_user_plan}
      has a value and is not {plan_excluded}, and they did {subscription_started} at least once between {window_min} and {window_max}
      ago.'
  - id: s2
    builds: email_plain
    uses:
    - renewals_team_list
    - user_email
    - s1
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to the {renewals_team_list} distribution list. For each user in the segment
      built in "Build the renewal list", name their {user_email}, so conversations start months early instead of the week
      before. Take names and addresses from the member list in the result of the step that built the list (at most 20, then
      how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text
      only: no HTML tags, no markup and no unsubscribe line.'
  - id: s3
    builds: email
    uses:
    - product_results
    - recap_sentences
    - recap_tone
    - account_manager_booking_page
    - call_booking_link_label
    - s1
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the segment built in "Build the renewal list" recapping
      one meaningful result they have gotten from the product this year, using {product_results}. The email must be {recap_sentences}
      sentences long, in a {recap_tone} tone, with no pricing or discount language. Include one button labeled {call_booking_link_label}
      that links to {account_manager_booking_page}. If the brand kit has no logo, use the brand name as a plain text header.
      Every button links to a URL given for this run or named in this step; never leave a button without a link.
---

# Accounts in the renewal window

Slash command: /renewal-window-90-day

## Step 1: Build the renewal list

Build a new segment of users named "Renewal Window 90 Days" who meet all of these conditions: their paying user plan has a value and is not free, and they did subscription started at least once between 275 d and 365 d ago.

## Step 2: Notify the renewals team

Generate a plain-text email to the renewals team list distribution list. For each user in the segment built in "Build the renewal list", name their user email, so conversations start months early instead of the week before. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.

## Step 3: Send a value recap

Generate a designed marketing email for the users in the segment built in "Build the renewal list" recapping one meaningful result they have gotten from the product this year, using product results. The email must be 3 sentences long, in a warm and appreciative tone, with no pricing or discount language. Include one button labeled Book a call with your account manager that links to account manager booking page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
