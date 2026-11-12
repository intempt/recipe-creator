---
frontmatter_id: decision-maker-prospects
slash_command: /decision-maker-prospects
description: Customers who have paid for a year or two straight, invited into loyalty recognition by email and flagged to customer marketing for a testimonial or case study.
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
  summary: placeholder
  parameters:
  - name: minDaysSinceSubscribed
    type: duration
    label: Minimum time since subscription started
    default: 365 d
  - name: maxDaysSinceSubscribed
    type: duration
    label: Maximum time since subscription started
    default: 730 d
  - name: excludedPlan
    type: string
    label: Plan value to exclude
    default: free
  - name: emailTone
    type: enum
    label: Email tone
    default: warm
    options:
    - warm
    - formal
    - playful
  - name: emailSentenceCount
    type: number
    label: Number of sentences in email body
    default: 3
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
  - slot: plan_attribute
    kind: attribute
    meaning: The plan a customer is currently on
  - slot: long_time_loyal_customers
    kind: segment
    meaning: Users who are on a paid plan and started a subscription 365 to 730 days ago
    creatable: true
    definition: users whose {plan_attribute} is not {excludedPlan} and who did {subscription_started_event} at least once
      between {minDaysSinceSubscribed} and {maxDaysSinceSubscribed} ago
  - slot: customer_marketing_channel
    kind: integration
    meaning: The Slack channel used by the customer marketing team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - plan_attribute
    - subscription_started_event
    - excludedPlan
    - minDaysSinceSubscribed
    - maxDaysSinceSubscribed
    instruction: Build a segment named "Long-Time Loyal Customers" containing users whose {plan_attribute} is not {excludedPlan}
      and who did {subscription_started_event} at least once between {minDaysSinceSubscribed} and {maxDaysSinceSubscribed}
      ago.
  - id: s2
    builds: email
    uses:
    - s1
    - emailTone
    - emailSentenceCount
    instruction: Generate a designed marketing email for the users in "Long-Time Loyal Customers" thanking them for their
      continued support and inviting them into loyalty recognition. The body is {emailSentenceCount} sentences in a {emailTone}
      and appreciative tone, with no discount language. Include one button linking to the loyalty or referral page.
  - id: s3
    builds: slack
    uses:
    - s1
    - customer_marketing_channel
    instruction: Generate a Slack message to {customer_marketing_channel} that lists the email address of each user in "Long-Time
      Loyal Customers" as candidates for a testimonial or case study.
---

# Long-time loyal customers

Slash command: /decision-maker-prospects

## Step 1: Build the loyal-customer list

Build a segment of users named "Long-Time Loyal Customers".
A user is in the segment only when all of these are true:
- their Plan attribute is not "free"
- they did the Subscription started event at least once between 365 and 730 days ago

## Step 2: Send a loyalty recognition email

Generate a designed marketing email for the users in "Long-Time Loyal Customers" thanking them for their continued support and inviting them into loyalty recognition. Three sentences, warm and appreciative tone, no discount language, one button linking to the loyalty or referral page. Use the result of "Build the loyal-customer list".

## Step 3: Alert customer marketing

Generate a Slack message to the customer marketing channel For each user in "Long-Time Loyal Customers", name their email address, as candidates for a testimonial or case study. Use the result of "Build the loyal-customer list".
