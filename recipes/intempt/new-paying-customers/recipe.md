---
frontmatter_id: new-paying-customers
slash_command: /new-paying-customers
description: Customers who started paying in the last month, welcomed by email and flagged to customer success during the window where onboarding decides whether they stay.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Welcomes new paying customers by email with one feature to try in their first week, and alerts customer success
    to check in personally.
  parameters:
  - name: lookback_window
    type: duration
    label: Lookback window for new subscriptions
    default: 30 d
    required: false
  - name: excluded_plans
    type: text
    label: Plan values excluded from the segment
    default: free, trial
    required: false
  - name: welcome_tone
    type: string
    label: Tone of the welcome email
    default: warm
    required: false
  - name: welcome_sentence_count
    type: number
    label: Number of sentences in the welcome email
    default: 3
    required: false
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
  - slot: plan_attribute
    kind: attribute
    meaning: The plan a customer is currently on (for example free, trial, or a paid plan)
  - slot: customer_success_team
    kind: destination
    meaning: The customer success distribution list that receives notifications about new paying customers
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_started_event
    - plan_attribute
    - lookback_window
    instruction: Build a segment of users named "New Paying Customers" containing users who performed {subscription_started_event}
      at least once in the last {lookback_window}, whose {plan_attribute} is not "free", and whose {plan_attribute} is not
      "trial".
  - id: s2
    builds: email
    uses:
    - s1
    - welcome_sentence_count
    instruction: Generate a designed marketing email for the users in the "New Paying Customers" segment. Welcome them warmly
      in {welcome_sentence_count} sentences and highlight one feature worth trying in their first week. Use no upsell language.
      Include one button linking to that feature inside the product.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - customer_success_team
    instruction: Generate a plain-text email to {customer_success_team}. For each user in the "New Paying Customers" segment,
      list their email address so the team can check in personally during their first week. Use the result of "Build the new-customer
      list".
---

# New paying customers

Slash command: /new-paying-customers

## Step 1: Build the new-customer list

Build a segment of users named "New Paying Customers".
A user is in the segment only when all of these are true:
- they did the Subscription started event at least once in the last 30 days
- their Plan attribute is not "free"
- their Plan attribute is not "trial"

## Step 2: Send a welcome email

Generate a designed marketing email for the users in "New Paying Customers" welcoming them and highlighting one feature worth trying in their first week. Three sentences, warm tone, no upsell language, one button linking to that feature inside the product. Use the result of "Build the new-customer list".

## Step 3: Notify customer success

Generate a plain-text email to the customer success distribution list For each user in "New Paying Customers", name their email address, so the team can check in personally during their first week. Use the result of "Build the new-customer list".
