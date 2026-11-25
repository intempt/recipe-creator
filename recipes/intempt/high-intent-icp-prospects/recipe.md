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
  - slot: product_feature_knowledge
    kind: knowledge
    meaning: Product features and their relevance for companies of different sizes
  - slot: call_booking_page
    kind: knowledge
    meaning: Link to the company's call-booking page used as the email button target
  steps:
  - id: s1
    builds: segment
    instruction: 'Build a new segment named "High-Intent ICP Prospects". An account is included only when all of these are
      true: its {account_employees} is {minEmployees} or more; its {account_employees} is less than {maxEmployees}; and the
      users in the account together did {view_page_event} at least once in the last {activityWindow}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - salesChannel
    dependsOn:
    - s1
    instruction: Write a Slack message for the {salesChannel} channel in {sales_slack} for each account in "High-Intent ICP
      Prospects". Name the account and its {account_employees} count so reps can reach out while interest is still warm. Use
      the result of "Build the hot ICP list". Take names and addresses from the member list in the result of the step that
      built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.
  - id: s3
    builds: email
    uses:
    - s1
    - product_feature_knowledge
    - call_booking_page
    - emailTone
    - emailSentenceCount
    dependsOn:
    - s1
    instruction: Create a designed marketing email for the accounts in "High-Intent ICP Prospects" (the segment from "Build
      the hot ICP list") introducing the product feature from {product_feature_knowledge} that is most relevant to a company
      of their size. Write {emailSentenceCount} sentences in a {emailTone} tone with no discount language. Include one button
      linking to {call_booking_page}. Use the result of "Build the hot ICP list". If the brand kit has no logo, use the brand
      name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button
      without a link.
---

# ICP accounts showing intent

Slash command: /high-intent-icp-prospects

## Step 1: Build the hot ICP list

Build a new segment named "High-Intent ICP Prospects". An account is included only when all of these are true: its account employees is 50 or more; its account employees is less than 1000; and the users in the account together did view page event at least once in the last 7 d.

## Step 2: Alert sales

Write a Slack message for the sales channel in sales slack for each account in "High-Intent ICP Prospects". Name the account and its account employees count so reps can reach out while interest is still warm. Use the result of "Build the hot ICP list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.

## Step 3: Send an outreach email

Create a designed marketing email for the accounts in "High-Intent ICP Prospects" (the segment from "Build the hot ICP list") introducing the product feature from product feature knowledge that is most relevant to a company of their size. Write 3 sentences in a confident and consultative tone with no discount language. Include one button linking to call booking page. Use the result of "Build the hot ICP list". If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
