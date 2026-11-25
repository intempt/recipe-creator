---
frontmatter_id: active-research-surge-accounts
slash_command: /active-research-surge-accounts
description: Accounts whose users are browsing your site heavily right now, flagged to sales while interest is at its peak and sent a relevant resource to keep them moving.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Flags accounts with a surge of site browsing to sales on Slack and sends them a helpful, low-pressure resource
    email with a call-booking button.
  parameters:
  - name: view_threshold
    type: number
    label: Minimum page views by account users
    default: 3
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window for page views
    default: 7 d
    required: false
  - name: sales_channel
    type: string
    label: Slack sales channel name
    default: sales
    required: false
  - name: email_sentence_count
    type: number
    label: Number of sentences in the email body
    default: 3
    required: false
  - name: email_tone
    type: string
    label: Email tone
    default: helpful and low-pressure
    required: false
  - name: cta_label
    type: string
    label: Button label linking to call booking
    default: Book a call
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the website
  - slot: sales_slack
    kind: integration
    meaning: A Slack workspace connected to post alerts to the sales channel
    channel: slack
  - slot: sales_team_channel
    kind: destination
    meaning: The Slack channel where the sales team receives alerts
    channel: slack
  - slot: account_name
    kind: attribute
    meaning: The name of the account
  - slot: call_booking_page
    kind: knowledge
    meaning: The call-booking page URL that the email button links to
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - view_threshold
    - lookback_window
    instruction: Build a new segment named "Active Research Surge Accounts" of accounts where users together did {page_view_event}
      {view_threshold} or more times in the last {lookback_window}.
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - sales_team_channel
    - account_name
    dependsOn:
    - s1
    instruction: Post a Slack message to {sales_team_channel} for each account in "Active Research Surge Accounts", naming
      the account ({account_name}) so reps can reach out while interest is at its peak. Use the result of "Build the research-surge
      list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then
      how many more); never write a placeholder or ask the reader to paste anything in.
  - id: s3
    builds: email
    uses:
    - s1
    - call_booking_page
    - email_sentence_count
    - email_tone
    - cta_label
    dependsOn:
    - s1
    instruction: Create a designed marketing email for the accounts in "Active Research Surge Accounts" offering a resource
      that answers the questions a researching buyer usually has at this stage. Write {email_sentence_count} sentences in
      a {email_tone} tone with no discount language. Include one button labeled "{cta_label}" linking to {call_booking_page}.
      Use the result of "Build the research-surge list". If the brand kit has no logo, use the brand name as a plain text
      header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
---

# Accounts showing a research surge

Slash command: /active-research-surge-accounts

## Step 1: Build the research-surge list

Build a new segment named "Active Research Surge Accounts" of accounts where users together did page view event 3 or more times in the last 7 d.

## Step 2: Alert sales

Post a Slack message to sales team channel for each account in "Active Research Surge Accounts", naming the account (account name) so reps can reach out while interest is at its peak. Use the result of "Build the research-surge list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.

## Step 3: Send a relevant resource

Create a designed marketing email for the accounts in "Active Research Surge Accounts" offering a resource that answers the questions a researching buyer usually has at this stage. Write 3 sentences in a helpful and low-pressure tone with no discount language. Include one button labeled "Book a call" linking to call booking page. Use the result of "Build the research-surge list". If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
