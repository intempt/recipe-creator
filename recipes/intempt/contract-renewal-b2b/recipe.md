---
frontmatter_id: contract-renewal-b2b
slash_command: /contract-renewal-b2b
description: For B2B accounts approaching contract end, emails the champion at 90 days, the economic buyer at 60 days and
  every contact at 30 days, and alerts the team about at-risk renewals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Runs a renewal email sequence at 90, 60 and 30 days before contract end, each to the right contact role, and alerts
    the team about at-risk renewals.
  parameters:
  - name: renewal_window_end
    type: duration
    label: How far ahead the renewal window reaches
    default: 90 d
    required: false
  - name: champion_touch_day
    type: number
    label: Days before contract end for the champion email
    default: 90
    required: false
  - name: economic_buyer_touch_day
    type: number
    label: Days before contract end for the economic buyer email
    default: 60
    required: false
  - name: final_reminder_day
    type: number
    label: Days before contract end for the final reminder
    default: 30
    required: false
  - name: tone
    type: enum
    label: Email tone
    default: business_formal
    required: false
    options:
    - business_formal
    - friendly_professional
  - name: alert_recipients
    type: string
    label: Email addresses of the CSM / AE team alerted about at-risk renewals
    required: true
  requirements:
  - slot: contract_end_date
    kind: attribute
    meaning: Account attribute with the date the account's contract ends
  - slot: account_tier
    kind: attribute
    meaning: Account attribute with the tier, such as enterprise, mid-market or smb
  - slot: subscription_status
    kind: attribute
    meaning: Account attribute with the subscription status, such as active or cancelled
  - slot: contact_role
    kind: attribute
    meaning: 'User attribute with the person''s role on the account: champion, economic_buyer or other'
  - slot: churn_signal
    kind: attribute
    meaning: Account attribute that is true when the account shows a churn risk
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - contract_end_date
    - account_tier
    - subscription_status
    - renewal_window_end
    instruction: Build a new segment of accounts named "Upcoming B2B renewals". An account is in it when its {contract_end_date}
      attribute is between today and {renewal_window_end} from now, its {account_tier} attribute is enterprise or mid-market,
      and its {subscription_status} attribute is active.
  - id: s2
    builds: email
    uses:
    - s1
    - tone
    - champion_touch_day
    dependsOn:
    - s1
    instruction: 'Write a designed HTML email for the champion at accounts in the segment from "Find renewals inside 90 days",
      sent {champion_touch_day} days before contract end. Subject: "A quick recap of the past year". Recap what is working
      and what comes next, and ask them to help line up the renewal conversation. Tone: {tone}, substantive, no pricing or
      discount language.'
  - id: s3
    builds: email
    uses:
    - s1
    - tone
    - economic_buyer_touch_day
    dependsOn:
    - s1
    instruction: 'Write a designed HTML email for the economic buyer at accounts in the segment from "Find renewals inside
      90 days", sent {economic_buyer_touch_day} days before contract end. Subject: "Your renewal is coming up: let''s talk
      terms". Focus on business value and growth opportunity, and offer a 30-minute call to agree renewal terms. Tone: {tone},
      no prices or discounts.'
  - id: s4
    builds: email
    uses:
    - s1
    - tone
    - final_reminder_day
    dependsOn:
    - s1
    instruction: 'Write a designed HTML email for every contact at accounts in the segment from "Find renewals inside 90 days",
      sent {final_reminder_day} days before contract end. A short, clear reminder that the contract ends soon, with one button
      to book the renewal call. Tone: {tone}, no prices or discounts.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - contract_end_date
    - contact_role
    - churn_signal
    - champion_touch_day
    - economic_buyer_touch_day
    - final_reminder_day
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation that runs every day at 09:00 on a schedule over the users of accounts in the segment
      from "Find renewals inside 90 days". When the account's {contract_end_date} is exactly {champion_touch_day} days away,
      it sends the email from "Write the champion value recap" to users whose {contact_role} is champion, and if the account's
      {churn_signal} is true it emails {alert_recipients} the account name and contract end date. When it is exactly {economic_buyer_touch_day}
      days away, it sends the email from "Write the economic buyer note" to users whose {contact_role} is economic_buyer.
      When it is exactly {final_reminder_day} days away, it sends the email from "Write the final renewal reminder" to every
      user of the account.
---

# B2B contract renewal

Slash command: /contract-renewal-b2b

## Step 1: Find renewals inside 90 days

Build a new segment of accounts named "Upcoming B2B renewals". An account is in it when its contract end date attribute is between today and 90 d from now, its account tier attribute is enterprise or mid-market, and its subscription status attribute is active.

## Step 2: Write the champion value recap

Write a designed HTML email for the champion at accounts in the segment from "Find renewals inside 90 days", sent 90 days before contract end. Subject: "A quick recap of the past year". Recap what is working and what comes next, and ask them to help line up the renewal conversation. Tone: business_formal, substantive, no pricing or discount language.

## Step 3: Write the economic buyer note

Write a designed HTML email for the economic buyer at accounts in the segment from "Find renewals inside 90 days", sent 60 days before contract end. Subject: "Your renewal is coming up: let's talk terms". Focus on business value and growth opportunity, and offer a 30-minute call to agree renewal terms. Tone: business_formal, no prices or discounts.

## Step 4: Write the final renewal reminder

Write a designed HTML email for every contact at accounts in the segment from "Find renewals inside 90 days", sent 30 days before contract end. A short, clear reminder that the contract ends soon, with one button to book the renewal call. Tone: business_formal, no prices or discounts.

## Step 5: Reach each stakeholder in turn

Build an automation that runs every day at 09:00 on a schedule over the users of accounts in the segment from "Find renewals inside 90 days". When the account's contract end date is exactly 90 days away, it sends the email from "Write the champion value recap" to users whose contact role is champion, and if the account's churn signal is true it emails the email addresses of the CSM / AE team alerted about at-risk renewals the account name and contract end date. When it is exactly 60 days away, it sends the email from "Write the economic buyer note" to users whose contact role is economic_buyer. When it is exactly 30 days away, it sends the email from "Write the final renewal reminder" to every user of the account.
