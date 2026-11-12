---
frontmatter_id: trial-expiring-soon
slash_command: /trial-expiring-soon
description: Trial users who started their trial 3 to 4 weeks ago and still have not paid, nudged by email and flagged to sales while there is still time to close them.
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
  summary: Emails trial users who started 3 to 4 weeks ago and have not paid a warm nearing-end nudge, and alerts sales in
    Slack so reps can reach out before the trial closes.
  parameters:
  - name: trial_min_days
    type: number
    label: 'Trial start window: earliest days ago'
    default: 23
  - name: trial_max_days
    type: number
    label: 'Trial start window: latest days ago'
    default: 30
  - name: plan_value
    type: string
    label: Plan attribute value that marks a trial
    default: trial
  - name: email_tone
    type: string
    label: Email tone
    default: warm and helpful
  - name: email_sentence_count
    type: number
    label: Number of sentences in the email
    default: 3
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
  - slot: plan_attribute
    kind: attribute
    meaning: The plan a user is currently on, such as trial or paid
  - slot: trial_expiring_segment
    kind: segment
    meaning: Users on a trial who started it 23 to 30 days ago and have not paid
    creatable: true
    definition: users whose {plan_attribute} is {plan_value} and who did {subscription_started_event} at least once between
      {trial_min_days} and {trial_max_days} days ago
  - slot: sales_slack
    kind: destination
    meaning: A Slack channel that the sales team reads
    channel: slack
  - slot: upgrade_page
    kind: destination
    meaning: The web page where users can upgrade to a paid plan
    channel: email
  - slot: user_email_attribute
    kind: attribute
    meaning: The email address of a user
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_started_event
    - plan_attribute
    - plan_value
    - trial_min_days
    - trial_max_days
    instruction: Build a segment named "Trial Expiring Soon" of users whose {plan_attribute} is {plan_value} and who did {subscription_started_event}
      at least once between {trial_min_days} and {trial_max_days} days ago.
  - id: s2
    builds: email
    uses:
    - s1
    - upgrade_page
    - email_tone
    - email_sentence_count
    instruction: Generate a designed marketing email for the users in "Trial Expiring Soon" telling them their trial is nearing
      its end and highlighting the one feature most worth trying before it does. Use {email_sentence_count} sentences, a {email_tone}
      tone, no discount language, and one button linking to {upgrade_page}.
  - id: s3
    builds: slack
    uses:
    - s1
    - sales_slack
    - user_email_attribute
    instruction: Generate a Slack message to {sales_slack} that names the email address ({user_email_attribute}) of each user
      in "Trial Expiring Soon", so reps can reach out personally before the window closes.
---

# Trials nearing the end

Slash command: /trial-expiring-soon

## Step 1: Build the expiring-trial list

Build a segment of users named "Trial Expiring Soon".
A user is in the segment only when all of these are true:
- their Plan attribute is "trial"
- they did the Subscription started event at least once between 23 and 30 days ago

## Step 2: Send a final nudge

Generate a designed marketing email for the users in "Trial Expiring Soon" letting them know their trial is nearing its end and highlighting the one feature most worth trying before it does. Three sentences, warm and helpful tone, no discount language, one button linking to the upgrade page. Use the result of "Build the expiring-trial list".

## Step 3: Alert sales

Generate a Slack message to the sales channel For each user in "Trial Expiring Soon", name their email address, so reps can reach out personally before the window closes. Use the result of "Build the expiring-trial list".
