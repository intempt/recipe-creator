---
frontmatter_id: trial-expiring-soon
slash_command: /trial-expiring-soon
description: Trial users whose trial ends within the next week and still have not paid, nudged by email and flagged to sales while there is still time to close them.
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
  summary: Emails trial users whose trial ends within the next week and have not paid a warm nearing-end nudge, and alerts
    sales in Slack so reps can reach out before the trial closes.
  parameters:
  - name: days_before_end
    type: number
    label: Days before the trial ends
    default: 7
  - name: trial_length_days
    type: number
    label: Trial length in days, used only when the trial start event has no end date
    default: 14
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
  - slot: trial_started_event
    kind: event
    meaning: A user started a trial (the event carries the trial's end date and its length in days)
  - slot: plan_attribute
    kind: attribute
    meaning: The plan a user is currently on, such as trial or paid
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
    - trial_started_event
    - plan_attribute
    - plan_value
    - days_before_end
    - trial_length_days
    instruction: 'Build a new segment named "Trial Expiring Soon" of users who are still on their trial and not yet paying
      (never people who already converted): their {plan_attribute} is {plan_value}, and the trial end date on their {trial_started_event}
      falls within the next {days_before_end} days. If that event has no trial end date, use people who did {trial_started_event}
      between ({trial_length_days} minus {days_before_end}) and {trial_length_days} days ago, and say that basis.'
  - id: s2
    builds: email
    uses:
    - s1
    - upgrade_page
    - email_tone
    - email_sentence_count
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in "Trial Expiring Soon" telling them their trial is nearing
      its end and highlighting the one feature most worth trying before it does. Use {email_sentence_count} sentences, a {email_tone}
      tone, no discount language, and one button linking to {upgrade_page}. If the brand kit has no logo, use the brand name
      as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without
      a link.
  - id: s3
    builds: slack
    uses:
    - s1
    - sales_slack
    - user_email_attribute
    dependsOn:
    - s1
    instruction: Generate a Slack message to {sales_slack} that names the email address ({user_email_attribute}) of each user
      in "Trial Expiring Soon", so reps can reach out personally before the window closes.
---

# Trials nearing the end

Slash command: /trial-expiring-soon

## Step 1: Build the expiring-trial list

Build a new segment named "Trial Expiring Soon" of users who are still on their trial and not yet paying (never people who already converted): their plan attribute is trial, and the trial end date on their trial started event falls within the next 7 days. If that event has no trial end date, use people who did trial started event between (14 minus 7) and 14 days ago, and say that basis.

## Step 2: Send a final nudge

Generate a designed marketing email for the users in "Trial Expiring Soon" telling them their trial is nearing its end and highlighting the one feature most worth trying before it does. Use 3 sentences, a warm and helpful tone, no discount language, and one button linking to upgrade page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Alert sales

Generate a Slack message to sales slack that names the email address (user email attribute) of each user in "Trial Expiring Soon", so reps can reach out personally before the window closes.
