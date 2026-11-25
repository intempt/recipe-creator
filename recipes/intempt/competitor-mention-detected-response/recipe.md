---
frontmatter_id: competitor-mention-detected-response
slash_command: /competitor-mention-detected-response
description: Spots paying customers showing competitor interest in first-party events, sends them an honest comparison email,
  alerts the CSM about high-value accounts, shows unused capabilities in the app and emails a weekly competitor digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds paying customers with recent competitor signals, emails them a helpful comparison, alerts CSMs about high-ARR
    accounts and sends a weekly competitor digest.
  parameters:
  - name: signal_window
    type: duration
    label: How recent a competitor signal counts
    default: 14 d
    required: false
  - name: first_response_window
    type: duration
    label: Wait before the comparison email
    default: 4 h
    required: false
  - name: high_arr_threshold
    type: number
    label: Account ARR above which the CSM is alerted
    default: 25000
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the CSM / AE team alerted about high-value accounts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: competitor_signal_event
    kind: event
    meaning: A customer showed competitor interest on a first-party channel, such as visiting a comparison page or clicking
      a competitor-named link
    properties:
    - name: competitor_name
      type: string
      meaning: Name of the competitor
      optional: false
    - name: signal_type
      type: string
      meaning: Kind of signal, such as comparison_page_view or competitor_link_click
      optional: false
    - name: signal_strength
      type: string
      meaning: low, medium or high
      optional: false
  - slot: plan
    kind: attribute
    meaning: The user's current plan, empty or free/trial when not paying
  - slot: cancel_page_visit_event
    kind: event
    meaning: A customer visited the cancellation page of the product
  - slot: account_arr
    kind: attribute
    meaning: Account attribute with annual recurring revenue
  - slot: customer_success_owner
    kind: attribute
    meaning: Name of the CSM or AE assigned to the account
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - competitor_signal_event
    - plan
    - signal_window
    instruction: Build a new segment of users named "Customers with competitor signals". A user is in it when their {plan}
      attribute has a value that is not free or trial and they did {competitor_signal_event} with {competitor_signal_event.signal_strength}
      equal to medium or high in the last {signal_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - competitor_signal_event
    - customer_success_owner
    dependsOn:
    - s1
    instruction: 'Write a designed HTML email for users in the segment from "Group by what they intend", signed with their
      {customer_success_owner}. Subject: "Comparing us with {competitor_signal_event.competitor_name}? Here is an honest view".
      Acknowledge they may be looking around, give a short fair comparison focused on what teams like theirs get from us,
      point to two capabilities they may not use yet, and offer a 20-minute call. Respectful, not defensive, no discounts.'
  - id: s3
    builds: recommendation
    uses:
    - s1
    dependsOn:
    - s1
    instruction: 'Build an in-app product recommendation titled "Capabilities you''re not using yet" for users in the segment
      from "Group by what they intend": recommend the 3 features most used by other paying users on the same plan that this
      user has not used in the last 90 days.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - competitor_signal_event
    - cancel_page_visit_event
    - account_arr
    - customer_success_owner
    - first_response_window
    - high_arr_threshold
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that starts when a user enters the segment from "Group by what they intend". It waits
      {first_response_window} and sends the email from "Write a reply per intent". If the account's {account_arr} is above
      {high_arr_threshold}, or the user did {cancel_page_visit_event} in the last 14 days, it also emails {alert_recipients}
      the user's name, account, {account_arr}, {customer_success_owner}, {competitor_signal_event.competitor_name} and {competitor_signal_event.signal_type}
      so the CSM can reach out.
  - id: s5
    builds: automation
    uses:
    - s1
    - competitor_signal_event
    - account_arr
    - plan
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {competitor_signal_event}
      by paying users in the last 7 days and writes these figures: signal count per {competitor_signal_event.competitor_name},
      with the 7 days before; the number of users in the segment from "Group by what they intend" now; the sum of {account_arr}
      of their accounts; and how many of the users who entered it 30 to 60 days ago now have a {plan} that is empty, free
      or trial. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else
      is sent.'
---

# Competitor signal response

Slash command: /competitor-mention-detected-response

## Step 1: Group by what they intend

Build a new segment of users named "Customers with competitor signals". A user is in it when their plan attribute has a value that is not free or trial and they did competitor signal event with signal strength equal to medium or high in the last 14 d.

## Step 2: Write a reply per intent

Write a designed HTML email for users in the segment from "Group by what they intend", signed with their customer success owner. Subject: "Comparing us with competitor name? Here is an honest view". Acknowledge they may be looking around, give a short fair comparison focused on what teams like theirs get from us, point to two capabilities they may not use yet, and offer a 20-minute call. Respectful, not defensive, no discounts.

## Step 3: Show what they are missing

Build an in-app product recommendation titled "Capabilities you're not using yet" for users in the segment from "Group by what they intend": recommend the 3 features most used by other paying users on the same plan that this user has not used in the last 90 days.

## Step 4: Respond within four hours

Build an automation that starts when a user enters the segment from "Group by what they intend". It waits 4 h and sends the email from "Write a reply per intent". If the account's account arr is above 25000, or the user did cancel page visit event in the last 14 days, it also emails the email addresses of the CSM / AE team alerted about high-value accounts the user's name, account, account arr, customer success owner, competitor name and signal type so the CSM can reach out.

## Step 5: See which rivals you lose to

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes competitor signal event by paying users in the last 7 days and writes these figures: signal count per competitor name, with the 7 days before; the number of users in the segment from "Group by what they intend" now; the sum of account arr of their accounts; and how many of the users who entered it 30 to 60 days ago now have a plan that is empty, free or trial. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
