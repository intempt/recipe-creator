---
frontmatter_id: vip-customers-high-ltv
slash_command: /vip-customers-high-ltv
description: Your highest lifetime value customers who are still active, welcomed into VIP recognition by email and flagged to the concierge team for a personal touch.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Welcomes your highest lifetime value, recently active customers into VIP recognition with a warm email and alerts
    the concierge team to give each a personal welcome.
  parameters:
  - name: ltv_threshold
    type: number
    label: Minimum lifetime value
    default: 1000
  - name: activity_window
    type: duration
    label: Recent activity window
    default: 7 d
  - name: email_tone
    type: string
    label: Email tone
    default: warm and appreciative
  - name: concierge_channel
    type: string
    label: Concierge Slack channel name
    default: concierge team
  requirements:
  - slot: session_start
    kind: event
    meaning: A customer started a session in the app or website
  - slot: lifetime_value
    kind: attribute
    meaning: The total lifetime value a customer has generated
  - slot: customer_email
    kind: attribute
    meaning: The email address of a customer
  - slot: concierge_slack
    kind: integration
    meaning: Slack workspace connection used to post messages to the concierge team channel
    optional: true
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start
    - lifetime_value
    - ltv_threshold
    - activity_window
    instruction: Build a new segment named "VIP Customers" containing users whose {lifetime_value} is {ltv_threshold} or more
      and who did {session_start} at least once in the last {activity_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - email_tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in "VIP Customers" thanking them for their loyalty and
      inviting them into VIP recognition. Write three sentences in a {email_tone} tone with no discount language, and include
      one button linking to the rewards or early-access page. If the brand kit has no logo, use the brand name as a plain
      text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
  - id: s3
    builds: slack
    uses:
    - s1
    - concierge_slack
    - customer_email
    - lifetime_value
    - concierge_channel
    dependsOn:
    - s1
    instruction: Generate a Slack message to the {concierge_channel} channel. For each user in "VIP Customers", name their
      {customer_email} and their {lifetime_value} so the team can give each one a personal welcome into the program. Take
      names and addresses from the member list in the result of the step that built the list (at most 20, then how many more);
      never write a placeholder or ask the reader to paste anything in.
---

# VIP customers

Slash command: /vip-customers-high-ltv

## Step 1: Build the VIP list

Build a new segment named "VIP Customers" containing users whose lifetime value is 1000 or more and who did session start at least once in the last 7 d.

## Step 2: Send a VIP recognition email

Generate a designed marketing email for the users in "VIP Customers" thanking them for their loyalty and inviting them into VIP recognition. Write three sentences in a warm and appreciative tone with no discount language, and include one button linking to the rewards or early-access page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Alert the concierge team

Generate a Slack message to the concierge team channel. For each user in "VIP Customers", name their customer email and their lifetime value so the team can give each one a personal welcome into the program. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.
