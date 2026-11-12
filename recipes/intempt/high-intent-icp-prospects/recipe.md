---
frontmatter_id: high-intent-icp-prospects
slash_command: /high-intent-icp-prospects
description: ICP-sized accounts with recent activity on your site, flagged to sales and sent an outreach email while interest is still warm.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Flags ICP-sized accounts with recent site activity to sales in Slack and sends them a short, consultative outreach
    email while interest is still warm.
  parameters:
  - name: minEmployees
    type: number
    label: Minimum employees in account
    default: 50
    required: false
  - name: maxEmployees
    type: number
    label: Maximum employees in account (exclusive)
    default: 1000
    required: false
  - name: activityWindow
    type: duration
    label: Activity lookback window
    default: 7 d
    required: false
  - name: salesChannel
    type: text
    label: Sales Slack channel
    default: sales
    required: false
  - name: emailTone
    type: enum
    label: Outreach email tone
    default: confident and consultative
    required: false
    options:
    - confident and consultative
    - friendly and casual
    - formal
  - name: emailSentenceCount
    type: number
    label: Outreach email sentence count
    default: 3
    required: false
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at a customer's account (company)
  - slot: view_page_event
    kind: event
    meaning: A user viewed a page on the website
    properties:
    - name: page
      type: text
      meaning: The page that was viewed
      optional: true
  - slot: sales_slack
    kind: integration
    meaning: Slack workspace connected for posting alerts to the sales channel
    channel: slack
  - slot: outreach_email_destination
    kind: destination
    meaning: Email sending capability for outreach emails to accounts
    channel: email
  - slot: product_feature_knowledge
    kind: knowledge
    meaning: Product features and their relevance for companies of different sizes
  - slot: call_booking_page
    kind: knowledge
    meaning: Link to the company's call-booking page used as the email button target
  - slot: high_intent_icp_prospects
    kind: segment
    meaning: Accounts that are ICP-sized and showed recent site activity
    creatable: true
    definition: accounts where {account_employees} is at least {minEmployees} and less than {maxEmployees}, and the users
      in the account together did {view_page_event} at least once in the last {activityWindow}
  steps:
  - id: s1
    builds: segment
    instruction: 'Build a segment named "High-Intent ICP Prospects" ({high_intent_icp_prospects}). An account is included
      only when all of these are true: its {account_employees} is {minEmployees} or more; its {account_employees} is less
      than {maxEmployees}; and the users in the account together did {view_page_event} at least once in the last {activityWindow}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - high_intent_icp_prospects
    - salesChannel
    instruction: Post a Slack message to the {salesChannel} channel in {sales_slack} for each account in "High-Intent ICP
      Prospects". Name the account and its {account_employees} count so reps can reach out while interest is still warm. Use
      the result of "Build the hot ICP list".
  - id: s3
    builds: email
    uses:
    - s1
    - outreach_email_destination
    - product_feature_knowledge
    - call_booking_page
    - high_intent_icp_prospects
    - emailTone
    - emailSentenceCount
    instruction: Create a designed marketing email for the accounts in "High-Intent ICP Prospects" ({high_intent_icp_prospects})
      introducing the product feature from {product_feature_knowledge} that is most relevant to a company of their size. Write
      {emailSentenceCount} sentences in a {emailTone} tone with no discount language. Include one button linking to {call_booking_page}.
      Send through {outreach_email_destination}. Use the result of "Build the hot ICP list".
---

# ICP accounts showing intent

Slash command: /high-intent-icp-prospects

## Step 1: Build the hot ICP list

Build a segment of accounts named "High-Intent ICP Prospects".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- its employees attribute is less than 1000
- the users in the account together did the View page event at least once in the last 7 days

## Step 2: Alert sales

Generate a Slack message to the sales channel For each account in "High-Intent ICP Prospects", name the account and its employees count, so reps can reach out while interest is still warm. Use the result of "Build the hot ICP list".

## Step 3: Send an outreach email

Generate a designed marketing email for the accounts in "High-Intent ICP Prospects" introducing the product's most relevant feature for a company of their size. Three sentences, confident and consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the hot ICP list".
